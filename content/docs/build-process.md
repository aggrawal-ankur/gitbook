---
id: 7ca52ec23a2c419b8bae36efade4dae0
title: C Build Process
weight: 3
---

---

## Expectations

If we explore the C build process just **on surface**, that would save our time today, but will create headaches tomorrow.

It is not at all assumed that you understand every single word just by reading it. If something is unclear, don’t worry; subsequent write-ups will clarify it. The process is long, but well-discussed in the upcoming write ups.

Let's start our journey.

---

Programming languages are written in English, but the CPU understands machine code. The process that transforms a human readable source code into CPU understandable code is called **build process**.

Every language has a different build process.

C's build process is divided into 4 phases, where each phase builds on the top of the previous one and requires a different tool.
  - Preprocessing is carried out by a preprocessor.
  - Compilation is carried out by a compiler.
  - Assembling is carried out by an assembler
  - Linking is carried out by a linker.

When multiple tools work together in a particular sequence to achieve the desired output, they form a toolchain.

Different toolchains exist for different purposes. For example: GCC stands for "GNU Compiler Collection", which is the GNU toolchain for "compilation utilities".
  - Although gcc has `cpp` (preprocessor), `cc1` (compiler), `as` (assembler) and `ld` (linker) for the four phases of the build process, it is not limited to that.
  - Practically, it is an orchestrator that manages the builder process and provides some extra features, which we will discuss shortly.

## Locating these tools

On Debian, we can locate these tools at:
```bash
/usr/bin/x86_64-linux-gnu-cpp                  # Preprocessor
/usr/libexec/gcc/x86_64-linux-gnu/14/cc1       # Compiler
/usr/bin/x86_64-linux-gnu-as                   # Assembler
/usr/bin/x86_64-linux-gnu-ld                   # Linker
```

Other distributions of Linux might manage them differently.

---

Let's dive into each phase with a simple C program.

```c {filename="hello.c"}
#include <stdio.h>
​
int main(){
  printf("Hello, World!\n");
  return 0;
}
```

Usually we do
```bash
gcc hello.c -o hello
```
... and an executable file named `hello` is generated.

Let's see how we can use them individually.

## Preprocessing

Every C program starts with some `#` prefixed words. These are known as *preprocessing directives*.

The preprocessor (cpp) processes all these directives and prepare the code for compilation.

Each directive is processed differently, so preprocessing depends on what directives are in use.

The result of this process is an intermediate file with a `.i` extension. It transforms the original source code into extended/immediate source code.

`gcc` with `-E` does preprocessing only. Since it doesn't create a file, we have to pair it with `-o OUT_FILE.i` to create  a file.
```bash
gcc -E hello.c -o hello_cpp.i
```

We can invoke the preprocessor (cpp) independently as well. And it works identical.
```bash
/usr/bin/x86_64-linux-gnu-cpp hello.c
```

If we save the output of both the commands in a file using **output redirection**,
```bash
$ /usr/bin/x86_64-linux-gnu-cpp hello.c > hello_cpp.i
$ gcc -E hello.c > hello_gcc.i
```
... and run diff on both the files
```bash
$ diff hello_cpp.i hello_gcc.i
```
... two **immediate files** are generated but there is no output after diff, which indicates the files are identical.

## Compilation

The compiler (cc1) processes the **preprocessed C source** and generate the assembly code for the targeted architecture.

Compilation undergoes multiple steps including:

- **Lexical analysis (or Tokenization)**, where the compiler reads the preprocessed source as a stream of characters and breaks it into tokens (identifiers, keywords, literals, punctuations, operators and operands). It strips white spaces and comments are already removed in preprocessing.
- **Syntax analysis (or parsing)**, where these tokens are parsed according to the C grammar. The compiler generates a structured representation of the program, called **abstract syntax tree (AST)**. Syntax errors like *missing ;* are caught here.
- The AST undergoes **semantic analysis** where the compiler checks for language standards compliance, which includes type checking, use after declaration, scope and linkage rules, function signatures and returns, etc.
- An **intermediate representation (IR)** is generated from the AST, which is easier to optimize.
- The IR undergoes various **optimizations**, which can be controlled with the `-O` flag (-O0, -O1, -O2, -O3) etc.
- The assembly code for the targeted architecture is generated. Instructions, calling mechanisms, register usage etc are managed here. This creates a `.s` file.
- The assembly code may undergo some architecture-specific optimizations.

Modern IDEs come with languages server protocols (or LSPs), which parses the opened source code and runs lexical, syntax and semantic analysis on the source in real-time. That's how VS Code flags the missing semi-colon or any language standard violation.

We can invoke the compiler on the intermediate files generated previously,
```bash
$ /usr/libexec/gcc/x86_64-linux-gnu/14/cc1 hello_cpp.i
$ /usr/libexec/gcc/x86_64-linux-gnu/14/cc1 hello_gcc.i
```
... two new files named `hello_cpp.s` and `hello_gcc.s` are generated. They too are identical except the value for the `.file` directive.
  - Some output is generated on the terminal side as well, which is build time stats, which can be different.

`gcc` with `-S` can be used to:
  - preprocess and compile a `.c` file, or
  - compile a `.i` file.

If we compare the assembly files generated by `gcc` and `cc1`, only the `.file` directive line is different, which proves they are identical.

