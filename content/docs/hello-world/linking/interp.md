---
id: 21938857c7dd43e3becd500a422764a3
title: Interpreter
weight: 5
---

***Originally written in early July 2025.***

***Polished on 04, 05 October 2025***

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

This information is used in resolving external symbol references. We will explore them later in detail.

## How they are interpreted?

When the kernel calls the interpreter program and transfers control to it, it passes some information in the form of arguments, including:
  - `AT_DYNAMIC`: Address of the .dynamic section of the main program.
  - `AT_PHDR`: Pointer to the PHDR segment.
  - `AT_ENTRY`: Original program entry point.

The interpreter uses AT_DYNAMIC to locate the .dynamic section.

---

Now we have to understand how external references are resolved.