---
description: Now we are going to unleash into ELF structures.
---

# Object Code Analysis

## What is object code?

Object code is a machine-readable representation of source code, typically the output of a compiler or assembler.

In Linux, it follows a specific file format, called **Executable and Linkable File** format.

To obtain object code for our source code, run

```c
gcc -c hello.c -o hello.o
```

We can start our analysis by inspecting the file type, using `file`.

```bash
$ file hello.o

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

We will inspect our file from the perspective of `objdump` and `readelf`. These are enough.

This section is long enough which is why it is divided into two separate articles, one is for `objdump` and the other one is for `readelf`.

1. [objdump-perspective.md](objdump-perspective.md "mention")
2. [readelf-perspective.md](readelf-perspective.md "mention")

**Note: The output of certain commands is slightly modified. Otherwise, it would be confusing to understand what it actually means.**
