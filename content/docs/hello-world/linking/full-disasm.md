---
id: 2ad66852fa5e40f98cac9d758c95135f
title: Full Disassembly
weight: 2
---

***Originally written between late June and early July 2025***

***Polished on October 04, 2025***

---

```bash
objdump linked_elf -D -M intel
```
The output is quite shocking as it is 800 lines long.

It reveals the complete infrastructure (instruction by instruction) that runs this _hello world_ thing. The build process constructs this infrastructure, section by section.

This proves that our source code is a tiny part in the whole ecosystem.

We are not going to read it line by line. This diassembly is like a roadmap which we will use in the process to understand things better.