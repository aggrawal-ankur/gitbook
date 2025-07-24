# Procedure Linkage Table

## Introduction To Procedure Linkage Table

The Procedure Linkage Table is a section in an ELF binary used to support dynamic function calls to external (shared library) functions. It acts as an indirect jump table, allowing a program to call shared library functions whose actual memory addresses are not known until runtime, typically resolved through lazy binding.

It is a table of stubs that handle runtime linkage of procedures (functions) in a dynamically linked environment.

The global offset table stores pointers to both function symbols and global variables, but procedure linkage table is used for external functions only.

Procedure linkage table is tightly coupled with the global offset table.

## Structure of Procedure Linkage Table

```
          +------------------------------+
PLT[0] -> | jmp *GOT[LINKER_FUNC_PTR]    | ; jump to the entry in GOT which points to thedynamic linker
          | jmp RESOLVER_FUNC            | ; usually _dl_runtime_resolve()
          +------------------------------+

          +------------------------------+
PLT[1] -> | jmp *GOT[FUNC1]              | ; jump to resolved address of FUNC(1)
          | push FUNC1_INDEX             | ; index for FUNC(1) in .rela.plt
          | jmp plt[0]                   | ; fallback to resolver
          +------------------------------+

          +------------------------------+
PLT[2] -> | jmp *GOT[FUNC2]              | ; jump to resolved address of FUNC(2)
          | push FUNC2_INDEX             | ; index for FUNC(2) in .rela.plt
          | jmp plt[0]                   | ; fallback to resolver
          +------------------------------+

      ...

          +------------------------------+
PLT[N] -> | jmp *GOT[FUNCN]              | ; jump to resolved address of FUNC(N)
          | push FUNCN_INDEX             | ; index for FUNC(N) in .rela.plt
          | jmp plt[0]                   | ; fallback to resolver
          +------------------------------+
```

Clearly, it is a little chaotic to understand. We have to use global offset table along with procedure linkage table to understand how lazy binding actually works, and in that process we will also understand how PLT works.

### PLT\[0] Entry

This entry is reserved for the actual resolution purpose. `PLT[1]` to `PLT[n]` onward are the actual relocation entries requiring lazy binding.

When the `main` of our program has control, and it is executing instructions one-by-one, it eventually encounters the call the puts via plt. This can be verified from the disassembly of `main`.

```
1147:	e8 e4 fe ff ff       	call   1030 <puts@plt>
```

Since `main` has the control, the control has to be passed to dynamic linker (interpreter) program so that the runtime resolver function (`_dl_runtime_resolve()`) can be called which would eventually find the address of `puts`.

* For this to happen, we need to know where is the dynamic linker program and where is the runtime resolver function in the memory.
* And that's what the the reserved entries in the global offset table are about. The `link_map` stores information about the loaded libraries. And the other entry stores a pointer to the runtime resolver function.
* And the two entries in the the `PLT[0]` stub exactly jump to these offsets, with necessary inputs to do the required job.

### PLT\[1] to PLT\[n]

These are the actual entries asking for lazy binding.

We have only one entry.

```
Relocation section '.rela.plt' at offset 0x610 contains 1 entry:
  Offset          Info           Type           Sym. Value       Sym. Name + Addend
000000004000  000300000007  R_X86_64_JUMP_SLO  0000000000000000  puts@GLIBC_2.2.5 + 0
```

## Process









