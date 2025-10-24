---
id: 259f273ff0484543b8720a5d8175bdd7
title: Dynamic Memory Allocation
weight: 5
---

_**9, 10, 15 September 2025**_

***

These are the primary functions used for dynamic memory allocation in C. These are wrappers in libc/glibc. The underlying machinery that powers them is called the **allocator program**.


| Function | Purpose | Inputs | Output | Notes / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| malloc(size) | Allocate uninitialized block | size(bytes) | Pointer orNULL | Contents uninitialized → using before writing =bug(may leak old data).On failure:NULL,errno=ENOMEM. |
| calloc(nmemb, size) | Allocate zeroed array | nmemb,size | Pointer orNULL | Safe against multiplication overflow (nmemb*size).Always initialized to zero. Slightly slower thanmalloc. |
| realloc(ptr, size) | Resize block | ptr(old block),size | New pointer orNULL | If moved, old block freed automatically.If fail: returnsNULLbut old block still valid →must not lose the old pointer.Ifptr=NULL, acts likemalloc.Ifsize=0with non-NULL ptr, frees block. |
| reallocarray(ptr, nmemb, size) | Resize array safely | nmemb,size | Pointer orNULL | Same asrealloc, but prevents integer overflow innmemb*size. |
| free(ptr) | Release block | ptr(malloc-family result) | None | Ifptr=NULL, no-op. Otherwise → block is invalid afterwards.Double free or use-after-free =undefined behavior(can crash or be exploited). |


Returned pointer is aligned for any built-in type.

Assembly just calls these functions and waits for `rax` to get the pointer to the memory.

***

An **allocator** is the program that manages dynamic memory requirements.

* Each process gets its own **allocator instance**, which manages its dynamic memory requirements.

There are multiple implementations of allocator, each designed for specific project requirements. We can create our own allocator program as well.

The most widely used allocators include:

1. `ptmalloc`: GNU's implementation for glibc, written by Wolfram Gloger.
2. `tcmalloc` : Google's implementation for their C/C++ projects.
3. `jemalloc` : Created by Jason Evans for a programming language project but came out as a great memory allocator which was integrated into FreeBSD and various other platforms like Facebook and Firefox use it. [Link](https://jasone.github.io/2025/06/12/jemalloc-postmortem/)

But the father of all allocators, not the first memory allocator, but definitely the most significant and influential one was `dlmalloc`. This is what we are going to start with.

`dlmalloc` stands for Doug Lea's memory allocator implementation.

* He is a professor of CS at State University of New York at Oswego.
* [This repository](https://github.com/DenizThatMenace/dlmalloc) has every version of dlmalloc.
* [This repository](https://github.com/aradzie/dlmalloc) has a clear version of dlmalloc as the the original version uses a strange dialect of C which is not beginner friendly.
* [This repository](https://github.com/emeryberger/Malloc-Implementations) has multiple allocator implementations under one roof.

{{< doclink "4dad5e63422947e2b702845a0ed95963" "" >}}
{{< doclink "7918f5d1358b402f8dc216ed1ab966d6" "" >}}
{{< doclink "68860c0125cc44f0bb05de46ee9fb6c3" "" >}}
{{< doclink "3ce161e7cb8f4147b683400a07e3d22d" "" >}}
{{< doclink "cce8e80c3d334b0d85942b848383a868" "" >}}
{{< doclink "5b14ef9b921c4b3b839676cc42601d21" "" >}}
{{< doclink "541b36bd3e7947d5a876102fc9531bbc" "" >}}