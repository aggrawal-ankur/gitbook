---
title: Lets Get Chunky
weight: 4
---

_**15 September 2025**_

***

In brief, the whole story of dlmalloc revolves around chunks.

## Clarity

DMA = "dynamic memory allocation"

process = "an executing binary"

"Chunkification" = not an actual term but I like to use it.

## How chunks are formed?

When a process start to exist, it rarely requires DMA.

When `malloc` is called for the first time, the idea of DMA starts to exist **for that process**.

We know that a pointer in heap is returned for each `malloc` request. The kernel releases memory in pages, the allocator processes them as _chunks_ and we get our requested bytes.

* The smallest page is 1 page, assuming 4 KiB of size, the allocator would receive at least 4 KiB of memory from the kernel at minimum, which is 4096 bytes.
* This 4096 bytes is our **arena**, the total unallocated pool of memory, that the allocator is now going to manage.
* **Note: 4096 bytes is a lot of memory so the allocator doesn't need to request the kernel every time there is a malloc request. Only when the arena is not sufficient to support allocation is when the allocator reaches the kernel.**

Let's take an example and visualize the theory.

***

## Visualizing Chunkification

_**Note 1: We are going to use ASCII Art to represent blocks in heap and 4096 bytes means 4096 blocks, which is too much and maybe an overkill. Therefore, for this experimentation, we are going to assume that the least the kernel can offer is "100 bytes", not 4096 bytes. This way, we can control the influx of information without losing context.**_

_**Note 2: This is just a simplified version of something that only exist in theory and there is no simple way to visualize it. The actual ground-level reality might differ because of "various rules". But the idea always remains like this. "We are not studying the wrong way, we are studying the way it becomes easy to comprehend and sets up a foundation which can handle chaos later, much better."**_

### The Playground

This is how our playground looks like.

```
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  1    2    3    4    5    6    7    8    9    10
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  11   12   13   14   15   16   17   18   19   20
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  21   22   23   24   25   26   27   28   29   30
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  31   32   33   34   35   36   37   38   39   40
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  41   42   43   44   45   46   47   48   49   50
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  51   52   53   54   55   56   57   58   59   60
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  61   62   63   64   65   66   67   68   69   70
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  71   72   73   74   75   76   77   78   79   80
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  81   82   83   84   85   86   87   88   89   90
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  91   92   93   94   95   96   97   98   99   100
```

