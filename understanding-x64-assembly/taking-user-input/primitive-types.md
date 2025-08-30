---
description: >-
  We have 4 primitive data types: char, int, float, double. But we will take
  `int` as reference. Rules are same for others.
---

# Primitive Types

_**27, 28, 29, 30 August 2025**_

***

## Theoretical View

We can classify memory allocation in terms of function scope and file scope.

```c
#include <stdio.h>

// FILE SCOPE

int another_function(){
  // FUNCTION SCOPE
  return something
}

int main(void){
  // FUNCTION SCOPE
}
```

In both of these scopes, we can have:

1.  Declaration only.

    ```c
    int num;
    char gen;
    ```
2.  Declaration + Initialization.

    ```c
    int num = 45;
    char gen = 'M';
    ```

***

### Outside Function Declarations

```c
#include <stdio.h>

int BASE = 16;            // extern, by default
auto int BASE = 16;       // Not allowed
static int BASE = 16;     // Makes the variable File Scoped.
extern int BASE = 16;     // Raises a warning as there is no need to explicitly say 'extern'

int main(void);
```

### Inside Function Declarations

```c
// main.c
#include <stdio.h>

int main(void){
  int BASE = 16;            // auto, by default
  auto int BASE = 16;

  static int BASE = 16;     // Lifetime is changed to "until the program exist"
                            // But the scope is still block-level

  extern int BASE = 16;     // Raises error; A block scope declaration can't be made extern

  // But we can refer to an already existing variable with external linkage/global visibility
  extern int global_BASE;     // refers to the declaration in another.c
}
```

```c
// another.c
int global_BASE = 16;       // extern, by default
```

***

#### What is the use of \`static\` in block scope?

```c
#include <stdio.h>

int main(void){
  static int BASE = 16;
}
```

This increases the lifetime of a variable but it remains block scoped. It makes the variable a "**private global**".

Take this:

```c
#include <stdio.h>

int sq(int n, int flag){
  static int ncalls = 0;
  
  if (flag != 1){
    ncalls++ ;
    return n*n;
  }
  if (flag == 1){
    return ncalls;
  }
  return -1;
}

int main(){
  printf("%d\n", sq(2, 0));
  printf("%d\n", sq(3, 0));
  printf("%d\n", sq(4, 0));
  printf("%d\n", sq(5, 0));
  printf("%d\n", sq(1, 1));

  return 0;
}
```

Here `ncalls` is a static variable, so, its state is retained in every function call, instead of being allocated every single time, which is why the last `printf` prints 4.

***

_Wait, the lifetime is increased but the scope remains the same, how does that work?_

* This is the most complicated case and we are going to talk about it soon.

## Practical View

Let's do some experiments to understand storage classes, the concept of scope and linkage.

We will use this command to compile our source to assembly.

```
gcc ./main.c -S -O0 -fno-asynchronous-unwind-tables -fno-dwarf2-cfi-asm -masm=intel
```

This ensures that we see intel syntax, no optimization and no `cfi*` directives, just pure assembly. You can use `godbolt.org` as well.

### Experiment 1: Function scope and default storage class

```c
#include <stdio.h>

int main(void){
  int a;
}
```

**Expectation:** An integer is sized 4-bytes but that makes `rsp` misaligned, so we are expecting the compiler to reserve 16 bytes on stack.

**Reality:** Function prologue and epilogue. No allocation on stack.

***

**Change:** Maybe the previous program was too short. So, we have added a printf.

```c
#include <stdio.h>

int main(void){
  int a;
  printf("Hi!\n");
}
```

**Expectation:** Same.

**Reality:** No allocation on stack.

***

**Change:** Lets use this declaration somewhere. Lets take user input.

```c
#include <stdio.h>

int main(void){
  int a;
  printf("Enter a: ");
  scanf("%d", &a);
}
```

**Expectation:** Same.

There you go. We have it.

```nasm
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16		       ; <- Here
	lea	rax, .LC0[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT
	lea	rax, -4[rbp]
	mov	rsi, rax
	lea	rax, .LC1[rip]
	mov	rdi, rax
	mov	eax, 0
	call	__isoc99_scanf@PLT
	mov	eax, 0
	leave
	ret
```

***

**Change:** What if we "declare + initialize", instead of user input?

```c
#include <stdio.h>

int main(void){
  int a = 45;
}
```

```c
main:
	push	rbp
	mov	rbp, rsp
	mov	DWORD PTR -4[rbp], 45
	mov	eax, 0
	pop	rbp
	ret
```

Here, we are not subtracting to reserve space. Instead, we are using `rbp` as a reference point (for the current stack frame) and subtracting 4 bytes from there. Then we are storing 45 at the 4th block (byte).

The stack is not misaligned because we are moving `rbp` relative, not `rsp` relative. `rsp` is still 16-bytes aligned.

* Compiler optimization, you know!

Doesn't this behavior makes it hard for accessing the value? Let's see.

***

