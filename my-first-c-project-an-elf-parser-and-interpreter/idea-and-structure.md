# Idea & Structure

## Project Design

The whole project can be divided into two parts.

1. Extracting raw bytes from the ELF.
2. Interpreting those raw bytes and creating a c-style dump of it.

## Structure

```
elf_parser
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
