---
id: 959488d570f24681a3612fd5f66e670c
title: Common Terminologies
weight: 3
---

1. **Mnemonic:** The actual CPU operation.
2. **Operand:** Arguments passed to the mnemonic, which could be a register, intermediate or a memory location.
3. **Instruction:** Something the CPU can execute. It includes both the mnemonic and the operands.
4. **Immediate**: An immediate is a constant value, like `4`.
5. **Label:** A name given to a particular memory address in the code.
   * It is made up of letters, digits and underscore.
   * A label must start with a letter or underscore.
   * A label must end with a colon.
   * There are `.` prepended labels which are used to make a label available to its parent and hides from others. _Just don't think about it for now, it's a complicated thing._
   * It holds meaning for the assembler (`GAS`, in our case), not the CPU. The assembler replaces the labels with virtual addresses or offsets.
6. **Directive (or Pseudo-Instruction):** Instructions defined for the assembler program, not the CPU.
   * They begin with a period (`.`).
   * Ex: `.section` creates a section within the program.
7. **Section:** The code is divided into multiple sections to organize the memory layout.
8. **Comment:** Anything after a semi-colon (;) or hash (#) is ignored by the assembler and is a note for the programmer itself.
9. **Keyword:** In high-level languages, keywords are reserved words (like if, for, while). In assembly, the idea of keywords basically overlaps with mnemonics and directives.
10. **Symbol:** Everything is a symbol. More on this in future.