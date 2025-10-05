---
id: 8bf1c94a19df485485fe7e3861821065
title: Performing Relocations
weight: 1
---

***Originally written in early July 2025.***

***Polished on 05 October 2025***

---

The dynamic linker needs to know where the relocation entries are to resolve the external symbol references.

```bash
Dynamic section at offset 0x2de0 contains 26 entries:
        Tag            Type              Name/Value
 0x0000000000000001    (NEEDED)          Shared library: [libc.so.6]
 0x000000000000000c    (INIT)            0x1000
 0x000000000000000d    (FINI)            0x1154
 0x0000000000000019    (INIT_ARRAY)      0x3dd0
 0x000000000000001b    (INIT_ARRAYSZ)    8 (bytes)
 0x000000000000001a    (FINI_ARRAY)      0x3dd8
 0x000000000000001c    (FINI_ARRAYSZ)    8 (bytes)
 0x000000006ffffef5    (GNU_HASH)        0x3b0
 0x0000000000000005    (STRTAB)          0x480
 0x0000000000000006    (SYMTAB)          0x3d8
 0x000000000000000a    (STRSZ)           141 (bytes)
 0x000000000000000b    (SYMENT)          24 (bytes)
 0x0000000000000015    (DEBUG)           0x0
 0x0000000000000003    (PLTGOT)          0x3fe8
 0x0000000000000002    (PLTRELSZ)        24 (bytes)
 0x0000000000000014    (PLTREL)          RELA
 0x0000000000000017    (JMPREL)          0x610
 0x0000000000000007    (RELA)            0x550
 0x0000000000000008    (RELASZ)          192 (bytes)
 0x0000000000000009    (RELAENT)         24 (bytes)
 0x000000006ffffffb    (FLAGS_1)         Flags: PIE
 0x000000006ffffffe    (VERNEED)         0x520
 0x000000006fffffff    (VERNEEDNUM)      1
 0x000000006ffffff0    (VERSYM)          0x50e
 0x000000006ffffff9    (RELACOUNT)       3
 0x0000000000000000    (NULL)            0x0
```

So far, we know that the first thing that the interpreter does is to load the shared libraries.

* In our case, it is `libc.so.6`.

After all the shared libraries are loaded, the interpreter goes about relocation.

CONTINUE FROM HERE

## Introducing Relocations

The interpreter uses the `RELA` entry to jump to the `.rela.dyn` relocation table. `RELA` entry in the dynamic section has a value of `0x550` and we can verify that the `.rela.dyn` table is also located at the same offset by this line `Relocation section '.rela.dyn' at offset 0x550 contains 8 entries:` .

To revise, a relocation entry can be read as: _at offset in the section, replace the placeholder address of the symbol with its actual address._

These are the relocation entries in the `.rela.dyn` table.

```
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
```

The `Info` field is 8 bytes long, although here it is 6 bytes, which is I am also wondering why readelf is not showing the remaining 2 bytes, but leave it.

* The upper 8-bytes refers to the symbol index value and the lower 8-bytes refers to the relocation type.

### \`R\_X86\_64\_RELATIVE\` Relocation

```
  Offset          Info            Type            Sym. Value     Sym. Name + Addend
000000003dd0  000000000008  R_X86_64_RELATIVE                      1130
```

Its symbol index is 0 and the relocation type is 8, which resolves to `R_X86_64_RELATIVE`.

* Entries of type 8 doesn't require any symbol lookup.
*   `Offset` is where we have to write the result. And the result is calculated as follows:
    ```
    *(Offset) = Base Address of the binary + Addend
    ```
* In simple words, take the base address of the binary and add the value in the `Sym. Name + Addend` field to it. Now write the obtained value at the mentioned offset. Relocation is done.
* ```
  relocation_address = base_addr + 0x3dd0;
  value_to_write = base_addr + 1130;

  *(relocation_address) = value_to_write
  ```

The remaining two entries are relocated in the same manner.

```
000000003dd8  000000000008  R_X86_64_RELATIVE                      10f0
000000004010  000000000008  R_X86_64_RELATIVE                      4010
```

### \`R\_X86\_64\_GLOB\_DAT\` Relocation

```
  Offset          Info            Type            Sym. Value     Sym. Name + Addend
000000003fc0  000100000006  R_X86_64_GLOB_DAT  0000000000000000  __libc_start_main@GLIBC_2.34 + 0
000000003fc8  000200000006  R_X86_64_GLOB_DAT  0000000000000000  _ITM_deregisterTM[...] + 0
000000003fd0  000400000006  R_X86_64_GLOB_DAT  0000000000000000  __gmon_start__ + 0
000000003fd8  000500000006  R_X86_64_GLOB_DAT  0000000000000000  _ITM_registerTMCl[...] + 0
000000003fe0  000600000006  R_X86_64_GLOB_DAT  0000000000000000  __cxa_finalize@GLIBC_2.2.5 + 0
```

Lets take the first entry here.

The symbol index is 1 and relocation type is 6.

* `R_X86_64_GLOB_DAT` does require symbol lookup.
* This is a global data relocation, commonly used for symbol pointers in the GOT (Global Offset Table).\
  Its purpose is to fill a pointer with the runtime address of a symbol — typically function pointers or global variables imported from shared libraries.

The symbol is `__libc_start_main.`

The relocation logic is

```
*(base_addr + 0x3fc0) = address_of(__libc_start_main)
```

The symbol is looked up in all the loaded shared libraries using the dynamic symbol table and the symbol hash tables. Once the runtime address is found in memory, the address is written in place of `0x3fc0` in the global offset table. And the relocation is done.

The term **global offset table** is new here.

We are done with `.rela.dyn` relocations.

Now the interpreter jumps to the `JUMPREL` entry in the dynamic section and finds `.rela.plt`. The real chaos starts here.

* PLT entries are about lazy binding, by default.
* For lazy binding, we need to understand global offset table (GOT) and procedure linkage table (PLT). Both of which are really complex and confusing.
* Since it is fairly long, it deserves its own separate place. Therefore, we are dividing this article into two parts.
* Here ends the first part.