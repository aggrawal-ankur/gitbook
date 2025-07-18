# Step 4: Symbols And Relocations

## Premise

We are using `printf()` to print `Hello, World!\n` in the output screen. But where is `printf()`?

I have not written it. So where is it coming from? `glibc`? Yes.

What is `glibc`? A shared library? Yes.

Great. `printf()` is coming from `glibc`. But our source code and the `glibc` are two distinct things. How will my source code know where is `glibc` and where is `printf()` in it?

We also know that our source code is just a tiny part of the infrastructure that runs it. I didn't write that infrastructure. That infra would also require various functions and other things. Where are those things coming from?

The answer is symbol relocation. And we are going to discuss the same in this article.

## Setting Up The Grounds

From assembly, we know that a lot of things are just symbols of different kinds.

The instruction `call puts@PLT` is a call to a function symbol `puts` via the procedure linkage table or `PLT`.

Often, these symbols are located in code written beyond the current file or something entirely written by a different person. To use these symbols, there has to be a way through which these are made available to our binary and our binary knows where they are.

**Symbols** are the entities which are required to be resolved. **Relocation** is the process that resolves the final runtime address of these symbols.

## What is required for relocation?

1. What are all the symbols that require relocation? These are those symbols whose runtime address is not known.
2. Relocation entries which define the metadata about these symbols.
3. A process to manage symbol resolution.

## Symbol Tables

A symbol table is a metadata table about symbols. That's it.

There are two symbol tables in our binary. These are `.symtab` and `.dynsym`.

```
Symbol table '.dynsym' contains 7 entries:
   Num:     Value          Size  Type     Bind    Visibility   Ndx   Name
     0:  0000000000000000     0  NOTYPE   LOCAL   DEFAULT      UND   
     1:  0000000000000000     0  FUNC     GLOBAL  DEFAULT      UND   _[...]@GLIBC_2.34 (2)
     2:  0000000000000000     0  NOTYPE   WEAK    DEFAULT      UND   _ITM_deregisterT[...]
     3:  0000000000000000     0  FUNC     GLOBAL  DEFAULT      UND   puts@GLIBC_2.2.5 (3)
     4:  0000000000000000     0  NOTYPE   WEAK    DEFAULT      UND   __gmon_start__
     5:  0000000000000000     0  NOTYPE   WEAK    DEFAULT      UND   _ITM_registerTMC[...]
     6:  0000000000000000     0  FUNC     WEAK    DEFAULT      UND   [...]@GLIBC_2.2.5 (3)

Symbol table '.symtab' contains 36 entries:
   Num:     Value          Size  Type    Bind   Vis       Ndx   Name
     0:  0000000000000000     0  NOTYPE  LOCAL  DEFAULT   UND   
     1:  0000000000000000     0  FILE    LOCAL  DEFAULT   ABS   Scrt1.o
     2:  00000000000020ec    32  OBJECT  LOCAL  DEFAULT    19   __abi_tag
     3:  0000000000000000     0  FILE    LOCAL  DEFAULT   ABS   crtstuff.c
     4:  0000000000001080     0  FUNC    LOCAL  DEFAULT    14   deregister_tm_clones
     5:  00000000000010b0     0  FUNC    LOCAL  DEFAULT    14   register_tm_clones
     6:  00000000000010f0     0  FUNC    LOCAL  DEFAULT    14   __do_global_dtors_aux
     7:  0000000000004018     1  OBJECT  LOCAL  DEFAULT    26   completed.0
     8:  0000000000003dd8     0  OBJECT  LOCAL  DEFAULT    21   __do_global_dtor[...]
     9:  0000000000001130     0  FUNC    LOCAL  DEFAULT    14   frame_dummy
    10:  0000000000003dd0     0  OBJECT  LOCAL  DEFAULT    20   __frame_dummy_in[...]
    11:  0000000000000000     0  FILE    LOCAL  DEFAULT   ABS   hello.c
    12:  0000000000000000     0  FILE    LOCAL  DEFAULT   ABS   crtstuff.c
    13:  00000000000020e8     0  OBJECT  LOCAL  DEFAULT    18   __FRAME_END__
    14:  0000000000000000     0  FILE    LOCAL  DEFAULT   ABS   
    15:  0000000000003de0     0  OBJECT  LOCAL  DEFAULT    22   _DYNAMIC
    16:  0000000000002014     0  NOTYPE  LOCAL  DEFAULT    17   __GNU_EH_FRAME_HDR
    17:  0000000000003fe8     0  OBJECT  LOCAL  DEFAULT    24   _GLOBAL_OFFSET_TABLE_
    18:  0000000000000000     0  FUNC    GLOBAL DEFAULT   UND   __libc_start_mai[...]
    19:  0000000000000000     0  NOTYPE  WEAK   DEFAULT   UND   _ITM_deregisterT[...]
    20:  0000000000004008     0  NOTYPE  WEAK   DEFAULT    25   data_start
    21:  0000000000000000     0  FUNC    GLOBAL DEFAULT   UND   puts@GLIBC_2.2.5
    22:  0000000000004018     0  NOTYPE  GLOBAL DEFAULT    25   _edata
    23:  0000000000001154     0  FUNC    GLOBAL HIDDEN     15   _fini
    24:  0000000000004008     0  NOTYPE  GLOBAL DEFAULT    25   __data_start
    25:  0000000000000000     0  NOTYPE  WEAK   DEFAULT   UND   __gmon_start__
    26:  0000000000004010     0  OBJECT  GLOBAL HIDDEN     25   __dso_handle
    27:  0000000000002000     4  OBJECT  GLOBAL DEFAULT    16   _IO_stdin_used
    28:  0000000000004020     0  NOTYPE  GLOBAL DEFAULT    26   _end
    29:  0000000000001050    34  FUNC    GLOBAL DEFAULT    14   _start
    30:  0000000000004018     0  NOTYPE  GLOBAL DEFAULT    26   __bss_start
    31:  0000000000001139    26  FUNC    GLOBAL DEFAULT    14   main
    32:  0000000000004018     0  OBJECT  GLOBAL HIDDEN     25   __TMC_END__
    33:  0000000000000000     0  NOTYPE  WEAK   DEFAULT   UND   _ITM_registerTMC[...]
    34:  0000000000000000     0  FUNC    WEAK   DEFAULT   UND   __cxa_finalize@G[...]
    35:  0000000000001000     0  FUNC    GLOBAL HIDDEN     11   _init
```

