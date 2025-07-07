# Introduction To Processes In Linux

## Introduction To Processes

A process is an instance of a running program. Every time you execute a command or run a program, the Linux kernel creates a process to run it.

Every process gets a virtual address space (VAS), which is mostly made up of the program image.

* A virtual memory address (VMA) is the same as the name of a street and the physical memory address (PMA) is the actual GPS coordinates.
* Two cities can have a "main street" but their coordinates would be unique.
* Every process gets its own isolated address space, thanks to virtual memory. So your program might access 0x400000, but that doesn't mean that's the physical address.
* The OS + hardware's MMU (Memory Management Unit) maps VMA to PMA.
* Without the MMU, all processes would share the same memory space — like roommates with no walls.
  * A bug in one process could overwrite another process's memory.
  * With MMU, each process gets its own private virtual address space. It's still messy on ground level but easier for management. It's a nice abstraction.

***

## Process Hierarchy

Processes follow a tree like structure in linux.

* The first process is `init` or `systemd`, depending on the system, which is started by the kernel. It's PID is 1, and PPID is 0.
* Every process is created by another process (its parent process).
* Every process is a descendant of the `init` process.
* Processes follow a parent-child relationship. Although each process is independent in nature, and the execution of a sub-process doesn't hinder the execution of the parent process, still, the child process is linked with the parent process and it has to report its exit status.

To view the tree like structure of processes, use `pstree`.

Why does process hierarchy exists? Why can't processes be truly independent?

* To understand this, we need to understand how processes are created.

***

## Process Creation

It is a 4 step "process".

| Step | Description                                                           | Syscall  |
| ---- | --------------------------------------------------------------------- | -------- |
| 1    | Clone the current process                                             | `fork()` |
| 2    | Replaces the process image with the new program in the cloned process | `exec()` |
| 3    | Parent waits for the child to finish                                  | `wait()` |
| 4    | Process finishes and returns the status to the parent                 | `exit()` |

Each process may require other helper processes.

* For example, when I did `pstree`, I found that VS Code is not a standalone process. It has a lot of sub-processes. Like the terminal opened within VS Code comes under it, not as a fully independent process with no parent.
* The same is with Firefox and everything else.

Hierarchical structure is not just a design philosophy, but a very logical decision.

* It is a proper way to manage which process spawned which sub-process.
* We fork the calling process (parent process), keep the identifying metadata as it is and replace the old process image with the new one. This ensures that the child process has proper links to the parent process, without any hustle.

Every process is independent in its execution. But it is answerable to the parent process so that it knows if the sub-process exited successfully or it acquired any problem.

* Just like children, who are although independent but they are always answerable to their parents.

***

## Key Properties Of A Process

| Property                 | Description                                                   |
| ------------------------ | ------------------------------------------------------------- |
| PID (Process ID)         | Unique identifier of a process.                               |
| PPID (Parent Process ID) | Unique identifier of the process that created the PID process |
| UID (User ID)            | Who owns the process                                          |
| State                    | Running, sleeping, zombie etc....                             |
| Memory Info              | RAM consumption                                               |
| Executable code and data | What it’s running and working with                            |

***

## A Real Example

We are going to run an ELF binary made from this C code and see how Linux does all the magic.

```c
#include <stdio.h>
#include <unistd.h>    // sleep()

int main(void){
  printf("Hello, World!");
  sleep(400);
}
```

To get the final ELF binary:

```bash
gcc main.c -o main_elf
```

### Step1 - Call The Binary

To call or execute the binary (`main_elf`), we need a shell (or terminal).

I have opened my shell, which is zsh.

```bash
$ echo $SHELL

/usr/bin/zsh
```

`zsh` itself is a "running" process.

```zsh
$ ps
  
PID       TTY       TIME         CMD
41027     pts/0     00:00:01     zsh
49852     pts/0     00:00:00     ps
```

Run the binary in background so that we can retain the shell session.

```bash
$ ./main_elf &

[1] 52184
```

`ps` \~

```bash
$ ps                

PID       TTY       TIME         CMD
41027     pts/0     00:00:02     zsh
52184     pts/0     00:00:00     main_elf
52325     pts/0     00:00:00     ps
```

Since main\_elf is executed within zsh, zsh must be the parent of main\_elf? Lets verify this.

