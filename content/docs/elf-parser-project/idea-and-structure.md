---
title: Idea & Structure
weight: 1
---

## Project Design

The whole project can be divided into two parts.

1. Extracting raw bytes from the ELF.
2. Interpreting those raw bytes and creating a c-style dump of it.

## Structure

```
elf_parser
└─ build-steps
   ...
   ...
└─ core_api
  └─ parser.c
  └─ parser.h
└─ dump_structure
  └─ dump.c
  └─ dump.h
  └─ mappings.c
  └─ mappings.h
└─ reference
  └─ hello_elf
  └─ hello_world.c
  └─ readelf_output
  └─ elf_spec.h
└─ main.c
```

## Few Things About The Project

1. It is not perfect.
2. I am not trying to compete with projects like `binutils` , which hosts `readelf` or `pax-utils` , which hosts `dumpelf` or any other project. It is purely to understand the elf specification not by reading docs but by implementing something myself.
3. It is verbose by design because I am not familiar with things that reduce code but at the cost of readability. I wanted something straightforward.
4. It is great for educational purposes, where beginners can read the code and understand it themselves, where things obscure to them are not used to do the thing.

## Timeline

Started on _July 24, 2025_

Finished writing core API on _July 31, 2025_

Finished writing c-style dumps on _August 02, 2025_

Starting documentation on _August 03, 2025_

**Improvements ahead.**
