# Functions && Stack: The Inseparable Two

_**August 15 and 16, 2025**_

***

## A Note Before Diving In

Earlier I have tried to keep them distinct. But, in the end, I found them so tightly coupled that exploring them individually makes no sense and unnecessarily complicates things further.

Therefore, we are going to explore them together.

Everyone knows stack as a data structure, the push/pop operations etc. And everyone knows what are functions. So, we are not going to repeat that theory.

## The basic idea behind stack

We know that memory is a flat-array at low level. Stack approaches that memory sequentially.

Stack as a memory management technique works exactly like a stack of plates in real life.

* The first plate is at the bottom and every other plate comes above it (_pop_).
* The last plate is the top one (\*_top_).
* When we take out plates, it happens from the top, not bottom (_pop_).

Why stack grows downward?

* _Checkout the_ [_process memory layout_](../all-roads-to-memory/general-process-layout-in-virtual-memory.md) _article. It explains it the best._

***

_**The whole addressable memory is not managed with stack. There are multiple techniques for multiple purposes.**_

## What makes something a function?

1. A function has a universe of its own, with its memory allocation and individual function calls.
2. A function can receive arguments.
3. A function has a return context.
4. A function can return values to the callee.

If something can explain functions at best, it is **code reusability**. It allows you to not repeat the code. This is what writing modular code is about, right?

***

We know that labels combined with jump statements help us achieving control flow. In case of iteration, we were able to reuse the code to some extent.

The problem with jump statements is that they are absolute in nature. There is no context for returning. If I have to return to the label which called this second label, the jump would be absolute, meaning, I would return to the start of the callee label, not where the callee label had called that second label.

This lack of context limits code reusability, which is paramount to functions.

***

Now the question is, how can we create labels such that they can emulate a function? We already know everything that makes up a function. Now the question is about finding something that can provide all of this.

* And the answer is **stack**.

## How stack qualifies for function management?

Primarily there are 2 parts to function management.

1. Managing the scope of one function.
2. Managing the scope of nested function calls.

Everyone has some experience with C. You create a `main` function and call `printf` from `stdio.h` to print `Hello, World!\n`.

* `printf` itself is a function, which uses other internal functions to perform the task it is meant to.
* Just imagine how many functions there would be? Lets say, 4, including `main` and `printf`.

We would not appreciate one function accessing the variables inside another function, right? But we want other functions to access a limited part of other functions, right? **That's the problem of scope**.

We would like to pass a function some arguments that it depends on external functions.

When we call `printf` from `main` , we would not appreciate `main` finishing before `printf`. We want it to wait, right? **That's the problem of lifecycle.**

Every function would have its own variables, which we would not appreciate to be accessible out of them. **Again, a problem of scope.**

When one function calls another function, we want the callee function to return to the caller function, so that it can know it has finished and can continue its execution. Maybe we want to return somethings to the caller function. **That's the problem of return context and return values.**

Now that we know the pain points, its time to see how stack solves these problems.

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

I hope that this was explicit and verbose enough for this who question why only stack! I hope this gives a broader overview of stack as methodology, not a data structure.

***

Now the next question would be, how functions actually exist in assembly. Let's see.

## Introducing Procedures

In simple words, a procedure is just a code symbol with jump statements and some clever usage of stack.

A procedure is a named, reusable block of code that performs a specific task, can accept input (arguments), has proper memory-management and can return a result — while managing control flow and memory context safely.

### Anatomy Of A Procedure

A procedure is composed of four core components:

1. **Header** (label) is the name of the function.
2. **Prologue** (entry setup) represents the clever use of stack.
3. **Body** represents the function body.
4. **Epilogue** (cleanup and return)

### Management Pointers

To use stack cleverly, implement stack frames and return context, we need some general purpose registers, reserved for some specific purposes in the System V ABI.

<table><thead><tr><th width="153">Pointer Register</th><th>Purpose</th></tr></thead><tbody><tr><td><code>rsp</code></td><td>Stack pointer register; holds a pointer to the top of the stack.</td></tr><tr><td><code>rbp</code></td><td>Base pointer register; holds a pointer to the start of a stack frame.</td></tr><tr><td><code>rip</code></td><td>Global instruction pointer register; holds the address of the next instruction.</td></tr></tbody></table>

### Stack Frame

A stack frame is chunk of stack that belongs to a single procedure call.

When a function calls another function, a new stack frame is created and the instruction pointer register (`rip`) is adjusted by the CPU to the instructions of that stack frame.

While the upper stack frame exists, the lower one can't execute itself. Once the upper stack frame is done with its execution and it is killed, `rip` is adjusted again to continue where it left.

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

This is how a stack frame is laid out.

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
|     (if needed)     |
*---------------------* <-- rsp
```

The first 6 arguments go in registers, we know that.

Successive frames built upon this.

### Padding

Stack pointer movement is word-aligned. It means that the stack pointer always moves in units of the machine's word size, which is 64-bit for us. Therefore, every push/pop operation adjusts `rsp` by that size, keeping the stack aligned for efficient memory access.

If you store the default integer, which is sized 4 bytes, additional padding of 4 bytes would be required so that the next thing that comes is properly aligned.

That means, allocating 1 character reserves 7 extra bytes? Yes!

* Allocating 10 character reserves 80 bytes in total? Well, yes!

***

_Its time to get my hands on something practical, otherwise I would go insane._

***

## Shorthand Operations

A call instruction calls a procedure, which is shorthand for pushing the address of next instruction (`rip`) to stack and jumping to the procedure's label, like this:

* ```nasm
  push rip
  jmp label
  ```

`push` is a shorthand for **subtract and move**. A push operation translates to:

* ```nasm
  sub rsp, 8
  mov [rsp], reg/imm
  ```

`pop` operation is a shorthand for **move and add**. A `pop` operations translates to:

* ```nasm
  mov reg, [rsp]
  add rsp, 8
  ```

To restore a stack frame, `leave` or `ret` like operations are used.

`leave` is a shorthand for:

* ```nasm
  mov rsp, rbp
  pop rbp
  ```

`ret` is a shorthand for take return address from stack and put it into `rip`:

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

You do your stuff now.

***

The epilogue is about cleanup and return.

First you call `leave` instruction, which restores the old base pointer and removes the current base pointer. Now the top of the stack (`rsp`) is pointing at the return address.

Then you call `ret` which pops the return address into `rip`. And we are back into the old stack frame.

## The Ultimate Question: Why functions In C return only one value?

I always have to use heap to return values. Why C is not like Python or JavaScript where your function can return multiple values?

I don't know! All I found was that the question is too broad to be answered.

A simple value can be returned in a register. Multiple values may require multiple registers, which would need complex ABI conventions. Although the existing ABI conventions are no simpler but that's all I have found.

We can return a complex data structure like struct though, but again, that only changes the scope of our question and to understand that, we have to understand how a complex data type like struct exists.

**For now, I am done.**

## Conclusion

And ladies and gentlemen, that's how functions and stack exist.

Now I am signing off. Hope you like it. Bye.