```bash
$ ps -T -o pid,ppid,cmd

PID     PPID    CMD
41027   40797   /usr/bin/zsh -i
59461   41027   ./main_elf
59559   41027   ps -T -o pid,ppid,cmd
```

* `-T` shows processes for the current terminal session.
* `-o` helps in custom formatting.

This proves that the `zsh` process was forked and the child process (main\_elf) born from it.

Until now, we can say that a base template for the child process is created.

* Now we have to find the evidence for the process image replacement.

***

### Step2 - Correct (Replace) The Process Image In The Child Process (Fork)

A fork is a near-clone of the parent process. But the child process is a different program than the parent. Therefore, the process image must have been changed.

`strace` is a Linux utility which helps in tracing all the syscalls a process has executed.

If we run our program with `strace`, like this:

```bash
strace ./main_elf
```

we can find a long list of output, which starts from `execve`.

What is `execve`?

* In simple words, `execve` is a syscall which executes a binary.
* In real terms, `execve` is a syscall which executes a binary passed in the `pathname` argument by replacing the process image of the current process (not the child process, the current process).
* `execve` is designed to be paired with `fork` in order to fit Linux's hierarchical process structure.
* This is the signature of the `execve` syscall, `int execve(const char *pathname, char *const _Nullable argv[], char *const _Nullable envp[]);`
  * `pathname` is the name of the binary.
  * `argv[]` is a `NULL` terminated array of arguments passed to the binary.
  * `envp[]` is a `NULL` terminated array of environment variables required in the process image.

***

What is a process image?

* Just imagine how crazy and chaotic it would get to manage millions of process inside a single RAM, with all demanding various services including stack and heap.
* This is why an abstraction known as virtual address space (VAS) exist. Every process is executed in an isolated environment called virtual address space.
* A process image is the complete in-memory layout of a program after it has been loaded into memory by the OS.
* It is the answer to the question, "What the process looks like in the RAM?" A process image is the memory representation of a program at runtime.
* It includes code, data, stack, heap, environment, memory-mapped regions, loaded libraries etc....
* It is created by the kernel during `execve()`, based on the ELF layout.

This is the whole process that `execve` syscall carries out.

The kernel opens the binary (`main_elf`) using virtual file system (VFS).

* It reads the ELF Header (first 64 bytes) to confirm that it is an ELF file, and find the `e_type`, `e_entry` and Program Headers Table (PHT) for carrying out its job.

What is VFS and Why the kernel is using it?

* It's an abstraction layer inside the Linux kernel that provides a uniform interface to access all kinds of file systems — regardless of their actual formats or physical devices.
* There exist multiple file systems, like ext4, btrfs, zfs, hfs, ntfs, fat32 and so on.... If there is no VFS, the kernel has to learn to speak in all the different file systems.
* VFS knows how to talk to different file systems and provide the kernel with a consistent interface.

The kernel loads the binary into memory by reading the PHT.

