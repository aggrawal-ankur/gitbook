---
id: 85fa67f76e174da39fbde619a1a87e85
title: Global Offset Table
weight: 10
---

So far, we know that when we are talking about relocation, we are updating a placeholder value at an offset in the loaded segments by the actual runtime address of the symbol.

But, there is a problem. To update means to write. To write something, you need write permission, correct? Is the `.text` section writable? Or, should it be writable?

See, the symbols we have resolved so far, like the `__libc_start_main` function symbol, these are called by the `_start` symbol. And they are a part of the `.text` section. We know that `.text` is not limited to our source code only. But, if the `.text` section is writable, doesn't that pose a security risk?

First of all, is the `.text` section writable? **No**.

How to find whether a section is writable or not? **Check the \`Flags\` attribute in the section headers table**.

* `[14] .text PROGBITS 0000000000001050 00001050 0000000000000103 0000000000000000 AX 0 0 16`&#x20;
* The flags are `AX` here, which means `allocate` and `execute`.
* This section is clearly not writable.
* Also, the segment it belongs to, which is the 2nd `LOAD` segment in the program headers table (checkout section to segment mapping just below the program headers table), that is also not writable. `LOAD 0x0000000000001000 0x0000000000001000 0x0000000000001000 0x000000000000015d 0x000000000000015d R E 0x1000`&#x20;
* It says `RE`, which means, `read-only` and `executable`.

Second, should a section like `.text` be writable?

* The obvious answer would be **NO.** That poses a security threat. It shouldn't be writable at runtime.

Then where is relocation happening? Where we are patching the **actual runtime address**?

*   Take this entry&#x20;

    ```
    000000003fc0  000100000006  R_X86_64_GLOB_DAT  0000000000000000  __libc_start_main@GLIBC_2.34 + 0
    ```
* The offset is `0x3fc0`. The section it belongs to is `.got` . _The first shock._
* The segment `.got` section belongs to is the 4th `LOAD` segment.
*   Checkout the properties for this segment.&#x20;

    ```
    LOAD           0x0000000000002dd0  0x0000000000003dd0  0x0000000000003dd0   0x0000000000000248   0x0000000000000250  RW     0x1000
    ```
* `R W`? It is readable and writable. _The second shock._

Now we have to take help from the **full disassembly.**

* Have a look at the `.text` section, line 341 on wards.
*   ```
    106b:	ff 15 4f 2f 00 00    	call   QWORD PTR [rip+0x2f4f]        # 3fc0 <__libc_start_main@GLIBC_2.34>
    ```

    The above instruction is calling that `libc` function. In the comment, we can see that it resolves to a location `0x3fc0`. Lets visit that.
* I suggest you to use _VS Code's Search_ functionality for this. Otherwise, I am already putting the lines numbers here.
*   Offset `0x3fc0` is found at line 764. And what it points to? `.got`. And guess what, this offset matches the one in the relocation table.&#x20;

    ```
    Disassembly of section .got:

    0000000000003fc0 <.got>:
    	...
    ```
* The rest of the functions in the `.rela.dyn` table have the same story. But, here is the twist and it can only be found by people who have not lost their sanity so far. Offsets `0x3fc8 0x3fd0 3fd8 3fe0` are nowhere to be found in the `.got` section. Just a call in their respective sections but no entry in `.got`.
* If you have found that, here is the answer. Global offset table is a runtime thing. It is meant to be filled dynamically, which is why no placeholder offsets are present in the `.got` disassembly as it is meaningless. We can also notice that the only sections which have got placeholder addresses are the ones which are `read-only`, and `.got` is `writable`.

We had a look at the disassembly. Can you infer anything from it? Why is it like this?

* The `.text` section is not writable. So, it points to entries in a section which is writable.
* The section which is writable is responsible for providing the real runtime address of the symbol.
* The `.text` section calls the symbol indirectly via this entry.

That's how relocations are carried out.

Enough building hype. Lets introduce global offset table now.

## Introduction to global offset table

The Global Offset Table (GOT) is a table in an ELF binary used at runtime to hold the absolute addresses of global variables and functions, allowing for position-independent code (PIC) by deferring the resolution of symbol addresses until execution.

Each entry in this table is an address. When it is created, it is a placeholder address, later, when it is resolved, it becomes the actual runtime address of that symbol.

The one thing that makes global offset table and procedure linkage table intimidating is the absence of the ability to visualize it. It is simple to say that **it is just a pointer table** but **how does it really look like?** That changes the game.

## Structure of GOT

Global offset table is logically divided into two parts. But it is one entity at the lowest level.

We are building the binary with default options, i.e&#x20;

```bash
gcc hello.c -o hello_elf
```

Default options use eager binding for startup functions and lazy binding for source code functions. And the distinction in global offset table is based on this binding principle only.

The global offset table starts from the eager binding section. This section is very simple as there is no requirement for anything extra. So, it is all offset entries.

When the eager binding section ends, lazy binding section starts. And here we need certain entries before the actual relocation entries using PLT can come. After those entries, regular relocation entries start.

The best we can do to actually visualize how the global offset table looks like is to see the one for our binary. Since it is a runtime thing, we can't actually see it right now, as we are doing static analysis. But that should not hinder our understanding, right?

What we are going to do is, we are going to utilize the full disassembly of the `.got` section, relocation tables along with the theory to form a structure. By the way, we will verify it later when we do the dynamic analysis.

## Finding the structure of global offset table

### Supplies

Relocation entries

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

The disassembly of the `_start` symbol to find where is `__libc_start_main` coming from.

```
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
```

Global offset table section

```
Disassembly of section .got:

