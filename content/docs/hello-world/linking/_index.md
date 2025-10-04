---
id: 7f2ea64082764610b828b6935c4a15f1
title: Linking
weight: 5
---

***Originally written between late june and early july 2025***

***Polished on October 04, 2025***

---

The object code can be link as:
```bash
gcc hello.o -o hello_elf
```

Lets start by inspecting the file type.
```bash
$ file hello_elf

hello_elf: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, not stripped
```

`pie executable` means it can be loaded in the memory for execution.

`dynamically linked` means the binary on a dynamic linker/interpreter program to resolve symbol addresses. It is `interpreter /lib64/ld-linux-x86-64.so.2` here.

`for GNU/Linux 3.2.0` means the binary was built for **Linux kernel version 3.2.0** as the minimum ABI (Application Binary Interface) compatibility level.
  - It **can run** on Linux 3.2.0 or **any newer kernel**.
  - It may **fail on older kernels** due to missing syscalls or ABI changes.

## What happens in linking?

## High Level Roadmap Of Execution

1. Verification of magic.
2. Checking if the ELF can be loaded or not.
3. Locating program headers to know how to map the binary in the memory.

Let's explore linking.