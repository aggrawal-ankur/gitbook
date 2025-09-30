---
title: Introduction To Linux Processes
weight: 1
---

Originally written in first and second week of **June 2025**.

Rewrite/Polish on **29, 30 September 2025**.

---

To execute a binary, Linux kernel creates a **process**.

*A **process** is a running instance of a binary.*

So far, we know that:

- Every process gets its own isolated address space, thanks to virtual memory. This gives processes an illusion that they have the whole memory.
- A virtual memory address (VMA) is the same as the name of a street and the physical memory address (PMA) is the actual GPS coordinates. Two cities can have a "main street" but their coordinates would be unique.
- The OS + hardware's MMU (Memory Management Unit) maps VMA to PMA. Without the MMU, all processes would share the same memory space — like roommates with no walls.
  * A bug in one process could overwrite another process's memory.
  * With MMU, each process gets its own private virtual address space. It's still messy on ground level but easier for management. It's a nice abstraction.

Let's move further.

## Process Hierarchy

Processes follow a tree like structure in linux.

* The first process is `init` or `systemd`, depending on the system, which is started by the kernel. It's PID is 1, and PPID is 0.
* Every process is a descendant of the `init` process.
* Processes follow a parent-child relationship. Every new process (child process) is created by an existing process (parent process).
* Although each process is independent in nature and the execution of a child process doesn't hinder the execution of the parent process or vice-versa, still, the child process is linked with the parent process and it has to report its exit status.

To view the tree like structure of processes, use `pstree`.

---

Why does process hierarchy exists? Why can't processes be truly independent?

- To understand this, we need to understand how processes are created.

## Process Creation

It is a 4 step "process".

| Step | Description | Syscall |
| :--- | :--- | :--- |
| 1 | Clone the current process | fork() |
| 2 | Replace the process image of the cloned process with the new binary. | exec() |
| 3 | Parent waits for the child to finish | wait() |
| 4 | Child finishes and returns the status to the parent | exit() |

Each process may require some helper processes.

* For example, when I did `pstree`, I found that VS Code is not a standalone process. It has a lot of child processes. Like the terminal opened within VS Code comes appears as a child process under the VS Code process.
* The same is with Firefox and everything else.

Hierarchical structure is not just a design philosophy, but a very logical decision.

* It's a very efficient way to organize all the processes in the system.
* We fork the current process (parent process), keep the identifying metadata as it is and replace the old process image with the new one. This ensures that the child process has proper links to the parent process, without any hustle.

Why the child process needs to be linked with the parent process?

- Every process is isolated and independent in its execution. But how will the parent process know if the child process is completed and has exited?
- That's why this "linkage" exist. It ensures that the parent process (like VS Code) has enough information about the state of the child processes they spawn (terminals, file I/O) so that they can make better decisions to manage them.

## Key Properties Of A Process

| Property | Description |
| :--- | :--- |
| PID (Process ID)         | Unique identifier of a process. |
| PPID (Parent Process ID) | Unique identifier of the process that created the PID process. |
| UID (User ID)            | The user who owns the process. |
| State                    | Running, sleeping, zombie etc. |
| Memory Info              | RAM consumption                |
| Executable code and data | What it is running and working with. |

## A Theoretical Example

We are going to run a binary made from this C program.
```c {filename=binary}
#include <stdio.h>
#include <unistd.h>    // sleep()

int main(void){
  printf("Hello, World!");
  sleep(400);
}
```

To get the final ELF binary:
```bash
gcc binary.c -o binary
```

### Call The Binary

To call/execute the binary (`binary`), we need a shell (or terminal).

I have opened my shell, which is zsh.
```bash
$ echo $SHELL
/usr/bin/zsh
```

`zsh` itself is a "running" process. We can verify that with `ps`.
```zsh
$ ps
  
PID       TTY       TIME         CMD
41027     pts/0     00:00:01     zsh
49852     pts/0     00:00:00     ps
```

We will run the binary in background so that we can retain the shell session and the capability to examine it.
```bash
$ ./binary &

[1] 52184
```

With ps, we can see all the child processes of the current terminal session.
```bash
$ ps               

PID       TTY       TIME         CMD
41027     pts/0     00:00:02     zsh
52184     pts/0     00:00:00     binary
52325     pts/0     00:00:00     ps
```

Since main\_elf is executed within zsh, zsh must be the parent of main\_elf? Lets verify this.

