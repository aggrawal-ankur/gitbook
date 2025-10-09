---
id: 7ca52ec23a2c419b8bae36efade4dae0
title: C Build Process
weight: 3
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

`gcc` with `-E` does preprocessing only. Since it doesn't create a file, we have to pair it with `-o OUT_FILE.i` to cerate a file.
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

It is possible that you have heard the words assembler and linker. One step ahead, you might also know `as` and `ld`. But it is highly unlikely that you know the C preprocessor and compiler by their names (cpp and cc1).

It is because `as` and `ld` have use cases beyond the "toolchain" as well. They are very versatile and feature-rich solutions, and developers often crete their own toolchains based on their likings and needs and `as` or `ld` might fit their use case.

On the other hand, `cpp` and `cc1` are primarily designed for internal use. They might be tightly coupled with the GNU toolchain. But they are still available to be used independently and they work normal.

# Assemble

The assembler (as) translates the assembly generated after compilation into machine understandable operation codes (or opcodes).

Just like compilation, assembling also undergoes multiple steps, including:

- **Lexical analysis and parsing** of the assembly source is done and each line is broken into labels, mnemonics, operands, and directives. Assembly itself has no grammar/rules, but the syntax is validated against the targeted architecture's ISA.
- A **symbol table** is constructed to record all the labels and declared symbols. Unresolved external references are tracked and marked *undefined* for the linker.
- Instructions and data is organized in appropriate sections. And section metadata is generated.
- Each assembly instruction is translated into its binary machine-code form (opcodes + operands).
- Addressing modes are resolved if possible (when directives are used for addressing, instead of runtime addressing modes). Otherwise, relocation entries are created.
- For external symbols, whose runtime address is not known, relocation records are generated for the linker to fix later.
- EVerything (machine instructions and data organized in sections, symbol tables and relocation records) are packed into a relocatable object file.
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

If we have passed multiple files to `gcc` for preprocessing/compilation/assembling, separate files would be generated. But if you do linking as well, only one file is generated.

The linker takes one or more object files and generate a single executable file.

Linking also undergoes multiple steps, including:

- **Symbol resolution**, where all symbol definitions and external references are collected from each object file, resolves which reference points to which definition (functions, global data/variable) and their runtime addresses are resolved.
- **Relocations** adjusts these runtime addresses based on the relocation entries collected from each object file.
- Sections from every object file are merged together. One `.text`, one `.data`, one `.bss` and so on.
- Static and dynamic libraries are loaded so that references to library functions can be resolved.
- Relocation entries for library references are generated for the dynamic linker/loader program.
- Runtime structures (symbol tables, got/plt etc) and the final memory layout is generated.
- Everything is written to an executable file.

NEEDS CORRECTION

When we invoke the linker on the `.o` file generated previously,
```bash
$ ld hello_as.o -o hello_ld_exe

ld: warning: cannot find entry symbol _start; defaulting to 0000000000401000
ld: hello_as.o: in function `main':
hello.c:(.text+0xf): undefined reference to `puts'
```
... we get errors.

If we use gcc, we don't get any errors:
```bash
$ gcc hello_as.o -o hello_gcc_exec
```

Here comes the distinction. gcc is not a neat script that executes the four commands, it's an orchestrator.

There is a difference in how these phases exist independently and as "gcc".

## What is gcc about?