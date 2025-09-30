---
id: 632446e0d44244308a8146eabf6433b3
title: Virtual Address Space
weight: 1
---

_**11, 12 August 2025 (init)**_

***29, 30 September 2025 (rewrite and merge)***

---

Virtual Address Space (or VAS) is divided into two parts.

- Kernel Space
- User Space

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

## Why this division?

User space and Kernel space are two logical divisions of virtual memory.

This logical division is achieved by access control (privileges) and protection rights, which are enforced both at hardware level (CPU) and software level (OS).

User space is the portion where unprivileged jobs are managed and kernel space is where privileged jobs are managed.

A very popular and generalized definition is that *user space is where **user mode** applications run and kernel space is where the **OS Kernel** runs. This doesn't sound accurate to me for one reason.*

- A task is usually made up of multiple atomic jobs. And we can verify this with assembly. An action as simple as printing something to the standard output can involve multiple steps.
- That's why, a task itself can't be tagged as "privileged" or "unprivileged". The atomic jobs that do the work can only be tagged.
- For example, running _VS Code_ is a user space action but within that are thousands of actions, many of which aren't possible without privileged access. Like writing code, which is an I/O operation inside a file, which is a privileged job.
- Therefore, it is a little ambiguous to say that "_user space runs user mode applications and kernel space is for elevated tasks_" or something like that. Saying that "_user space executes unprivileged jobs and kernel space executes privileged jobs_" is far more accurate in my opinion.

There is no limit on what you can execute, which creates problems. There are malwares and other program threatening the functioning of the hardware.

This division ensures that programs can be contained by default. Its a version of _**deny by default, allow by exception**_ strategy. Everything is considered unsafe before it passes the kernel's checks.

Any attempt to access privileged area doesn't get unnoticed. And if it is inappropriate, the system denies it.

There is a proper mechanism through which the execution mode changes from user space to kernel space, when required.

### Analogy

Consider an office space with employees of different kinds. And there is a room for the boos.

The boss's room is what kernel space is really is. Only privileged access is allowed and rest has to undergo a process to come there.

Then there is general area which is accessible to everyone as long as they are an employee in the company. This is our user space.

When you need to something that requires permission from the boss, you go through a standard process, which is exactly how the execution context changes from user space to kernel space when required.

### Hardware Enforced Privilege Levels

**Rings** are hardware-enforced CPU privilege levels, which forms a core part of how modern processors (like x64) separates trusted code (kernel) from untrusted (user) code.

CPUs implement multiple **protection rings** numbered 0 to 3, with:

* **Ring 0 = highest privilege (kernel mode)**
* **Ring 3 = lowest privilege (user mode)**
* **Rings 1 and 2** exist but are rarely used in mainstream Linux.

## Kernel Space

***TO BE WRITTEN***

***AND ITS LAYOUT***

## User Space

The user space is divided into:

- Text: To store program instructions.
- Data: Storage for static/extern declarations.
- Heap: Dynamic memory allocation.
- Mmap: Memory mapped region.
- Stack: To manage function frames (arguments and local variables)

This is the layout of user space:
```
0x0000800000000000 *-----------------------------* End of User Space ↓
                   |   Stack (grows downward) ↓  |
                   *-----------------------------*
                   |    Memory-Mapped Region     |
                   |  (shared libs, mmap, ....)  |
                   *-----------------------------*
                   |         Free Space          |
                   *-----------------------------*
                   |    Heap (grows upward) ↑    |
                   *-----------------------------*
                   |  Static && Extern Variables |
                   |       (.bss / .data)        |
                   *-----------------------------*
                   |        Code (.text)         |
0x0000000000400000 *-----------------------------* Start Of User Space ↑
```

`.data` and `.bss` are packed together because they are functionally the same thing, just differ in initialization.

### What are stack and heap really?

Stack and heap are two approaches to manage memory.

There are no specialized regions in the physical memory which refer to stack or heap. They are just two ways to manage the same flat memory.

### Why the stack grows downward?

When we learn stack as a data structure, we imagine it as a stack of plates. A stack of anything starts from bottom and approaches sky as the top.

When you learn assembly, you find that stack grows downward. And you keep scratching your head. I was no different.

There is a simple solution to this problem. **Reverse the address space.**

* Right now we are looking from top to bottom or higher addresses to lower addresses.
* Just flip the structure and you get an upward growing stack.

Remember, this doesn't change the address management in stack. A push would still reduce the memory address and a pop would increase it. But, at least it solves the mental overhead of imagining stack growing downward.

***

Anyways, "why stack was put at the top of the user space" is a question I genuinely I have no answer. But if I find anything interesting, I will update this block.

### Why the stack is fast and heap is slow?

This question is not completely answerable as it is based on comparison.

We can explore why stack is fast because we are familiar with it. But we don't know what heap is.

Although we know why stack is fast because it is based on sequential allocation. But what makes heap slow is not known.

When we will explore dynamic memory allocation, it will become obvious.

## How it connects?

We know that a binary follows ELF format (on Linux) which basically tells the OS how to load that binary into memory.

In other words, Virtual address space is the runtime representation of a binary.

## Virtual Address

Total number of bits we have are 64. But not all the 64-bits are required to manage addresses now. It would be huge to manage 2^64 addresses.

So, we stick to 48-bit virtual addresses. The rest of the 16-bits are sign extension of the 47th bit. We'll explore what that means in a while.

A virtual address is divided into several pieces. More precisely, the bits in the a virtual address are grouped together to represent different parts of the 4-level paging system that we have discussed previously.

At high level, a virtual address is structured like this:

```
+--------------+ +--------------+ +--------------+ +------------+ +----------------------+
| PML4: 9-bits | | PDPT: 9-bits | | PDIT: 9-bits | | PT: 9-bits | | Page Offset: 12-bits |
+--------------+ +--------------+ +--------------+ +------------+ +----------------------+
47            39 38            30 29            21 20          12 11                     0
```

### Why like this?

All the 4 page tables have 512 entries, which require a minimum of 9-bits to represent. So, 9-bits are reserved for them.

Page offset is the actual byte being addressed within the page. Since there are 4096 bytes in total, 12-bit are required at minimum to represent them.

### Some Good-To-Know Things

A virtual address is in big endian notation, so most significant bits are in left and least significant bits in the right.

As long as we are dealing with pen paper math, there is no need for bit shifts. But with programming, bit shifting becomes important for extracting values the right way and avoiding falling at edge cases.

Each process gets a virtual address space, which has 256 TiB worth of addressable space, most of which is empty. Yes, the calculation we have done previously is applied individually to every single process.

* The program never runs out of virtual address spaces. It only runs out of mappings in the physical memory.

**Note: Addressable space ≠ Usable space.**

## Address Range Split

The virtual address space is split into two halves for user space and kernel space.

```
0x0000000000000000  →  0x00007FFFFFFFFFFF  (Lower half, ~128 TiB)   → User space
0xFFFF800000000000  →  0xFFFFFFFFFFFFFFFF  (Upper half, ~128 TiB)   → Kernel space
```

* The middle region (`x00007FFFFFFFFFFF to 0xFFFF800000000000`) is unused guard space.

**Note: The split is logical and exist only in virtual memory, except the hardware enforced rules.**