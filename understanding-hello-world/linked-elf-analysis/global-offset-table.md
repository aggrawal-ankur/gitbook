# Global Offset Table

### What is global offset table?

To understand the idea behind global offset table we have to go back to how a relocation entry is read.

* _At this offset in the loaded segments, replace the placeholder value of the symbol with the actual runtime address._

If you are not feeling insane already, not consumed by complexity and confusion, you understand that we are talking about replacing something, which means, we are talking about writing something. Isn't it?

To write something, we must have the permission to do so?

But how do we find if we have the necessary permissions or not? We have to visit program headers once again!

```
Program Headers:
  Type           Offset              VirtAddr            PhysAddr             FileSiz              MemSiz              Flags  Align
  PHDR           0x0000000000000040  0x0000000000000040  0x0000000000000040   0x0000000000000310   0x0000000000000310  R      0x8
  INTERP         0x0000000000000394  0x0000000000000394  0x0000000000000394   0x000000000000001c   0x000000000000001c  R      0x1
              └─ [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
  LOAD           0x0000000000000000  0x0000000000000000  0x0000000000000000   0x0000000000000628   0x0000000000000628  R      0x1000
  LOAD           0x0000000000001000  0x0000000000001000  0x0000000000001000   0x000000000000015d   0x000000000000015d  R E    0x1000
  LOAD           0x0000000000002000  0x0000000000002000  0x0000000000002000   0x000000000000010c   0x000000000000010c  R      0x1000
  LOAD           0x0000000000002dd0  0x0000000000003dd0  0x0000000000003dd0   0x0000000000000248   0x0000000000000250  RW     0x1000
  DYNAMIC        0x0000000000002de0  0x0000000000003de0  0x0000000000003de0   0x00000000000001e0   0x00000000000001e0  RW     0x8
  NOTE           0x0000000000000350  0x0000000000000350  0x0000000000000350   0x0000000000000020   0x0000000000000020  R      0x8
  NOTE           0x0000000000000370  0x0000000000000370  0x0000000000000370   0x0000000000000024   0x0000000000000024  R      0x4
  NOTE           0x00000000000020ec  0x00000000000020ec  0x00000000000020ec   0x0000000000000020   0x0000000000000020  R      0x4
  GNU_PROPERTY   0x0000000000000350  0x0000000000000350  0x0000000000000350   0x0000000000000020   0x0000000000000020  R      0x8
  GNU_EH_FRAME   0x0000000000002014  0x0000000000002014  0x0000000000002014   0x000000000000002c   0x000000000000002c  R      0x4
  GNU_STACK      0x0000000000000000  0x0000000000000000  0x0000000000000000   0x0000000000000000   0x0000000000000000  RW     0x10
  GNU_RELRO      0x0000000000002dd0  0x0000000000003dd0  0x0000000000003dd0   0x0000000000000230   0x0000000000000230  R      0x1

 Section to Segment mapping:
  Segment Sections...
   00     
   01    .interp 
   02    .note.gnu.property .note.gnu.build-id .interp .gnu.hash .dynsym .dynstr .gnu.version .gnu.version_r .rela.dyn .rela.plt 
   03    .init .plt .plt.got .text .fini 
   04    .rodata .eh_frame_hdr .eh_frame .note.ABI-tag 
   05    .init_array .fini_array .dynamic .got .got.plt .data .bss 
   06    .dynamic 
   07    .note.gnu.property 
   08    .note.gnu.build-id 
   09    .note.ABI-tag 
   10    .note.gnu.property 
   11    .eh_frame_hdr 
   12
   13    .init_array .fini_array .dynamic .got 
```

Lets take this relocation entry as example

```
  Offset          Info            Type            Sym. Value     Sym. Name + Addend
000000003fc0  000100000006  R_X86_64_GLOB_DAT  0000000000000000  __libc_start_main@GLIBC_2.34 + 0
```

The offset `0x3fc0` lies in `.got` section (have a look at the section headers). This section is in the 4th LOAD segment. Have a look at the 4th `LOAD` segment entry in the program headers table. The flags says `RW`.&#x20;





