# Object Code

## What is object code?

Object code is a machine-readable representation of source code, typically the output of a compiler or assembler.

In Linux, it follows a specific file format, called **Executable and Linkable File** format.

To obtain object code for our source code, run

```c
gcc -c hello.c -o hello.o
```

We can start our analysis by inspecting the file type, using `file`.

```bash
file hello.o

hello.o: ELF 64-bit LSB relocatable, x86-64, version 1 (SYSV), not stripped
```

* "ELF" means the file follows Executable && Linkable Format.
* "LSB" means it is in little-endian format.
* "relocatable" means that the file is ready to be linked and is not an executable yet.
* "x86-64" means it is compiled for 64-bit architecture.
* "SYSV" means it follows System V (five, not literal-v) convention.
* "not stripped" means that file still contains items which are not necessary and the code will function the same if they are removed.

***

Object files can't be opened with standard text editors as they are not designed for that purpose. To open them, we need specialized editors and parsers, which can read these files. These include:

1. Hex editors like `xxd` and `hexdump`.
2. Disassemblers, which convert machine code into readable assembly, like `objdump`, `ndisasm` and `ghidra`.
3. ELF parsers like `readelf` and `objdump`.

Lets inspect our object file using `objdump`.

***

## Introduction To \`objdump\`

`objdump` or object dump, is a GNU development tool, which is used to specializes in displaying information from object files.

Syntax of usage looks like: `objdump <elf_file> flag(s)`

It is a feature-rich tool. The ones that concern us include these:

```bash
objdump hello.o -D -M intel   # Complete disassembly using Intel syntax
objdump hello.o -d -M intel   # Disassembly of .text using Intel syntax
objdump hello.o -t            # Symbol table
objdump hello.o -r            # Relocation entries
objdump hello.o -h            # Section headers
```















