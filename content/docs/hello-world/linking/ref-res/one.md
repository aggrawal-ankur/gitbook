---
id: 8bf1c94a19df485485fe7e3861821065
title: Performing Relocations
weight: 1
---

***Originally written in early July 2025.***

***Polished on 05 October 2025***

---

The interpreter is at the .dynamic section now.
  - It has loaded `libc.so.6`, whcih is the only shared library dependency in our program.

It's time for relocations. The interpreter uses:
  - `RELA` to find `.rela.dyn` section. It is at 0x550.
  - `RELASZ` to find the size of .rela.dyn section.
  - `RELACOUNT` to find the number of entries in .rela.dyn section. It is 8.
  - `RELAENT` to find the size of each entry in .rela.dyn table.

These are the relocation entries in the `.rela.dyn` table.

```bash
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

| Attribute |	Description |
| :-------- | :---------- |
| Offset | Offset in a section where relocation is required. |
| Info   | Encodes relocation type and symbol index. |
| Type   | Relocation type. |

There are no "Sym. Value" and "Sym. Name + Addend" fields in the raw ELF. They are just readelf's creation.

A relocation entry can be read as: _at offset in the section, replace the placeholder value with the runtime address._

The `Info` field is 4/8 bytes in size on 32-bit/64-bit architecture. It is present in hex form and readelf missed the upper 4 bits which is why it is 6 bytes long here.
  - The upper-half is for symbol index and the lower-half is for relocation type.

Let's understand R_X86_64_RELATIVE and R_X86_64_GLOB_DAT.

CONTINUE FROM HERE

### R_X86_64_RELATIVE Relocation

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

### R_X86_64_GLOB_DAT Relocation

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

---

Before we end this, let's explore one thing we have deferred so far.

## Relocation At Object Level vs Link Level

The object code also had relocations.

```bash
$ readelf hello.o -r

Relocation section '.rela.text' at offset 0x168 contains 2 entries:
  Offset          Info           Type           Sym. Value    Sym. Name + Addend
000000000007  000300000002 R_X86_64_PC32     0000000000000000 .rodata - 4
00000000000f  000500000004 R_X86_64_PLT32    0000000000000000 puts - 4

Relocation section '.rela.eh_frame' at offset 0x198 contains 1 entry:
  Offset          Info           Type           Sym. Value    Sym. Name + Addend
000000000020  000200000002 R_X86_64_PC32     0000000000000000 .text + 0
```

You may ask, *what's the point of having relocations when the code can't be loaded into memory?*
  - That's because, these relocations lay down the foundation for what we see at link-time.
  - In huge projects, the code exists in multiple source files. Each file is compiled and assembled separately.
  - When we link them, all of them tell the linker that we have these external references. If there were no relocations at object level, that would be a nightmare for the linker.