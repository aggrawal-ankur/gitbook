---
description: >-
  This article explores Executable & Linkable File Format (popularly known as
  ELF) and the lifecycle of processes in Linux
layout:
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: false
---

# Understanding ELF And Processes In Linux

The article is structured into three parts.

1. How the source code is compiled into an executable file?
2. What is an executable?
3. What is the lifecycle of a process in Linux?

## Part 1 - The Journey Of From Source Code To Executable

This is a simple C program

```c
// hello.c
#include <stdio.h>
​
void main(){
  printf("Hello, World!");
  return 0;
}
```

which we can compile using GNU C Compiler or `gcc` with the following command

```bash
gcc hello.c -o hello_executable
./hello_executable
​
Hello, World!
```

This simple process involves a lot of complexity, which is hidden under abstractions. The first thing we need to do is to remove this abstraction and understand what happens under the hood.

A source code becomes an executable file after following these 4 steps -

1. Preprocessing
2. Compilation
3. Assembling
4. Linking

Lets dive into each.

### Preprocessing

Every C code at least includes this one line, #include \<stdio.h>, where #include is a preprocessing directive.

These directives are needed to be processed (or extended) before we can move any further.

This preprocessing is carried out using `gcc -E hello.c -o hello.i`.

The file obtained here is an intermediate file with `.i` extension, which is a raw-c file with all the preprocessing directives resolved into actual references.

**Note:** If you look at `hello.i` and `stdio.h` simultaneously, you will find that it is not exactly copied. It is because the header file itself has got various macros. And the extension is based on those macros.

### Compilation

The intermediate C code is compiled into assembly instructions, which is the closest we can get to CPU yet retaining some readability.

The flavor of assembly (Intel or AT\&T) depends upon the assembler program used to compile the source code. For example,

* If GNU Assembler (or`as`) is used, it generates AT\&T assembly by default. Although it can be configured to generate Intel assembly as well. Same is followed by `gcc`.
* If netwide assembler (or`nasm`) is used, it generates Intel assembly.

The architecture specific things (x86 and x86\_64) are taken care by the assembler itself.

To compile intermediate C code into assembly code, we can run the following command:

```bash
gcc -S hello.i -o hello.s
```

### Assembling

The assembly code is converted into object code, or machine code. This is the actual code which gets executed on the CPU.

The object code can be obtained as:

```bash
gcc -c hello.s -o hello.o
# OR
as hello.s -o hello.o
```

Here, the assembly instructions are translated into binary opcodes (operation codes).

The file obtained in this step is an object file with `.o` extension.

Object files are strict in their structure. They follow a format known as **Executable File Format**, popularly known as ELF.

But this object file is not an executable yet. It needs to be linked.

### Linking

To give an object code execution power, we need to link it with specific libraries.

In the above program, we are using a function called `printf` for printing `Hello, World!` to the output.&#x20;

* Where is that function coming from? The header file!
* Where is the header file coming from? `glibc`!
* Where is `glibc`? Somewhere in the OS!

An object code has unresolved references to various library functions. Until these are resolved, how can you execute a file?

Linking can be static or dynamic. Both have their use cases.

Dynamic linking is the preferred linking mechanism by a compiler. But it can be used to statically link as well.

Now we are ready to execute our binary.

It is a surface level overview to what actually happens under the hood. We will dive deeper into this when we start reverse engineering. Until then, we have enough knowledge to move forward.

## Part 2 - Understanding An Executable

An executable file is a type of computer file containing instructions that the computer's processor can directly execute.

Executable files differ greatly on Windows and Linux. The reason is that both the environments are designed differently.

| Property                   | Windows                                      | Linux                                   |
| -------------------------- | -------------------------------------------- | --------------------------------------- |
| Binary File Format         | Executable and Linkable File Format (or ELF) | Portable Executable File Format (or PE) |
| File Extension             | No extension required                        | `.exe`, `.dll`                          |
| System Call Interface      | Linux System Calls (`syscall`)               | Windows NT syscall layer or WinAPI      |
| Dynamic Linker/Loader      | ld-linux.so                                  | Windows Loader                          |
| C Runtime Library          | GNU C Library (or `glibc`)                   | Microsoft C Runtime (`MSVCRT`)          |
| Linker                     | `ld`                                         | `link.exe`                              |
| Calling Convention         | System V AMD64 ABI                           | Microsoft x64 ABI                       |
| Format For Dynamic Linking | Shared objects (`.so`)                       | Dynamic Link Library (`.dll`)           |

This time, we are learning about Linux environment.

### Brief History

It is a common standard file format for executable files, object code, shared libraries, and core dumps on Linux.

It was first released in "_System V ABI, Release 4_".

In 1999, it was chosen as the standard binary file format for Unix and Unix-like systems on x86 processors by the 86open project.

### Modern ELF

ELF is a general-purpose file format in Linux ecosystem, which defines the structure for binaries, libraries, and core files.

It is used throughout the build and execution pipeline.

* Different "types" of ELF files (relocatable, executable, shared object, core) exist to serve different roles in this pipeline.
* These are typically created during specific phases.

### Structure Of An ELF File

Regardless of the type of ELF, the structure of an ELF file remains mostly the same.

An ELF file can be divided into 4 parts.

<table><thead><tr><th width="222">Part</th><th>Importance</th></tr></thead><tbody><tr><td>ELF Header</td><td>Identifies the file as ELF and file metadata.</td></tr><tr><td>Program Header Table</td><td>Used by the dynamic loader at runtime.</td></tr><tr><td>Section Header Table</td><td>Used by the linker at build time.</td></tr><tr><td>Data (segments/sections)</td><td>Includes things which are referred by the above 2 tables, such as, text (code), data (globals), bss (uninitialized data), and others.</td></tr></tbody></table>

Lets take an example to understand ELF.

```c
// hello.c
#include <stdio.h>
​
void main(){
  printf("Hello, World!");
  return 0;
}
```

The object code can be obtained by

```bash
gcc -c hello.c hello_object.o
```

Object files are binary representations of a program's source code, intended to be executed directly on a processor, which is why they are required to follow a consistent structure.

We can check the type of this object file.

```bash
file hello_object.o

hello_object.o: ELF 64-bit LSB relocatable, x86-64, version 1 (SYSV), not stripped
```

ELF is not reserved for executable files only. It is used by a variety of other files of the same genre, and object code (.o), shared object (.so) libraries are two of them.

ELF files aren't readable by a text editor. Therefore, we use some command line utilities. The two most widely used and versatile utilities are `objdump` and `readelf`. There exist other like `nm`, `xxd`, `hexdump` and so on.  And they'll be introduced as needed.













