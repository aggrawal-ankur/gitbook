# Deallocation

_**10 September 2025**_

***

Deallocation as a process can be divided into two parts.

1. Making the memory inaccessible.
2. Reclamation by kernel.

***

There are hundreds of process getting created and exiting simultaneously. All of them are accessing the same computer memory.

Although the virtual address space is quite large, the physical space is still limited. And the virtual space is mapped with the physical space by the MMU.

When a process used a part of memory and now it's time for deallocation, there can be two path. Either you zero the whole memory used by the process or you make it inaccessible.

* Path 1 sounds more safe as it ensures that there is no possibility of data leaks.
* Path 2 sounds more like a irresponsible way to handle memory. But is it really?

As we have seen before, there are hundreds of processes in action simultaneously. And their virtual address space do differs but at the end of the day, it is going to be mapped with physical memory.

When memory is constantly in use, it is so complex to leak data. It is highly unlikely that you won't find the memory location with some data on it, but the question is, how you are going to make sense of it? How you are going to establish the integrity that this data belongs to that process specifically?

* This is the reason that makes path 2 a clever way instead of an irresponsible one.
* Because deallocation will come at a cost. You have to put zero or any sentinel value on all the memory locations. While this is possible for smaller allocations, this can be really a resource exhausting take on deallocation.

That is why making memory inaccessible is cheaper and makes logically sense as well.

***

Now comes part 2, reclamation by the kernel.

When we call `free(ptr)`, it just tells the allocator that this part of memory can be reused by the process. The allocator marks this memory as free to use.

* This memory is still mapped in that process as it is allocated to it.
* The memory still has the contents but they aren't accessible (directly).
* `free(ptr)` never really frees anything in an absolute sense. It just makes the memory inaccessible **via usual means**.

As we know, there can be two ways in which dynamic memory is allocated, `brk()` and `mmap()`.

* For `brk()` based allocation, if the top of the heap is free, the allocator can move the program break back down and this is called as **heap trimming**. This part of heap is now unmapped and the kernel reclaims it instantly, mid-process.
* For `mmap()` based allocation, on a call to `free(ptr)` , the kernel calls `munmap()` , which stands for memory unmapping. And the kernel reclaims the memory instantly, again mid-process.
* Stack also grows automatically with page faults. if you don't use much of the space, the kernel can unmap and reclaim the space instantly.
* In all of these cases, the kernel destroys the part of the data structure which was accounting the memory allocation for that part in that process. Every region, stack/heap/mmap becomes unmapped and the memory is reclaimed. And the memory reclaimed is **no longer accessible via any means**.

***

When the process dies, the kernel destroys the entire data structure which was accounting the memory allocation for that process. Every region, stack/heap/mmap becomes unmapped and the memory is reclaimed.

When a new process spawns and demands memory, the kernel zeroes the memory before making it available for that process. This guarantees no cross-process leaks. Zeroing happens on demand, so idle freed pages aren’t wasted effort.



So effectively, there are two cases:

1. Freed but not reclaimed.
2. Freed and reclaimed.

And zeroing happens for inter-process, not intra-process.



