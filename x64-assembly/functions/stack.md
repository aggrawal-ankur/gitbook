# Functions && Stack

_**August 15 and 16, 2025**_

_**September 3, 2025**_

***

Everyone knows stack as a data structure, and functions as reusable code blocks. So we are not going to repeat that theory.

## The basic idea behind stack

We know that memory is a flat-array. Stack approaches that memory sequentially.

Stack as a memory management technique works exactly like a stack of plates.

* The first plate is at the bottom and every other plate comes above it (_push_).
* The last plate is the top one.
* When we take out plates, it happens from the top, not bottom (_pop_).

Why stack grows downward?

* _Checkout the_ [_process memory layout_](../../all-roads-to-memory/virtual-memory-layout.md) _article. It explains it the best._

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

Everyone has some experience with C. You create `main` function and call `printf` from `stdio.h` to print `Hello, World!`.

* `printf` itself is a function, which uses other internal functions to perform the task it is meant to.

We would not appreciate one function accessing the variables declared inside another function, right? But we want functions to access a limited part of other functions.

* **That's the problem of scope**.

When we call `printf` from `main` , we would not appreciate `main` finishing before `printf`. We want it to wait.

* **That's the problem of lifecycle.**

When one function calls another function, we want the callee function to return to the caller function, so that it knows it has finished and can continue its execution. Maybe we want to return something to the caller function as well.

* **That's the problem of return context and return values.**

### How stack fits in?

Close your eyes and imagine a stack of plates.

* The last plate, which is on the top, is always taken out first.
* When more plates come after getting washed, they come on the top of the existing stack.
* Plates can't be taken out from middle.

Isn't this the same as order and lifecycle of function calls?

* Until the callee is not finished, caller can't execute further.
* Until the plate on top is not taken, the bottom ones can't be taken out.

***

Now imagine a stack of office files, organized from high priority (top) to low priority (bottom), each containing a number of pages.

* Each file has a case study and each case has its own data collection and outcomes.
* Similarly, each function gets its own universe where its declarations and nested calls reside.

***

Close your eyes one last time and imagine adding and removing plates from the stack.

Can you see stack smoothly lining up with our priorities?

* There is `main` which calls `printf`. A stack frame is created and the control is transferred to it.
* When `printf` is finished, the control naturally returns to `main` , without any extra managerial logic.
* When `scanf` is called, another stack frame is created and the control is transferred to it. And when it finishes, the control returns back `main`.
* Each stack frame is isolated, so the previous frame or the next frame can't mess with it.

***

I've deliberately kept it explicit and verbose so that we can have a broader overview of stack as a methodology, not just a data structure. I hope it was worth it.

***

Let's see how functions actually exist in assembly.

## Introducing Procedures

In simple words, a procedure is just a code symbol with jump statements and some "clever" usage of stack.

A procedure is a named, reusable block of code that performs a specific task, can accept input (arguments), has proper memory-management and returns a result.

### Anatomy Of A Procedure

A procedure is composed of four core components:

1. **Header** (label) is the name of the function.
2. **Prologue** (entry setup) represents the clever use of stack.
3. **Body** represents the function body.
4. **Epilogue** (cleanup and return)

### Management Pointers

The clever use of stack is about implementing stack frames and return context, which requires some general purpose registers, reserved for some specific purposes in the System V ABI.

<table><thead><tr><th width="153">Pointer Register</th><th>Purpose</th></tr></thead><tbody><tr><td><code>rsp</code></td><td>Stack pointer register; holds a pointer to the top of the stack.</td></tr><tr><td><code>rbp</code></td><td>Base pointer register; holds a pointer to the start of a stack frame, acts as a stable pointer as <code>rsp</code> is volatile.</td></tr><tr><td><code>rip</code></td><td>Global instruction pointer register; holds the address of the next instruction.</td></tr></tbody></table>

### Stack Frame

A stack frame is chunk of stack that belongs to a single procedure call.

When a function calls another function, a new stack frame is created and the instruction pointer register (`rip`) is adjusted by the CPU to point to the instructions in the new procedure.

While the upper stack frame exists, the lower one can't execute itself. Once the stack frame at top is done with its execution and it is killed, `rip` is adjusted again to continue where it has left.

***

### How is a stack frame structured?