```bash
$ ps -o pid,ppid,cmd

PID     PPID    CMD
41027   40797   /usr/bin/zsh -i
59461   41027   ./binary
59559   41027   ps -T -o pid,ppid,cmd
```

- `-o` helps in custom formatting.

Notice the PID of zsh process is the PPID of the binary process. This proves the parent-child relationship between `zsh` and `binary`.

This also proves that `fork()` was called on the zsh process.

---

A fork is a near-clone of the parent process. It is not an exact clone because things like PPID (and other metadata) are different for obvious reasons.
- But the child process have a different binary than the parent. Therefore, the process image must be replaced.

`strace` is a Linux utility which helps in tracing all the syscalls a process has executed.

If we run our program with `strace`, like this:
```bash
$ strace ./binary

execve("./out", ["./out"], 0x7ffe0b2853a0 /* 56 vars */) = 0
brk(NULL)                               = 0x561db0e70000
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f4405902000
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=79019, ...}) = 0
mmap(NULL, 79019, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f44058ee000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0p\236\2\0\0\0\0\0"..., 832) = 832
pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 840, 64) = 840
fstat(3, {st_mode=S_IFREG|0755, st_size=2003408, ...}) = 0
pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 840, 64) = 840
mmap(NULL, 2055800, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f44056f8000
mmap(0x7f4405720000, 1462272, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x28000) = 0x7f4405720000
mmap(0x7f4405885000, 352256, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x18d000) = 0x7f4405885000
mmap(0x7f44058db000, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1e2000) = 0x7f44058db000
mmap(0x7f44058e1000, 52856, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7f44058e1000
close(3)                                = 0
mmap(NULL, 12288, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f44056f5000
arch_prctl(ARCH_SET_FS, 0x7f44056f5740) = 0
set_tid_address(0x7f44056f5a10)         = 22924
set_robust_list(0x7f44056f5a20, 24)     = 0
rseq(0x7f44056f5680, 0x20, 0, 0x53053053) = 0
mprotect(0x7f44058db000, 16384, PROT_READ) = 0
mprotect(0x561d7a7b4000, 4096, PROT_READ) = 0
mprotect(0x7f440593e000, 8192, PROT_READ) = 0
prlimit64(0, RLIMIT_STACK, NULL, {rlim_cur=8192*1024, rlim_max=RLIM64_INFINITY}) = 0
munmap(0x7f44058ee000, 79019)           = 0
fstat(1, {st_mode=S_IFCHR|0600, st_rdev=makedev(0x88, 0x1), ...}) = 0
getrandom("\xf5\x5d\x3a\x53\x4e\x3d\x5b\x81", 8, GRND_NONBLOCK) = 8
brk(NULL)                               = 0x561db0e70000
brk(0x561db0e91000)                     = 0x561db0e91000
clock_nanosleep(CLOCK_REALTIME, 0, {tv_sec=1, tv_nsec=0}, 0x7ffc48c784e0) = 0
write(1, "Hello, World!", 13)           = 13
exit_group(0)                           = ?
+++ exited with 0 +++
```

It gives us lead to the next thing, `execve`.

### Update The Process Image

Imagine millions of processes inside a single RAM (or a bunch of RAM if you are rich), with all demanding various services constantly.
  - That's why an abstraction called virtual address space (VAS) exist to streamline that chaos.

A process image is the runtime representation of a binary in the virtual address space after it has been loaded into memory (RAM) by the OS for execution.

As we know it already, binaries follow ELF format on Linux, which is a specification that standardize the format for executables on Linux so that they can be easily loaded in the memory.

---

After forking(cloning) the current process, the process image in the cloned process needs to be changed. This is done by `execve`.

`execve` is a syscall which executes a binary passed to it as an argument. It does that by replacing the process image of the current process (not the child process, the current process) with the new binary, effectively running a different program without creating a new process.

- `execve` is designed to be paired with `fork()` in order to fit Linux hierarchical process structure.
- First we fork the current process, then we run execve on it so that it can undergo a process image replacement.

This is the signature of the `execve` syscall:
```c
int execve(const char *pathname, char *const _Nullable argv[], char *const _Nullable envp[]);
```

Welcome to C lessons once again.

- `_Nullable` means the array should have `NULL` as the last value.

- `const char*` means "pointer to a constant character stream". The pointer can be changed to point to a different memory address, but the value stored at the address it points to cannot be changed using this pointer.

- `char *const` means "constant pointer to a character stream". The pointer itself is constant and cannot be changed to point to a different memory address. However, the value stored at the address it points to can be modified.

