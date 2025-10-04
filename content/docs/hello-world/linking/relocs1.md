---
id: 37c3bf4339444f10afc641a908538316
title: Introduction To Relocation
weight: 6
---

***Originally written in July 2025.***

***Polished on October 04, 2025.***

---

## Why relocation?

We are using `printf()` to print `Hello, World!\n` in the output stream but we have not write the printf() ourselves. We use the standard I/O header file to access it.

`printf()` is just one thing. We are talking about the whole that infrastructure that runs C programs. How many functions that infrastructure would be made up of?
  - This is where shared libraries come.
  - Header files like standard I/O and math are just frontends that makes these functions available while writing source code.
  - At the end of the day, printf is also a code, which needs to undergo the same build process.
  - These functions exist in the form of shared libraries, which we link our binaries with.

Now we have access to these functions we have not written. Yet we can't use them because we don't know where they exist in the memory. To solve this problem, we have to resolve their actual runtime address.
  - This process of symbol resolution is called relocation.

## What is required for relocation?

1. The symbols whose runtime address is not known.
2. Relocation entries which define the metadata about these symbols.

## Symbol Table

A symbol table is a metadata table about symbols. There are two symbol tables in our binary: `.symtab` and `.dynsym`.

```bash
Symbol table '.dynsym' contains 7 entries:
   Num:     Value          Size  Type     Bind    Visibility   Ndx   Name
     0:  0000000000000000    0   NOTYPE   LOCAL   DEFAULT      UND   
     1:  0000000000000000    0   FUNC     GLOBAL  DEFAULT      UND   _[...]@GLIBC_2.34 (2)
     2:  0000000000000000    0   NOTYPE   WEAK    DEFAULT      UND   _ITM_deregisterT[...]
     3:  0000000000000000    0   FUNC     GLOBAL  DEFAULT      UND   puts@GLIBC_2.2.5 (3)
     4:  0000000000000000    0   NOTYPE   WEAK    DEFAULT      UND   __gmon_start__
     5:  0000000000000000    0   NOTYPE   WEAK    DEFAULT      UND   _ITM_registerTMC[...]
     6:  0000000000000000    0   FUNC     WEAK    DEFAULT      UND   [...]@GLIBC_2.2.5 (3)

Symbol table '.symtab' contains 36 entries:
   Num:     Value          Size  Type     Bind    Vis       Ndx   Name
     0:  0000000000000000    0   NOTYPE   LOCAL   DEFAULT   UND   
     1:  0000000000000000    0   FILE     LOCAL   DEFAULT   ABS   Scrt1.o
     2:  00000000000020ec   32   OBJECT   LOCAL   DEFAULT    19   __abi_tag
     3:  0000000000000000    0   FILE     LOCAL   DEFAULT   ABS   crtstuff.c
     4:  0000000000001080    0   FUNC     LOCAL   DEFAULT    14   deregister_tm_clones
     5:  00000000000010b0    0   FUNC     LOCAL   DEFAULT    14   register_tm_clones
     6:  00000000000010f0    0   FUNC     LOCAL   DEFAULT    14   __do_global_dtors_aux
     7:  0000000000004018    1   OBJECT   LOCAL   DEFAULT    26   completed.0
     8:  0000000000003dd8    0   OBJECT   LOCAL   DEFAULT    21   __do_global_dtor[...]
     9:  0000000000001130    0   FUNC     LOCAL   DEFAULT    14   frame_dummy
    10:  0000000000003dd0    0   OBJECT   LOCAL   DEFAULT    20   __frame_dummy_in[...]
    11:  0000000000000000    0   FILE     LOCAL   DEFAULT   ABS   hello.c
    12:  0000000000000000    0   FILE     LOCAL   DEFAULT   ABS   crtstuff.c
    13:  00000000000020e8    0   OBJECT   LOCAL   DEFAULT    18   __FRAME_END__
    14:  0000000000000000    0   FILE     LOCAL   DEFAULT   ABS   
    15:  0000000000003de0    0   OBJECT   LOCAL   DEFAULT    22   _DYNAMIC
    16:  0000000000002014    0   NOTYPE   LOCAL   DEFAULT    17   __GNU_EH_FRAME_HDR
    17:  0000000000003fe8    0   OBJECT   LOCAL   DEFAULT    24   _GLOBAL_OFFSET_TABLE_
    18:  0000000000000000    0   FUNC     GLOBAL  DEFAULT   UND   __libc_start_mai[...]
    19:  0000000000000000    0   NOTYPE   WEAK    DEFAULT   UND   _ITM_deregisterT[...]
    20:  0000000000004008    0   NOTYPE   WEAK    DEFAULT    25   data_start
    21:  0000000000000000    0   FUNC     GLOBAL  DEFAULT   UND   puts@GLIBC_2.2.5
    22:  0000000000004018    0   NOTYPE   GLOBAL  DEFAULT    25   _edata
    23:  0000000000001154    0   FUNC     GLOBAL  HIDDEN     15   _fini
    24:  0000000000004008    0   NOTYPE   GLOBAL  DEFAULT    25   __data_start
    25:  0000000000000000    0   NOTYPE   WEAK    DEFAULT   UND   __gmon_start__
    26:  0000000000004010    0   OBJECT   GLOBAL  HIDDEN     25   __dso_handle
    27:  0000000000002000    4   OBJECT   GLOBAL  DEFAULT    16   _IO_stdin_used
    28:  0000000000004020    0   NOTYPE   GLOBAL  DEFAULT    26   _end
    29:  0000000000001050   34   FUNC     GLOBAL  DEFAULT    14   _start
    30:  0000000000004018    0   NOTYPE   GLOBAL  DEFAULT    26   __bss_start
    31:  0000000000001139   26   FUNC     GLOBAL  DEFAULT    14   main
    32:  0000000000004018    0   OBJECT   GLOBAL  HIDDEN     25   __TMC_END__
    33:  0000000000000000    0   NOTYPE   WEAK    DEFAULT   UND   _ITM_registerTMC[...]
    34:  0000000000000000    0   FUNC     WEAK    DEFAULT   UND   __cxa_finalize@G[...]
    35:  0000000000001000    0   FUNC     GLOBAL  HIDDEN     11   _init
```