* It maps each segment defined in the PHT into memory regions using `mmap()` (memory map) syscall and sets the permissions (R, W, X) accordingly.
*   This is the PHT for our ELF:

    ```bash
    $ readelf -l main_elf

    Elf file type is DYN (Position-Independent Executable file)
    Entry point 0x1060
    There are 14 program headers, starting at offset 64

    Program Headers:
      Type           Offset             VirtAddr           PhysAddr           FileSiz            MemSiz              Flags  Align
      PHDR           0x0000000000000040 0x0000000000000040 0x0000000000000040 0x0000000000000310 0x0000000000000310  R      0x8
      INTERP         0x0000000000000394 0x0000000000000394 0x0000000000000394 0x000000000000001c 0x000000000000001c  R      0x1
                     [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
      LOAD           0x0000000000000000 0x0000000000000000 0x0000000000000000 0x0000000000000660 0x0000000000000660  R      0x1000
      LOAD           0x0000000000001000 0x0000000000001000 0x0000000000001000 0x0000000000000179 0x0000000000000179  R E    0x1000
      LOAD           0x0000000000002000 0x0000000000002000 0x0000000000002000 0x000000000000010c 0x000000000000010c  R      0x1000
      LOAD           0x0000000000002dd0 0x0000000000003dd0 0x0000000000003dd0 0x0000000000000250 0x0000000000000258  RW     0x1000
      DYNAMIC        0x0000000000002de0 0x0000000000003de0 0x0000000000003de0 0x00000000000001e0 0x00000000000001e0  RW     0x8
      NOTE           0x0000000000000350 0x0000000000000350 0x0000000000000350 0x0000000000000020 0x0000000000000020  R      0x8
      NOTE           0x0000000000000370 0x0000000000000370 0x0000000000000370 0x0000000000000024 0x0000000000000024  R      0x4
      NOTE           0x00000000000020ec 0x00000000000020ec 0x00000000000020ec 0x0000000000000020 0x0000000000000020  R      0x4
      GNU_PROPERTY   0x0000000000000350 0x0000000000000350 0x0000000000000350 0x0000000000000020 0x0000000000000020  R      0x8
      GNU_EH_FRAME   0x0000000000002014 0x0000000000002014 0x0000000000002014 0x000000000000002c 0x000000000000002c  R      0x4
      GNU_STACK      0x0000000000000000 0x0000000000000000 0x0000000000000000 0x0000000000000000 0x0000000000000000  RW     0x10
      GNU_RELRO      0x0000000000002dd0 0x0000000000003dd0 0x0000000000003dd0 0x0000000000000230 0x0000000000000230  R      0x1

    Section to Segment mapping:
      Segment Sections...
      00     
      01     .interp 
      02     .note.gnu.property .note.gnu.build-id .interp .gnu.hash .dynsym .dynstr .gnu.version .gnu.version_r .rela.dyn .rela.plt 
      03     .init .plt .plt.got .text .fini 
      04     .rodata .eh_frame_hdr .eh_frame .note.ABI-tag 
      05     .init_array .fini_array .dynamic .got .got.plt .data .bss 
      06     .dynamic 
      07     .note.gnu.property 
      08     .note.gnu.build-id 
      09     .note.ABI-tag 
      10     .note.gnu.property 
      11     .eh_frame_hdr 
      12     
      13     .init_array .fini_array .dynamic .got
    ```

**Note: It is slightly formatted so that we can see it clearly.**

Program headers table describes how the operating system should load the ELF binary into the memory. It maps parts of the binary file into memory regions with specific permissions and purposes.

A simple decode of this cryptic table is:

*   Type: PHDR

    ```
    Offset:  0x40
    VirtAddr:0x40
    Size:    0x310
    Flags:   R
    ```

    This describes where in the memory the program headers themselves are located.

    The loader reads this to get all other segment info.
*   Type: INTERP

    ```
    Offset: 0x394
    VirtAddr: 0x394
    Size: 0x1c
    Flags: R
    [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
    ```

    Specifies the dynamic linker to load and run this PIE executable.

    This linker will resolve symbols and apply relocations before main() runs.
*   Type: LOAD Segments, The actual loadable code/data in the binary

    ```bash
    # LOAD 1
    Offset: 0x0
    VirtAddr: 0x0
    FileSiz: 0x660
    Flags: R
    ```

    The R flag shows that this is a read only section, contains the initial part of ELF.

    ```bash
    # LOAD 2
    Offset: 0x1000
    VirtAddr: 0x1000
    Size:    0x179
    Flags:   R E
    ```

    This is a read + executable section. This implies that it contains the actual code segment

    ```bash
    # LOAD 3
    Offset: 0x2000
    VirtAddr: 0x2000
    Size:    0x10c
    Flags:   R
    ```

    Another readonly segment, which may contain constants and other ro-data.

    ```bash
    # LOAD 4
    Offset: 0x2dd0
    VirtAddr: 0x3dd0
    Size: File=0x250, Mem=0x258
    Flags: RW
    ```

    This section is both readable and writeable. This is where .data, .bss, etc.... are stored.
*   Type: DYNAMIC

    ```bash
    Offset: 0x2de0
    VirtAddr: 0x3de0
    Size: 0x1e0
    Flags: RW
    ```

    Contains relocations, library names, symbol tables, etc...., which are used by the dynamic linker to perform symbol resolution and relocation at runtime.
* Type: Note Segments and GNU\_PROPERTY, for metadata handling. Nothing explosive.
* Type: GNU\_EH\_FRAME, exception handling frame, used by debuggers and during crashes.
* Type: GNU\_STACK, specifies stack permissions.
* Type GNU\_RELRO, a region that is read-only after relocation.

