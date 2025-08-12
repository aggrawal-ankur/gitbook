# General Process Layout In Virtual Memory

_**August 12, 2025**_

***

## A Big Picture Layout Of The Virtual Address Space

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

### User Space Layout

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

* `.bss` and `.data` lives together because they are functionally the same thing, they just differ in initialization.

## What are stack and heap really?

In simple words, stack and heap are two approaches to manage memory. There are no specialized regions either in the virtual memory or physical memory which refer to stack or heap. They are just two ways to manage the same flat memory.

These approaches are very dense and exceeds the scope of this series, not just the write up. So, if you want to read more about them, you can visit [here](https://ankuragrawal.gitbook.io/home/~/revisions/9oCulmOXQVthvPHUANsQ/approaches-to-memory-management).

## Why the stack grows downward?

When we learn stack as a data structure, we imagine it as a stack of plates. A stack of anything starts from bottom and approaches sky as the top.

But, when you learn assembly, you find that stack grows downward. And you keep scratching your head. I was no different.

There is a simple solution to this problem. **Reverse the address space.**

* Right now we are looking from top to bottom or higher addresses to lower addresses.
* Just flip the structure and you get an upward growing stack.
* Just remember that this doesn't change the address management of stack. A push would still reduce the memory address mathematically and a pop would increase it. But, at least it solves the mental overhead of imagining stack growing downwards.

***

Apart from this, there is a genuine question that why stack was put at the top of the user space. The reasoning that they shouldn't collide is not applicable here as the memory-mapped region will always come in-between. While I don't have any answer to that, but if I find anything, I will update this block.

***

## Why the stack is fast and heap is slow?

Right now this question is not completely answerable because it is based on comparison. We can explore why stack is fast because we are familiar with it and we already know the answer unconsciously, that stack is based on sequential allocation. But we don't know what heap is.

I pointed this out so that I don't forget to answer it. Later when we will explore heap allocation, it will itself clear why stack is fast and heap is slow.

***

Until then, we are now prepared to understand how all of this fits in the grand scheme of memory management with MMU.
