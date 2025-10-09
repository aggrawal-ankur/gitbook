---
id: 7ca52ec23a2c419b8bae36efade4dae0
title: C Build Process
weight: 3
---

Programming languages are written in English, but the CPU understands machine code. The process that transforms a human readable C source into CPU understandable machine code is called **build process**.

Every language has a different build process.

C's build process is divided into 4 phases, where each phase requires a different tool to process the C source.
  - Preprocessing is carried out by a preprocessor.
  - Compilation is carried out by a compiler.
  - Assembling is carried out by an assembler
  - Linking is carried out by a linker.

When tools come together, they form a toolchain.
  - A toolchain is a set of software development tools that are used in sequence to create a software product. The output of one tool often serves as the input for the next, forming a "chain".
  - There are different toolchains for different purposes.

For example: GCC stands for "GNU Compiler Collection", which is the GNU toolchain for compilation utilities. It has `ccp` (preprocessor), `cc1` (compiler), `as` (assembler) and `ld` (linker).

On Debian, we can locate these tools at:
```bash
/usr/bin/x86_64-linux-gnu-cpp                  # Preprocessor
/usr/libexec/gcc/x86_64-linux-gnu/14/cc1       # Compiler
/usr/bin/x86_64-linux-gnu-as                   # Assembler
/usr/bin/x86_64-linux-gnu-ld                   # Linker
```

Let's dive into each phase with a simple C program.

```c {filename="hello.c"}
#include <stdio.h>
​
int main(){
  printf("Hello, World!\n");
  return 0;
}
```

## Preprocessing (WHAT HAPPENS HERE??)

Every C program includes at least this line: `#include <stdio.h>`, where `#include` is a preprocessing directive.

These directives must be handled before we move further.
```bash
gcc -E hello.c -o hello.i
```

This step produces an intermediate file with a `.i` extension. It is the raw C file where all the preprocessing directives are resolved.

Preprocessing directives resolve into header files, which may contain other preprocessing directives. So, it is a recursive process which happens until there is no more directive left. 

For more information, check out {{< doclink "42957ab7594145f0b492a14d2f38a783" "preprocessing directives" >}}

## Compilation (WHAT HAPPENS HERE??)

The intermediate C code is compiled into assembly instructions—the closest we can get to the CPU while still keeping it somewhat readable.

The assembly flavor (Intel or AT&T) depends on the assembler used to compile the source code.

* If GNU Assembler is used, it generates AT&T assembly by default. Although it can be configured to generate Intel assembly as well. Same is followed by `gcc`.
* If netwide assembler is used, it generates Intel assembly.

The architecture-specific details (x86 and x86_64) are handled by the assembler.

To compile the intermediate C code into assembly code, we do:

```bash
gcc -S -masm=intel hello.i -o hello.s
```

## Assembling (WHAT HAPPENS HERE??)

Assembly instructions are converted to actual machine instructions (binary opcodes). This process is called assembling.
  - For more information, check out the {{< doclink "773caf1fe02945b5bc61a332be9c90aa" "machine instructions" >}} write up.

The assembly code undergoes a transformation process that lays the foundation for linking. This involves several steps, including:

* Lexing and parsing the assembly source
* Encoding instructions into machine code
* Creating sections
* Resolving labels within the file
* Generating the symbol table
* Creating relocation entries for unresolved references
* Constructing ELF headers

The assembly code can be assembled as:

```bash
gcc -c hello.s -o hello.o
```
  - The file produced in this step is an object file with a `.o` extension.

Object files follow a strict structure called the Executable and Linkable Format (ELF).

Object files aren't executable. They need to be linked.

## Linking (WHAT HAPPENS HERE??)

Object code contains unresolved references to various library functions (like printf). Until these are resolved, the file cannot be executed.

To make the object code executable, we link it with external libraries.
```bash
gcc hello.o -o hello_elf
```

Linking can be static or dynamic, both having their use cases.

Dynamic linking is commonly used, but we can also instruct the compiler to link statically.

Now the binary is ready to be executed.

```bash
$ ./hello_elf

Hello, World!
```