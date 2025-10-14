---
id: 404e85e72b324ae9b1e70330b5696f1d
title: Executable & Linkable File Format
weight: 2
---

---

## The Official Document ELF Specification

Before ELF existed as we know it, UNIX and UNIX-like vendors had their own tools for building a source into a binary. There was no interoperability.

With System V Release 4 (SVR4), the engineers at the UNIX System Laboratories (USL) worked on a format which was *scalable by design* to keep up with future advancements. This was non other than but ELF.

ELF had the potential to become a standard specification for all the vendors to follow, which could eliminate platform dependency and increase interoperability among the vendors.

Major hardware and software leaders came together and formed a committee to standardize the ELF format. This committee was known as the tool interface standards (TIS) committee.

TIS not just standardized ELF, but also standardized other specifications which directly or indirectly depended on the format of object files. For example, `TIS DWARF` standardized the format for debugging information.

All the information here is based on the official TIS ELF v1.2 document, which can be located at [refspecs.linuxfoundation.org](https://refspecs.linuxfoundation.org/elf/elf.pdf)

Let's start our journey.

---

## Introduction

An object file is a structured binary representation of a program.

The executable and linkable file format defines the structure for object files in the Linux ecosystem.

Every stage in the build-execution pipeline works with a different subset of this structure, which gives birth to different object files. Primarily there are 3 object file formats:
  - Relocatable object
  - Executable object
  - Shared libraries

Let's talk about these representations.

### Relocatable Object

### Executable Object

Statically and dynamically linked objects

### Shared Libraries

Dynamic (.so) and archived (.a) libraries.

---

Let's talk about the ELF standard now.

## ELF Standard

The ELF standard organizes an object file into multiple sections and associated metadata. It offers two views of that same layout, which are used at different stages in the build-execution pipeline.











## Resources

1. This document from Linux Foundation is a formal document for ELF specification. It can be found at [refspecs.linuxfoundation.org](https://refspecs.linuxfoundation.org/elf/elf.pdf?utm_source=chatgpt.com)

2. The `<elf.h>` header file in C is another great source.

3. The man page for ELF, which can be accessed as `man 5 elf` locally or at [man7.org](https://man7.org/linux/man-pages/man5/elf.5.html?utm_source=chatgpt.com) is a great, straightforward, NO BS, quick-reference in my opinion.