I have used box-drawing characters to create this playground. You can check them out on [Wikipedia](https://en.wikipedia.org/wiki/Box-drawing_characters).

### Example 1

Suppose the process requests dynamic memory like this:

```
p = malloc(20);
q = malloc(10);
r = malloc(15);
s = malloc(18);
t = malloc(32);
```

The first request is for 20 bytes and the allocator asks the kernel to release memory and it gets a total of 100 bytes. The **arena** is established now.

The allocator carves a chunk of 20 bytes and returns a pointer to it to the process. **The first in-use chunk** came into existence.

Following the remaining four requests, a total of 95 bytes is allocated, which is shared by **5** i**n-use chunks** and 5 bytes of unallocated/free memory.

This is how it will look in our heap art:

```
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| p. |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  1    2    3    4    5    6    7    8    9    10
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    | .p |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  11   12   13   14   15   16   17   18   19   20
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| q. |    |    |    |    |    |    |    |    | .q |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  21   22   23   24   25   26   27   28   29   30
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| r. |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  31   32   33   34   35   36   37   38   39   40
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    | .r | s. |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  41   42   43   44   45   46   47   48   49   50
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  51   52   53   54   55   56   57   58   59   60
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    | .s | t. |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  61   62   63   64   65   66   67   68   69   70
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  71   72   73   74   75   76   77   78   79   80
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  81   82   83   84   85   86   87   88   89   90
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    | .t | // | // | // | // | // |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  91   92   93   94   95   96   97   98   99   100
```

_Unallocated and free bytes are represented using `//` and all the blocks between `p. to .p` belong to one chunk which is pointed by `p`._

Now the process is coming to an end and we are freeing every allocation.&#x20;

```
free(20); free(10); free(15); free(28); free(32);
```

* and the process exited.

In this scenario, there were no free chunks and honestly, there was no need as well.

This example was pretty straightforward and had no space for the real chaos. So, let's take another example which is slightly more real.

***

### Example 2

This time we will free memory in-between.

```
p = malloc(10);
q = malloc(20);
free(10);
r = malloc(30);
free(20);
s = malloc(32);
t = malloc(26);
u = malloc(12);
```

The total allocation size is 118 bytes but we will not need anything beyond 100 bytes as memory is being freed in the middle.

```
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| p. |    |    |    |    |    |    |    |    | .p |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  1    2    3    4    5    6    7    8    9    10
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| q. |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  11   12   13   14   15   16   17   18   19   20
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    | .q |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  21   22   23   24   25   26   27   28   29   30
  .
  .
```

Now we have to stop as there is a free instruction. On `free(p)` , the state of memory becomes this:

```asciidoc
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| // | // | // | // | // | // | // | // | // | // |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  1    2    3    4    5    6    7    8    9    10
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| q. |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  11   12   13   14   15   16   17   18   19   20
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    | .q |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  21   22   23   24   25   26   27   28   29   30
  .
  .
```

* And that's how the first **free chunk** comes into existence. This free chunk is sized 10 bytes.

Next comes `r`.

```
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| // | // | // | // | // | // | // | // | // | // |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  1    2    3    4    5    6    7    8    9    10
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| q. |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  11   12   13   14   15   16   17   18   19   20
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    | .q |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  21   22   23   24   25   26   27   28   29   30
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| r. |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  31   32   33   34   35   36   37   38   39   40
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  41   42   43   44   45   46   47   48   49   50
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    | .r |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  51   52   53   54   55   56   57   58   59   60
  .
  .
```

After `free(q)` , the state of memory becomes this:

```asciidoc
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| // | // | // | // | // | // | // | // | // | // |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  1    2    3    4    5    6    7    8    9    10
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| // | // | // | // | // | // | // | // | // | // |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  11   12   13   14   15   16   17   18   19   20
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| // | // | // | // | // | // | // | // | // | // |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  21   22   23   24   25   26   27   28   29   30
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| r. |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  31   32   33   34   35   36   37   38   39   40
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  41   42   43   44   45   46   47   48   49   50
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    | .r |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  51   52   53   54   55   56   57   58   59   60
  .
  .
```

We already had a free chunk of `10` bytes and now we have another `20` bytes. Is there any point in keeping these chunks different? Can we bring them together, like collapse them into one?

* The rule is simple, allocated chunks can be adjacent to each other, but a free chunk is always surrounded by in-use chunks. So, when an in-use chunk adjacent to a free chunk is freed, the 2 free chunks are **coalesced** to form one single chunk.&#x20;
* Now we have one free chunk of size 30 bytes and one in-use chunk of 30 bytes.

Next comes `s`.

* We already had a free chunk but that free chunk is sized 30 bytes and we need 32.
* So we have to allocate after `r`.

```asciidoc
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| // | // | // | // | // | // | // | // | // | // |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  1    2    3    4    5    6    7    8    9    10
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| // | // | // | // | // | // | // | // | // | // |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  11   12   13   14   15   16   17   18   19   20
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| // | // | // | // | // | // | // | // | // | // |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  21   22   23   24   25   26   27   28   29   30
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| r. |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  31   32   33   34   35   36   37   38   39   40
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  41   42   43   44   45   46   47   48   49   50
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    | .r |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  51   52   53   54   55   56   57   58   59   60
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| s. |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  61   62   63   64   65   66   67   68   69   70
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  71   72   73   74   75   76   77   78   79   80
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  81   82   83   84   85   86   87   88   89   90
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    | .s | // | // | // | // | // | // | // | // |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  91   92   93   94   95   96   97   98   99   100
```

Next we have `malloc(26)`.&#x20;

* The memory after `s` is insufficient so we have to request the kernel to allocated more memory.
* But there is a free chunk of size 30 bytes, we can use that chunk. But that chunk is more than what we need so we carve 26 bytes out of it for `t` and leave the rest as a free chunk.

And the final state of our arena would be:

```
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| t. |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  1    2    3    4    5    6    7    8    9    10
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  11   12   13   14   15   16   17   18   19   20
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    | .t | // | // | // | // |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  21   22   23   24   25   26   27   28   29   30
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| r. |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  31   32   33   34   35   36   37   38   39   40
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  41   42   43   44   45   46   47   48   49   50
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    | .r |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  51   52   53   54   55   56   57   58   59   60
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| s. |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  61   62   63   64   65   66   67   68   69   70
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  71   72   73   74   75   76   77   78   79   80
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  81   82   83   84   85   86   87   88   89   90
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    | .s | // | // | // | // | // | // | // | // |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  91   92   93   94   95   96   97   98   99   100
```

We have 3 in-use chunks, 1 free chunk and 1 unallocated memory (like free chunk only).

At last, we have to allocate 12 bytes for `u`.

* If you notice, the total size of free/unallocated memory is 12 bytes, precisely what we need, but it is "**fragmented**".
* This is what external fragmentation looks like. It wastes memory.

## External Fragmentation

This is a 15X16 grid, so 240 byte-addressable blocks in heap.

```
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
| .. | .. | .. | .. | .. | .. | .. | .. |    |    |    |    | .. | .. | .. | .. |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
| .. | .. | .. | .. |    |    |    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
|    |    |    |    |    |    | .. | .. | .. | .. | .. | .. | .. | .. |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
|    | .. | .. |    |    |    |    | .. | .. | .. | .. |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
|    |    |    |    |    |    | .. | .. | .. | .. | .. | .. | .. | .. | .. | .. |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
|    | .. | .. | .. | .. | .. | .. | .. | .. | .. | .. | .. | .. | .. | .. | .. |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
|    | .. | .. | .. | .. | .. | .. | .. | .. | .. | .. | .. | .. | .. | .. | .. |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
|    | .. | .. | .. | .. | .. | .. | .. | .. | .. | .. | .. | .. | .. | .. |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
|    |    |    |    | .. | .. | .. | .. | .. | .. |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
|    | .. | .. | .. | .. | .. | .. |    |    |    |    | .. | .. | .. | .. | .. |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
|    |    |    |    |    |    | .. | .. | .. | .. | .. | .. |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
|    |    |    |    |    | .. | .. | .. | .. | .. | .. | .. |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
|    |    |    |    |    | .. | .. | .. | .. | .. | .. |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
|    | .. | .. | .. | .. | .. | .. |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
| .. | .. | .. | .. | .. | .. |    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
```

The dotted blocks are reserved while the rest are free. Roughly 108 bytes are lying freely. This is almost half of the total available bytes, 45%. Yet if I want 50 bytes contiguously, that's not possible.

Now scale it to 8 GiB of RAM or more. This is how memory is wasted

This is external fragmentation in miniature.

And there are mechanisms to deal with it and this is what we are going to explore next.

## Conclusion

Use memory responsibly.

We saw memory allocation on surface and tried to picture it so that we can feel confident. And I am sure we are.

But how that allocation is actually managed by dlmalloc is still unknown. And to answer that, we have to get more chunky.

Basically, now we have to explore the real structure of a in-use and free chunks, as perceived by `dlmalloc` and how the concept of bins is applied to manage chunks efficiently.

Until then, bye bye.