# Free Chunk Management

_**17, 18, 19, 20 September 2025 (definitions taken out from a previous**_ [_**write up**_](https://ankuragrawal.gitbook.io/home/~/revisions/0fLrDsjrcXzDo0NctRkY/all-roads-to-memory/dynamic-memory-allocation/doug-leas-memory-model)_**, written on 11, 15, 16 September 2025, optimized)**_

***

In-use chunks are self-owned. Their bookkeeping lives in the chunk header itself and no external registry maintains them. Free chunks require management.

Let's explore how free chunks are managed by the allocator.

## Bins

A bin is a bucket for storing free chunks. Different buckets exist for different chunk size.

Bins are implemented using two data structures:

1. Linked Lists (Singly and Circular Doubly)
2. Bitwise Digital Trees

When chunks are not in use, they are treated as nodes of either of these.

Bins are categorized as following:

<table><thead><tr><th width="155">Name</th><th>Use</th></tr></thead><tbody><tr><td>Small Bins</td><td>For exact size classes (multiples of 8, up to 256 bytes).<br>Implemented using doubly-linked circular list.</td></tr><tr><td>Unsorted Bins<br>(Cache Bins)</td><td>Acts as a temporary holding for newly freed chunks. Helps in quick reuse and reduces bin searching overhead.<br>Implemented using doubly-linked circular lists.</td></tr><tr><td>Tree Bins<br>(Large bins)</td><td>Implemented using bitwise digital trees.<br>Used for managing very large size free chunks (typically > 256 bytes).</td></tr></tbody></table>

This categorization of bins helps balancing rapid allocation, memory usage and fragmentation.

**Note: v2.7.0 of dlmalloc used fast bins, but they were removed in v2.8.0. The last version of dlmalloc is v2.8.6, as per this repository on** [**GitHub**](https://github.com/DenizThatMenace/dlmalloc)**.**

## Structures In Account

We have 3 structs and some aliases to them for different use cases. The structs remains the same, only the naming changes so that it fits the context, that's it.

1. `malloc_chunk`: used for small size free chunks (by small bins).

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

2. `malloc_tree_chunk`: used for large size free chunks (by tree bins).

```c
struct malloc_tree_chunk {
  // Usual metadata from ll-chunks
  size_t prev_foot;
  size_t head;
  struct malloc_tree_chunk* fd;
  struct malloc_tree_chunk* bk;

  // Bookkeeping for trees
  struct malloc_tree_chunk* child[2];
  struct malloc_tree_chunk* parent;
  bindex_t index;
};

typedef struct malloc_tree_chunk  tchunk;
typedef struct malloc_tree_chunk* tchunkptr;
typedef struct malloc_tree_chunk* tbinptr;
```

3. `malloc_state`: The master record which manages everything for an allocator instance.

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

* `32U` means, take the value 32 as an unsigned integer.

## malloc\_state

The actual bins that manage free chunks are `smallbins[]` and `treebins[]` .

Using the two macros above, we can find the lengths of both the bins, i.e `smallbins[66]` and `treebins[32]`.

### Small Bins

Since small bins are implemented using circular doubly-linked list. We have to maintain two pointers, i.e `fd` and `bd` for each bin.

The small bin at 1-index is used for unsorted bin. So there will be 32 small bins and 1 unsorted bin.

Since array indices start from zero and we are counting bins from 1, for alignment purposes, the 0th element is sentinel and is not used.

Small bins manage fixed size chunks. Each small bin, `smallbin_1` to `smallbin_32` manage sizes in multiple of 8. Therefore, the `smallbins` array look something like this:

```c
smallbins = [
  0, ubin, fd_8, bk_8, fd_16, bk_16, fd_24, bk_24, fd_32,
  bk_32, fd_40, bk_40, fd_48, bk_48, fd_56, bk_56, fd_64,
  bk_64, fd_72, bk_72, fd_80, bk_80, fd_88, bk_88, fd_96,
  bk_96, fd_104, bk_104, fd_112, bk_112, fd_120, bk_120,
  fd_128, bk_128, fd_136, bk_136, fd_144, bk_144, fd_152,
  bk_152, fd_160, bk_160, fd_168, bk_168, fd_176, bk_176,
  fd_184, bk_184, fd_192, bk_192, fd_200, bk_200, fd_208,
  bk_208, fd_216, bk_216, fd_224, bk_224, fd_232, bk_232,
  fd_240, bk_240, fd_248, bk_248, fd_256, bk_256
]
```

What do these entries mean?

* Small bins are maintained using doubly-linked circular lists, so `fd_8` represents the first node in a linked list that links all the free chunks of size 8 bytes together. And `bd_8` represents the end of that same linked list.

The `malloc_chunk` struct has 4 `size_t` elements, which weigh 16/32 bytes on 32-bit/64-bit systems. The least memory you can request is 1 bytes, which would round up the chunk size to 24/48 bytes on 32-bit/64-bit system. That means, the small bins linking chunks of 8 and 16 bytes makes no sense?

* Yeah, that's right. But dlmalloc keeps that overhead for clarity and alignment purposes.
* Those bins are empty. And we will see this practically very soon.

***

When a chunk is freed, it goes into unsorted small bin. When multiple chunks are freed together, or there is no malloc request in between multiple frees, like this:

```
free(p);
free(q);

// or

free(a);
..
free(b);
..
free(c);
..
free(d);
```

* free chunks are inserted in the unsorted bin in LIFO order. So the last freed chunk is the first one.
* But popping doesn't follow LIFO. If 2nd chunk is found to be appropriate in a list of 5, the allocator manages linking/unlinking itself.

If the next malloc request finds nothing in the unsorted bin, every chunk is popped out and linked in the respective bins.

### Tree Bins

There are 32 tree bins in total. They manage chunks falling in a specific range of bytes. This range is obtained using power of 2.

Small bins manage size < 256 bytes. Everything after that is managed by tree bins.

256 is 2^8. So, the first range is 257-512 bytes (512 is 2^9). Similarly we have 513-1024, 1025-2048 bytes and so on.

Tree bins are implemented using bitwise digital trees. Every element in a tree bin is a pointer to the root node of the bitwise digital tree.

Linked List are fairly simple but bitwise digital trees are not. To understand them and visualize them, we have to practically see how a tree bin is managed by dlmalloc, which we will do very soon.

## Arena

The first malloc request sets up the arena.

Let's say we requested 10 bytes. The allocator is guaranteed to receive at least one page. On Linux, 4 KiB pages are more popular. So the allocator is guaranteed to setup an arena of at least 4096 bytes in in the first request.

Depending on the system (32-bit/64-bit), the allocator will carve a chunk of size 24/48 bytes because of double-word alignment rule. So a minimum of 4072/4048 bytes will be left unused in the arena.

These \~4k bytes are unallocated. Where do they live?

* Remember program break we read about in syscalls section? [Link](linux-syscalls-for-dma.md).
* The program break is just after the data segment. When we extend the heap, the kernel releases more memory than requested, and that memory is not used all at once, but it is allocated to the allocator.
* The program break is the partition between the used arena and the unallocated arena.
* When 24 bytes are used in the arena, the program break would be at the 25th bit.

The program break is a pointer to the next free byte in the arena. When there is no space left in the arena for the requested allocation, the allocator requests more memory from the kernel.

The `topsize` entry in `malloc_state` stores the size of the top chunk, which means the amount of unallocated space in the arena. `top` is a pointer to the first byte in the unallocated arena.

The allocator keeps requesting memory from the kernel when it runs out, the total memory ever requested by the allocator instance is recorded by the `max_footprint` declaration.

The `least_addr` declaration points to the lowest memory address in the arena.

`footprint_limit` is the user-defined ceiling on how much memory the allocator may request.

### Designated Victim

Many programs do repeated allocations of the same similar sizes. Designated victim is a recently freed chunk which is a part of small-medium size.

If a malloc request matches the the size of designated victim (`dvsize`), it saves the allocator some work by reusing the chunk pointer by `dv`.&#x20;

***

<table><thead><tr><th width="278">Declaration (in malloc_state)</th><th>Meaning</th></tr></thead><tbody><tr><td>binmap_t smallmap, treemap</td><td>An <code>unsigned int</code> (32-bit) value whose bits are masked to represent the state of small/tree bins. It is like a heat map for for bins, telling which one is free and which on has nodes in it.</td></tr></tbody></table>

## Rules For Coalescing

1. If the previous chunk is free, merge it with the current chunk. Use `prev_foot` to find the previous chunk’s size and adjust pointers.
2. If the next chunk is free (top chunk excluded), merge it with the current chunk. Remove the next chunk from its bin before merging.
3. If the next chunk is the **top chunk**, just extend the top chunk’s size instead of placing the chunk in bins.

If coalescing has happened, update the size field of the resulting chunk and insert it in appropriate bin.

If the coalesced chunk is larger than `dvsize`, may replace the designated victim.

## Fits Strategy

It refers to how the allocator chooses a free chunk from bins when multiple could work.

1. **First-fit**: pick the first sufficiently large chunk you find. Fast, but can cause uneven fragmentation.
2. **Best-fit**: search for the chunk closest in size to request. Reduces waste but costs more CPU (searching).
3. **Next-fit**: like first-fit but resume search where you left off. Spreads allocations, less clustering.

`dlmalloc` uses:

* **exact fits** in small bins.
* **best-fit within size range** for large bins (but not global best-fit, just best within that bin).

This hybrid gives both speed and decent fragmentation control.
