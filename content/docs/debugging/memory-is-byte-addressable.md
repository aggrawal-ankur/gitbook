---
title: Memory Is Byte Addressable
weight: 6
---

_**26 September 2025**_

***

The first idea that we are going to verify is:

&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "_memory is a flat array of byte addressable blocks_".

## Setup

Take this program.

```c {filename=main.c}
#include <stdio.h>

int main() {
  int x = 0x12345678;
  return 0;
}
```

The variable `x` is of size 32-bits (or 4 bytes) and it is storing a hexadecimal value.

0x12345678 = 305419896

---

Compile with debug information:

```bash
gcc -g main.c -o binary
```

Open inside gdb.

```
$ gdb ./binary
(gdb)
```

Clear the window with `CTRL+L` . And we are done with the setup.

## The "examine" Command

GDB allows us to inspect memory locations via the "examine" command. 

The "examine" command is used to inspect "a piece of memory starting from an address".

It can be invoked by lowercase "x".

We can open its help page as:
```
(gdb) help x
```

The examine command has the following syntax:
```
(gdb) x/FORMAT ADDRESS
```

- FORMAT specifies how we want to inspect memory.
- ADDRESS refers to the memory location we want to inspect.

### The FORMAT Argument

It is made up of three arguments.

The third argument specifies how much memory we want to inspect starting from the ADDRESS argument.

| Valid Values | Description |
| :--- | :--- |
| b (byte) | Inspect "one block" of memory from the starting ADDRESS. |
| h (halfword) | Inspect "two blocks" of memory from the starting ADDRESS. |
| w (word) | Inspect "four blocks" of memory from the starting ADDRESS. |
| g (giant) | Inspect "eight blocks" of memory from the starting ADDRESS. |

---

The second argument in FORMAT specifies "how to interpret the value at that memory location".
- Remember the rule we have studied during assembly, "context decides interpretation, and interpretation decides the meaning of the binary stream obtained at a memory location".

| Valid Values | Description |
| :--- | :--- |
| t (binary)  | Interpret the value as literal binary stream. |
| o (octal)   | Interpret the value as octal. |
| d (decimal) | Interpret the value as decimal. |
| x (hexadecimal) | Interpret the value as hexadecimal. |
| u (unsigned decimal) | Interpret the value as an unsigned decimal. |
| f (float)   | Interpret the value as a float. |
| a (address) | Interpret the value as an address. |
| i (instruction) | Interpret the value as a machine instruction. |
| c (char)    | Interpret the value as a char. |
| s (string)  | Interpret the value as a string. |
| z (hex, zero padded on the left) | Interpret the value as a full 8-byte hex and left pad zero when require. |

---

The first argument in FORMAT specifies how many times we want to repeat the act of "memory inspection".

That's all we need to understand about the "examine" command.

## Let's "examine"

Create a breakpoint at `main`.
```bash
(gdb) break main
Breakpoint 1 at 0x112d: file main.c, line 4.
```

Run the program.
```bash
(gdb) run

Starting program: /home/username/Desktop/RE/out 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

Breakpoint 1, main () at main.c:4
4         int x = 0x12345678;
```

We know that `main` is just a procedure, so when we set a breakpoint on `main`, the breakpoint would be inside the `main` procedure.

In terms of C, the execution is stopped at the "C instruction" which is about to reserve a memory for the "variable x".

In terms of assembly, which is a close representation of machine instructions, "not exact", `main` is a leaf function. So, no need to subtract bytes on the stack as the ABI (System V on Linux 64) guarantees to provide 128 bytes of unused memory.
- That means, we would have only one instruction which subtracts `rbp` to reserve space for the "variable x" on stack. We can verify that on godbolt.org as well.
- So in terms of x64 assembly, the execution is stopped right at the instruction which is to reserve memory for the "variable x", which would be somthing like this:
  ```asm
  mov DWORD PTR [rbp-4], 305419896
  ```
  Remember, this is a 32-bit value, so we are using a double word pointer, where DWORD means 32-bits in terms of x64 assembly.

---

Run this instruction so that memory is reserved for our variable.
```bash
(gdb) next
5         return 0;
```

Lets examine the memory location now.

### print Command

"Examine" is for granular access to memory, so using it first might look like we are manipulating facts. That's why we are using `print` which has no shenanigans.
```bash
(gdb) print x
$1 = 305419896
```

This shows that memory is allocated correctly.
  - **Note: print defaults to decimal.**

To get the address of `x`:
```bash
(gdb) print &x
$2 = (int *) 0x7fffffffdc4c
```
- This shows that `x` is just an integer pointer to a memory location 0x7fffffffdc4c.

Now we can use "examine".

### "examine x"

Examine provides multiple ways to access memory and this feature of it will prove that memory is byte addressable and when you store any arbitrary integer of any predefined size, it is distributed evenly on those byte addressable locations and it is the interpretation part that makes it a number.

According to the theory we have studied, 0x12345678 as a 32-bit integer would look like `00010010001101000101011001111000` in binary. Let's verify.

- We have to interpret the "value at memory" as binary, so we will use `t`.
- Since it is a 32-bit value, we need to explore 32-bits in total.
- 32-bits are basically 4-bytes. So we have to explore 4 bytes.
- When we are exploring "bytes", we use `b` as the size. Since we are exploring 4-bytes, 4 is the number of times we want "examine" to examine the memory starting from 0x7fffffffdc4c.

With that in mind, our command would be:

```bash
(gdb) x/4tb 0x7fffffffdc4c

0x7fffffffdc4c: 01111000        01010110        00110100        00010010
```

If we make pairs of 8 in the above mentioned binary representation of 0x12345678, we get:
```
00010010 00110100 01010110 01111000
```

Since computers store and access memory in little-endian, because that is more efficient to them, but we see values in big-endian, lets reverse the order of pairs we have created.
```
01111000 01010110 00110100 00010010
```

Matching it with the output of gdb, its the same.

If the memory was laid differently, how is it possible that exploring four consecutive byte addressable locations gave us the exact binary stream for 0x12345678 ?

Still not convincing enough? Let's "examine" a little more.

---

32-bits of 4-bytes is basically a "word" for gdb, so `x/1bw` should also work?
```bash
(gdb) x/1bw &x

0x7fffffffdc4c: 00010010001101000101011001111000
```
- Again, the same thing.
- We changed the "rules of interpretation", but the value remained the same. This is possible only when the memory is laid integrally.

---

Take this:
```bash
(gdb) x/1xw &x

0x7fffffffdc4c: 0x12345678
```

Now, lets explore this byte-by-byte.
```bash
(gdb) x/4xb &x

0x7fffffffdc4c: 0x78    0x56    0x34    0x12
```

Want to go even further?
```bash
(gdb) x/1xb 0x7fffffffdc4c
0x7fffffffdc4c: 0x78

(gdb) x/1xb 0x7fffffffdc4c+1
0x7fffffffdc4d: 0x56

(gdb) x/1xb 0x7fffffffdc4c+2
0x7fffffffdc4e: 0x34

(gdb) x/1xb 0x7fffffffdc4c+3
0x7fffffffdc4f: 0x12
```
- All these address are 1 byte apart (4c:76, 4d:77, 4e:78, 4f:79).
- If the memory is not byte addressable, how incrementing by 1 is providing the next part of the value?

This proves that memory indeed is a flat-array of byte addressable blocks and the illusion of data types is created by splitting the binary stream for that data into chunks of 8 and interpretation rules ensures management on the human side.

## Conclusion