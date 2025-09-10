# Linux Syscalls For DMA

_**10 September 2025**_

***

## User Space Layout

This is the virtual address space layout for user space memory. For more information, checkout [virtual-memory-layout.md](../virtual-memory-layout.md "mention")

```
  User Space Memory Layout
*--------------------------*
|  High Memory (~128 TiB)  |
|  *-----------------*     |
|  |    Stack (↓)    |     |
|  *-----------------*     |
|  |   mmap region   |     |
|  *-----------------*     |
|  |    Free Space   |     |
|  *-----------------*     |
|  |     Heap (↑)    |     |
|  *-----------------*     |
|  | Data (data/bss) |     |
|  *-----------------*     |
|  |      Code       |     |
|  *-----------------*     |
|  Low Memory (0..0)       |
*--------------------------*
```

The "heap" region and the "mmap" region both supports dynamic memory allocation. But both are managed differently, which is why we have two different methods for dynamic memory allocation.

* They are `sbrk()` and `mmap()` .
* `sbrk()` manages the heap region and `mmap()` manages the mmap region.

## brk()

There is a syscall named `brk()` which is used to extend the **program break**. What is program break?

In the early days of dynamic memory allocation, the data segment was data/bss and heap together.

* It is perfectly logical as compilation already reveals how much space you need for static/globals so the lower part of the data segment was reserved for static/globals and the upper part was reserved for heap.

_Therefore, program break is the boundary which logically separates the data/bss part from heap._

* For example, the data segment starts at `0d1000` and ends at `0d1015` . This means that 16 bytes are required for data/bss. Now the program break is at `0d1016` just one byte after the data/bss allocation.

If any function from `malloc` family is called, the `brk()` is executed to extend the program break. And this new space is what heap is.

`brk()` takes an address and changes the program break to it. But how we are supposed to know where the current program break is?

* `brk(0)` gives the current program break.
* But a problem with `brk()` is that it doesn't return the pointer to the newly allocated space.

## sbrk()

`sbrk()` is a C library function, which is a wrapper over the actual `brk()` syscall.

`brk()` returns 0 on success and -1 on failure. `sbrk()` returns the pointer to the newly allocated memory or the previous program break on success and `(void *)-1` on failure.

***

In practice, we use `sbrk()` not `brk()`. Although the use of both is not recommended today; instead we should use functions from `malloc` family.

A key thing about `sbrk(n)` is that it extends heap contiguously. And we can prove this by a simple example:

```c
#include <stdio.h>
#include <unistd.h>

int main() {
  void *initial_break = sbrk(0);  // get current break
  
  // Allocate 32 bytes using sbrk
  void *new_mem = sbrk(32);
  if (new_mem == (void*) -1) {
    perror("sbrk failed");
    return 1;
  }

  // New program break
  void *after_alloc = sbrk(0);

  printf("Initial program break: %p\n", initial_break);
  printf("Allocated 32 bytes at: %p\n", new_mem);
  printf("Program break after sbrk: %p\n", after_alloc);

  return 0;
}
```

The output is:

```bash
$ gcc main.c
$ ./a.out

Initial program break: 0x55bc200da000
Allocated 32 bytes at: 0x55bc200da000
Program break after sbrk: 0x55bc200da020
```

```
0x55bc200da000 = 0d94266479976448
0x55bc200da020 = 0d94266479976480
```

The difference is exactly 32 bytes.

***

But, if you do this:

```c
#include <stdio.h>
#include <unistd.h>

int main() {
  void *initial_break = sbrk(0);  // get current break
  printf("Initial program break: %p\n", initial_break);
  
  // Allocate 32 bytes using sbrk
  void *new_mem = sbrk(32);
  if (new_mem == (void*) -1) {
    perror("sbrk failed");
    return 1;
  }
  printf("Allocated 32 bytes at: %p\n", new_mem);

  // New program break
  void *after_alloc = sbrk(0);
  printf("Program break after sbrk: %p\n", after_alloc);

  return 0;
}
```

the output changes significantly.

```bash
$ gcc main.c
$ ./a.out  
 
Initial program break: 0x559b4fc4b000
Allocated 32 bytes at: 0x559b4fc6c000
Program break after sbrk: 0x559b4fc6c020
```

Just by the output we can see that the jump in address is way too much. This behavior might be attributed to `printf` calling `malloc` internally for its requirements.

**Therefore, never mix the two**.

## mmap()

`mmap` is a Linux syscall and `mmap()` is libc wrapper around it.

mmap stands for memory map which lets a process map files or anonymous memory into its virtual address space.

Unlike `brk/sbrk`, which adjust the heap break, `mmap` can allocate memory anywhere in the `mmap` region of the virtual address space, not just growing the heap upward.

If `mmap()` was successful, it returns a pointer to the allocated memory. If failed, `(void *) -1`.

Every time we run a program on Linux, the dynamic linker (`ld.so`) uses `mmap` to load shared libraries (`.so` files) in our address space. So, we don't use `mmap` directly, unless we're doing systems programming; but we are incomplete without it.

* _In a more melodramatic way, we might not use it directly, but Its presence is a boon to us._

***

`mmap` has a variety of use cases and dynamic memory allocation is one of them.

1. **File mapping.** Map a file into memory and access it like an array.
2. **Anonymous mapping:** Heap-like memory without touching the process break.
3. **Shared memory:** Two processes can map the same file and see each other’s updates.



## Where are the boundaries?

If you notice, stack is free flowing, heap is free flowing and mmap is free flowing. Where are the boundaries that prevent collision?

* Code section is fixed at compile-time.
* data/bss size is known at compile-time, so that is also fixed.
* The start of heap is fixed, just after data/bss. But the end is floating.
* The start of stack is fixed at the top of user space and grows downwards. But the end is floating again, depending on stack pointer.
* At last we have `mmap` region, which is surrounded by floating regions.

The answer is that there are no boundaries.&#x20;

First of all, the virtual address space is large enough to make this problem insignificant for normal use case.

Second, the kernel has data structures which keep every allocation in control and lets the kernel not allocate memory when there is a point of conflict.

***

## sbrk() or mmap()

How the allocator decides whether to use `sbrk()` or `mmap()` ?

* Although the exact implementation can vary, the concept remains the same.
* Small allocations via `sbrk()` and large allocations via `mmap()`. The definition of small and large can be allocator specific which we will explore later.







