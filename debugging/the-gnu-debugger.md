---
description: We know what a debugger is, so we will skip that.
---

# The GNU Debugger

_**24 September 2025**_

***

## Starting A GDB Session

There are two ways to start gdb.

1. We provide the source (binary/core) to be debugged while starting gdb.
2. We attach a running process or provide gdb a core or even a binary after the gdb session is started.

When we do this:

```
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

<table><thead><tr><th width="188">Command</th><th>Description</th><th>Debug Information Required?</th></tr></thead><tbody><tr><td><code>break &#x3C;source_line></code></td><td>Creates a breakpoint at a memory location.</td><td>Not required strictly but works best when provided.</td></tr><tr><td><code>watch &#x3C;var></code></td><td>Creates a watchpoint at a memory location.</td><td>Not required strictly but works best when provided.</td></tr><tr><td><code>catch &#x3C;event></code></td><td>Creates a catchpoint for an event.</td><td>No</td></tr></tbody></table>

### Accessing The Source Code

<table><thead><tr><th width="196">Command</th><th width="349">Description</th><th>Debug information Required?</th></tr></thead><tbody><tr><td><code>list</code></td><td>Lists 10 lines after or around the original C source code.</td><td>Yes</td></tr><tr><td><code>disassemble &#x3C;symbol></code></td><td>Dumps the assembler code for the specified symbol.</td><td>No</td></tr><tr><td><code>disassemble /s &#x3C;sym></code></td><td>Dumps assembly along with the C source it belongs to.</td><td>Yes</td></tr></tbody></table>

### Stack Management

<table><thead><tr><th width="148">Command</th><th width="410">Description</th><th>Debug information Required?</th></tr></thead><tbody><tr><td><code>backtrace</code> or <code>bt</code></td><td>Tells which stack frame we are in.</td><td></td></tr><tr><td><code>bt full</code></td><td>The complete stack frame with arguments and values.</td><td></td></tr><tr><td><code>info frame</code></td><td>Information for the current stack frame.</td><td></td></tr><tr><td><code>info args</code></td><td>Arguments passed to this function frame.</td><td></td></tr><tr><td><code>info locals</code></td><td>Local variables on the stack frame.</td><td></td></tr><tr><td><code>info frame &#x3C;></code></td><td>Information for the selected stack frame.</td><td></td></tr><tr><td><code>up</code></td><td>To change stack frame away from <code>main</code></td><td></td></tr><tr><td><code>down</code></td><td>To change stack frame towards <code>main</code>.</td><td></td></tr></tbody></table>

### Execution State Information

**Requirement**: An inferior which has been stopped for inspection.

**Note:** All the commands here are frame-specific. When you change the current stack frame, the values will change. So remember that and save yourself headaches.

<table><thead><tr><th width="194">Command</th><th>Description</th></tr></thead><tbody><tr><td><code>info registers</code></td><td>State of registers or the selected stack frame at that instant.</td></tr><tr><td><code>info registers &#x3C;reg></code></td><td>To inspect a specific register.</td></tr><tr><td><code>info all-registers</code></td><td>State of all the registers at that instant.<br><br>Quite extensive so not required as a beginner.</td></tr><tr><td><code>info breakpoints</code></td><td>Lists all the breakpoints, catchpoints and watchpoints.</td></tr><tr><td><code>info checkpoints</code></td><td>Lists all the checkpoints.</td></tr><tr><td><code>info watchpoints</code></td><td>Lists all the watchpoints.</td></tr><tr><td><code>info files</code></td><td>All the target files gdb is debugging in this session.</td></tr><tr><td><code>info sharedlibrary</code></td><td>All the shared libraries in use.</td></tr><tr><td><code>info source</code></td><td>Information of the source binary.</td></tr><tr><td><code>info inferiors</code></td><td>GDB can debug multiple sources at once, to see all the programs loaded in the current gdb session, we use this.</td></tr></tbody></table>

### Managerial Commands

All the i-suffixed commands operate on machine instruction. Their equivalent with no `i` in them operates on C source lines.

* Therefore, the i-suffixed ones work even when there are no debug symbols, because they don't rely on them.

<table><thead><tr><th width="133">Command</th><th width="450">Description</th><th>Debug information Required?</th></tr></thead><tbody><tr><td><code>attach pid</code></td><td>Attach gdb to a running process (inferior).<br>Make sure the security policies allow it.</td><td>NA</td></tr><tr><td><code>detach pid</code></td><td>Used to detach an already attached inferior.</td><td>NA</td></tr><tr><td><code>run</code> , <code>r</code> </td><td>To start the debugee process inside gdb.<br><code>run</code> alone is not enough as it will just execute the whole binary, so we have to manually create a breakpoint before using <code>run</code>.</td><td>NA</td></tr><tr><td><code>start</code></td><td>With <code>run</code> we need to create a breakpoint manually, but <code>start</code> creates a <em>temporary breakpoint</em> at the <code>main</code> function/symbol itself and completes the execution until that break.</td><td>Yes</td></tr><tr><td><code>starti</code></td><td>Starts the inferior and stops at the first machine instruction.</td><td>No</td></tr><tr><td><code>advance &#x3C;loc></code></td><td>Continues the program up to the specified location.<br>Can be used to execute multiple instructions together.</td><td>Not required strictly.</td></tr><tr><td><code>continue</code><br><code>fg</code>, <code>c</code></td><td>Continues the debugee process after a breakpoint is debugged.</td><td>NA</td></tr><tr><td><code>next</code></td><td>Executes the next line in the C source and stop.<br>If the next line is a function call, it doesn't step into it. Instead, it executes the function completely, treating it as one-single line and displays the output.<br>[N] can be passed to step thru N lines.</td><td>Yes</td></tr><tr><td><code>step</code></td><td>Executes the next line in the C source and stop.<br>If the next line is a function call, it steps into it.<br>The function call is not treated as one-single line and leaves us inside the first instruction in that procedure so we can travel thru it ourselves.<br>[N] can be passed to step thru N lines.</td><td>Yes</td></tr><tr><td><code>nexti</code></td><td>Executes the next machine instruction.<br>If the next instruction is a function call, it doesn't step into it. Instead, it executes the function completely, treating it as one-single line and displays the output.<br>[N] can be passed to step thru N lines.</td><td>No</td></tr><tr><td><code>stepi</code></td><td>Executes the next machine instruction.<br>If the next line is a function call, it steps into it.<br>The function call is not treated as one-single line and leaves us inside the first instruction in that procedure so we can travel thru it ourselves.<br>[N] can be passed to step thru N lines.</td><td>No</td></tr><tr><td><code>finish</code></td><td>Execute the process until the selected frame returns.</td><td>NA</td></tr><tr><td><code>kill</code></td><td>Kill the inferior being debugged.</td><td>NA</td></tr></tbody></table>

This write up is already quite dense so we'll leave it as is. In the next one, we will explore gdb fully practically, no theory.

## Conclusion

I mentioned this earlier as well that GDB is very extensive. It can do so much. Therefore, understanding how gdb does all of that is quite important because it primes you for future explorations.

If you have read my previous write ups, you might remember it, but if you don't, this is for you.

_**No one is born with knowledge and understanding. You do the work and you build it. That's the recipe.**_

_**In 2025, you have a proper**_ [_**GDB manual**_](https://sourceware.org/gdb/current/onlinedocs/gdb.pdf)_**, spread across 994 pages. You have awesome reference cards. GDB itself comes with a built-in `help` .Make use of these resources.**_&#x20;

_**This is the age of AI, ask AI chatbots what is this?, why it is like this? They will help you.**_

_**That is how I have understood all of this. It's not magic, it's just work. So explore yourself, there is so much out there. The horizon expands as long as you want to see it.**_
