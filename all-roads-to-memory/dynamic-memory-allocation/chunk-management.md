# Chunk Management

_**17 September 2025 (definitions taken out from a previous**_ [_**write up**_](https://ankuragrawal.gitbook.io/home/~/revisions/0fLrDsjrcXzDo0NctRkY/all-roads-to-memory/dynamic-memory-allocation/doug-leas-memory-model)_**, written on 11, 15, 16 September 2025, optimized)**_

***

Let's explore how free chunks are managed by the allocator.

When chunks are not in use, they are treated as nodes of either lists or trees.

* Linked List and Trees are the two major data structures that dlmalloc utilizes to manage free chunks efficiently.

## Bins

Free chunks are organized into bins.

In-use chunks are self-owned. Their bookkeeping lives in the chunk header itself and no external registry maintains them.

Once a chunk is allocated, it disappears from the bin it was in. When an in-use chunk is freed, it re-enters the bin system.

Consider a bin as a bucket for storing chunks. Different buckets exist for different chunks. This categorization of bins helps balancing speed and memory usage.

### Types Of Bins

<table><thead><tr><th width="131">Name</th><th>Use</th></tr></thead><tbody><tr><td>Fast Bins</td><td>For small and fixed size ranges (e.g. 16-64 bytes).<br>Implemented using singly-linked list. Uses LIFO methodology.<br>No coalescing allowed; fast, but can cause short-term external fragmentation</td></tr><tr><td>Small Bins</td><td>For exact size classes (which are in multiple of alignment, up to some threshold).<br>Implemented using circular doubly-linked list.<br>Coalescing is allowed.</td></tr><tr><td>Large Bins</td><td>Used for serving big requests.<br>Implemented using doubly-linked list.<br>Uses fit-strategy to find the best chunk efficiently.</td></tr><tr><td>Unsorted Bins<br>(Cache Bins)</td><td>Acts as a temporary holding for newly freed chunks.<br>Helps in quick reuse and reduces bin searching overhead.<br>Implemented using doubly-linked circular lists.</td></tr></tbody></table>

## Fits Strategy

It refers to how the allocator chooses a free chunk from bins when multiple could work.

1. **First-fit**: pick the first sufficiently large chunk you find. Fast, but can cause uneven fragmentation.
2. **Best-fit**: search for the chunk closest in size to request. Reduces waste but costs more CPU (searching).
3. **Next-fit**: like first-fit but resume search where you left off. Spreads allocations, less clustering.

`dlmalloc` uses:

* **exact fits** in small bins.
* **best-fit within size range** for large bins (but not global best-fit, just best within that bin).

This hybrid gives both speed and decent fragmentation control.
