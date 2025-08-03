# My First C Project, An ELF Parser & Interpreter

Hey, what's up?

## Why This Project?&#x20;

After finishing the static analysis of the Hello World binary (with some parts still left), I needed a break. But I don't want to stop learning.

While I was studying the hello world binary, I felt something was missing: a clear, C-style view of the entire ELF structure. I wanted to see actual structs with spec-defined types, populated with values parsed directly from a real binary.

I have found a project called `pax-utils`, from GNU Project, which has a utility named `dumpelf`. And i decided that I will explore ELF spec myself by extracting raw bytes from an elf file and dump the values in a C-style format.

I began this project on **24/07/2025** with one goal in mind. I have to build a tool which can parse a Hello World ELF binary on **x86\_64**. That's it.

I used `readelf` as a reference throughout this process as it is too easy to get lost in raw bytes without a guide.

The language would be C.

Here is the project repository, [GitHub](https://github.com/hi-anki/elf-dump).
