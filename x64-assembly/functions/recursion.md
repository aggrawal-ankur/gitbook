# Recursion (Recursive Function)

## Definition

## Factorial

A loop based program to calculate factorial

```c
int factorial(int n){
  if (n == 0){
    return 1;
  }
  int f = 1;
  for (int i = 1; i <= n; i++){
    f *= i;
  }
  return f;
}
```

How to do this with recursion?

*   If you remember, the formula to calculate the factorial of a number is:&#x20;

    ```nb
    n! = n * (n - 1) * (n - 2) * .... * (n - (n-1))
    ```

    We just have to implement this function.
* We know that the `0!` is `1` and factorial is not defined for negative integers. This means the `0!` forms the base case, something you can't go after.
* To calculate `5!`, we would have to work like: `5 * 4 * 3 * 2 * 1` we stop just before hitting zero.

Thus, recursion can be implemented as:

```c
#include <sdtio.h>

int rec_fact(int n){
  if (n == 0){
    return 1;
  }
  return (n * rec_fact(n - 1));
}

int main(){
  int n = 5;
  rec_fact(n);
}
```

This the assembly.

```nasm
	.text
	.globl	rec_fact
	.type	rec_fact, @function
rec_fact:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16

	mov	DWORD PTR -4[rbp], edi		; n received as func arg is moved to stack

	cmp	DWORD PTR -4[rbp], 0		; (n == 0) check
	jne	.L2				   ; if not, prepare for next call
	mov	eax, 1
	jmp	.L3				   ; if yes, we've hit the base case

; return n * rec_fact(n - 1)
.L2:
	mov	eax, DWORD PTR -4[rbp]		; load n in eax
	sub	eax, 1				; eax = eax - 1 OR ( n - 1)
	mov	edi, eax			; setup arg1 = eax
	call	rec_fact			; call again
	imul	eax, DWORD PTR -4[rbp]		; when the function call hit the base case, and there is a return, multiply the return (rax) with n
.L3:
	leave
	ret

	.globl	main
	.type	main, @function
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16
	mov	DWORD PTR -4[rbp], 5
	mov	eax, DWORD PTR -4[rbp]
	mov	edi, eax
	call	rec_fact
	mov	eax, 0
	leave
	ret
```

The assembly is pretty simple. Lets do a dry run and understand the state of stack and how the original value of `n` and returns are managed.

***

Procedures receive the first 6 arguments in registers, where the first one goes into `edi` .

* But in a continuous recursion, `edi` is constantly in use, which makes it unreliable to store the original `n`.
* We may have used other registers. We may have tried managing the caller/callee discipline ourselves. But, there are two problems.
  * There is no standardized way to do it. We can implement the above thing when we write pure assembly.
  * There is no limit to how many arguments a function can receive, which makes relying on registers a mess.
* When we are translating a language into another one, we would better prefer a more safe and consistent way to do it.
* That's the reason behind creating a local copy of `n` on stack. This keeps the original value intact and the `rdi` is also free.

```
4008: rsp

        *------------------*
4000 -> | old rbp on stack | (push rbp)
        *------------------*
           new rbp = 4000
        Stack Frame: main()
        *------------------*
3996 -> | edi (n = 5)      | -4[rbp]
        *------------------*
3992 -> |                  | -8[rbp]
        *------------------*
3988 -> |                  | -12[rbp]
        *------------------*
3984 -> |                  | -16[rbp]
        *------------------*
3976 -> | addr(mov eax, 0) |
        *------------------*
3968 -> | main() rbp [4000]|
        *------------------*
           new rbp = 3968
       Stack Frame: rec_fact()
        *------------------*
3964 -> | edi (n = 5)      | -4[rbp]
        *------------------*
3960 -> |                  | -8[rbp]
        *------------------*
3956 -> |                  | -12[rbp]
        *------------------*
3952 -> |                  | -16[rbp]
        *------------------*
3944 -> | addr(imul eax, 5)|
        *------------------*
3936 -> | old rbp [3968]   |
        *------------------*
           new rbp = 3936
       Stack Frame: rec_fact()
        *------------------*
3932 -> | edi (n = 4)      | -4[rbp]
        *------------------*
3928 -> |                  | -8[rbp]
        *------------------*
3924 -> |                  | -12[rbp]
        *------------------*
3920 -> |                  | -16[rbp]
        *------------------*
3912 -> | addr(imul eax, 4)|
        *------------------*
3904 -> | old rbp [3936]   |
        *------------------*
           new rbp = 3904
       Stack Frame: rec_fact()
        *------------------*
3900 -> | edi (n = 3)      | -4[rbp]
        *------------------*
3896 -> |                  | -8[rbp]
        *------------------*
3892 -> |                  | -12[rbp]
        *------------------*
3888 -> |                  | -16[rbp]
        *------------------*
3880 -> | addr(imul eax, 3)|
        *------------------*
3872 -> | old rbp [3904]   |
        *------------------*
           new rbp = 3872
       Stack Frame: rec_fact()
        *------------------*
3868 -> | edi (n = 2)      | -4[rbp]
        *------------------*
3864 -> |                  | -8[rbp]
        *------------------*
3860 -> |                  | -12[rbp]
        *------------------*
3856 -> |                  | -16[rbp]
        *------------------*
3848 -> | addr(imul eax, 2)|
        *------------------*
3840 -> | old rbp [3872]   |
        *------------------*
           new rbp = 3840
       Stack Frame: rec_fact()
        *------------------*
3836 -> | edi (n = 1)      | -4[rbp]
        *------------------*
3832 -> |                  | -8[rbp]
        *------------------*
3828 -> |                  | -12[rbp]
        *------------------*
3824 -> |                  | -16[rbp]
        *------------------*
3816 -> | addr(imul eax, 1)|
        *------------------*
3808 -> | old rbp [3840]   |
        *------------------*
           new rbp = 3808
       Stack Frame: rec_fact()
        *------------------*
3804 -> | edi (n = 0)      | -4[rbp]
        *------------------*
3800 -> |                  | -8[rbp]
        *------------------*
3796 -> |                  | -12[rbp]
        *------------------*
3792 -> |                  | -16[rbp]
        *------------------*

```















