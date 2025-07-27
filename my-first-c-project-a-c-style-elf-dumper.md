---
hidden: true
---

# My First C Project, A C-Style ELF Dumper

Hi.&#x20;

So, we are done with static analysis of the hello world binary, although several things left but it was really exhausting and I wanted to freshen up myself. So, here we are.

## Problem Statement

As I was trying to make sense of ELF through the lens of ELF spec and the output of readlef, something was missing. I wanted a solution which dumps a c-style interpretation of the whole elf, where I can see the actual structs with those individual data types defined in the spec, having values obtained from the hello world elf binary. I found one project, named `dumpelf`. But I was not satisfied.

As I started to think about it, I saw an opportunity to create a full project here. An elf parser program that can create a c-style dump of the raw values.

I waited for the hello world to finish and now I am working on that project since 24/07/2025



















