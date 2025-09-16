# Structure Of A Chunk

_**16 September 2025**_

***

We'll start by understanding the structure of a chunk. This is how a chunk looks like:

```c
struct malloc_chunk {
  size_t prev_foot;
  size_t head;
  struct malloc_chunk* fd;
  struct malloc_chunk* bk;
};
```

A chunk is just a piece of metadata.

## What is size\_t?

`size_t` is an unsigned integer type defined by the C standard, which is guaranteed to be able to hold the size (in bytes) of the largest possible object (word size) in the architecture we are in.

At the end of the day, `size_t` is just a type definition alias for some unsigned integer type. In that case, why don't we just use that instead? What's the need for `size_t` ?

Every major kernel like Windows, Unix and Linux has a different ABI. Then there are platform specific ABIs. What looks easy outside is not really that simple inside.

Leave the topic of ABIs for a second. We have multiple implementations of integer itself. Just open `stdint.h` . But when you malloc for any kind, it just works.

Despite all these differences which we can't comprehend as beginners, we still use the same `malloc()` on Windows, Linux and anywhere else. How is that made possible?

We use the same frontend but beneath that lies the complexity to keep malloc as one single frontend instead of

```
mallocWin32(); mallocWin64()
mallocUnix32(); mallocUnix64() and so on.
```

So, we hide all that complication programmatically. The toolchain decides the most appropriate value and make it `size_t` so that we as programmers have no difficulty working across different systems.

That's why when we are at 32-bit system, the size of a chunk becomes 16 bytes. And when we are at 64-bit system, it becomes 32 bytes automatically without any extra lines.

***

## The Confusion Of Size

When we see a chunk as a struct, it's literal size is always going to 16/32 bytes on 32-bit/64-bit. But when we talk about chunk as an allocation medium, it includes the size of both the chunk (as a metadata keeper) and the raw memory location to which a pointer is returned to the process.

And this size is stored within the `head` declaration in the chunk itself.

You might be wondering where is the actual memory location. And it's right to feel perplexed about it.

* What happens is that for every allocation, first comes a metadata chunk, followed by the actual memory location to which a pointer is returned to the process.
*   So for every allocation, it is more like:

    ```
    ┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
    | pf | he | fd | bk | p. |    |    |    |    |    | .p | // | // | // | // | // |
    └────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
    ```
* Remember, pointer `p` is not a part of the struct. And this is very loosely represented which we will try to manage with more realism later.

***

That means, every malloc request creates a chunk, where a chunk literally is just a metadata struct followed by the actual raw memory, but logically we consider them together.

## size\_t head

Let's talk about this declaration within the struct first because this probably the only declaration which is present both in free chunks and in-use chunks.

As `head` is of type `size_t` it will be 4 bytes on 32-bit and 8 bytes on 64-bit. So, size is sorted, I guess.

We need to do 2 things.

1. We know that a free chunk must be surrounded by in-use chunks only. This is only possible when you coalesce adjacent free chunks. To do that, we need to know whether the adjacent chunk is free or in-use.
2. We also need to identify whether the current chunk is free or in-use.

And we do that using flags bits. These are `PINUSE` and `CINUSE` bits.

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
* The largest primitive data type in any architecture is double, which basically means a double-word type. If the chunk is only word-aligned, any double word request would mess up the whole calculation of the CPU.
* To keep things consistent and ensure that memory access for every type is managed efficiently, dlmalloc uses double-word aligned chunks.

Double-word aligned means 8 bytes on 32-bit and 16-bytes on 64-bit.

* Any number which is a multiple of 8 or 16 is not going to use the lower 3 bits, i.e 0, 1, 2. These bits are always going to be free. _You can do the math if unsure._
* So, why don't we use them to mask `pinuse` and `cinuse`? The third bit is not used by dlmalloc but ptmalloc uses it.

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

If something still feels off, remember that rule, _memory interpretation is context dependent. The same group of 8 bits can be interpreted as an unsigned int, a signed int, an ASCII character, or maybe an emoji. So, bit masking doesn't looses the original size. It just utilizes the bits which have become null function under the "alignment rule" situation._

## size\_t prev\_foot

Remember the `pinuse` bit?

* When it is 0, `prev_foot` stores the size of the previous free chunk.
* When it is 1, `prev_foot` is not managed.

## \*fd and \*bd

These are only used by free chunks. They help us traverse forward and backward in the bin they are associated with.

## Final Looks

### In-use Chunk

```c
struct malloc_chunk {
  size_t prev_foot = "DEPENDS ON PINUSE BIT";
  size_t head = "8/16 + REQUESTED_BYTES + DWORD_PADDING";
    CINUSE=1;
    PINUSE="DEPENDS";
  struct malloc_chunk* fd = GARBAGE;
  struct malloc_chunk* bk = GARBAGE;
};
```

### Free Chunk

```c
struct malloc_chunk {
  size_t prev_foot = "DEPENDS ON PINUSE BIT";
  size_t head = "8/16 + REQUESTED_BYTES + DWORD_PADDING";
    CINUSE=0;
    PINUSE="DEPENDS";
  struct malloc_chunk* fd = "NEXT FREE CHUNK IN THE BIN";
  struct malloc_chunk* bk = "PREVIOUS FREE CHUNK IN THE BIN";
};
```

## Conclusion

`size_t` is the real MVP as it helps in making your code platform independent.

Everything is confusing until you don't understand it. Chunks is one of those things.

Next we have to understand binning and how chunks are managed. Questions like:

1. How a free chunk is associated to a bin?
2. What about coalesced free chunks?

can be answered only when we understand binning. And that's going to be our next exploration.

Until then, goodbye.
