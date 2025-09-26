---
title: Hello, World!
weight: 7
---

How To Print "Hello, World!" ?

* **Step 1:** Store the hello world string somewhere in the memory.
* **Step 2:** Prepare a write syscall.
* **Step 3:** Invoke the syscall.
* **Step 4:** Prepare an exit syscall.
* **Step 5:** Invoke the syscall.

The assembly code for hello world looks like:

```asm
.intel_syntax noprefix

.section .data
  msg: .ascii "Hello, world!\n"
  len = . - msg

.section .text
  .global _start

_start:
  mov rax, 1              # syscall number for write (1)
  mov rdi, 1              # file descriptor (stdout)
  mov rsi, offset msg     # pointer to the buffer to print
  mov rdx, len            # buffer length
  syscall                 # invoke kernel

  # Exit syscall
  mov rax, 60         # syscall number for exit (60)
  xor rdi, rdi        # exit code 0
  syscall

```

**Note: Indentation makes no sense in assembly, but I have write it for visual clarity.**

Lets explore this line by line.

## Line 1: Assembler Directive For Syntax Clarity

Since we are writing in intel syntax but assembling it through GAS, we have to inform GAS about it.

* `.intel_syntax` tells GAS we are writing in intel syntax.
* `.no_prefix` tells GAS to strictly avoid `%` and `$` in instructions.

## Line 2: Define Data

Remember, sections are assembler directives, not something that the CPU understands. This is for the assembler to maintain clarity in asm code.

The data section keeps all the static and global initialized data variables.

`.section` marks the start of a section and `.data` tells that it is data section.

A section continues until a new section is defined. Therefore, both `msg` and `len` are part of the data section, where `msg` and `len` are **constant labels**.

**Note: Sections can be user-defined as well. But they are for advance use-cases.**

## Line 3 And 4: DATA (Global And Static Variables)

```asm
msg: .ascii "Hello, world!\n"
len = . - msg
```

`msg:` is a label. It can contain anything "but we are storing a string buffer in it".

* What else can it contain? A future topic.

`len` is a assembly-time constant. It calculates and contains the length of the buffer. It does this using the `.` directive in GAS.

* The `.` directive represents the current address in memory, where current address is defined as how much the assembler has moved in the memory.
* When we created a label `msg`, memory started to get occupied. Once that is done, we came on `len`.
* Now the pointer is just after where the buffer finished. This is what the `.` directive "**in GAS**" represents.
* And the `msg` label is a pointer to the start of the "hello world" buffer.
* Subtracting the two gives us the effective length of the "hello world!" buffer.

Data section completed.

## The Instructions Section

`.section .text` marks the start of text section. This section contains the instructions to the CPU. Basically, here goes the actual code.

`.global` is used to declare a symbol as globally accessible. Here, globally accessible means accessibility outside of the current file.

* Again, an assembler directive, allowing a symbol to be accessed in other files or modules during the linking process.

If you remove it, the code will still work. But it is important when there are multiple files.

* Example, a C project might have multiple source files combined to generate one binary. There it becomes important.

`_start` is the memory location (a label) where the execution starts from. Same as main() in C.

* It is called by the OS. It is the entry-point label.

`.global _start` makes `_start` globally accessible.

**Note**: `_start` is just another label. But this is what everyone has mutually agreed upon. Thus, assemblers look for it. We can define our own label and tell the linker to use it as well.

## Syscall Setup

`mov rax, 1`

* By convention, `rax` is used to specify the system call number.
* 1 identifies the "write" system call.

`move rdi, 1` sets the file descriptor to 1, which is used for standard output. This ensures that we see "hello world!\n" in the terminal.

`mov rsi, offset msg` sets `rsi` to hold the pointer to the message buffer.

* `offset` is a GAS directive.

`mov rdx, len` sets the length of the buffer in `rdx`.

`syscall`, invoke the syscall.

### The `write` Syscall

```
write(fd=rdi, buffer=rsi, buffer_len=rdx)`
```

The write syscall is used to output data to a file descriptor.

It takes 3 arguments which are passed through registers.

**Argument 1**: File descriptor.

* This defines where to write or where the output would go.
* It goes in the `rdi` register.
* 0 for `stdin`.
* 1 for `stdout`.
* 2 for `stderr`.

**Argument 2**: Pointer to the buffer that contains the data to be written.

* This defines where is the item that has to be written.
* This goes in `rsi` register.

**Argument 3**: Length of the buffer.

* This defines the number of bytes to write.
* This goes in the `rdx` register.

## Exit Syscall

`mov rax, 60` sets the register for the next syscall, which is exit.

`xor rdi, rdi` sets `rdi` to 0 using a bitwise XOR (which is faster than `mov rdi, 0`). This sets the exit code to zero.

`syscall`, invoke the syscall.

Done.

## Fun Thing

A hello world program written in C won't translate to such an assembly. That's a complete rabbit hole but the reason is that it uses C runtime for setup and cleanup, which makes the assembly slightly different.

I have explored it in depth [here](../../understanding-hello-world/). But it is lengthy and takes time, so I would suggest not to explore that now.
