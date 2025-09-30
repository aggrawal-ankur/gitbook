---
id: 6c40d67971f54377b365a2fe95333bf3
title: What Powers Debuggers? — 1
weight: 1
---

_**22, 23 September 2025**_

***

It looks like debuggers are doing some sort of black magic, which is not the case. To remove that black magic, we have to understand what powers debuggers.

Primarily there are 2 things behind a debugger's existence on Linux 64-bit.

- Trap instructions, CPU flags, signals and exceptions are the basis of this **black magic**.
- `ptrace` syscall is the dedicated API that allows a debugger to act as a sentinel being and observe other processes.

There is one more thing, called **symbol and debug information**.

* This is not strictly required but it makes debugging intuitive and less mentally draining. Without debug information, you'd have raw assembly and memory addresses.
* If you have no problem seeing raw assembly and memory addresses, this part is just add-on for you.
* By the way, this is a part of ELF and DWARF specs, not ptrace.

## Exceptions

An **exception** is a synchronous event that is generated when the processor detects one or more "predefined special conditions" while executing an instruction.

* Take `4/0`, that's going to raise divide by zero exception. This is only going to be raised when the CPU reaches that instruction, this is what synchronous means. The exception is not going to be raised arbitrarily, it is systematic.

Exceptions is how the CPU _stops normal execution_ and transfers control to the OS.

There are 3 classes of exceptions: faults, traps, and aborts.

* A synchronous exception detected before the instruction completes is called a **fault**. Ex: divide by zero and page fault.
* A synchronous exception after the instruction completes is called a **trap**. Ex: Breakpoint, overflow and single-step via trap flag (TF).
* An **abort** is a catastrophic exception, which typically **cannot be handled normally**. Usually indicates hardware failure or an unrecoverable condition.

## Interrupts

An **interrupt** is an asynchronous event which is typically triggered by an I/O device. For example:

* `CTRL + C` to exit an infinite loop or a hanged terminal process.
* `CTRL + D` to exit python shell.

When an interrupt or an exception is signaled, the processor halts the execution of the program and switches to a handler procedure that has been written specifically to handle the interrupt/exception condition.

The processor accesses the handler procedure through an entry in the **interrupt descriptor table** (IDT). When the handler is done handling the interrupt/exception, program control is returned to the interrupted program.

The IA-32 architecture has 18 predefined interrupts and exceptions and 224 user defined interrupts.

| Vector | Mnemonic | Description | Type |
| :--- | :--- | :--- | :--- |
| 0 | #DE | Divide Error (div by zero or quotient too large) | Fault |
| 1 | #DB | Debug (single-step, hardware breakpoints) | Fault/Trap |
| 2 | NMI | Non-maskable Interrupt (NMI) | Interrupt |
| 3 | #BP | Breakpoint (INT3instruction) | Trap |
| 4 | #OF | Overflow (INTOinstruction) | Trap |
| 5 | #BR | BOUND Range Exceeded (BOUND instruction) | Fault |
| 6 | #UD | Invalid Opcode | Fault |
| 7 | #NM | Device not available | Fault |
| 8 | #DF | Double Fault | Abort |
| 9 | — (Legacy Coprocessor) | Coprocessor Segment Overrun | Fault |
| 10 | #TS | Invalid TSS | Fault |
| 11 | #NP | Segment Not Present | Fault |
| 12 | #SS | Stack Segment Fault | Fault |
| 13 | #GP | General Protection Fault | Fault |
| 14 | #PF | Page Fault | Fault |
| 15 | Intel Reserved | Reserved | — |
| 16 | #MF | x87 FPU Floating-Point Error (Math Fault) | Fault |
| 17 | #AC | Alignment Check (only in ring 3, CR0.AM=1) | Fault |
| 18 | #MC | Machine Check | Abort |
| 19 | #XM/#XF | SIMD Floating-Point Exception (SSE, AVX) | Fault |
| 20–31 |  | Reserved for future Intel use |  |

When the trap flag in `RFLAGS` is set, the CPU generates a debug exception (#DB) after every instruction. This is the hardware single-step mode.

### Breakpoint

`INT3` is a one-byte (`0xCC`) instruction inserted by the debugger, which when executed CPU raises a breakpoint exception (`#BP`). The kernel delivers a `SIGTRAP` to the process.

To insert a breakpoint at an address, the debugger modifies the first byte of that instruction to `0xCC`. When the CPU reaches that instruction, a break point exception is triggered.

To resume execution, the debugger restores the first byte of that instruction.
- Since `RIP` has advanced by one while triggering `0xCC`, the debugger decrements `RIP` by 1 so that it points back to the intended instruction.

It is used to stop execution at a certain address in the process.

### Trap Flag

Trap flag or `RFLAGS.TF` is the 8th bit in the CPU flags register.

When this bit is set to 1, CPU raises a debug exception (`#DB`) after every instruction in the process. Then the kernel delivers `SIGTRAP` to the debugger.

**Single-step** means execute one instruction and then stop. It is achieved by setting `RFLAGS.TF=1`.

## Conclusion

A debugger program sets up either an `INT3` instruction to create a breakpoint at an address or it sets the `RFLAGS.TF` bit to 1 to stop after each instruction.

When a breakpoint is set on an instruction, an `INT3` instruction executes immediately, which raises a `#BP` exception. The kernel responds to this by sending a `SIGTRAP` to the debugger, which the debugger process catches via ptrace.

When `RFLAGS.TF=1`, a `#DB` exception is raised after every instruction in the process. The kernel responds similarly by sending a `SIGTRAP`, which the debugger program catches via `ptrace`.

## References

[Intel 64 and 32 bit Manual](https://cdrdv2.intel.com/v1/dl/getContent/671200)