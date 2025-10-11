---
id: e5a0bbb59138438fa3d33b51fc92a158
title: Introduction To Assembly
weight: 1
---

Assembly is a low-level programming language, which provides direct-access to computer hardware. It maps "almost" one-to-one with machine instructions.

Assembly is the closest we can get to the CPU while still understanding what's going on.

Every CPU architecture (like x86, ARM, MIPS, RISC-V) has a different instruction set architecture, which leads to different assemblies.

## Architectural History

The x86 CPU architecture, which refers to a family of processors — 8086, 80186, 80286, 80386, 80486 — was originally developed by **Intel Corporation**, starting in **1978**.

The x86 ISA is **Intel's proprietary**, but other companies (notably **AMD**) were **licensed** to create compatible CPUs.

All these processors share the same **Instruction Set Architecture (ISA)** and are collectively known as **x86**.

The original **8086** was a **16-bit** processor.
  - Intel extended it to **32-bit**, known as **IA-32** (or x86_32).
  - In **2003**, AMD extended the architecture to **64-bit**, releasing **AMD64**. Later, Intel adopted the same ISA, as **Intel 64**. Both are **functionally identical**.

Since Intel designed the original architecture, they also defined the syntax for its assembly — known as, **Intel syntax**. This style is widely used in **Microsoft and Windows ecosystem**.

## The Origins of AT\&T Syntax

Along the same time, **AT&T**, through **Bell Labs**, created **Unix** in **1969**, originally for **PDP-7** machines, which was initially written in assembly. By **1973**, Unix was rewritten in **C**, making it portable.

In **1978**, Intel introduced the x86 architecture, which eventually became popular on personal computers.

In **1983**, **GNU Project** was launched to create a **free, Unix-like operating system**. It required a new assembler to avoid proprietary issues with Intel and adopted a **new assembly syntax**.

This new syntax, although created by GNU, was based on conventions from Unix systems — and **Unix was synonymous with AT&T**, so this style became popular as **the AT&T syntax**.

When **Linux** was created in **1991**, it relied heavily on GNU tools like **GCC** and **GAS**, which used AT&T syntax. As a result, **AT&T** syntax became the _de facto_ in the Linux ecosystem.

## ISA and Assembler

Every CPU has an instruction set architecture which defines the capabilities of a CPU.

Assembly instructions are converted into ISA compatible machine code by a program called assembler.

There are multiple assemblers such as `as` (GNU Assembler), `nasm` (Netwide Assembler), `fasm` (Fish Assembler), and `masm` (Microsoft Assembler).

Assemblers provide some ease of development in the form of directives, which they resolve to actual machine understandable instructions while assembling the program.
  - This makes assembly code dependent on the assembler.
  - If the developer had used `nasm` to assemble it, we can't use any other assembler.

---

Learn assembly, not syntax. We will use the GNU assembler with intel syntax.

## Difference Between Assembly And Other Languages

### 1. Core Purpose

High level languages abstract the core functionality to provide the programmer with ease of usability and reduce the development time.

Assembly has everything in the raw form and the programmer has to write every single instruction themselves.

### 2. Platform Dependency

Languages like python are easy to download. Just grab the right installer for your OS, download, run the installer and start coding.
  - Python code written on Mac works on Windows and Linux.

But assembly is **architecture and assembler dependent**.
  - Assembly written for x86 will not work on ARM.
  - Assembly processed by one assembler will fail on the other.

### 3. Control >> Convenience

Assembly gives the programmer **maximum control** at the cost of **convenience**.

What is convenience?
  * No variables. We've to work with memory and registers directly.
  * No data types. Everything is just bytes.
  * No if-else ladder. We've to implement it using jump statements.
  * No Loops. Use jump statements.
  * No functions. User jump statements.
  * No I/O wrappers. Direct syscalls.
