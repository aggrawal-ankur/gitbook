---
id: 9d652181ee714f7988c5ed164e4cae4e
title: Compilation
weight: 3
---

```c {filename=main.c}
#include <stdio.h>

int main(void){
    printf("Hello, World!\n");
}
```

This source code can be compiled using gcc.
```bash
gcc -S -masm=intel hello.c -o hello_asm.s
```

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

`-masm=intel` ensures intel assembly

Lets understand this assembly.

USE A TABLE INSTEAD

  - `.file` is GAS directive, used to make the file name available to the binary.
  - `.intel_syntax noprefix` is a GAS directive, specified to use intel assembly.
  - `.text` starts the code section.
  - `.rodata` is for read-only section.
  - `.LC0` is a read-only label for a literal constant under the .rodata section. This is where `"Hello, World\n"` goes.
  - `.string` is used to define null-terminated, C-style string literals.
  - `.globl` makes a symbol visible to the linker.
  - `.type  main, @function` specifies `main` as a function symbol.
  - `.LFB0` stands for local function begin label, used internally by GCC for debugging info.
  - `push rbp` pushes the base pointer of current frame on stack.
  - `mov rbp, rsp` sets up a new stack frame.
  - `lea rax, .LC0[rip]` uses RIP-relative addressing to load the address of `"Hello, World!\0"` string.
  - `mov rdi, rax` moves the address of the string into destination index register.
  - `call puts@plt` call the `puts` function in `glibc` via procedure linkage table (plt).
  - `mov eax, 0` zeroes the accumulator to send as exit code.
  - `pop rbp` pops the current base address.
  - `ret` return.

`.cfi_*` stands for **call frame information** directives.

***

There is no exit syscall.

When we write raw assembly, we manage the exit ourselves. When we use shared libraries, the infrastructure sets up the environment for run and exit. The binary just comes and runs.

In the upcoming articles, we will find that there is so much that goes before and after our source code runs that will show how tiny our source is in this ecosystem.

***

Next is object code.