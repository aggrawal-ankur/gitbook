# Parameter Passing

## Parameters and Arguments

Parameters are defined in function definition, which act as placeholders.

Arguments are the actual value passed in the function call.

For example:

```c
#include <stdio.h>

int square(int n){
  return n*n
}

int main(){
  square(5);
}
```

* Here, `n` is parameter and `5` is the argument.

## Passing Methods

Parameters can be passed in two ways:

1. A copy of the actual value.
2. The value directly.

This is what call by value and call by reference is.

Let's take an example. We have a number and we want to increment it by 10.

```c
#include <stdio.h>

int inc1(int n){
  printf("Inside inc1\n");
  printf("  Before increment: %d\n", n);
  n += 10;
  printf("  After increment: %d\n", n);
}

int inc2(int *m){
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

When we normally pass a value, a copy of it is passed. When we pass the reference of a value, the memory address at which it is stored is passed, which is why the change persist after function call.

* Swapping two numbers problem is very famous in this space.

## Distinction

Lets see how the assembly differs for both the methods.

This is call by value, the one we have been exploring all this time.

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

As you can see, nothing new. We are copying the value and passing it to the procedure.

Lets talk about reference now.

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

	mov	QWORD PTR -8[rbp], rdi          ; reference of 5
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

    In call by reference, we are computing the address where 5 is loaded:

    ```nasm
    lea rax, -4[rbp]
    ```
* Since integers are interpreted as 4-bytes here, call by value assembly uses 32-bit registers. Although we can say that compiler optimized it but the call by value one used 64-bit registers and no optimization is possible by default as pointers are 8-bytes in size in 64-bit Linux.
* The rest is the same in both.

***

Let's shift our focus on the `sq` symbol now.

*   In call by value, we are moving a double word value, which is 5.

    ```nasm
    mov DWORD PTR -4[rbp], edi
    ```

    In call by reference, we are moving a quad word value, and we know that an integer is not sized "quad-word" or "64-bits" by default on Linux. This again reinforces the fact that this is a pointer to/address of 5, not 5 itself.

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
*   First we are loading the quad-word address in `rax`.

    ```nasm
    mov   rax, QWORD PTR -8[rbp]
    ```

    Now we are dereferencing the quad-word value (address) to obtain the actual value (5) and we are moving the 32-bit version of it in `edx` as there is no need to waste computation. _Compiler optimization, basically._

    ```nasm
    mov   edx, DWORD PTR [rax]
    ```

    Now we are repeating the same process to hold a 32-bit version of 5 in another register for multiplication.

    ```nasm
    mov   rax, QWORD PTR -8[rbp]
    mov   eax, DWORD PTR [rax]
    ```
* By the way, why we have to use separate registers here when we have used the same previously?
*   Now the updated value `25` has to update the existing instance of stack. In call by value, it was again quite simple.

    ```nasm
    mov   DWORD PTR -4[rbp], eax
    ```

    In call by reference, first we have to load the quad-word address in `rax`:

    ```nasm
    mov   rax, QWORD PTR -8[rbp]
    ```

    Then we dereference it and mov a 32-bit version of 25.
* After this we print the value, which is different again but we are now familiar with the difference at this point.

And that's how call by reference works.

But, what is the utility of it? Let's find that.

***

## The Need Of Call By Reference

```c
#include <stdio.h>

void printArray(){
  
}

int main(){
  int a;
}
```







