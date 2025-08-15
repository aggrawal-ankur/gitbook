# Functions In Assembly

_**August 15, 2025**_

***

## Premise

As we know that plain jump statements are too raw. **There is no return context.**

* If you try to return back to a label which called the current label, the return would be absolute.&#x20;
* Meaning, the instruction pointer will point to the start of the label, not where you have left.

This is a big problem because reusability suffers here. So, how functions are implemented then?

### What makes something a function?

A function has scope of receiving arguments from the caller.

A function has a universe of its own, with its memory allocations and function calls.

A function has return context.

A function can return something to the callee.

***

Now the question is, how can we replicate something like this?

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















