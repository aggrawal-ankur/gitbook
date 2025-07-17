---
hidden: true
---

# Full Disassembly

### All the sections in the disassembly

These are all the sections in the disassembly.

```
.note.gnu.property
.note.gnu.build-id
.interp
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.plt
.plt.got
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.note.ABI-tag
.init_array
.fini_array
.dynamic
.got
.got.plt
.data
.comment

= 26 sections
```

The ELF headers said there are 31 section headers. The disassembly shows 26. Where are the remaining 5 headers?

* First of all, index 0 is NULL. So 4, not 5.
* What are these 4 sections even? `.bss .symtab .strtab .shstrtab`
* From assembly, we know that `.bss` is for uninitialized global/static variables.
* `.symtab .strtab .shstrtab` are compiler generated internal bookkeeping material. They are used in linking and debugging only. And we know that it can be stripped. When something is neither a part of the executable code nor really required at runtime, these form enough reasons for `objdump` not include them in full disassembly.

