# Stack

## The basic idea behind stack

We know that memory is a flat-array at low level. Stack approaches that memory sequentially.

Stack a memory management technique works exactly how a stack of plates work.

* The first plate is the bottom plate and every other plate comes above it.
* The last plate is the top one.
* When we take out plates, it happens from the top, not bottom.

## Why the stack grows downward?

We know that the virtual address space is divided among user space and kernel space and the top of the user space is reserved for stack.

The notion that stack grows downwards comes from the fact that it is located at the top of the user space. It can't grow in upward direction. So it grows downwards.

* When we push something, the stack grows downward. Meaning, a push operation reduces the value of top pointer's address.
* When we pop something, the stack reclaims its space and moves upward. Meaning, a pop operation increments the value of the top pointer's address.

This increment/decrement of address value might sound counter-intuitive, and maybe it is, but it doesn't take much time to get used to it. What's important is that the idea itself is not violated, just the implement differs.

And if you flip the address space, you get an upward growing stack. But the addresses still move in the same fashion.

***

_**The whole addressable memory is not managed with the idea stack. There are multiple techniques for multiple purposes.**_

## What are some places where stack is irreplaceable?

This section would effectively explore what the stack actually has to offer.

### Argument Management In Variable Length Functions

Functions like `printf` expect multiple arguments. Stack can do this flawlessly.&#x20;

### Nested / Recursive Function Calls

If you want to explore how functions exist at low level and how recursion is managed at low level, you can checkout these two articles:

1. [functions-in-assembly.md](../understanding-x64-assembly/functions-in-assembly.md "mention")
2. [special-case-of-functions-recursion.md](../understanding-x64-assembly/special-case-of-functions-recursion.md "mention")









Advantages

Limitations

Shortcomings
