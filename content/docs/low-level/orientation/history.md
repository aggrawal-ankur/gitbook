---
id: e5a0bbb59138438fa3d33b51fc92a158
title: Historical Introduction
weight: 1
---

Assembly is a low-level programming language, which provides direct-access over computer hardware. It maps almost one-to-one with machine instructions.

Assembly is the closest we can get to the CPU while still understanding what's going on.

What distinguishes assembly from other programming languages is that **every CPU architecture** (like x86, ARM, MIPS, RISC-V) has its **own assembly language**.

Different flavors of assembly exist because every CPU has a different **Instruction Set Architecture (ISA)**.
- In simple words, ISA lists all the capabilities of a CPU.

----

## Architectural History

The x86 CPU architecture, which refers to a family of processors — 8086, 80186, 80286, 80386, 80486 — was originally developed by **Intel Corporation**, starting in **1978**.

The x86 ISA is a **Intel's proprietary**, but other companies (notably **AMD**) were **licensed** to create compatible CPUs.

All these processors share the same **Instruction Set Architecture (ISA)** and are collectively known as **x86**.

The original **8086** was a **16-bit** processor. Intel extended it to **32-bit**, known as **IA-32** (or x86_32). Then in **2003**, AMD extended the architecture to **64-bit**, releasing **AMD64**. Intel later adopted the same ISA, calling their version **Intel 64** — both are **functionally identical**.

Since Intel designed the architecture, they also defined the original syntax for its assembly — known as, **Intel syntax**. This style is widely used in **Microsoft** development tools and the **Windows** ecosystem.

But Intel is not the only syntax for x86 processors.

----

## The Origins of AT\&T Syntax

Along the same time, **AT\&T**, through **Bell Labs**, created **Unix** in **1969**, originally for **PDP-7** machines, which was initially written in assembly. By **1973**, Unix was rewritten in **C**, making it portable.

In **1978**, Intel introduced the x86 architecture, which eventually became popular on personal computers.

In **1983**, **GNU Project** was launched to create a **free, Unix-like operating system**. It needed a new assembler and adopted a **new assembly syntax** for x86 that was more consistent and easier to parse than Intel's. Also, they wanted to avoid the proprietary issues, and this created the need for a new syntax.

This new syntax, although created by GNU, was based on conventions from Unix systems — and since **Unix was synonymous with AT\&T**, this style became popular as **AT\&T syntax**.

When **Linux** was created in **1991**, it relied heavily on GNU tools like **GCC** and **GAS**, which used AT\&T syntax. As a result, **AT\&T** syntax became the _de facto_ in the Linux ecosystem.

----

## Which Syntax We Are Going To Use?

We are learning assembly, not syntaxes. The only thing that matters here is the assembler program. Because assembly programs are assembler dependent.

- Right now, if you write a hello world program in C and compile it with `gcc`, it works. You use `clang`, it works again. But that's not the case with assembly.
- If you use netwide assembler, your assembly program would be different then the person who used GNU assembler.
- This difference is based on assembler directives. Each assembler has different set of directives. So the idea remains the same, only the implementation changes.
- But the object code generated after assembling the assembly source remains the same, whether you use `nasm` or `as`. Check out the {{< doclink "7ca52ec23a2c419b8bae36efade4dae0" "C build process" >}} write up if you are feeling uneasy.

Take assemblers as different dialects of a language.
- One uses "Hi", the other uses "Hello".
- In the end, both are processed as "greeting" by the other person.

We will use GNU assembler because we are on Linux 64-bit as the GNU toolchain is readily available here. But we will write intel syntax as it is more clear and the operand style matches the mathematical style.

```
// Intel Syntax
mnemonic destination, source

// AT&T Syntax
mnemonic source, destination
```
  - Don't worry about mnemonic, we will understand them soon.

**Learn Assembly, Not Syntaxes.**

----

## Difference Between Assembly And Other Languages (C, Python.....)

### 1. Core Purpose

High level languages abstract the core functionality. Their core purpose is to provide the programmer with ease of usability and reduce development time.

Assembly, on the other hand, is completely raw. There's no abstraction. Everything is open and the programmer has to write every single instruction themselves.

This exposes the reality that even a simple "Hello, World!" program requires multiple low-level steps before it can actually run.
  - Just to prove the depth of this statement, check out the hello world series {{< doclink "243880d83f464517a201007716ffc581" "here" >}}
  - This series proves that even hello-ing the world is not simple when you account the low level angle.

Anyways, let's come back to assembly.

### 2. Platform Dependency

Languages like python are easy to download. Just grab the right installer for your OS and start coding. We don't have to worry about how CPU will understand our hand writing because that's taken care by the developer.
- Python code written on Mac works flawlesely on Windows, two completely different operating systems.

But assembly doesn't work like that. It is **architecture-dependent**. Assembly written for x86 will not work on ARM.

### 3. Control >> Convenience

Assembly gives you **maximum control**, at the cost of **convenience**.

What is convenience?

* **Pretty and verbose named variables**? Nah. You work with memory and registers directly.
* **Data types**? Everything is just bytes. It's up to **you** to interpret the bytes as intended.
* **Control flow**? Nothing is built in. You implement it using jump instructions.
* **Loops**? Jump statements.
* **I/O**? Direct syscalls. No printf/scanf.
* **Data Structures**? **Functions**? **DO. IT. YOURSELF.**

You are given all the raw material, and building anything is your responsibility.

----

## Fun Fact

C is called portable assembly.