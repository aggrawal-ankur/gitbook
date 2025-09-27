---
title: Control Flow
weight: 3
---

_**Polished on 8 September 2025 (First written in May 2025)**_

***

Control flow helps in breaking the linearity of execution in assembly.

These three high level constructs in C are all implemented using jump statements.

1. **If else ladder**: if, else if and else.
2. **Iteration**: for, while and do-while loops.
3. **Switch case**.

## Jump Statements

1. **Unconditional jumps** are the jumps that are certain to happen. Nothing can stop them. `jmp` mnemonic is used for this.
2. **Conditional jumps** are based on a conditions. The `cmp` mnemonic helps in comparing two entities.
3. The comparison instruction affects certain **CPU Flags** which the jump statements use to make their decision of jumping.
4. The jump is made to a **code symbol**.

## Comparison Operation

`cmp` compares two operands by subtracting the second operand from the first operand.

```asm
cmp op1, op2
=> op1 - op2
```

The result is used to set certain CPU flags. There is a special purpose register called `RFLAGS` in x64 and `EFLAGS` in x86 which holds these flags. And other architectures have similar mechanisms.

* Note: `cmp` is just one instruction that changed `RFLAGS`; there are other operations that set them as well.
* Although `RFLAGS` is a 64-bit wide register, the total CPU flags aren't 64. Most of the bits are reserved by the CPU for internal things. The most common ones include: `CF ZF OF PF AF SF TF` .


| Flag | Bit Place | Meaning (Set When) | How it’s Set | Assumption |
| :--- | :--- | :--- | :--- | :--- |
| CF(Carry Flag) | 0 | Unsigned overflow (carry/borrow out of MSB) | From final carry out of the adder/subtractor |  |
| PF(Parity Flag) | 2 | Result has even parity in low 8 bits | 1 if least-significant byte of result has even number of 1s |  |
| AF(Auxiliary Carry) | 4 | Carry out from bit 3 → bit 4 | Set if lower nibble overflowed |  |
| ZF(Zero Flag) | 6 | Result is zero | Set if result == 0 | Both the operands are same. |
| SF(Sign Flag) | 7 | Sign of result (MSB) | Set to MSB of result |  |
| OF(Overflow Flag) | 11 | Signed overflow occurred | Set if (carry into MSB) ≠ (carry out of MSB) |  |


Based on these CPU flags the conditional jump statements make an assumption about the result of comparison.

***

### Unsigned Comparison


| Instruction | High-level Equivalent | Meaning | Flags Tested | Condition (Flag State) |
| :--- | :--- | :--- | :--- | :--- |
| JE / JZ | == | Jump if equal / zero | ZF | ZF = 1 |
| JNE / JNZ | != | Jump if not equal / not zero | ZF | ZF = 0 |
| JB / JC / JNAE | < | Jump if below / carry / not above or equal | CF | CF = 1 |
| JAE / JNB / JNC | >= | Jump if above or equal / not below / not carry | CF | CF = 0 |
| JA | > | Jump if above (strictly greater, unsigned) | CF, ZF | (CF = 0) AND (ZF = 0) |
| JBE | <= | Jump if below or equal (unsigned) | CF, ZF | (CF = 1) OR (ZF = 1) |


_Since unsigned integers uses full set of bits available to store the magnitude of the value, we don't require other flags._

### Signed Comparison


| Instruction | High-level Equivalent | Meaning | Flags Tested | Condition (Flag State) |
| :--- | :--- | :--- | :--- | :--- |
| JE / JZ | == | Jump if equal / zero | ZF | ZF = 1 |
| JNE / JNZ | != | Jump if not equal / not zero | ZF | ZF = 0 |
| JL / JNGE | < | Jump if less (signed) | SF, OF | SF ≠ OF |
| JGE / JNL | >= | Jump if greater or equal (signed) | SF, OF | SF = OF |
| JG / JNLE | > | Jump if greater (signed) | ZF, SF, OF | (ZF = 0) AND (SF = OF) |
| JLE / JNG | <= | Jump if less or equal (signed) | ZF, SF, OF | (ZF = 1) OR (SF ≠ OF) |


***