---
title: Debugging In Depth
weight: 5
---

_**21 September 2025**_

***

The most popular debugger on Linux is the GNU Debugger, bettern known as gdb. There are two way to learn it.

1. You pick a crash course that teaches it ASAP.
2. You learn debugging as a concept and understand how gdb implements it.

***

You might have guessed it already, we are going for the second method. And I have two reasons for this decision:

1. My consciousness and learning methodology will not even allow me to open gdb, let alone memorizing the commands. Unless I understand the WH-family behind it and it no longer feels black magic, I can't do anything.

2. GDB is just one debugger. There are plenty more. The current landscape is such that you have to be proficient in multiple toolchains, and there are two ways to do it. One is sustainable, the other is not.

   - The first one is the quickest one: memorize the commands and don't give a damn about anything.
   - The second method is to understand debugging as a concept and gdb as one of its implementations. Learning debugging as a concept is a **transferable skill**, as the fundamentals don't change across systems and architecture. The rules remains the same, only the implementation changes.

The more you can prioritize on **transferable skills**, the more you are consciously choosing to pay upfront to avoid chaos later. And here we do exactly that.