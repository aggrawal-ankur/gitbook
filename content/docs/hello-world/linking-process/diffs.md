---
id: 3c66d1046644432f94ee90f8518d9216
---

# A Surface Level Overview Of The Differences

## Introduction

To use static linking on your object files, use the `-static` flag.

```bash
gcc hello.o -o dynamically_linked
gcc -static hello.o -o statically_linked
```

## ELF Size Difference

```bash
$ ls -l ./*_linked

-rwxrwxr-x 1 kali kali  15952 Aug  4 10:27 ./dynamically_linked
-rwxrwxr-x 1 kali kali 758424 Aug  4 10:27 ./statically_linked

$ ls -l ./*_linked -h

-rwxrwxr-x 1 kali kali    16K Aug  4 10:27 ./dynamically_linked
-rwxrwxr-x 1 kali kali   741K Aug  4 10:27 ./statically_linked
```

`(15952/758424)*100 = 2.1%`

The dynamically linked elf is just 2% of the size of the statically linked one.

## Disassembly Difference

```bash
objdump -D dynamically_linked > dyn_obj -M intel
objdump -D statically_linked > stat_obj -M intel
```

### Size Difference

```bash
$ ls -l ./*_obj

-rw-rw-r-- 1 kali kali   34436 Aug  4 10:40 ./dyn_obj
-rw-rw-r-- 1 kali kali 9892579 Aug  4 10:40 ./stat_obj

$ ls -l ./*_obj -h

-rw-rw-r-- 1 kali kali     34K Aug  4 10:40 ./dyn_obj
-rw-rw-r-- 1 kali kali    9.5M Aug  4 10:40 ./stat_obj
```

`(34436/9892579)*100 = ~0.35%`

The disassembly for the dynamically linked elf is \~0.35% of the total size of the statically linked one. That's not even 1%.

### Content Difference

The dynamically linked elf generates a disassembly of 801 lines, whereas the statically linked elf generated a disassembly of 187385 lines.

## \`readelf\` Interpretation

```bash
readelf ./dynamically_linked -a > dyn_read
readelf ./statically_linked -a > stat_read 
```

### Size Difference

```bash
$ ls -l ./*_read
-rw-rw-r-- 1 kali kali  15584 Aug  4 11:06 ./dyn_read
-rw-rw-r-- 1 kali kali 167259 Aug  4 11:06 ./stat_read

$ ls -l ./*_read -h
-rw-rw-r-- 1 kali kali  16K Aug  4 11:06 ./dyn_read
-rw-rw-r-- 1 kali kali 164K Aug  4 11:06 ./stat_read
```

`(15584/167259)*100 = 9.31%`

The output of readelf is significantly smaller for the dynamically linked elf.

### File Header


| Property | Dynamically Linked | Statically Linked |
| :--- | :--- | :--- |
| OS/ABI | UNIX - System V | UNIX - GNU |
| Type | ET_DYN | EX_EXEC |
| Entry Point Address | 0x1050 | 0x401600 |
| Start of Shdrs | 13968 | 756760 |
| Program Headers Count | 14 | 11 |
| Section Headers Count | 31 | 26 |
| Shstrtab Index | 30 | 25 |


The most interesting part here is the difference in ABI. This means, an operating system supports multiple ABI contracts?

* The GNU ABI is just an extension of the System V ABI.

### Section Headers

```bash
# Dynamically Linked          # Statically Linked
NULL                          NULL
.note.gnu.property            .note.gnu.property
.note.gnu.build-id            .note.gnu.build-id
.interp
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt                     .rela.plt
.init                         .init
.plt                          .plt
.plt.got
.text                         .text
.fini                         .fini
.rodata                       .rodata
                              rodata.cst32
.eh_frame_hdr
.eh_frame                     .eh_frame
                              .gcc_except_table
.note.ABI-tag                 .note.ABI-tag
                              .tdata
                              .tbss
.init_array                   .init_array
.fini_array                   .fini_array
                              .data.rel.ro
.dynamic
.got                          .got
.got.plt                      .got.plt
.data                         .data
.bss                          .bss
.comment                      .comment
.symtab                       .symtab
.strtab                       .strtab
.shstrtab                     .shstrtab
```

The statically linked ELF lacks these sections, which are mostly used by the dynamic interpreter program.

```bash
.interp
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.plt.got
.eh_frame_hdr
.dynamic
```

#### Why?

`.interp, .dynsym, .dynstr, .rela.dyn, .plt.got. eh_frame_hdr, .dynamic` are self-explanatory. These are specific to runtime resolution.

`.gnu.hash, .gnu.version, .gnu.version_r` are also runtime used during runtime resolution.

* To make symbol lookup fast, ELF uses hash tables for dynamic symbols.
* Since a static ELF has all the relocations performed during link-time, there is no need for a hash table for lookup.

These sections are new in the static ELF.

```
rodata.cst32
.gcc_except_table
.tdata
.tbss
.data.rel.ro
```

* We can avoid this for now.

***

Comparing the size for section headers,

| Header        | Dynamically Linked | Statically Linked |
| :--- | :--- | :--- |
| `.rela.plt`   | 0x18               | 0x210             |
| `.plt`        | 0x20               | 0xb0              |
| `.text`       | 0x103              | 0x74ff9           |
| `rodata`      | 0x12               | 0x1bba4           |
| `.eh_frame`   | 0xac               | 0xb800            |
| `.init_array` | 0x10               | 0x08              |
| `.fini_array` | 0x10               | 0x08              |
| `.got`        | 0x28               | 0x88              |
| `.got.plt`    | 0x20               | 0xc8              |
| `.data`       | 0x10               | 0x1a00            |
| `.bss`        | 0x08               | 0x5808            |
| `.symtab`     | 0x360              | 0xc3c0            |
| `.strtab`     | 0x1db              | 0x7c84            |
| `.shstrtab`   | 0x11a              | 0x00f0            |

Clearly, the size of major sections in a statically linked ELF Is much higher.

### Program Headers

```bash
# Dynamically Linked           # Statically Linked
PHDR
INTERP
LOAD                           LOAD
LOAD                           LOAD
LOAD                           LOAD
LOAD                           LOAD
DYNAMIC                        
NOTE                           NOTE
NOTE                           NOTE
NOTE                           NOTE
                               TLS
GNU_PROPERTY                   GNU_PROPERTY
GNU_EH_FRAME                   
GNU_STACK                      GNU_STACK
GNU_RELRO                      GNU_RELRO
```

Section to segment mapping also differs because of different sections.

The size of every program header varies a lot as well. Except `GNU_STACK`, which is unused in both.

### Dynamic Section

There is reason for it to be present in a statically linked ELF.

### Relocations

Since there is no dynamic section, `.rela.dyn` doesn't make any sense. It is also absent in the statically linked ELF.

There are 22 entries in `.rela.plt` and their type is `R_X86_64_IRELATIV`, which is a new relocation type. All of these entries are unknown, with no symbol name. Their `info` field also lacks symbol index.

### Symbol Tables

`.dynsym` as expected, absent. So as `.dynstr`&#x20;

`.symtab` , on the other hand, is heavily populated. It houses 2088 entries.

## Conclusion

A statically linked ELF is a self-contained ELF, and the high size of specific sections shows why it is called _a self-contained elf_.

Thanks. Bye.