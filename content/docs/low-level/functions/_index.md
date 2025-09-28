---
title: Stack And Functions
weight: 4
---

Function and stack might seem unrelated when you work at high level. At low level, these are in a very inseparable relationship. You can't study one without other.

* If stack is an idea, function is its best implementation.
* If function is an idea, it can't exist in its best form without stack.

***

To understand their relationship, we have to move slow enough that we don't gloss over anything and fast enough that we don't dry ourselves up. Here is the progression:

1. [Introduction](stack.md) introduces to the idea of functions and stack at assembly level. Although it dives deep into theory, it will not feel like that because I have included real-life examples, interactive questions, gradual flow and introduction, ASCII art and a small "theoretical-practical" in the end.
2. [Recursion](recursion.md): introduces us to stack discipline and how stack frames are actually stacked. Here we implement the theory we have studied so far. **Fully practical.**
3. [Parameter Passing](parameter-passing.md) improves our understanding of reference and returns by one step. It lays the foundation without which you can't understand how complex value are returned. **Fully practical.**
4. [How returns are managed?](return.md) is the final boss. **Fully practical.**

***

For the time being, practical means that we are going to study an implementation of a set of concepts that feel superficial. We can definitely use `GDB` to inspect the real stack in the memory but to me, it is not the right way to understand.

* To me, the right approach is that you study the theory, you implement it on paper (in terms of loose ideas) and then you move towards ultimate practicality.
* Right now, we are exploring the first two parts in this process. But very soon we will explore the third one as well.












