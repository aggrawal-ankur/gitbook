# Basic Introduction

## Introducing Computer Architecture

Learning assembly is not similar to learning yet another programming language. There are no high-level constructs. There is memory and instructions. That's it.

### Memory (RAM)

Imagine a room inside of a bank, full of personal-lockers. Every locker is the same.

1. Same size and color,
2. Same capacity,
3. Same access mechanism, and
4. An addressing system to uniquely identify them.

The locker can contain anything, but what identifies them commonly is **valuables**. A person can keep gold or silver items in their locker while another person can keep the photos of their family. Items are different but both of them identifies as a valuable.

Similarly, memory is a huge collection of boxes, which have common properties, like:

1. They are fixed in capacity, 1 byte (or 8-bits).
2. Each box is identified by a unique number, called **memory address**.

Just as the locker itself can't identify its contents, everything is just a valuable, the same is with memory.

* Everything is raw bytes. What defines a byte as an integer, a decimal, an emoji, an alphabet is the interpretation of that byte (or a group of bytes).
* Previously, we have read that **context** and **interpretation** is what that rules assembly. We can see it in practice here.
* A byte can be interpreted as digit, as an alphabet. When those same bytes are grouped, and interpreted, their meaning changes.
* Understanding the context we are in enables the kind of interpretation that has to be performed in order to get the right meaning out of those bytes.

### Central Processing Unit

CPU is the physical component that actually executes instructions.

While modern systems are very complex, the role of CPU is quite simple: fetch, decode, and execute instructions stored in memory. And this what a **fetch-execute** cycle is.

The CPU needs to know the instruction to be executed, for this, it has got **Program Counter**, whose purpose is to hold the memory address of the next instruction to be executed.

The CPU has the instruction now and it needs to figure-out what this instruction means. For this, the CPU has **instruction decoder**.

In our everyday life, anything we do involves movement. We are moving things from one place to other. **Locations** are one the most important things in our life. And so as with CPU.

* Every instruction uses some memory locations, where some data is stored, which is required in the instruction. Instructions themselves can be stored at a memory location.
* To fetch that data from that memory location, what comes handy is the **data bus**. It is the connection between CPU and memory.

Suppose you have to go to your best friend's house. You have picked up the keys for your bike, the cap, the scarf to protect from heat, and the sun glasses. All these things are stored somewhere in your house.

* The key is probably on the top of the fridge or in the key-holding area.
* The sun glasses are at the dressing table.
* The scarf is in the closet.
* And the cap is on the table.
* What about the address to your friend's house? Where is that? In your mind?
* If you don't go mad on me, can I ask why don't you write the address of your friend on a paper and store it your closet?
* Obviously, you are saying, "I am not mad!" Keeping the address in your mind ensures that it is accessible all the time.
* The CPU also has some highly-efficient and rapidly-accessible locations for this exact purpose. They are called **general purpose registers**. These are high-speed memory locations inside the processor itself, that takes part in the actual execution.

At last, the **Arithmetic and Logic Unit**. The data and the decoded instruction is passed here for further processing. Here, the instruction is actually executed. The computed results are placed on the data bus and sent to the appropriate location (a memory, or a register), as specified by the instruction.

And these are the core elements of the CPU.

### Fetch-Execute Cycle

1. **Fetch** – Read the instruction from memory (address held in instruction pointer).
2. **Decode** – Understand what the instruction means.
3. **Execute** – Perform the operation (move data, add, compare, etc).
4. **Store** – Write the result (often into a register or memory).
5. **Repeat** – Move to the next instruction.

And this happens billions of times.

### Registers

In addition to the memory outside of the processor, the processor itself has some special, high-speed memory locations called registers.

The primary purpose of a register is to hold the data that the CPU is actively working on. Just like the desk has a pen-holder which holds necessary pens like black and blue ball pens, a correction pen, a ruler, pencil, and a rubber. But it doesn't contain the whole stationary. We have cupboards for that.

Since registers are high-speed and are located within the processor itself, they are limited in number, for various valid reasons.

Most information is stored in the main memory, brought in the registers \[,for processing], and then put back into memory when the processing is completed.

Just like memory, registers also hold bits. It's up to you to interpret them correctly (as numbers, characters, addresses, etc.)

Mainly, there are two types of registers:

1. **General Purpose Registers**, this is where the main action happens. Addition, subtraction, multiplication, comparisons, and other operations generally use GPRs. They are expansive and are very less in number. There are 16 GPRs in x86\_64 (amd64 or 64-bit) architecture.
2. **Special Purpose Registers**, self-explanatory?

### Size/Width Of A Register

The size or the width of the register depends on the architecture.

"Word" is the fundamental unit of CPU. Just like m/s is for velocity.

* The word is the size of the registers in a particular CPU architecture.
* For example: 32-bit systems has a word size of 32-bits or 4-bytes.

Word size is the size of the data, or the number of bits the CPU can process at once.

### Wait, What Is This 32-bit && 64-bit?

We download software. If that's a technical software, it is always mentioned whether you are at 32-bit or 64-bit OS. And there are different software for both.

Most modern systems are based on 64-bit architecture.

This 32-bit and 64-bit tells us how many numbers the CPU is capable of dealing at once.

* A 32-bit CPU can work with numbers that are 32 bits long.
* A 64-bit CPU can work with numbers that are 64-bits long.
