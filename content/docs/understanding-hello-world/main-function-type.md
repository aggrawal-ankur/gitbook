---
title: Why main Function Shouldn't Be Of Type void ?
weight: 4
---

```c {filename="hello.c"}
#include <stdio.h>

void main(){
  printf("Hello, World!\n");
}
```

But when I started analyzing it, I found out that `void` signature for main function is not valid. And I was shocked.

Before I started this journey, I have explored processes in x86\_64 Linux.

There I understood why every process **must** return an exit code. Although there can be many reasons for this, but the most easily comprehensible ones are:

* how the OS will know that a process is finished?, or
* how the OS will know if an error occurred and the process can no longer execute?

All in all, the operating system is the one that manages all these processes and it needs something to manage the state of processes.

`void` data type returns nothing. If I used `void main();` signature, I am returning nothing, which is a violation of how processes actually work in Linux.

If you look at **ISO C standard**, it clearly defines that the `main` function must be of type `int` and should return an integer value, which is considered the exit status.

* [Here is that document.](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n2310.pdf)
* Open page 24 in the PDF or, search for "Program startup". It is located at "5.1.2.2.1" section.
*   The two valid signatures for `main` function are:\


    ```c
    int main(void);
    int main(int argc, char *argv[]);
    // Both returns 0 by default, if nothing else is mentioned.
    ```

Then why does `void main();` work despite being incorrect? Why old C tutorials use this signature?

* C++ raises an error during compile time, `error: '::main' must return 'int'` .

## If That's Wrong, Why It Works?

In simple words, there is no guarantee it will work.

* It is a case of **undefined behavior**. And the problem with undefined behavior is that it maybe what you expect or what you may not.
* Compilers optimize it.

## Can this undefined behavior be tested?

Well, I am still learning about it and if I find something, I'll share.

## Why old tutorials use it?

Only those tutors can answer this. But I have a few ideas in mind.

1. Online tutorials are never really meant to understand low level engineering behind programming. They are aimed at learning to pass instructions to the computer, and high level abstractions allow that very easily. So, practically there is no need to understand this. And when someone do actual development in C, they themself find what is right and wrong.
2. Understanding low level engineering is also not easy.
   1. Why a function needs a data type?
   2. Why does a function returns?
   3. Who calls `main`?
   4. What are processes? How Linux manages processes?
   5. Why a process returns an exit code?
3. All the above mentioned things are largely a part of computer architecture. And you know how many people start with computer architecture. I too didn't learn it until now. Not everyone might need it as well but those who need it will find it.
4. It's a complex space. So, lets not blame anyone.

It is highly possible that only I don't know about this. But I thought there is nothing bad in sharing this.
