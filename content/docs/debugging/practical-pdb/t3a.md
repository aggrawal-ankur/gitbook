---
id: a91507ff9bbf4fbe82ffe1633e869b6b
title: Hello World (Part 1)
weight: 3
---

***1 October 2025***

***Note: This write up seems very long but it is filled with snippets of command output so that the reader doesn't have to do a lot of work to verify everything.***

---

We have already explored `Hello World!` statically using tools like objdump and readelf for 35 days. Honestly, it was an eye-opening and a rewarding exploration. It set the foundation for future low level exploration as those concepts are used extensively.

Now its time to explore `Hello, World!` dynamically.

From static exploration, we didn't just gain knowledge, we also got to know about a few gotchas. One of them was "the problem of scale".
  - During the exploration, we have felt clueless almost all the time because we didn't have any idea about the terrain.
  - But now we know the terrain, to some extent.
  - But we also know that the runtime mapping of a binary is a little different than the binary itself.

Therefore, the first thing we will do is to map the terrain. This will save our time, energy and some headaches.
  - But before that, let's do the setup for this exploration.

You can visit the old hello world write ups {{< doclink "243880d83f464517a201007716ffc581" "here" >}}

## Setup

Source program:
```c {filename=hello.c}
#include <stdio.h>

int main(void){
  printf("Hello, World!\n");
}
```

Source binary:
```bash
gcc -g hello.c -o hello
```

Start a gdb session:
```bash
$ gdb ./hello
(gdb)
```

Clear the window with `CTRL+L`.

## Mapping The Terrain

Virtual address space layout is the "terrain" we are talking about because that's where the binary gets mapped. Right now, we can be sure that there is nothing beyond text/data/heap/mmap/stack.

### File Information

To know how the binary is mapped in VAS, we can use the `info files` command. It gives information about all the files (binaries, core dumps and running processes) loaded in the current gdb session.
  - At basic, this includes the source binary and the shared libraries.
  - For every file, it lists all the regions which are mapped into the VAS and their address range.

Let's invoke this command. Remember, no breakpoint and no run.
```bash
(gdb) info files

Symbols from "/home/username/Desktop/RE/out/hello".
Local exec file:
        `/home/username/Desktop/RE/out/hello`, file type elf64-x86-64.
        Entry point: 0x1050
        0x0000000000000350 - 0x0000000000000370 is .note.gnu.property
        0x0000000000000370 - 0x0000000000000394 is .note.gnu.build-id
        0x0000000000000394 - 0x00000000000003b0 is .interp
        0x00000000000003b0 - 0x00000000000003d4 is .gnu.hash
        0x00000000000003d8 - 0x0000000000000480 is .dynsym
        0x0000000000000480 - 0x000000000000050d is .dynstr
        0x000000000000050e - 0x000000000000051c is .gnu.version
        0x0000000000000520 - 0x0000000000000550 is .gnu.version_r
        0x0000000000000550 - 0x0000000000000610 is .rela.dyn
        0x0000000000000610 - 0x0000000000000628 is .rela.plt
        0x0000000000001000 - 0x0000000000001017 is .init
        0x0000000000001020 - 0x0000000000001040 is .plt
        0x0000000000001040 - 0x0000000000001048 is .plt.got
        0x0000000000001050 - 0x0000000000001153 is .text
        0x0000000000001154 - 0x000000000000115d is .fini
        0x0000000000002000 - 0x0000000000002012 is .rodata
        0x0000000000002014 - 0x0000000000002040 is .eh_frame_hdr
        0x0000000000002040 - 0x00000000000020ec is .eh_frame
        0x00000000000020ec - 0x000000000000210c is .note.ABI-tag
        0x0000000000003dd0 - 0x0000000000003dd8 is .init_array
        0x0000000000003dd8 - 0x0000000000003de0 is .fini_array
        0x0000000000003de0 - 0x0000000000003fc0 is .dynamic
        0x0000000000003fc0 - 0x0000000000003fe8 is .got
        0x0000000000003fe8 - 0x0000000000004008 is .got.plt
        0x0000000000004008 - 0x0000000000004018 is .data
        0x0000000000004018 - 0x0000000000004020 is .bss
```

As we have invested so much time and energy in static analysis, the addresses look familiar.
  - Yes they are and we can verify that with readelf as well.

You may ask why fixed addresses are used at runtime. Where is ASLR?
  - As mentioned earlier, GDB disables ASLR to make the process easier, by default.
  - As decided we are not going to enable it as we are still learning. Once we are done with the basics, we'll explore programs with ASLR enabled.

