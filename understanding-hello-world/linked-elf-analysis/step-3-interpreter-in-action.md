---
description: Now the interpreter has the control, what will it do? Let's find out.
---

# Step 3: Interpreter In Action

## Setup

This is the `.dynamic` section.

```
Dynamic section at offset 0x2de0 contains 26 entries:
  Tag                  Type             Name/Value
 0x0000000000000001    (NEEDED)         Shared library: [libc.so.6]
 0x000000000000000c    (INIT)           0x1000
 0x000000000000000d    (FINI)           0x1154
 0x0000000000000019    (INIT_ARRAY)     0x3dd0
 0x000000000000001b    (INIT_ARRAYSZ)   8 (bytes)
 0x000000000000001a    (FINI_ARRAY)     0x3dd8
 0x000000000000001c    (FINI_ARRAYSZ)   8 (bytes)
 0x000000006ffffef5    (GNU_HASH)       0x3b0
 0x0000000000000005    (STRTAB)         0x480
 0x0000000000000006    (SYMTAB)         0x3d8
 0x000000000000000a    (STRSZ)          141 (bytes)
 0x000000000000000b    (SYMENT)         24 (bytes)
 0x0000000000000015    (DEBUG)          0x0
 0x0000000000000003    (PLTGOT)         0x3fe8
 0x0000000000000002    (PLTRELSZ)       24 (bytes)
 0x0000000000000014    (PLTREL)         RELA
 0x0000000000000017    (JMPREL)         0x610
 0x0000000000000007    (RELA)           0x550
 0x0000000000000008    (RELASZ)         192 (bytes)
 0x0000000000000009    (RELAENT)        24 (bytes)
 0x000000006ffffffb    (FLAGS_1)        Flags: PIE
 0x000000006ffffffe    (VERNEED)        0x520
 0x000000006fffffff    (VERNEEDNUM)     1
 0x000000006ffffff0    (VERSYM)         0x50e
 0x000000006ffffff9    (RELACOUNT)      3
 0x0000000000000000    (NULL)           0x0
```

## Understanding the attributes

The `Tag` field identifies the purpose of each entry. It's an enum-like value defined in the ELF specification, used by the dynamic linker to understand what kind of information the entry holds.

The `Type` field again is an interpretation of the underlying unique numeric identifier which has a special meaning defined in the ELF specification. All in all, it identifies the type of entry.

The `Name/Value` field is the most complicated one here.

* When it comes to a shared library, this attribute holds a string name.
* When it comes to anything related to size, it stores a size.
* When it comes to offset, it stores `0x` prefixed addresses.

## Understanding Each Entry Type

<table data-header-hidden><thead><tr><th width="148"></th><th></th></tr></thead><tbody><tr><td><strong>Tag</strong></td><td><strong>Purpose</strong></td></tr><tr><td><code>NEEDED</code></td><td>Tells the linker a shared library is needed; value is offset into <code>.dynstr</code> pointing to the lib name (e.g. <code>"libc.so.6"</code>). Multiple entries can exist.</td></tr><tr><td><code>INIT</code></td><td>Address of a function to run before <code>main()</code>.</td></tr><tr><td><code>FINI</code></td><td>Address of a function to run after <code>main()</code> returns, or <code>exit()</code> is called.</td></tr><tr><td><code>INIT_ARRAY</code></td><td>Address of an array of constructor function pointers to run before <code>main()</code> (more flexible than <code>INIT</code>).</td></tr><tr><td><code>INIT_ARRAYSZ</code></td><td>Size in bytes of the <code>INIT_ARRAY</code>.</td></tr><tr><td><code>FINI_ARRAY</code></td><td>Address of an array of destructor function pointers to run on exit.</td></tr><tr><td><code>FINI_ARRAYSZ</code></td><td>Size in bytes of the <code>FINI_ARRAY</code>.</td></tr><tr><td><code>GNU_HASH</code></td><td>Address of the GNU-style hash table used for fast symbol lookup (alternative to <code>HASH</code>).</td></tr><tr><td><code>STRTAB</code></td><td>Address of the string table used for dynamic symbols (like lib names, function names).</td></tr><tr><td><code>SYMTAB</code></td><td>Address of the dynamic symbol table (function/variable names, sizes, bindings).</td></tr><tr><td><code>STRSZ</code></td><td>Size in bytes of the string table pointed to by <code>STRTAB</code>.</td></tr><tr><td><code>SYMENT</code></td><td>Size of each symbol table entry.</td></tr><tr><td><code>DEBUG</code></td><td>Reserved for debugger use; ignored at runtime.</td></tr><tr><td><code>PLTGOT</code></td><td>Address of the Global Offset Table (GOT) used for dynamic symbol resolution.</td></tr><tr><td><code>PLTRELSZ</code></td><td>Size in bytes of the <code>.rela.plt</code> section.</td></tr><tr><td><code>PLTREL</code></td><td>Type of relocation used in the PLT (<code>RELA</code> or <code>REL</code>).</td></tr><tr><td><code>JMPREL</code></td><td>Address of relocation entries for procedure linkage table (PLT) — e.g. <code>.rela.plt</code>.</td></tr><tr><td><code>RELA</code></td><td>Address of relocation entries with addends — e.g. <code>.rela.dyn</code>.</td></tr><tr><td><code>RELASZ</code></td><td>Size in bytes of the <code>.rela.dyn</code> section.</td></tr><tr><td><code>RELAENT</code></td><td>Size of each entry in <code>.rela.dyn</code>.</td></tr><tr><td><code>FLAGS_1</code></td><td>Flags providing additional behavior control to the dynamic linker (e.g. <code>DF_1_NOW</code>, <code>DF_1_GLOBAL</code>).</td></tr><tr><td><code>VERNEED</code></td><td>Address of the version dependency table (which symbol versions are needed from shared libs).</td></tr><tr><td><code>VERNEEDNUM</code></td><td>Number of entries in the version dependency table.</td></tr><tr><td><code>VERSYM</code></td><td>Address of the version symbol table — gives the version of each symbol in the symbol table.</td></tr><tr><td><code>RELACOUNT</code></td><td>Number of <code>RELA</code> relocations not part of PLT — for optimization.</td></tr><tr><td><code>NULL</code></td><td><strong>Terminator</strong> — marks the end of the dynamic section. No further entries are processed after this.</td></tr></tbody></table>

Lots of information we have no idea about. Don't stress about it. We will go through everything. Nothing would be left.



















