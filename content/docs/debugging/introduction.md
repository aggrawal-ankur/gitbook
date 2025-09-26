---
title: Introduction To Debugging
weight: 1
---

_**22, 23 September 2025**_

***

At its core, _**debugging**_ can be defined as a process of actively observing and controlling a program to understand what it’s doing, why it’s doing it, and how to manipulate it.

A **debugger** is like a sentinel being who can observe everything about a process and change it against its will. It's like _S2 Loki (A Marvel Studious TV Series)_.

Any debugger primarily does these three things:

* Stop execution at a known point (breakpoints, signals, traps)
* Inspect program state (memory, registers, stack, variables)
* Modify execution if needed (change variable values, registers, or program counter)

To understand debuggers, we have to understand what enables debugging. Otherwise, gdb will feel black magic.
