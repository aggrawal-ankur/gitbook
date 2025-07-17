# Why main Function Shouldn't Be Of Type \`void\` ?

## Back Story

I got my first laptop in June 2020. I started my coding journey from 19 December 2020. The first language I learned was `C`. Right now, it is June 2025.

All the lectures used the `void main();` signature for the main function. That time, I was in school.

Even when I entered college, all the C programs used to have the `void main();` signature.

As I started my low level journey, in May 2025, because I want to learn reverse engineering, I decided to start with x64 assembly. After that I started reverse engineering.&#x20;

Since reverse engineering is a niche field, there were very few dedicated resources. Most of the resources aren't even named "for reverse engineering" and now I know why. Plus, I don't like shallow learning. I like to operate at depth, no matter how chaotic it gets. And that's how I decided that I am going to carve my way out.

I decided to write simple C programs myself and analyze them with the help of Chat GPT and various documentations available on internet, which aren't necessarily about reverse engineering but are about low level engineering.&#x20;

In that pursuit, the first program I decided to analyze was "**Hello, World!\n**". And I have written it as I was used to:

{% code title="hello.c" %}
```c
#include <stdio.h>

void main(){
  printf("Hello, World!\n");
}
```
{% endcode %}

But when I started analyzing it, I found out that `void` signature for main function is not valid. And I was shocked.

## Why \`void main();\` Is Technically Incorrect?

Before I started reverse engineering C programs, I had also learned about processes in x86\_64 Linux.

There I understood why every process **must** return an exit code. Although there can be many reasons for this, but the most easily comprehensible include

* how the OS will know that a process is finished?, or
* how the OS will know if an error occurred and the process can no longer execute?

All in all, the operating system is the one that manages all these processes and it needs something to manage the state of processes.

`void` data type returns nothing. If I used `void main();` signature, I am returning nothing, which is a violation of how processes actually work in Linux.

If you look at **ISO C standard**, it clearly defines that the `main` function must be of type `int` and should return an integer value, which is considered the exit status.

* [Here is that document.](../)
* Open page 9 in the PDF or, search for "Program startup". It is located at "5.1.2.2.1" section.
*   The two valid signatures for `main` function are:\


    ```c
    int main(void);
    int main(int argc, char *argv[]);
    // Both returns 0 by default, if nothing else is mentioned.
    ```

Great. All that is very logical. But their are some questions.

* Why does `void main();` work despite being incorrect?
* Why C tutorials use this signature? C++ raises an error during compile time, `error: '::main' must return 'int'` .

## If That's Wrong, Why It Works?

In simple words, there is no guarantee it will work.

* It is a case of **undefined behavior**. And the problem with undefined behavior is that it maybe what you expect or what you may not.
* It is a compiler optimization.
* In the upcoming articles, we'll see how our source code is just a tiny part in the computer universe. There is a lot that comes before it and after it. And the system is so meticulously designed that as a by product it ends up supporting the `void main();` signature.

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
3. All the above mentioned things are largely a part of computer architecture. And you know how many people start with computer architecture. I too didn't learn it until now. Not everyone might need it as well but those who are doing serious work will someday find it.
4. It's a complex space. So, lets not blame anyone.

It is highly possible that only I don't know about this. But I thought there is nothing bad in sharing this.
