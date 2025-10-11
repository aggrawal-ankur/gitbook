---
id: 8070b094e93d4ac98501c3d89d2ca6e8
title: Instructions
weight: 4
---

An instruction is an atomic operation that tells the CPU what to do.

```asm
mnemonic destination, source
```

Mnemonic is the actual CPU operation. Destination and source are the operands it is generally performed on.

Some mnemonics take one operand only. So, this is not strict.

Example:
```asm
mov rax, 1
```
  * move 1 into `rax` register.
  * It also aligns with the mathematical assignment of values, `a = 4`, assign 4 to a.

## Common Operations

There are hundreds of instructions in assembly. But the core ones are as follows.

| Category | Purpose | Common Instructions |
| :--- | :--- | :--- |
| Data Movement | Move data between register and memory. | mov,lea,xchg |
| Arithmetic | Mathematical operations | add,sub,mul,div,inc,dec |
| Logic/Bitwise | Logical or bit manipulation | and,or,xor,not,shl,shr |
| Control Flow | Changing execution path (conditionals and iteration) | jmp,je,jne,call,ret |
| Comparison/Test | Set CPU flags based on results | cmp,test |
| Stack Operations | Push and Pop | push,pop |
| System/Interrupt | Interacting with the OS or hardware | syscall,int |

## CPU Flags

CPU flags are binary indicators (either 0 or 1) that reflect the outcome of certain operations or hold special status information. They're part of the processor's status register, which is used by instructions like `cmp` (compare) and `test`.

When an instruction modifies the flags, other instructions can check the state of these flags to make decisions, like jumping to different parts of code based on conditions.

Example:

| Flag | Description |
| :--- | :---------- |
| **ZF** (Zero Flag) | Set to 1 if the result of an operation is zero; otherwise, it’s 0.                                |
| **SF** (Sign Flag) | Set to 1 if the result of an operation is negative (the most significant bit of the result is 1). |

There are other flags as well.

## Memory/Pointer Dereferencing

It refers to obtaining the actual value stored at a memory location.

It is done by `[]`.

For example, if a memory location like 100000 stores a number, such as 45, dereferencing the memory location would give 45, like this, `[100000] = 45`

## Common Instructions

### `mov`

In simple words, it is assignment operator (`=`) in assembly.

Syntax:

```asm
mov destination, source
```

Mathematically, it is `destination = source`.

Most commonly, these operands are registers like rax, rsi etc.... But there are other options as well.

  - `mov rax, rsi` means `rsi = rax`.
  - `mov rax, [rsi]`: dereference the value in `rsi` and put it into `rax`.
  - `mov [rsi], rax`: dereference the value in `rsi` and store what's inside `rax` in there.

**Note: `mov` copy data from one place to other. Its not 'move' in literal sense.**

### `cmp`

It compares two values by subtracting them, later deciding what might be the case.

In C, we can do something like this: `a = (4 > 2)` and `a` will contain the result. However, that's not the case here.

Syntax:
```asm
cmp a, b
```
... which evaluates to `a - b`.

When we do `cmp 4, 2`, `cmp` does `4-2`, and the result is 2. This result is not stored. Instead, certain CPU flags are changed based on the result. Jump statements use these flags to decide what to do next.

### Jump Statements

They change the flow of execution. Instead of executing the next line, they send the CPU to another part of the code based on some condition. This is what `if-else` stands on.

There are two types of jumps, conditional and unconditional.

An unconditional jump always goes to some label, no matter what. `jmp some_label` is an unconditional jump.

A conditional jump is based on the flags set by `cmp`.

## Type Specifier

Type specifiers are used to explicitly tell the assembler what size of data we're working with while accessing memory.

They ensure that the assembler knows how much data to read or write.

Common type specifiers include:

  - `byte ptr`: load only 1-byte from the memory address.
  - `word ptr`: load a word or 2-bytes (in x86_64) from the memory address.
  - `dword ptr`: load a double word or 4-bytes from the memory address.
  - `qword ptr`: load a quad word or 8-bytes from the memory address.

They are particularly important (actually necessary) when working with memory operands and dereferencing pointers because x86_64 architecture can handle different size of data (like bytes, words, double words, etc).

Many assemblers offer separate mnemonics for special data movements, like GAS.