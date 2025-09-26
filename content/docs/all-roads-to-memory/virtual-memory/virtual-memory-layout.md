---
title: Virtual Memory Layout
weight: 3
---

_**August 12, 2025**_

***

## Big Picture

```
High Address
                    Top Of Virtual Address Space

0xFFFFFFFFFFFFFFFF *-----------------------------* End Of Kernel Space ↓
                   |                             |
                   |        Kernel Space         |
                   |                             |
                   |       Size: ~128 TiB        |
                   |                             |
                   |         Upper Half          |
                   |                             |
0xFFFF800000000000 *-----------------------------* Start Of Kernel Space ↑
                   |                             |
                   |    Unused / Guard Space     |
                   |                             |
0x0000800000000000 *-----------------------------* End of User Space ↓
                   |                             |
                   |         User Space          |
                   |                             |
                   |       Size: ~128 TiB        |
                   |                             |
                   |         Lower Half          |
                   |                             |
0x0000000000400000 *-----------------------------* Start Of User Space ↑
                   |                             |
                   |     Reserved / Unmapped     |
                   |                             |
0x0000000000000000 *-----------------------------*

                   Bottom Of Virtual Address Space
Low Address
```

## User Space Layout

```
0x0000800000000000 *-----------------------------* End of User Space ↓
                   |    Stack (grows downward)   |
                   *-----------------------------*
                   |    Memory-Mapped Region     |
                   |  (shared libs, mmap, ....)  |
                   *-----------------------------*
                   |     Heap (grows upward)     |
                   *-----------------------------*
                   |  Static && Global Variables |
                   |       (.bss / .data)        |
                   *-----------------------------*
                   |            .text            |
0x0000000000400000 *-----------------------------* Start Of User Space ↑
```

`.data` and `.bss` are packed together because they are functionally the same thing, just differ in initialization.

### What are stack and heap really?

In simple words, stack and heap are two approaches to manage memory. There are no specialized regions either in the physical memory which refer to stack or heap. They are just two ways to manage the same flat memory.

### Why the stack grows downward?

When we learn stack as a data structure, we imagine it as a stack of plates. A stack of anything starts from bottom and approaches sky as the top.

But, when you learn assembly, you find that stack grows downward. And you keep scratching your head. I was no different.

There is a simple solution to this problem. **Reverse the address space.**

* Right now we are looking from top to bottom or higher addresses to lower addresses.
* Just flip the structure and you get an upward growing stack.
* Just remember that this doesn't change the address management of stack. A push would still reduce the memory address mathematically and a pop would increase it. But, at least it solves the mental overhead of imagining stack growing downwards.

***

Apart from this, there is a genuine question that why stack was put at the top of the user space. The reason that they shouldn't collide is not applicable as the memory-mapped region will always come in-between.

As of now, I don't have any answer, but if I find anything interesting, I will update this block.

***

### Why the stack is fast and heap is slow?

This question is not completely answerable as it is based on comparison.

We can explore why stack is fast because we are familiar with it. But we don't know what heap is.

Although we know why stack is fast because it is based on sequential allocation. But what makes heap slow is not known.

When we will explore dynamic memory allocation, it will become clear why stack is fast and heap is slow.

***

Until then, we are now prepared to understand how all of this fits in the grand scheme of memory management with MMU.
