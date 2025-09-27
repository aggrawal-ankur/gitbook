---
title: Doug Lea's Memory Model
weight: 3
---

_**11, 15, 17 September 2025**_

***


| Terminology | Meaning |
| :--- | :--- |
| Allocator Instance | Every process gets an instance of the allocator program,dlmallocin this case.It is the manager of dynamic memory for that process. It ensures that the process's ask for dynamic memory gets fulfilled. |
| Arena | The entire pool of memory managed by thedlmallocinstance for a process is called arena.It is not fixed. The kernel releases it as required. |
| Chunk | A chunk is the fundamental unit of memory indlmalloc.Chunks are of two types: in-use chunks and free chunks.The last chunk near the end of the heap (near the program break) is called thetop chunk. |
| Mmap'd Chunk | Requests above a certain threshold of size are handled by anonymous mapping in mmap region. Such allocations are called mmap chunks. |
| Bins | Bin is a strategy to manage free chunks.Implemented using linked lists. |
| Trees | Tree is strategy to manage large free chunks. |
| Splitting | When a big chunk is available but a small chunk is requested, the allocator carves the requested size out of the big chunk and leave the rest in bins. This is calledsplitting. |
| Coalescing | When the process frees an allocation, it makes the chunk available for reuse to the allocator. When such chunks are present adjacent to each other, they can be merged into one large free chunk. This is calledcoalescing. |
| Consolidation |  |
| Fragmentation | Wastage of memory. |
| External Fragmentation | Free memory exists but in pieces too small or scattered to satisfy a request.Example: you have three 1 KB holes but need 3 KB contiguous. |
| Internal Fragmentation | Memory inside an allocated chunk that the program doesn’t use.Example: the process asked for 13 bytes, allocator rounded up to 16. 3 bytes wasted in padding. |
| Trimming | Releasing memory from the top chunk back to the kernel.It prevents unbounded growth. |
| Fit Strategy | Refers to how the allocator decides which is the best chunk for a malloc request. |
