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

The main has the control and it now executes the following instruction:

```
1147:	e8 e4 fe ff ff       	call   1030 <puts@plt>
```

Now we are at offset `0x1030`. It resolves to this in the full disassembly.

```
0000000000001030 <puts@plt>:
  1030:	ff 25 ca 2f 00 00    	jmp    QWORD PTR [rip+0x2fca]        # 4000 <puts@GLIBC_2.2.5>
  1036:	68 00 00 00 00       	push   0x0
  103b:	e9 e0 ff ff ff       	jmp    1020 <_init+0x20>
```

* This is the PLT stub for the `puts` function.

According to the structure we have studied previously, this jump instruction should be to the corresponding global offset table.

*   We can visit `0x4000` to confirm that this is indeed true.

    ```
    0000000000003fe8 <_GLOBAL_OFFSET_TABLE_>:
        3fe8:	e0 3d                	loopne 4027 <_end+0x7>
    	...
        3ffe:	00 00                	add    BYTE PTR [rax],al
        4000:	36 10 00             	ss adc BYTE PTR [rax],al
        4003:	00 00                	add    BYTE PTR [rax],al
        4005:	00 00                	add    BYTE PTR [rax],al
    	...
    ```
* The disassembly is garbage so don't focus on that.

The question is, what does the corresponding global offset entry for a PLT entry points to?

* It points to the next instruction in the PLT stub, which is about pushing the symbol index for the `puts` function from the `.rela.plt` table to the stack.
* After the symbol index is pushed (ins 1036), the next instruction is jumping to offset 1020.

The instruction at offset 0x1020 pushes the link\_map to the stack. This includes important information for the runtime resolver function. The instruction at 0x1026 jumps to runtime resolver function, uses the link map and symbol index to find the actual address of the symbol and updates the got entry.

After this, the control is given to main again and a call to puts is successfully made.





