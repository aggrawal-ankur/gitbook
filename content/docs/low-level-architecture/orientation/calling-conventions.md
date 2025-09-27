---
title: Calling Conventions
weight: 6
---

Registers are fast, low-level storage locations inside the CPU. While x86\_64 offers 16 general-purpose registers, their usage is often guided by conventions rather than absolute freedom.

The use of these registers usually depends on the context. Primarily there exist two contexts:

1. Function Call Context
2. System Call Context

How the registers would be used in the above two contexts is defined in a system-level agreement, called ABI, which stands for _Application Binary Interface_.

As long as we are out of these two contexts, we can use a register as we want. And we will demonstrate this later.

## Function Call Convention

| Argument   | Register | Description      |
| :--- | :--- | :--- |
| Syscall #  | `rax`    | Identifier       |
| Argument 1 | `rdi`    | First parameter  |
| Argument 2 | `rsi`    | Second parameter |
| Argument 3 | `rdx`    | Third parameter  |
| Argument 4 | `r10`    | Fourth parameter |
| Argument 5 | `r8`     | Fifth parameter  |
| Argument 6 | `r9`     | Sixth parameter  |

## Syscall Convention


| Register | Purpose / Convention |
| :--- | :--- |
| rax | Accumulator; return values, syscall # |
| rbx | Base register; often callee-saved |
| rcx | Counter for loops, shifts |
| rdx | Data register; I/O, syscall args |
| rsi | Source index; memory ops, args |
| rdi | Destination index; memory ops, args |
| rbp | Base pointer; stack frame reference |
| rsp | Stack pointer; top of the stack |
| r8 | 5th syscall argument |
| r9 | 6th syscall argument |
| r10 | 4th syscall argument |
| r11 | Temporary scratch for syscall |
| r12–r15 | Callee-saved; general-purpose |


**Note:** _Caller_ is the function that makes a call to another function. The function that is being called is termed as _callee_.

* When a register is callee-saved, the callee function must preserve the state of that register if it wants to use it and restore its state before returning.
* When a register is caller-saved, the caller function must preserve its state if it wants to use it later because a function call in-between might use it and it has no reason to preserve its state.

In Linux (x86\_64), the most common calling convention is **System V AMD64 ABI**. It defines how functions and system calls exchange data by assigning specific roles to specific registers.

To successfully invoke a system call, our data must be placed in these registers accordingly. Otherwise, the kernel will not interpret our request correctly.

## But Why Do These Conventions Even Exist?

System V ABI (where V is 5) is not the only ABI that exist. It is the one that Linux uses. Microsoft Windows 64-bit uses x64 ABI.

If every organization used their own calling convention, one thing is sure to suffer — cross-compatibility. These ABIs are contracts that everyone agrees upon. When every system uses the same convention, cross-compatibility improved. Software support improved.