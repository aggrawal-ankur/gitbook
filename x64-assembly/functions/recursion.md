# Recursion (Recursive Function)

_**04 September 2025**_

***

## Definition

A recursive function is a function that calls itself during its execution to solve a problem by breaking it down into smaller, simpler instances of the same problem.

It requires a **base case**, which is the stopping condition that prevents infinite calls, and a **recursive step** where the function calls itself with a modified input.

There are a lot of problems which can be implemented recursively, but for our use case, factorial is the best one. Why? Because it is very straightforward.

* Problems like Tower of Hanoi and Fibonacci series can be solved with recursion but it is a little complicated to understand.
* But we can definitely touch that once we complete factorial.

***

Recursion is the ideal next step to understand:

1. how stack frames are stacked?
2. how stack frame returns?
3. how locals are managed?

## Factorial

To calculate the factorial of a number, we use this formula:

```nb
n! = n * (n - 1) * (n - 2) * .... * (n - (n-1))
```

* where `n` is a positive integer and the factorial of 0 is 1.

For example - `5! = 120`, which is calculated as:

* `5 * (5 - 1) * (5 - 2) * (5 - 3) * (5 - 4)`&#x20;
* `5 * 4 * 3 * 2 * 1`&#x20;
* `120`&#x20;

A loop based program would be:

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

To do this with recursion, we need a base condition and recursive condition.

* Base condition: `0! = 1`.
* Recursive condition: `n * func(n - 1)`&#x20;

The idea is that each recursive call reduces the value of `n`  until it becomes 0. When it becomes zero, return is triggered. And the final return computes `n!` .

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

; return
.L3:
	leave
	ret

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

The assembly is straightforward, so we will skip that. Lets do a dry run and understand the state of stack, because, we already know what the code is doing.

***

Procedures receive the first 6 arguments in registers, where the first one goes into `edi` . But in a continuous recursion, `edi` is constantly in use, which makes it unreliable to keep the original value of `n`.

* We can use other registers? We can manage the caller/callee discipline ourselves?
* We can, but we've to deal with two problems.
  * We can only implement this when we write pure assembly.
  * There is no limit to how many arguments a function can receive, which makes relying on registers a mess.
* We are compiling C into assembly. When we are translating a language into another one, we would prefer standard rules which remain consistent over edge cases.
* That's the reason behind creating a local copy of `n` on stack. This keeps the original value intact, stack frames clean and predictable and no management hell.

***

We can talk theory all the day, but how one interprets that theory changes everything. And the best way to ensure that we are on the same page is by visualizing the stack.

**Note: This visual representation of stack might not be very accurate, but it explains things in a way that ensures that all of use are interpreting the theory the right way.**

With this ASCII Art, we can draw the theory. That's the main thing.

All the addresses are in decimal, no hex is used as it creates an overhead of calculation. The addresses are kept deliberately small so that **subtraction of bytes** is easier to calculate.

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
3968 -> | main() rbp (4000)|
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
3936 -> | old rbp (3968)   |
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
3904 -> | old rbp (3936)   |
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
3872 -> | old rbp (3904)   |
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
3840 -> | old rbp (3872)   |
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
3808 -> | old rbp (3840)   |
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

* If you have noticed, the addresses feel inconsistent. The difference is oscillating between 4 and 8.
* That's because, a direct `push` is a shorthand for subtracting 8 bytes and moving a value at that memory. When we reserve 16 bytes separately, those bytes are used to store an integer, which is why they are 4-byte aligned as an integer is normally sized 4-bytes.

This ASCII drawing has stopped at `(n = 0)` as we have reached the base condition. Now the stack frames will be removed one-by-one. Let's see how that works.



CONTINUE FROM HERE



For instant access, this is a compressed look of stack:

```
| Stack Frame | rbp  | n |
*-------------*------*---*
| main        | 4000 | 5 | <- Bottom
| rec_fact    | 3968 | 5 |
| rec_fact    | 3936 | 4 |
| rec_fact    | 3904 | 3 |
| rec_fact    | 3872 | 2 |
| rec_fact    | 3840 | 1 |
| rec_fact    | 3808 | 0 | <- Top
```

The top stack frame is the one with `rbp=3808` . Let's have a look at the assembly.

* If `(n==0)` , we jump to `.L3` , not `.L2` .
*   The `leave` instruction resets the stack pointer by using `rbp`&#x20;

    ```
    mov rsp, rbp
    ```

    and pops the old base pointer (located in `rsp`) into `rbp`, which changes the current base pointer to the previous stack frame.&#x20;

    ```
    pop rbp
    ```
*   The `leave` instruction is doing:

    ```
    mov rsp, 3808
    mov rbp, 3840       ; [3808] = 3840
    add rsp, 8
    ```
* Now `rsp` is at `3816`.
* So far, we have partially entered into the old context as the `rbp` is updated. But the context restoration happens when `ret` instruction is executed.
*   When we do `pop rip`, it is:&#x20;

    ```
    mov rip, [3816]
    ```

    dereferencing 3816 gives the address of `imul eax, DWORD PTR -4[rbp]` instruction in the previous stack frame (3840).
* And we have successfully returned to the previous stack frame, the one with `rbp=3840` .
*   What about return value? We have set `1` in `eax` already.

    ```
    	cmp	DWORD PTR -4[rbp], 0
    	jne	.L2
    	mov	eax, 1
    	jmp	.L3
    ```
*   So,

    ```
    imul eax, DWORD PTR -4[rbp]
    ```

    translates to&#x20;

    ```
    imul 1, 1
    ```

    as we are inside the `3840` frame, `n=1` .









