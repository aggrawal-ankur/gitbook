---
description: Now we are going to unleash into ELF structures.
---

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



**Note: The output of certain commands is slightly modified. Otherwise, it would be confusing to understand what it actually means.**

***

## Introduction To \`objdump\`

`objdump` or object dump, is a GNU development tool, which specializes in displaying information from object files.

Syntax of usage looks like: `objdump <elf_file> <flag(s)>`

It is a feature-rich tool. The ones that concern us include these:

```bash
objdump hello.o -D -M intel   # Complete disassembly using Intel syntax
objdump hello.o -t            # Symbol table
objdump hello.o -r            # Relocation entries
objdump hello.o -h            # Section headers
```

***

### Full Disassembly (-D)

It can be found here at [GitHub](https://github.com/hi-anki/reverse-engineering/blob/main/program1/assets/full_disasm_from_obj_code).

The full disassembly is 69 lines long. But wait, the assembly generated from source was only 29 lines long!

* As we have read before, assembling lays down the base at which linking can be performed.
  * Refer to [a-high-level-overview-of-build-process-in-c.md](../a-high-level-overview-of-build-process-in-c.md "mention")
* Our source is a tiny part of the picture.
* The instructions for printing the string are in the `.text` section, while the string itself is a read-only data and thus it is stored in the `.rodata` section.
* `.comment` and `.eh_frame` are compiler sections.

***

If you notice, there is no sign of "Hello, World!\n" in the disassembly.

* But, it is there in encoded form. And we can verify that.
* Strings are immutable, therefore, they must be in the `.rodata` section.
*   This is the `.rodata` section.

    ```bash
    Disassembly of section .rodata:

    0000000000000000 <.rodata>:
       0:	  48                   	rex.W
       1:	  65 6c                	gs ins BYTE PTR es:[rdi],dx
       3:	  6c                   	ins    BYTE PTR es:[rdi],dx
       4:	  6f                   	outs   dx,DWORD PTR ds:[rsi]
    ```

    ```bash
       5:	  2c 20                	sub    al,0x20
       7:	  57                   	push   rdi
       8:	  6f                   	outs   dx,DWORD PTR ds:[rsi]
       9:	  72 6c                	jb     77 <main+0x77>
       b:	  64 21 00             	and    DWORD PTR fs:[rax],eax

    # Offset  Machine Code          Disassembly
    ```
* Now visit this website [https://www.rapidtables.com/convert/number/ascii-to-hex.html](https://www.rapidtables.com/convert/number/ascii-to-hex.html) and paste `"Hello, World!\n"` there.
* In the bottom box, you can find a stream of characters as `48 65 6C 6C 6F 2C 20 57 6F 72 6C 64`.
* Visit an [ASCII to Hex reference](https://www.ascii-code.com/) table. And match the characters above in the `HEX` column with the `Symbol` column.
* `48(H) 65(e) 6C(l) 6C(l) 6F(o) 2C(,) 20(SP) 57(W) 6F(o) 72(r) 6C(l) 64(d)`&#x20;

***

### Symbol Table (-t)

```bash
SYMBOL TABLE:
0000000000000000      l          df        *ABS*       0000000000000000    hello.c
0000000000000000      l          d         .text       0000000000000000    .text
0000000000000000      l          d         .rodata     0000000000000000    .rodata
0000000000000000      g          F         .text       000000000000001a    hello
0000000000000000                           *UND*       0000000000000000    puts

# Value (Offset   Linker       Symbol    Section it    Size of symbol     Symbol name
# relative to     Visibility   Type      belongs to
# section)
```

* Since it is unlinked, the `00...` part in the first column is all about placeholders, which would be replaced at runtime.
* `l`: local; `g`: global.
  * Only `main` has global visibility, because we made it so.
* `df`: file definition (name).
  * Remember the `.file` directive?
* `*ABS*`: absolute section, not relocatable.
* `d`: section definition, marks the beginning of a section.
* `F`: a function. It is located within the `.text` section. The size is `1a` bytes or `0001 1010`, which is 26 bytes.
* `*UND*` refers to an undefined symbol which would be resolved at link time.
  * This is for the `puts` function which comes from `glibc`.

***

### Relocation Entries (-r)

```bash
RELOCATION RECORDS FOR [.text]:
OFFSET           TYPE              VALUE
0000000000000007 R_X86_64_PC32     .rodata-0x0000000000000004
000000000000000f R_X86_64_PLT32    puts-0x0000000000000004

RELOCATION RECORDS FOR [.eh_frame]:
OFFSET           TYPE              VALUE
0000000000000020 R_X86_64_PC32     .text
```

Relocations are instructions for the linker/loader program (`ld-linux.so`).

* In simple words, a relocation entry asks to replace the mentioned placeholder offset with the real address or offset for this symbol.
* The offset value is the position relative from the binary where the relocation is required.

***

### Section Headers (-h)

{% code fullWidth="false" %}
```bash
Sections:
Idx         Name             Size      VMA               LMA               File off     Algn
  0         .text            0000001a  0000000000000000  0000000000000000  00000040     2**0
                           └─ CONTENTS, ALLOC, LOAD, RELOC, READONLY, CODE
  1         .data            00000000  0000000000000000  0000000000000000  0000005a     2**0
                           └─ CONTENTS, ALLOC, LOAD, DATA
  2         .bss             00000000  0000000000000000  0000000000000000  0000005a     2**0
                           └─ ALLOC
  3         .rodata          0000000e  0000000000000000  0000000000000000  0000005a     2**0
                           └─ CONTENTS, ALLOC, LOAD, READONLY, DATA
  4         .comment         00000020  0000000000000000  0000000000000000  00000068     2**0
                           └─ CONTENTS, READONLY
  5         .note.GNU-stack  00000000  0000000000000000  0000000000000000  00000088     2**0
                           └─ CONTENTS, READONLY
  6         .eh_frame        00000038  0000000000000000  0000000000000000  00000088     2**3
                           └─ CONTENTS, ALLOC, LOAD, RELOC, READONLY, DATA

# Section   Section          Size in   Virtual Memory    Load Memory       Offset In    Alignment
# Index     Name             Bytes     Addrress          Address           File Where   Requirement
#                                                                          It Begins
```
{% endcode %}

`CONTENTS, ALLOC, LOAD, DATA, RELOC, READONLY, CODE` are flags.

* `CONTENTS`: has data in the file.
* `ALLOC`: should exist in memory at runtime.
* `LOAD`: should be loaded by the linker/loader program.
* `RELOC`: has relocation entries.
* `READONLY`: not writable.
* `CODE`: contains executable instructions.
* `DATA`: contains data.

The code section (`.text`) must be available at runtime, has dynamic entries which are required to be loaded by `ld-linux.so` and it obviously has data in it. Therefore, it has `CONTENTS, ALLOC, LOAD, DATA` flags.

***

What is `VMA` and `LMA` ?

* We are going to talk about this very soon, in a separate article.

***

Here comes the end of inspection through `objdump`. Next we are going to be using `readelf`.

## Introduction To \`readelf\`

`readelf` is a part GNU Binutils Project.

It's a versatile program that excels at parsing files with ELF structure.

Syntax of usage looks like: `readelf <elf_file> [flag(s)]`

And yes, it is feature-rich just like `objdump` . The ones that concern us now include these:

```bash
readelf hello.o -a            # Everything under one roof
readelf hello.o -h            # ELF headers
readelf hello.o -l            # Program headers
readelf hello.o -S            # Section headers
readelf hello.o -s            # Symbol table
readelf hello.o -r            # Relocation entries
```

```
$ readelf hello.o -a

ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              REL (Relocatable file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x0
  Start of program headers:          0 (bytes into file)
  Start of section headers:          536 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           0 (bytes)
  Number of program headers:         0
  Size of section headers:           64 (bytes)
  Number of section headers:         13
  Section header string table index: 12

Section Headers:
  [Nr] Name              Type             Address           Offset
       Size              EntSize          Flags  Link  Info  Align
  [ 0]                   NULL             0000000000000000  00000000
       0000000000000000  0000000000000000           0     0     0
  [ 1] .text             PROGBITS         0000000000000000  00000040
       000000000000001a  0000000000000000  AX       0     0     1
  [ 2] .rela.text        RELA             0000000000000000  00000168
       0000000000000030  0000000000000018   I      10     1     8
  [ 3] .data             PROGBITS         0000000000000000  0000005a
       0000000000000000  0000000000000000  WA       0     0     1
  [ 4] .bss              NOBITS           0000000000000000  0000005a
       0000000000000000  0000000000000000  WA       0     0     1
  [ 5] .rodata           PROGBITS         0000000000000000  0000005a
       000000000000000e  0000000000000000   A       0     0     1
  [ 6] .comment          PROGBITS         0000000000000000  00000068
       0000000000000020  0000000000000001  MS       0     0     1
  [ 7] .note.GNU-stack   PROGBITS         0000000000000000  00000088
       0000000000000000  0000000000000000           0     0     1
  [ 8] .eh_frame         PROGBITS         0000000000000000  00000088
       0000000000000038  0000000000000000   A       0     0     8
  [ 9] .rela.eh_frame    RELA             0000000000000000  00000198
       0000000000000018  0000000000000018   I      10     8     8
  [10] .symtab           SYMTAB           0000000000000000  000000c0
       0000000000000090  0000000000000018          11     4     8
  [11] .strtab           STRTAB           0000000000000000  00000150
       0000000000000013  0000000000000000           0     0     1
  [12] .shstrtab         STRTAB           0000000000000000  000001b0
       0000000000000061  0000000000000000           0     0     1
Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings), I (info),
  L (link order), O (extra OS processing required), G (group), T (TLS),
  C (compressed), x (unknown), o (OS specific), E (exclude),
  D (mbind), l (large), p (processor specific)

There are no section groups in this file.

There are no program headers in this file.

There is no dynamic section in this file.

Relocation section '.rela.text' at offset 0x168 contains 2 entries:
  Offset          Info           Type           Sym. Value    Sym. Name + Addend
000000000007  000300000002 R_X86_64_PC32     0000000000000000 .rodata - 4
00000000000f  000500000004 R_X86_64_PLT32    0000000000000000 puts - 4

Relocation section '.rela.eh_frame' at offset 0x198 contains 1 entry:
  Offset          Info           Type           Sym. Value    Sym. Name + Addend
000000000020  000200000002 R_X86_64_PC32     0000000000000000 .text + 0
No processor specific unwind information to decode

Symbol table '.symtab' contains 6 entries:
   Num:    Value          Size Type    Bind   Vis      Ndx Name
     0: 0000000000000000     0 NOTYPE  LOCAL  DEFAULT  UND 
     1: 0000000000000000     0 FILE    LOCAL  DEFAULT  ABS hello.c
     2: 0000000000000000     0 SECTION LOCAL  DEFAULT    1 .text
     3: 0000000000000000     0 SECTION LOCAL  DEFAULT    5 .rodata
     4: 0000000000000000    26 FUNC    GLOBAL DEFAULT    1 main
     5: 0000000000000000     0 NOTYPE  GLOBAL DEFAULT  UND puts

No version information found in this file.
```

The output is long but when we'll inspect a linked binary, the output would be huge. So, in comparison to that, the output of inspecting an object file through and elf parser like `readelf` is quite short.

Lets start understanding this output.

### ELF Headers

These headers include information (metadata) that identifies a file as an ELF.

`Magic` (magic number) is a stream of characters which are used to identify a file format or protocol.\
(Source [Wikipedia](https://en.wikipedia.org/wiki/Magic_number_\(programming\)))

* They are often placed at the beginning of a data stream and serve as a unique signature to indicate the type or origin of a data.
* For example, a PNG file typically starts with `89 50 4E 47 0D 0A 1A 0A`
* Here it is `7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00`
*   Here we have 16 pairs of hexadecimal digits, each representing 1-byte. Therefore, it is 16-bytes long.

    | Magic Number Part | Explanation                                                      |
    | ----------------- | ---------------------------------------------------------------- |
    | `7f 45 4c 46`     | This is an ELF file.                                             |
    | `02`              | Architecture is 64-bit (`01` for 32-bit).                        |
    | `01`              | Bits are stored in little-endian notation (`02` for big-endian). |
    | `01`              | Version, nothing interesting about it.                           |
    | `00`              | OS/ABI is System V                                               |
* `7f` is 127 in decimals, which is for `DEL` , which is a non-printable ASCII character. Each binary file format (like PNG, JPEG etc) uses a non-printable ASCII character so that the system can distinguish the file from a random text file. This non-printable character indicates that this is a structured file and the next 3 bytes will tell which structure it really uses.
* `45 4c 46` translates to `E L F` .

`Type` field explains the purpose of the ELF file.

* `CORE` (value 4).
* `DYN` (Shared object file), used by libraries (value 3).
* `EXEC` (Executable file), used by binaries (value 2).
* `REL` (Relocatable file), object code ready to be linked (value 1).

ELF headers is the first thing in an ELF file, which is why the entry point address is `0x0` .

Programs headers are created during linking, that's why there is `0` for the start, number and size of program headers.

No flags were provided so `0x0` in that.

Section headers are used by the linker during build time. Also, the assembling process lays down a basic section layout. That's why we are seeing values related to section headers.

* It starts from 536 bytes in the binary.
* Total 13 section headers.
* And their size is 64-bytes.

The size of this ELF header is 64 bytes.

* On 64-bit architecture, it is 64-bytes.
* On 32-bit architecture, it is 32-bytes.











