# What Powers Debuggers? — 2

_**23 September 2025**_

***

## Premise

We have a process that we want to debug/trace. We call it debugee/tracee process.

To debug a process, we have a program called debugger, which itself becomes a process upon running, which is called, debugger/tracer process.

Since we have to bypass a lot of restrictions to do debugging, all the requests of the debugger process are mediated by the kernel. The arm of the kernel that does all of it is called `ptrace`.

`ptrace` is a syscall interface that lets one process (the tracer) observe and control another process (the tracee).

***

## The Mental Model

There are 4 steps in the debugging model.

### 1. Triggering Event

The tracee is running fine and there is no need for a debugger to intervene. But for a debugger to intervene in a process, it needs to stop the process. To stop the tracee, the debugger needs a triggering event.

Triggering event is anything that signals the kernel to halt the execution of the tracee.

So far, we have read about breakpoint `#BP` and single-step `#DB`. But there is more to it.

* For example: syscall entry/exit

When the kernel detects that event, it suspends the tracee process.

### 2. Notification To The Debugger

When the tracee is suspended, the debugger is notified about the activation of the event that the debugger told the kernel to stop at.

The tracer process is notified via `waitpid()`/`waitid()` that the tracee has stopped and why.

### 3. Transfer Of Control

After notifying the tracer, the control is transferred to the tracer/debugger process. This is where the debugger gains control over the tracee process.

The debugger can inspect/modify the state of the tracee process, often called **process/execution context**.

The inspection includes examining general purpose registers, CPU flags, memory, open file descriptors, etc....

And everything is mediated by the kernel.

### 4. Resuming Tracee

When the debugger process is done with its work, it can notify the kernel about resuming the tracee process.

The tracee is now resumed and the control is given back to the kernel until another event triggers.

### Where do signals fit?

Suppose our process accessed an invalid memory location. A page fault occurs as there is no page mapping between the physical and virtual memory. That's basically a segfault and the kernel has to send the process a `SIGSEGV`.

When there is no debugger, the kernel directly sends the `SIGSEGV` signal to the process and the process handles it.

When there is a debugger process listening for a segfault, the segfault is the event here. When that even is triggered, the tracee is suspended and the tracer is notified using `waitpid()/waitid()` that "the tracee has been suspended because this event occurred".

* Since the tracee is suspended, it can't receive the signal until the debugger resumes it.







## What is all in the process context?

## What is all that the debugger can inspect?&#x20;

## How ptrace is protected against abuse?
