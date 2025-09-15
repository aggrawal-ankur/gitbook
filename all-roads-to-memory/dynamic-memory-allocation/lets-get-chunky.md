# Lets Get Chunky

_**15 September 2025**_

***

In brief, the whole story of dlmalloc revolves around chunks. And the story is quite big so we need a path to follow. Let's try to map the surface first.

## Clarity

DMA = "dynamic memory allocation"

process = "an executing binary"

"Chunkification" is not an actual term but I like to use it as it summarizes everything well.

***

## How chunks are formed?

When a process start to exist, it rarely requires DMA. There are shared libraries in the memory mapped region but that's not DMA.

When the code calls `malloc` , this is when the idea of DMA starts to exist **for that process**.

Suppose the ask was `malloc(20)`. We know that a pointer in heap is returned such that it is suitable for any built-in type.

We are asking for 20 bytes but memory is managed in terms of pages.

* The solution is simple. The kernel gives pages and the allocator divides them into chunks as required.
* Since the smallest page can be 1 page only, assuming 4 KiB size, for `malloc(20)` request, the allocator would receive 4 KiB of memory from the kernel, that is 4096 bytes.
* This 4096 bytes is our **arena**, the total unallocated pool of memory, that the allocator is now going to manage.

Since 20 bytes were requested, a chunk of 20 bytes will be carved out from the arena and will be allocated to the process.

* In this operation, the program break would be increased by 20 bytes. (_Remember, sbrk is page-granular not per malloc. So, this is just a simplification of the idea._)

Now we have 4076 bytes of unallocated memory and one **in-use chunk** of 20 bytes.

* That's how **the first in-use chunk** comes into existence for a process.

Suppose we had a few more allocations following,&#x20;

```
malloc(10);
malloc(15);
malloc(28);
malloc(22);
```

* A total of `110` bytes is request here. And we have plenty in the arena.
* After this allocation, we would have 3066 bytes of unallocated memory and **five in-use chunks** of varying size.

Now the process is coming to an end and we are freeing every allocation.&#x20;

```
free(20);
free(10);
free(15);
free(28);
free(32);
```

* and the process exited.

In this scenario, there were no free chunks and honestly, there was no need as well.

But, this was all theoretical. Can we visualize it? Off course, but on a condition.

## Visualizing Chunkification

To visualize this, we can use an ASCII drawing which represents byte addressable heap.

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

* Looks pretty, huh? I want a complement on this. Just kidding.
* If anyone is wondering how i obtained these upper scores (macron) and angles, checkout this article on Wikipedia, [Box-drawing characters](https://en.wikipedia.org/wiki/Box-drawing_characters). I first saw these characters in VS Code's terminal specifically in Kali Linux and ever since I can't get over how great they look.
* Anyways, back to the topic. Such diversions are healthy so yeah.

***

We know that kernel releases memory in terms of pages and the allocator manages them in chunks.

But drawing 4096 boxes is neither easy nor fruitful. So, we will assume that our first request to `malloc` got 100 bytes from the kernel and this would be our **arena**.

Let's start visualizing.

```
p = malloc(20);
q = malloc(10);
r = malloc(15);
s = malloc(18);
t = malloc(32);

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
|    |    |    |    |    | .t | // | // | // | // |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  91   92   93   94   95   96   97   98   99   100
```

There are five in-use chunks and 4 bytes of unallocated heap. We can consider those 4 bytes either as unallocated heap space or a free chunk.

Once we do free, we free everything and the memory comes back to its place. This proves that there was no need for "free chunks" at all.

This example was pretty straightforward and had no space for the real chaos. So, let's take another example which creates chaos but, I don't think it will be chaotic in front of such a beautiful ASCII. Anyways.

***

## Visualizing Chunkification - Part II

This time we will free memory in-between.

```
p = malloc(10);
q = malloc(20);
free(10);
r = malloc(30);
free(20);
s = malloc(32);
t = malloc(26);
```

The total allocation size is 118 bytes but we will require that much as memory is being freed in the middle. Let's jump right into it.

Remember, the arena is still 100 bytes.

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

```
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
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

* And that's how the first **free chunk** comes into existence.
* Now we have 1 free chunk of size 10 bytes and 1 in-use chunk of size 20 bytes.

Moving next comes `r`.

```
┌────┐────┐────┐────┐────┐────┐────┐────┐────┐────┐
|    |    |    |    |    |    |    |    |    |    |
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

Another free, `free(q)` and the state of memory becomes this:

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
|    |    |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  61   62   63   64   65   66   67   68   69   70
  .
  .
```

We already had a free chunk of `10` bytes and now we have another `20` bytes. Is there any point in keeping these chunks different? Can we bring them together, like collapse them into one? Off course we can do that.

* So now we have one big free chunk of size 30 bytes and one in-use chunk of 30 bytes.

Next we have `s`.

* We already had a free chunk but that free chunk is sized 30 bytes and we need 32.
* Since we can't use that free portion of memory, we have to allocate after `r`.

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
|    | .s |    |    |    |    |    |    |    |    |
└────┘────┘────┘────┘────┘────┘────┘────┘────┘────┘
  91   92   93   94   95   96   97   98   99   100
```

Next we have `malloc(26)`. This one is special as now we lack forward memory in our arena. Either we extend the arena and request more memory from kernel, but there is a free chunk of 30 bytes, so we carve 26 bytes out of it for `t`. And the final state of our arena would be:

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

Suppose we have to do `malloc(12)`. Although we have 12 bytes free, but sadly we can't utilize them. They are **fragmented**. This is what external fragmentation looks like.

Since we are assuming from so long, the C-Assembly connection and memory stuff, just visualize this at scale now.

* 1000 blocks of byte-addressable heap memory, of which 400 blocks (not chunks) are free to use and still you can't allocate 100 bytes in that arena because there is no one contiguous block of 100 bytes.
* And we have not even crossed 1 page. That's why, fragmentation is a real challenge for an allocator. And this was just external, there is internal as well but we can't see it until we factor in some rules.
