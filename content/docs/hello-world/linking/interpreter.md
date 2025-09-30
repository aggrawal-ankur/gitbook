---
id: 21938857c7dd43e3becd500a422764a3
title: "Step 4 : Interpreter In Action"
weight: 5
---

## Setup

This is the `.dynamic` section.

```
Dynamic section at offset 0x2de0 contains 26 entries:
  Tag                  Type             Name/Value
 0x0000000000000001    (NEEDED)         Shared library: [libc.so.6]
 0x000000000000000c    (INIT)           0x1000
 0x000000000000000d    (FINI)           0x1154
 0x0000000000000019    (INIT_ARRAY)     0x3dd0
 0x000000000000001b    (INIT_ARRAYSZ)   8 (bytes)
 0x000000000000001a    (FINI_ARRAY)     0x3dd8
 0x000000000000001c    (FINI_ARRAYSZ)   8 (bytes)
 0x000000006ffffef5    (GNU_HASH)       0x3b0
 0x0000000000000005    (STRTAB)         0x480
 0x0000000000000006    (SYMTAB)         0x3d8
 0x000000000000000a    (STRSZ)          141 (bytes)
 0x000000000000000b    (SYMENT)         24 (bytes)
 0x0000000000000015    (DEBUG)          0x0
 0x0000000000000003    (PLTGOT)         0x3fe8
 0x0000000000000002    (PLTRELSZ)       24 (bytes)
 0x0000000000000014    (PLTREL)         RELA
 0x0000000000000017    (JMPREL)         0x610
 0x0000000000000007    (RELA)           0x550
 0x0000000000000008    (RELASZ)         192 (bytes)
 0x0000000000000009    (RELAENT)        24 (bytes)
 0x000000006ffffffb    (FLAGS_1)        Flags: PIE
 0x000000006ffffffe    (VERNEED)        0x520
 0x000000006fffffff    (VERNEEDNUM)     1
 0x000000006ffffff0    (VERSYM)         0x50e
 0x000000006ffffff9    (RELACOUNT)      3
 0x0000000000000000    (NULL)           0x0
```

## Understanding the attributes

The `Tag` field identifies the purpose of each entry. It's an enum-like value defined in the ELF specification, used by the dynamic linker to understand what kind of information the entry holds.

The `Type` field again is an interpretation of the underlying unique numeric identifier which has a special meaning defined in the ELF specification. All in all, it identifies the type of entry.

The `Name/Value` field is the most complicated one here.

* When it comes to a shared library, this attribute holds a string name.
* When it comes to anything related to size, it stores a size.
* When it comes to offset, it stores `0x` prefixed addresses.
* It only stores offset or size. It is the elf-parser that resolves it to string names, if possible.

## Understanding Each Entry Type


|  |  |
|  |
| Tag | Purpose |
| NEEDED | Tells the linker a shared library is needed; value is offset into.dynstrpointing to the lib name (e.g."libc.so.6"). Multiple entries can exist. |
| INIT | Address of a function to run beforemain(). |
| FINI | Address of a function to run aftermain()returns, orexit()is called. |
| INIT_ARRAY | Address of an array of constructor function pointers to run beforemain()(more flexible thanINIT). |
| INIT_ARRAYSZ | Size in bytes of theINIT_ARRAY. |
| FINI_ARRAY | Address of an array of destructor function pointers to run on exit. |
| FINI_ARRAYSZ | Size in bytes of theFINI_ARRAY. |
| GNU_HASH | Address of the GNU-style hash table used for fast symbol lookup (alternative toHASH). |
| STRTAB | Address of the string table used for dynamic symbols (like lib names, function names). |
| SYMTAB | Address of the dynamic symbol table (function/variable names, sizes, bindings). |
| STRSZ | Size in bytes of the string table pointed to bySTRTAB. |
| SYMENT | Size of each symbol table entry. |
| DEBUG | Reserved for debugger use; ignored at runtime. |
| PLTGOT | Address of the Global Offset Table (GOT) used for dynamic symbol resolution. |
| PLTRELSZ | Size in bytes of the.rela.pltsection. |
| PLTREL | Type of relocation used in the PLT (RELAorREL). |
| JMPREL | Address of relocation entries for procedure linkage table (PLT) — e.g..rela.plt. |
| RELA | Address of relocation entries with addends — e.g..rela.dyn. |
| RELASZ | Size in bytes of the.rela.dynsection. |
| RELAENT | Size of each entry in.rela.dyn. |
| FLAGS_1 | Flags providing additional behavior control to the dynamic linker (e.g.DF_1_NOW,DF_1_GLOBAL). |
| VERNEED | Address of the version dependency table (which symbol versions are needed from shared libs). |
| VERNEEDNUM | Number of entries in the version dependency table. |
| VERSYM | Address of the version symbol table — gives the version of each symbol in the symbol table. |
| RELACOUNT | Number ofRELArelocations not part of PLT — for optimization. |
| NULL | Terminator— marks the end of the dynamic section. No further entries are processed after this. |


Lots of information we have no idea about. Don't stress about it. We will go through everything. Nothing would be left.

## How does the interpreter reads them?

First, it walks through each entry until it hits the `NULL` termination entry. And stores pointers to key entries for later use.

Second, all the entries of type `NEEDED` refers to the shared libraries, so it reads the name of the library from `.dynstr` table and loads the shared library. And it handles transitive dependencies recursively..

Third, it maps relocation-related sections into memory for later processing during symbol resolution and relocation.

Fourth, cross-references are relocated.

Fifth, it sets up the procedure linkage table for lazy binding.

Sixth, it uses `DT_VERNEED`, `DT_VERNEEDNUM`, `DT_VERSYM` to check symbol versions match between binary and shared libraries.

Seventh, constructors are called, `INIT` and `INIT_ARRAY` .

Finally, our source gets the control.

***

This was an high level overview of how the interpreter works. Now, its time to learn relocations. And don't worry. All the things that were left unresolved here will start to get resolved from relocations on wards.

Take rest.