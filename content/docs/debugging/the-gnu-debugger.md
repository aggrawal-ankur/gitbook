---
title: The GNU Debugger
weight: 3
---

_**24, 25 September 2025**_

***

## Starting A GDB Session

There are two ways to start gdb.

1. We provide the source (binary/core) to be debugged while starting gdb.
2. We attach a running process or provide gdb a core or even a binary after the gdb session is started.

When we do this:

```bash
$ gdb ./source-binary
```

We get a message along with a `gdb` prompt.

```
GNU gdb ......
.
.
For help, type "help".
Type "apropos word" to search for commands related to "word".

(gdb)
```

This means we are in a gdb session. But the source binary has not become a process yet.

Passing the source binary name ensures that the source binary can be run as a child process for gdb so that there are no problems on the permission side, as discussed in the previous write up [wpd-2.md](wpd-2.md "mention")

We will learn attaching to a running process later.

## Premise

There is a lot that can be done with GDB. But using a bunch of commands and memorizing them is not my cup of tea. There are awesome reference cards on the internet, take this one: [https://users.ece.utexas.edu/\~adnan/gdb-refcard.pdf](https://users.ece.utexas.edu/~adnan/gdb-refcard.pdf) but memorization is not the point.

To really understand gdb, we have to understand how gdb perceives everything, what is gdb's mental model.

## GDB's View Of The Debugee

The debugee process is divided into three parts.

### 1. Memory Image

The process is seen as a set of mapped regions in the virtual address space. It includes everything we have studied in the ELF specification: text, data/bss, heap, stack, and shared libraries (as memory mapped regions).

### 2. Execution State

The execution state is what the CPU is doing at any point in time. It includes the state of registers, the syscall it is preparing for, flags, instruction pointer, frame information etc.

GDB can walk thru all of that and give us an in-detail, low level overview of what's happening in the process at any instant.

GDB can modify the execution state as well to test how arbitrary or even precision-guided changes in the execution state drives the debugee in a different direction.

The execution state is often tied to a specific call stack. When you change the call stack, the execution state changes as well.

_We have already explored process state in detail in the previous article,_ [wpd-2.md](wpd-2.md "mention")

### 3. Debug Information

As mentioned in previous articles, debug information is semantic information which aids the debugging process. It's not necessary if you are great with raw assembly and memory addresses.

If the source was compiled with `-g` option in `gcc`, we can observe exact source lines, function names, local variables etc.

***

This is how a debugee process is perceived by gdb.

If we hurry up and run commands randomly, we are not going to get anything useful because gdb  expects us to behave in a certain way so that it can help us to the best of its capabilities.

To understand what gdb expects us, we have to map how gdb functions at high level.

## Mapping GDB

Mapping gdb is about priming ourselves with gdb's terminology.

### 1. Inferior

Normally, inferior means _lower in rank or quality_. Here, inferior refers to the debugee that gdb works on. It can be

1. A live process started by gdb or attached later.
2. A core dump.
3. An executable file (only static information).

GDB can debug multiple processes in a single session, so there can be multiple inferiors.

If you don't have an inferior, there is nothing for gdb to process.

* If you run `info registers`, gdb should give the state of the registers, but where there is no debugee process, how gdb is supposed to give the register state?

That is why, an inferior is the first thing we should provide to gdb.

The inferior must be stopped to allow meaningful inspection of the execution state.

If the source is not compiled with debug symbols, gdb can't give any semantic information about the source.

_**From now on, we will refer the debugee process as inferior.**_

### 2. Frame

A single function activation in the **call stack**. Frames are numbered from 0 to n.

```
frame 0: currently_executing()
frame 1: called the currently_executing frame
frame 2: called frame 1
.
.
```

### 3. Breakpoint

A "stop here" marker.

We can set a breakpoint on a source line and on an address.

We can set breakpoints directly or based on a condition.

* GDB processes that condition and decides when to set the breakpoint.

### 4. Watchpoint

A watchpoint observes for a change in the specified memory location and stops when the change happens.

For example - If we created a watchpoint on a variable and updated it later in the process, the moment it is updated, the execution would be halted.

### 5. Catchpoint

A catchpoint observes for an event and when that happens, the execution is halted.

GDB supports many events like exec, fork, shared libraries (load/unload), signal, syscalls (entry/exit), vfork, throw and rethrow (c++).

### 6. Source Line

It refers to a human-friendly view that maps back to machine addresses.

_Remember, it is possible only when the source is compiled with debug information._

### 7. Location

Location is any place you can stop the execution at. A line, an address, or a function.

Breakpoints/watchpoints are always attached to a location.

### 8. Core Dump

A memory snapshot from a crashed process.

It is used extensively in memory analysis.

***

Now we can explore the actual commands.

## GDB Commands

Few things before the exciting part.

1. GDB is very extensive. It can do a lot of things, so sticking to our purpose is very important. Otherwise, it's a recipe for time and energy wastage.
2. We can organize gdb commands based on some high level categories.
3. Under these "high level categories", we can further divide the commands based on their usability factor. The usability factor is simple. Some commands completely rely on debug information, other don't. Later we'll find the importance of this categorization.

### Stopping The Debugee

| Command | Description | Debug Information Required? |
| :--- | :--- | :--- |
| break <source_line> | Creates a breakpoint at a memory location. | Not required strictly but works best when provided. |
| watch <var> | Creates a watchpoint at a memory location. | Not required strictly but works best when provided. |
| catch <event> | Creates a catchpoint for an event. | No |

### Accessing The Source Code

| Command | Description | Debug information Required? |
| :--- | :--- | :--- |
| list | Lists 10 lines after or around the original C source code. | Yes |
| disassemble <symbol> | Dumps the assembler code for the specified symbol. | No |
| disassemble /s <sym> | Dumps assembly along with the C source it belongs to. | Yes |

Since GDB is a GNU software, it defaults to AT\&T syntax for assembly. But we can tell gdb to use intel syntax as well.

```bash
(gdb) set disassembly-flavor intel
```

### Stack Management

| Command | Description | Debug information Required? |
| :--- | :--- | :--- |
| backtraceorbt | Tells which stack frame we are in. |  |
| bt full | The complete stack frame with arguments and values. |  |
| info frame | Information for the current stack frame. |  |
| info args | Arguments passed to this function frame. |  |
| info locals | Local variables on the stack frame. |  |
| info frame <> | Information for the selected stack frame. |  |
| up | To change stack frame away frommain |  |
| down | To change stack frame towardsmain. |  |

### Execution State Information

**Requirement**: An inferior which has been stopped for inspection.

**Note:** All the commands here are frame-specific. When you change the current stack frame, the values will change. So remember that and save yourself headaches.

| Command | Description |
| :--- | :--- |
| info registers | State of registers or the selected stack frame at that instant. |
| info registers <reg> | To inspect a specific register. |
| info all-registers | State of all the registers at that instant.Quite extensive so not required as a beginner. |
| info breakpoints | Lists all the breakpoints, catchpoints and watchpoints. |
| info checkpoints | Lists all the checkpoints. |
| info watchpoints | Lists all the watchpoints. |
| info files | All the target files gdb is debugging in this session. |
| info sharedlibrary | All the shared libraries in use. |
| info source | Information of the source binary. |
| info inferiors | GDB can debug multiple sources at once, to see all the programs loaded in the current gdb session, we use this. |

### Managerial Commands

All the i-suffixed commands operate on machine instruction. Their equivalent with no `i` in them operates on C source lines.

* Therefore, the i-suffixed ones work even when there are no debug symbols, because they don't rely on them.

| Command | Description | Debug information Required? |
| :--- | :--- | :--- |
| attach pid | Attach gdb to a running process (inferior).Make sure the security policies allow it. | NA |
| detach pid | Used to detach an already attached inferior. | NA |
| run,r | To start the debugee process inside gdb.runalone is not enough as it will just execute the whole binary, so we have to manually create a breakpoint before usingrun. | NA |
| start | Withrunwe need to create a breakpoint manually, butstartcreates atemporary breakpointat themainfunction/symbol itself and completes the execution until that break. | Yes |
| starti | Starts the inferior and stops at the first machine instruction. | No |
| advance <loc> | Continues the program up to the specified location.Can be used to execute multiple instructions together. | Not required strictly. |
| continue, fg,c | Continues the debugee process after a breakpoint is debugged. | NA |
| next | Executes the next line in the C source and stop.If the next line is a function call, it doesn't step into it. Instead, it executes the function completely, treating it as one-single line and displays the output.[N] can be passed to step thru N lines. | Yes |
| step | Executes the next line in the C source and stop.If the next line is a function call, it steps into it.The function call is not treated as one-single line and leaves us inside the first instruction in that procedure so we can travel thru it ourselves.[N] can be passed to step thru N lines. | Yes |
| nexti | Executes the next machine instruction.If the next instruction is a function call, it doesn't step into it. Instead, it executes the function completely, treating it as one-single line and displays the output.[N] can be passed to step thru N lines. | No |
| stepi | Executes the next machine instruction.If the next line is a function call, it steps into it.The function call is not treated as one-single line and leaves us inside the first instruction in that procedure so we can travel thru it ourselves.[N] can be passed to step thru N lines. | No |
| finish | Execute the process until the selected frame returns. | NA |
| kill | Kill the inferior being debugged. | NA |

This write up is already quite dense so we'll leave it as is. In the next one, we will explore gdb fully practically, no theory.

## Conclusion

I mentioned this earlier as well that GDB is very extensive. It can do so much. Therefore, understanding how gdb does all of that is quite important because it primes you for future explorations.

If you have read my previous write ups, you might remember it, but if you don't, this is for you.

_**No one is born with knowledge and understanding. You do the work and you build it. That's the recipe.**_

_**In 2025, you have a proper**_ [_**GDB manual**_](https://sourceware.org/gdb/current/onlinedocs/gdb.pdf)_**, spread across 994 pages. You have awesome reference cards. GDB itself comes with a built-in `help` .Make use of these resources.**_

_**This is the age of AI, ask AI chatbots what is this?, why it is like this? They will help you.**_

_**That is how I have understood all of this. It's not magic, it's just work. So explore yourself, there is so much out there. The horizon expands as long as you want to see it.**_