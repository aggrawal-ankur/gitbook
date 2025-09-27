---
title: What Powers Debuggers? — 2
weight: 3
---
_**23 September 2025**_

***

## Premise

We have a process that we want to debug/trace. We call it debugee/tracee process.

To debug a process, we have a program called debugger, which itself becomes a process upon running, which is called, debugger/tracer process.

_Note: We are going to stick to the debugger/debugee terminology._

Since we have to bypass a lot of restrictions to do debugging, all the requests of the debugger process are mediated by the kernel. The arm of the kernel that does all of it is called `ptrace`.

`ptrace` is a syscall interface that lets one process (the debugger) observe and control another process (the debugee).

## The Mental Model

There are 4 steps in the debugging model.

### 1. Triggering Event

The debugee is running fine and there is no need for a debugger to intervene. But for a debugger to intervene in a process, it needs to stop the process. To stop the debugee, the debugger needs a triggering event.

Triggering event is anything that signals the kernel to halt the execution of the debugee process.

So far, we have read about breakpoint `#BP` and single-step `#DB`. But there is more to it.

* For example: syscall entry/exit

When the kernel detects that event, it suspends the debugee process.

### 2. Notification To The Debugger

When the debugee is suspended, the debugger is notified about the activation of the event that the debugger told the kernel to stop at.

The debugger process is notified via `waitpid()`/`waitid()` that the debugee has stopped and the reason behind it.

### 3. Transfer Of Control

After notifying the debugger, the debugger process gains the ability to inspect/modify the state of the debugee process via `ptrace`. This state is often referred to as **process/execution context**.

Everything is mediated by the kernel.

### 4. Resuming The Debugee Process

When the debugger process is done with its work, it can notify the kernel about resuming the debugee process.

The debugee is now resumed by the kernel until another event triggers.

### Where do signals fit?

Suppose our process accessed an invalid memory location. A page fault occurs as there is no page mapping between the physical and virtual memory. That's basically a segfault and the kernel has to send the process a `SIGSEGV`.

When there is no debugger, the kernel directly sends the `SIGSEGV` signal to the process and the process handles it.

When there is a debugger process waiting for a segfault event, the debugee is suspended when it occurs and the debugger is notified using `waitpid()/waitid()` that "the debugee has been suspended because this event occurred".

* Since the debugee is suspended, it can't receive the signal until the debugger resumes it.

## Process Context

Process context refers to the state of a process at any given instance. Process context includes multiple things, some important ones are:

1. General purpose registers
2. Flags register
3. Segment registers (read-only)
4. Floating point registers (SSE/AVX)
5. Virtual address space (.text/.data/.bss/heap/stack)
6. Signals
7. Process metadata (pid, ppid, uid, gid)

## What can a debugger do?

Based on the process context, a debugger can inspect, modify, and control the execution flow of the debugee.

A debugger can do a lot of things, most of which might be beyond the scope of this exploration, but here are the most important ones, which a debugger does almost all the times.

### Inspecting the state of registers

General purpose registers can reveal the state of current execution context.

Calling convention like System V ABI on Linux 64-bit have syscall convention which mandates certain registers to be used in a specific way for cross-compatibility.

* Inspecting `rax` for example can tell us which syscall the debugee is preparing for.
* Inspecting `rsi`, `rdi` can tell us what are the arguments to that syscall.

Inspecting `rip` can inform about the next instruction.

`rsp` can be used to inspect local variables and overall stack state.

### Modifying registers

Flags register is great to inspect the result of various computations like `OF ZF SF PF` etc.

We also have trap flag on 8th-bit which can be modified to raise debug exception `#DB` after each instruction.

### Execution Control

A debugger needs access to the debugee’s memory to set breakpoints and modify instructions.

This temporarily bypasses normal memory protections, but all access is mediated by the kernel via ptrace.

### Event Monitoring

Breakpoints and Debug exceptions are just two events. There are multiple events like fork, execve, syscall entry/exit, which the debugger can monitor.

The kernel mediates all reads/writes, so the debugger cannot bypass protections directly.

This event monitoring is what tools like `strace` do.

## Rules For Debugging

A process can deny to be debugged.

**Only the processes with the same user ID (`UID`) can trace each other.** If you try to attach to a process owned by another user, the kernel denies it.

Root can trace any process.

Modern Linux restricts tracing even further using the Linux Security Module `YAMA`: `/proc/sys/kernel/yama/ptrace_scope`.

* `0` → trace anything allowed by UID.
* `1` → only direct parent can trace.
* `2` → no tracing allowed (even by parent).

This prevents arbitrary processes from attaching to random programs.

A child is always traceable by its parent. This is why we usually use gdb to execute the program, so that gdb can have the privilege to do debugging.

A process can voluntarily call `ptrace(PTRACE_TRACEME)` to allow its parent to debug it. If it doesn’t, a child cannot be traced unless `PTRACE_ATTACH` is used by a permitted debugger (and the kernel verifies the security policies).

***

These are some of the rules that protects `ptrace` from abuse.

## Conclusion

This is what that enables debugging.

Now we are primed to understand how the GNU Debugger works.