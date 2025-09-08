# Control Flow

_**Polished on 8 September 2025 (First written in May 2025)**_

***

## Introduction

Control flow helps in breaking the linearity of execution in assembly.

These three high level constructs in C are all implemented using jump statements.

1. **If else ladder**: if, else if and else.
2. **Iteration**: for, while and do-while loops.
3. **Switch case**.

Synopsis

1. **Unconditional jumps** are the jumps that are certain to happen. Nothing can stop them. `jmp` mnemonic is used for this.
2. **Conditional jumps** are based on a conditions. The `cmp` mnemonic helps in comparing two entities.
3. The comparison instruction affects certain **CPU Flags** which the jump statements use to make their decision of jumping.
4. The jump is made to a **code symbol**.

## Comparison

`cmp` compares two operands by subtracting the second operand from the first operand.

```asm
cmp op1, op2
=> op1 - op2
```

The result is used to set certain CPU flags. There is a special purpose register called `RFLAGS` in x64 and `EFLAGS` in x86 which holds these flags. And other architectures have similar mechanisms.

* Note: `cmp` is just one instruction that changed `RFLAGS`; there are other operations that set them as well.
* Although `RFLAGS` is a 64-bit wide register, the total CPU flags aren't 64. Most of the bits are reserved by the CPU for internal things. The most common ones include: `CF ZF OF PF AF SF TF` .

<table><thead><tr><th width="119">Flag</th><th width="97">Bit Place</th><th width="163">Meaning (Set When)</th><th width="182">How it’s Set</th><th>Assumption</th></tr></thead><tbody><tr><td><strong>CF</strong> (Carry Flag)</td><td>0</td><td>Unsigned overflow (carry/borrow out of MSB)</td><td>From final carry out of the adder/subtractor</td><td></td></tr><tr><td><strong>PF</strong> (Parity Flag)</td><td>2</td><td>Result has even parity in low 8 bits</td><td>1 if least-significant byte of result has even number of 1s</td><td></td></tr><tr><td><strong>AF</strong> (Auxiliary Carry)</td><td>4</td><td>Carry out from bit 3 → bit 4</td><td>Set if lower nibble overflowed</td><td></td></tr><tr><td><strong>ZF</strong> (Zero Flag)</td><td>6</td><td>Result is zero</td><td>Set if result == 0</td><td>Both the operands are same.</td></tr><tr><td><strong>SF</strong> (Sign Flag)</td><td>7</td><td>Sign of result (MSB)</td><td>Set to MSB of result</td><td></td></tr><tr><td><strong>OF</strong> (Overflow Flag)</td><td>11</td><td>Signed overflow occurred</td><td>Set if (carry into MSB) ≠ (carry out of MSB)</td><td></td></tr></tbody></table>

Based on these CPU flags the conditional jump statements make an assumption about the result of comparison.

***

### Unsigned Comparison

<table><thead><tr><th width="138">Instruction</th><th width="131">High-level Equivalent</th><th width="163">Meaning</th><th width="119">Flags Tested</th><th>Condition (Flag State)</th></tr></thead><tbody><tr><td>JE / JZ</td><td><code>==</code></td><td>Jump if equal / zero</td><td>ZF</td><td>ZF = 1</td></tr><tr><td>JNE / JNZ</td><td><code>!=</code></td><td>Jump if not equal / not zero</td><td>ZF</td><td>ZF = 0</td></tr><tr><td>JB / JC / JNAE</td><td><code>&#x3C;</code></td><td>Jump if below / carry / not above or equal</td><td>CF</td><td>CF = 1</td></tr><tr><td>JAE / JNB / JNC</td><td><code>>=</code></td><td>Jump if above or equal / not below / not carry</td><td>CF</td><td>CF = 0</td></tr><tr><td>JA</td><td><code>></code></td><td>Jump if above (strictly greater, unsigned)</td><td>CF, ZF</td><td>(CF = 0) AND (ZF = 0)</td></tr><tr><td>JBE</td><td><code>&#x3C;=</code></td><td>Jump if below or equal (unsigned)</td><td>CF, ZF</td><td>(CF = 1) OR (ZF = 1)</td></tr></tbody></table>

_Since unsigned integers uses full set of bits available to store the magnitude of the value, we don't require other flags._

### Signed Comparison

