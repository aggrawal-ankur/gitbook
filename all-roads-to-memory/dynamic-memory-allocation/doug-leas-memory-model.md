# Doug Lea's Memory Model

_**11, 15 September 2025**_

***

Now we will explore Doug Lea's memory model.

## Allocator Instance

Every process gets an instance of the allocator program, `dlmalloc` in this case.

The allocator instance is like the manager of dynamic memory for that process. It ensures that the process's ask for dynamic memory gets fulfilled the right way.

## Arena

The entire pool of memory managed by the `dlmalloc` instance for a process is called arena.

## Chunks

A chunk is the fundamental unit of memory in `dlmalloc`.

Every allocation is backed by a **chunk**, not just raw bytes.

A chunk is made up of a header and payload.

* Header contains metadata about the chunk.
* Payload refers to the place where user data would go after allocation.

A chunk can be divided into two types based on its availability.

1. **In-use chunks** refers to chunks which are allocated to the process.
2. **Free-chunks** refers to chunks which are available to the allocator for allocation.

The minimum size of a chunk is equal to enough for metadata and alignment.

* On 64-bit: typically **16 or 24 bytes** minimum.
* Chunk sizes are **multiples of alignment** (8 or 16 bytes).

`dlmalloc` requests memory in multiple of pages and carves those into chunks for fine-grained allocations.

The last chunk near the end of the heap (near the program break) is called the **top chunk**. When bins can't satisfy an allocation, dlmalloc extends the top chunk using `sbrk` .

## Bins

Free chunks or the chunks available to the allocator for allocation are organized into bins.

A bin is implemented using a linked list as they allow `O(1)` removal and insertion from anywhere.

Consider a bin as a bucket, where different buckets exist for different kinds of chunks. This categorization of bins helps balancing speed vs memory usage.

### Fast Bins

Small fixed-size ranges (e.g., 16–64 bytes).

Singly-linked LIFO (push/pop).

No coalescing on free (fast, but can cause short-term fragmentation).

### Small Bins

Exact size classes (multiples of alignment up to some threshold, e.g., 512 bytes).

Implemented using doubly-linked circular lists.

Coalescing is supported.

### Large Bins

For bigger requests.

Free chunks are sorted by size inside bins.

Implemented using doubly linked list.

Allow searching for a "fit" (best, first, etc.) efficiently.

### Unsorted Bins

Temporary holding bin for newly freed chunks before they are placed into proper bin.

Helps with quick reuse and reduces bin searching overhead.

Implemented using doubly-linked circular lists.

## Mmap'd Chunks

Large requests are allocated with `mmap` and released with `munmap`.

`dlmalloc` uses a threshold to decide when to use mmap and heap.

## Split and Merge

When a big chunk is available but a small chunk is requested, the allocator carves the requested size out of the big chunk and leave the rest in bins. This is called **splitting**.

When the process frees an allocation, `free(ptr)` , it makes the chunk available for reuse to the allocator. When such chunks are present adjacent to each other, they can be merged into one large free chunk. This is called **coalescing**.

## Fragmentation

Fragmentation is wasted memory that can’t be used efficiently:

1. **External fragmentation**: free memory exists, but in pieces too small or scattered to satisfy a request. Example: you have three 1 KB holes but need 3 KB contiguous.
2. **Internal fragmentation**: memory inside an allocated chunk that the program doesn’t use. Example: program asked for 13 bytes, allocator rounds up to 16 (3 wasted). 3 bytes wasted in padding.

## Fits Strategy

It refers to how the allocator chooses a free chunk from bins when multiple could work.

1. **First-fit**: pick the first sufficiently large chunk you find. Fast, but can cause uneven fragmentation.
2. **Best-fit**: search for the chunk closest in size to request. Reduces waste but costs more CPU (searching).
3. **Next-fit**: like first-fit but resume search where you left off. Spreads allocations, less clustering.

`dlmalloc` uses:

* **exact fits** in small bins.
* **best-fit within size range** for large bins (but not global best-fit, just best within that bin).

This hybrid gives both speed and decent fragmentation control.

## Trimming

Releasing memory from the top chunk back to the kernel (lowering program break) is called **trimming**.

It prevents unbounded growth.
