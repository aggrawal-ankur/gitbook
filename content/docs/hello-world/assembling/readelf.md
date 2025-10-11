---
id: a0f32ecb875b466eb17cc08105d28a57
title: Introduction To readelf
weight: 2
---

`readelf` parse and interprets the an ELF in human-readable terms.

It can be used as:
```bash
readelf ELF_FILE FLAGS
```

It is as feature-rich as objdump. The ones that concern us include:
```bash
readelf hello.o -a      # Everything under one roof
readelf hello.o -h      # ELF headers
readelf hello.o -l      # Program headers
readelf hello.o -S      # Section headers
readelf hello.o -s      # Symbol table
readelf hello.o -r      # Relocation entries
```

Let's start with the file header.

## ELF Header (File Header)

This is the first piece of information in an ELF file.
```bash
$ readelf hello.o -h

ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 
  Class:                             ELF64
  Data:                              2`s complement, little endian
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
```

### Magic Number

`Magic` is a stream of characters used to identify a file format or protocol. ([Wikipedia](https://en.wikipedia.org/wiki/Magic_number_\(programming\)))

They are often placed at the beginning of a data stream and serve as a unique signature to indicate the type or origin of a data.
  - For example, a PNG file typically starts with `89 50 4E 47 0D 0A 1A 0A`.
  - For an ELF, it is `7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00`.

These are 16 pairs of hexadecimal digits, each representing 1-byte. Therefore, it is 16-bytes long.

| Magic Number Portion | Description |
| :--- | :--- |
| `7f 45 4c 46` | This is an ELF file.                      |
| `02`          | Architecture is 64-bit (`01` for 32-bit). |
| `01`          | Bits are stored in little-endian notation (`02` for big-endian). |
| `01`          | Version, nothing interesting about it.    |
| `00`          | OS/ABI is System V                        |

- Each binary file format (like PNG, JPEG etc) uses a non-printable ASCII character so the system can distinguish the file from a random text file as a random text file can't start with `DEL` unless manipulated.
- `7f` which is a non-printable ASCII character `DEL`, is reserved for ELF format. And `45 4c 46` translates to `E L F`.

### ELF Type

`Type` field specifies the purpose of the ELF file.

| Value  | Integer Value (used internally) | Description |
| :----- | :---- | :---- |
| `REL`  | 1 | Relocatable file, object code ready to be linked. |
| `EXEC` | 2 | Executable file, represents linked binaries. |
| `DYN`  | 3 | Shared object file, represents libraries. |
| `CORE` | 4 | Core dump, used in memory-analysis. |

### Entry Point, Program Headers and Flags

Entry point address is `0x0` because this is a relocatable file, i.e it can't be loaded in memory for execution.

Programs headers are created during linking, that's why there is `0` for the start, number and size of program headers.

No flags were provided so `0x0` in that.

### Section Headers

Assembling lays down a basic section layout. That's why section headers are present in the object file.
  - They start after 536 bytes in the binary.
  - Total 13 section headers.
  - Their size is 64-bytes.

### File Header Size

On 64-bit architecture, it is 64-bytes.

On 32-bit architecture, it is 32-bytes.

### Section Header String Table Index

Discussed in the section headers section below.

## Section Headers

Section are used to organize the ELF file. Section headers table contains metadata about these sections.

The output is formatted for readability.
```bash
$ readelf hello.o -S

