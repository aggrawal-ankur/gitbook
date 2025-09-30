---
id: fa0c4991c33d40a09cd3b555bac74823
title: Address Translation
weight: 3
---

This is the exact moment we were preparing for.

_**August 12, 2025**_

***

## What Is MMU?

MMU stands for memory management unit, which is a hardware component in the CPU, that sits between.

* The **core** executing instructions (which always works in virtual addresses), and
* The **memory bus** (which only understands physical addresses).

Its entire reason to exist is to intercept every memory access and translate it from a virtual address to a physical address in real time, applying protection checks along the way.

So, MMU exists for one purpose, **address translation**.

Before we hop on address translation, we have to understand translation lookaside buffer.

## Translation Lookaside Buffer (TLB)

Translation Lookaside Buffer (TLB) is a specialized cache used by the CPU to speed up the process of translating virtual memory addresses to physical memory addresses.

It stores recently used address translations, allowing for quicker access if the same translation is needed again. Basically, it's a cache for page table entries.

Its primary function is to reduce the time it takes to access memory. A full 4-level page table walk would be very slow and come costly for every memory access.

For the time being, there is no need to dive further into it.

***

Lets understand address translation now.

## Address Translation

This process can be divided into an if-else chart.

When MMU receives a virtual address, first it checks the translation lookaside buffer.

* If it finds an entry which maps the input with a physical address, it is considered **TLB Hit** and translation is done instantly.
* If no mapping is found, it is a **TLB Miss.** The CPU has to do a page walk to find the mapping and possibly cache it.

Now the thing we were waiting for, page walk.

### Page Walk

There is a special purpose register called `CR3`. This register keeps the base address of PML4 table.

The OS loads CR3 with the **physical address** of the PML4 for that process. When the MMU needs to translate a virtual address, it reads `CR3` and gets the PML4 base physical address.

Side by side, the virtual address is parsed to obtain the first 9-bits (from MSB) which represent the PML4 entry this virtual address belongs to.

* The value obtained from these 9-bits is added to the base address of PML4 and the desired entry within the PML4 table is found.
* The desired entry is pointer to the PDPT table.&#x20;

Now we are at the base address of PDPT table.

* The next 9-bits of the virtual address are parsed to obtain the right index/offset in the PDPT table.
* This value is added to the base address and we are at the correct entry now. This entry is a pointer to PDIT table.

Now we are at the PDIT table.

* The next 9-bits of the virtual address are parsed to obtain the right index/offset in the PDIT table.
* The value is added to the base address and we are at the correct entry now. This entry is a pointer to the plain page table this address belongs to.

Now we are at the plain page table.

* The next 9-bits of the virtual address are parsed to obtain the right index/offset in the page table.
* The value is added to the base address and we are at the correct entry now. This entry is the address to the actual physical frame this address is mapped to.

The PTE entry is parsed and the bits 51 to 12 are extracted, which forms the page frame number.

* The page frame number is the base address of the 4 KiB physical frame.

Next, the last 12-bits of the virtual address are parsed to obtain the page offset.

* The page offset is the actual byte in the group of 4096 bytes (4 KiB frame) that the virtual address is mapped to.

The PFN and page offset are added to form the final **physical address**.

And the page walk is done.

***

After a successful page walk, the translation lookaside buffer is updated to contain this mapping for faster lookup.

What if the page walk failed?

* A page fault;