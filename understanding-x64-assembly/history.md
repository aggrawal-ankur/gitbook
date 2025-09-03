# Theoretical Introduction

## Introduction to Assembly

Assembly is a low-level programming language, which provides direct-access over computer hardware. It almost maps one-to-one with machine instructions.

Assembly is the closest we can get to the CPU while still understanding what's going on.

What distinguishes assembly from other programming languages is that **every CPU architecture** (like x86, ARM, MIPS, RISC-V) has its **own assembly language**.

Why different flavors of assembly exist?

* Because of the **Instruction Set Architecture (ISA)**.
* Each CPU has its own set of instructions, which creates demand for specific-assembly.

### Architectural History

The x86 CPU architecture, which refers to a family of processors — 8086, 80186, 80286, 80386, 80486 — was originally developed by **Intel Corporation**, starting in **1978**.

The x86 ISA is a **Intel's proprietary**, but other companies (notably **AMD**) were **licensed** to create compatible CPUs.

All these processors share the same **Instruction Set Architecture (ISA)** and are collectively known as **x86**.

The original **8086** was a **16-bit** processor. Intel extended it to **32-bit**, known as **IA-32** (or x86\_32). Then in **2003**, AMD extended the architecture to **64-bit**, releasing **AMD64**. Intel later adopted the same ISA, calling their version **Intel 64** — both are **functionally identical**.

Since Intel designed the architecture, they also defined the original syntax for its assembly — known as, **Intel syntax**. This style is widely used in **Microsoft** development tools and the **Windows** ecosystem.

But Intel is not the only syntax for x86 processors.

### The Origins of AT\&T Syntax

Along the same time, **AT\&T**, through **Bell Labs**, created **Unix** in **1969**, originally for **PDP-7** machines, which was initially written in assembly. By **1973**, Unix was rewritten in **C**, making it portable.

In **1978**, Intel introduced the x86 architecture, which eventually became popular on personal computers.

In **1983**, **GNU Project** was launched to create a **free, Unix-like operating system**. It needed a new assembler and adopted a **new assembly syntax** for x86 that was more consistent and easier to parse than Intel's. Also, they wanted to avoid the proprietary issues, and this created the need for a new syntax.

This new syntax, although created by GNU, was based on conventions from Unix systems — and since **Unix was synonymous with AT\&T**, this style became popular as **AT\&T syntax**.

When **Linux** was created in **1991**, it relied heavily on GNU tools like **GCC** and **GAS**, which used AT\&T syntax. As a result, **AT\&T** syntax became the _de facto_ in the Linux ecosystem.

### Which Syntax We Are Going To Be Using?

We are learning assembly, not syntaxes. The only thing that matters here is an assembler. Because an assembly code heavily uses assembler directives. That's it.

We will write intel syntax and use GAS. Because, the operand style matches the mathematical style, `LHS = RHS`.

```
// Intel
mnemonic destination, source

// AT&T
mnemonic source, destination
```

**Learn Assembly, Not Syntaxes.**

## Difference Between Assembly And Other Languages (C, Python.....)

### 1. Core Purpose

High level languages abstract the core functionality. Their core purpose is to provide the programmer with ease of usability and reduce development time.

Assembly, on the other hand, is completely raw. There's no abstraction. Everything is open and the programmer has to write every single instruction themselves.

This exposes the reality that even a simple "Hello, World!" program requires multiple low-level steps before it can actually run.

### 2. Platform Dependency

We are used to download python for our windows, Linux or mac machine and start coding. We don't have to worry about how CPU will understand our hand writing.

But assembly doesn't work like that. It is **architecture-dependent**. Assembly written for x86 will not work on ARM.

### 3. Control >> Convenience

Assembly gives you **maximum control**, at the cost of **convenience**.

What is convenience?

* **Pretty and verbose named variables**? Not in assembly. You work directly with memory and registers.
* **Data types**? Everything is just bytes. It's up to **you** to interpret the bytes as intended.
* **Control flow**? Nothing is built in. You implement it using jump instructions.
* **Loops**? You use jump statements to create them as well.
* **I/O**? Use direct syscalls. No dedicated `printf` and `scanf`
* **Data Structures**? **Functions**? **DO. IT. YOURSELF.**

You have got every raw material, and building anything is your responsibility.

***

How these things exist then? We will explore each of them soon.

## Fun Fact

C is called portable assembly.