The kernel finds the `LOAD` segments and maps them into memory.

All the offsets are relative to the location where the binary would be actually loaded.

Now our program is loaded in the memory, but we're not executing yet.

#### Handle Dynamic Linking

Since the PHT has `INTERP` header, this tells the kernel to run this interpreter `lib64/ld-linux-x86-64.so.2` before jumping to the entry point in the binary.

The kernel now loads the dynamic linker/loader (`ld-linux-x86-64.so.2`) into the memory.

The dynamic linker is the first code that will run in this process.

Now the kernel set up the stack, `rip` to `ld-linux`'s entry point and returns the control to user space.

And the child process is finally alive.

`ld-linux` now:

1. Parses the `.dynamic` section (`readelf -S main_elf`)
2. Finds the required shared libraries, like `libc.so.6`
3. Loads them into the memory using `mmap()`.
4. Applies relocations to the code.
5. Finally, jumps to our ELF binary's real entry point (not `main`, but `_start`).

#### Entry point Management && Program Execution

The dynamic linker jumps to `_start` in our binary (provided by crt1.o).

`_start` sets up the runtime.

Then it calls `__libc_start_main()`, a libc function that initializes more stuff and finally calls the `main()` .

Now the program runs.

* `printf()` is a call into `libc`.
* `sleep()` sleeps the process for 400 seconds using `nanosleep` syscall.

***

### Step3 - End Of The Program

After main() ends, control goes back to `__libc_start_main()`, which handles the final cleanup and calls `exit()`.

The kernel:

* Cleans up the process resources.
* Returns the exit code to parent (zsh).

***

## Lets Manage An Actual Process Using C

