# Procedure Linkage Table

## Problem Statement

Now we are inside the `main` symbol and our code i executing. The program reached the instruction where a call to puts is made. Just think about how it would get resolved?

* Right now, the control is in the hands of `main`. And `puts` is hiding somewhere in the shared libraries.
* It is essential that the interpreter program has the control, so that we can use the runtime resolver function to find `puts`. Right? Where we would get it?

The global offset table is designed to contain offsets only. How will you encapsulate the logic for finding `puts` or any function that needs lazy binding?

* You may say that the GOT entry can point to the interpreter program.
* In that case, how will you jump to the runtime resolver function? How will you tell the runtime resolver function which symbol is needed to be found?
* A single entry in the global offset table can't afford to do all of this.

So, whats the solution, then?

## Introduction To Procedure Linkage Table

The Procedure Linkage Table is a section in an ELF binary used to support dynamic function calls to external (shared library) functions. It acts as an indirect jump table, allowing a program to call shared library functions whose actual memory addresses are not known until runtime, typically resolved through lazy binding.

The global offset table stores pointers to both function symbols and global variables, but procedure linkage table is used for external functions only.

Procedure linkage table is tightly coupled with the global offset table.

### Why it is called procedure linkage table? Is there any meaning?

Just like the global offset table is a table where each entry is designed to be an offset to the actual runtime address of a symbol, the procedure linkage table is also meaningful in its name.

_It is a table of stubs that handle runtime linkage of procedures (functions) in a dynamically linked environment._

## Structure of Procedure Linkage Table

### First of all, what is a stub?

I have understood stub as _a piece of instructions, consistent across all entries._

***

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

`PLT[0]` is reserved for providing the base for relocation. `PLT[1 to n]` onward are the actual relocation entries requiring lazy binding.

## Understanding \`puts\` Relocation

When the `main` has control, and it is executing instructions one-by-one, it eventually encounters the call to puts via plt. This can be verified from the disassembly of `main`.

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

## Possible Look Of Our \`.got.plt\` And \`.plt\` Section

\[ERASER.IO DRAWING]

## Final Structure Of The Global Offset Table

```
----------------------------------------------------------------------------------------
| // Eager Binding Division -> .got at offset 0x0000 (RELA) (.rela.dyn)                |
| ----------    --------------------------    ----------    -------------------------- |
| | GOT[0] | -> | *(func/symb 1)         | -> | 0x0000 | -> | Actual Runtime Address | |
| ----------    --------------------------    ----------    -------------------------- |
| | GOT[1] | -> | *(func/symb 2)         | -> | 0x0008 | -> | Actual Runtime Address | |
| ----------    --------------------------    ----------    -------------------------- |
| | GOT[2] | -> | *(func/symb 3)         | -> | 0x0010 | -> | Actual Runtime Address | |
| ----------    --------------------------    ----------    -------------------------- |
| | GOT[3] | -> | *(func/symb 4)         | -> | 0x0018 | -> | Actual Runtime Address | |
| ----------    --------------------------    ----------    -------------------------- |
| | GOT[4] | -> | *(func/symb 5)         | -> | 0x0020 | -> | Actual Runtime Address | |
| ----------    --------------------------    ----------    -------------------------- |
| ....                                                                                 |
| ....                                                                                 |
| ----------    --------------------------    ----------    -------------------------- |
| | GOT[N] | -> | *(func/symb N)         | -> | 0x.... | -> | Actual Runtime Address | |
| ----------    --------------------------    ----------    -------------------------- |
|--------------------------------------------------------------------------------------|
| // Lazy Binding Division -> .got.plt at offset 0x0028 (JMPREL) (.rela.plt)           |
| ----------    --------------------------    ----------    -------------------------- |
| | GOT[0] | -> | *(.dynamic)            | -> | 0x0028 | -> | Actual Runtime Address | | <- Reserved for enabling lazy binding 
| ----------    --------------------------    ----------    -------------------------- |
| | GOT[1] | -> | *(link_map)            | -> | 0x0030 | -> | Actual Runtime Address | | <- Reserved for enabling lazy binding 
| ----------    --------------------------    ----------    -------------------------- |
| | GOT[2] | -> | *(_dl_runtime_resolve) | -> | 0x0038 | -> | Actual Runtime Address | | <- Reserved for enabling lazy binding 
| ----------    --------------------------    ----------    -------------------------- |
| | GOT[3] | -> | *(PLT stub for func 1) | -> | 0x0040 | -> | Actual Runtime Address | |
| ----------    --------------------------    ----------    -------------------------- |
| | GOT[4] | -> | *(PLT stub for func 2) | -> | 0x0048 | -> | Actual Runtime Address | |
| ----------    --------------------------    ----------    -------------------------- |
| ....                                                                                 |
| ....                                                                                 |
| ----------    --------------------------    ----------    -------------------------- |
| | GOT[M] | -> | *(PLT stub for func M) | -> | 0x.... | -> | Actual Runtime Address | |
| ----------    --------------------------    ----------    -------------------------- |
----------------------------------------------------------------------------------------
```
