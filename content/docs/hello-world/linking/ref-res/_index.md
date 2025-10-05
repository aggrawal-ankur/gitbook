---
id: 37c3bf4339444f10afc641a908538316
title: Resolving External References
weight: 6
---

***Originally written in July 2025.***

***Polished on 04, 05 October 2025.***

---

Functions like `printf()` and `scanf()` don't belong to us, but we use them in our source code. We use header files like stdio.h and stdlib to access them.
  - But header files are just frontend APIs which make the writing process easier.
  - When we talk about the whole infrastructure that runs C code, we can easily count hundreds of procedures and sub-routines doing the actual work.
  - In the end, an executable binary has to exist for these functions. This is where shared libraries come into picture.
  - We link our source code with these shared libraries to use those functions at runtime.

Now we have access to functions present in shared libraries. And we have to deal with one last problem. **We don't know their runtime address.**
  - The solution to this problem is a 2-step process.
  - First, we find the runtime address of the symbol. This process is called symbol resolution.
  - Second, we patch the placeholder offset with this runtime address. This process is called relocation.

## Relocation Entries

There are 100s of procedures and sub-routines doing the actual work.
  - But not all of them are available as frontend APIs. They are called internally by the frontend APIs. 
  - That's why only few symbols need relocation.

There are two relocation tables in our binary.
  - `.rela.dyn` is for symbols requiring eager binding.
  - `.rela.plt` is for symbols requiring lazy binding.

These two tables cover most of the general C binaries, but relocation tables aren't limited to them. There are special cases when a different relocation table might be used. But we need not to worry about them.

To understand their purpose, we have to understand binding.

### Binding

Now we know that multiple routines run before our program. This number is little in our binary but this can be huge in big projects. 

Take two cases.

Case1:
  - There is no way an internal routine using `printf` because it is a frontend API used to put stuff on the output stream.
  - Is it fruitful to load `printf` far before we need it? Because, first, the symbols are resolved, then they run.
  - Now increase the scale to all the functions present in a large project. This can easily become an overhead.

Case2:
  - If I decide to call a function based on a certain condition, that creates an uncertainty that whether the symbol would be used or not.
  - For ex: factorial is defined only for +ve integers. So we have to check positivity before using it.
  - If you preload it and not use it, it's a waste.

What if we can devise a process that intelligently determines when to resolve which symbol, we can balance speed and reliability. ***Binding*** is the answer.

---

Binding is the process that determines when and how external references are resolved.

There are 3 types of binding we need to study right now.
  - Load-time dynamic binding (Eager binding)
  - Lazy PLT binding
  - Static binding

Static binding is a different beast, where everything is resolved at link-time (not load-time), in the build-process only.
  - It requires no relocation/got/plt stuff. The most straightforward option.
  - But that straightforward-ness comes at a cost we will study separately later.

Eager binding resolves a symbol at load-time.
  - It ensures that any code runs safely by resolving symbols which are absolutely required.
  - This includes all non-PLT relocations.

Lazy binding defers symbol resolution until the symbol is not called.

CONTINUE FROM HERE

### Addend

There can be cases where the symbol is a specific part of a complex structure, a blob or a function.
  - Symbol resolution calculates only the runtime base address of the symbol. It doesn't account for specifics.
  - For basic symbols (variables/functions), this is not a problem. But for complex scenarios, this is a problem.

To solve this problem, we need to add a constant value to the runtime base address of a symbol to obtain the final runtime address. This constant value is called **addend**.

For simple symbols, addend is usually 0, which is reflected in the relocation tables above as well.

When this addend is stored in the relocation entry, the dynamic linker computes the final value by combining the base address of the symbol with addend. Such relocation is called "relocation with addend, or RELA".

When this addend is embedded in the instruction/data itself and the relocation entry only tells the dynamic linker where to patch, such a relocation is called "relocation without addend, or REL".
  - This one doesn't make sense right now so don't scratch your head.
  - There is no REL entry in our binary. But we will cover this later for sure.

## Symbol Table

A symbol table is a metadata table for symbols. There are two symbol tables in our binary: `.symtab` and `.dynsym`.

