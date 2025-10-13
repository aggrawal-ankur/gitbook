---
id: 43bddcfbd0e34201afa4a3b2fe6c3b1e
title: Program Headers
weight:
---

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