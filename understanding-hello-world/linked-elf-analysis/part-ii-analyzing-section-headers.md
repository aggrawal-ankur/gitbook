---
description: >-
  Section headers, segments and program headers; all of these are linked.
  Therefore, this article is aimed at establishing that understanding before we
  move to program headers table.
---

# Analyzing Section Headers

## What are sections?

Sections are formally defined logical divisions inside an ELF file in the ELF specification. They describe how an ELF file organizes its contents for linking, loading, and debugging.

These are the section headers in our binary.

```
Section Headers:
  [Nr] Name              Type           Address            Offset     Size               EntSize           Flags  Link  Info  Align
  [ 0]                   NULL           0000000000000000   00000000   0000000000000000   0000000000000000            0     0     0
  [ 1] .note.gnu.pr[...] NOTE           0000000000000350   00000350   0000000000000020   0000000000000000    A       0     0     8
  [ 2] .note.gnu.bu[...] NOTE           0000000000000370   00000370   0000000000000024   0000000000000000    A       0     0     4
  [ 3] .interp           PROGBITS       0000000000000394   00000394   000000000000001c   0000000000000000    A       0     0     1
  [ 4] .gnu.hash         GNU_HASH       00000000000003b0   000003b0   0000000000000024   0000000000000000    A       5     0     8
  [ 5] .dynsym           DYNSYM         00000000000003d8   000003d8   00000000000000a8   0000000000000018    A       6     1     8
  [ 6] .dynstr           STRTAB         0000000000000480   00000480   000000000000008d   0000000000000000    A       0     0     1
  [ 7] .gnu.version      VERSYM         000000000000050e   0000050e   000000000000000e   0000000000000002    A       5     0     2
  [ 8] .gnu.version_r    VERNEED        0000000000000520   00000520   0000000000000030   0000000000000000    A       6     1     8
  [ 9] .rela.dyn         RELA           0000000000000550   00000550   00000000000000c0   0000000000000018    A       5     0     8
  [10] .rela.plt         RELA           0000000000000610   00000610   0000000000000018   0000000000000018   AI       5    24     8
  [11] .init             PROGBITS       0000000000001000   00001000   0000000000000017   0000000000000000   AX       0     0     4
  [12] .plt              PROGBITS       0000000000001020   00001020   0000000000000020   0000000000000010   AX       0     0     16
  [13] .plt.got          PROGBITS       0000000000001040   00001040   0000000000000008   0000000000000008   AX       0     0     8
  [14] .text             PROGBITS       0000000000001050   00001050   0000000000000103   0000000000000000   AX       0     0     16
  [15] .fini             PROGBITS       0000000000001154   00001154   0000000000000009   0000000000000000   AX       0     0     4
  [16] .rodata           PROGBITS       0000000000002000   00002000   0000000000000012   0000000000000000    A       0     0     4
  [17] .eh_frame_hdr     PROGBITS       0000000000002014   00002014   000000000000002c   0000000000000000    A       0     0     4
  [18] .eh_frame         PROGBITS       0000000000002040   00002040   00000000000000ac   0000000000000000    A       0     0     8
  [19] .note.ABI-tag     NOTE           00000000000020ec   000020ec   0000000000000020   0000000000000000    A       0     0     4
  [20] .init_array       INIT_ARRAY     0000000000003dd0   00002dd0   0000000000000008   0000000000000008   WA       0     0     8
  [21] .fini_array       FINI_ARRAY     0000000000003dd8   00002dd8   0000000000000008   0000000000000008   WA       0     0     8
  [22] .dynamic          DYNAMIC        0000000000003de0   00002de0   00000000000001e0   0000000000000010   WA       6     0     8
  [23] .got              PROGBITS       0000000000003fc0   00002fc0   0000000000000028   0000000000000008   WA       0     0     8
  [24] .got.plt          PROGBITS       0000000000003fe8   00002fe8   0000000000000020   0000000000000008   WA       0     0     8
  [25] .data             PROGBITS       0000000000004008   00003008   0000000000000010   0000000000000000   WA       0     0     8
  [26] .bss              NOBITS         0000000000004018   00003018   0000000000000008   0000000000000000   WA       0     0     1
  [27] .comment          PROGBITS       0000000000000000   00003018   000000000000001f   0000000000000001   MS       0     0     1
  [28] .symtab           SYMTAB         0000000000000000   00003038   0000000000000360   0000000000000018           29    18     8
  [29] .strtab           STRTAB         0000000000000000   00003398   00000000000001db   0000000000000000            0     0     1
  [30] .shstrtab         STRTAB         0000000000000000   00003573   000000000000011a   0000000000000000            0     0     1

 Key to Flags:
   W (write), A (alloc), X (execute), M (merge), S (strings), I (info),
   L (link order), O (extra OS processing required), G (group), T (TLS),
   C (compressed), x (unknown), o (OS specific), E (exclude),
   D (mbind), l (large), p (processor specific)
```

