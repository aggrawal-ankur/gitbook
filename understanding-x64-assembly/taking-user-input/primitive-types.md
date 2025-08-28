# Primitive Types

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

_Wait, if the scope is still block for static variables inside a block scope, how the lifetime is increased? Where they are declared? Stack wouldn't allow this, right?_

* Wait for a while.

## Practical View

It's time for experiments.

We will use this command to compile our source to assembly.

```
gcc ./main.c -S -O0 -fno-asynchronous-unwind-tables -fno-dwarf2-cfi-asm -masm=intel
```

This ensures that we see intel syntax, no optimization and no `cfi*` directives, just assembly. You can use `godbolt.org` as well.

### Experiment 1

```c
#include <stdio.h>

int main(void){
  int a;
}
```

Compile this source.

**Expectation:** An integer is sized 4-bytes but that makes `rsp` misaligned, so, we are expecting the compiler to reserve 16 bytes on stack.

**Reality:** A dried bu assembly with function prologue and epilogue. No allocation on stack.

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

**Reality:** We got an assembly to call printf, but no allocation on stack.

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

Here, we are not subtracting to allocate space. Instead, we are using `rbp` as a reference point (for the current stack frame) and subtracting 4 bytes from there. Then we are storing 45 at the 4th block (byte).

You may ask, isn't the stack misaligned here? The answer is NO.

* We are moving `rbp` relative, not `rsp` relative. `rsp` is still 16-bytes aligned.
* Compiler optimization, you know!

Doesn't this behavior makes it hard for accessing the value? Let's see.

***

**Change:** This time we are also accessing the value.

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

**Result:** There you go. Now it is using subtraction because there is need for it.

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

### Experiment 2

```c
#include <stdio.h>

int main(void){
  static int num;
}
```

**Expectation:** Since this declaration is **static** and **uninitialized**, we are expecting an entry in `.bss`.

**Reality:** Function prologue and epilogue only.

**Conclusion:** The case of "uninitialized declaration" is applicable here as well.

***

**Change:** Declare and Use

```c
#include <stdio.h>

int main(void){
  static int num;
  printf("%d", num);
}
```

**Expectations:**

1. An entry in `.data` section reserving 4 bytes as we are using this declaration later in the program.
2. `printf` should give 0 in output because static/globals are zero initialized at runtime.

**Curious:** Where it would be allocated?

**Reality:** It prints zero so that is verified.

Lets talk about assembly.

```nasm
main:
;prologue
	push	rbp
	mov	rbp, rsp
; Preparation for printf
	mov	eax, DWORD PTR num.0[rip]
	mov	esi, eax
	lea	rax, .LC0[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT
; epilogue
	mov	eax, 0
	pop	rbp
	ret
; Memory Allocation
	.local	num.0
	.comm	num.0,4,4
```

* `num.0` is the label that is for our variable `num`.
* `.local` is a GAS directive which controls the visibility of `num.0`, it makes it file scoped.
* `.comm` is a GAS directive which allocates memory in `.bss`. `num.0, 4, 4` means allocate 4 bytes for `num.0` and align the storage by 4 bytes for efficient access. 4 bytes of alignment because it is an integer.

So, the allocation is indeed in `.bss` and we can further verify this with readelf if we are still unsure.

***

**Change:** Declare + Initialize

```c
#include <stdio.h>

int main(void){
  static int num = 15;
}
```

**Expectation:** Declaration should be in `.data` as we are initializing it directly.

**Reality:** Indeed.

```nasm
main:
	push	rbp
	mov	rbp, rsp
	mov	eax, 0
	pop	rbp
	ret
; Reserving space
	.data
	.align 4
	.type	num.0, @object
	.size	num.0, 4
; Allocation
num.0:
	.long	15

```

Although it is clear, but there is one question, what's the purpose of `.size`? It's extra bookkeeping.

* For example, 4 can belong to multiple casts of int, if you know `<inttypes.h>`. Which one it exactly belongs to? This metadata can be kept by using the `.size` directive.

