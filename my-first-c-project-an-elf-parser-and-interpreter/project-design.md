# Project Design

## Project Design

The whole project can be divided into two parts.

1. Extracting raw bytes from the ELF.
2. Interpreting those raw bytes and creating a c-style dump of it.

I want two separate interpretations of the raw bytes.

1. With raw values, extracted as-is from the ELF.
2. Human interpretation of those raw values.

Therefore, the project can be divided into 3 sections.

1. Core API.
2. Raw C-style dump.
3. Interpreted C-style dump.

The core API would extract the raw bytes and we can use those bytes to create our interpretations.

## Structure

```
elf_parser
└─ core_api
  └─ elf_parser.c
  └─ elf_parser.h
  └─ verify_elf.c
  └─ verify_elf.h
└─ raw_interp
└─ eng_interp
└─ reference
  └─ hello_elf
  └─ hello_world.c
  └─ readelf_output
```

The project is version controlled on [GitHub](https://github.com/hi-anki/elf-dump-project).

I will document the code so that I can reinforce my understanding of it. Since this is my first C project, I will document everything other than the code, that I don't know, as well.
