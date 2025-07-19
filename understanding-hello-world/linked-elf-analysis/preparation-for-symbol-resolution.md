# Preparation For Symbol Resolution

## Premise

We are using `printf()` to print `Hello, World!\n` in the output screen. But where is `printf()`?

I have not written it. So where is it coming from? `glibc`? Yes.

What is `glibc`? A shared library? Yes.

Great. `printf()` is coming from `glibc`. But our source code and the `glibc` are two distinct things. How will my source code know where is `glibc` and where is `printf()` in it?

We also know that our source code is just a tiny part of the infrastructure that runs it. I didn't write that infrastructure. That infra would also require various functions and other things. Where are those things coming from?

The answer is symbol resolution. And we are going to discuss the same in this article.

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

<table><thead><tr><th width="138">Attribute</th><th width="277">Description</th><th>Extra Information</th></tr></thead><tbody><tr><td><code>Num</code></td><td>Symbol number (index in the symbol table).</td><td></td></tr><tr><td><code>Value</code></td><td>Symbol's value (usually an address or offset, depending on section context)</td><td></td></tr><tr><td><code>Size</code></td><td>Size of the symbol in bytes (zero for undefined size or functions sometimes)</td><td></td></tr><tr><td><code>Type</code></td><td>What kind of symbol it is (<code>FUNC</code>, <code>OBJECT</code>, <code>SECTION</code>, etc.)</td><td></td></tr><tr><td><code>Bind</code></td><td>Symbol binding: how it is linked (<code>LOCAL</code>, <code>GLOBAL</code>, <code>WEAK</code>, etc.)</td><td><code>LOCAL</code>: Visible only within this object.<br><code>GLOBAL</code>: Externally visible and usable by others.<br><code>WEAK</code>: Like global but with lower priority.</td></tr><tr><td><code>Visibility</code></td><td>Symbol visibility: how it is seen across objects (<code>DEFAULT</code>, <code>HIDDEN</code>, etc.)</td><td><code>DEFAULT</code>: Visible to all.<br><code>HIDDEN</code>: Internal, not exported.<br><code>PROTECTED</code>: Visible, but not preemptable.</td></tr><tr><td><code>Ndx</code></td><td>Section index: which section the symbol is defined in (<code>UND</code>, number, etc.)</td><td><code>UND</code>: Undefined, needs resolution.<br><code>INT_VAL</code>: The section it is defined in.<br><code>ABS</code>: Absolute symbol, not tied to any section.<br><code>COMMON</code>: Uninitialized global.</td></tr><tr><td><code>Name</code></td><td>The symbol's name (looked up via the string table)</td><td></td></tr></tbody></table>

### What are these two tables used for?

<table><thead><tr><th width="116">Table</th><th width="540">Purpose</th><th>In short</th></tr></thead><tbody><tr><td><code>.symtab</code></td><td>Full symbol table for internal use by the linker (includes all symbols: static, local, global). Not needed at runtime.</td><td>Link-time</td></tr><tr><td><code>.dynsym</code></td><td>Minimal symbol table used by the dynamic linker at runtime (includes only dynamic/global symbols needed for relocation or symbol resolution).</td><td>Run-time</td></tr></tbody></table>

### String Table

String table is the general table which serves as the central table for symbol names, just like we talked about the section header string table.

To access it, run

```bash
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

## Relocation Entries

Relocations are instructions for the linker/loader program (`ld-linux.so`).

* In simple words, a relocation entry asks to replace the mentioned placeholder offset with the real address or offset for this symbol.

Primarily, there are two kinds of relocation entries.

* Relocation with addend, `RELA`.
* Relocation without addend, `REL`.

An addend is a constant value added to the symbol's address during relocation.

* When this constant is stored in the relocation entry itself, we call it `RELA`, which means, "Relocation with Addend".
* When this constant is embedded in the section being relocated, we call it `REL`, which means, "Relocation without Addend".

There are two relocation tables in our binary, `.rela.dyn` and `.rela.plt`.

* `.rela.dyn` is for general data/function pointer relocations.
* `.rela.plt` is for function calls through the PLT, typically used for lazy binding.

These are the relocation entries in our binary.

```
Relocation section '.rela.dyn' at offset 0x550 contains 8 entries:
  Offset          Info            Type            Sym. Value     Sym. Name + Addend
000000003dd0  000000000008  R_X86_64_RELATIVE                      1130
000000003dd8  000000000008  R_X86_64_RELATIVE                      10f0
000000004010  000000000008  R_X86_64_RELATIVE                      4010
000000003fc0  000100000006  R_X86_64_GLOB_DAT  0000000000000000  __libc_start_main@GLIBC_2.34 + 0
000000003fc8  000200000006  R_X86_64_GLOB_DAT  0000000000000000  _ITM_deregisterTM[...] + 0
000000003fd0  000400000006  R_X86_64_GLOB_DAT  0000000000000000  __gmon_start__ + 0
000000003fd8  000500000006  R_X86_64_GLOB_DAT  0000000000000000  _ITM_registerTMCl[...] + 0
000000003fe0  000600000006  R_X86_64_GLOB_DAT  0000000000000000  __cxa_finalize@GLIBC_2.2.5 + 0

Relocation section '.rela.plt' at offset 0x610 contains 1 entry:
  Offset          Info           Type           Sym. Value       Sym. Name + Addend
000000004000  000300000007  R_X86_64_JUMP_SLO  0000000000000000  puts@GLIBC_2.2.5 + 0
```

### Understanding The Attributes

<table><thead><tr><th width="148">Attribute</th><th>Description</th></tr></thead><tbody><tr><td><code>Offset</code></td><td>Location in the section where the relocation has to be applied.</td></tr><tr><td><code>Info</code></td><td>Encodes the relocation type and symbol index (e.g., high bits: symbol, low bits: type).</td></tr><tr><td><code>Type</code></td><td>Relocation type, how to apply the relocation.</td></tr><tr><td><code>Sym. Value</code></td><td>The value of the referenced symbol (from the symbol table), if applicable</td></tr><tr><td><code>Sym. Name</code></td><td>Name of the symbol being relocated against (can be empty for some types like <code>RELATIVE</code>)</td></tr><tr><td><code>Addend</code></td><td>Constant value added to the relocation calculation (explicit in <code>.rela.*</code>)</td></tr></tbody></table>

Addend is probably the only foreign term here. Next we are going to understand that. But before that we need to clear a small concept.
