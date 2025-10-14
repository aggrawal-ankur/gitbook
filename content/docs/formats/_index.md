---
id: c0c11864d8c043429261974140250bca
title: Binary Object Formats
weight: 2
---

Continuing our journey from the build-execution pipeline in C, we know that exist

An *executable file* contains instructions that the computer's processor can execute directly.

Microsoft's Windows, Apple's MacOS and Linux based distributions are the three major operating systems in the OS market.

Microsoft's Windows and Apple's MacOS are proprietary software, which is why the boundary between the kernel and the operating systems feels blurred.

Linux, being open source, exposes the boundaries that proprietary systems conceal, hence the confusion.
  - Unlike Windows or macOS, where the kernel distinction is rarely discussed, Linux explicitly separates the kernel and the OS.

With Linux, you can easily draw the boundaries.
  - Ubuntu, Debian, Fedora, Arch, Gentoo; all are operating systems (or distributions, in Linux world) based on the "Linux kernel".

The kernel is the core engine of an operating system, which performs all the system tasks.
  - When we talk about running executables, it is the kernel that does it.

Every kernel perceives executables differently for historical and practical reasons.
  - The NT kernel of the Windows OS considers files with the PE format as an executable.
  - The XNU kernel of the Mac OS considers files with the Mach-O format as an executable.
  - The Linux kernel considers files with the ELF format as an executable.

Whether in reverse engineering or binary exploitation, the story revolves around these **executable files**.

Since every kernel has different standards, we need to understand these in order to do the work efficiently.

It is not a prerequisite to explore each format in-detail just to get started.

I use Debian 14, which is a Linux distribution. Therefore, I am starting with the ELF format.

## History

Early computers had no "executable file formats" in today's sense.

The first formal "executable file format" was originated from the "Bell Laboratories" in the 1970s for PDP-11 UNIX. It was called "*a.out*".
  - It was extremely simple, but had no support for future advancements.

In 1983, the successor of the `a.out` format was released. It was the common object file format (or COFF), designed by AT&T for their "System V Release 1 (SVR1)". System V (or SysV) refers to the family of Unix operating systems developed by AT&T.
  - COFF was designed to solve a.out's shortcomings but COFF itself had its own shortcomings.

In 1988, the engineers at the UNIX System Laboratories (USL) started working on a format which was "*extensible by design*". It was designed for the SysV lineup and released with SVR4 (UNIX System V Release 4). It was called the "*executable and linkable file format (or ELF)*".
  - ELF had potential to become a universal format for executable files.
  - Major vendors joined hands to develop ELF as an independent format for executable files.

Microsoft extended the existing COFF layout to support future advancements, prioritizing backward compatibility as market leaders.
  - This new format was called "*portable executable (PE) format*".
  - It was released in 1993 with Windows NT 3.1.

NeXT Inc., founded by Steve Jobs in 1985, worked on the NeXTSTEP OS. They developed their own format, called Mach-O. It was developed parallel to ELF and later incorporated in the MacOS ecosystem.

It is evident that **extensibility demanded by future advancements** was the driving factor for innovation here.

To understand why a.out and COFF lacked scalability and why modern formats like ELF and Mach-O are so extensible, we have to understand each format in-depth. It is an extremely rewarding but equally time taking process.
  - As discussed previously, we will stick to the ELF format for now.