# Step 1: Analyzing ELF Headers

## Understanding ELF Headers

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

We know that object code can't be loaded in memory, which is why it is not an executable.

* Here, the value in the `Entry point address` field has changed from `0x0` to `0x1050`.
* It is because an object code which has undergo linking has everything necessary to be loaded into memory, which we will talk about very soon.
* `0x1050` is the starting virtual address at which execution begins when the OS transfers the control to the ELF.

As we have discussed earlier, program headers are used by the `dynamic linker/loader` program at runtime to resolve cross-references. And it is build time linker program that actually creates those headers in the final executable ELF.

* We can notice that `Start of program headers` entry has a value of `64 (bytes into file)`.
* We know that the ELF header is of the size 64-bytes on 64-bit architecture. So, 0-63 bytes in the ELF are occupied by ELF headers.
* At the 64th byte, program headers start.
* `Number of program headers` entry is also populated. There are 14 program headers.
* They are found together in the program headers table, which we are going to refer to as PHT.
* `Size of program headers` entry is also populated. It is 56 bytes.

What's interesting to see here is **section headers**.

* Earlier section headers started from 536 bytes into the ELF. This time, it is 13968 bytes into the file. Maybe it is a part of restructuring as a lot of things have been added.
* Wait, the number of section headers has moved from 13 to 31. And the size is still the same, 64 bytes. How's that possible?
* The answer is, compilation (.asm to .o) lay downs only a partial structure. Linking completes the object code. These extra section headers are about the things which were absent earlier.
* If you notice, `.note.GNU-stack` is not present in the linked ELF. This is because it is empty in size and that means "non-executable stack". It is not needed in the final binary so it got stripped.

`Section header string table index: 30` we need not to talk about. We have invested great amount of time understanding this.

* The entry at index 30 in the section headers table is where the string table for section headers is located.

***

## What to do about this?

When this linked elf (or binary) is executed in the terminal, the first thing that happens is the kernel checks if the binary can be loaded into the memory.

If the binary can't be loaded into memory, it doesn't poses relevant information required to setup the environment in which it can be executed.

To find this, the kernel checks up the ELF headers. The `Type` header we have talked about recently is the one that is checked. If the value is `REL`, it can't be loaded.

Since our elf is linked now, it has the value of `DYN` in the `Type` field, which means that it has necessary information required to setup the environment for execution.

Therefore, the first task is done.

## What is the next step?

Now the kernel goes to the program headers, which are present just after the ELF headers at offset 0x64 in the binary.

What are we waiting for? Lets go there. But before that, we need to clear our mind about something.
