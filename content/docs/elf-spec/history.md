---
id: 1e2ab6d8f5fb40e697a446980aff3e3f
title: A Brief History
weight: 1
---

Early computers had no "executable file formats" in today's sense. 

The first formal "executable format" originated from "Bell Laboratories" in 1970s for PDP-11 UNIX. It was called `a.out`.
  - It was extremely simple, but had not support for future advancements such as virtual memory and shared libraries.

In 1983, the successor of the `a.out` format was released. It was common object file format (or COFF), designed by AT&T for their "System V Release 1". System V (or SysV) refers to the family of Unix operating systems developed by AT&T.
  - COFF was designed to solve a.out's shortcomings and be extensible. It provided richer metadata for compilers, debuggers and linkers.
  - But COFF itself had its shortcomings.

In early 1988, the engineers at the UNIX system laboratories (USL) started working on a format which was "*extensible by design*". They were designing it to be used in the SysV line up and was released with UNIX System V Release 4. It was called the executable and linkable file format (or ELF).
  - Other vendors (notably Intel) sensed a potential of ELF becoming a universal format for executable files.
  - Therefore, major hardware vendors joined hands to develop that format as an independent format for executable files.

Microsoft, on the other hand, extended the existing COFF layout to support future advancements as they were market leaders and can't afford to lose backwards compatibility. This new format came to known as the portable executable (PE) format. It was released in 1993 from Windows NT 3.1.

NeXT Incorporation, founded by Steve Jobs in 1985, worked on the NeXTSTEP OS. They developed their own format, called Mach-O, which was a descendent of the existing `a.out` format. It was developed parallel to ELF. Later it was incorporated in the MacOS ecosystem.

Therefore, there are major executable file formats, one for each ecosystem.
  - Windows uses PE (descendent of COFF).
  - UNIX OS and OS with Linux kernel uses ELF.
  - The Apple ecosystem has Mach-O.

It is noticeable that **extensibility demanded by future advancements** was the driving factor for innovation.

To understand why a.out and COFF lacked scalability and why modern formats like ELF and Mach-O are so extensible, we have to understand each format in-depth. It is a rewarding but equally time taking process.
  - The good part is that we need not to explore them all at once.
  - Each format is tightly coupled with its ecosystem. As long as we remain in one ecosystem, there is no need to learn any other format.

Right now, we will explore the ELF format in detail as we are in the Linux ecosystem.