**Note:** You may not find your output like this because I have formatted it manually so that it is clear and makes sense.

We are already familiar with the attributes of this table, so we'll skip that. Lets have a look at these sections.

## Baseline Understanding Of Sections

<table><thead><tr><th width="202">Name</th><th width="112">Type</th><th width="239">Explanation</th><th>View</th></tr></thead><tbody><tr><td>Section 0</td><td>NULL</td><td>This section is empty. It is their just of alignment purposes. Nothing much. That's why it is of type NULL and everything is zeroed out.</td><td></td></tr><tr><td><code>.note.gnu.property</code></td><td><code>NOTE</code></td><td>Metadata for hardware/ABI features (e.g., IBT, SHSTK).</td><td><code>readelf -n</code></td></tr><tr><td><code>.note.gnu.build-id</code></td><td><code>NOTE</code></td><td>Unique hash/fingerprint of the binary for debug symbol matching.</td><td><code>readelf -n</code></td></tr><tr><td><code>.interp</code></td><td><code>PROGBITS</code></td><td><p>Path to the dynamic loader program (<code>ld.so</code>) for resolving cross-references.</p><p><code>PROGBITS</code> means a section that holds <strong>raw data</strong> to be loaded into memory, such as code, constants, or initialized variables.</p></td><td><code>readelf -p .interp</code></td></tr><tr><td><code>.gnu.hash</code></td><td><code>GNU_HASH</code></td><td>Hash table for faster dynamic symbol lookup.<br><strong>We need not to dive into this much.</strong></td><td>NA</td></tr><tr><td><code>.dynsym</code></td><td><code>DYNSYM</code></td><td>Dynamic symbol table used at runtime linking by the interpreter program (<code>ld-linux</code>).</td><td>NA</td></tr><tr><td><code>.dynstr</code></td><td><code>STRTAB</code></td><td>String table for names in <code>.dynsym</code>.</td><td><code>readelf -p .dynstr</code></td></tr><tr><td><code>.gnu.version</code></td><td><code>VERSYM</code></td><td>Version info for each dynamic symbol.</td><td>NA</td></tr><tr><td><code>.gnu.version_r</code></td><td><code>VERNEED</code></td><td>Declares required versions of shared libraries.</td><td>NA</td></tr><tr><td><code>.rela.dyn</code></td><td><code>RELA</code></td><td>Relocation entries for global data and non-PLT addresses.</td><td></td></tr><tr><td><code>.rela.plt</code></td><td><code>RELA</code></td><td>Relocation entries via PLT.</td><td></td></tr><tr><td><code>.init</code></td><td><code>PROGBITS</code></td><td>Code run before <code>main()</code> (init routine).</td><td>NA</td></tr><tr><td><code>.plt</code></td><td><code>PROGBITS</code></td><td>Procedure Linkage Table — stubs for external function calls.</td><td>NA</td></tr><tr><td><code>.plt.got</code></td><td><code>PROGBITS</code></td><td>Used in lazy binding (jump to GOT entries).</td><td>NA</td></tr><tr><td><code>.text</code></td><td><code>PROGBITS</code></td><td>Main executable code section.</td><td>NA</td></tr><tr><td><code>.fini</code></td><td><code>PROGBITS</code></td><td>Code run after <code>main()</code> returns (cleanup).</td><td>NA</td></tr><tr><td><code>.rodata</code></td><td><code>PROGBITS</code></td><td>Read-only static data (e.g., strings, constants).</td><td><code>readelf -p .rodata</code></td></tr><tr><td><code>.eh_frame_hdr</code></td><td><code>PROGBITS</code></td><td>Header for exception handling frames.</td><td></td></tr><tr><td><code>.eh_frame</code></td><td><code>PROGBITS</code></td><td>Stack unwinding info for exceptions or debugging.</td><td></td></tr><tr><td><code>.note.ABI-tag</code></td><td><code>NOTE</code></td><td>Identifies the target OS/ABI version.</td><td></td></tr><tr><td><code>.init_array</code></td><td><code>INIT_ARRAY</code></td><td>List of constructor function pointers (run before <code>main</code>).</td><td></td></tr><tr><td><code>.fini_array</code></td><td><code>FINI_ARRAY</code></td><td>List of destructor function pointers (run after <code>main</code>).</td><td></td></tr><tr><td><code>.dynamic</code></td><td><code>DYNAMIC</code></td><td>Table used by the dynamic linker to resolve symbols/relocations.</td><td></td></tr><tr><td><code>.got</code></td><td><code>PROGBITS</code></td><td>Global Offset Table for storing resolved addresses.</td><td></td></tr><tr><td><code>.got.plt</code></td><td><code>PROGBITS</code></td><td>GOT entries specifically for <code>.plt</code> lazy binding.</td><td></td></tr><tr><td><code>.data</code></td><td><code>PROGBITS</code></td><td>Writable static/global data.</td><td></td></tr><tr><td><code>.bss</code></td><td><code>NOBITS</code></td><td>Uninitialized global/static data (zeroed at runtime).</td><td></td></tr><tr><td><code>.comment</code></td><td><code>PROGBITS</code></td><td>Compiler version or build metadata (ignored at runtime).</td><td></td></tr><tr><td><code>.symtab</code></td><td><code>SYMTAB</code></td><td>Full symbol table (for static linking/debugging).</td><td></td></tr><tr><td><code>.strtab</code></td><td><code>STRTAB</code></td><td>String table for names in <code>.symtab</code>.</td><td><code>readelf -p .strtab</code></td></tr><tr><td><code>.shstrtab</code></td><td><code>STRTAB</code></td><td>String table for section names themselves.</td><td><code>readelf -p .shstrtab</code></td></tr></tbody></table>

