# Orientation

_**August 11, 2025**_

***

## Premise

It's complicated, so diving in directly is foolish. Therefore, here is a tasting of each concept.

## Physical Memory

1. **Byte-addressable**: each address refers to 1-byte.
2. **Flat address space**: goes from `0` to `total_bytes - 1`.
3. Linux abstracts physical memory into **page frames**.
4. Physical addresses aren't directly visible (and accessible). The visible addresses are in **virtual memory**.
5. Virtual addresses are mapped into physical address space by the Memory Management Unit (MMU).

## Virtual Memory

1. Every process is allotted a virtual address space, which gives a fake sense of owning all the memory.
2. Each process gets the same address layout, which gives predictability.
3. The addresses generally visible are from VAS.
4. MMU with the OS manages to translate these addresses to physical memory mappings.
5. Processes can't directly see each other's memory.
6. Virtual memory is divided into pages of 4 KiB (other configs also available, but 4 KiB is the most widely used).
7. Each page in virtual memory maps to a page in physical memory.

## Virtual Address Space

Address space is the set of all addresses available for a program to use.

MMU with the OS manages to translate these addresses to physical memory.

Virtual address space is split into _user space_ and _kernel space_.

1. User space is where the program runs.
2. Kernel space is where the OS runs.

## Page

A page is the smallest fixed-size chunk of memory that the CPU and the OS manages together.

In most modern x86-64 Linux systems: 1 page = 4 KiB (4096 bytes). There exist huge pages (2 MiB, 1 GiB) as well, but 4 KiB is the baseline.

Page size is a hardware choice, not just an OS thing.

Every virtual address is a part of some page.

Paging solves three problems:

1. Memory isolation → each process has its own mapping from virtual pages to physical frames.
2. Flexible allocation → you can give a process scattered physical memory but make it look contiguous.
3. Protection → per-page permissions: read, write, execute.

***

A **Page** is a portion of memory in the virtual address space. A **Page frame** is the portion of memory in the physical space that maps to a page in virtual space.

* Basically, **page** is a virtual memory term and **page frame** is a physical memory term.

***

**Page table** is a data structure that the MMU uses to translate an address in virtual space to its corresponding address in the physical memory space.

A **page table entry** (PTE) is a mapping record from a page to frame with permissions.

**MMU** is a piece of hardware that uses page tables to translate addresses.

***

A page fault occurs when the CPU tries to access a virtual address, but the page table entry for that address says:

1. the page is not present in RAM, or
2. the access violates permissions.

The CPU stops the instruction and hands control to the OS so it can handle the situation.

## Memory Size Unit

KB can be ambiguous as it may represent both the binary and the decimal representations, which vary greatly in terms of value.

* 1 KB is 1000 bytes while 1 KiB is 1024 bytes.

We will use the `i` ones because they are more relevant here.