Now, lets run the debugee.
```bash
(gdb) run
```

Let's isnpect again.
```bash
(gdb) info files

Symbols from "/home/username/Desktop/RE/hello".
Local exec file:
        `/home/username/Desktop/RE/hello`, file type elf64-x86-64.
        Entry point: 0x555555555050
        0x0000555555554350 - 0x0000555555554370 is .note.gnu.property
        0x0000555555554370 - 0x0000555555554394 is .note.gnu.build-id
        0x0000555555554394 - 0x00005555555543b0 is .interp
        0x00005555555543b0 - 0x00005555555543d4 is .gnu.hash
        0x00005555555543d8 - 0x0000555555554480 is .dynsym
        0x0000555555554480 - 0x000055555555450d is .dynstr
        0x000055555555450e - 0x000055555555451c is .gnu.version
        0x0000555555554520 - 0x0000555555554550 is .gnu.version_r
        0x0000555555554550 - 0x0000555555554610 is .rela.dyn
        0x0000555555554610 - 0x0000555555554628 is .rela.plt
        0x0000555555555000 - 0x0000555555555017 is .init
        0x0000555555555020 - 0x0000555555555040 is .plt
        0x0000555555555040 - 0x0000555555555048 is .plt.got
        0x0000555555555050 - 0x0000555555555153 is .text
        0x0000555555555154 - 0x000055555555515d is .fini
        0x0000555555556000 - 0x0000555555556012 is .rodata
        0x0000555555556014 - 0x0000555555556040 is .eh_frame_hdr
        0x0000555555556040 - 0x00005555555560ec is .eh_frame
        0x00005555555560ec - 0x000055555555610c is .note.ABI-tag
        0x0000555555557dd0 - 0x0000555555557dd8 is .init_array
        0x0000555555557dd8 - 0x0000555555557de0 is .fini_array
        0x0000555555557de0 - 0x0000555555557fc0 is .dynamic
        0x0000555555557fc0 - 0x0000555555557fe8 is .got
        0x0000555555557fe8 - 0x0000555555558008 is .got.plt
        0x0000555555558008 - 0x0000555555558018 is .data
        0x0000555555558018 - 0x0000555555558020 is .bss
        0x00007ffff7fc7238 - 0x00007ffff7fc725c is .note.gnu.build-id in /lib64/ld-linux-x86-64.so.2
        0x00007ffff7fc7260 - 0x00007ffff7fc7398 is .hash in /lib64/ld-linux-x86-64.so.2
        0x00007ffff7fc7398 - 0x00007ffff7fc74f4 is .gnu.hash in /lib64/ld-linux-x86-64.so.2
        0x00007ffff7fc74f8 - 0x00007ffff7fc78a0 is .dynsym in /lib64/ld-linux-x86-64.so.2
        0x00007ffff7fc78a0 - 0x00007ffff7fc7b51 is .dynstr in /lib64/ld-linux-x86-64.so.2
        0x00007ffff7fc7b52 - 0x00007ffff7fc7ba0 is .gnu.version in /lib64/ld-linux-x86-64.so.2
        0x00007ffff7fc7ba0 - 0x00007ffff7fc7c8c is .gnu.version_d in /lib64/ld-linux-x86-64.so.2
        0x00007ffff7fc7c90 - 0x00007ffff7fc7ca8 is .rela.dyn in /lib64/ld-linux-x86-64.so.2
        0x00007ffff7fc7ca8 - 0x00007ffff7fc7cc8 is .relr.dyn in /lib64/ld-linux-x86-64.so.2
        0x00007ffff7fc8000 - 0x00007ffff7fef2d1 is .text in /lib64/ld-linux-x86-64.so.2
        0x00007ffff7ff0000 - 0x00007ffff7ff6458 is .rodata in /lib64/ld-linux-x86-64.so.2
        0x00007ffff7ff6458 - 0x00007ffff7ff6f64 is .eh_frame_hdr in /lib64/ld-linux-x86-64.so.2
        0x00007ffff7ff6f68 - 0x00007ffff7ffac40 is .eh_frame in /lib64/ld-linux-x86-64.so.2
        0x00007ffff7ffb260 - 0x00007ffff7ffce80 is .data.rel.ro in /lib64/ld-linux-x86-64.so.2
        0x00007ffff7ffce80 - 0x00007ffff7ffd000 is .dynamic in /lib64/ld-linux-x86-64.so.2
        0x00007ffff7ffd000 - 0x00007ffff7ffdb4c is .data in /lib64/ld-linux-x86-64.so.2
        0x00007ffff7ffdb60 - 0x00007ffff7ffe310 is .bss in /lib64/ld-linux-x86-64.so.2
        0x00007ffff7fc5120 - 0x00007ffff7fc5170 is .hash in system-supplied DSO at 0x7ffff7fc5000
        0x00007ffff7fc5170 - 0x00007ffff7fc51d4 is .gnu.hash in system-supplied DSO at 0x7ffff7fc5000
        0x00007ffff7fc51d8 - 0x00007ffff7fc5340 is .dynsym in system-supplied DSO at 0x7ffff7fc5000
        0x00007ffff7fc5340 - 0x00007ffff7fc53dc is .dynstr in system-supplied DSO at 0x7ffff7fc5000
        0x00007ffff7fc53dc - 0x00007ffff7fc53fa is .gnu.version in system-supplied DSO at 0x7ffff7fc5000
        0x00007ffff7fc5400 - 0x00007ffff7fc5438 is .gnu.version_d in system-supplied DSO at 0x7ffff7fc5000
        0x00007ffff7fc5438 - 0x00007ffff7fc5558 is .dynamic in system-supplied DSO at 0x7ffff7fc5000
        0x00007ffff7fc5560 - 0x00007ffff7fc5570 is .rodata in system-supplied DSO at 0x7ffff7fc5000
        0x00007ffff7fc5570 - 0x00007ffff7fc55d4 is .note in system-supplied DSO at 0x7ffff7fc5000
        0x00007ffff7fc55d4 - 0x00007ffff7fc5628 is .eh_frame_hdr in system-supplied DSO at 0x7ffff7fc5000
        0x00007ffff7fc5628 - 0x00007ffff7fc5788 is .eh_frame in system-supplied DSO at 0x7ffff7fc5000
        0x00007ffff7fc57a0 - 0x00007ffff7fc6601 is .text in system-supplied DSO at 0x7ffff7fc5000
        0x00007ffff7fc6601 - 0x00007ffff7fc66d3 is .altinstructions in system-supplied DSO at 0x7ffff7fc5000
        0x00007ffff7fc66d3 - 0x00007ffff7fc670f is .altinstr_replacement in system-supplied DSO at 0x7ffff7fc5000
        0x00007ffff7db5388 - 0x00007ffff7db53a8 is .note.gnu.property in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7db53a8 - 0x00007ffff7db53cc is .note.gnu.build-id in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7db53d0 - 0x00007ffff7db9520 is .hash in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7db9520 - 0x00007ffff7dbe600 is .gnu.hash in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7dbe600 - 0x00007ffff7dd0e58 is .dynsym in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7dd0e58 - 0x00007ffff7dd9701 is .dynstr in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7dd9702 - 0x00007ffff7ddafb4 is .gnu.version in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7ddafb8 - 0x00007ffff7ddb588 is .gnu.version_d in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7ddb588 - 0x00007ffff7ddb5d8 is .gnu.version_r in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7ddb5d8 - 0x00007ffff7ddbe18 is .rela.dyn in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7ddbe18 - 0x00007ffff7ddc3d0 is .rela.plt in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7ddc3d0 - 0x00007ffff7ddc4e8 is .relr.dyn in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7ddd000 - 0x00007ffff7ddd3e0 is .plt in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7ddd3e0 - 0x00007ffff7ddd3f0 is .plt.got in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7ddd400 - 0x00007ffff7f4117d is .text in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7f42000 - 0x00007ffff7f680e0 is .rodata in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7f680e0 - 0x00007ffff7f6fafc is .eh_frame_hdr in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7f6fb00 - 0x00007ffff7f96de8 is .eh_frame in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7f96de8 - 0x00007ffff7f973d3 is .gcc_except_table in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7f973d4 - 0x00007ffff7f973f4 is .note.ABI-tag in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7f97400 - 0x00007ffff7f97460 is rodata.cst32 in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7f97460 - 0x00007ffff7f9747c is .interp in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7f98b58 - 0x00007ffff7f98b68 is .tdata in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7f98b68 - 0x00007ffff7f98be0 is .tbss in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7f98b68 - 0x00007ffff7f98b80 is .init_array in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7f98b80 - 0x00007ffff7f9b920 is .data.rel.ro in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7f9b920 - 0x00007ffff7f9bb60 is .dynamic in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7f9bb60 - 0x00007ffff7f9bfe8 is .got in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7f9c000 - 0x00007ffff7f9d6c8 is .data in /lib/x86_64-linux-gnu/libc.so.6
        0x00007ffff7f9d6e0 - 0x00007ffff7faae78 is .bss in /lib/x86_64-linux-gnu/libc.so.6
```

