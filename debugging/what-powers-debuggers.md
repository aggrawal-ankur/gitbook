# What Powers Debuggers?

_**22 September 2025**_

***

It looks like debuggers are doing some sort of black magic, which is not the case. To remove that black magic, we have to understand what powers debuggers.

Primarily there are 2 things that power a debugging program.

1. Trap instructions, CPU flags, signals and exceptions are the basis of this **black magic**.
2. `ptrace` syscall is the dedicated API that allows a debugger to act as a sentinel being and observe another processes. It allows the debugger to make use of traps and signals to do the black magic.

But there is one more thing, **symbol and debug information**.

* This is not strictly required but this is what that makes debugging intuitive and less mentally draining. Without debug information, you'd have raw assembly and memory addresses.
* If you have no problem seeing raw assembly and memory addresses, this part is just add-on for you. But to make the process easier, debug information is a necessary part.

