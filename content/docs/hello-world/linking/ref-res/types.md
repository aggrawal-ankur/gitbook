---
id: 68520c11ac874803820d4c64784efd23
title: Types Of Relocations
weight:
---

***October 06, 2025***

*Make sure you are familiar with ABIs. If not, check out the {{< doclink "1943e22373c34e3a9d2ff310e1781982" "application binary interface" >}} write up.*
---

Relocations are carried out differently on 32-bit and 64-bit systems.
  - Both architectures have different gABI and psABI so they support different relocation types as well.

## 32-bit

---

# 64-bit

The generic ELF spec (gABI) defines 10 relocation types.
  - 3 of them are defined for object code.
  - 7 of them are defined for linked code.

| Types | Description |
| :---- | :---------- |
| R_386_NONE  |
| R_386_32    |
| R_386_PC32  |
| R_386_GOT32 |
| R_386_PLT32 |
| R_386_COPY  |
| R_386_GLOB_DAT |
| R_386_JMP_SLOT |
| R_386_RELATIVE |
| R_386_GOTOFF |
| R_386_GOTPC  |

However, the platform-specific ABI (psABI) for x64 architecture defines some extra relocation types.