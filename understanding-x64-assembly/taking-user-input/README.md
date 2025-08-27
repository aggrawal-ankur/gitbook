# Static Memory Allocation

## The Problem

We have one memory only, but how it is managed decides where the allocation will happen.

Namely, we have `.data`, `.bss`, stack and heap for memory allocation.

* From [common-terminologies.md](../common-terminologies.md "mention"), we know that `.data` is for initialized static/globals and `.bss` is for uninitialized static/globals.
* We have not explored stack and heap yet, and we don't need. Just remember that heap is used in dynamic memory allocation and stack is for static memory allocation.
* Heap is an advanced concept so we are going to avoid that for the time being.

***

The question is, who will decide where the memory is going to be allocated?

* Storage classes.

## The Solution

**Storage classes** guide the compiler to manage static memory allocation.

There are primarily 4 thing associated with a variable which are needed to managed.

1. Where in the memory the variable would be stored (**location**)?
   1. Registers?
   2. Stack?
   3. Heap?
   4. .data?
   5. .bss?
2. How long the variable should exist and be accessible (**lifetime**)?
3. Who can access that variable? And where that variable can be accessed from (**scope**)?
4. Whether the variable has a default initial value when uninitialized or it will be garbage?

<table><thead><tr><th width="129">Storage Class</th><th width="154">Scope &#x26;&#x26; Lifetime</th><th width="134">Default Value (when undeclared)</th><th width="141">Storage Location</th><th>Notes</th></tr></thead><tbody><tr><td><strong>auto</strong></td><td>The block it is declared in (local)<br><br>Until the block ends</td><td>Garbage (undefined)</td><td>Stack</td><td>Default for local variables; no need to mention explicitly.</td></tr><tr><td><strong>register</strong></td><td>The block it is declared in (local)<br><br>Until the block ends</td><td>Garbage</td><td>CPU register (if available)</td><td>Hint to store in CPU register for faster access (compiler may ignore it). Cannot take address with <code>&#x26;</code>.</td></tr><tr><td><strong>static</strong></td><td>File Scope<br><br>Until the program exists in the memory</td><td>0</td><td><code>.data</code> (if initialized)<br><br><code>.bss</code> (if uninitialized or 0 initialized)</td><td>Local static: retains value between function calls. Global static: limits scope to file (internal linkage).</td></tr><tr><td><strong>extern</strong></td><td>File/global<br><br>Until the program exists in the memory</td><td>0</td><td><code>.data</code> (if initialized)<br><br><code>.bss</code> (if uninitialized or 0 initialized)</td><td>Declares a variable that’s defined elsewhere; used for sharing globals across files.</td></tr></tbody></table>

You may ask why the default storage class stores variables on stack. What's the logic behind it?

* The answer lies in how function calls exist and managed at low level.
* In simple words, each function call gets a stack frame in the stack region for that process.
* These frames are stacked over each other. You would not appreciate a function accessing a variable defined in another function without receiving it as "function arguments".
* Those rights are enforced by stack frames and that is why the `auto` storage class or the default storage class makes the variables inside a **function call or block** stack allocated because it protects them.
* For a deep dive on functions and stack, explore [stack.md](../stack.md "mention").

***

## Way Forward

Before we get lost in the vastness of memory allocation, lets define some checkpoints.

1. Initialized and uninitialized variables.
2. Static/globals.
3. In-program declared variables and user-input managed variables.
4.









## Reading Input From The User

```
.intel_syntax noprefix

.section .bss
  buffer: .skip 100

.section .text
  .global _start

  _start:
  # Step 1: Take user-input
    mov rax, 0                  # sys_read
    mov rdi, 0                  # stdin
    lea rsi, buffer             # buffer to read into
    mov rdx, 100                # bytes to read
    syscall

  # Step 2: Display the input
    mov rdx, rax                # number of bytes read (from previous syscall)
    mov rax, 1                  # sys_write
    mov rdi, 1                  # stdout
    lea rsi, buffer             # buffer to write from
    syscall

  # Exit
    mov rax, 60         # sys_exit
    xor rdi, rdi        # status 0
    syscall

```

