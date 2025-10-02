---
id: 7f85ac8f999d4486a718747efdd166d4
title: Debugging In Depth
weight: 5
---

_**21 September 2025**_

***22, 23 September 2025 (merged the next article)***

***

The most popular debugger on Linux is the GNU Debugger, bettern known as gdb. There are two way to learn it.

- You pick a crash course that teaches it ASAP.
- You learn debugging as a concept and understand how gdb implements it.

You might have guessed it already, we are going for the second method. And I have two reasons for this decision:

- My consciousness and learning methodology will not even allow me to open gdb, let alone memorizing the commands. Unless I understand the WH-family behind it and it no longer feels black magic, I can't do anything.

- GDB is just one debugger. There are plenty more. The current landscape is such that you have to be proficient in multiple toolchains, and there are two ways to do it. One is sustainable, the other is not.

  - The first one is the quickest one: memorize the commands and don't give a damn about anything.
  - The second method is to understand debugging as a concept and gdb as one of its implementations. Learning debugging as a concept is a **transferable skill**, as the fundamentals don't change across systems and architecture. The rules remains the same, only the implementation changes.

The more you can prioritize on **transferable skills**, the more you are consciously choosing to pay upfront to avoid chaos later. And here we do exactly that.

---

Anyways, at its core, _**debugging**_ can be defined as a process of actively observing and controlling a program to understand what it’s doing, why it’s doing it, and how to manipulate it.

A **debugger** is like a sentinel being who can observe everything about a process and change it against its will. It's like _S2 Loki (A Marvel Studious TV Series)_.

Any debugger primarily does these three things:

* Stop execution at a known point (breakpoints, signals, traps)
* Inspect program state (memory, registers, stack, variables)
* Modify execution if needed (change variable values, registers, or program counter)

To understand debuggers, we have to understand what enables debugging. Otherwise, gdb will feel black magic.

{{< doclink "6c40d67971f54377b365a2fe95333bf3" "" >}}
{{< doclink "dbfd38c8b6c64c299e06428a83b15ad9" "" >}}
{{< doclink "f7b8cc4c1a6f4ebb8124944fbf283068" "" >}}
{{< doclink "32490ce1c9a646d2a505ee9bc1b0cda6" "" >}}