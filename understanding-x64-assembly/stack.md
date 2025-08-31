# Functions && Stack

_**August 15 and 16, 2025**_

***

Everyone knows stack as a data structure, and functions as reusable code blocks. So we are not going to repeat that theory.

## The basic idea behind stack

We know that memory is a flat-array. Stack approaches that memory sequentially.

Stack as a memory management technique works exactly like a stack of plates.

* The first plate is at the bottom and every other plate comes above it (_push_).
* The last plate is the top one.
* When we take out plates, it happens from the top, not bottom (_pop_).

Why stack grows downward?

* _Checkout the_ [_process memory layout_](../all-roads-to-memory/virtual-memory-layout.md) _article. It explains it the best._

***

_**The whole addressable memory is not managed with stack. There are multiple techniques for multiple purposes.**_

## What makes something a function?

1. A function has its own variable declarations and nested function calls.
2. A function can receive arguments.
3. A function has a return context.
4. A function can return values to the callee.

If something can explain functions at best, it's **code reusability**.

***

We know that labels combined with jump statements help us achieve control flow.

The problem with jump statements is that they are absolute in nature.

* There is no return context.
* If I have to return to the label which called this second label, the jump would be absolute, means, I would return to the start of the callee label, not where the callee label had called that second label.

This lack of context limits code reusability, which is paramount to functions.

***

Now the question is, how can we create labels such that they can emulate a function?

* And the answer is **stack**.

## How stack qualifies for function management?

Primarily there are 2 parts to function management.

1. Managing the scope of a function.
2. Managing the scope of nested function calls.

Everyone has some experience with C. You create a `main` function and call `printf` from `stdio.h` to print `Hello, World!\n`.

* `printf` itself is a function, which uses other internal functions to perform the task it is meant to.

We would not appreciate one function accessing the variables declared inside another function, right? But we want other functions to access a limited part of other functions, right? **That's the problem of scope**.

We would like to pass a function some arguments that it depends on external functions.

When we call `printf` from `main` , we would not appreciate `main` finishing before `printf`. We want it to wait, right? **That's the problem of lifecycle.**

Every function has its own variable declarations, which we would not appreciate to be accessible out of the function. **Again, a problem of scope.**

When one function calls another function, we want the callee function to return to the caller function, so that it can know it has finished and can continue its execution. Maybe we want to return something to the caller function. **That's the problem of return context and return values.**

### How stack fits in?

Close your eyes and imagine a stack of plates.

* The last plate, which is on the top, is always taken out first.
* When more plates come after getting washed, they come on the top of the existing stack.
* Plates can't be taken out from middle.

Isn't this the same thing we are looking to manage the order and lifecycle of function calls?

* Until the callee is not finished, caller can't execute further.

***

Close your eyes again and imagine a stack of office files, organized from high priority to low priority, each containing a number of pages.

* Each file is a case and each case has its own data collection, studies and outcomes.

Isn't this the same thing we are looking for to manage storage for individual functions?

* Each function gets its own universe where its declarations and calls reside.

***

Close your eyes one last time and imagine adding and removing plates from the stack.

Can you see stack smoothly lining up with our priorities?

* There is `main` which calls `printf`. A stack frame is created. The execution control is transferred to it.
* When `printf` is finished, the control naturally returns to `main` , without any extra managerial logic.
* When `scanf` is called, another stack frame is created. And the execution is transferred to it. And when it finishes, the control returns back `main`.
* Each stack frame is isolated, so the previous frame or the next frame can't mess with it.

***

I hope this was explicit and verbose enough and gives a broader overview of stack as a methodology, not a data structure.

***

Let's see how functions actually exist in assembly.

## Introducing Procedures

In simple words, a procedure is just a code symbol with jump statements and some clever usage of stack.

A procedure is a named, reusable block of code that performs a specific task, can accept input (arguments), has proper memory-management and returns a result.

### Anatomy Of A Procedure

A procedure is composed of four core components:

1. **Header** (label) is the name of the function.
2. **Prologue** (entry setup) represents the clever use of stack.
3. **Body** represents the function body.
4. **Epilogue** (cleanup and return)

### Management Pointers

The clever use of stack is about implementing stack frames and return context, which requires some general purpose registers, reserved for some specific purposes in the System V ABI.

<table><thead><tr><th width="153">Pointer Register</th><th>Purpose</th></tr></thead><tbody><tr><td><code>rsp</code></td><td>Stack pointer register; holds a pointer to the top of the stack.</td></tr><tr><td><code>rbp</code></td><td>Base pointer register; holds a pointer to the start of a stack frame.</td></tr><tr><td><code>rip</code></td><td>Global instruction pointer register; holds the address of the next instruction.</td></tr></tbody></table>

### Stack Frame

A stack frame is chunk of stack that belongs to a single procedure call.

When a function calls another function, a new stack frame is created and the instruction pointer register (`rip`) is adjusted by the CPU to point to the instructions in the new procedure.

