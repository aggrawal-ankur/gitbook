---
id: bcc66e8c953b422480cc7f21902e3805
title: ELF Parser Project
weight: 2
---

We have discussed the ELF format in detail. Now we will write a parser that takes an ELF as input and dumps a C-style interpretation of the raw values.

The GNU project has a project named `pax-utils`, which has a utility named `dumpelf`. It works similarly. We can install it as:
```bash
sudo apt install pax-utils
```

And use dumpelf as:
```bash
dumpelf ELF_FILE
```

It is written in verbose C and can be easily understood.

The project is version controlled on [GitHub](https://github.com/aggrawal-ankur/elf-dump).

To use it,
```bash
git clone https://github.com/hi-anki/elf-dump.git

cd ./elf-dump

gcc main.c core_api/parser.c dump_structure/dump.c dump_structure/mappings.c -o elfdump

./elfdump <ELF_FILE>
```