# Paging

_**August 11 and 12, 2025**_

## Why Pages?

Memory is **byte-addressable**. In 2025, most laptops at least comes with 8 GiB RAM. How many bytes does 8 GiB have?

* 1 GiB = 1024 MiB
* 1 MiB = 1024 KiB
* 1 KiB = 1024 bytes
* Therefore, 1 GiB = 1024 \* 1024 \* 1024 bytes = 1073741824 bytes.
* And, 8 GiB would be 8 \* 1073741824 = 8589934592 bytes or, \~8.6 billion bytes.

If we have to keep track of every byte in a flat table, it would have \~8.6 billion entries. And this is for 8 GiB RAM stick. The number would become crazy for higher valued RAMs.

So, the solution? Group these bytes. And the group of these bytes is came to known as a **page**.

Generally, a page is sized 4 KiB in modern Linux systems, though Linux supports huge pages as well. But we need not to worry about them yet. Plus, if you ask why a page is 4 KiB only? Its historical and technical as well. But we can avoid that for now.

4 KiB means 4 \* 1024 bytes or 4096 bytes. That means, a page is a gateway to 4096 unique byte-addressable locations.

Remember, the concept of pages exist in virtual memory only. The equivalent concept in physical memory is page frame, which we will talk about later.

## Page Table

A page table is a data structure that manages pages. That's it.

These page tables are then used by the memory management unit to translate virtual addresses to physical addresses.

Modern systems are based on 64-bit architecture, which have 64-bit wide addressable length.

* Virtual Addresses are large and if a single flat page table was used, it would be huge.
* Managing such a page table would be a nightmare.

To solve this problem, a hierarchical approach was implemented, which ensures that each access reduces the sample space of possibilities.

* The closest example that explains this problem is linear search.
* If there is a sorted array of 1,000 elements, and our element lies at index 762, we have to traverse 763 entries before we find our match.
* But binary search reduces this exponentially. In just 9 iterations, we will find our match. Roughly 1% of linear search. That's the same level of reduction we are talking about through paging.
* If you are wondering how binary search works, you can google it. In simple words, we divide the sample space in half and take the value at mid index. If the value at mid index is lesser than the target value, we have to search the upper half, otherwise, the lower half. We do this until the value at mid index becomes the target.

This hierarchical approach is what we call as 4-level paging.

## 4-Level Paging

In simple words, there are 4 levels and each level has a version of page table. These are structured in a way that as you move through these tables, you are reducing the sample space by multiple folds. Lets zero in and find out how it actually happens.

We will move from low to high because that is more logical and comprehensible.

1. Plain page table.
2. Page directory index table.
3. Page directory pointer table.
4. Page map level 4 table.

### Plain Page Table

A page is a collection of individual bytes. At basic, we are dealing with 4 KiB pages. So, a page is a collection of 4096 addressable bytes in virtual memory.

As named, a page table should be a collection of pages, right? Not really.

Page is just a conceptual term. It exist in theory only. What we really deal with is page frame in the physical memory. And, a page table is a collection of page frames. How many page frames, to be exact? The number is 512.

This number is obtained by dividing the page size by size of each entry, where size of each entry is given by the register width, which is 8 bytes on x64. So, we get, `4096/8`, giving us 512 entries. And this mathematics is applicable to rest of the tables as well.

***

Therefore, a plain page table is a collection of 512 page frames, or, each entry in a page table is a gateway to a page frame in the physical memory.

A page is sized 4096 bytes, so, a plain page table manages a total of `512 * 4096` bytes, which is `2097152` bytes.

### Page Directory Index Table (PDIT)

Each entry in this table is of type **page table**. Therefore, a page directory index table is a collection of 512 page tables, or, each entry in a page directory index table is a gateway to a page table.

A single page table manages a total of `2097152` bytes, so, a page directory index table would manage a total of `512 * 2097152` bytes, which is `1073741824` bytes.

### Page Directory Pointer Table (PDPT)

Each entry in this table is of type **page directory**. Therefore, a page directory pointer table is a collection of page directories.

It has 512 entries, each pointing to a separate page directory.

A page directory manages `1073741824` bytes. So, a page directory pointer table would manage a total of `512 * 1073741824` bytes, which is `549755813888` bytes.

### Page Map Level 4 (PML4) Table

Each entry in this table is of type PDPT.

A PDPT manages `549755813888` bytes. So, a page map level 4 table would manage a total of `512 * 549755813888` bytes, which is `281474976710656` bytes.

***

So these bytes look daunting. Lets simplify them.

1 KiB = 1024 bytes

1 MiB = 1024 KiB = 1024 \* 1024 bytes = 1048576 bytes

2 MiB = (2 \* 1048576) bytes = 2097152 bytes

1 GiB = 1024 MiB = (1024\*1024) KiB = (1024\*1024\*1024) bytes = 1073741824 bytes.

549755813888/1073741824 = 512 GiB

1 TiB = 1024 GiB = (1024\*1024) MiB = (1024\*1024\*1024) KiB = (1024\*1024\*1024\*1024) bytes = 1099511627776

281474976710656/1099511627776 = 256 TiB

Therefore:

| Page Tables                | Bytes Managed         | Simplified Size |
| -------------------------- | --------------------- | --------------- |
| Plain Page Table           | 2097152 bytes         | 2 MiB           |
| Page Directory Table       | 1073741824 bytes      | 1 GiB           |
| Page Directory Index Table | 549755813888 bytes    | 512 GiB         |
| Page Map Level 4 Table     | 281474976710656 bytes | 256 TiB         |

***

That's enough for paging. Lets talk about virtual addresses.

### But what really exist in these tables?

What we just had was a conceptual view of these page tables. But what do these page tables actually contain? That is important to understand, especially for the plain page table. Otherwise, it would lead to mental ruckus.

In simple words, all of them are pointer tables. And each address (pointer) is 64-bit, obviously.

* The PML4 table contains 512 pointers to page directory pointer tables.
* The page directory pointer table contains 512 pointers to page directory index/offset tables.
* The page directory index table contains 512 pointers to plain page tables.
* A plain page table contains 512 pointers to physical page frames.

The only important thing to understand here is the entries in the plain page tables.

A page table is a gateway to physical page frames. A page table entry looks like this:

```
*--------* *----------* *-------------* *-------------------* *---------------------*
| NX-bit | | CPU bits | | OS-Reserved | | Page Frame Number | Flags && Control Bits |
*--------* *----------* *-------------* *-------------------* *---------------------*
        63 62        59 58           52 51                 12 11                    0
```

If you are deep into the trenches, and constantly thinking, you will spot that something is missing. Let me tell you that something. _**How everything fits in the bigger picture?**_

## A Note

Before you start to wonder how these 4 page tables work together and stuff, I want to say, sit tight and enjoy the journey. Right now we don't know virtual addresses in-depth, which are essential to understand how all of this fits in.

Once we understand the virtual addressing system, we can hop on a process called **page walk**, which would piece everything we have understood so far together.

And the next thing we are going to study is exactly that.
