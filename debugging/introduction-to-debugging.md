# Introduction To Debugging

_**22 September 2025**_

***

At its core, _**debugging**_ can be defined as a process of actively observing and controlling a program to understand what it’s doing, why it’s doing it, and how to manipulate it.

A **debugger** is like a sentinel being who can observe everything about a process and change it against its will. It's like _S2 Loki (A Marvel Studious TV Series)_.

Any debugger primarily does these three things:

* Stop execution at a known point (breakpoints, signals, traps)
* Inspect program state (memory, registers, stack, variables)
* Modify execution if needed (change variable values, registers, or program counter)

***

But from virtual memory, we know that every process is isolated and no other process can intervene into other processes and debugging seems to be violating that. How does that work?

* Yes. To understand this, we have to understand what enables debugging.

Debugging is not something that a normal user requires. It is for developers who have to test the strength of their programs. On Linux, the `ptrace` syscall gives you debugging capabilities.

* `ptrace` is like fire. It is lethal but that doesn't mean we don't use it.
* Similarly, `ptrace` is an extension not meant to be used by everyone and those who use it (developers primarily), have to do that cautiously.
* `ptrace` lets one process (the debugger) control another process (the debuggee).
* But `ptrace` is not the only thing that enables debugging. Debugging relies heavily on CPU traps and flags, signals and exception and direct memory access.

many systems don't come with `ptrace` as a normal user have no use of it. It's an add-on feature.

***

By default, only a process with the **same UID as the target** can attach via `ptrace`.

* Example: your user can debug programs you own, but not root’s programs.







## What enables debugging?

Breakpoints

1. Software (traps and flags)
2. Hardware

Single-stepping

Memory inspection and modification

Signals and exceptions



## What processes can a debugger debug? Can a process deny debugging?
