---
layout:
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: false
---

# Why \`main()\` In C Can't Be \`void\` ?

## Premise

I got my first laptop in June 2020. I started my coding journey from 19 December 2020. The first language I learned was `C`. Right now, it is June 2025

All the lectures used the `void main();` signature for the main function. That time I was in school.

Even when I entered college, all the C programs used to have the `void main();` signature.

And as I started my low level journey, because I want to learn reverse engineering, I decided to write simple C programs myself and analyze them. In that pursuit, the first program I decided to analyze was "Hello, World!\n". And I have written it as I was used to:

```c
#include <stdio.h>

void main(){
  printf("Hello, World!\n");
}
```

But when I started analyzing it, with Chat GPT, I found out that `void` signature for main function is not valid. And I was shocked. And this article is exactly about this confusion.

## Why \`void main();\` Is Technically Incorrect?

Before I started reverse engineering C programs, I had learned about processes in x86\_64 Linux.

There I understood why every process **must** return an exit code. There are many reasons for this.

* How the OS will know that a process is finished?
* How the OS will know if an error occurred and the process can no longer execute?

If I used `void main();` signature, practically, I am returning nothing, which is a violation of how processes actually work in Linux.

If you look at ISO C standard, it clearly defines that the `main` function must be of type `int` and should return an integer value, which is considered the exit status.

* Here is that document, [https://www.open-std.org/jtc1/sc22/wg14/www/docs/n2310.pdf](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n2310.pdf)
* Open page 9 in the PDF or, search for "Program startup". It is located at "5.1.2.2.1" section.
*   The two valid signatures for `main` function are:\


    ```c
    int main(void);
    // or
    int main(int argc, char *argv[]){/** Code **/ return 0;};
    ```

All that is very logical. But the question is, why does `void main();` even work then?

## If That's Wrong, Why It Works?

In simple words, there is guarantee it will work.

* It is a case of undefined behavior. And the problem with undefined behavior is that it maybe what you expect or what you may not.
* It is a compiler optimization.

## Is There Any Way I Can Test It?

Well, I am still learning about it and if I find something, I'll share.

## What's The Exact Answer?

I am learning that as well. Once I find something solid, I'll share.
