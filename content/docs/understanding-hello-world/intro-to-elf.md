---
title: A Brief Introduction To ELF
weight: 2
---

An executable file is a type of computer file containing instructions that the computer's processor can directly execute.

Executable files differ greatly on Windows and Linux. The reason is that both the environments are designed differently.

| Property                   | Linux                                        | Windows                                 |
| -------------------------- | -------------------------------------------- | --------------------------------------- |
| Binary File Format         | Executable and Linkable File Format (or ELF) | Portable Executable File Format (or PE) |
| File Extension             | No extension required                        | `.exe`, `.dll`                          |
| System Call Interface      | Linux System Calls (`syscall`)               | Windows NT syscall layer or WinAPI      |
| Dynamic Linker/Loader      | `ld-linux.so`                                | Windows Loader                          |
| C Runtime Library          | GNU C Library (or `glibc`)                   | Microsoft C Runtime (`MSVCRT`)          |
| Linker                     | `ld`                                         | `link.exe`                              |
| Calling Convention         | System V AMD64 ABI                           | Microsoft x64 ABI                       |
| Format For Dynamic Linking | Shared objects (`.so`)                       | Dynamic Link Library (`.dll`)           |

### Brief History

It was first released in "_System V ABI, Release 4_".

In 1999, it was chosen as the standard binary file format for Unix and Unix-like systems on x86 processors by the 86open project.

### Modern ELF

ELF is a general-purpose file format in Linux ecosystem, which defines the structure for binaries, libraries, and core files.

It is used throughout the build and execution pipeline.

* Different "types" of ELF files (relocatable, executable, shared object) exist to serve different roles in this pipeline.
* These are typically created during specific phases.

### Structure Of An ELF File

Regardless of the type of ELF, the structure of an ELF file remains mostly the same.

An ELF file can be divided into 4 parts.

<table><thead style="text-align:left"><tr><th width="222">Part</th><th>Importance</th></tr></thead><tbody><tr><td>ELF Header</td><td>Identifies the file as ELF and file metadata.</td></tr><tr><td>Program Header Table</td><td>Used by the dynamic loader at runtime.</td></tr><tr><td>Section Header Table</td><td>Used by the linker at build time.</td></tr><tr><td>Data (segments/sections)</td><td>Includes things which are referred by the above 2 tables, such as code/data/bss and others.</td></tr></tbody></table>

If you assembly this code and stop before linking, you'll get an object file.

```c {filename="hello.c"}
#include <stdio.h>
​
int main(void){
  printf("Hello, World!\n");
}
```

```bash
gcc -c hello.c hello_object.o
```

Object files are binary representations of a program's source code.

ELF is not reserved for executable files only. It is used by a variety of other files of the same genre, and object code (.o) & shared object (.so) libraries are two of them.

ELF files aren't readable by a text editor. Therefore, we use some command line utilities. The two most versatile utilities are `objdump` and `readelf`.

### Understanding The Result Of \`file\`

We can check the type of this object file using the `file` utility. It is designed to read certain bytes in a file to find the type of it.

```bash
$ file hello_object.o

hello_object.o: ELF 64-bit LSB relocatable, x86-64, version 1 (SYSV), not stripped
```

* `LSB` tells that the binary is structured in `little-endian` format, which means that the the least significant bit (or LSB) comes first.
  * It is different from `big-endian` where the MSB comes first.
  * In simple words, normal arithmetic is big-endian based and CPU arithmetic is little-endian based.
* `relocatable` means the file is ready to be linked with shared libraries but not for execution.
  * A relocatable ELF is one which has unresolved references to symbols whose definition lies in shared libraries.
  * For example, `printf` comes from `glibc`.
* `not stripped` means that the file still contains items which are not necessary and the code will still function the same if they are removed.
* `version 1 (SYSV)` means it uses System V AMD64 ABI (for conventions).
* `x86-64` tells we are on 64-bit Linux.

***

A linked binary file also follows the same structure. The above object file can be linked like this:

```bash
gcc hello_object.o -o hello_elf
```

Lets check this one.

```bash
$ file hello_elf

hello_elf: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, not stripped
```

* `pie executable` means position independent executable. No static locations are required.
* `dynamically linked` means the binary resolves references during runtime via an `interpreter` called `ld-linux.so` (can be different though).

***

Here comes the end of _a brief introduction to ELF._ Very soon we will explore it in depth.
