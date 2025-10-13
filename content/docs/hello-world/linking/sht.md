---
id: a27011754d064d3d809e59d9108a0ea8
title: Section Headers
weight: 3
---

Sections are logical divisions inside an ELF file. They describe how an ELF file organize its contents.

These are the section headers in our binary.
```bash
$ readelf hello -S

Section Headers:
  [Nr] Name              Type           Address            Offset     Size               EntSize           Flags  Link  Info  Align
  [ 0]                   NULL           0000000000000000   00000000   0000000000000000   0000000000000000           0     0     0
  [ 1] .note.gnu.pr[...] NOTE           0000000000000350   00000350   0000000000000020   0000000000000000    A      0     0     8
  [ 2] .note.gnu.bu[...] NOTE           0000000000000370   00000370   0000000000000024   0000000000000000    A      0     0     4
  [ 3] .interp           PROGBITS       0000000000000394   00000394   000000000000001c   0000000000000000    A      0     0     1
  [ 4] .gnu.hash         GNU_HASH       00000000000003b0   000003b0   0000000000000024   0000000000000000    A      5     0     8
  [ 5] .dynsym           DYNSYM         00000000000003d8   000003d8   00000000000000a8   0000000000000018    A      6     1     8
  [ 6] .dynstr           STRTAB         0000000000000480   00000480   000000000000008d   0000000000000000    A      0     0     1
  [ 7] .gnu.version      VERSYM         000000000000050e   0000050e   000000000000000e   0000000000000002    A      5     0     2
  [ 8] .gnu.version_r    VERNEED        0000000000000520   00000520   0000000000000030   0000000000000000    A      6     1     8
  [ 9] .rela.dyn         RELA           0000000000000550   00000550   00000000000000c0   0000000000000018    A      5     0     8
  [10] .rela.plt         RELA           0000000000000610   00000610   0000000000000018   0000000000000018   AI      5    24     8
  [11] .init             PROGBITS       0000000000001000   00001000   0000000000000017   0000000000000000   AX      0     0     4
  [12] .plt              PROGBITS       0000000000001020   00001020   0000000000000020   0000000000000010   AX      0     0    16
  [13] .plt.got          PROGBITS       0000000000001040   00001040   0000000000000008   0000000000000008   AX      0     0     8
  [14] .text             PROGBITS       0000000000001050   00001050   0000000000000103   0000000000000000   AX      0     0    16
  [15] .fini             PROGBITS       0000000000001154   00001154   0000000000000009   0000000000000000   AX      0     0     4
  [16] .rodata           PROGBITS       0000000000002000   00002000   0000000000000012   0000000000000000    A      0     0     4
  [17] .eh_frame_hdr     PROGBITS       0000000000002014   00002014   000000000000002c   0000000000000000    A      0     0     4
  [18] .eh_frame         PROGBITS       0000000000002040   00002040   00000000000000ac   0000000000000000    A      0     0     8
  [19] .note.ABI-tag     NOTE           00000000000020ec   000020ec   0000000000000020   0000000000000000    A      0     0     4
  [20] .init_array       INIT_ARRAY     0000000000003dd0   00002dd0   0000000000000008   0000000000000008   WA      0     0     8
  [21] .fini_array       FINI_ARRAY     0000000000003dd8   00002dd8   0000000000000008   0000000000000008   WA      0     0     8
  [22] .dynamic          DYNAMIC        0000000000003de0   00002de0   00000000000001e0   0000000000000010   WA      6     0     8
  [23] .got              PROGBITS       0000000000003fc0   00002fc0   0000000000000028   0000000000000008   WA      0     0     8
  [24] .got.plt          PROGBITS       0000000000003fe8   00002fe8   0000000000000020   0000000000000008   WA      0     0     8
  [25] .data             PROGBITS       0000000000004008   00003008   0000000000000010   0000000000000000   WA      0     0     8
  [26] .bss              NOBITS         0000000000004018   00003018   0000000000000008   0000000000000000   WA      0     0     1
  [27] .comment          PROGBITS       0000000000000000   00003018   000000000000001f   0000000000000001   MS      0     0     1
  [28] .symtab           SYMTAB         0000000000000000   00003038   0000000000000360   0000000000000018          29    18     8
  [29] .strtab           STRTAB         0000000000000000   00003398   00000000000001db   0000000000000000           0     0     1
  [30] .shstrtab         STRTAB         0000000000000000   00003573   000000000000011a   0000000000000000           0     0     1

 Key to Flags:
   W (write), A (alloc), X (execute), M (merge), S (strings), I (info),
   L (link order), O (extra OS processing required), G (group), T (TLS),
   C (compressed), x (unknown), o (OS specific), E (exclude),
   D (mbind), l (large), p (processor specific)
```
  - The output is formatted to improve readability.