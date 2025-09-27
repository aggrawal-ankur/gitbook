---
title: Build Process In C
weight: 1
---

To compile this source, we can use a variety of compilers.

```c {filename="hello.c"}
#include <stdio.h>
​
int main(){
  printf("Hello, World!\n");
  return 0;
}
```

Here we are using `gcc`.

```bash
$ gcc hello.c -o hello_executable
$ ./hello_executable
​
Hello, World!
```

Although it looks simple, this process has four layers of hidden complexity. Let's peel them back to understand what happens under the hood.

A source code turns into an executable file through these four steps:

1. Preprocessing
2. Compilation
3. Assembling
4. Linking

Let's dive into each.

## Preprocessing

Every C program includes at least this line: `#include <stdio.h>`, where `#include` is a preprocessing directive.

These directives must be handled before we move further.

This preprocessing is carried out using:

```bash
gcc -E hello.c -o hello.i
```

This step produces an intermediate `.i` file, a raw C file where all preprocessing directives are resolved.

**Note:** If you look at `hello.i` and `stdio.h` side by side, you'll see it isn't a direct copy. That’s because the header file contains various macros, and preprocessing continues until all directives are resolved.

For more information on preprocessing, check out [preprocessing-directives.md](../x64-assembly/preprocessing-directives.md "mention").

## Compilation

The intermediate C code is compiled into assembly instructions—the closest we get to the CPU while still keeping it somewhat readable.

The assembly flavor (Intel or AT\&T) depends on the assembler used to compile the source code.

* If GNU Assembler is used, it generates AT\&T assembly by default. Although it can be configured to generate Intel assembly as well. Same is followed by `gcc`.
* If netwide assembler is used, it generates Intel assembly.

Architecture-specific details (x86 and x86\_64) are handled by the assembler.

To compile the intermediate C code into assembly code, we do:

```bash
gcc -S -masm=intel hello.i -o hello.s
```

## Assembling

The assembly code undergoes a transformation process that lays the foundation for linking. This involves several steps, including:

* Lexing and parsing the assembly source
* Encoding instructions into machine code
* Creating sections
* Resolving labels within the file
* Generating the symbol table
* Creating relocation entries for unresolved references
* Constructing ELF headers

The object code can be generated as:

```bash
gcc -c hello.s -o hello.o
```

The file produced in this step is an object file with a `.o` extension.

Object files are strict in structure and follow a format called the Executable and Linkable Format (ELF).

This object file isn’t an executable yet. It needs to be linked.

## Linking

To make the object code executable, we link it with the necessary libraries.

```bash
gcc hello.o -o hello_elf
```

In the above program, we are using a function called `printf` for printing `Hello, World!` to the output.

* Where is that function coming from? The header file!
* Where is the header file coming from? `glibc`!
* Where is `glibc`? Somewhere on the OS!

Object code contains unresolved references to various library functions. Until these are resolved, the file cannot be executed.

***

Linking can be static or dynamic, and both have their use cases.

Dynamic linking is commonly used, but we can also instruct the compiler to link statically.

Now the binary is ready to be executed.

```bash
$ ./hello_elf

Hello, World!
```

## A Misconception About GCC

GCC isn't just a compiler—it's actually a toolchain. If it were only a compiler, how could it assemble and link code?