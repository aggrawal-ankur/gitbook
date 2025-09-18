# Free Chunk Management

_**17, 18 September 2025 (definitions taken out from a previous**_ [_**write up**_](https://ankuragrawal.gitbook.io/home/~/revisions/0fLrDsjrcXzDo0NctRkY/all-roads-to-memory/dynamic-memory-allocation/doug-leas-memory-model)_**, written on 11, 15, 16 September 2025, optimized)**_

***

Let's explore how free chunks are managed by the allocator.

Linked List and Trees are the two major data structures that dlmalloc utilizes to manage free chunks efficiently. When chunks are not in use, they are treated as nodes of either lists or trees.

## Bins

A bin is a bucket for storing free chunks. Different buckets exist for different chunks.

In-use chunks are self-owned. Their bookkeeping lives in the chunk header itself and no external registry maintains them.

Once a chunk is allocated, it disappears from the bin it was in. When an in-use chunk is freed, it re-enters the bin system.

Bins are implemented using two data structures:

1. Linked Lists (Singly and Circular Doubly)
2. Bitwise Digital Trees

Bins are categorized as following:

<table><thead><tr><th width="131">Name</th><th>Use</th></tr></thead><tbody><tr><td>Fast Bins</td><td>For small and fixed size ranges (e.g. 16-64 bytes).<br>Implemented using singly-linked list. Uses LIFO methodology.<br>No coalescing allowed; fast, but can cause short-term external fragmentation</td></tr><tr><td>Small Bins</td><td>For exact size classes (which are in multiple of alignment, up to some threshold).<br>Implemented using circular doubly-linked list.<br>Coalescing is allowed.</td></tr><tr><td>Large Bins</td><td>Used for serving big requests.<br>Implemented using doubly-linked list.<br>Uses fit-strategy to find the best chunk efficiently.</td></tr><tr><td>Unsorted Bins<br>(Cache Bins)</td><td>Acts as a temporary holding for newly freed chunks.<br>Helps in quick reuse and reduces bin searching overhead.<br>Implemented using doubly-linked circular lists.</td></tr><tr><td>Tree Bins</td><td>Implemented using bitwise digital trees.<br>Used for managing very large size free chunks.</td></tr></tbody></table>

&#x20;This categorization of bins helps balancing speed and memory usage.

## Structures In Account

Primarily we have 3 structures that are involved in all the heavy lifting. And we have different aliases to them for different use cases. The structs remains the same, only the naming changes so that it fits the context, that's it.

First we have `malloc_chunk`, which is used in managing free chunks via small bins.

```c
struct malloc_chunk {
  size_t prev_foot;
  size_t head;
  struct malloc_chunk* fd
  struct malloc_chunk* bk;
};

typedef struct malloc_chunk  mchunk;
typedef struct malloc_chunk* mchunkptr;
typedef struct malloc_chunk* sbinptr;
```

Second we have `malloc_tree_chunk`, which is used in managing free chunks via tree bins.

```c
struct malloc_tree_chunk {
  size_t prev_foot;
  size_t head;
  struct malloc_tree_chunk* fd;
  struct malloc_tree_chunk* bk;

  struct malloc_tree_chunk* child[2];
  struct malloc_tree_chunk* parent;
  bindex_t index;
};

typedef struct malloc_tree_chunk  tchunk;
typedef struct malloc_tree_chunk* tchunkptr;
typedef struct malloc_tree_chunk* tbinptr;
```

Third we have the master record which manages everything for an allocator instance, it is called `malloc_state`.

```c
struct malloc_state {
  binmap_t   smallmap;
  binmap_t   treemap;
  size_t     dvsize;
  size_t     topsize;
  char*      least_addr;
  mchunkptr  dv;
  mchunkptr  top;
  size_t     trim_check;
  size_t     release_checks;
  size_t     magic;
  mchunkptr  smallbins[(NSMALLBINS+1)*2];
  tbinptr    treebins[NTREEBINS];
  size_t     footprint;
  size_t     max_footprint;
  size_t     footprint_limit;
  flag_t     mflags;
  msegment   seg;
  void*      extp;
  size_t     exts;
};
```

We have a few type definitions to ensure size consistency across systems.

```c
typedef unsigned int bindex_t;
typedef unsigned int binmap_t;
typedef unsigned int flag_t;
```

At last, we have a few macros which define some constant values.

```c
#define NSMALLBINS   (32U)
#define NTREEBINS    (32U)
```

That's all we need to understand the process of managing free chunks.



















## Fits Strategy

It refers to how the allocator chooses a free chunk from bins when multiple could work.

1. **First-fit**: pick the first sufficiently large chunk you find. Fast, but can cause uneven fragmentation.
2. **Best-fit**: search for the chunk closest in size to request. Reduces waste but costs more CPU (searching).
3. **Next-fit**: like first-fit but resume search where you left off. Spreads allocations, less clustering.

`dlmalloc` uses:

* **exact fits** in small bins.
* **best-fit within size range** for large bins (but not global best-fit, just best within that bin).

This hybrid gives both speed and decent fragmentation control.
