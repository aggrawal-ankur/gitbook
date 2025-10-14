---
id: 0760c453ded149aa8a9aaef2bc02ee15
title: File Header
weight:
---

### Magic Number

`Magic` is a stream of characters used to identify a file format or protocol. ([Wikipedia](https://en.wikipedia.org/wiki/Magic_number_\(programming\)))

They are often placed at the beginning of a data stream and serve as a unique signature to indicate the type or origin of a data.
  - For example, a PNG file typically starts with `89 50 4E 47 0D 0A 1A 0A`.
  - For an ELF, it is `7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00`.

These are 16 pairs of hexadecimal digits, each representing 1-byte. Therefore, it is 16-bytes long.

| Magic Number Portion | Description |
| :--- | :--- |
| `7f 45 4c 46` | This is an ELF file.                      |
| `02`          | Architecture is 64-bit (`01` for 32-bit). |
| `01`          | Bits are stored in little-endian notation (`02` for big-endian). |
| `01`          | Version, nothing interesting about it.    |
| `00`          | OS/ABI is System V                        |

- Each binary file format (like PNG, JPEG etc) uses a non-printable ASCII character so the system can distinguish the file from a random text file as a random text file can't start with `DEL` unless manipulated.
- `7f` which is a non-printable ASCII character `DEL`, is reserved for ELF format. And `45 4c 46` translates to `E L F`.

### ELF Type

`Type` field specifies the purpose of the ELF file.

| Value  | Integer Value (used internally) | Description |
| :----- | :---- | :---- |
| `REL`  | 1 | Relocatable file, object code ready to be linked. |
| `EXEC` | 2 | Executable file, represents linked binaries. |
| `DYN`  | 3 | Shared object file, represents libraries. |
| `CORE` | 4 | Core dump, used in memory-analysis. |

### Entry Point, Program Headers and Flags

Entry point address is `0x0` because this is a relocatable file, i.e it can't be loaded in memory for execution.

Programs headers are created during linking, that's why there is `0` for the start, number and size of program headers.

No flags were provided so `0x0` in that.

### Section Headers

Assembling lays down a basic section layout. That's why section headers are present in the object file.
  - They start after 536 bytes in the binary.
  - Total 13 section headers.
  - Their size is 64-bytes.

### File Header Size

On 64-bit architecture, it is 64-bytes.

On 32-bit architecture, it is 32-bytes.

### Section Header String Table Index

Discussed in the section headers section below.

## Section Headers

Section are used to organize the ELF file. Section headers table contains metadata about these sections.

---

If you notice, the `Name` field has entries of varied length. The `Name` field has to be long enough but the longest range is never utilized always. This leads to increase in size, which leads to wastage.
  - For example, the longest entry in the in the above output is 15 characters. We have 12 sections in total, so `12*15 = 180 bytes`.
  - `Name` has to be 15 characters long for each entry. But how many bytes we are actually using? 87 bytes only. 93 bytes are wasted space.

This was just one table. There are other tables which have similar varied length fields. This would waste a lot of memory.

The solution is to **minimize the maximum wastage.**
  - We create a **flat central string registry** and anyone can refer to it.
  - Keeping the central registry flat removes the space problem as strings would be null-terminated and the the null character would create the distinction.
  - Changing strings would also be easier as only one place would it require it.
  - We can remove these **central tables** when not required. This happens when you strip the binary to reduce its size for production use. Remember the `not stripped` part in the output of `file`? It is about such things only.

Therefore, the `Section header string table index: 12` entry in the ELF header specifies the index of the "section header string table" entry in the section headers table.