| Attribute  | Description |
| :--------  | :---------- |
| Num   | Index in the symbol table. |
| Value | Symbol's value (usually an address) |
| Size  | Size of the symbol in bytes |
| Type  | The kind of symbol (FUNC, OBJECT, SECTION, etc.) |
| Bind  | Symbol binding. How it is linked. |
| | LOCAL: Visible only within the object. |
| | GLOBAL: Externally visible and usable by others. |
| | WEAK: Like global but with lower priority. |
| Visibility/Vis | Symbol visibility. |
| | DEFAULT: Visible to all. |
| | HIDDEN: Internal, not exported. |
| | PROTECTED: Visible, but not preemptable. |
| Ndx (Section index) | The section the symbol is defined in. |
| | ABS: Absolute symbol, not tied to any section. |
| | INT_VALUE: The section it is defined in. |
| | UND: Undefined, needs relocation. |
| | COMMON: Uninitialized global symbol. |
| Name | Name of the symbol; An offset in the corresponding string table. |

### Purpose Of These Tables

| Table   | Purpose |
| :----   | :------ |
| .symtab | Full symbol table for internal use by the linker (or in debugging). Not needed at runtime. |
| .dynsym | Dynamic symbol table used by the dynamic linker at runtime (for symbols requiring relocation). |

### String Table

A string table is a central name registry.

| Symbol Table | Name Registry |
| :------ | :------ |
| .dynsym | .dynstr |
| .symtab | .symtab |

## Relocation Entries

Relocation entries are instructions for the linker/loader program (`ld-linux.so`).
  - A relocation entry asks to replace the mentioned placeholder offset with the real address offset the symbol.

There are two kinds of relocation entries.
  - Relocation with addend, `RELA`.
  - Relocation without addend, `REL`.

There are two relocation tables in our binary, `.rela.dyn` and `.rela.plt`.
  - `.rela.dyn` is used in eager binding.
  - `.rela.plt` is used in lazy binding.

These are the relocation entries in our binary.
```bash
$ readelf hello -r

Relocation section '.rela.dyn' at offset 0x550 contains 8 entries:
  Offset          Info            Type            Sym. Value     Sym. Name + Addend
000000003dd0  000000000008  R_X86_64_RELATIVE                      1130
000000003dd8  000000000008  R_X86_64_RELATIVE                      10f0
000000004010  000000000008  R_X86_64_RELATIVE                      4010
000000003fc0  000100000006  R_X86_64_GLOB_DAT  0000000000000000  __libc_start_main@GLIBC_2.34 + 0
000000003fc8  000200000006  R_X86_64_GLOB_DAT  0000000000000000  _ITM_deregisterTM[...] + 0
000000003fd0  000400000006  R_X86_64_GLOB_DAT  0000000000000000  __gmon_start__ + 0
000000003fd8  000500000006  R_X86_64_GLOB_DAT  0000000000000000  _ITM_registerTMCl[...] + 0
000000003fe0  000600000006  R_X86_64_GLOB_DAT  0000000000000000  __cxa_finalize@GLIBC_2.2.5 + 0

Relocation section '.rela.plt' at offset 0x610 contains 1 entry:
  Offset          Info           Type           Sym. Value       Sym. Name + Addend
000000004000  000300000007  R_X86_64_JUMP_SLO  0000000000000000  puts@GLIBC_2.2.5 + 0
```

| Attribute | Description |
| :-------- | :---------- |
| Offset | Location in the section where the relocation has to be applied. |
| Info   | Encodes relocation type and symbol index (high bits: symbol, low bits: type). |
| Type   | How to do relocation. |
| Sym. Value | The value of the symbol (from the symbol table), if applicable |
| Sym. Name  | Name of the symbol being relocated (can be empty for some types, like `RELATIVE`) |
| Addend | A constant value added to the relocation calculation. |

### Addend

An addend is a constant value added to the base address of a symbol during relocation to obtain the final runtime address required to be patched.

For simple variables and functions, addend is usually 0. But for complex structures and blobs, maybe a very specific part in that structure is required, rather than the full structure.
  - The offset you have to travel from the base address of that symbol to obtain that precise location is what an addend is.

When this addend is stored in the relocation entry, the dynamic linker computes the final value by combining the symbol address and the addend. Such relocation is called "relocation with addend, or RELA".

When this addend is embedded in the instruction/data itself and the relocation entry only tells the dynamic linker where to patch, such a relocation is called "relocation without addend, or REL".