While the upper stack frame exists, the lower one can't execute itself. Once the upper stack frame is done with its execution and it is killed, `rip` is adjusted again to continue where it has left.

***

### How is a stack frame structured?

Lets revise how user space memory is laid out.

```
  User Space Memory Layout
*--------------------------*
|  High Memory (~128 TiB)  |
|  *--------------*        |
|  |   Stack (↓)  |        |
|  *--------------*        |
|  |  Free Space  |        |
|  *--------------*        |
|  |   Heap (↑)   |        |
|  *--------------*        |
|  |     Data     |        |
|  *--------------*        |
|  |     Code     |        |
|  *--------------*        |
|  Low Memory (0..0)       |
*--------------------------*
```

***

This is the general layout of a stack frame.

```
*---------------------*
| Function Arugments  | <-- [rbp+16], [rbp+24], ....
|     (beyond 6)      |
*---------------------*
|   Return Address    |
| (next ins in prev.) | <-- [rbp+8]
*---------------------*
| Old Base Ptr Saved  | <-- [rbp]: old base pointer && <-- rbp: new base pointer
*---------------------*
|   Local Variables   | <-- [rbp-8], [rbp-16], ....
*---------------------*
|     Empty Space     |
|   (for alignment)   |
|     (as needed)     |
*---------------------* <-- rsp
```

The first 6 arguments go in registers, we know that.

Successive frames built upon this.

### Padding

Stack pointer movement is word-aligned. It means, the stack pointer always moves in units of the machine's word size, which is 64-bit for us.

But, there are some special instructions (`SIMD`) which require the stack to be 16-bytes aligned.

Before `call`, `rsp` is 16-bytes aligned. After the return address is pushed to the stack, it becomes 8-bytes aligned. Next we push `rbp` on stack, which makes it 16-bytes aligned again.

The total allocation on stack has to be 16-bytes aligned as well. As long as it is true, no padding is required. If not, extra space is calculated and saved.

If 100 bytes of locals were required, 112 bytes are actually reserved. The 12 bytes are for 16-bytes alignment. And this is perfectly possible as we know the size of total allocation already.

***

There are leaf functions which are functions which don't call any other functions inside them. For leaf functions, a concept called **red zone** exists in x64 System V ABI.

* Red zone is a small area of memory on the stack that a function can use for temporary storage without explicitly moving the stack pointer.
* The red zone is 128 bytes immediately below `rsp` (the stack pointer) at function entry.
* The red zone is guaranteed safe, nothing will write there unexpectedly.

***

## Shorthand Operations

A call instruction calls a procedure, which is shorthand for pushing the address of next instruction (`rip`) to stack and jumping to the procedure's label, like this:

* ```nasm
  push rip
  jmp label
  ```

`push` is a shorthand for:

* ```nasm
  sub rsp, 8
  mov [rsp], reg/imm
  ```

`pop` is a shorthand for:

* ```nasm
  mov reg, [rsp]
  add rsp, 8
  ```

`leave` restores the previous stack frame, which is a shorthand for:

* ```nasm
  mov rsp, rbp
  pop rbp
  ```

`ret` is a shorthand to take the return address from stack and put it into `rip`:

* ```nasm
  pop rip
  ```

## How procedures are set up?

The prologue is about saving the base pointer for the previous stack frame and create a new base pointer for another stack frame.

* ```nasm
  push rbp
  mov rbp, rsp
  ```
* Lets stop for a while and understand this operation.
* A push operation subtracts 8 bytes and stores the old base pointer there. It doesn't move `rsp` further.
* After the old base pointer is saved, the current value of stack pointer is moved into `rbp`, which acts as the base pointer for new stack frame.
* Suppose `rsp` is pointing at `4000`. After subtracting 8 bytes, it becomes `3992`. You dereference `3992`, you get old base pointer. And `3992` itself becomes the new base pointer. This is it.

***

Function body.

***

The epilogue is about cleanup and return.

First you call `leave` instruction, which restores the old base pointer and removes the current base pointer. Now the top of the stack (`rsp`) is pointing at the return address.

Then you call `ret` which pops the return address into `rip`. And we are back into the old stack frame or old function context.

### And what about return value?

As per the ABI conventions, the return goes in the accumulator (`rax`).

When you write raw assembly, you can technically return multiple things as long as you keep ABI rules in mind. When you are writing in C, only one return value is allowed.

## The Ultimate Question: Why functions In C return only one value?

I always have to use heap to return values. Why C is not like Python or JavaScript where your function can return multiple values?

A simple value can be returned in a register. Multiple values require multiple registers, which would need complex ABI rules. Although the existing ABI conventions are no simpler but that's all I have found.

Although we can return a complex data structure like `struct`, but again, that only changes the scope of our question.

***

**For now, I am done. I hope you like it.**

Now I am signing off. Bye.