Now the shared libraries have been mapped in the `mmap` region. And these extra mappings are for them.

---

### What gets mapped?

Let's print the program headers table.
```bash
$ readelf hello -l

Elf file type is DYN (Position-Independent Executable file)
Entry point 0x1050
There are 14 program headers, starting at offset 64

Program Headers:
  Type           Offset             VirtAddr           PhysAddr           FileSiz            MemSiz              Flags  Align
  PHDR           0x0000000000000040 0x0000000000000040 0x0000000000000040 0x0000000000000310 0x0000000000000310  R      0x8
  INTERP         0x0000000000000394 0x0000000000000394 0x0000000000000394 0x000000000000001c 0x000000000000001c  R      0x1
           [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
  LOAD           0x0000000000000000 0x0000000000000000 0x0000000000000000 0x0000000000000628 0x0000000000000628  R      0x1000
  LOAD           0x0000000000001000 0x0000000000001000 0x0000000000001000 0x000000000000015d 0x000000000000015d  R E    0x1000
  LOAD           0x0000000000002000 0x0000000000002000 0x0000000000002000 0x000000000000010c 0x000000000000010c  R      0x1000
  LOAD           0x0000000000002dd0 0x0000000000003dd0 0x0000000000003dd0 0x0000000000000248 0x0000000000000250  RW     0x1000
  DYNAMIC        0x0000000000002de0 0x0000000000003de0 0x0000000000003de0 0x00000000000001e0 0x00000000000001e0  RW     0x8
  NOTE           0x0000000000000350 0x0000000000000350 0x0000000000000350 0x0000000000000020 0x0000000000000020  R      0x8
  NOTE           0x0000000000000370 0x0000000000000370 0x0000000000000370 0x0000000000000024 0x0000000000000024  R      0x4
  NOTE           0x00000000000020ec 0x00000000000020ec 0x00000000000020ec 0x0000000000000020 0x0000000000000020  R      0x4
  GNU_PROPERTY   0x0000000000000350 0x0000000000000350 0x0000000000000350 0x0000000000000020 0x0000000000000020  R      0x8
  GNU_EH_FRAME   0x0000000000002014 0x0000000000002014 0x0000000000002014 0x000000000000002c 0x000000000000002c  R      0x4
  GNU_STACK      0x0000000000000000 0x0000000000000000 0x0000000000000000 0x0000000000000000 0x0000000000000000  RW     0x10
  GNU_RELRO      0x0000000000002dd0 0x0000000000003dd0 0x0000000000003dd0 0x0000000000000230 0x0000000000000230  R      0x1

 Section to Segment mapping:
  Segment Sections...
   00     
   01     .interp 
   02     .note.gnu.property .note.gnu.build-id .interp .gnu.hash .dynsym .dynstr .gnu.version .gnu.version_r .rela.dyn .rela.plt 
   03     .init .plt .plt.got .text .fini 
   04     .rodata .eh_frame_hdr .eh_frame .note.ABI-tag 
   05     .init_array .fini_array .dynamic .got .got.plt .data .bss 
   06     .dynamic 
   07     .note.gnu.property 
   08     .note.gnu.build-id 
   09     .note.ABI-tag 
   10     .note.gnu.property 
   11     .eh_frame_hdr 
   12     
   13     .init_array .fini_array .dynamic .got 
```