Lets revise how user space memory is laid out. _For more information, checkout_ [virtual-memory-layout.md](../../all-roads-to-memory/virtual-memory-layout.md "mention")

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
| Old Base Ptr Saved  | <-- [rbp]: old base pointer && rbp: new base pointer
*---------------------*
|   Local Variables   | <-- [rbp-8], [rbp-16], ....
*---------------------*
|     Empty Space     |
|   (for alignment)   |
|    (as required)    |
*---------------------* <-- rsp
```

_The first 6 arguments go in registers, we know that. Checkout_ [calling-conventions.md](../calling-conventions.md "mention")

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

1. Call to procedure
2. Function prologue
3. Body
4. Function epilogue

### Prologue

As per System V ABI, `rsp` is guaranteed to be 16-bytes aligned.

Before calling a procedure, `rsp` is 16-bytes aligned. The `call` instruction is a shorthand for two instructions.

1. Push the return address on stack, which is basically the next instruction in the current (caller's) stack frame. This makes `rsp` misaligned by 8-bytes.
2. Jump on the procedure's header (label).

After `call` , we push the base pointer of the caller's stack frame on stack, this is used to return to the caller function. This instruction makes the `rsp` 16-bytes aligned again.

After this, we setup the base pointer for the current stack frame. This is a little confusing so we will move a little slowly here.

* A push instruction is a shorthand for "reserve 8 bytes, then populate them".
* When we push return address, the `rsp` now points to the memory where return address is stored.
* Similarly, when we push `rbp` on stack, the `rsp` now points to the memory where `rbp` is stored.
*   We have pushed `rbp` on stack but the original value of `rbp` is still in `rbp`, right? When we do:

    ```nasm
    mov rbp, rsp
    ```

    We are updating the base pointer. The new base or the stack frame starts from here.

Take this:

* If the `rsp` was `0d4000` before `call`, pushing the return address would subtract it to `0d3992`. `0d3992` stores the return address.
* When we push `rbp`, the `rsp` is subtracted by 8 again and `rbp` goes on `0d3984`. The stack also points at `0d3984` now.
* When we do `mov rbp, rsp`, `rbp` now stores `0d3984` .
* When you ask what is `0d3984`, it would be the new base pointer. When you ask what is at `0d3984`, it would be the old base pointer. I hope it is clear.

***

These two instructions form the **function prologue**.

```nasm
push rbp
mov rbp, rsp
```

***

### Body

Next comes the **function body**. It is made up of two parts.

1. Reservation on stack.
2. Everything else (instructions and static allocation).

Reservation on stack is a little tricky. This is where the concept of padding becomes important.

Stack pointer movement is word-aligned. Meaning, `rsp` always moves in units of the machine's word size, which is 64-bit for us.

But, there are some special instructions (`SIMD`) which require the stack to be 16-bytes aligned.

* _Why? Checkout_ [simd.md](../simd.md "mention"), _**but it is not required here, so you can do that later.**_

So far, the stack is aligned. But now we have to reserve space for locals.

* To keep `rsp` 16-bytes aligned, the total allocation on stack must be divisible by 16.
* As long as the total allocation on stack is 16 divisible, no padding is required. If that's not the case, the allocation is rounded up to the next 16-divisible digit.

If 100 bytes of locals were required, 112 bytes are reserved. The 12 bytes are for 16-bytes alignment.

***

There are **leaf functions** which are functions which don't call any other functions inside them. For leaf functions, a concept called **red zone** exists in x64 System V ABI.

* Red zone is a small area of memory on the stack that a function can use for temporary storage without explicitly moving the stack pointer.
* The red zone is 128 bytes immediately below the `rsp` (stack pointer).
* The red zone is guaranteed to be safe, nothing will write there unexpectedly.

***

### Epilogue

It is about cleanup and return.

```nasm
leave
ret
```

Stack does not need a deallocation process. To free the memory, we just make it inaccessible and it is quite efficient. How does that work?

* Technically, reducing `rsp` doesn't clear the memory. The values are still there.
* The point is that there are so many processes running on a machine constantly. You mark a memory inaccessible, ends the program and another process quickly overwrites the stack memory.

When we execute the `leave` instruction,

* It restores the `rsp` by moving `rbp` into it. Remember, what is `rbp` pointing at? The old base pointer.
* When we do `pop rbp` it restores the old base pointer in `rbp` by popping `rsp` , moving its value into `rbp` and adding 8-bytes to `rsp` to point at the return address.

At last we execute the `ret` instruction, which pops the return address into `rip`. And we are back into the old stack frame or old function context.

### What about return value?

As per the ABI, the return goes in the accumulator (`rax`).

When you write raw assembly, you can technically return multiple things as long as you keep ABI rules in check. But when you are writing C, only one return value is possible.

## The Ultimate Question: Why functions In C return only one value?

I always have to use heap to return values. Why C is not like Python or JavaScript where your function can return multiple values?

A simple value can be returned in a register. Multiple values require multiple registers, which would need complex ABI rules. Although the existing ABI conventions are no simpler but that's all I have found.

Although we can return a complex data structure like `struct`, but again, that changes the situation.

***

## Conclusion

This sets up the foundation for the next exploration. Now we know how functions exist at basic. From here we can study:

1. Function arguments.
2. How assembly sees function parameters. _For clarity, parameters are declared in definition and arguments are passed in actual call. Although they are treated synonymous, they aren't, at least at low level._
3. Single return value.
4. Returning a complex type (array, structure, union and pointer)
5. Recursion
6. Calling mechanisms: call by value and call by reference.

***

Always keep in mind, low level systems aren't black magic. They are complex but can be understood if approached the right way.

By the way, this article is polished multiple times, which proves that I didn't learned all this in one run, nor even in consecutive runs. Although the head offers a count of dates, you can always check the GitHub. I am mentioning this because I don't want you mistreat your overwhelm. It is genuine. I too have faced that.
