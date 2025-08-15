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

_**The whole addressable memory is not managed with stack. There are multiple techniques for multiple purposes.**_

## How stack managed memory?

## What are some places where stack is irreplaceable?

This section would effectively explore what the stack actually has to offer.

### Argument Management In Variable Length Functions

Functions like `printf` expect multiple arguments. Managing the state of those arguments is a pain if you don't use stack.

If you use stack, its fairly straight forward.

### Nested /Function Calls

If you want to explore how functions exist at low level, you can checkout these two articles:

1. [functions-in-assembly.md](functions-in-assembly.md "mention")
2. [special-case-of-functions-recursion.md](special-case-of-functions-recursion.md "mention")

In simple words, a function manages a lot of things.

1. Local variables.
2. Global variables.
3. Function arguments.
4. Return context.

Managing all of this is a cakewalk with stack. It is still not easy, but provided that it is the easiest when stack is used, we can safely say stack is irreplaceable when the talk is about managing function calls.&#x20;







Advantages

Limitations

Shortcomings
