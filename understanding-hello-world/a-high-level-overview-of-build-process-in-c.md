---
description: How does `gcc main.c -o main` works? That's what we are going to explore here.
---

# A High Level Overview Of Build Process In C

This article explores the C build process which is abstracted by the GNU C Compiler (or `gcc`) in one line, which is `gcc main.c -o main`.

This is a simple C program \~

{% code title="hello.c" %}
```c
#include <stdio.h>
​
int main(){
  printf("Hello, World!\n");
  return 0;
}
```
{% endcode %}

which we can compile using GNU C Compiler or `gcc` with the following command

```bash
$ gcc hello.c -o hello_executable
$ ./hello_executable
​
Hello, World!
```

This simple process involves a lot of complexity, which is hidden under 4 layers of abstractions. The first thing we need to do is to remove this abstraction and understand what happens under the hood.

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
gcc -S masm=intel hello.i -o hello.s
```

### Assembling

The assembly code undergoes a transformation process, which lay down a foundation for **linking** to work. Various steps are taken in this process. Some of them include:

* Lexing and parsing of assembly source.
* Instructions are encoded into machine code.
* Sections are created.
* Labels within the file are resolved.
* Symbol table is generated.
* Relocation entries are created for unresolved foreign references.
* ELF headers are constructed.

The object code can be obtained as:

```bash
gcc -c hello.s -o hello.o
# OR
as hello.s -o hello.o
```

The file obtained in this step is an object file with `.o` extension.

Object files are strict in their structure. They follow a format known as **Executable and Linkable File Format**, popularly known as ELF.

But this object file is not an executable yet. It needs to be linked.

### Linking

To give an object code execution power, we need to link it with specific libraries.

```
gcc hello.o -o hello_elf
```

In the above program, we are using a function called `printf` for printing `Hello, World!` to the output.&#x20;

* Where is that function coming from? The header file!
* Where is the header file coming from? `glibc`!
* Where is `glibc`? Somewhere in the OS!

An object code has unresolved references to various library functions. Until these are resolved, how can you execute a file?

Linking can be static or dynamic. Both have their use cases.

Dynamic linking is the preferred linking mechanism by a compiler. But it can be used to statically link as well.

Now we are ready to execute our binary.

```
$ ./hello_elf

Hello, World!
```

