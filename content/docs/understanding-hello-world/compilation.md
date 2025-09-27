---
title: "Compilation: Turning C Into Assembly"
weight: 5
---

Let's start our journey with the output of compilation.

The source can be compiled into assembly using&#x20;

```
gcc -S -masm=intel hello.c -o hello_asm.s
```

Previously, we've learned that `void main();` is a wrong signature for main function. But if we compile the code with `void main();` signature, we get an almost similar assembly.

```asm
    .file     "hello.c"
    .intel_syntax noprefix
    .text
    .section  .rodata
.LC0:
    .string   "Hello, World!"
    .text
    .globl    main
    .type     main, @function
main:
.LFB0:
    .cfi_startproc
    push rbp
    .cfi_def_cfa_offset 16
    .cfi_offset 6, -16
    mov	rbp, rsp
    .cfi_def_cfa_register 6
    lea	rax, .LC0[rip]
    mov	rdi, rax
    call     puts@PLT
    nop
    pop	rbp
    .cfi_def_cfa 7, 8
    ret
    .cfi_endproc
.LFE0:
    .size	main, .-main
    .ident	"GCC: (Debian 14.2.0-19) 14.2.0"
    .section	.note.GNU-stack,"",@progbits
```

And this is the assembly generated for `int main(void);` signature.

```asm
    .file     "hello.c"
    .intel_syntax noprefix
    .text
    .section  .rodata
.LC0:
    .string   "Hello, World!"
    .text
    .globl    main
    .type     main, @function
main:
.LFB0:
    .cfi_startproc
    push rbp
    .cfi_def_cfa_offset 16
    .cfi_offset 6, -16
    mov	rbp, rsp
    .cfi_def_cfa_register 6
    lea	rax, .LC0[rip]
    mov	rdi, rax
    call     puts@PLT
    mov eax, 0
    pop	rbp
    .cfi_def_cfa 7, 8
    ret
    .cfi_endproc
.LFE0:
    .size	main, .-main
    .ident	"GCC: (Debian 14.2.0-19) 14.2.0"
    .section	.note.GNU-stack,"",@progbits
```

It's clear that only line 21 is different, from `nop` to `mov eax, 0`.

* `nop` translates to **no operation**. We need not to think about it right now.
* In the other one, we are zeroing the accumulator to pass the exit code to the next sequence in the pipeline.

***

Lets understand this assembly now.

* `.file` is an assembler (GAS) directive to make the file name available to the binary.
* `.intel_syntax noprefix` is a GAS specific directive, which is specified to use intel style assembly.
* `.text` marks the start of code section.
* `.rodata` marks the start of a read-only section.
* `.LC0` is a label for a literal constant.
* `.string` is used to define null-terminated, C-style string literals. This is where our `"Hello, World\n"` goes.
* `.globl` makes a symbol visible to the linker.
* `.type  main, @function` specifies that `main` is a function symbol.
* `.LFB0` stands for local function begin label, used internally by GCC for debugging info.
* `push rbp` pushes the base pointer of current frame on stack.
* `mov rbp, rsp` sets up a new stack frame.
* `lea rax, .LC0[rip]` uses RIP-relative addressing to load the address of "Hello, World!\0" string.
* `mov rdi, rax` moves the address of the string into destination index register.
* `call puts@plt` calls the `puts` function in `glibc` via procedure linkage table (plt).
  * We'll expand on it further.
* `mov eax, 0` zeroes the accumulator to send as exit code.
* `pop rbp` pops the current base address.
* `ret` return.

***

If you are not learning passively, you are definitely wondering what about `.cfi_*` directives?

* It stands for **call frame information** directives. And we don't have to worry about them.

***

There is something that is missing here. Can you spot it? There is no exit syscall. There is nothing like

```asm
mov rax, 60
xor rdi, rdi
syscall
```

Exit is never controlled by our source code.&#x20;

* When we write raw assembly, we manage exit ourselves. When we use shared libraries, we are using a complete infrastructure to run something. Now it is the duty of the infrastructure to take care of this.
* In the upcoming articles, we will find that there is so much that goes before our source code gets executed and there is so much that comes after it is executed, we'll understand how tiny our source code really is.

***

If we visit [https://godbolt.org/](https://godbolt.org/) and paste our source code there, we can find that the assembly generated there is very different. Something like this:

```asm
.LC0:
    .string "Hello, World!"
main:
    push  rbp
    mov   rbp, rsp
    mov   edi, OFFSET FLAT:.LC0
    call  puts
    mov   eax, 0
    pop   rbp
    ret
```

In the right section, where the assembly part is displayed, you can find a clickable link to **Libraries**. Above that is green tick. Click on that and you will find that different options are passed to the compiler to optimize the command.

* It is the result of those compiler options that we see such a simple and stripped away assembly.

By default, there is no optimization done on the code, which is why it is lengthy and readable. Shortening (optimizing) the code would result in less readability, which is not good for us as are trying to understand things.

* And we will stick to no optimization.

***

And we have walked the first step. This marks the end of understanding assembly.

Now we will move to object code.