Focus on the section to segment mapping part.
  - The four LOAD segments are indexed as 2, 3, 4 and 5. Let's check the mappings for these segments.
  - Their order matches with the output of `info files`.
  - They are 26 in total and the count matches as well.
  - ***This proves that only the segments of type "LOAD" are mapped in the virtual address space.***

---

### Mapped sections

Let's print the section headers table.
```bash
$ readelf hello -S

There are 37 section headers, starting at offset 0x38f8:

Section Headers:
  [Nr] Name              Type         Address           Offset    Size              EntSize          Flags  Link  Info  Align
  [ 0]                   NULL         0000000000000000  00000000  0000000000000000  0000000000000000         0     0     0
  [ 1] .note.gnu.pr[...] NOTE         0000000000000350  00000350  0000000000000020  0000000000000000   A     0     0     8
  [ 2] .note.gnu.bu[...] NOTE         0000000000000370  00000370  0000000000000024  0000000000000000   A     0     0     4
  [ 3] .interp           PROGBITS     0000000000000394  00000394  000000000000001c  0000000000000000   A     0     0     1
  [ 4] .gnu.hash         GNU_HASH     00000000000003b0  000003b0  0000000000000024  0000000000000000   A     5     0     8
  [ 5] .dynsym           DYNSYM       00000000000003d8  000003d8  00000000000000a8  0000000000000018   A     6     1     8
  [ 6] .dynstr           STRTAB       0000000000000480  00000480  000000000000008d  0000000000000000   A     0     0     1
  [ 7] .gnu.version      VERSYM       000000000000050e  0000050e  000000000000000e  0000000000000002   A     5     0     2
  [ 8] .gnu.version_r    VERNEED      0000000000000520  00000520  0000000000000030  0000000000000000   A     6     1     8
  [ 9] .rela.dyn         RELA         0000000000000550  00000550  00000000000000c0  0000000000000018   A     5     0     8
  [10] .rela.plt         RELA         0000000000000610  00000610  0000000000000018  0000000000000018  AI     5    24     8
  [11] .init             PROGBITS     0000000000001000  00001000  0000000000000017  0000000000000000  AX     0     0     4
  [12] .plt              PROGBITS     0000000000001020  00001020  0000000000000020  0000000000000010  AX     0     0     16
  [13] .plt.got          PROGBITS     0000000000001040  00001040  0000000000000008  0000000000000008  AX     0     0     8
  [14] .text             PROGBITS     0000000000001050  00001050  0000000000000103  0000000000000000  AX     0     0     16
  [15] .fini             PROGBITS     0000000000001154  00001154  0000000000000009  0000000000000000  AX     0     0     4
  [16] .rodata           PROGBITS     0000000000002000  00002000  0000000000000012  0000000000000000   A     0     0     4
  [17] .eh_frame_hdr     PROGBITS     0000000000002014  00002014  000000000000002c  0000000000000000   A     0     0     4
  [18] .eh_frame         PROGBITS     0000000000002040  00002040  00000000000000ac  0000000000000000   A     0     0     8
  [19] .note.ABI-tag     NOTE         00000000000020ec  000020ec  0000000000000020  0000000000000000   A     0     0     4
  [20] .init_array       INIT_ARRAY   0000000000003dd0  00002dd0  0000000000000008  0000000000000008  WA     0     0     8
  [21] .fini_array       FINI_ARRAY   0000000000003dd8  00002dd8  0000000000000008  0000000000000008  WA     0     0     8
  [22] .dynamic          DYNAMIC      0000000000003de0  00002de0  00000000000001e0  0000000000000010  WA     6     0     8
  [23] .got              PROGBITS     0000000000003fc0  00002fc0  0000000000000028  0000000000000008  WA     0     0     8
  [24] .got.plt          PROGBITS     0000000000003fe8  00002fe8  0000000000000020  0000000000000008  WA     0     0     8
  [25] .data             PROGBITS     0000000000004008  00003008  0000000000000010  0000000000000000  WA     0     0     8
  [26] .bss              NOBITS       0000000000004018  00003018  0000000000000008  0000000000000000  WA     0     0     1
  [27] .comment          PROGBITS     0000000000000000  00003018  000000000000001f  0000000000000001  MS     0     0     1
  [28] .debug_aranges    PROGBITS     0000000000000000  00003037  0000000000000030  0000000000000000         0     0     1
  [29] .debug_info       PROGBITS     0000000000000000  00003067  000000000000008c  0000000000000000         0     0     1
  [30] .debug_abbrev     PROGBITS     0000000000000000  000030f3  0000000000000045  0000000000000000         0     0     1
  [31] .debug_line       PROGBITS     0000000000000000  00003138  0000000000000050  0000000000000000         0     0     1
  [32] .debug_str        PROGBITS     0000000000000000  00003188  0000000000000097  0000000000000001  MS     0     0     1
  [33] .debug_line_str   PROGBITS     0000000000000000  0000321f  0000000000000031  0000000000000001  MS     0     0     1
  [34] .symtab           SYMTAB       0000000000000000  00003250  0000000000000360  0000000000000018        35    18     8
  [35] .strtab           STRTAB       0000000000000000  000035b0  00000000000001db  0000000000000000         0     0     1
  [36] .shstrtab         STRTAB       0000000000000000  0000378b  000000000000016a  0000000000000000         0     0     1
```
  - As always, the output is formatted for better readability.