### Understanding The Attributes

<table><thead><tr><th width="120">Attribute</th><th>Description</th></tr></thead><tbody><tr><td><strong>Num</strong></td><td>Symbol number (index in the symbol table)</td></tr><tr><td><strong>Value</strong></td><td>Symbol's value (usually an address or offset, depending on section context)</td></tr><tr><td><strong>Size</strong></td><td>Size of the symbol in bytes (zero for undefined size or functions sometimes)</td></tr><tr><td><strong>Type</strong></td><td>What kind of symbol it is (<code>FUNC</code>, <code>OBJECT</code>, <code>SECTION</code>, etc.)</td></tr><tr><td><strong>Bind</strong></td><td>Symbol binding: how it is linked (<code>LOCAL</code>, <code>GLOBAL</code>, <code>WEAK</code>, etc.)</td></tr><tr><td><strong>Visibility</strong></td><td>Symbol visibility: how it is seen across objects (<code>DEFAULT</code>, <code>HIDDEN</code>, etc.)</td></tr><tr><td><strong>Ndx</strong></td><td>Section index: which section the symbol is defined in (<code>UND</code>, number, etc.)</td></tr><tr><td><strong>Name</strong></td><td>The symbol's name (looked up via the string table)</td></tr></tbody></table>

### What are these two tables used for?

<table><thead><tr><th width="116">Table</th><th>Purpose</th></tr></thead><tbody><tr><td><code>.symtab</code></td><td>Full symbol table for internal use by the linker (includes all symbols: static, local, global). Not needed at runtime.</td></tr><tr><td><code>.dynsym</code></td><td>Minimal symbol table used by the dynamic linker at runtime (includes only dynamic/global symbols needed for relocation or symbol resolution).</td></tr></tbody></table>

In short:

* `.symtab` is for **link-time**.
* `.dynsym` is for **run-time**.

### String Table

String table is the general table which serves as the central table for symbol names, just like we talked about the section header string table.

To access it, run

```
$ readelf ./linked_elf -p .strtab

String dump of section '.strtab':
  [     1]  Scrt1.o
  [     9]  __abi_tag
  [    13]  crtstuff.c
  [    1e]  deregister_tm_clones
  [    33]  __do_global_dtors_aux
  [    49]  completed.0
  [    55]  __do_global_dtors_aux_fini_array_entry
  [    7c]  frame_dummy
  [    88]  __frame_dummy_init_array_entry
  [    a7]  hello.c
  [    af]  __FRAME_END__
  [    bd]  _DYNAMIC
  [    c6]  __GNU_EH_FRAME_HDR
  [    d9]  _GLOBAL_OFFSET_TABLE_
  [    ef]  __libc_start_main@GLIBC_2.34
  [   10c]  _ITM_deregisterTMCloneTable
  [   128]  puts@GLIBC_2.2.5
  [   139]  _edata
  [   140]  _fini
  [   146]  __data_start
  [   153]  __gmon_start__
  [   162]  __dso_handle
  [   16f]  _IO_stdin_used
  [   17e]  _end
  [   183]  __bss_start
  [   18f]  main
  [   194]  __TMC_END__
  [   1a0]  _ITM_registerTMCloneTable
  [   1ba]  __cxa_finalize@GLIBC_2.2.5
  [   1d5]  _init
```











