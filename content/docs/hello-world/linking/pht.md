---
id: 03ae9097699f47bcac2df5d89343591e
title: Program Headers
weight: 4
---

***Originally written in early july 2025.***

***Polished on October 04, 2025***

---

Program headers describes how to map a binary in virtual memory.

These are the program headers in our binary.
```bash
$ readelf hello -l

Program Headers:
  Type           Offset              VirtAddr            PhysAddr            FileSiz             MemSiz              Flags   Align
  PHDR           0x0000000000000040  0x0000000000000040  0x0000000000000040  0x0000000000000310  0x0000000000000310    R      0x8
  INTERP         0x0000000000000394  0x0000000000000394  0x0000000000000394  0x000000000000001c  0x000000000000001c    R      0x1
              └─ [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
  LOAD           0x0000000000000000  0x0000000000000000  0x0000000000000000  0x0000000000000628  0x0000000000000628    R      0x1000
  LOAD           0x0000000000001000  0x0000000000001000  0x0000000000001000  0x000000000000015d  0x000000000000015d    R E    0x1000
  LOAD           0x0000000000002000  0x0000000000002000  0x0000000000002000  0x000000000000010c  0x000000000000010c    R      0x1000
  LOAD           0x0000000000002dd0  0x0000000000003dd0  0x0000000000003dd0  0x0000000000000248  0x0000000000000250    RW     0x1000
  DYNAMIC        0x0000000000002de0  0x0000000000003de0  0x0000000000003de0  0x00000000000001e0  0x00000000000001e0    RW     0x8
  NOTE           0x0000000000000350  0x0000000000000350  0x0000000000000350  0x0000000000000020  0x0000000000000020    R      0x8
  NOTE           0x0000000000000370  0x0000000000000370  0x0000000000000370  0x0000000000000024  0x0000000000000024    R      0x4
  NOTE           0x00000000000020ec  0x00000000000020ec  0x00000000000020ec  0x0000000000000020  0x0000000000000020    R      0x4
  GNU_PROPERTY   0x0000000000000350  0x0000000000000350  0x0000000000000350  0x0000000000000020  0x0000000000000020    R      0x8
  GNU_EH_FRAME   0x0000000000002014  0x0000000000002014  0x0000000000002014  0x000000000000002c  0x000000000000002c    R      0x4
  GNU_STACK      0x0000000000000000  0x0000000000000000  0x0000000000000000  0x0000000000000000  0x0000000000000000    RW     0x10
  GNU_RELRO      0x0000000000002dd0  0x0000000000003dd0  0x0000000000003dd0  0x0000000000000230  0x0000000000000230    R      0x1

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

Every entry in this table is a program header. These program headers are what segments.
  - A segment groups multiple sections based on usability.

## Segments

| Segment      | Description |
| :------      | :---------- |
| PHDR         | Specifies where the program headers themselves are located.  |
| LOAD         | Loadable segment. Only segments can be loaded in the memory. |
| DYNAMIC      | The address of the dynamic section.   |
| INTERP       | Path to dynamic linker (ld-linux.so). |
| NOTE         | Auxiliary information (e.g., build ID, security notes). |
| GNU_STACK    | Stack permissions. |
| GNU_RELRO    | Read-only after relocation. |
| GNU_EH_FRAME | Exception handling info.    |

## Attributes

| Attribute   | Description |
| :--------   | :---------- |
| Offset      | The location of this segment relative to where the binary is loaded in the memory. |
| VirtualAddr | The virtual memory address where the segment should be mapped in memory during execution. |
| PhysAddr    | Usually ignored by modern OS. Same as `VirtAddr` or meaningless. |
| FileSize    | The size of the segment in the binary. |
| MemSize     | The size of the segment in memory after loading. |
| Flags       | Memory access permissions. `R`: Readable, `W`: Writable, `E`: Executable |
| Align       | Required alignment for the segment. |

## Logic Behing This Segmentation

The **section to segment mapping** part defines the sections grouped under each each segment.

The `LOAD` segments are at indices 2, 3, 4 and 5.
```
02  .note.gnu.property .note.gnu.build-id .interp .gnu.hash .dynsym .dynstr .gnu.version .gnu.version_r .rela.dyn .rela.plt 
03  .init .plt .plt.got .text .fini 
04  .rodata .eh_frame_hdr .eh_frame .note.ABI-tag 
05  .init_array .fini_array .dynamic .got .got.plt .data .bss 
```

These LOAD segments have different memory protection flags.
  - The 1st LOAD segment groups all the **read-only** sections. If we open the section header table, these sections have `A` flag, means allocate these sections in the memory.
  - The 2nd LOAD segment has program bits which must be readable and executable.
  - The 3rd LOAD segment has read-only data again.
  - The 4th LOAD segment has read and writable sections.

## Where does it fit in the process?

After verifying that the binary can be loaded in memory for execution, the kernel searches for program headers. They tell the kernel how to load the binary in virtual memory.

The kernel runs a loop on the program headers and starts processing them on-by-one.
  - It maps all the segments of type `LOAD` in the virtual address space.
  - It notes if there was an `INTERP` segment. It doesn't act on it right now.
  - If there was a `DYNAMIC` segment, it notes its virtual address and pass it to the interpreter later.
  - Rest of the segments aren't that important right now.

After the loop ends, the kernel checks if there was an `INTERP` segment. 
  - If there was an INTERP segment (`DYN`), it locates it and loads the interpreter program as a separate ELF in the same VAS. Then it sets the program entry point to the interpreter's entry point.
  - If no INTERP segment was found (`EXEC`), the kernel defaults to the main binary's entry point.

**Interpreter program** and **dynamic linker/loader** refer to the same thing, i.e ld-linux.so. We use them interchangeably.

Once the interpreter is mapped in VAS, the kernel
  - Sets up the new process’s stack and aux vector.
  - Overwrites the process’s entry point with the interpreter’s entry point (from its ELF header).
  - Transfers control to it. Therefore, the first code that executes belongs to the interpreter, not the main.

---

This sums up the program headers. Next is the interpreter.