# Part I

## Premise

Since we have already explored one elf (object code), we have an idea of how things certainly move. We are not going to do something new. We are going to use contrast to differentiate between the two stages.

If you are anxious and you didn't get anything, just sit tight and trust me. Your times is not going to be wasted at all. I hope you are ready.

### Full Disassembly (-D)

```bash
objdump linked_elf -D -M intel
```

Shocked, right! The generated assembly is 800 lines long. The first and the immediate question is **WHERE ALL THIS ASSEMBLY IS COMING FROM?**

This is what linking has done, precisely. It is all compiler (`gcc`) generated.

Before complexity consumes us, lets try to organize the abundance of knowledge available here.

### All the sections in the disassembly

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
```

There are total 26 sections here.

We can also verify this with elf headers

















