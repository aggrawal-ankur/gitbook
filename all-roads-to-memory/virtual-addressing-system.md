---
description: >-
  There were so many virtual prefixed concepts that they were driving me crazy.
  So to bring all of them together, I named this article virtual addressing
  system
---

# Virtual Addressing System

## A Virtual Address

Total number of bits we have are 64. But not all the 64-bits are required to manage addresses now. It would be huge to manage 2^64 addresses.

So, we stick to 48-bit virtual addresses. The rest of the 16-bits are sign extension of the 47th bit. We'll explore what that means in a while.

A virtual address is divided into several pieces. More precisely, the bits in the a virtual address are grouped together to represent different parts of the 4-level paging system that we have discussed previously.

At high level, a virtual address is structured like this:

```
+--------------+ +--------------+ +--------------+ +------------+ +--------------------------------+
| PML4: 9-bits | | PDPT: 9-bits | | PDIT: 9-bits | | PT: 9-bits | | Page Offset: 12-bits |
+--------------+ +--------------+ +--------------+ +------------+ +--------------------------------+
47            39 38            30 29            21 20          12 11                               0
```

### Why like this?

All the 4 page tables have 512 entries, which require a minimum of 9-bits to represent. So, 9-bits are reserved for them.

Page offset is the actual byte being addressed within a page. Since there are 4096 bytes in total, 12-bit are required at minimum to represent them.

## Some Good-To-Know Things

A virtual address is in big endian notation, so most significant bits are in left and least significant bits in the right.

As long as we are dealing with pen paper math, there is no need for bit shifts. But with programming, bit shifting becomes important for extracting values the right way and avoiding falling at edge cases.

Each process gets a virtual address space, which has 256 TiB worth of addressable space, most of which is empty. Yes, the calculation we have done previously is done for every process.

**Note: Addressable space ≠ Usable space.**

***

