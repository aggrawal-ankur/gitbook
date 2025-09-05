# Recursion (Recursive Function)

_**04 September 2025**_

***

## Definition

A recursive function is a function that calls itself during its execution to solve a problem by breaking it down into smaller, simpler instances of the same problem.

It requires a **recursive step** where the function calls itself with a modified input and a **base case**, which is the stopping condition that prevents infinite calls.

These recursive case and base case are the things that makes a recursion either easy to understand or very complex. For this reason, we are using **factorial**, because it is very straightforward.

* Problems like Tower of Hanoi and Fibonacci series can be solved with recursion but they are a little complex to understand.
* But we can definitely touch that later.

***

Recursion is the ideal next step to understand:

1. how stack frames are "stacked"?
2. how stack frame returns?
3. how arguments are managed across calls?

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
#include <stdio.h>

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
	push rbp
	mov  rbp, rsp
	sub  rsp, 16

	mov DWORD PTR -4[rbp], edi		; n received as func arg is moved to stack

	cmp  DWORD PTR -4[rbp], 0		; (n == 0) check
	jne  .L2				; if not, prepare for next call
	mov  eax, 1
	jmp  .L3				; if yes, we've hit the base case

; return n * rec_fact(n - 1)
.L2:
	mov  eax, DWORD PTR -4[rbp]		; load n in eax
	sub  eax, 1				; eax = eax - 1 OR ( n - 1)
	mov  edi, eax				; setup arg1 = eax
	call rec_fact				; call again
	imul eax, DWORD PTR -4[rbp]		; when the function call hit the base case, and there is a return, multiply the return (rax) with n

; return
.L3:
	leave
	ret

main:
	push rbp
	mov  rbp, rsp
	sub  rsp, 16
	mov  DWORD PTR -4[rbp], 5
	mov  eax, DWORD PTR -4[rbp]
	mov  edi, eax
	call rec_fact
	mov  eax, 0
	leave
	ret
