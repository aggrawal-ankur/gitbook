---
id: 7f2ea64082764610b828b6935c4a15f1
title: Linking
weight: 5
---

***Originally written between late June and early July 2025***

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

---

Let's explore linking.

{{< doclink "a286b3f6fb904fd182774bb9217728b8" "" >}}
{{< doclink "2ad66852fa5e40f98cac9d758c95135f" "" >}}
{{< doclink "a27011754d064d3d809e59d9108a0ea8" "" >}}
{{< doclink "03ae9097699f47bcac2df5d89343591e" "" >}}
{{< doclink "21938857c7dd43e3becd500a422764a3" "" >}}
{{< doclink "37c3bf4339444f10afc641a908538316" "" >}}
{{< doclink "cea7ad0d7b744f2d90c08a19355bc07a" "" >}}