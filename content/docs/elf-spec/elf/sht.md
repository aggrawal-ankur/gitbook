---
id: 5df3decc9bc24cbd92f4c1fc43d349e8
title: Sections
weight:
---

| Attributes | Description |
| :-------- | :---------- |
| [Nr] | Index value. |
| Name | An offset into the `.shstrtab` (section header string table), which stores the actual section names as strings. readelf uses this offset to locate and display the human-readable name of these sections.
| Type | The type of the section. |
| | `PROGBITS`: contains code/data from the source. |
| | `RELA`: relocation entries with addends. |
| | `BSS`: uninitialized data. |
| | `SYMTAB`: symbol table. |
| | `STRTAB`: string table. |
| | `NULL`: for alignment purposes as computers index from 0 and ELF has preserved that. This way, the actual sections start from 1. |
| Offset  | The position of a section inside the ELF. |
| Address | The virtual address at which the section is loaded inside the virtual address space. 00..00 denotes a placeholder value which needs to be relocated. |
| Size    | Size of the section in hexadecimal bytes. |
| EntSize | The size of each individual entry within a section, if the section stores uniform entries. Otherwise, it is 0. |
| Flags   | How the section should be treated in the memory. |
| Link    | Index of a related section. |
| Info    | Extra information. |
| Align   | Required alignment in the memory and/or file. We can gloss over it for now. |

---

| Name | Type | Explanation | How To Inspect |
| :--- | :--- | :--- | :--- |
| Section 0 | NULL   | An empty to align the rest of the section from 1. | NA |
| .note.gnu.property | NOTE | Metadata for hardware/ABI features. | readelf -n |
| .note.gnu.build-id | NOTE | Unique hash/fingerprint of the binary. | readelf -n |
| .interp | PROGBITS | Path of the dynamic interpreter program. | readelf -p .interp |
| .gnu.hash | GNU_HASH | Hash table used by the dynamic linker to speed up symbol lookup. | More on this later. |
| .dynsym | DYNSYM | Dynamic symbol table used by the interpreter program (ld-linux). | NA |
| .dynstr | STRTAB | String table for names in .dynsym. | readelf -p .dynstr |
| .gnu.version   | VERSYM | Version info for each dynamic symbol. | NA |
| .gnu.version_r | VERNEED | Declares required versions of shared libraries. | NA |
| .rela.dyn | RELA | Relocation entries for global data and non-PLT addresses. | readelf -r |
| .rela.plt | RELA | Relocation entries via PLT. | readelf -r |
| .init     | PROGBITS | Code that runs before main() to initialize stuff. | NA |
| .plt      | PROGBITS | Procedure Linkage Table — stubs for external function calls. | NA |
| .plt.got  | PROGBITS | Used in lazy binding (jump to GOT entries). | NA |
| .text     | PROGBITS | Our source code. | NA |
| .fini     | PROGBITS | Code that runs after main() returns. | NA |
| .rodata   | PROGBITS | Read-only static data (e.g., strings, constants). | readelf -p .rodata |
| .eh_frame_hdr | PROGBITS | Header for exception handling frames. | NA |
| .eh_frame | PROGBITS | Stack unwinding info for exceptions/debugging. | NA |
| .note.ABI-tag | NOTE | Identifies the target OS/ABI version. | readelf -n |
| .init_array | INIT_ARRAY | List of constructor function pointers to run before main(). | NA |
| .fini_array | FINI_ARRAY | List of destructor function pointers to run after main(). | NA |
| .dynamic | DYNAMIC  | Used by the dynamic linker to. | NA |
| .got     | PROGBITS | Global Offset Table to store resolved addresses. | NA |
| .got.plt | PROGBITS | GOT entries for lazy binding through PLT. | NA |
| .data | PROGBITS | Initialized global/static data.   | NA |
| .bss  | NOBITS   | Uninitialized global/static data. | NA |
| .comment  | PROGBITS | Compiler version or build metadata (ignored at runtime). | readelf -p .comment |
| .symtab   | SYMTAB   | Symbol table for static linking/debugging. | NA |
| .strtab   | STRTAB   | String table for names in .symtab. | readelf -p .strtab |
| .shstrtab | STRTAB   | String table for section names. | readelf -p .shstrtab  |

## Importance of sections

Sections are used by the linker to organize our code/data/symbols etc. Let's take an example.

Consider an ELF as a room, containing different kinds of things. There are clothes, pens and paper, bottle, bag, notebooks etc. And everything is scattered.

To make sense of them, you decided to clear the floor and put everything categorized on the floor.

* You put papers together.
* You put notebooks together.
* You put pens together.
* You put jeans together.
* You put shirts together.
* You put books together.

**This is what sections does. They organize the source code into relevant groups.**

Now we have some organized. But we can do better.

* Books, papers and pens identifies as stationary. They go in the bookshelf.
* Jeans, shirts, t-shirts, lower, jacket etc. are clothes. They go in the wardrobe.
* And so on....

**This further categorization is what segments are. These segments exist as a roadmap for you to traverse your room.**

* To find books and stationary, check the bookshelf.
* To find clothes, check the wardrobe.

## Conclusion

At the end of the day, sections is what that gets mapped into the virtual memory and segments guide this mapping.