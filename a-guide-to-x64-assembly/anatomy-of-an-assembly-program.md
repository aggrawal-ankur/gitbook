# Anatomy Of An Assembly Program

## Section

Sections define how the memory layout at runtime would be prepared. Common sections include:

1. `.text`, for code or instructions.
2. `.data`, for initialized.
3. `.bss`, for uninitialized, where bss stands for "Block Started by Symbol".
   * It refers to a label (symbol) that marks the start of a block of uninitialized data in memory.
   * It helps in reducing the size of the object files by leaving a note for the system to allocate x bytes at runtime for this block and zero-initialize them.
4. `.rodata`, for read-only.

## Registers (As Operands)

You might have seen some old lectures of assembly where someone might be using ax, bx, cx, dx like registers, or eax, ebx, ecx, edx and the most recent ones might be using rax, rsi, rdi etc....

We know that x86 architecture emerged from 8086 processor, which was a 16-bit processor. The two lettered registers we see belongs to the 16-bit architecture.

* These 16-bit registers also have smaller ones. They are sized 8-bits each.
* They are called high and low. For example, `ax` has `al` and `ah`.

Intel extended them to 32-bit architecture. This increased the register width and now all the registers from the previous 16-bit architecture got prefixed by an e. So, ax become eax, bx become ebx and so on. `e` stands for extended.

AMD extended it further to 64-bit architecture. The register width increased again and we get new registers prefixed with r, while retaining the existing ones. So, ax become rax, bx become rbx and so on. Along with this, we have got 8 new general purpose registers from r8-r15.

The newer systems are also backward compatible. This means that x86\_32 still supports x86 registers, x86\_64 still supports x86 and x86\_32.

* Or, in simple terms, we can address each pair of bits.
* `rax` is refers to complete 64-bits, `eax` refers to 32-bits, `ax` refers to 16-bits, `ah` refers to high 8-15 bits and `al` refers to 0-7 bits of the same register.
* [This is hard to explain in words, so here is a visual diagram](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*PSTOKsqSfpKLxrFEr2BY2Q.png).

[A complete GPR list](https://www.google.com/imgres?q=x86%2064%20rax%20register%20anatomy\&imgurl=https%3A%2F%2Fwww.researchgate.net%2Fpublication%2F342043300%2Ffigure%2Ftbl1%2FAS%3A900496000827404%401591706385889%2FThe-sixteen-x86-64-general-purpose-registers-and-their-sub-registers.png\&imgrefurl=https%3A%2F%2Fwww.researchgate.net%2Ffigure%2FThe-sixteen-x86-64-general-purpose-registers-and-their-sub-registers_tbl1_342043300\&docid=xbGBS-ISu9YcPM\&tbnid=iHb1hi27pi33ZM\&vet=12ahUKEwjtu8-Zo4yNAxW7XmwGHfwTDG4QM3oECFoQAA..i\&w=565\&h=466\&hcb=2\&ved=2ahUKEwjtu8-Zo4yNAxW7XmwGHfwTDG4QM3oECFoQAA)

* When we use rax, we are using the complete 64-bit register.
* When we use eax, we are using the lower 32-bits of the rax register.
* When we use ax, we are using the lower 16-bits of the rax register.
* When we use al, we are using the lowest 8-bits of the rax register, 0-7.
* When we use ah, we are using the 8-bits after al, 8-15.

## Data Addressing Modes

1. Immediate Mode.
   * The simplest method.
   * Here, the data to access is embedded in the instruction itself.
   * Example: `mov eax, 5 ; Move the value 5 into EAX register`
2. Register Addressing Mode.
   * The instruction contains a register to access, rather than a memory location.
3. Direct Addressing Mode.
   * The instruction contains the reference to the memory address to access.
   * Example: `mov eax, [some_address] ; Move data from memory at some_address into EAX`
4. Indexed Addressing Mode.
   * The instruction contains a memory address to access, and also specifies an index register to offset that address.
   * Example: `mov eax, [ebx + 4] ; Move data from the address in EBX + 4 into EAX`
5. Indirect Addressing Mode.
   * The instruction contains a register that contains a pointer to where the data should be accessed.
   * Example: `mov eax, [ebx] ; Move data from the address in EBX into EAX`
6. Base Pointer Addressing Mode.
   * This is similar to indirect addressing, but you also include a number called the offset to add to the register's value before using it for lookup.

***

Always leave an empty line at end of the program. This gracefully marks the end of assembly code. Otherwise, you'll get a warning by the assembler.

***

## System Calls

A **system call** is the controlled gateway between a user-space program and the kernel. It lets your code request services that require higher privileges — like writing to the screen, reading a file, or exiting the program.

### User Mode vs Kernel Mode

The CPU operates in two modes:

* **User Mode**: Restricted environment in which our code runs.
* **Kernel Mode**: Full-access mode where the operating system runs.

Our program cannot perform privileged operations directly. Instead, it uses **syscalls** to request the kernel to perform them on its behalf.

Linux supports hundreds of syscalls. Here are a few common ones:

| Purpose          | Syscall | Syscall Number |
| ---------------- | ------- | -------------- |
| Read from a file | `read`  | 0              |
| Write to a file  | `write` | 1              |
| Open a file      | `open`  | 2              |
| Map memory       | `mmap`  | 9              |
| Exit the program | `exit`  | 60             |

## Variables v/s Labels

A variable is a container to store a value. A label is a named memory location. Both are different.

A label can point to a group of instructions, a constant value, a procedure, anything. But a variable only stores some value. It can store the result of a computation, but not the instruction itself.

In simple terms, every variable is a label, but every label need not to be a variable.

The difference will become more apparent when we will understand control flow.
