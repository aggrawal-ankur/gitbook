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

---

We're done with object code analysis. Next is linked ELF.