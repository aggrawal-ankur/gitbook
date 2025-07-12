# \`readelf\` Perspective

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

At last, we have this weird entry in the ELF headers, `Section header string table index: 12` . Lets not gloss over it as it contains an important design concept.

*   Just for the time being, run `readelf hello.o -S` . You can see an output like&#x20;

    ```
    Section Headers:
      [Nr] Name              Type             Address           Offset
           Size              EntSize          Flags  Link  Info  Align
      [ 0]                   NULL             0000000000000000  00000000
           0000000000000000  0000000000000000           0     0     0
      [ 1] .text             PROGBITS         0000000000000000  00000040
           000000000000001a  0000000000000000  AX       0     0     1
    ```
*   It is less formatted. After formatting, we will get something like this&#x20;

    ```
    Section Headers:
      [Nr]   Name    Type       Address           Offset    Size              EntSize          Flags  Link  Info  Align
      [ 0]           NULL       0000000000000000  00000000  0000000000000000  0000000000000000           0     0     0
      [ 1]   .text   PROGBITS   0000000000000000  00000040  000000000000001a  0000000000000000  AX       0     0     1
    ```
* Have a look at all of the attributes here. You will find that most of these attributes are having a fixed size. For example, the `Address` field is always made up of 16 hexadecimal digits, so as the `Size` field.
* The only field we are concerned about is the `Name` field. This field practically has no bounds. Name of a section has to be verbose for practical reasons. Verbosity often comes at the price of length. But, not all the fields need that much verbosity. For example, there is `.text` and `.rela.eh_frame` . This creates a tension.
* The `Name` field has to be long enough to contain the longest possible values. But the longest possible range is never really utilized fully. This leads to increase in size, which leads to wastage.
* For example, the longest entry in the "section headers" section in the output above  (`readelf -a`) is 15 characters long. We have 12 sections in total. `12*15 = 180 bytes` . `Name` has to be 15 characters long for each entry. On the contrary, how many bytes are actually used? `87 bytes` ONLY. `93 bytes` are wasted space.

***

* This was just one table. There are other tables as well which uses the same `Name` field and similar values. If separate tables were created, that would lead to an awful lot of wastage of space.
* If we have to change these name entries, we have to change it everywhere they are used. Imagine how much compute would get wasted just to manage these names.

***

* What is the solution? **Minimize the maximum wastage.**
* What if we create a **central name registry** and ask everyone to refer to it, instead of storing it individually?
* Only the central registry would have to face the space problem. This would drastically reduce the overall wastage of space.
* If any name needs a change, you have to change it once and it would be reflected everywhere else.
*   Plus, since these names are independent now, we can altogether remove these **central tables** when not required. You remember the output of `file`?&#x20;

    ```bash
    $ file hello.o

    hello.o: ELF 64-bit LSB relocatable, x86-64, version 1 (SYSV), not stripped
    ```
* This "not stripped" part is actually about removing stuff which is not really required. Removing these string tables is one of the things that happen when turning an elf from "not stripped" to "stripped".
* Why remove? Because these are required only by toolchains and during debugging. A binary ready for production doesn't really need it, which is why it is stripped.

***

* So, `Section header string table index: 12` means the section header string table, which contains string names to all of these sections in the section header, is at the 12th entry inside section headers table.

It was huge! Anyways, you can take some rest before continuing further.















