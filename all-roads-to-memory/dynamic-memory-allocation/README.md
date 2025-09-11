# Dynamic Memory Allocation

9, _**10 September 2025**_

***

## C Functions For D M A

<table><thead><tr><th width="113">Function</th><th width="124">Purpose</th><th width="116">Inputs</th><th width="114">Output</th><th>Notes / Gotchas</th></tr></thead><tbody><tr><td><code>malloc(size)</code></td><td>Allocate uninitialized block</td><td><code>size</code> (bytes)</td><td>Pointer or <code>NULL</code></td><td>Contents uninitialized → using before writing = <strong>bug</strong> (may leak old data).<br>On failure: <code>NULL</code>, <code>errno=ENOMEM</code>.</td></tr><tr><td><code>calloc(nmemb, size)</code></td><td>Allocate zeroed array</td><td><code>nmemb</code>, <code>size</code></td><td>Pointer or <code>NULL</code></td><td>Safe against multiplication overflow (<code>nmemb*size</code>). <br>Always initialized to zero. Slightly slower than <code>malloc</code>.</td></tr><tr><td><code>realloc(ptr, size)</code></td><td>Resize block</td><td><code>ptr</code> (old block), <code>size</code></td><td>New pointer or <code>NULL</code></td><td>If moved, old block freed automatically.<br>If fail: returns <code>NULL</code> but old block still valid → <strong>must not lose the old pointer</strong>.<br>If <code>ptr=NULL</code>, acts like <code>malloc</code>. <br>If <code>size=0</code> with non-NULL ptr, frees block.</td></tr><tr><td><code>reallocarray(ptr, nmemb, size)</code></td><td>Resize array safely</td><td><code>nmemb</code>, <code>size</code></td><td>Pointer or <code>NULL</code></td><td>Same as <code>realloc</code>, but prevents integer overflow in <code>nmemb*size</code>.</td></tr><tr><td><code>free(ptr)</code></td><td>Release block</td><td><code>ptr</code> (malloc-family result)</td><td>None</td><td>If <code>ptr=NULL</code>, no-op. Otherwise → block is invalid afterwards.<br>Double free or use-after-free = <strong>undefined behavior</strong> (can crash or be exploited).</td></tr></tbody></table>

Returned pointer is suitably aligned for any built-in type.

Assembly just calls these functions and waits for `rax` to get the pointer to the memory.

And as with everything, the above mentioned functions are wrappers in libc. The underlying machinery, which does the heavy lifting is called **an allocator.**

There are multiple implementations of allocator, catering for the project's requirements. We can also create our own allocator program.

The most widely used allocators include:

1. `ptmalloc`: GNU's implementation for glibc.
2. `tcmalloc` : google's implementation for their c/c++ projects
3. `jemalloc` : created by Jason Evans for a personal programming language project but came out as a great memory allocator which was integrated into FreeBSD and various other platforms like Facebook and Firefox use it.

But the father of all allocators, not the first memory allocator, but definitely the most significant one was `dlmalloc`. This is what we are going to start with.

`dlmalloc` stands for Doug Lea's memory allocator implementation.

* He is a professor of CS at State University of New York at Oswego.

Before diving into `dlmalloc`, we have to understand some dynamic memory concepts.