We remember that our elf had 31 sections. The 6 extra sections are for debug information.

Let's focus on the size field. It is the length of each section. For example, take `.text`.
  - The size is 0x103, which is 295 in decimal.
  - The address range for `.text` as reported by `info files` is: `0x0000000000001050 - 0x0000000000001153`.
  - "0x1153 - 0x1050" is 0x103, exactly the same.
  - ***This proves that sections which are mapped are mapped exactly without any modification.***

---

### The address ranges?

Let's "examine" `.text`.

From our first gdb session, i.e {{< doclink "7b2345107d0e4d3ab0e3369174a52eb1" "byte addressable memory" >}}, we know that the "examine" command has an option to interpret the memory as instructions. We are going to use that.

```bash
(gdb) set disassembly-flavor intel
(gdb) x/295ib 0x1050

   0x1050 <_start>:     xor    ebp,ebp
   0x1052 <_start+2>:   mov    r9,rdx
   0x1055 <_start+5>:   pop    rsi
   0x1056 <_start+6>:   mov    rdx,rsp
   0x1059 <_start+9>:   and    rsp,0xfffffffffffffff0
   0x105d <_start+13>:  push   rax
   0x105e <_start+14>:  push   rsp
   0x105f <_start+15>:  xor    r8d,r8d
   0x1062 <_start+18>:  xor    ecx,ecx
   0x1064 <_start+20>:  lea    rdi,[rip+0xce]        # 0x1139 <main>
   0x106b <_start+27>:  call   QWORD PTR [rip+0x2f4f]        # 0x3fc0
   0x1071 <_start+33>:  hlt
   0x1072:      cs nop WORD PTR [rax+rax*1+0x0]
   0x107c:      nop    DWORD PTR [rax+0x0]

   0x1080 <deregister_tm_clones>:       lea    rdi,[rip+0x2f91]        # 0x4018 <completed.0>
   0x1087 <deregister_tm_clones+7>:     lea    rax,[rip+0x2f8a]        # 0x4018 <completed.0>
   0x108e <deregister_tm_clones+14>:    cmp    rax,rdi
   0x1091 <deregister_tm_clones+17>:    je     0x10a8 <deregister_tm_clones+40>
   0x1093 <deregister_tm_clones+19>:    mov    rax,QWORD PTR [rip+0x2f2e]        # 0x3fc8
   0x109a <deregister_tm_clones+26>:    test   rax,rax
   0x109d <deregister_tm_clones+29>:    je     0x10a8 <deregister_tm_clones+40>
   0x109f <deregister_tm_clones+31>:    jmp    rax
   0x10a1 <deregister_tm_clones+33>:    nop    DWORD PTR [rax+0x0]
   0x10a8 <deregister_tm_clones+40>:    ret
   0x10a9 <deregister_tm_clones+41>:    nop    DWORD PTR [rax+0x0]

   0x10b0 <register_tm_clones>: lea    rdi,[rip+0x2f61]        # 0x4018 <completed.0>
   0x10b7 <register_tm_clones+7>:       lea    rsi,[rip+0x2f5a]        # 0x4018 <completed.0>
   0x10be <register_tm_clones+14>:      sub    rsi,rdi
   0x10c1 <register_tm_clones+17>:      mov    rax,rsi
   0x10c4 <register_tm_clones+20>:      shr    rsi,0x3f
   0x10c8 <register_tm_clones+24>:      sar    rax,0x3
   0x10cc <register_tm_clones+28>:      add    rsi,rax
   0x10cf <register_tm_clones+31>:      sar    rsi,1
   0x10d2 <register_tm_clones+34>:      je     0x10e8 <register_tm_clones+56>
   0x10d4 <register_tm_clones+36>:      mov    rax,QWORD PTR [rip+0x2efd]        # 0x3fd8
   0x10db <register_tm_clones+43>:      test   rax,rax
   0x10de <register_tm_clones+46>:      je     0x10e8 <register_tm_clones+56>
   0x10e0 <register_tm_clones+48>:      jmp    rax
   0x10e2 <register_tm_clones+50>:      nop    WORD PTR [rax+rax*1+0x0]
   0x10e8 <register_tm_clones+56>:      ret
   0x10e9 <register_tm_clones+57>:      nop    DWORD PTR [rax+0x0]

   0x10f0 <__do_global_dtors_aux>:      endbr64
   0x10f4 <__do_global_dtors_aux+4>:    cmp    BYTE PTR [rip+0x2f1d],0x0        # 0x4018 <completed.0>
   0x10fb <__do_global_dtors_aux+11>:   jne    0x1128 <__do_global_dtors_aux+56>
   0x10fd <__do_global_dtors_aux+13>:   push   rbp
   0x10fe <__do_global_dtors_aux+14>:   cmp    QWORD PTR [rip+0x2eda],0x0        # 0x3fe0
   0x1106 <__do_global_dtors_aux+22>:   mov    rbp,rsp
   0x1109 <__do_global_dtors_aux+25>:   je     0x1117 <__do_global_dtors_aux+39>
   0x110b <__do_global_dtors_aux+27>:   mov    rdi,QWORD PTR [rip+0x2efe]        # 0x4010
   0x1112 <__do_global_dtors_aux+34>:   call   0x1040 <__cxa_finalize@plt>
   0x1117 <__do_global_dtors_aux+39>:   call   0x1080 <deregister_tm_clones>
   0x111c <__do_global_dtors_aux+44>:   mov    BYTE PTR [rip+0x2ef5],0x1        # 0x4018 <completed.0>
   0x1123 <__do_global_dtors_aux+51>:   pop    rbp
   0x1124 <__do_global_dtors_aux+52>:   ret
   0x1125 <__do_global_dtors_aux+53>:   nop    DWORD PTR [rax]
   0x1128 <__do_global_dtors_aux+56>:   ret
   0x1129 <__do_global_dtors_aux+57>:   nop    DWORD PTR [rax+0x0]

   0x1130 <frame_dummy>:        endbr64
   0x1134 <frame_dummy+4>:      jmp    0x10b0 <register_tm_clones>

   0x1139 <main>:       push   rbp
   0x113a <main+1>:     mov    rbp,rsp
   0x113d <main+4>:     lea    rax,[rip+0xec0]        # 0x2004
   0x1144 <main+11>:    mov    rdi,rax
   0x1147 <main+14>:    call   0x1030 <puts@plt>
   0x114c <main+19>:    mov    eax,0x0
   0x1151 <main+24>:    pop    rbp
   0x1152 <main+25>:    ret

   0x1153:      Cannot access memory at address 0x1153
```

