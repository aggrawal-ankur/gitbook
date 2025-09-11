# Doug Lea's Memory Model

_**11 September 2025**_

***

Now we will explore Doug Lea's memory model.

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

## Bins

Free chunks or the chunks available to the allocator for allocation are organized into bins.

A bin is implemented using a linked list as they allow `O(1)` removal and insertion from anywhere.

Consider a bin as a bucket, where different buckets exist for different kinds of chunks. This categorization of bins helps balancing speed vs memory usage.

### Fast Bins

Small fixed-size ranges (e.g., 16–64 bytes).

Singly-linked LIFO (push/pop).

No coalescing on free (fast, but can cause short-term fragmentation).

***

### Small Bins

Exact size classes (multiples of alignment up to some threshold, e.g., 512 bytes).

Implemented using doubly-linked circular lists.

Coalescing is supported.

***

### Large Bins

For bigger requests.

Free chunks are sorted by size inside bins.

Implemented using doubly linked list.

Allow searching for a "fit" (best, first, etc.) efficiently.

### Unsorted Bins

Temporary holding bin for newly freed chunks before they are placed into proper bin.

Helps with quick reuse and reduces bin searching overhead.

Implemented using doubly-linked circular lists.

## Coalescing

When the process uses `free(ptr)` , it makes the chunk available for reuse to the allocator. When such chunks are present adjacent to each other, they can be merged into one large free chunk. This is called coalescing.

## Top Chunk

It is the last chunk near the end of the heap (near the program break).

When bins can't satisfy an allocation, dlmalloc extends the top chunk using `sbrk` .

## Mmap'd Chunks

Large requests bypass bins/top chunk and directly use `mmap`.

They are released using `munmap`.

dlmalloc uses a threshold to decide when to use mmap and heap.

## Split and Merge

When a big chunk is available but a small chunk is requested, carve the requested size out of the big chunk and leave the rest in bins. This is called splitting.

Too many small chunks, which can't be allocated alone are merged together to form a big chunk. This is called merging or coalescing.

## Arena

The entire heap managed by the a `dlmalloc` instance is called arena.

Every process gets an instance of `dlmalloc` along with some memory in heap by the kernel.

## Fragmentation

Fragmentation is wasted memory that can’t be used efficiently:

1. **External fragmentation**: free memory exists, but in pieces too small or scattered to satisfy a request. Example: you have three 1 KB holes but need 3 KB contiguous.
2. **Internal fragmentation**: memory inside an allocated chunk that the program doesn’t use. Example: program asks for 13 bytes, allocator rounds up to 16 (3 wasted).

## Fits Strategy

It refers to how the allocator chooses a free chunk from bins when multiple could work.

1. **First-fit**: pick the first sufficiently large chunk you find. Fast, but can cause uneven fragmentation.
2. **Best-fit**: search for the chunk closest in size to request. Reduces waste but costs more CPU (searching).
3. **Next-fit**: like first-fit but resume search where you left off. Spreads allocations, less clustering.

`dlmalloc` uses:

* **exact fits** in small bins.
* **best-fit within size range** for large bins (but not global best-fit, just best within that bin).

This hybrid gives both speed and decent fragmentation control.