<table><thead><tr><th width="118">Instruction</th><th width="132">High-level Equivalent</th><th width="171">Meaning</th><th width="123">Flags Tested</th><th>Condition (Flag State)</th></tr></thead><tbody><tr><td>JE / JZ</td><td><code>==</code></td><td>Jump if equal / zero</td><td>ZF</td><td>ZF = 1</td></tr><tr><td>JNE / JNZ</td><td><code>!=</code></td><td>Jump if not equal / not zero</td><td>ZF</td><td>ZF = 0</td></tr><tr><td>JL / JNGE</td><td><code>&#x3C;</code></td><td>Jump if less (signed)</td><td>SF, OF</td><td>SF ≠ OF</td></tr><tr><td>JGE / JNL</td><td><code>>=</code></td><td>Jump if greater or equal (signed)</td><td>SF, OF</td><td>SF = OF</td></tr><tr><td>JG / JNLE</td><td><code>></code></td><td>Jump if greater (signed)</td><td>ZF, SF, OF</td><td>(ZF = 0) AND (SF = OF)</td></tr><tr><td>JLE / JNG</td><td><code>&#x3C;=</code></td><td>Jump if less or equal (signed)</td><td>ZF, SF, OF</td><td>(ZF = 1) OR (SF ≠ OF)</td></tr></tbody></table>

***

### Which flag is set when?



CONTINUE FROM HERE



#### SF && OF Settlement

SF is set when the result is -ve.

OF is set if there was a signed overflow. This means, the result didn't fit in the signed range so it gor wrapped around.

The whole SF and OF conflict arises from how ranges work.

Lets take al. al is 8-bit wide. Meaning, al can contain a total of 256 combinations. In unsigned range, they are from 0-255. In signed range, they are from \[-128, +127]

Lets do some calculations.

* 100 + 25 = 125 and 125 is in \[-128, +127]. No problem!
* 100 - 109 = -9 and -9 is in \[-128, +127]. No problem again!
* 20 + 109 = 129 and 129 doesn't comes in \[-128, +127]. That's a problem.
* 127 is represented as 01111111
* To represent 129, we need 1 extra bit, but that is reserved for -ve numbers. In such a case, 129 will overwrapped to -127.
* What's the final result of last computation? -127.
* It is negative so sign flag (SF) must be set to 1.
* It also overflowed and got wrapped, so overflow (OF) flag must also be 1.

But this is all for the computer. Real mathematics doesn't work like that. 20 + 109 will give "+129" not "-127"

Therefore, SF is set wrong. But OF is set right.

Take another example: -80 - 70 = -150

* Again, -150 doesn't belong to 8-bit range. Therefore, it will be overwrapped to +105
* Result = +105
* SF = 0. OF = 1
* Again, this is not how normal mathematics would go.

If you notice, in both the cases, OF came to rescue. It ensured that reality must be preserved.

And this is what SF and OF conflict is about. When the result overwraps, the value that came after is treated as the final result, which is mathematically wrong. And this will bring chaos to calculations. OF is set so that this chaos can be managed.

Lets examine some cases:

* Case 1: Operand 1 is greater than operand 2.
  * 120 - 119 = 1.
  * There is no overflow problem.
  * SF = OF = 0.
* Case 2: Operand 1 is lesser than operand 2.
  * 119 - 120 = -1
  * SF = 1 because of -ve result. But no overflow so OF remains 0.
* Case 3: Operand 1 is greater than or equal to operand 2.
  * 120 - 120 = 0 && 120 - 119 = 1
  * Simple. SF = OF = 0
* Case 4: Operand 1 is less than equal to operand 2.
  * 119 - 120 = -1 && 119 - 119 = 0
  * SF = 1 and OF = 0

If you notice,

* ZF is not that signifcant in examining extreme cases.
* SF counts on the final value. This certainly helps but extreme cases still get out of hand.
* OF especially counts these special (overflow) cases. And that is why it is important.

#### Conclusion

| Comparison | Jump  | Flag Logic             |
| ---------- | ----- | ---------------------- |
| `a > b`    | `jg`  | `ZF = 0` and `SF = OF` |
| `a < b`    | `jl`  | `ZF = 0` and `SF ≠ OF` |
| `a >= b`   | `jge` | `ZF = 1` and `SF = OF` |
| `a <= b`   | `jle` | `ZF = 1` and`SF ≠ OF`  |

OF flag becomes a necessity when an arithmetic operation, not just subtraction, leads to results which overflow the range.
