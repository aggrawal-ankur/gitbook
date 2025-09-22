# The Mechanics Of Debugging

_**21 September 2025**_

***

The most popular debugger for us is the GNU Debugger or gdb. There are two way to learn it.

1. You pick a crash course that teaches it ASAP.
2. You learn debugging as a concept and understand how gdb implements it.

***

As you have guessed right, we are going for the second method.&#x20;

And I have two reasons for this decision

1. My consciousness and learning methodology will not allow me to even open gdb, let alone memorizing the commands. Unless I understand the WH-family behind it and it no longer feels black magic, I can't do anything. But that's a personal reason and you can skip that.
2. GDB is just one debugger. There are plenty more. The current landscape is such that you have to be proficient in multiple toolchains, and there are two ways to do it. One is sustainable, the other is not. The first one is memorizing and don't give a damn about anything, the quickest way. The second way is to understand the underlying machinery thru foundational concepts, which is a **transferable skill**, which means that no matter which system, which architecture you are in, the rules are gonna be largely the same. The more you can prioritize on **transferable skills**, the more you are consciously choosing to pay upfront to avoid chaos later.

***

We will start our journey with [GNU Debugger Manual](https://sourceware.org/gdb/current/onlinedocs/gdb.pdf).