## What is their significance?

Sections are used by the linker to organize our code/data/symbols etc. Lets usage an analogy to understand the importance of their existence.

Consider an ELF as a room, containing so many different types of things. There are clothes, pens and paper, bottle, bag, notebooks etc. And everything is scattered.

To make sense of them, you decided to clear the floor and put everything categorized on the floor.

* You put papers together.
* You put notebooks together.
* You put pens together.
* You put jeans together.
* You put shirts together.
* You put books together.

**This resembles sections.**

Now we have so many things, a little bit organized. But, further organization can be made.

* Books, papers and pens are related things. They are all stationary. So, they can be put together in the bookshelf.
* &#x20;Jeans, shirts, t-shirts, lower, jacket etc.... all of them are clothes. So, they can be put together in the wardrobe.
* And so on....

**This further categorization is what segments are.**

* When you have to look for fiction books, or course books, you don't go to different place. They are within the same bookshelf.
* When you want a lower or a jacket, you don't go to separate places again. They are within the same wardrobe. You want party clothes or comfy clothes, all of them are in the same wardrobe.
* The idea behind segments is that you group sections logically to the point that no further categorization can be made and all the related things can be accessed at one place in a logical manner.

Ultimately, do you end up accessing the clothes individually or through the wardrobe? The answer is through the wardrobe.

* Sections are just kind of intermediaries. They are used initially to do things but they are not the ones that are ultimately used in the end.
* Segments, on the other hand, evolve from sections and these are what that get used at runtime.

Once these segments are created, program headers come into existence.

## There's something off here



## Conclusion

Sections are used at build time.

Segments are used at runtime.