---

It is possible that you have heard the words "assembler" and "linker". One step ahead, you might also know `as` and `ld`. But it is highly unlikely that you know the C preprocessor and compiler by their names (cpp and cc1).

It is because `as` and `ld` have use cases beyond the "toolchain" as well. They are very versatile and feature-rich solutions, and developers often create their own toolchains based on their likings and needs and `as` or `ld` might fit their use case.

On the other hand, `cpp` and `cc1` are primarily designed for internal use. They might be tightly coupled with the GNU toolchain. But they are still available to be used independently and they work normal.

## Assemble

The assembler (as) translates the assembly generated after compilation into machine understandable instructions.

Just like compilation, assembling also undergoes multiple steps, including:

- **Lexical analysis and parsing** of the assembly source is done and each line is broken into labels, mnemonics, operands, and directives. Assembly itself has no grammar/rules, but the syntax is validated against the targeted architecture's ISA.
- A **symbol table** is constructed to records all the labels and declared symbols. Unresolved external references are tracked and marked *undefined* for the linker.
- Instructions and data is organized in appropriate sections. And section metadata is generated.
- Each assembly instruction is translated into its binary machine-code form (opcodes + operands).
- Relocation entries are created for instructions involving symbols whose runtime address is not yet known.
- Everything (machine instructions and data organized in sections, symbol tables and relocation records) are packed into a relocatable object file.
- The object file follows the ELF specification for its structure.

The assembler can be used on the `.s` file generated previously.
```bash
$ as hello.s -o hello_as.o
```

We can use `gcc` with `-c` to do the same.
```bash
$ gcc -c hello.s -o hello_gcc.o
```

With `-c`, gcc carries out:
  - preprocessing, compilation and assembling on `.c` files.
  - compilation and assembling on `.i` files.
  - assembling on `.s` files.

Running `diff` on both shows no difference. Also, the files sizes are the same, which proves they are identical.

## Linking

If we have passed multiple files to `gcc` for either preprocessing/compilation/assembling, separate files would be generated. But if you pass multiple files in the linking phase, they are properly joined/linked and one single executable file is generated.

The linker takes one or more object files and generates a single executable file. This executable file also follows the ELF specification.

Linking also undergoes multiple steps, including:

- Sections from all the object files are **merged and unified** sections (one for each, instead of separate) are created. Every instruction, symbol, relocation entry is assigned a virtual address and an offset within the unified layout.
- If a symbol's definition exists in the combined layout, the linker calculates its offset and patch all the references of it during link-time only.
- If a symbol's definition doesn't exist in the combined layout, and is meant to be resolved via dynamic libraries, the linker creates a **dynamic relocation entry** for the runtime linker/loader program to fix it.
- Instructions to load dynamic shared libraries at runtime are created as per the linker flags, so that references to library functions can be resolved at runtime.
- Various structures for runtime efficiency are generated and the final memory layout is created.
- Last, everything is written to an executable file.

When we use gcc, we don't get any error.
```bash
$ gcc hello_as.o -o hello_gcc_exec
```

But if we invoke the linker directly on the `.o` file generated previously,
```bash
$ ld hello_as.o -o hello_ld_exe

ld: warning: cannot find entry symbol _start; defaulting to 0000000000401000
ld: hello_as.o: in function `main':
hello.c:(.text+0xf): undefined reference to `puts'
```
... we get errors.

These errors exist because the linker doesn't magically knows which libraries you want to link your object code with.
  - The linker expects certain arguments/flags which gives that information.
  - This is the reason why `as` and `ld` are so versatile because they are not coupled with the GNU compilation toolchain.
  - Developers can use programs of their choice and still get the work done.

But newbies are far from this specificity. They need working solutions instead of customizations. That's where gcc comes in. GCC is an excellent orchestrator that smartly manages everything for you until you become capable to customize it.

Let's talk about `gcc` in brief.

## GCC as an Orchestrator

GCC, at its prime, is not just a compiler collection. It's a program that orchestrates multiple specialized tools in the build pipeline.

Its power lies in orchestration, not execution. It abstracts the complexity of the build pipeline while remaining open enough that advanced users can peek underneath, modify, or replace any stage when needed.

It's an excellent coordinator because it embeds vast range of intelligence about platform-specificity, toolchain, and language semantics.

It supports multiple languages like C, C++, Go, Ada, Fortran and Objective-C. You can mix and link across them because GCC knows how to unify them.

GCC can target architectures other than the host, that's why you can develop softwares for embedded systems without using an embedded system to develop them.
  - You can build binaries for 32-bit or even 16-bit sitting on a 64-bit architecture.
  - You can build binaries for ARM while on x86.
  - Is softwares for mobile built on mobile? No. Because the tools that build them are intelligent enough that they can build them without being on that exact architecture. GCC is one such tool.

If you use `-g`, GCC orchestrates the compiler and assembler to include magical information that streamlines the process of debugging. That magical information is known as DWARF/debug symbols, which is not a part of the build pipeline, but debug pipeline.

GCC also lets us optimize the code to an extent where multiple lines can be condensed into a bunch of assembly instructions.

We had errors running the linker but GCC doesn't because it passes the appropriate arguments and flags internally, intelligently, so that it can work without any issues.

There are other toolchains as well, but this was GCC for you.