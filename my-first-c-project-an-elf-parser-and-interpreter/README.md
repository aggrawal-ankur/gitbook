# My First C Project, An ELF Parser & Interpreter

Hey, what's up?

## Why This Project?&#x20;

After finishing the static analysis of the Hello World binary (with some parts still left), I needed a break. But I don't want to stop learning.

While I was studying the hello world binary, I felt something was missing: a clear, C-style view of the entire ELF structure. I wanted to see actual structs with spec-defined types, populated with values parsed directly from a real binary.

I found a project called `dumpelf`, but it didn’t meet my expectations.

That’s when the idea struck: build a tool that parses an ELF file and generates a C-style dump of its structure — variables defined in the ELF spec, filled with real binary values.

I began this project on **24/07/2025** with one goal in mind. I have to build a tool which can parse a Hello World ELF binary on **x86\_64**. That's it. Once that works, I’ll consider extending it.

I’ll use `readelf` as a reference throughout as it is too easy to get lost in raw bytes without a guide.

## Which Language?

I will use because everything here is present as is. There is no abstraction. Plus, it directly matches with elf type definitions.

## Resources?

The `elf.h` header file in C is a goldmine to understand ELF. It has all the type definitions and what are the possible set of values for any entry.

`gcc` in tool-chain.

VS Code as the IDE.

And internet.

That's it.
