---
id: 9d652181ee714f7988c5ed164e4cae4e
title: Compilation
weight: 3
---

***Originally written between late june and early july 2025***

***Polished on October 03, 2025***

---

The source can be compiled into x64 assembly as:
```bash
gcc -S -masm=intel hello.c -o hello_asm.s
```

## What happens in compilation?

---

If you have learned basic C a long time ao, it is highly possible that you write `void main(){}` instead of `int main()`. Many old tutorials use it, even I learned C the same way 5 years ago.

But `void main(){}` is a wrong signature for main function. For more information, check out the {{< doclink "0bfa9b05f9c345bcba55bf5d19329ce3" "Linux Processes" >}} write up. Although I don't recommend as it is not required.

Despite being wrong, it works.

If we compile the code with `void main();` signature, we get an almost similar assembly.

```asm {filename="void.asm"}
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

```asm {filename="int.asm"}
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

Only line 21 is different, from `nop` to `mov eax, 0`.

* `nop` translates to **no operation**. We need not to think about it right now.
* In the other one, we are zeroing the accumulator to pass the exit code to the next sequence in the pipeline.

***

Lets understand this assembly.

* `.file` is GAS directive, used to make the file name available to the binary.
* `.intel_syntax noprefix` is a GAS directive, specified to use intel assembly.
* `.text` starts the code section.
* `.rodata` is for read-only section.
* `.LC0` is a read-only label for a literal constant under the .rodata section. This is where `"Hello, World\n"` goes.
* `.string` is used to define null-terminated, C-style string literals.
* `.globl` makes a symbol visible to the linker.
* `.type  main, @function` specifies `main` as a function symbol.
* `.LFB0` stands for local function begin label, used internally by GCC for debugging info.
* `push rbp` pushes the base pointer of current frame on stack.
* `mov rbp, rsp` sets up a new stack frame.
* `lea rax, .LC0[rip]` uses RIP-relative addressing to load the address of `"Hello, World!\0"` string.
* `mov rdi, rax` moves the address of the string into destination index register.
* `call puts@plt` call the `puts` function in `glibc` via procedure linkage table (plt).
* `mov eax, 0` zeroes the accumulator to send as exit code.
* `pop rbp` pops the current base address.
* `ret` return.

`.cfi_*` stands for **call frame information** directives. We don't have to worry about them right now.

***

There is something missing here. There is no exit syscall. There is nothing like:
```asm
mov rax, 60
xor rdi, rdi
syscall
```

When we write raw assembly, we manage the exit ourselves. When we use shared libraries, the infrastructure sets up the environment for run and exit. The binary just comes and runs.

In the upcoming articles, we will find that there is so much that goes before and after our source code runs that will show how tiny our source is in this ecosystem.

***

If we go on [https://godbolt.org/](https://godbolt.org/) and paste our source code there, a different assembly is generated there.
```asm {filename="godbolt.asm"}
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

Right above the assembly, we can find a green tick. It shows the different options it has used to the compile the command.

By default, there is no optimization done on the code, which is why it is lengthy and readable. Shortening (optimizing) the code would result in less readability, which is not good for us as are trying to understand things.
  - So we will stick to no optimization.

***

Next is object code. Until then, bye bye.