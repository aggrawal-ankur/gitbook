---
description: We know what a debugger is, so we will skip that.
---

# The GNU Debugger

_**24 September 2025**_

***

## Premise

There is a lot that can be done with GDB. But using a bunch of commands and memorizing them is not my cup of tea.

There are awesome reference cards that can be found on internet, take this one: [https://users.ece.utexas.edu/\~adnan/gdb-refcard.pdf](https://users.ece.utexas.edu/~adnan/gdb-refcard.pdf) but that's not the point.

Unless I understand how GDB perceives the debugee process, I can't fathom _what is all that can be done with gdb._

That is why we are going to start with how GDB views the debugee process.

## GDB's View Of Debugee

The debugee process is divided into three parts.

### 1. Memory Image

The process is seen as a set of mapped regions in the virtual address space.

It includes all the sections we have studied in ELF specification:

1. Text
2. Data/Bss
3. Heap
4. Stack
5. Shared libraries

GDB can walk and examine each region.

### 2. Execution State

The execution state is what the CPU is doing at any point of time.

It includes the state of registers, the syscall it is preparing for, flags, instruction pointer, frame information etc.

GDB can walk thru all of that and give us an in-detail, low level overview of what's happening in the process at any instance.

_We have already explored process state in detail in the previous article, checkout_ [wpd-2.md](wpd-2.md "mention")

### 3. Debug Information

As mentioned in previous articles, debug information is semantic information which aids the debugging process. It's not necessary if you are great with raw assembly and memory addresses.

If the source was compiled with `-g` option in `gcc`, we can observe exact source lines, function names, local variables, their types etc.

This comes very handy in debugging, otherwise you'll be seeing raw memory addresses and you yourself have to resolve them into actual names as used in the program source probably.

***

This is how a debugee process is perceived by gdb. Now we have to prime ourselves with GDB 's mental model.

## GDB's Mental Model

If you run commands arbitrarily, you are not going to get anything useful. GDB expects the user to behave in a certain way so that GDB can help the user to the best of its capabilities.

To understand what gdb expects ME, or YOU, we have to understand the execution model of GDB.

### 1. Inferior

Normally, inferior means _lower in rank or quality_.

Here, an inferior is the target that gdb works on. It can be:

1. A live process started by gdb or attached later.
2. A core dump.
3. An executable file (only static information).

If you don't have an inferior, there is nothing for gdb to process.

* If you run `info registers`, gdb should give the state of registers, right?
* When there is no context, how gdb is supposed to give you the state of the registers?

That is why, an inferior is the first and foremost thing we should worry about.

The inferior must be stopped to allow meaningful inspection of the execution state.

If the source is not compiled with debug symbols, gdb can't give any semantic information about the source.

***

Although we have not studied the commands yet, but I am leaving this note. Passing the source binary name to gdb doesn't start the binary as a process.

* It just tells gdb that "this is the binary we are going to be inspecting, so execute it as a child process when I say".
* We have to run that binary before we start asking gdb about its state.

### 2. Frame

A single function activation in the **call stack**.

The current function is represented by **frame 0**. The caller function for this frame is represented by **frame 1**.

### 3. Breakpoint

A "stop here" marker.

We can set a breakpoint on a source line and an address.

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

Remember, it is possible only when the source is compiled with debug information.

### 7. Location

Location is any place you can stop the execution at. A line, an address, or a function.

Breakpoints/watchpoints are always attached to a location.

### 8. Core Dump

A memory snapshot from a crashed process.

It is used extensively in analysis purposes.

***

Now we can explore gdb commands.

## GDB Commands

GDB is very extensive. It can do a lot of things, so sticking to our purpose is very important. Otherwise, it's a recipe for time and energy wastage.

We can organize gdb commands based on category.

### Stopping The Debugee

<table><thead><tr><th width="349">Command</th><th>Description</th></tr></thead><tbody><tr><td><code>break &#x3C;source_line></code></td><td>Creates a breakpoint at a memory location.</td></tr><tr><td><code>watch &#x3C;var></code></td><td>Creates a watchpoint at a memory location.</td></tr><tr><td><code>catch &#x3C;event></code></td><td>Creates a catchpoint for an event.</td></tr></tbody></table>

### Accessing The Source Code

<table><thead><tr><th width="308">Command</th><th>Description</th></tr></thead><tbody><tr><td><code>list</code></td><td>Lists 10 lines after or around the original C source code.</td></tr><tr><td><code>disassemble &#x3C;symbol></code></td><td>Dumps the assembler code for the specified symbol.</td></tr><tr><td><code>disassemble /s &#x3C;symbol></code></td><td>Dumps assembly along with the C source it belongs to.</td></tr></tbody></table>

### Stack Management

As you already know, and if you don't, I will make you remember, _**you can't escape stack, anywhere.**_

A **frame** is one function call activation on the call stack.

Frames are numbered from 0 to n.

The frame at which the execution is halted right now is **frame 0**.

The frame which called the **frame 0** is **frame 1**. And so on.... up to the bottom of the stack, which is usually `main` or `_start`.

<table><thead><tr><th width="307">Command</th><th>Description</th></tr></thead><tbody><tr><td><code>backtrace</code> or <code>bt</code></td><td>Tells which stack frame we are in.</td></tr><tr><td><code>bt full</code></td><td>The complete stack frame with arguments and values.</td></tr><tr><td><code>info frame</code></td><td>Information for the current stack frame.</td></tr><tr><td><code>info args</code></td><td>Arguments passed to this function frame.</td></tr><tr><td><code>info locals</code></td><td>Local variables on the stack frame.</td></tr><tr><td><code>info frame &#x3C;></code></td><td>Information for the selected stack frame.</td></tr><tr><td><code>up</code></td><td>To change stack frame away from <code>main</code></td></tr><tr><td><code>down</code></td><td>To change stack frame towards <code>main</code>.</td></tr></tbody></table>

### Execution State Information

**Requirement**: An inferior which has been stopped for inspection.

**Note:** All the commands are applicable to the current stack frame. When you mess with the current stack frame, the values will change. So remember that and save headaches.

<table><thead><tr><th width="242">Command</th><th width="501">Description</th></tr></thead><tbody><tr><td><code>info registers</code></td><td>State of registers or the selected stack frame at that point of time.</td></tr><tr><td><code>info registers &#x3C;reg></code></td><td>To inspect a specific register.</td></tr><tr><td><code>info all-registers</code></td><td>State of all the registers at that point of time.<br><br>Quite extensive so not required as a beginner.</td></tr><tr><td><code>info breakpoints</code></td><td>Lists all the breakpoints, catchpoints and watchpoints.</td></tr><tr><td><code>info checkpoints</code></td><td>Lists all the checkpoints.</td></tr><tr><td><code>info watchpoints</code></td><td>Lists all the watchpoints.</td></tr><tr><td><code>info files</code></td><td>All the target files gdb is debugging in this session.</td></tr><tr><td><code>info sharedlibrary</code></td><td>All the shared libraries in use.</td></tr><tr><td><code>info source</code></td><td>Information of the source binary.</td></tr><tr><td><code>info inferiors</code></td><td>GDB can debug multiple sources at once, to see all the programs loaded in the current gdb session, we use this.</td></tr></tbody></table>