Applying this lesson to the execve signature, we can say that:

- `pathname` is the name of the binary. It is of type `const char*`, ensuring that it can't be changed.

- `argv[]` is a *pointer* to a *null-terminated array* of *character pointers*. These pointers point to null-terminated strings that serve as the command-line arguments for the new program.
  - The first value, `argv[0]` must be the name of the binary being run, by convention.
  - The last value must be `NULL` to signify its end.

- `envp[]` is a pointer to a null-terminated array of character pointers. These pointers reference null-terminated strings that define the new program's environment variables.
  - Each string is typically in the format "KEY=VALUE".
  - The last value must be `NULL` to signify its end.

On success, execve returns nothing.

On failure, it returns -1.

---

Rest of the syscalls in the strace output are not required to be understood right now.

Let's understand how execve manage to replace the process image in the cloned process.

#### How execve works?

The kernel opens the binary (`binary`) using virtual file system (VFS). It reads the ELF Header (the first 64 bytes) to confirm it is an ELF, and find the `e_type`, `e_entry` and `e_phoff` fields. Although we know it, but let's revise.
  - e_type: type of elf (REL, EXEC, DYN)
  - e_entry: where the binary is loaded in VAS.
  - e_phoff: the location of program headers.

What is VFS?
  - There exist multiple file systems, like ext4, btrfs, zfs, hfs, ntfs, fat32 and so on...
  - Virtual filesystem is a uniform inform interface to access them, regardless of their differences.

---

After opening the binary, the kernel loads the binary into memory by reading program headers table. We aldready know this from ELF, but let's revise.

- Sections organize stuff within the binary. And segments organize those sections.
- We can have multiple sections of clothing inside one single showroom. That showroom is a segment that organizes multiple clothing sections.
- It maps each segment defined in the PHT into memory regions using `mmap()` (memory map) syscall and sets the memory protection permissions (R, W, X) accordingly.

This is the PHT for our ELF:

```bash
$ readelf -l binary

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
  - **Note: It is slightly formatted so that we can see it clearly.**

All the offsets are relative to the location where the binary is loaded, where "the binary is loaded" means the address from which the binary starts to exist in the VAS.

Program headers table describes how the OS should load the ELF binary into the memory. It loads parts of the binary into VAS with specified permissions.

Explanation of entries in PHT.

| Type      | Description |
| :-------- | :--- |
| PHDR      | The location of program headers in VAS.|
|           | 0x40 is 0d64, which means PHT lives just after elf headers. |
| INTERP    | Specifies the dynamic linker to load and run this PIE executable. This linker will resolve symbols and apply relocations before main() runs. |
| LOAD      | The actual loadable code/data in the binary. |
|           | Only R flag means it is a read-only section. There can be multiple such sections, eg: strings in printf identifies as rodata. |
|           | Our code is usually represented by the RE segment.
|           | The RW section is where mutable stuff goes, like data/bss.
| DYNAMIC   | Contains relocations, library names, symbol tables, etc., which are used by the dynamic linker to perform symbol resolution and relocation at runtime. |
| GNU_STACK | Specifies stack permissions. |
| GNU_RELRO | A region that is read-only after relocation. |
| Note, GNU_PROPERTY | Metadata |
| GNU_EH_FRAME | Exception handling frame, used by debuggers. |

Now our program is loaded in the memory, but we're not executing yet.

#### Dynamic Linking

Since the PHT has `INTERP` header, the kernel has to run this interpreter `lib64/ld-linux-x86-64.so.2` before jumping to the entry point in the binary.

The kernel now loads the dynamic linker/loader (`ld-linux-x86-64.so.2`) into the memory.
  - It exist as a shared object.
  - The dynamic linker is the first code that will run in this process.

Now the kernel set up the stack, `rip` to `ld-linux`'s entry point and returns the control to user space.

And the child process is finally alive.

`ld-linux` now:

1. Parses the `.dynamic` section (`readelf -S binary`)
2. Finds the required shared libraries, like `libc.so.6`
3. Loads them into the memory using `mmap()`.
4. Applies relocations to the code.
5. At last it jumps to our binary's entry point (not `main`, but `_start`).

#### Entry point Management && Program Execution

The dynamic linker jumps to `_start` in our binary (provided by crt1.o).

`_start` sets up C runtime.

Then it calls `__libc_start_main()`, a libc function that initializes more stuff and finally calls the `main()`.

Now the program runs.

- `printf()` is a call into `libc`.
- `sleep()` sleeps the process for 400 seconds using `nanosleep` syscall.

### End Of The Program

After main() finishes, the control goes back to `__libc_start_main()`, which handles the final cleanup and calls `exit()`.

The kernel cleans up the process resources and returns the exit code to the parent (zsh).

That's how it works!

## A Practical Example

We are going to create a program which manually calls fork, execve, wait and exit to manage the `binary` we have created previously as a child process.

```c {filename=process.c}
#include <stdio.h>         // Standard I/O: printf() and perror()
#include <stdlib.h>        // General Utils: exit()
#include <unistd.h>        // POSIX API: fork(), execvp(), getpid(), getppid()
#include <sys/types.h>     // Defines data types used in system calls: pid_t (the data type for process IDs)
#include <sys/wait.h>      // Provides macros and functions for waiting on child processes: waitpid(), WIFEXITED(), WEXITSTATUS()

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
    char *args[] = {"./binary", NULL};
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

