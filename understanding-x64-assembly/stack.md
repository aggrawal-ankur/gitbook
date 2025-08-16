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

Isn't stack the same thing we are looking for while managing the scope of function calls?

* Until the callee is not finished, caller can't execute further.

***

Close your eyes again and imagine a stack of office files, organized from high priority to low priority, each containing a number of pages.

* Each file is a case and each case has its own data collection, studies and outcomes.

Isn't this the same thing that we are looking for while managing storage for individual functions?

* Each function has its own universe where declarations and calls reside.













## Introducing Procedures

In simple words, a procedure is just a label with a return context.

A procedure is a named, reusable block of code that performs a specific task, can accept input (arguments), has proper memory-management and can return a result — while managing control flow and memory context safely, everything that a function needs.

Basically, a procedure is a disciplined version of label.

## Anatomy Of A Procedure

A procedure is composed of four core components:

1. Procedure Header (label)
2. Prologue (entry setup)
3. Body (the actual logic)
4. Epilogue (cleanup and return)

## What are some places where stack is irreplaceable?

This section would effectively explore what the stack actually has to offer.

### Argument Management In Variable Length Functions

Functions like `printf` expect multiple arguments. Managing the state of those arguments is a pain if you don't use stack.

If you use stack, its fairly straight forward.

### Nested /Function Calls

If you want to explore how functions exist at low level, you can checkout these two articles:

1. [Broken link](broken-reference "mention")
2. [special-case-of-functions-recursion.md](special-case-of-functions-recursion.md "mention")

In simple words, a function manages a lot of things.

1. Local variables.
2. Global variables.
3. Function arguments.
4. Return context.

Managing all of this is a cakewalk with stack. It is still not easy, but provided that it is the easiest when stack is used, we can safely say stack is irreplaceable when the talk is about managing function calls.&#x20;
