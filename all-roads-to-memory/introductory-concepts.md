# Introductory Concepts

## Physical Memory

Byte-addressable: each address refers to 1-byte.

Flat address space: goes from 0 to (total\_bytes - 1).

Linux abstracts physical memory into pages.

Physical addresses aren't directly visible. The visible addresses are in virtual memory.

Virtual addresses are connected with physical address space by the Memory Management Unit (MMU).



## Virtual Memory

Every process is allotted a virtual address space, which gives a fake sense of owning all the memory.

The addresses generally visible are from this virtual address space.

MMU with the OS manages to translate these addresses to physical memory mappings.

Each process gets the same address layout, which gives predictability.

Processes can't directly see each other's memory.

Virtual memory is divided into pages of 4 KiB.

Each page in virtual memory maps to a page in physical memory or on disk (swap).

## Address Space (or Virtual Address Space)

Address space is the set of all addresses available for a program to use.

MMU with the OS manages to translate these addresses to physical memory.

### Spaces

Virtual address space is split into _user space_ and _kernel space_.

User space is where the program runs. Kernel space is where the OS runs.

Provides isolation and privilege control.&#x20;

Prevents accidental or malicious modification of OS memory.

## Page

A page is the smallest fixed-size chunk of memory that the CPU and the OS manages together.

In most modern x86-64 Linux systems: 1 page = 4 KB (4096 bytes). There exist huge pages (2 MB, 1 GB), as well, but 4 KB is the baseline.

The page size is a hardware choice, not just an OS thing.

Every virtual address is a part of some page.

Paging solves three problems:

1. Memory isolation → each process has its own mapping from virtual pages to physical frames.
2. Flexible allocation → you can give a process scattered physical memory but make it look contiguous.
3. Protection → per-page permissions: read, write, execute.

***

**Page** is a chunk of memory in virtual space. **Page frame** is the chunk of memory in the physical space that maps to a page in virtual space. Same size.

* Basically, page is a virtual memory term and page frame is a physical memory term.

***

**Page table** is a data structure that the MMU uses to translate an address in virtual space to its corresponding address in the physical memory space.

A **page table entry** (PTE) is a mapping record from a page to frame with permissions.

**MMU** is a piece of hardware that uses page tables to translate addresses.

***

A page fault occurs when the CPU tries to access a virtual address, but the page table entry for that address says:

1. the page is not present in RAM, or
2. the access violates permissions.

The CPU stops the instruction and hands control to the OS so it can handle the situation.
