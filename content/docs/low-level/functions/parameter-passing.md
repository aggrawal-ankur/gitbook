---
id: d2c671c57f4e4bc5b37e227f1df99b6e
title: Parameter Passing
weight: 3
---

_**5 September 2025**_

***

## Parameters and Arguments

Parameters are variables defined in a function definition that act as placeholders for values the function will receive.

Arguments are the actual values supplied to a function when it is called.

For example:

```c
#include <stdio.h>

int square(int n){
  return n*n;
}

int main(){
  square(5);
}
```

* Here, `n` is parameter and `5` is the argument.

## Parameter Passing

Functions can receive arguments from the caller. These arguments can be passed in two ways.

1. Call by value -> a copy of the actual value is passed.
2. Call by reference -> the memory address of the value is passed, allowing the function to modify the original variable.

Let's take an example. We have a number and we want to increment it by 10.

```c
#include <stdio.h>

void inc1(int n){
  printf("Inside inc1\n");
  printf("  Before increment: %d\n", n);
  n += 10;
  printf("  After increment: %d\n", n);
}

void inc2(int *m){
  printf("Inside inc2\n");
  printf("  Before increment: %d\n", *m);
  *m += 10;
  printf("  After increment: %d\n", *m);
}

int main(){
  int n = 2;
  printf("In main\n");
  printf("  Before increment: %d\n", n);
  inc1(n);
  printf("In main\n");
  printf("  After increment: %d\n", n);

  printf("\n--------\n\n");

  int m = 4;
  printf("In main\n");
  printf("  Before increment: %d\n", m);
  inc2(&m);
  printf("In main\n");
  printf("  After increment: %d\n", m);
}
```

When we normally pass a value, a copy of it is passed. When we pass the reference of a value, the memory address at which it is stored is passed, which is why the change persists after function call.

* **Swapping two numbers** is very famous in this space.

## Assembly Comparison

This is call by value.

```c
#include <stdio.h>

void sq(int n){
  int s = n*n;
  printf("%d\n", s);
}

int main(){
  sq(5);
}
```

And there is nothing new.

```nasm
.LC0:
	.string	"%d\n"

sq:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16

	mov	DWORD PTR -4[rbp], edi               ; 5
	mov	eax, DWORD PTR -4[rbp]
	imul	eax, eax                             ; 25
	mov	DWORD PTR -4[rbp], eax               ; update local n

	mov	eax, DWORD PTR -4[rbp]
	mov	esi, eax
	lea	rax, .LC0[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT

	nop
	leave
	ret

main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16

	mov	DWORD PTR -4[rbp], 5
	mov	eax, DWORD PTR -4[rbp]
	mov	edi, eax
	call	sq

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

This is call by reference.

```c
#include <stdio.h>

void sq(int* n){
  *n = (*n)*(*n);
  printf("%d\n", *n);
}

int main(){
  int num = 5;
  sq(&num);
  printf("%d\n", num);
}
```

This is the assembly.

```nasm
.LC0:
	.string	"%d\n"

sq:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16

	mov	QWORD PTR -8[rbp], rdi          ; address of num passed from main
	mov	rax, QWORD PTR -8[rbp]
	mov	edx, DWORD PTR [rax]
	mov	rax, QWORD PTR -8[rbp]
	mov	eax, DWORD PTR [rax]
	imul	edx, eax                     	; 5 * 5

	mov	rax, QWORD PTR -8[rbp]          ; load the address of -8[rbp]
	mov	DWORD PTR [rax], edx            ; mov the updated value of n (n*n)

	mov	rax, QWORD PTR -8[rbp]
	mov	eax, DWORD PTR [rax]
	mov	esi, eax
	lea	rax, .LC0[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT

	nop
	leave
	ret

main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16

	mov	DWORD PTR -4[rbp], 5
	lea	rax, -4[rbp]                    ; We are loading the address of 4[rbp], not what is at -4[rbp]
	mov	rdi, rax
	call	sq

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

And the fun begins here. Let's start with the `main` symbol.

*   In call by value assembly, we load the value at stack memory:

    ```nasm
    mov eax, DWORD PTR -4[rbp]
    ```

    In call by reference, we are computing the address where 5 is in the stack memory:

    ```nasm
    lea rax, -4[rbp]
    ```
* In call by reference, the compiler uses 64-bit registers for the pointer, because addresses on a 64-bit system are 8 bytes. The integer itself is 4 bytes, so we still use 32-bit registers for arithmetic.
* The rest is the same.

***

Let's shift our focus on the `sq` symbol now.

*   In call by value, we are moving a 4-byte value at `-4[rbp]`, which is 5.

    ```nasm
    mov DWORD PTR -4[rbp], edi
    ```

    In call by reference, we are moving a 8-byte value, and we know that an integer is not sized "8-bytes" by default on Linux. This again reinforces the fact that this is a pointer to/address of 5, not 5 itself.

    ```nasm
    mov QWORD PTR -8[rbp], rdi
    ```
*   The call by value code simply loaded the local instance of `n` in `eax` , multiplied with itself and updated the local instance with new value.

    ```nasm
    mov   eax, DWORD PTR -4[rbp]
    imul  eax, eax
    mov   DWORD PTR -4[rbp], eax
    ```

    This is quite complicated for the call by reference program.
*   First we load 8-bytes starting from `-8[rbp]`.

    ```nasm
    mov   rax, QWORD PTR -8[rbp]
    ```

    Next we dereference the address to obtain the actual value (5). Since it is a 32-bit value, we are using `DWORD` to move it in `edx` .

    ```nasm
    mov   edx, DWORD PTR [rax]
    ```

    We repeat the same process to hold 5 in another register for multiplication.

    ```nasm
    mov   rax, QWORD PTR -8[rbp]
    mov   eax, DWORD PTR [rax]
    ```
* We are using different registers here to avoid overwriting values that are still required for computation.
*   Now we have to update the existing instance of stack with 25. In call by value, it was again quite simple.

    ```nasm
    mov   DWORD PTR -4[rbp], eax
    ```

    In call by reference, first we have to load the 8-bytes of address in `rax`:

    ```nasm
    mov   rax, QWORD PTR -8[rbp]
    ```

    Then we dereference it and mov 25 there.
* After this we print the value.

And that's how call by reference works.

## But what is the utility of call by reference?

That's the only way stack frames can interact.

That's the only way stack frames can manage complex data.

Pointers are the _**only**_**&#x20;mechanism** that lets a function access memory outside its own frame