`pid_t` is a type definition, defined in the `POSIX` API to hold process IDs. It allows the kernel and user-space programs to use a portable data type for managing process IDs.

`fork()` is used to clone the process that calls fork.
  - If the calling process is cloned successfully, it returns 0 to the **cloned process** and the process ID of the cloned process to the calling process (which is now the parent process).
  - If cloning failed, it returns `-1` to the calling process.

`getpid()` and `getppid()` are relative to the process that has invoked them.
  - `getpid()` gives the process ID of the current process.
  - `getppid()` gives the ID of the parent process of the current process.

***

The execve syscall is wrapped around `exec` prefixed functions in the GNU C library. They provide a variety of ways to use the execve syscall.

This is the signature of `execvp()`:
```c
int execvp(const char *file, char *const argv[]);
```
  - Arg1 is the name of the binary.
  - Arg2 is the argument set, where the first element must be the binary name, by convention.

Why not `execvp(argv)` directly? Remember,
  - `sys.argv[0]` is reserved to the filename in python.
  - `$0` is reserved for the script name in bash. The same principle is followed here.

The `exec()` family of functions returns only when an error occur, just like the syscall, which is -1.
  - More on exec family of function later in the write up.

The `waitpid()` function is like `async()` function in JavaScript, which waits for a longer process to finish and then adjusts the results appropriately, without stopping the current execution.

After that some cleanup happens and we are done.

***

Lets understand the flow of execution.

We are naming the parent (process.c) as `p_proc` and the child (binary.c) as `c_proc`.

The calling process is cloned.

We know that processes are independent in their execution, which means `p_proc` and `c_proc` will be running independently.
  - If we print something just after cloning the process, there is no guarantee if the first print came from the parent or the child because the child is a near-copy of the parent and the process image is not changed yet.
  - It depends on scheduling algorithms that which goes first.

Both the processes continue executing the same code from the point where fork() returned. Lets look at the execution of `p_proc` first.
  - If fork succeeded in cloning, the `pid` variable for the calling process would have a random **unsigned value**, representing the process ID of the cloned process. So the parent process never goes in the first `if` block.
  - It is not 0 as well. So, it never goes in the second `if` block.
  - It will go in the `else` block. Here, it will find `waitpid()`, which will tell it to wait until the cloned process ends up.
    * If you comment this part, this means, the parent didn't wait until the child finished. Such a process is called zombie process. Such processes are adopted by `init`.
    * You'll only see `Hello, World!` and no `sleep(10)` effect.
    * But wait. After 10 seconds, you'll see that too, but in a new prompt.
    * Here the parent process finished.

Lets focus on the child now.

The `c_proc` receives `0` in its `pid` variable. So it qualifies to go inside the second `if` block.
  * And everything happens as stated before in `execve` section.
  * But remember, both the processes are executing independently. But because of `waitpid()`, the parent waits for the child to finish.

That's how it works.

## The exec Family Of Functions

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

* `execv(path, argv)`: inherit caller's environment.
* `execl(path, arg0, arg1, ..., NULL)`: Same as `execv`, except that the arguments are directly passed as varargs, rather than an array.
* `execvp(file, argv)`: searches the `$PATH` variable for the binary. Good to run programs like a shell would do, like `ls` or `./exe`
* `execlp(file, arg0, ...., argN, NULL)`: combines `execl + $PATH`
* `execle(path, arg0, ..., NULL, envp)`: varargs + custom env

And that is a beginners introduction to a Linux process.

Thank You very much.