```c
#include <stdio.h>

int main(void){
  int a = 45;
  printf("%d\n", a);
}
```

**Expectation:** Extra work to access `a` due to this "so called optimization".

```nasm
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16
	mov	DWORD PTR -4[rbp], 45
	mov	eax, DWORD PTR -4[rbp]
	mov	esi, eax
	lea	rax, .LC0[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT
	mov	eax, 0
	leave
	ret
```

**Result:** Now it is using subtraction.

***

### Outcomes Of E-1

1. Any allocation in block scope goes on stack by default.
2. In case of uninitialized declarations, if the declaration is not used later in the program, the compiler has no incentive to reserve space for it.
3. `rsp` is subtracted 16-bytes aligned to reserve space.
4. `rbp` is used as a stable pointer to reference allocations inside a stack frame.

***

### Experiment 2: Outside function scope and default storage class

```c
#include <stdio.h>

int BASE;

int main(void){}
```

**Expectation:** Since it is uninitialized, it should be zero-initialized at runtime and declared in `.bss`.

**Reality:** Indeed.

```nasm
	.text
	.globl	BASE
	.bss
	.align 4
	.type	BASE, @object
	.size	BASE, 4
PI:
	.zero	4
```

We can use readelf to check its linkage as we are not using .c multiple files so there is no other way to verify if it is "globally" available or not.

```bash
$ readelf ./out --symbols | grep BASE

31: 0000000000004014     4 OBJECT  GLOBAL DEFAULT   25 BASE
```

* Verified.

***

**Change:** Initialize it.

```c
#include <stdio.h>

int BASE = 16;

int main(void){}
```

**Expectation:** Now the declaration should be in `.data`.

**Reality:** Indeed.

```nasm
	.text
	.globl	BASE
	.data
	.align 4
	.type	BASE, @object
	.size	BASE, 4
PI:
	.long	16
```

### **Outcomes Of E-2**

A global declaration has external linkage and always exist in memory, unlike block scope declarations which require usage.

***

### Experiment 3: Outside function scope and \`static\` class

```c
#include <stdio.h>

static int BASE;

int main(void){}
```

**Expectation:** Internal linkage and a declaration in `.bss`.

**Reality:** Indeed.

```nasm
.text
.local	BASE
.comm	BASE,4,4
```

You might find it different from previous ones. There is no `PI:` as a label. And, as of now (29 August 2025), I have no answer for that.

***

```c
#include <stdio.h>

static int BASE = 16;

int main(void){}
```

**Expectation:** In `.bss`.

**Reality:** Indeed.

```nasm
	.data
	.align 4
	.type	BASE, @object
	.size	BASE, 4
PI:
	.long	16
```

***

### Experiment 4: Function scope + \`static\` :: The Final Boss

```c
#include <stdio.h>

int main(void){
  static int num;
}
```

**Expectation:** In `.bss`.

**Reality:** Indeed.

```nasm
    .local   num.0
    .comm    num.0,4,4
```

***

```c
#include <stdio.h>

int main(void){
  static int num = 45;
}
```

**Expectation:** In `.data`.

**Reality:** Indeed.

```nasm
	.data
	.align 4
	.type	num.0, @object
	.size	num.0, 4
num.0:
	.long	45
```

***

Lets analyze what is happening here.

* `num.0` is the label that is for our variable `num`.
* `.local` is a GAS directive which controls the visibility of `num.0`, it makes it file scoped.
* `.comm` is a GAS directive which allocates memory in `.bss`. `num.0, 4, 4` means allocate 4 bytes for `num.0` and align the storage by 4 bytes for efficient access. 4 bytes of alignment because it is an integer.

***

The biggest mystery here is how the lifetime is increased but the scope remains block level?

To understand this, we have to understand how scopes are enforced.

If you were _not zoning out_ so far, you could have noticed that

* Implementing block scope via `auto` class and program scope via `extern` class is very straightforward. Either you completely hide something, or you make it visible.
* When you use static with a global variable, you make it file scope. And this file level scope is directly managed by assembly. You use `.lcomm` or `.local` directly to enforce this strictness.
* The problem comes when you try to make a block scope (`auto`) declaration static. The declaration is happening inside `.data/.bss` but the scope is limited to the block.

The way `.local` and `.global` directives work is that they affect the linker visibility attribute for a symbol. `.global` makes the symbol visible to the linker while `.local` doesn't.