```

Procedures receive the first 6 arguments in registers, where the first one goes into `edi` . But in a continuous recursion, `edi` is constantly in use, which makes it unreliable to keep the original value of `n`.

* We can use other registers? We can manage the caller/callee discipline ourselves?
* We can, but we've to deal with two problems.
  * We can only implement this in pure assembly.
  * There is no limit to how many arguments a function can receive, which makes relying on registers a mess.
* We are compiling C into assembly. When we are translating one language into another one, we would prefer standard rules which remain consistent across all the cases.
* That's the reason behind creating a local copy of `n` on stack. This keeps the original value intact, stack frames clean and predictable and no management hell.

***

The assembly is straightforward, so we will skip that. Lets do a dry run and understand the state of stack, because, we already know what the code is doing.

## Stack Layout

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

* If you notice, the addresses feel inconsistent. The difference is oscillating between 4 and 8.
* That's because a direct `push` is a shorthand for subtracting 8 bytes and moving a value at that memory. When we reserve 16 bytes separately, and they bytes are used to store an integer, they are 4-byte aligned for efficient memory access, as an integer is normally 4-bytes in size.

This ASCII Art has stopped at `(n = 0)` as we have reached the base condition. Now the frames will remove one-by-one. Let's see how that works.

***

## Return Management

This is a compressed view of stack.

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

* If you notice, each frame is exactly 32-bytes in size; 16 for locals, 8 for return address and 8 for old `rbp` .

### 3808 Frame

The top stack frame is `rbp=3808` , and is `rsp=3792` here. Let's look at assembly.

* If `(n==0)` , we set `eax``=1` (which is the return value) and jump to `.L3` .
*   The `leave` instruction resets the stack pointer by using `rbp`&#x20;

    ```
    mov rsp, 3808
    ```

    and pops the old base pointer (located in `rsp`) into `rbp`, which changes the current base pointer to the previous stack frame.&#x20;

    ```
    mov rbp, [3808]        ; [3808] = 3840
    add rsp, 8             ; rsp = 3816
    ```

    Now `rsp=3816` and `rbp=3840` .
*   When we do `pop rip`, it is:&#x20;

    ```
    mov rip, [3816]
    add rsp, 8             ; rsp = 3824
    ```

    dereferencing 3816 gives the address of `imul eax, DWORD PTR -4[rbp]` instruction in the previous stack frame (3840).
* And we have successfully returned to the previous stack frame, the one with `rbp=3840` .
* State of pointers: `rsp=3824` and `rbp=3840` .

***

### 3840 Frame

Now we are inside the `rbp=3840` stack frame.

* Here, `n``=1`. So, `.L2` was executed, which sets up the next recursion call.
* The next recursion call was `rbp=3808`, which successfully returned 1 in `eax` .
*   Now we are at:

    ```
    imul eax, DWORD PTR -4[rbp]
    ```
* For this stack frame, `rbp=3840`. `-4[3840]` would go to `3836` which stores a local copy of `n` received by this procedure's frame, which is `1` here.
*   So, the instruction translates to:

    ```
    imul eax, 1
    ```

    and `eax` is already 1, so the result in `eax` would be 1.
*   After this, `.L3` is called.

    ```
    ; leave
    mov rsp, 3840
    mov rbp, [3840]        ; [3840] = 3872
    add rsp, 8             ; rsp = 3848

    ; return
    mov rip, [3848]
    add rsp, 8             ; rsp = 3856
    ```
* And we have successfully returned to the previous stack frame, the one with `rbp=3872` .
* State of pointers: `rsp=3856` and `rbp=3872` .

***

### 3872 Frame

Now we are inside the `rbp=3872` stack frame.

* Here, `n``=2`. So, `.L2` was executed, which sets up the next recursion call.
* The next recursion call was `rbp=3840` , which successfully returned 1 in `eax`.
*   Now we are at:

    ```
    imul eax, DWORD PTR -4[rbp]
    ```
* For this stack frame, `rbp=3872` . `-4[3872]` would go to `3868` , which stores a local copy of `n` received by this procedure's frame, which is `2` here.
*   So, the instruction translates to:

    ```
    imul eax, 2
    ```

    &#x20;`eax` is 1, so the result in `eax` would be 2.
*   After this, `.L3` is called.

    ```
    ; leave
    mov rsp, 3872
    mov rbp, [3872]        ; [3872] = 3904
    add rsp, 8             ; rsp = 3880

    ; ret
    mov rip, [3880]
    add rsp, 8             ; rsp = 3888
    ```
* And we have successfully returned to the previous stack frame, the one with `rbp=3904` .
* State of pointers: `rsp=3888` and `rbp=3904` .

***

### 3904 Frame

Now we are inside the `rbp=3904` stack frame.

* Here, `n``=3`. So, `.L2` was executed, which sets up the next recursion call.
* The next recursion call was `rbp=3872` , which successfully returned 2 in `eax`.
*   Now we are at:

    ```
    imul eax, DWORD PTR -4[rbp]
    ```
* For this stack frame, `rbp=3904` , `-4[3904]` would go to `3900` , which stores a local copy of `n` received by this procedure's frame, which is `3` here.
*   So, the instruction translates to:

    ```
    imul eax, 3
    ```

    &#x20;`eax` is 2, so the result in `eax` would be 6.
*   After this, `.L3` is called.

    ```
    ; leave
    mov rsp, 3904
    mov rbp, [3904]        ; [3904] = 3936
    add rsp, 8             ; rsp = 3912

    ; ret
    mov rip, [3912]
    add rsp, 8             ; rsp = 3920
    ```
* And we have successfully returned to the previous stack frame, the one with `rbp=3936` .
* State of pointers: `rsp=3920` and `rbp=3936` .

***

### 3936 Frame

Now we are inside the `rbp=3936` stack frame.

* Here, `n``=4`. So, `.L2` was executed, which sets up the next recursion call.
* The next recursion call was `rbp=3904` , which successfully returned 6 in `eax`.
*   Now we are at:

    ```
    imul eax, DWORD PTR -4[rbp]
    ```
* For this stack frame, `rbp=3936` , `-4[3936]` would go to `3932` , which stores a local copy of `n` received by this procedure's frame. The value of `n` is `4` here.
*   So, the instruction translates to:

    ```
    imul eax, 4
    ```

    &#x20;`eax` is 6, so the result in `eax` would be 24.
*   After this, `.L3` is called.

    ```
    ; leave
    mov rsp, 3936
    mov rbp, [3936]        ; [3936] = 3968
    add rsp, 8             ; rsp = 3944

    ; ret
    mov rip, [3944]
    add rsp, 8             ; rsp = 3952
    ```
* And we have successfully returned to the previous stack frame, the one with `rbp=3968` .
* State of pointers: `rsp=3952` and `rbp=3968` .

***

### 3968 Frame

Now we are inside the `rbp=3968` stack frame.

* Here, `n``=5`. So, `.L2` was executed, which sets up the next recursion call.
* The next recursion call was `rbp=3936` , which successfully returned 24 in `eax`.
*   Now we are at:

    ```
    imul eax, DWORD PTR -4[rbp]
    ```
* For this stack frame, `rbp=3968` , `-4[3968]` would go to `3964` , which stores a local copy of `n` received by this procedure's , which is `5` here.
*   So, the instruction translates to:

    ```
    imul eax, 5
    ```

    &#x20;`eax` is 24, so the result in `eax` would be 120.
*   After this, `.L3` is called.

    ```
    ; leave
    mov rsp, 3968
    mov rbp, [3968]        ; [3968] = 4000
    add rsp, 8             ; rsp = 3976

    ; ret
    mov rip, [3976]
    add rsp, 8             ; rsp = 3984
    ```
* And we have successfully returned to the previous stack frame, the one with `rbp=4000` .
* State of pointers: `rsp=3984` and `rbp=4000` .

***

Now we are inside the `rbp=4000` stack frame.

* This is where we started from.
* From here, we return to the almighty gods of C, the startup code, which handles the exit and remaining cleanup.

***

Sigh. It was crazy, isn't it? Conclusion is still remaining.

## Conclusion

The only conclusion that is worth reading is that,&#x20;

_<mark style="color:$danger;">it's a hoax that low level systems are complex and impossible to understand without the help of some C God. It's a hoax that you can't draw theory, visualize theory. Any idea that restricts you from doing the work to build deep understanding is just a hoax. It takes time and it takes energy, but the output is worth every bit of effort.</mark>_

It took me a whole day to build this understanding and stack art, roughly \~7h accumulated.

* And the result of that is that I will never be confused about stack discipline.
* I am sure that stack is not done yet. There is a lot to explore. But I am also ready to do that, _**the hard way, the boring way, the repetitive way**_.