## Why \`stdin\` goes in \`.bss\` and not in \`.data\` section?

`.bss` section is the place for uninitialized data.

The allocation in .bss is zero-initialized at runtime. Why can't we just zero initialize the memory locations ourselves in the .data section only?

`.data` section holds static and global variables, which are already initialized. This directly affects the size of the binary.

When we allocate an array of size 100 bytes, zero-initialized in .data section, those 100 bytes are basically excess space, because they aren't used right away. We have to populate them before using.

Those 100 bytes could also have been allocated directly at runtime, reducing the size of the overall binary? This is the whole idea behind the existence of `.bss` and why stdin goes in `.bss` not `.data`.

## Reserve Space

`buffer` is a user-defined label which is reserving number of bytes for stdin.

`.skip` is a GAS directive used to reserve uninitialized space by skipping N-bytes.

## Setup Read Syscall

The accumulator (`rax`) is set for read syscall, which is 0.

The file descriptor (`rdi`) is set to 0, which is for stdin.

Now we need the runtime address of the `buffer` label in the source index register (`rsi`). To obtain this, we use `lea` instruction, which stands for _load effective address_.

Set `rdx` with the number of bytes to read (arg 3).

Invoke the syscall and read from console.

***

With that in mind, read syscall would look like: `read(fd, buffer, bytes)`

## Displaying The Input

Setup `rax` for write syscall, 1.

Set the file descriptor to 1, for stdout.

Load the buffer to write from in `rsi`.

Set the number of bytes to write in `rdx`.

* The question is, how we are going to know the length of our input?
* Because 100 is the maximum number of bytes that can be read, not necessarily the bytes we have read in total.

### How to find the number of bytes being read?

If we open the man page for `read` syscall, we can find this signature:

```c
ssize_t read(int fd, void buf[.count], size_t count);
```

If you are still unsure, lets look at the `RETURN VALUE` section.

```
On success, the number of bytes read is returned (zero indicates end of file), and the file position is advanced by this number.
```

Now it is confirmed that the number of bytes read is returned, but where? As this is a C wrapper on the actual syscall!

If you go back to the calling convention article, you can find that `rax` is where the result of a syscall is returned.

* We can also verify this by visiting the System V ABI documentation.
* Visit this GitLab repo, [x86-64 psABI](https://gitlab.com/x86-psABIs/x86-64-ABI).
* Search for "Download latest PDF" and open the link.
* Check Appendix A, AMD64 Linux Kernel Conventions on page 146.
* Point number 5 reads as: _Returning from the syscall, register %rax contains the result of the system-call. A value in the range between -4095 and -1 indicates an error, it is -errno_

That's why we are setting up rdx before setting the accumulator for write syscall.

Invoke the syscall, print to console.

Exit syscall. And we are done.

## What is `lea` and Why is `lea`?

It stands for "load effective address".

It computes the address of a memory operand and loads it into a register, but it never access the value at that memory address.

Why we haven't used `offset`?

* Remember assembly-time v/s runtime constraints? That's the reason.
* `offset` is an assembler directive. It replaces the label with a virtual address or offset. It doesn't resemble the actual runtime address of that label (symbol).
* `lea` is a CPU instruction which specializes in finding the runtime memory address of a label.

Lets talk about an undefined behavior here.

* Right now we don't know how memory is managed, so we don't know what an offset, virtual address or anything else actually mean.
* Sometimes, just using `offset` with mov can perfectly work. But, its not guaranteed.
* This undefined behavior exists when that offset or virtual address is mapped as it is in the actual memory, which in today's world is almost impossible if you use production-grade principles.
* ASLR exists to eliminate such possibilities. ASLR stands for address space layout randomization. But we need not to know about it.
* Just keep this in mind that `offset` might work but it is not right.
