---
id: 13e94d7a205c4b309f82d234663a8b8d
title: A Brief Introduction To ELF
weight: 2
---

***Originally written between late june and early july 2025***

***Polished on October 03, 2025***

---

An executable file is a computer file containing instructions that the computer's processor can directly execute.

ELF is a general-purpose file format in Linux ecosystem, which defines the structure for binaries, libraries, and core files.

It was first released in "_System V ABI, Release 4_". In 1999, it was chosen as the standard binary file format for Unix and Unix-like systems on x86 processors by the 86open project.

Executable files differ greatly on Windows and Linux as both the environments are designed differently.

## Linux vs Windows

| Property | Linux | Windows |
| :------- | :---- | :------ |
| Binary File Format    | Executable and Linkable File Format (ELF) | Portable Executable File Format (PE) |
| File Extension        | No extension required          | `.exe`                             |
| System Call Interface | Linux System Calls (`syscall`) | Windows NT syscall layer or WinAPI |
| Dynamic Linker/Loader | ld-linux.so                    | Windows Loader                     |
| C Runtime Library     | GNU C Library (`glibc`)        | Microsoft C Runtime (`MSVCRT`)     |
| Linker                | ld                             | `link.exe`                         |
| Calling Convention    | System V AMD64 ABI             | Microsoft x64 ABI                  |
| Format For Dynamic Linking | Shared objects (`.so`)    | Dynamic Link Library (`.dll`)      |

Different types of ELF files (relocatable, executable, shared object) exist for different purposes. But their structure remains largely the same.

## Structure Of An ELF File

It can be divided into 4 parts.

| Part | Importance |
| :--- | :--- |
| ELF Header | Identifies the file as ELF and file metadata. |
| Program Headers Table | Used by the dynamic loader at runtime. |
| Section Headers Table | Used by the linker at build time. |
| Data (segments/sections) | Includes things which are referred by the above 2 tables, such as code/data/bss and others. |

ELF files aren't readable by a general-purpsoe text editor. We use special programs like `objdump` and `readelf` for that purpose.

## ELF Types

We can check the type of a file using the `file` utility. It is designed to read certain bytes in a file to find the type of it.

### Object File

```bash
$ file hello_object.o

hello_object.o: ELF 64-bit LSB relocatable, x86-64, version 1 (SYSV), not stripped
```

| Value | Description |
| :---- | :---------- |
| LSB   | The binary follows `little-endian` format. For more information, check out the {{< doclink "297e81d11b3d4d169feb19f2c4ea66f5" "endian system" >}} article. |
| relocatable | The file is ready to be linked with shared libraries. *More on this later in the series.* |
| not stripped | The file contains stuff which is not necessary and can be removed safely. *More on this later in the series.* |
| version 1 (SYSV) | Uses System V AMD64 ABI. For more information, check out the {{< doclink "530165083f3f4ed2bd9156905c68f282" "calling conventions" >}} article. |
| x86-64 | Compiled for 64-bit Linux architecture. |

### Linked Binary

```bash
$ file hello_elf

hello_elf: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, not stripped
```

| Value | Description |
| :---- | :---------- |
| pie executable | The binary is position independent. For more information, check out the {{< doclink "98594536dd60406ca3820f14366503ac" "position independent code" >}} article.
| dynamically linked | The binary resolves references during runtime via an interpreter program, called `/lib64/ld-linux-x86-64.so.2`. |

***

Later we will explore ELF in-depth.

## Resources

1. This document from Linux Foundation is a formal document for ELF specification. It can be found at [refspecs.linuxfoundation.org](https://refspecs.linuxfoundation.org/elf/elf.pdf?utm_source=chatgpt.com)

2. The `<elf.h>` header file in C is another great source.

3. The man page for ELF, which can be accessed as `man 5 elf` locally or at [man7.org](https://man7.org/linux/man-pages/man5/elf.5.html?utm_source=chatgpt.com) is a great, straightforward, NO BS, quick-reference in my opinion.