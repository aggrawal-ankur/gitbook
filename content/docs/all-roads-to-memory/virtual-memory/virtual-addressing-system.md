---
title: Virtual Addressing System
weight: 2
---

_**August 11 and 12, 2025**_

***

## A Virtual Address

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

***

## Address Range Split

The virtual address space is split into two halves for user space and kernel space.

```
0x0000000000000000  →  0x00007FFFFFFFFFFF  (Lower half, ~128 TiB)   → User space
0xFFFF800000000000  →  0xFFFFFFFFFFFFFFFF  (Upper half, ~128 TiB)   → Kernel space
```

* The middle region (`x00007FFFFFFFFFFF to 0xFFFF800000000000`) is unused guard space.

**Note: The split is logical and exist only in virtual memory, except the hardware enforced rules.**

### What are user space and kernel space really?

In simple words, user space and kernel space are two logical distinctions within the virtual memory layout.

This logical distinction is achieved by access control (privileges) and protection rights, which are enforced both at the hardware level (CPU) and the software level (OS).

User space is the portion where unprivileged jobs are managed and kernel space is where privileged jobs are managed.

A definition which is quite popular is that user space is where **user mode** applications run and kernel space is where the **OS Kernel** runs or privileged tasks are executed. This doesn't sound accurate to me for one reason.

* A task is usually made up of multiple atomic jobs. And we can verify this with assembly. An action as simple as printing something to standard output can involve multiple steps.
* A task itself can't be tagged as privileged or unprivileged. The atomic jobs that actually do something are the ones that can be actually tagged.
* For example, running _VS Code_ is a user space action but within that are several thousands of actions, many of which aren't possible without privileged access. Like writing code, which is an I/O operation inside a file, which is a privileged job.
* Therefore, it is a little ambiguous to say that "_user space runs user mode applications and kernel space runs elevated tasks_" or something like that. Saying that "_user space executes unprivileged jobs and kerne space executes privileged jobs_" is far more accurate in my opinion.

### Why this distinction exist?

There is no limit on what you can execute, which creates problems. There malwares and other program threatening the functioning of the hardware.

This distinction ensures that programs can be contained by default. Its a version of _**deny by default, allow by exception**_ strategy. Anything is considered unsafe before it passes the kernel's checks.

And any attempt to access privileged area doesn't get unnoticed. And if it is inappropriate, the system denies it.

There is a proper mechanism through which the execution mode switches from user space to kernel space, when required.

### Analogy

Consider an office space with employees of different kinds. And there is a room for the boos.

The boss's room is what kernel space is really is. Only privileged access is allowed and rest has to undergo a process to come there.

Then there is general area which is accessible to everyone as long as they are an employee in the company. This is out user space.

When you need to something that requires permission from the boss, you go through a standard process, which is exactly how the execution context changes from user space to kernel space when required.

### Hardware Enforced Privilege Levels

**Rings** are hardware-enforced CPU privilege levels, which forms a core part of how modern processors (like x64) separates trusted code (kernel) from untrusted (user) code.

CPUs implement multiple **protection rings** numbered 0 to 3, with:

* **Ring 0 = highest privilege (kernel mode)**
* **Ring 3 = lowest privilege (user mode)**
* **Rings 1 and 2** exist but are rarely used in mainstream Linux.

System calls cause a CPU privilege level switch from Ring 3 → Ring 0.













