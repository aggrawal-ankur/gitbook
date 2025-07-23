# Global Offset Table

## Setup

There are solutions which were primarily created for solving a problem at a certain place but their feasibility was so good that they end up getting applied to some other places as well, where the problem was either non-existing or separate solutions were applied to deal with them. Basically, to keep the system consistent, the solution was applied everywhere it could.

Kind of same vibe is with the global offset table

## Problem Statement

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
* Offset `0x3fc0` is found at line 764. And what it points to? `.got`. And guess what, this offset matches the one in the relocation table.
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

Each entry in this table is an address. Earlier it is a placeholder address, later, when resolved, it becomes the actual runtime address of that symbol.

The one thing that makes global offset table and procedure linkage table intimidating is the absence of the ability to visualize it. It is simple to say that **it is just a pointer table** but **how does it really look like?** That does matter.

## Structure of GOT

It depends on the architecture.

For 32-bit systems:

```
+------------------------+
| GOT[0]                 |  --> Reserved entry (often for dynamic linker)
+------------------------+
| GOT[1]                 |  --> Reserved (e.g., for link-time resolver, __dl_runtime_resolve)
+------------------------+
| GOT[2]                 |  --> Pointer to global function or variable #1
+------------------------+
| GOT[3]                 |  --> Pointer to global function or variable #2
+------------------------+
| GOT[4]                 |  --> Pointer to global function or variable #3
+------------------------+
| ...                    |
+------------------------+
| GOT[n]                 |  --> Pointer to global function or variable #n
+------------------------+
```

For 64-bit systems:

```
+------------------------+
| GOT[0]                 |  --> Reserved (often unused)
+------------------------+
| GOT[1]                 |  --> Reserved (link_map)
+------------------------+
| GOT[2]                 |  --> Reserved (address of the runtime resolver function, __dl_runtime_resolve)
+------------------------+
| GOT[3]                 |  --> Pointer to global function or variable #1
+------------------------+
| GOT[4]                 |  --> Pointer to global function or variable #2
+------------------------+
| ...                    |
+------------------------+
| GOT[n]                 |  --> Pointer to global function or variable #n
+------------------------+
```



Immediately, we can infer this from the table that actual entries start from `GOT[2]`. What's interesting here is the first two entries.

### What is \`GOT\[0]\` ?

The value of the 0th entry in the global offset table depends on the architecture.

<table><thead><tr><th width="198">Architecture</th><th>GOT[0]</th></tr></thead><tbody><tr><td>32-bit (x86)</td><td>The address of the <code>.dynamic</code> section.</td></tr><tr><td>64-bit (x64 or x86_64)</td><td>Generally unused or reserved. The entry exists, but it's <strong>not meant for direct use</strong> by the application.</td></tr></tbody></table>

`GOT[0]` has less to no use on 64-bit systems.

### What is \`GOT\[1]\` ?

<table><thead><tr><th width="198">Architecture</th><th>GOT[1]</th></tr></thead><tbody><tr><td>32-bit (x86)</td><td>The address of the resolver function (<code>_dl_runtime_resolve</code>) used by the PLT stub to transfer control to the dynamic linker.</td></tr><tr><td>64-bit (x64 or x86_64)</td><td>The address of the <code>.dynamic</code> section's link map, which is a runtime data structure used by the dynamic linker to track loaded shared objects and their metadata. We can't see it in static analysis but in dynamic analysis we can see it. (<em>Wait for dynamic analysis part, not now, but later.</em>)</td></tr></tbody></table>

***

In 32-bit architecture, relocation entries start from 2nd GOT entry on wards.

In 64-bit architecture, relocation entries start from 3rd GOT entry on wards.

***

Entries from `GOT[3]` to `GOT[n]` are placeholder offsets, which get replaced when the actual address is resolved.

That's it.
