# Part I

## Premise

Since we have already explored one elf (object code), we have an idea of how things certainly move. We are not going to do something new. We are going to use contrast to differentiate between the two stages.

If you are anxious and you didn't get anything, just sit tight and trust me. Your times is not going to be wasted at all. I hope you are ready.

## ELF Headers

These are the ELF headers from the object code.

```bash
$ readelf ./object_code.o -h

ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              REL (Relocatable file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x0
  Start of program headers:          0 (bytes into file)
  Start of section headers:          536 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           0 (bytes)
  Number of program headers:         0
  Size of section headers:           64 (bytes)
  Number of section headers:         13
  Section header string table index: 12
```

These are the ELF headers from the linked elf.

```bash
$ readelf ./linked_elf -h

ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 
  Class:                             ELF64
  Data:                              2's complement, little endian
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

Lets examine the differences.

The first difference is obviously in `Type`. And we have already spotted this difference in the output of `file` just before.

* It has changed from `REL` to `DYN`.
* This means that this ELF is dynamically linked and is ready to be executed.

We know that object code can't be loaded in memory, which is why it can't be executed.

* Here, the value in the `Entry point address` field has changed from `0x0` to `0x1050`.
* It is because an object code which has undergo linking has everything necessary to be loaded into memory \[, which we will talk about very soon].
* `0x1050` is the starting virtual address at which execution begins when the OS transfers the control to the ELF.

As we have discussed earlier, program headers are used by the `dynamic linker/loader` program at runtime to resolve cross-references. And it is build time linker program that actually creates those headers in the final executable ELF.

* We can notice that `Start of program headers` entry has a value of `64 (bytes into file)`.
* We know that the ELF header is of the size 64-bytes on 64-bit architecture. So, 0-63 bytes in the ELF are occupied by ELF headers.
* At the 64th byte, program headers start.
* `Number of program headers` entry is also populated. There are 14 program headers.
* They are found together in the program headers table, which we are going to refer to as PHT.
* `Size of program headers` entry is also populated. It is 56 bytes.

What's interesting to see here is about **section headers**.

* Earlier section headers started from 536 bytes into the ELF. This time, it is 13968 bytes into the file. Maybe it is a part of restructuring as a lot of things have been added.
* Wait, the number of section headers has moved from 13 to 31. And the size is still the same, 64 bytes. How's that possible?



## Full Disassembly (-D)

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

