```bash
Symbol table '.dynsym' contains 7 entries:
   Num:     Value          Size  Type     Bind    Visibility   Ndx   Name
     0:  0000000000000000    0   NOTYPE   LOCAL   DEFAULT      UND   
     1:  0000000000000000    0   FUNC     GLOBAL  DEFAULT      UND   _[...]@GLIBC_2.34 (2)
     2:  0000000000000000    0   NOTYPE   WEAK    DEFAULT      UND   _ITM_deregisterT[...]
     3:  0000000000000000    0   FUNC     GLOBAL  DEFAULT      UND   puts@GLIBC_2.2.5 (3)
     4:  0000000000000000    0   NOTYPE   WEAK    DEFAULT      UND   __gmon_start__
     5:  0000000000000000    0   NOTYPE   WEAK    DEFAULT      UND   _ITM_registerTMC[...]
     6:  0000000000000000    0   FUNC     WEAK    DEFAULT      UND   [...]@GLIBC_2.2.5 (3)

Symbol table '.symtab' contains 36 entries:
   Num:     Value          Size  Type     Bind    Vis       Ndx   Name
     0:  0000000000000000    0   NOTYPE   LOCAL   DEFAULT   UND   
     1:  0000000000000000    0   FILE     LOCAL   DEFAULT   ABS   Scrt1.o
     2:  00000000000020ec   32   OBJECT   LOCAL   DEFAULT    19   __abi_tag
     3:  0000000000000000    0   FILE     LOCAL   DEFAULT   ABS   crtstuff.c
     4:  0000000000001080    0   FUNC     LOCAL   DEFAULT    14   deregister_tm_clones
     5:  00000000000010b0    0   FUNC     LOCAL   DEFAULT    14   register_tm_clones
     6:  00000000000010f0    0   FUNC     LOCAL   DEFAULT    14   __do_global_dtors_aux
     7:  0000000000004018    1   OBJECT   LOCAL   DEFAULT    26   completed.0
     8:  0000000000003dd8    0   OBJECT   LOCAL   DEFAULT    21   __do_global_dtor[...]
     9:  0000000000001130    0   FUNC     LOCAL   DEFAULT    14   frame_dummy
    10:  0000000000003dd0    0   OBJECT   LOCAL   DEFAULT    20   __frame_dummy_in[...]
    11:  0000000000000000    0   FILE     LOCAL   DEFAULT   ABS   hello.c
    12:  0000000000000000    0   FILE     LOCAL   DEFAULT   ABS   crtstuff.c
    13:  00000000000020e8    0   OBJECT   LOCAL   DEFAULT    18   __FRAME_END__
    14:  0000000000000000    0   FILE     LOCAL   DEFAULT   ABS   
    15:  0000000000003de0    0   OBJECT   LOCAL   DEFAULT    22   _DYNAMIC
    16:  0000000000002014    0   NOTYPE   LOCAL   DEFAULT    17   __GNU_EH_FRAME_HDR
    17:  0000000000003fe8    0   OBJECT   LOCAL   DEFAULT    24   _GLOBAL_OFFSET_TABLE_
    18:  0000000000000000    0   FUNC     GLOBAL  DEFAULT   UND   __libc_start_mai[...]
    19:  0000000000000000    0   NOTYPE   WEAK    DEFAULT   UND   _ITM_deregisterT[...]
    20:  0000000000004008    0   NOTYPE   WEAK    DEFAULT    25   data_start
    21:  0000000000000000    0   FUNC     GLOBAL  DEFAULT   UND   puts@GLIBC_2.2.5
    22:  0000000000004018    0   NOTYPE   GLOBAL  DEFAULT    25   _edata
    23:  0000000000001154    0   FUNC     GLOBAL  HIDDEN     15   _fini
    24:  0000000000004008    0   NOTYPE   GLOBAL  DEFAULT    25   __data_start
    25:  0000000000000000    0   NOTYPE   WEAK    DEFAULT   UND   __gmon_start__
    26:  0000000000004010    0   OBJECT   GLOBAL  HIDDEN     25   __dso_handle
    27:  0000000000002000    4   OBJECT   GLOBAL  DEFAULT    16   _IO_stdin_used
    28:  0000000000004020    0   NOTYPE   GLOBAL  DEFAULT    26   _end
    29:  0000000000001050   34   FUNC     GLOBAL  DEFAULT    14   _start
    30:  0000000000004018    0   NOTYPE   GLOBAL  DEFAULT    26   __bss_start
    31:  0000000000001139   26   FUNC     GLOBAL  DEFAULT    14   main
    32:  0000000000004018    0   OBJECT   GLOBAL  HIDDEN     25   __TMC_END__
    33:  0000000000000000    0   NOTYPE   WEAK    DEFAULT   UND   _ITM_registerTMC[...]
    34:  0000000000000000    0   FUNC     WEAK    DEFAULT   UND   __cxa_finalize@G[...]
    35:  0000000000001000    0   FUNC     GLOBAL  HIDDEN     11   _init
```

| Attribute  | Description |
| :--------  | :---------- |
| Num   | Index in the symbol table. |
| Value | Symbol's value (usually an address) |
| Size  | Size of the symbol in bytes |
| Type  | The kind of symbol (FUNC, OBJECT, SECTION, etc.) |
| Bind  | Symbol binding. How it is linked. |
| | LOCAL: Visible only within the object. |
| | GLOBAL: Externally visible and usable by others. |
| | WEAK: Like global but with lower priority. |
| Visibility/Vis | Symbol visibility. |
| | DEFAULT: Visible to all. |
| | HIDDEN: Internal, not exported. |
| | PROTECTED: Visible, but not preemptable. |
| Ndx (Section index) | The section the symbol is defined in. |
| | ABS: Absolute symbol, not tied to any section. |
| | INT_VALUE: The section it is defined in. |
| | UND: Undefined, needs relocation. |
| | COMMON: Uninitialized global symbol. |
| Name | Name of the symbol; An offset in the corresponding string table. |

### Purpose

| Table   | Purpose |
| :----   | :------ |
| .symtab | Full symbol table for internal use by the linker (or in debugging). Not needed at runtime. |
| .dynsym | Dynamic symbol table used by the dynamic linker at runtime (for symbols requiring relocation). |

### String Table

A string table is a central name registry.

| Symbol Table | Name Registry |
| :------ | :------ |
| .dynsym | .dynstr |
| .symtab | .symtab |