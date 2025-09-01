---
layout:
  width: wide
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: false
---

# Arrays

_**1 September 2025**_

***

## Premise

Arrays are just consecutive blocks of memory interpreted together as a collection.

We are already familiar with theory so we will focus on practical only.

To avoid mentioning red zone every time, we will use a printf to make main a non-leaf function.

## Example 1: Declaration Only

```c
#include <stdio.h>

int main(void){
  int arr[5];
}
```

```nasm
	.text
	.globl	main
	.type	main, @function
main:
	push	rbp
	mov	rbp, rsp
	mov	eax, 0
	pop	rbp
	ret
```

As expected, there is no reservation on stack.

***

## Example 2 - Declare and Use (No init)

If you run a for loop on the previous program to print all the values, you will find garbage values.

***

## Example 3 - Declaration + Initialization

```c
#include <stdio.h>

int main(void){
  int arr[5] = {1, 2, 3, 4, 5};
  printf("Hello\n");
}
```

We need `5*4 = 20 bytes` on stack and the closest round off for 20 is 32 so 32 bytes will be reserved on stack.

```nasm
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 32
	mov	DWORD PTR -32[rbp], 1
	mov	DWORD PTR -28[rbp], 2
	mov	DWORD PTR -24[rbp], 3
	mov	DWORD PTR -20[rbp], 4
	mov	DWORD PTR -16[rbp], 5
```

**Note: If you do not mention 5 explicitly, the assembly generated is no different, which proves that the calculation for size allocation is done at compilation level.**

***

## Example 4 - Empty Initialization

```c
#include <stdio.h>

int main(void){
  int arr[5] = {};
}
```

This is the assembly.

```nasm
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 32

	pxor	xmm0, xmm0
	movaps	XMMWORD PTR -32[rbp], xmm0
	movaps	XMMWORD PTR -16[rbp], xmm0
```

The 3 instructions above are used to zero-initialize the 5 elements at runtime.

We could have used simple `mov` instructions or even `xor` to do the same thing, why these instructions then? First of all, we can definitely do that. If we use `-mno-sse -mno-sse2 -mno-avx` flags with `gcc` , we can see that the compiler now uses `mov`.

```nasm
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 32
	mov	QWORD PTR -32[rbp], 0
	mov	QWORD PTR -24[rbp], 0
	mov	QWORD PTR -16[rbp], 0
	mov	QWORD PTR -8[rbp], 0
```

If we change from `arr[5]` to `arr[100]` and keep these flags, we'd expect too many `mov` instructions. Let's see.

```nasm
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 400
	lea	rdx, -400[rbp]
	mov	eax, 0
	mov	ecx, 50
	mov	rdi, rdx
	rep stosq
```

This was completely out of the blue. And the best part is yet to come. I tried to compile the `arr[5]` code again and now I have a slightly different assembly. The number of `mov` instructions reduced.

```c
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 32
	mov	QWORD PTR -20[rbp], 0
	mov	QWORD PTR -12[rbp], 0
	mov	DWORD PTR -4[rbp], 0
```

Now the question is, what's happening here?

* Modern compilers are optimization monsters. They have evolved for decades and now they have too many tricks under their sleeves. You close one door and another is opened.
* Compilers search for the most efficient way to do something, and that depends on so many parameters. This is why there is always a possibility that two identical systems in an identical environment with the same compiler can generate a different assembly. The extent of difference also varies.
* The generated assembly has no guarantee to be the same, but the intent remains the same, always.

That's why I didn't jumped on explaining what are `pxor` and `movaps`. I wanted to prove the point that _understanding the intent is a far better strategy than understanding every optimization that the compiler can make to do the same thing. There is no end to it._

***

So, what's the intent here?

* The intent is to zero-initialize the array. **Efficiently is always present.**
* SIMD instructions are one way to do that. They stand for **single instruction, multiple data**. They help you operate efficiently on a group of data in one single instruction, reducing the total number of instructions required to operate on a large chunk of data.
* And, with the idea of intent, that's all we need to know about SIMD instructions right now. Otherwise, this would have spiraled into a SIMD tutorial.

***

_So, when we do empty initialization, the array is zero-initialized._

_Note: When we use an uninitialized array, the elements have garbage value, by default, in `auto` class, obviously._

***

## Example  5 - Incomplete Initialization

We are declaring an array of 5 elements but we are not initializing all the 5 elements.

```c
#include <stdio.h>

int main(void){
  int arr[5] = {1, 2, 3};
  printf("Hello\n");
}
```

If you printf all the 5 values using a loop, you will find that 3rd and 4th positions are zeroed out. Let's see what the assembly says.

```nasm
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 32

	; Zero-initialize the array
	pxor	xmm0, xmm0
	movaps	XMMWORD PTR -32[rbp], xmm0
	movd	DWORD PTR -16[rbp], xmm0

	; Initialize the positions from starting
	mov	DWORD PTR -32[rbp], 1
	mov	DWORD PTR -28[rbp], 2
	mov	DWORD PTR -24[rbp], 3
```

An uninitialized array has garbage values but an initialized one should have values properly.

When you initialize the array completely along the length, there is no need for zeroing out. Here, we are doing partial initialization, which is why we need to zero-initialize the array so that each element has a proper value, then we are initializing the positions which have received a value.

***

## Example 6 - Variable Length Allocation