Section Headers:
  [Nr] Name              Type        Address           Offset    Size              EntSize          Flags  Link  Info  Align
  [ 0]                   NULL        0000000000000000  00000000  0000000000000000  0000000000000000          0     0     0
  [ 1] .text             PROGBITS    0000000000000000  00000040  000000000000001a  0000000000000000  AX      0     0     1
  [ 2] .rela.text        RELA        0000000000000000  00000168  0000000000000030  0000000000000018   I     10     1     8
  [ 3] .data             PROGBITS    0000000000000000  0000005a  0000000000000000  0000000000000000  WA      0     0     1
  [ 4] .bss              NOBITS      0000000000000000  0000005a  0000000000000000  0000000000000000  WA      0     0     1
  [ 5] .rodata           PROGBITS    0000000000000000  0000005a  000000000000000e  0000000000000000   A      0     0     1
  [ 6] .comment          PROGBITS    0000000000000000  00000068  0000000000000020  0000000000000001  MS      0     0     1
  [ 7] .note.GNU-stack   PROGBITS    0000000000000000  00000088  0000000000000000  0000000000000000          0     0     1
  [ 8] .eh_frame         PROGBITS    0000000000000000  00000088  0000000000000038  0000000000000000   A      0     0     8
  [ 9] .rela.eh_frame    RELA        0000000000000000  00000198  0000000000000018  0000000000000018   I     10     8     8
  [10] .symtab           SYMTAB      0000000000000000  000000c0  0000000000000090  0000000000000018         11     4     8
  [11] .strtab           STRTAB      0000000000000000  00000150  0000000000000013  0000000000000000          0     0     1
  [12] .shstrtab         STRTAB      0000000000000000  000001b0  0000000000000061  0000000000000000          0     0     1

 Key to Flags:
   W (write), A (alloc), X (execute), M (merge), S (strings), I (info),
   L (link order), O (extra OS processing required), G (group), T (TLS),
   C (compressed), x (unknown), o (OS specific), E (exclude),
   D (mbind), l (large), p (processor specific)

There are no section groups in this file.
```

| Attributes | Description |
| :-------- | :---------- |
| [Nr] | Index value. |
| Name | An offset into the `.shstrtab` (section header string table), which stores the actual section names as strings. readelf uses this offset to locate and display the human-readable name of these sections.
| Type | The type of the section. |
| | `PROGBITS`: contains code/data from the source. |
| | `RELA`: relocation entries with addends. |
| | `BSS`: uninitialized data. |
| | `SYMTAB`: symbol table. |
| | `STRTAB`: string table. |
| | `NULL`: for alignment purposes as computers index from 0 and ELF has preserved that. This way, the actual sections start from 1. |
| Offset  | The position of a section inside the ELF. |
| Address | The virtual address at which the section is loaded inside the virtual address space. 00..00 denotes a placeholder value which needs to be relocated. |
| Size    | Size of the section in hexadecimal bytes. |
| EntSize | The size of each individual entry within a section, if the section stores uniform entries. Otherwise, it is 0. |
| Flags   | How the section should be treated in the memory. |
| Link    | Index of a related section. |
| Info    | Extra information. |
| Align   | Required alignment in the memory and/or file. We can gloss over it for now. |

---

If you notice, the `Name` field has entries of varied length. The `Name` field has to be long enough but the longest range is never utilized always. This leads to increase in size, which leads to wastage.
  - For example, the longest entry in the in the above output is 15 characters. We have 12 sections in total, so `12*15 = 180 bytes`.
  - `Name` has to be 15 characters long for each entry. But how many bytes we are actually using? 87 bytes only. 93 bytes are wasted space.

This was just one table. There are other tables which have similar varied length fields. This would waste a lot of memory.

The solution is to **minimize the maximum wastage.**
  - We create a **flat central string registry** and anyone can refer to it.
  - Keeping the central registry flat removes the space problem as strings would be null-terminated and the the null character would create the distinction.
  - Changing strings would also be easier as only one place would it require it.
  - We can remove these **central tables** when not required. This happens when you strip the binary to reduce its size for production use. Remember the `not stripped` part in the output of `file`? It is about such things only.

Therefore, the `Section header string table index: 12` entry in the ELF header specifies the index of the "section header string table" entry in the section headers table.

## Symbol Table

```bash
$ readelf object_code.o -s

Symbol table '.symtab' contains 6 entries:
   Num:    Value          Size  Type     Bind    Vis       Ndx  Name
     0: 0000000000000000     0  NOTYPE   LOCAL   DEFAULT   UND  
     1: 0000000000000000     0  FILE     LOCAL   DEFAULT   ABS  hello.c
     2: 0000000000000000     0  SECTION  LOCAL   DEFAULT     1  .text
     3: 0000000000000000     0  SECTION  LOCAL   DEFAULT     5  .rodata
     4: 0000000000000000    26  FUNC     GLOBAL  DEFAULT     1  main
     5: 0000000000000000     0  NOTYPE   GLOBAL  DEFAULT   UND  puts
```

We have explored this already.

---

We're done with object code analysis. Next is linked ELF.