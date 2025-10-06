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

---

## R_X86_64_RELATIVE

```
  Offset          Info            Type            Sym. Value     Sym. Name + Addend
000000003dd0  000000000008  R_X86_64_RELATIVE                      1130
000000003dd8  000000000008  R_X86_64_RELATIVE                      10f0
000000004010  000000000008  R_X86_64_RELATIVE                      4010
```
  - Let's understand the first one.

Since readelf uses hex format to display the `Info` field, we can simply make pairs of 8 digits to obtain and the high and low bits.
  - Since it only displays 12 digits, we will append 4 in the left side to make it a 8-byte value: 0000000000000008
  - Now, high bits: 0x00000000 && low bits: 0x00000008

So the symbol index is 0 and relocation type is 8, which is `R_X86_64_RELATIVE`.

Entries of type 8 doesn't require any symbol lookup.

The symbol's runtime address can be calculated as:
```
Base Address of the binary + Addend
```
  - This value needs to be patched at `0x3dd0` offset.

---

The remaining two entries are relocated in the same manner.

## R_X86_64_GLOB_DAT

```
  Offset          Info            Type            Sym. Value     Sym. Name + Addend
000000003fc0  000100000006  R_X86_64_GLOB_DAT  0000000000000000  __libc_start_main@GLIBC_2.34 + 0
000000003fc8  000200000006  R_X86_64_GLOB_DAT  0000000000000000  _ITM_deregisterTM[...] + 0
000000003fd0  000400000006  R_X86_64_GLOB_DAT  0000000000000000  __gmon_start__ + 0
000000003fd8  000500000006  R_X86_64_GLOB_DAT  0000000000000000  _ITM_registerTMCl[...] + 0
000000003fe0  000600000006  R_X86_64_GLOB_DAT  0000000000000000  __cxa_finalize@GLIBC_2.2.5 + 0
```
  - Lets take the first entry.

The symbol index is 1 and relocation type is 6, which is for R_X86_64_GLOB_DAT.

It is a global data relocation, commonly used for symbol pointers in the GOT (Global Offset Table). This does require relocation.

The symbol is `__libc_start_main`, which belongs to libc.so.6 shared library.

The relocation logic is simple.
```
*(base_addr + 0x3fc0) = address_of(__libc_start_main)
```
  - At the offset, write the final runtime address of __libc_start_main.

The symbol is looked up in all the loaded shared libraries using the dynamic symbol table and the hash tables. Once the runtime address is found in memory, the address is written in place of `0x3fc0` in the global offset table. And the relocation is done.

We are done with `.rela.dyn` relocations.

The term **global offset table** is new here.

Now the interpreter jumps to the `JUMPREL` entry in the dynamic section and finds `.rela.plt`. The real chaos starts here.
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