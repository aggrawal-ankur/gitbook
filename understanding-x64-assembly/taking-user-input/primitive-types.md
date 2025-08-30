# Primitive Types

_**27, 28, 29, 30 August 2025**_

***

## Note

We have 4 primitive data types: `char`, `int`, `float`, `double`. But we will talk only about `char` and `int`. The same rules apply to `float` and `double` .

## Theoretical View

Broadly, we can classify memory allocation in terms of function scope and file scope.

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

1.  Declaration + Initialization.

    ```c
    int num = 45;
    char gen = 'M';
    ```
2.  Declaration only.

    ```c
    int num;
    char gen;
    ```

    Here, the two locations can be populated either later in the program itself or via user-input.

***

### Outside Function Declarations

```c
#include <stdio.h>

int PI = 3.14;            // extern, by default
auto int PI = 3.14;       // Not allowed
static int PI = 3.14;     // Makes the variable File Scoped.
extern int PI = 3.14;     // Raises a warning, but no problem

int main(void);
```

### Inside Function Declarations

```c
// main.c
#include <stdio.h>

int main(void){
  int PI = 3.14;            // auto, by default
  auto int PI = 3.14;
  static int PI = 3.14;     // Lifetime is changed to "until the program exist"
                            // Scope is still block-level

  extern int PI = 3.14;     // Raises error; A block scope declaration can't be made extern

  // But, we can refer to an already existing variable with external linkage/global visibility
  extern int global_PI;     // refers to the declaration in another.c
}
```

```c
// another.c
int global_PI = 3.14;       // extern, by default
```

***

#### What is the use of \`static\` in block scope?

```c
#include <stdio.h>

int main(void){
  static int PI = 3.14;
}
```

This increases the lifetime of a variable (PI, here) but it is still block scoped. It makes the variable a "**private global**".

Take this:

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

Here, `ncalls` is a static variable, so, its state is retained in every function call, instead of being allocated every single time, which is why the printf in main prints 4.

***

_Wait, the lifetime is increased but the scope remains the same, how does that work?_

* That is answered the best with experimentation.

## Practical View

It's time for experiments.

We will use this command to compile our source to assembly.

```
gcc ./main.c -S -O0 -fno-asynchronous-unwind-tables -fno-dwarf2-cfi-asm -masm=intel
```

This ensures that we see intel syntax, no optimization and no `cfi*` directives, just assembly. You can use `godbolt.org` as well.

### Experiment 1: Function scope and default storage class

```c
#include <stdio.h>

int main(void){
  int a;
}
```

Compile this source.

**Expectation:** An integer is sized 4-bytes but that makes `rsp` misaligned, so, we are expecting the compiler to reserve 16 bytes on stack.

**Reality:** Function prologue and epilogue. No allocation on stack.

***

**Change:** Maybe the previous program was too short. So, we have added a printf.

```c
#include <stdio.h>

int main(void){
  int a;
  printf("Heyy.\n");
}
```

**Expectation:** Same.

**Reality:** The same. No allocation on stack.

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

You may ask, isn't the stack misaligned here? NO.

* We are moving `rbp` relative, not `rsp` relative. `rsp` is still 16-bytes aligned.
* Compiler optimization, you know!

Doesn't this behavior makes it hard for accessing the value? Let's see.

***

**Change:** Lets access the value.

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

**Result:** Now it is using subtraction because there is need for it.

***

So, in a realistic situation, what behavior can we expect?

Here is a simple (very non-realistic) program.

```c
#include <stdio.h>

int main(void){
  int num = 2;
  
  int inc_num;
  printf("Increment number: ");
  scanf("%d", &inc_num);

  printf("Incremented by %d, becomes %d\n", inc_num, num+inc_num);
}
```

It initializes one digit and takes another as input and uses both of them **generously**.

This is the assembly.

```c
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16
	mov	DWORD PTR -4[rbp], 2
	lea	rax, .LC0[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT
	lea	rax, -8[rbp]
	mov	rsi, rax
	lea	rax, .LC1[rip]
	mov	rdi, rax
	mov	eax, 0
	call	__isoc99_scanf@PLT
	mov	edx, DWORD PTR -8[rbp]
	mov	eax, DWORD PTR -4[rbp]
	add	edx, eax
	mov	eax, DWORD PTR -8[rbp]
	mov	esi, eax
	lea	rax, .LC2[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT
	mov	eax, 0
	leave
	ret
```

Although we are using two integers, we are still subtracting 16 bytes because now the `rsp` is 8-bytes misaligned (previously it was 12-bytes).

***

### Outcomes Of E-1

1. Any allocation that uses default storage class for block scope goes on stack.
2. In case of uninitialized declarations, if the declaration is not used later in the program, the compiler has no incentive to reserve space for it.
3. `rsp` is subtracted 16-bytes aligned to reserve space.
4. `rbp` is used as a stable pointer to reference allocations inside a stack frame.

***

### Experiment 2: Outside function scope and default storage class

**Note: I am using** `PI` **as an example but declaring it as an integer, which is obviously wrong. So, in assembly, you will see** `3` **not** `3.14`**. But that doesn't create any problem.**

```c
#include <stdio.h>

int PI;

int main(void){}
```

**Expectation:** Since it is uninitialized, it should be zero-allocated at runtime and declared in `.bss`.

**Reality:** Indeed.

```nasm
	.text
	.globl	PI
	.bss
	.align 4
	.type	PI, @object
	.size	PI, 4
PI:
	.zero	4
```

We can use readelf to check its linkage.

```bash
$ readelf ./out --symbols | grep PI

31: 0000000000004014     4 OBJECT  GLOBAL DEFAULT   25 PI
```

* It is global (external).

***

**Change:** Initialize it.

```c
#include <stdio.h>

int PI = 3.14;

int main(void){}
```

**Expectation:** Now the declaration should be in `.data`.

**Reality:** Indeed.

```nasm
	.text
	.globl	PI
	.data
	.align 4
	.type	PI, @object
	.size	PI, 4
PI:
	.long	3
```

### **Outcomes Of E-2**

1. A global declaration always exist.
2. They have external linkage.

***

### Experiment 3: Outside function scope and \`static\` class

```c
#include <stdio.h>

static int PI;

int main(void){}
```

**Expectation:** Internal linkage and a declaration in `.bss`.

**Reality:** Indeed.

```nasm
	.text
	.local	PI
	.comm	PI,4,4
```

You might find it different from previous ones. There is no `PI:` as a label. And right now (29 August 2025), I have no answer for that.

***

```c
#include <stdio.h>

static int PI = 3.14;

int main(void){}
```

**Expectation:** In `.bss`.

**Reality:** Indeed.

```nasm
	.data
	.align 4
	.type	PI, @object
	.size	PI, 4
PI:
	.long	3
```

***

### The Final Boss; Experiment 4: Function scope + \`static\`

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
