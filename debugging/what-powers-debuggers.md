# What Powers Debuggers?

_**23 September 2025**_

***

## Premise

It looks like debuggers are doing some sort of black magic, which is not the case. To remove that black magic, we have to understand what powers debuggers.

Primarily there are 2 things that power a debugging program.

1. Trap instructions, CPU flags, signals and exceptions are the basis of this **black magic**.
2. `ptrace` syscall is the dedicated API that allows a debugger to act as a sentinel being and observe other processes. It allows the debugger to make use of traps and signals to do the black magic.

But there is one more thing, called **symbol and debug information**.

* This is not strictly required but it makes debugging intuitive and less mentally draining. Without debug information, you'd just have raw assembly and memory addresses.
* If you have no problem seeing raw assembly and memory addresses, this part is just add-on for you. But to make the process easier, debug information is a necessary thing.
* By the way, this is a part of ELF and DWARF specs.

## Exceptions

An **exception** is a synchronous event that is generated when the processor detects one or more "predefined special conditions" while executing an instruction.

* Take `4/0`, that's going to raise divide by zero exception. This is only going to be raised when the CPU reaches that instruction, this is what synchronous means. The exception is not going to be raised arbitrarily but systematically.

Exceptions is how the CPU _stops normal execution_ and transfers control to the OS.

There are 3 classes of exceptions: faults, traps, and aborts.

* A synchronous exception detected before the instruction completes is called a **fault**. Ex: divide by zero and page fault.
* A synchronous exception after the instruction completes is called a **trap**. Ex: Breakpoint, overflow and single-step via trap flag (TF).
* An **abort** is a catastrophic exception, which typically **cannot be handled normally**. Usually indicates hardware failure or an unrecoverable condition.

## Interrupts

An **interrupt** is an asynchronous event that is typically triggered by an I/O device. For example:

* `CTRL + C` to exit an infinite loop or a hanged terminal process.
* `CTRL + D` to exit python shell.

When an interrupt or an exception is signaled, the processor halts the execution of the program and switches to a handler procedure that has been written specifically to handle the interrupt or exception condition.

The processor accesses the handler procedure through an entry in the **interrupt descriptor table** (IDT). When the handler has completed handling the interrupt or exception, program control is returned to the interrupted program.

The IA-32 Architecture defines 18 predefined interrupts and exceptions and 224 user defined interrupts.

<table><thead><tr><th width="84">Vector</th><th width="139">Mnemonic</th><th width="404">Description</th><th>Type</th></tr></thead><tbody><tr><td>0</td><td>#DE</td><td>Divide Error (div by zero or quotient too large)</td><td>Fault</td></tr><tr><td>1</td><td>#DB</td><td>Debug (single-step, hardware breakpoints)</td><td>Fault/Trap</td></tr><tr><td>2</td><td>NMI</td><td>Non-maskable Interrupt (NMI)</td><td>Interrupt</td></tr><tr><td>3</td><td>#BP</td><td>Breakpoint (<code>INT3</code> instruction)</td><td>Trap</td></tr><tr><td>4</td><td>#OF</td><td>Overflow (<code>INTO</code> instruction)</td><td>Trap</td></tr><tr><td>5</td><td>#BR</td><td>BOUND Range Exceeded (BOUND instruction)</td><td>Fault</td></tr><tr><td>6</td><td>#UD</td><td>Invalid Opcode</td><td>Fault</td></tr><tr><td>7</td><td>#NM</td><td>Device not available</td><td>Fault</td></tr><tr><td>8</td><td>#DF</td><td>Double Fault</td><td>Abort</td></tr><tr><td>9</td><td>— (Legacy Coprocessor)</td><td>Coprocessor Segment Overrun</td><td>Fault</td></tr><tr><td>10</td><td>#TS</td><td>Invalid TSS</td><td>Fault</td></tr><tr><td>11</td><td>#NP</td><td>Segment Not Present</td><td>Fault</td></tr><tr><td>12</td><td>#SS</td><td>Stack Segment Fault</td><td>Fault</td></tr><tr><td>13</td><td>#GP</td><td>General Protection Fault</td><td>Fault</td></tr><tr><td>14</td><td>#PF</td><td>Page Fault</td><td>Fault</td></tr><tr><td>15</td><td>Intel Reserved</td><td>Reserved</td><td>—</td></tr><tr><td>16</td><td>#MF</td><td>x87 FPU Floating-Point Error (Math Fault)</td><td>Fault</td></tr><tr><td>17</td><td>#AC</td><td>Alignment Check (only in ring 3, CR0.AM=1)</td><td>Fault</td></tr><tr><td>18</td><td>#MC</td><td>Machine Check</td><td>Abort</td></tr><tr><td>19</td><td>#XM/#XF</td><td>SIMD Floating-Point Exception (SSE, AVX)</td><td>Fault</td></tr><tr><td>20–31</td><td></td><td>Reserved for future Intel use</td><td></td></tr></tbody></table>

When the trap flag in `RFLAGS` is set, which is the 8th bit, the CPU generates a debug exception (#DB) after every instruction. This is the hardware single-step mode.

### Breakpoint

`INT3` is a one-byte (`0xCC`) instruction inserted by the debugger, which when executed CPU raises a breakpoint exception (`#BP`). The kernel delivers a `SIGTRAP` to the process.

To insert a breakpoint at an address, the debugger modifies the first byte of that instruction to `0xCC`. When the CPU reaches that instruction, a break point exception is triggered.

To resume execution, the debugger restores the original byte at that instruction’s address. Since `RIP` has advanced by one (past the `0xCC`), the debugger decrements `RIP` by 1 so that it points back to the intended instruction.

It is used to stop execution at a certain address in the process.

### Trap Flag

Trap flag or `RFLAGS.TF` is the 8th bit in the CPU flags register.

When this bit is set to 1, the CPU raises a debug exception (`#DB`) after every instruction in the process. Kernel delivers `SIGTRAP` to the debugger.

**Single-step** means execute one instruction and then stop. It is achieved by setting `RFLAGS.TF=1`.

## Conclusion

A debugger program sets up either an `INT3` instruction to create a breakpoint at an address or it sets up the `RFLAGS.TF` bit to 1 to stop after each instruction.

When a breakpoint is set after an instruction an `INT3` instruction executes immediately after it, which raises a `#BP` exception. The kernel responds to this by sending a `SIGTRAP` , which the debugger program catches via `ptrace`. The rest is taken care by `ptrace`.

When `RFLAGS.TF=1` , a `#DB` exception is raised after every instruction in the process. The kernel responds similarly by sending a `SIGTRAP`, which the debugger program catches via `ptrace`. The rest is taken care by `ptrace` itself.

## References

[Intel 64 and 32 bit Manual](https://cdrdv2.intel.com/v1/dl/getContent/671200)
