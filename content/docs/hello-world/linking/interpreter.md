---
id: 21938857c7dd43e3becd500a422764a3
title: Interpreter Program
weight: 5
---

***Originally written in early July 2025.***

***Polished on October 04, 2025***

---

This is the `.dynamic` section, located at 0x3de0 in the VAS.
```
Dynamic section at offset 0x2de0 contains 26 entries:
       Tag            Type           Name/Value
0x0000000000000001    NEEDED         Shared library: [libc.so.6]
0x000000000000000c    INIT           0x1000
0x000000000000000d    FINI           0x1154
0x0000000000000019    INIT_ARRAY     0x3dd0
0x000000000000001b    INIT_ARRAYSZ   8 (bytes)
0x000000000000001a    FINI_ARRAY     0x3dd8
0x000000000000001c    FINI_ARRAYSZ   8 (bytes)
0x000000006ffffef5    GNU_HASH       0x3b0
0x0000000000000005    STRTAB         0x480
0x0000000000000006    SYMTAB         0x3d8
0x000000000000000a    STRSZ          141 (bytes)
0x000000000000000b    SYMENT         24 (bytes)
0x0000000000000015    DEBUG          0x0
0x0000000000000003    PLTGOT         0x3fe8
0x0000000000000002    PLTRELSZ       24 (bytes)
0x0000000000000014    PLTREL         RELA
0x0000000000000017    JMPREL         0x610
0x0000000000000007    RELA           0x550
0x0000000000000008    RELASZ         192 (bytes)
0x0000000000000009    RELAENT        24 (bytes)
0x000000006ffffffb    FLAGS_1        Flags: PIE
0x000000006ffffffe    VERNEED        0x520
0x000000006fffffff    VERNEEDNUM     1
0x000000006ffffff0    VERSYM         0x50e
0x000000006ffffff9    RELACOUNT      3
0x0000000000000000    NULL           0x0
```

| Attribute | Description |
| :-------- | :---------- |
| Tag | A numeric identifier telling what an entry means. It is not an address, just the value is represented using hexadecimal values. |
| Type | It is a human interpretation of the value in the Tag field. |
| Name/Value | For a shared library, this attribute has a string name as value. |
| | For size, it stores a size. |
| | For integer/count, a number only |
| | For address, it stores `0x` prefixed addresses. |

## Understanding Each Entry

| Tag    | Purpose |
| :----  | :------ |
| NEEDED | Tells the linker a shared library is needed. |
| | The value is an offset in the .dynstr table pointing to the library's name (e.g."libc.so.6"). | 
| | There can be multiple entries of this type. |
| INIT | Address of the function to run before the main() from the source program runs. |
| INIT_ARRAY   | Address of an array of constructor function pointers to run before the main() runs (more flexible than INIT). |
| INIT_ARRAYSZ | Size of the INIT_ARRAY in bytes. |
| FINI | Address of the function to run after the main() has returned. |
| FINI_ARRAY   | Address of an array of destructor function pointers to run after the main() has returned (more flexible than FINI_ARRAY). |
| FINI_ARRAYSZ | Size of the FINI_ARRAY in bytes. |
| GNU_HASH | Address of the GNU-style hash table used to speed symbol lookup. |
| STRTAB   | Address of string table (used for global symbols). |
| STRSZ    | Size of string table in bytes.   |
| SYMTAB   | Address of dynamic symbol table. |
| SYMENT   | Size of each symbol table entry. |
| DEBUG    | Reserved for debugger use; ignored at runtime. |
| RELA     | Address of relocation entries using eager binding (.rela.dyn). |
| RELASZ   | Size of the .rela.dyn section in bytes. |
| RELAENT  | Size of each entry in .rela.dyn in bytes. |
| JMPREL   | Address of relocation entries using lazy binding via plt (.rela.plt). |
| PLTRELSZ | Size of the .rela.plt section in bytes. |
| PLTREL   | Type of relocation entries the PLT uses (RELA or REL). |
| PLTGOT   | Address of the PLT specific global offset table (GOT) used for dynamic symbol resolution via PLT. |
| FLAGS_1  | Flags for the dynamic linker. |
| VERNEED  | Address of version dependency table (defines symbol versions). |
| VERNEEDNUM | Number of entries in the version dependency table. |
| VERSYM     | Address of the version symbol table — gives the version of each symbol in the symbol table. |
| RELACOUNT  | Number of RELA relocations not part of PLT — for optimization. |
| NULL | Marks the end of the dynamic section. No entries are processed after this. |

All this information is used in relocation. We will explore it in detail.

## How does the interpreter reads them?

When the kernel calls the interpreter program and transfers control to it, it passes some information in the form of arguments, including:
  - `AT_DYNAMIC`: Address of the .dynamic section of the main program.
  - `AT_PHDR`: Pointer to the PHDR segment.
  - `AT_ENTRY`: Original program entry point.

The interpreter uses the AT_DYNAMIC to locate the .dynamic section. It loops over each entry loads the shared libraries marked by the DT_NEEDED types and records pointers and other values relevant for relocation.

Now the interpreter starts relocation.