* But the thing is that "no linkage" and "internal linkage" both uses `LOCAL` as visibility to the linker and that is perfectly normal.
* You don't want a block scope symbol and a file scope symbol to be available outside of the current translation unit (a name for extended source code file).
* Therefore, if you were given just an unstripped binary (because stripped ones don't have `.symtab`), you can't tell if a `LOCAL` symbol is a file scope static or a block scope static.

Making a block scope declaration static is a rule enforced at compilation level.

* First, the code undergoes lexical analysis. Then abstract syntax tree formation. Next comes semantic analysis, here happens the magic.
* An internal symbol table is created using the AST, and that table enforces this rule. It sees that this variable requires allocation in static storage but the scope has to be kept block. So, it doesn't explicitly allows any code that refers to that declaration because it is not available outside.
* But, once you cross compilation and reach assembly, there is no such thing. If you want, you can mess with it. There is no "program lifespan but block scope" thing at assembly. And we can try that out.

Take this example we have seen before:

```c
#include <stdio.h>

int sq(int n, int flag){
  static int ncalls = 0;
  
  if (flag != 1){
    ncalls++ ;
    printf("sq(%d) = %d\n", n, n*n);
    return ncalls;
  }
  if (flag == 1){
    return ncalls;
  }
  return -1
}

int main(){
  sq(2, 0);
  sq(3, 0);
  sq(4, 0);
  sq(5, 0);
  printf("Number of calls made to square function: %d\n", sq(1, 1));

  return 0;
}
```

Lets see assembly.

```nasm
	.text
	.globl	sq
	.type	sq, @function
sq:
	push	rbp
	mov	rbp, rsp

	mov	DWORD PTR -4[rbp], edi			; arg1 saved on stack
	mov	DWORD PTR -8[rbp], esi			; arg2 saved on stack

	; flag != 1 check
	cmp	DWORD PTR -8[rbp], 1
	je	.L2
	; continue downwards if not 1

	; increment ncalls
	mov	eax, DWORD PTR ncalls.0[rip]
	add	eax, 1
	mov	DWORD PTR ncalls.0[rip], eax

	; setup return value
	mov	eax, DWORD PTR -4[rbp]
	imul	eax, eax
	jmp	.L3															  ; jump to return Label

; (flag == 1) Label
.L2:
	cmp	DWORD PTR -8[rbp], 1
	jne	.L4
	mov	eax, DWORD PTR ncalls.0[rip]
	jmp	.L3

; setup return value == -1
.L4:
	mov	eax, -1

; return
.L3:
	pop	rbp
	ret

; %d string for printfs
	.section	.rodata
.LC0:
	.string	"%d\n"
	.text
	.globl	main
	.type	main, @function

main:
	push	rbp
	mov	rbp, rsp

	mov	esi, 0
	mov	edi, 2
	call	sq					; sq(2, 0)

	mov	esi, eax				; arg2 for printf
	lea	rax, .LC0[rip]
	mov	rdi, rax				; arg1 for printf
	mov	eax, 0
	call	printf@PLT				; printf for sq(2, 0)

	mov	esi, 0
	mov	edi, 3
	call	sq					; sq(3, 0)

	mov	esi, eax				; arg2 for printf
	lea	rax, .LC0[rip]
	mov	rdi, rax				; arg1 for printf
	mov	eax, 0
	call	printf@PLT				; printf for sq(3, 0)

	mov	esi, 0
	mov	edi, 4
	call	sq					; sq(4, 0)

	mov	esi, eax				; arg2 for printf
	lea	rax, .LC0[rip]
	mov	rdi, rax				; arg1 for printf
	mov	eax, 0
	call	printf@PLT				; printf for sq(4, 0)

	mov	esi, 0
	mov	edi, 5
	call	sq					; sq(5, 0)

	mov	esi, eax				; arg2 for printf
	lea	rax, .LC0[rip]
	mov	rdi, rax				; arg1 for printf
	mov	eax, 0
	call	printf@PLT				; printf for sq(4, 0)

	mov	esi, 1
	mov	edi, 1
	call	sq					; sq(1, 1)

	mov	esi, eax				; arg2 for printf
	lea	rax, .LC0[rip]
	mov	rdi, rax				; arg1 for printf
	mov	eax, 0
	call	printf@PLT				; printf for sq(1, 1)

	mov	eax, 0
	pop	rbp
	ret

; ncalls declaration
	.local	ncalls.0
	.comm	ncalls.0,4,4
```

This follows the usual flow. I have added comments to understand the flow better.

* Every `printf` is taking 2 arguments. First one is the %d string and the second one is the actual integer to be printed.
* The second argument is the return value of the `sq` function, via `eax`.

If you are using VS Code, you can select all the `mov esi, eax` lines and replace them with `mov, esi, DWORD PTR ncalls.0[rip]`, we will see a magic. The assembly is perfectly assembled and linked. And the output is completely transformed.

```bash
gcc main.s -o out
./out
```

```bash
1
2
3
4
4
```

Voila. This proves our point that **lifetime + block scope** is just a rule, not a hardly imposed impossibility, which is why it can be bypassed at assembly level.

***

IDE like VS Code have language server protocol, which is basically a real time parser of the source code and verifies it against the language rules. If there are anomalies, it flags them. There is nothing magical.

***

## Conclusion

SO, what's the gain? If you have not lost your sanity yet, you can clearly observe that we have just seen how storage class and the concept is applied. We have not studied anything other than the two tables mentioned in the previous article. We have just tried to go as deeper as we can to prove the point even further.

It is overwhelming and I won't deny that. Take your time. Enjoy.
