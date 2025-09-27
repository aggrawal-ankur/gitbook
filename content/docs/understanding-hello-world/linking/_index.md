---
title: "Linking: Object Code To Executable Binary"
weight: 7
---

## Setup

We had the object code from previous step, which we can link in order to make it an executable.

```bash
gcc object_code.o -o linked_elf
```

This one is going to be quite lengthy. So, be prepared.

## Type Inspection

Lets start by inspecting the type of this file.

```bash
$ file linked_elf

linked_elf: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, not stripped
```

For comparison, this was the output for object code.

```bash
$ file object_code.o

hello.o: ELF 64-bit LSB relocatable, x86-64, version 1 (SYSV), not stripped
```

The first thing that is changed is `relocatable` is transformed into `pie executable`. This tells that the binary has got execution powers.

* The word `pie` matters here. It stands for **position independent executable**.
* A `pie executable` is loaded randomly in the memory. It is not fixed, unlike `non-pie executable` binaries.

It is `dynamically linked` . It means the ELF binary depends on external shared libraries that are loaded at runtime by the dynamic linker.

`interpreter /lib64/ld-linux-x86-64.so.2` is the program that helps the binary achieve its dynamic nature. It loads the shared libraries, resolves the cross-references and do so extra stuff we'll see very soon, which is very very interesting.

I have omitted the `BuildId` thing. It has no use.

`for GNU/Linux 3.2.0` means the binary was built targeting **Linux kernel version 3.2.0** as the minimum ABI (Application Binary Interface) compatibility level.

* It **can run** on Linux 3.2.0 or **any newer kernel**.
* It may **fail on older kernels** due to missing syscalls or ABI changes.

***

## What really happens during linking?

This question is really hard to answer for me at this point. Why not to see it directly?

## Macro Level Roadmap

Complete output of `readelf` can be found at [GitHub](https://github.com/hi-anki/reverse-engineering/blob/main/program1/assets/complete_elf_headers).

1. [step-1-analyzing-elf-headers.md](step-1-analyzing-elf-headers.md "mention")
2. Before moving to the next step, it would be nice to clear a doubt, if it exists. [full-disassembly.md](full-disassembly.md "mention")
3. The next step is analyzing program headers table but it has got some prerequisites.
   1. [part-ii-analyzing-section-headers.md](part-ii-analyzing-section-headers.md "mention")
   2. [a-brief-introduction-to-processes-in-linux.md](../a-brief-introduction-to-processes-in-linux.md "mention")
4. [step-2-analyzing-program-headers-table.md](step-2-analyzing-program-headers-table.md "mention")



