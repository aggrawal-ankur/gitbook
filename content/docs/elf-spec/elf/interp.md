---
id: 9f422213e0194d0e8a06b2bb5deaf0d6
title: Dynamic linker/loader (Interpreter)
weight:
---

| Attribute | Description |
| :-------- | :---------- |
| Tag | A numeric identifier for an entry represented using hexadecimal values. |
| Type | A human interpretation of the numeric Tag. |
| Name/Value | For a shared library, it is a string. |
| | For size/count, an integer |
| | For address, a `0x` prefixed addresses. |

## Types

| Tag    | Purpose |
| :----  | :------ |
| NEEDED | Tells the linker a shared library is needed. |
| | The value is an offset in the .dynstr table pointing to the library's name (e.g. libc.so.6). | 
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

We can classify the entries in .dynamic section based on **when and how** the interpreter processes them.

| Phase (When) | Task (How) | Entries |
| :----------- | :--------- | :------ |
| 0  | Control linker behavior; Affects later phases | FLAGS_1 |
| 0  | Let debuggers (e.g. gdb) hook into the internal state of dynamic linker. | DEBUG |
| 1  | Load shared libraries | NEEDED |
| 2  | Perform immediate relocation | RELA, RELAENT, RELASZ, RELACOUNT |
| 3  | Setup for delayed relocation | JMPREL, PLTREL, PLTRELSZ, PLTGOT |
| 4  | Setup before main  | INIT, INIT_ARRAY, INIT_ARRAYSZ |
| 5  | Cleanup after main | FINI, FINI_ARRAY, FINI_ARRAYSZ |
| NA | Section terminator | NULL |

  - GNU_HASH, STRTAB, SYMTAB, STRSZ, SYMENT, VERNEED, VERNEEDNUM, VERSYM are used in resolving external references (symbol resolution + relocation).

Based on the classification above, we can map the purpose of the interpreter as:
  - Load shared libraries.
  - Perform immediate relocations.
  - Set up environment for delayed relocations.
  - Initialize the environment and transfer control to our C program.
  - Do cleanup after main has returned.
  - Initiate exit.