Downloadable source code of the program can be found at [https://github.com/hi-anki/process-creation-in-linux/blob/main/process.c](https://github.com/hi-anki/process-creation-in-linux/blob/main/process.c)

```c
// Standard I/O: printf() and perror()
#include <stdio.h>

// General Utils: exit()
#include <stdlib.h>

// POSIX OS API: fork(), execvp(), getpid(), getppid()
#include <unistd.h>

// Defines data types used in system calls: pid_t, the data type for process IDs
#include <sys/types.h>

// Provides macros and functions for waiting on child processes: waitpid(), WIFEXITED(), WEXITSTATUS()
#include <sys/wait.h>

int main() {
  pid_t pid;

  printf("Calling Process `p_proc`:\n");
  printf("  PPID: %d\n", getppid());
  printf("  PID : %d\n", getpid());
  printf("---------------------------\n");
  
  // 1. Process creation (fork)
  printf("Calling fork.....\n");
  pid = fork();
  
  if (pid == -1) {
    perror("fork failed");
    printf("`p_proc`: return value from fork(): %d\n", pid);
    exit(EXIT_FAILURE);
  }
  
  if (pid == 0) {
    printf("Cloned Process `c_proc`:\n");
    printf("  PPID: %d\n", getppid());
    printf("  PID : %d\n", getpid());
    printf("Return value from fork() to `c_proc`: %d\n", pid);
    printf("---------------------------\n");

    // 2. Image replacement using exec
    char *args[] = {"./main_elf", NULL};
    if (execvp(args[0], args) == -1) {
      perror("exec failed");
      exit(EXIT_FAILURE);
    }
  }

  else {
    // Parent process
    int status;
    waitpid(pid, &status, 0);  // Wait for child to finish
    
    if (WIFEXITED(status)) {
      printf("Child exited with status %d\n", WEXITSTATUS(status));
      printf("---------------------------\n");
      printf("Return value from fork(): to `p_proc` %d\n", pid);
    } else {
      printf("Child did not exit normally.\n");
    }
  }

  return 0;
}
```

Lets understand this program.

`pid_t` is a type definition, defined in`POSIX` to hold process IDs. It allows the kernel and user-space programs to use a consistent and portable data type for managing process IDs.

* The `pid` variable is very important. Understanding this small and harmless looking part is very important.
* The confusion is paired with `fork`, so we'll learn it there.

***

`fork()` function is used to clone the calling process. Tell me, where would `fork` send its return value?

* To the calling process? or, To the cloned process?
* The answer is, both. And this is where the question how the parent process maintains its state arises from.

&#x20;It returns

* `0` to the **cloned process** if the calling process is cloned successfully and the process ID of the cloned process to the calling process (which is now the parent process).
* `-1` to the **parent process**, if an error occurred and cloning didn't succeed.

Remember, `fork()` makes a near-clone of the calling process. Only certain things are different.

***

The functions `getpid()` and `getppid()` are used to obtain the child process ID and the parent process ID, respectively.

* These functions are relative to the process that has invoked them.
* This is why `getpid()` before forking the process returned the process ID of the current process, which became the parent process after forking.

***

The `exec()` family of functions replaces the current process image with a new process image. Under the hood, they all use the mighty `execve` syscall.

* The `char *argv[]` argument is an array of pointers to null-terminated strings that represent the argument list available to the new program.
* The first argument, by convention, should point to the filename associated with the file being executed. The array of pointers must be terminated by a `null` pointer.
*   `execvp()` is wrapper build upon `execve` syscall. Internally, it is just:

    ```c
    int execvp(const char *file, char *const argv[]);
    ```
* The first argument is a pointer to the binary which is to be executed and the second argument is an array to the arguments provided to the binary.
* Why not `execvp(argv)` directly?
  * Remember, `sys.argv[0]` is reserved to the filename in python. `$0` is reserved for the script name in bash. The same principle is followed here.
* The `exec()` family of functions returns only when an error has occurred, which is -1, which is why we are running the binary through `execvp` and matching if the return value is -1, to indicate failure or success.
* The `waitpid()` function is like `async()` function in JavaScript, which waits for a longer process to finish and then adjusts the results appropriately, without stopping the current thread.
* After that some cleanup happens and we are done.

***

Now, lets understand the flow of execution, that's the most important thing here.

* Lets name the process of the calling C program as `p_proc` and the process of the binary it is calling internally as `c_proc` .
* The calling process is cloned.
* We know that process are independent in their execution context, which means that `p_proc` and `c_proc` will be running independently.
  * If we print something just after cloning the process, there is no guarantee if the first print came from the parent or the child because the child has a copy of the file descriptors and it depends on scheduling algorithms that which on goes first.
* Both the processes continue executing the same code from the point where fork() returned. Lets look at the execution of `p_proc` first.
  * The `pid` variable for the calling process would have a random 4-5 digit unsigned value, which is definitely not equal to -1. Therefore, it never goes in the first `if` block.
  * Also, it is not 0. So, it never goes in the second `if` block as well.
  * Remaining `else` block. Here, it will find `waitpid()`, which will tell it to wait until the cloned process ends up.
    * If you comment this part, this means, the parent didn't wait until the child finished. Such a process is called zombie process. Such processes are adopted by `init`.
    * You'll only see `Hello, World!` and no `sleep(10)` effect.
    * But wait. After 10 seconds, you'll see that too, but in a new prompt.
    * Here the parent process finished. Lets focus on the child now.&#x20;
* The `c_proc` receives `0` in its `pid` variable. Thus, it qualifies to go inside the second `if` block.
  * And everything happens as stated before in `execve` section.
  * But remember, both the processes are executing independently. But because of `waitpid()`, the parent waits for the child to finish and cleans up everything.
* That's how it works.

## \`exec\` Family Of Functions

`execve` syscall has multiple wrappers in the form of C library functions. The questions is, which one to use when?

`execve(path, argv, envp)` is the raw signature of this syscall.

```c
char *argv[] = {"/path/to/binary", .., .., NULL};
char *envp[] = {"variable=value", "var2=val2", NULL}
execve(args[0], args, envp);
```

### Prefix Guide

* `v`: vector: refers to an array/vector of arguments
* `l`: list: refers to a list of arguments, passed as varargs
* `p`: path: tells the function to search $PATH for the executable
* `e`: environment: lets you explicitly pass the environment

### Functions

* `execv(path, argv)`: inherits caller's environment.
* `execl(path, arg0, arg1, ..., NULL)`: Same as `execv`, except that the arguments are directly passed as varargs, rather than an array.
* `execvp(file, argv)`: searches `$PATH` variable for the binary. Good to run programs like a shell would do, like `ls` or `./exe`
* `execlp(file, arg0, ...., argN, NULL)`: combines `execl + $PATH`
* `execle(path, arg0, ..., NULL, envp)`: varargs + custom env

And that's how we finish establishing a baseline understanding in Linux processes.

Thank You.