The output looks quite familiar once again. Because we've already explored `objdump -D`. And if we do:
```bash
$ objdump hello -D -j .text

hello:     file format elf64-x86-64


Disassembly of section .text:

0000000000001050 <_start>:
    1050:	31 ed                	xor    ebp,ebp
    1052:	49 89 d1             	mov    r9,rdx
    1055:	5e                   	pop    rsi
    1056:	48 89 e2             	mov    rdx,rsp
    1059:	48 83 e4 f0          	and    rsp,0xfffffffffffffff0
    105d:	50                   	push   rax
    105e:	54                   	push   rsp
    105f:	45 31 c0             	xor    r8d,r8d
    1062:	31 c9                	xor    ecx,ecx
    1064:	48 8d 3d ce 00 00 00 	lea    rdi,[rip+0xce]        # 1139 <main>
    106b:	ff 15 4f 2f 00 00    	call   QWORD PTR [rip+0x2f4f]        # 3fc0 <__libc_start_main@GLIBC_2.34>
    1071:	f4                   	hlt
    1072:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    1079:	00 00 00 
    107c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]

0000000000001080 <deregister_tm_clones>:
    1080:	48 8d 3d 91 2f 00 00 	lea    rdi,[rip+0x2f91]        # 4018 <__TMC_END__>
    1087:	48 8d 05 8a 2f 00 00 	lea    rax,[rip+0x2f8a]        # 4018 <__TMC_END__>
    108e:	48 39 f8             	cmp    rax,rdi
    1091:	74 15                	je     10a8 <deregister_tm_clones+0x28>
    1093:	48 8b 05 2e 2f 00 00 	mov    rax,QWORD PTR [rip+0x2f2e]        # 3fc8 <_ITM_deregisterTMCloneTable@Base>
    109a:	48 85 c0             	test   rax,rax
    109d:	74 09                	je     10a8 <deregister_tm_clones+0x28>
    109f:	ff e0                	jmp    rax
    10a1:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
    10a8:	c3                   	ret
    10a9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

00000000000010b0 <register_tm_clones>:
    10b0:	48 8d 3d 61 2f 00 00 	lea    rdi,[rip+0x2f61]        # 4018 <__TMC_END__>
    10b7:	48 8d 35 5a 2f 00 00 	lea    rsi,[rip+0x2f5a]        # 4018 <__TMC_END__>
    10be:	48 29 fe             	sub    rsi,rdi
    10c1:	48 89 f0             	mov    rax,rsi
    10c4:	48 c1 ee 3f          	shr    rsi,0x3f
    10c8:	48 c1 f8 03          	sar    rax,0x3
    10cc:	48 01 c6             	add    rsi,rax
    10cf:	48 d1 fe             	sar    rsi,1
    10d2:	74 14                	je     10e8 <register_tm_clones+0x38>
    10d4:	48 8b 05 fd 2e 00 00 	mov    rax,QWORD PTR [rip+0x2efd]        # 3fd8 <_ITM_registerTMCloneTable@Base>
    10db:	48 85 c0             	test   rax,rax
    10de:	74 08                	je     10e8 <register_tm_clones+0x38>
    10e0:	ff e0                	jmp    rax
    10e2:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
    10e8:	c3                   	ret
    10e9:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

00000000000010f0 <__do_global_dtors_aux>:
    10f0:	f3 0f 1e fa          	endbr64
    10f4:	80 3d 1d 2f 00 00 00 	cmp    BYTE PTR [rip+0x2f1d],0x0        # 4018 <__TMC_END__>
    10fb:	75 2b                	jne    1128 <__do_global_dtors_aux+0x38>
    10fd:	55                   	push   rbp
    10fe:	48 83 3d da 2e 00 00 	cmp    QWORD PTR [rip+0x2eda],0x0        # 3fe0 <__cxa_finalize@GLIBC_2.2.5>
    1105:	00 
    1106:	48 89 e5             	mov    rbp,rsp
    1109:	74 0c                	je     1117 <__do_global_dtors_aux+0x27>
    110b:	48 8b 3d fe 2e 00 00 	mov    rdi,QWORD PTR [rip+0x2efe]        # 4010 <__dso_handle>
    1112:	e8 29 ff ff ff       	call   1040 <__cxa_finalize@plt>
    1117:	e8 64 ff ff ff       	call   1080 <deregister_tm_clones>
    111c:	c6 05 f5 2e 00 00 01 	mov    BYTE PTR [rip+0x2ef5],0x1        # 4018 <__TMC_END__>
    1123:	5d                   	pop    rbp
    1124:	c3                   	ret
    1125:	0f 1f 00             	nop    DWORD PTR [rax]
    1128:	c3                   	ret
    1129:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]

0000000000001130 <frame_dummy>:
    1130:	f3 0f 1e fa          	endbr64
    1134:	e9 77 ff ff ff       	jmp    10b0 <register_tm_clones>

0000000000001139 <main>:
    1139:	55                   	push   rbp
    113a:	48 89 e5             	mov    rbp,rsp
    113d:	48 8d 05 c0 0e 00 00 	lea    rax,[rip+0xec0]        # 2004 <_IO_stdin_used+0x4>
    1144:	48 89 c7             	mov    rdi,rax
    1147:	e8 e4 fe ff ff       	call   1030 <puts@plt>
    114c:	b8 00 00 00 00       	mov    eax,0x0
    1151:	5d                   	pop    rbp
    1152:	c3                   	ret
```
..boom, the magic has happened.

