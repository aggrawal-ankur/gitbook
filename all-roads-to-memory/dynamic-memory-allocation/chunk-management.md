# Chunk Management

_**16 September 2025**_

***

We'll start by understanding the structure of a chunk.

## Structure Of A Chunk

In-use chunk and free chunk both have a different structure because of different needs. But the idea remains the same.

A chunk is made up of a header and a payload.

* The header stores metadata about the chunk.
* Payload is where the actual data goes to.

Depending on the type of chunk, these header and payloads take different shapes.

### Size Field

The first thing that goes in the header is the size of the whole chunk, which includes both the header and the payload.

The size of the header is dependent on the size of its contents, and the size of its contents is architecture-dependent.

dlmalloc doesn't use unsigned ints, it uses `size_t`, which refers to the largest size the architecture can manage. Internally it is an unsigned int of some kind.

If you run this simple program:

```c
#include<stdio.h>
#include<stddef.h>

int main(void){
  int x = (sizeof(size_t));
  printf("Bytes = %d\n", x);
  printf("Bits = %d\n", x << 3);
}
```

You will get 8 as bytes and 64 as bits by default as every system is 64-bit today.

However, if you compile this program for a 32-bit system, which you can do that by installing libraries for 32-bit, you'll have a different output. For example, on Debian you can do this:

```bash
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install build-essential gcc-multilib g++-multilib
```

and compile using the `-m32` option, you will have 4 and 32 in output.

Therefore, on 32-bit systems, the size of the `size` field is 4 bytes and on 64-bit systems, it is 8 bytes. However, the whole size field is not used to represent size. Why? Explained below.

***

We know that a free chunk must be surrounded by in-use chunks only. This is only possible when you coalesce adjacent free chunk. To coalesce adjacent free chunks, you need to know whether the adjacent chunk is free or in-use.

We also need to identify whether the current chunk is free or in-use.

For these two purposes, we use flags bits. These are `PINUSE` and `CINUSE` bits.

The `PINUSE` bit is for "_previous chunk type_".

* 0 ⇒ previous chunk is free.
* 1 ⇒ previous chunk is in-use.

The `CINUSE` bit is for "_current chunk type_".

* 0 ⇒ current chunk is free.
* 1 ⇒ current chunk is in-use.

There are two ways to store these bits. Either we allocate separate ints for both, which would waste memory, or we use bit masking. And dlmalloc uses bit masking.

You may ask, _wouldn't that mess with the original size?_ No it won't.

* Remember the stack pointer has to be double word aligned (16 for 64-bits and 8 for 32-bits) because there are SIMD instructions which expects that? A similar story is repeated here as well.
* _**The total size of the chunk has to be double-word aligned.**_
* The largest primitive data type in any architecture is double, which basically means a double-word type. Integer is considered word aligned in the default case.
* If the chunk is only word-aligned, any double word request would mess up the whole calculation of the CPU. To keep things consistent and ensure that memory access for every type is managed efficiently, dlmalloc uses double-word aligned chunks.

Double-word aligned means 8 bytes on 32-bit and 16-bytes on 64-bit.

* Anything that stands on a base of 8 is going to be a multiple of 8. Take 24 and 96.
* Anything that stands on a base of 16 is going to be a multiple of 16. Take 32 and 48.
* Any number that is a multiple of 8 or 16 is not going to use the lower 3 bits, i.e 0, 1, 2. These bits are always going to be free.
* So, why don't we use them to mask `pinuse` and `cinuse`? The third bit is not used by dlmalloc but ptmalloc uses it. It might be used for indicating whether the chunk belongs to mmap or heap. But it doesn't concern us for the time being.

To retrieve the `cinuse` bit:

```
size_field & 0x1
```

To retrieve the `pinuse` bit:

```
size_field & 0x2
```

To retrieve the size, clear the lower 3 bits.

```
size_field & ~0x7
```

If something still feels off, remember that rule, _memory interpretation is context dependent. The same group of 8 bits can be interpreted as an unsigned int, a signed int, an ASCII character, maybe an emoji. So, bit masking doesn't looses the original size. It just utilizes the bits which have become null function under the "alignment rule" situation._

