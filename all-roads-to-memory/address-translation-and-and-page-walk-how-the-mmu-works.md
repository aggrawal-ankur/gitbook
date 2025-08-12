---
description: This is the exact moment we are preparing for.
---

# Address Translation && Page Walk: How The MMU Works?

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

## Address Translation

This process can be divided into an if-else chart.

When MMU receives a virtual address, first it checks the translation lookaside buffer

























