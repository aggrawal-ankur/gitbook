# ISA & Assemblers

## ISA v/s Assemblers

There are multiple assemblers in the market. GNU assembler, Netwide assembler, fish assembler, Microsoft assembler and so on....

Assembler does one thing — translate human readable assembly instructions into machine opcodes, which the CPU can understand and execute directly.

A CPU's instruction set architecture defines its capabilities. It conceptualizes everything that the CPU can do.

Assemblers are the programs that decides how the programmers will interact with the CPU.

Take this, there are handful of firms that research on semiconductor chips, but there are relatively many who does the manufacturing. ISA is that research while assemblers are the manufacturers. Each manufacturer (assembler) has the freedom to manufacture its own way.

## Assembly-Time vs Run-Time

Assembler directives mean nothing to the CPU. They exist to streamline development. Assembler resolves them into machine understandable things while assembling the code. This is called assembly-time management. (Checkout [a-high-level-overview-of-build-process-in-c.md](../understanding-hello-world/a-high-level-overview-of-build-process-in-c.md "mention"))

There are things that are consistent across all the assemblers because the CPU directly understand them. These are runtime managed things.

For example, `OFFSET` is an assembler directive, while `lea` is a CPU understood operation, defined in the ISA itself.
