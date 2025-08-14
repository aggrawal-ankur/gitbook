# How a character buffer exist and managed at low level?

_**August 14, 2025**_

***

## Premise

This article explores the following low level concepts,

1. How storage class affects memory allocation?
2. How are format specifiers interpreted?

based on the following C source.

```c
#include<stdio.h>

int main(void){
  char NAME_BUFF[100];

  printf("Enter your name: ");
  scanf("%s", NAME_BUFF);

  printf("Hello, %s!\n", NAME_BUFF);
}
```

## Where is NAME\_BUFF in the memory?

If you paste this source on [godbolt.org](https://godbolt.org), you will find this assembly:

```nasm
.LC0:
        .string "Enter your name: "
.LC1:
        .string "%s"
.LC2:
        .string "Hello, %s!\n"
main:
        push    rbp
        mov     rbp, rsp
        sub     rsp, 112
        mov     edi, OFFSET FLAT:.LC0
        mov     eax, 0
        call    printf
        lea     rax, [rbp-112]
        mov     rsi, rax
        mov     edi, OFFSET FLAT:.LC1
        mov     eax, 0
        call    __isoc99_scanf
        lea     rax, [rbp-112]
        mov     rsi, rax
        mov     edi, OFFSET FLAT:.LC2
        mov     eax, 0
        call    printf
        mov     eax, 0
        leave
        ret
```

You can also use `gcc` with `-01 -masm=intel -S` flags to generate the same assembly. But there will be two differences.

1. There would be `cfi*` directives.
2. It would use `rip` relative addressing instead of assembler specific `OFFSET` directive because it is already built completely with ASLR.

But these things don't affect what we are looking for.

***

You can immediately notice that there is no `.data` section or `.rodata` section. There is no `.bss` section as well. Where is `NAME_BUFF` defined then?

* This is a classic case to understand how memory allocation for even simple variables work.
*   For clarity, I have divided the `main:` section in smaller chunks using empty lines. The assembly looks like this now:&#x20;

    ```nasm
    main:
            ; Function Prologue
            push    rbp
            mov     rbp, rsp

            ; Reserve 112 bytes for locals
              ; 100 bytes for buffer + 12 bytes for alignment
            sub     rsp, 112

            ; Setup to print .LC0
            mov     edi, OFFSET FLAT:.LC0
            mov     eax, 0
            call    printf

            ; Setup to read the buffer into stack
            lea     rax, [rbp-112]
            mov     rsi, rax
            mov     edi, OFFSET FLAT:.LC1
            mov     eax, 0
            call    __isoc99_scanf

            ; Setup to out (print) the buffer in terminal (stdout)
            lea     rax, [rbp-112]
            mov     rsi, rax
            mov     edi, OFFSET FLAT:.LC2
            mov     eax, 0
            call    printf
            mov     eax, 0
            leave
            ret
    ```

Since we already know assembly, we can tell that  the buffer is being stored on stack. But what's the reasoning behind it? Why the system chose to store the buffer on stack? The answer lies within storage classes.

### Storage Class

Storage classes tell the compiler how to manage a variable.

1. Where the variable would be stored?
2. How long it would exist (lifetime) ?
3. Who can access it, or where it can be accessed from (scope) ?
4. Whether it has a default initial value?

There are 4 main storage classes in C.

<table><thead><tr><th width="138">Storage Class</th><th>Scope &#x26;&#x26; Lifetime</th><th>Default Value</th><th width="160">Storage Location</th><th>Notes</th></tr></thead><tbody><tr><td><strong>auto</strong></td><td>The block it is declared in (local)<br><br>Until the block ends</td><td>Garbage (undefined)</td><td>Stack</td><td>Default for local variables; no need to mention explicitly.</td></tr><tr><td><strong>register</strong></td><td>The block it is declared in (local)<br><br>Until the block ends</td><td>Garbage</td><td>CPU register (if available)</td><td>Hint to store in CPU register for faster access (compiler may ignore it). Cannot take address with <code>&#x26;</code>.</td></tr><tr><td><strong>static</strong></td><td>File Scope<br><br>Until the program exists in the memory</td><td>0</td><td>Data segment</td><td>Local static: retains value between function calls. Global static: limits scope to file (internal linkage).</td></tr><tr><td><strong>extern</strong></td><td>File/global<br><br>Until the program exists in the memory</td><td>0</td><td>Data segment</td><td>Declares a variable that’s defined elsewhere; used for sharing globals across files.</td></tr></tbody></table>

Now you can see why the `NAME_BUFF` wasn't stored in the `.data` segment, because it was never meant to be.

* The `.data` section hold static/globals which are already initialized in the program.
* The `.bss` section hold static/globals which are uninitialized in the program and reserve memory in the heap.

***

You may still ask _why the variables are stored on the stack by default?_ And the answer to it is quite simple.

* _For a detailed answer, you can visit this article which explores the whole idea behind_ [_stack_](../approaches-to-memory-management/stack.md)_._
* Functions go on the stack in the form of stack frame. And every thing related to that function is scoped to it. A variable declared in that function is scoped to that function. And it should be accessible until that stack frame exist. This you can't achieve with heap. That's why `NAME_BUFF` goes on the stack, because they way we expect to manage it aligns perfect with the idea of stack.

## How the format specifier exist here?

We can notice that `%s` is stored as a separate string symbol (`.LC1`) and it is passed to `scanf` as an argument via register. But for `printf`, no such thing. Why?

Because format specifiers are meaningful to C only.

If you remember function call argument order, the first argument goes into `rdi`, and the second one goes into `rsi`.

We are passing the format specifier as the first argument and it tells `scanf` to interpret the second argument (in `rsi` ) as a pointer to a writable memory, read input from `stdin` until `EOF/whitespace` and append a null-character (`\0`) to it.

***

While printing the string to `stdout`, the flow is like this.

Load the address of `NAME_BUFF` into `rsi` as the 2nd argument.

Load the address of `.LC2` into `rdi` as the 1st argument. The `%s` is embedded in `.LC2` itself and tells `printf` to interpret the 2nd argument as a null-terminated string.

## Why we are zeroing the accumulator so many times?

The ABI defines that the accumulator (`eax`) must be cleared before a function call for varargs call.

If it is not clear to you, it is not clear to me as well. **I am leaving this for now because it relates to variadic nature of `printf` like functions and it is not required here.**

## So, how a a character buffer exists at low level?

A character can be of different types. The program below briefly lists all of them.

```c
#include <stdio.h>

static char BUFF5[20];

static char BUFF6[100] = "my name is anna.\n";

int main(void){
  char BUFF1[100] = "my name is anna.\n";

  char BUFF2[10];

  static char BUFF3[100];

  static char BUFF4[100] = "Heyy, wassup?\n";
}
```

We can quickly categorize them as local buffers and static/global buffers.

* `BUFF1` and `BUFF2` are local variables, so they must go into the stack.
* `BUFF3` and `BUFF4` are static/global variables, which have broader scope than the stack frame. Therefore, they must persist.&#x20;
  * `BUFF3` is uninitialized so it must go to `.bss` section.
  * `BUFF4` is initialized so it must go to `.data` section.
* Again, `BUFF5` and `BUFF6` follows the same idea as `BUFF3` and `BUFF4` respectively. So,
  * `BUFF5` is uninitialized so it must go to `.bss` section.
  * `BUFF6` is initialized so it must go to `.data` section.

Lets check. Use `-01 -masm=intel -S` with `gcc`

```nasm
	.text
	.local	BUFF5
	.comm	BUFF5,20,16

	.data
	.align 32
	.type	BUFF6, @object
	.size	BUFF6, 100

BUFF6:
	.string	"my name is anna.\n"
	.zero	82
	.text
	.globl	main
	.type	main, @function

main:
.LFB0:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 8

	movabs	rax, 2334392247088347501
	movabs	rdx, 3342073818840593257

	mov	QWORD PTR -112[rbp], rax
	mov	QWORD PTR -104[rbp], rdx
	mov	QWORD PTR -96[rbp], 10
	mov	QWORD PTR -88[rbp], 0
	mov	QWORD PTR -80[rbp], 0
	mov	QWORD PTR -72[rbp], 0
	mov	QWORD PTR -64[rbp], 0
	mov	QWORD PTR -56[rbp], 0
	mov	QWORD PTR -48[rbp], 0
	mov	QWORD PTR -40[rbp], 0
	mov	QWORD PTR -32[rbp], 0
	mov	QWORD PTR -24[rbp], 0
	mov	DWORD PTR -16[rbp], 0

	mov	eax, 0
	leave
	ret

.LFE0:
	.size	main, .-main
	.data
	.align 32
	.type	BUFF4.1, @object
	.size	BUFF4.1, 100

BUFF4.1:
	.string	"Heyy, wassup?\n"
	.zero	85

	.local	BUFF3.0
	.comm	BUFF3.0,100,32

	.ident	"GCC: (Debian 14.2.0-19) 14.2.0"
	.section	.note.GNU-stack,"",@progbits
```

If you remember, GAS provides 3 directives to declare uninitialized buffers.

* `.skip`&#x20;
* `.comm`&#x20;
* `.lcomm`&#x20;