Lets diff both the assemblies.

| Symbol | Lines In Runtime Disassembly | Lines In Objdump Disassembly |
| :--- | :--- | :--- |
| _start | 14 | 15 (empty instruction) |
| deregister_tm_clones  | 11 | 11 |
| register_tm_clones    | 16 | 16 |
| __do_global_dtors_aux | 16 | 17 (empty instruction) |
| frame_dummy | 2 | 2 |
| main   | 8 | 8 |
| Total | 67 | 67 + 2 |

I don't know if we can get any better proof for the fact that *"sections which are to be mapped are mapped exactly without any modification"*.
  - This shows why our decision to statically explore the "full disassembly" was the right decision.
  - It looked pointless and time wasting 3 months back. But now it is helping us because we have burnt the fear of looking at huge disassemblies.
  - Every gdb session is just going to increase our capacity to comprehend huge disassemblies without shivering.

That happens when you avoid shortcuts and I am glad we have avoided those shortcuts.

---

### What to do with this information?

This information alone is not going to do any wonders. But the best part is, the information "which we supposedly lack right now" is already with us, we just need to revise a few things.

We have discussed ELF quite in-detail, which is why we have a rough idea about "what goes where". For example:
  - All the printfs take at least one constant string. That string is not changing in any circumstance. This means it qualifies to be a part of `.rodata` section.
  - With this information, whenever we see a .rodata section mapped in VAS, we know what it will contain probably.
  - This knowledge of "what might be there" helps us forming the right "examine" command.
  - If the data is a string, we will use `s` in type interpretation. If it is an instruction, we will use `i`. And so on..

The terrain is basically:
  - what is mapped in the virtual address space? and
  - which mapping requires which interpretation rules?

That's it. We have mapped the terrain.

We'll explore the practical side in the next write up.