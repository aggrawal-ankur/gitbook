---
id: a286b3f6fb904fd182774bb9217728b8
title: ELF Headers
weight: 1
---

***Originally written between late june and early july 2025***

***Polished on October 04, 2025***

---

```bash
$ readelf ./linked_elf -h

ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 
  Class:                             ELF64
  Data:                              2`s complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              DYN (Position-Independent Executable file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x1050
  Start of program headers:          64 (bytes into file)
  Start of section headers:          13968 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         14
  Size of section headers:           64 (bytes)
  Number of section headers:         31
  Section header string table index: 30
```

This binary is linked dynamically so the `Type` is `DYN`.

The binary can be loaded in the memory for execution, which is why the `Entry point address` field is populated.
  - It means the binary is loaded at `0x1050` in the virtual address space.
  - This is only useful for non-PIE code. For more information, check out the {{< doclink "98594536dd60406ca3820f14366503ac" "position-independent code" >}} write up.

To be able to load the binary in memory, some metadata is required. That is known as program headers.
  - Since this ELF is linked, the file headers show entries for program headers related fields.
  - They are present just after the file header. 0-63 bytes are reserved for file header and from 64th byte comes program headers.
  - Their size is 56 bytes.
  - Their count is 14.

In object code, the number of section headers was 13. Now it is 31 because extra sections were added in the linking process.

## Where does it fit in the process?

When we run a command, like `ls`, it refers to a binary present somewhere on the computer.

The kernel checks if the file represented by the command can be executed. This is done by inspecting the magic characters of the file. They should be `7F 45 4C 46`.
  - If the file has this magic number, it is an ELF.
  - Otherwise, the kernel drops the request.

After verifying the ELF, it opens the file header and checks the type of the ELF. It has to be `DYN` (for dynamically linked) or `EXEC` (for statically linked).
  - If it is `REL`, the ELF needs to be linked and the kernel drops the request.

The first task is done.

Now the kernel goes to the program headers, so as we.