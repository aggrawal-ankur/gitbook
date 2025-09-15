# Lets Get Chunky

_**15 September 2025**_

***

In brief, the whole story of dlmalloc revolves around chunks. And the story is quite big so we need a path to follow. Let's try to map the surface first.

## How chunks are formed?

When a process start to exist, it rarely requires dynamic memory allocation. There are shared libraries in the memory mapped region but that's not dynamic memory allocation.

When the code calls `malloc` , this is when the idea of dynamic memory allocation starts to exist for that process.

Suppose the ask was `malloc(20)`. We know that a pointer in heap is returned such that it is suitable for any built-in type. We are asking for 20 bytes.

But memory is managed in terms of pages. Now there is a difference in how the allocator is managing memory and how the kernel is managing memory. To solve this problem, the kernel allocates in terms of pages, while the allocator divides the page into chunks. Simple.

Since the smallest page can be 1 page only, assuming 4 KiB size, for `malloc(20)` request, the allocator receives 4 KiB from the kernel, that is 4096 bytes.

These 4096 bytes is our **arena**, the total unallocated pool of memory, that the allocator is now going to manage.

Since a chunk of 20 bytes was requested, 20 bytes will be carved out from 4096 bytes of heap memory and will be allocated to the process.

* In this process, the program break would have increased by 20 bytes.

Now we have `4076` bytes of unallocated memory and one **in-use chunk** of 20 bytes.

* That's how **the first in-use chunk** comes into existence for a process.

Suppose we had few more allocations following, `malloc(40); malloc(10); malloc(28); malloc(32);`.

* A total of `110` bytes is request here. And we have plenty in the arena.
* After this allocation, we have `3066` bytes of unallocated memory and **five in-use chunks** or varying sizes.

Now the process is coming to an end and we are freeing every allocation.

*   ```
    free(20); free(40); free(10); free(28); free(32);
    ```

    and the process died.

In this scenario, there were no free chunks and honestly, there was no need as well.

***

Let's take another example.

This time, this is going to be the flow \~

```
malloc(10);
malloc(20);
free(10);
malloc(30);
free(20);
malloc(35);
malloc(30);         goes in the first group from cache bins
```

To understand this better, let's create a small ASCII drawing representing byte-addressable memory.







