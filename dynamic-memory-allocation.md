# Dynamic Memory Allocation (Heap)

## C Functions For D M A

<table><thead><tr><th width="113">Function</th><th width="124">Purpose</th><th width="116">Inputs</th><th width="114">Output</th><th>Notes / Gotchas</th></tr></thead><tbody><tr><td><code>malloc(size)</code></td><td>Allocate uninitialized block</td><td><code>size</code> (bytes)</td><td>Pointer or <code>NULL</code></td><td>Contents uninitialized → using before writing = <strong>bug</strong> (may leak old data).<br>On failure: <code>NULL</code>, <code>errno=ENOMEM</code>.</td></tr><tr><td><code>calloc(nmemb, size)</code></td><td>Allocate zeroed array</td><td><code>nmemb</code>, <code>size</code></td><td>Pointer or <code>NULL</code></td><td>Safe against multiplication overflow (<code>nmemb*size</code>). <br>Always initialized to zero. Slightly slower than <code>malloc</code>.</td></tr><tr><td><code>realloc(ptr, size)</code></td><td>Resize block</td><td><code>ptr</code> (old block), <code>size</code></td><td>New pointer or <code>NULL</code></td><td>If moved, old block freed automatically.<br>If fail: returns <code>NULL</code> but old block still valid → <strong>must not lose the old pointer</strong>.<br>If <code>ptr=NULL</code>, acts like <code>malloc</code>. <br>If <code>size=0</code> with non-NULL ptr, frees block.</td></tr><tr><td><code>reallocarray(ptr, nmemb, size)</code></td><td>Resize array safely</td><td><code>nmemb</code>, <code>size</code></td><td>Pointer or <code>NULL</code></td><td>Same as <code>realloc</code>, but prevents integer overflow in <code>nmemb*size</code>.</td></tr><tr><td><code>free(ptr)</code></td><td>Release block</td><td><code>ptr</code> (malloc-family result)</td><td>None</td><td>If <code>ptr=NULL</code>, no-op. Otherwise → block is invalid afterwards.<br>Double free or use-after-free = <strong>undefined behavior</strong> (can crash or be exploited).</td></tr></tbody></table>

Returned pointer is suitably aligned for any built-in type.

***

Assembly just calls these functions and waits for `rax` to get the pointer to the memory. That's it. All the magic is in the backend.

## The Backend

The backend here means the whole memory management process.

`mallo callo realloc reallocarray free` are just frontends, the actual engine powering these APIs is the **allocator**. There are multiple implementations of an allocator, catering for the developer's requirements and we can also create our own allocator.

The most widely used allocators include:

1. `ptmalloc`: `glibc` implementation
2. `tcmalloc`
3. `jemalloc`
4. And the father of all allocators, the allocator, `dlmalloc`. This is what we are going to start with.

***

`dlmalloc` stands for Doug Lea's `malloc` implementation.

* He is a professor of CS at State University of New York at Oswego.

To understand `dlmalloc` , we have to understand how Doug Lea visualized the "heap memory". For that, we have to understand some terms.

## Doug Lea's Memory Model

This is the virtual address space layout for user space memory. For more information, checkout [virtual-memory-layout.md](all-roads-to-memory/virtual-memory-layout.md "mention")

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

There are two methods to allocation heap memory. They are `sbrk()` and `mmap()` .

### brk()

There is a syscall named `brk()` which is used to extend the **program break**. What is program break?

In the early days of dynamic memory allocation, the data segment was data/bss and heap together.

* It is perfectly logical as compilation already reveals how much space you need for static/globals so the lower part of the data segment was reserved for static/globals and the upper part was reserved for heap.

_Therefore, program break is the boundary which logically separates the data/bss part from heap._

* For example, the data segment starts at `0d1000` and ends at `0d1015` . This means that 16 bytes are required for data/bss. Now the program break is at `0d1016` just one byte after the data/bss allocation.

If any function from `malloc` family is called, the `brk()` is executed to extend the program break. And this new space is what heap is.

`brk()` takes an address and changes the program break to it. But how we are supposed to know where the current program break is?

* `brk(0)` gives the current program break.
* But a problem with `brk()` is that it doesn't return the pointer to the newly allocated space.

### sbrk()

`sbrk()` is a C library function, which is a wrapper over the actual `brk()` syscall.

`brk()` returns 0 on success and -1 on failure. `sbrk()` returns the pointer to the newly allocated memory or the previous program break on success and `(void *)-1` on failure.

***

So in practice, we use `sbrk()` not `brk()`. Although the use of both is not recommended today; instead we should use functions from `malloc` family.

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

0x55bc200da000 = 0d94266479976448

0x55bc200da020 = 0d94266479976480

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

Just by the output we can see that the jump in address is way too much. This behavior might be attributed to `printf` calling `malloc` internally for its requirements. **Never mix the two**.

### mmap()