0000000000003fc0 <.got>:
	...

Disassembly of section .got.plt:

0000000000003fe8 <_GLOBAL_OFFSET_TABLE_>:
    3fe8:	e0 3d                	loopne 4027 <_end+0x7>
	...
    3ffe:	00 00                	add    BYTE PTR [rax],al
    4000:	36 10 00             	ss adc BYTE PTR [rax],al
    4003:	00 00                	add    BYTE PTR [rax],al
    4005:	00 00                	add    BYTE PTR [rax],al
	...
```

### Lets dive in!

We are going to start with this relocation entry.

```
000000003fc0  000100000006  R_X86_64_GLOB_DAT  0000000000000000  __libc_start_main@GLIBC_2.34 + 0
```

* The offset is `0x3fc0`. If we locate it in the full disassembly, we can find that it points to the global offset table itself.
*   If we go to the disassembly of the `_start` symbol, we can find this instruction telling that _the call to this function symbol points to this offset in the disassembly._ And the offset is again `0x3fc0`.

    ```
    106b:	ff 15 4f 2f 00 00    	call   QWORD PTR [rip+0x2f4f]        # 3fc0 <__libc_start_main@GLIBC_2.34>
    ```

This means that the first entry in the global offset table is allocated to `__libc_start_main` symbol.

And it should not be hard to think that the rest of the entries in the `.rela.dyn` table follows the same trend. Just because it is a runtime table, those entries don't exist.

We know that, each address in 64-bit architecture is 8-byte long. That means, addresses should be separated by 8 units.&#x20;

With that in mind, the eager binding part of the global offset table should look like this:

```
GOT[0] -> *(__libc_start_main) -> 0x3fc0 (placeholder) -> [Actual Runtime Address]
GOT[1] -> *(_ITM_deregisterTM) -> 0x3fc8 (placeholder) -> [Actual Runtime Address]
GOT[2] -> *(__gmon_start__)    -> 0x3fd0 (placeholder) -> [Actual Runtime Address]
GOT[3] -> *(_ITM_registerTMCl) -> 0x3fd8 (placeholder) -> [Actual Runtime Address]
GOT[4] -> *(__cxa_finalize)    -> 0x3fe0 (placeholder) -> [Actual Runtime Address]
```

Now comes the lazy binding part.

* To do lazy binding, you need to know certain things. Since we have not touched on lazy binding yet, we will keep it simple.
* There are 3 entries required to be reserved for lazy binding in the global offset table. These are offsets to `.dynamic` segment, link\_map, and the runtime resolver function.
* Link map is a data structure which tracks all the loaded objects and runtime resolver function is the function that find those symbols in the loaded shared objects and resolve their runtime address.

Since the last entry was at `0x3fe0` offset, the next entry should start at `0x3fe8`, right? Have a look at the disassembly for `.got.plt` section. Just look at the offset, the disassembly is garbage.

That means, the lazy binding section in the global offset table should look like this:

```
GOT[5] -> *(.dynamic)         -> 0x3fe8 -> [Actual Runtime Address]
GOT[6] -> *(link_map)         -> 0x3ff0 -> [Actual Runtime Address]
GOT[7] -> *(runtime resolver) -> 0x3ff8 -> [Actual Runtime Address]
GOT[8] -> *(puts)             -> 0x4000 -> [Actual Runtime Address]
```

Combining both of them, the final structure should emerge something like this:

```
----------    ------------------------    ----------    --------------------------
| GOT[0] | -> | *(__libc_start_main) | -> | 0x3fc0 | -> | Actual Runtime Address |
----------    ------------------------    ----------    --------------------------
| GOT[1] | -> | *(_ITM_deregisterTM) | -> | 0x3fc8 | -> | Actual Runtime Address |
----------    ------------------------    ----------    --------------------------
| GOT[2] | -> | *(__gmon_start__)    | -> | 0x3fd0 | -> | Actual Runtime Address |
----------    ------------------------    ----------    --------------------------
| GOT[3] | -> | *(_ITM_registerTMCl) | -> | 0x3fd8 | -> | Actual Runtime Address |
----------    ------------------------    ----------    --------------------------
| GOT[4] | -> | *(__cxa_finalize)    | -> | 0x3fe0 | -> | Actual Runtime Address |
----------    ------------------------    ----------    --------------------------
| GOT[5] | -> | *(.dynamic)          | -> | 0x3fe8 | -> | Actual Runtime Address |
----------    ------------------------    ----------    --------------------------
| GOT[6] | -> | *(link_map)          | -> | 0x3ff0 | -> | Actual Runtime Address |
----------    ------------------------    ----------    --------------------------
| GOT[7] | -> | *(runtime)           | -> | 0x3ff8 | -> | Actual Runtime Address |
----------    ------------------------    ----------    --------------------------
| GOT[8] | -> | *(puts)              | -> | 0x4000 | -> | Actual Runtime Address |
----------    ------------------------    ----------    --------------------------
```

That's it.

### A Generalized Structure

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
| :--- |
| // Lazy Binding Division -> .got.plt at offset 0x0028 (JMPREL) (.rela.plt)           |
| ----------    --------------------------    ----------    -------------------------- |
| | GOT[0] | -> | *(.dynamic)            | -> | 0x0028 | -> | Actual Runtime Address | | <- Reserved for enabling lazy binding 
| ----------    --------------------------    ----------    -------------------------- |
| | GOT[1] | -> | *(link_map)            | -> | 0x0030 | -> | Actual Runtime Address | | <- Reserved for enabling lazy binding 
| ----------    --------------------------    ----------    -------------------------- |
| | GOT[2] | -> | *(_dl_runtime_resolve) | -> | 0x0038 | -> | Actual Runtime Address | | <- Reserved for enabling lazy binding 
| ----------    --------------------------    ----------    -------------------------- |
| | GOT[3] | -> | *(func 1)              | -> | 0x0040 | -> | Actual Runtime Address | |
| ----------    --------------------------    ----------    -------------------------- |
| | GOT[4] | -> | *(func 2)              | -> | 0x0048 | -> | Actual Runtime Address | |
| ----------    --------------------------    ----------    -------------------------- |
| ....                                                                                 |
| ....                                                                                 |
| ----------    --------------------------    ----------    -------------------------- |
| | GOT[M] | -> | *(func M)              | -> | 0x.... | -> | Actual Runtime Address | |
| ----------    --------------------------    ----------    -------------------------- |
----------------------------------------------------------------------------------------
```

But, this table is still incomplete. And we will complete it in the next section, which is procedure linkage table.

## Conclusion

I took \~5 days to write understand global offset table and write this article. Its painful, chaotic, confusing, agitating, frustrating and what not. But it is worth it.

Thank you. Next we would go through PLT as it is necessary to understand `.rela.plt` based relocations.

Until then, take rest.