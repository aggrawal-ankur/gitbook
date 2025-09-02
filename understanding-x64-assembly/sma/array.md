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

_**1, 2 September 2025**_

***

## Premise

Arrays are just consecutive blocks of memory interpreted together as a collection.

We use printf to make `main` a non-leaf function so that we don't get confused with red zone.

## Starters

We are already familiar with these concepts, so we just have to reinforce them for arrays.

### Example 1: Declaration Only

```c
#include <stdio.h>

int main(void){
  int arr[5];
}
```

```nasm
main:
	push	rbp
	mov	rbp, rsp
	mov	eax, 0
	pop	rbp
	ret
```

As expected, there is no reservation on stack.

***

### Example 2 - Declare and Use (No init)

If you print the elements, you will find garbage values.

***

### Example 3 - Declaration + Initialization

```c
#include <stdio.h>

int main(void){
  int arr[5] = {1, 2, 3, 4, 5};
  printf("Hello\n");
}
```

We need `5*4 = 20 bytes` on stack and the closest 16-bytes aligned round off for 20 is 32 so 32 bytes will be reserved on stack.

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

### Example 4 - Empty Initialization

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

We could have used simply `mov` instructions or even `xor` to do the same thing, why these instructions then? First of all, we can definitely do that. If we use `-mno-sse -mno-sse2 -mno-avx` flags with `gcc` , we can see that the compiler now uses `mov`.

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

This was completely unexpected, isn't it? And the best part is yet to come. I tried to compile the `arr[5]` code again and now I have a slightly different assembly. The number of `mov` instructions reduced.

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

* Modern compilers are **optimization monsters**. They have evolved for decades and now they have too many tricks under their sleeves. You close one door and another is opened.
* Compilers search for the most efficient way to do something, and that depends on so many parameters. This is why there is always a possibility that two identical systems in an identical environment with the same compiler can generate a different assembly. The extent of difference also varies.
* The generated assembly has no guarantee to be the same, but the intent remains the same, always.

That's why I didn't jumped on explaining what are `pxor` and `movaps`. I wanted to prove the point that _understanding the intent is a far better strategy than understanding every optimization that the compiler can make to do the same thing. There is no end to it._

***

So, what's the intent here?

* The intent is to zero-initialize the array, efficiently.
* SIMD instructions are one way to do that. They zero multiple integers in parallel, reducing instruction count and improving throughput. Here, `pxor` clears the register, and `movaps` writes aligned 128-bit blocks.
* For now, it's enough to know that SIMD zeroes multiple elements in parallel for efficiency. A deeper SIMD deep-dive deserves its own write-up.

***

_So, when we do empty initialization, the array is zero-initialized._

_Note: When we use an uninitialized array, the elements have garbage value, by default, in `auto` class, obviously._

***

### Example 5 - Incomplete Initialization

We are declaring an array of 5 elements but we are not initializing all the 5 elements.

```c
#include <stdio.h>

int main(void){
  int arr[5] = {1, 2, 3};
  printf("Hello\n");
}
```

If you printf the elements, you will find that 3rd and 4th positions are zeroed out. Let's have a look at assembly.

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

When you initialize the array completely along the length, there is no need to zero before. Here we are doing partial initialization, which is why we need to zero-initialize the array so that each element has a proper value, then we are initializing the initial from starting positions with specified values.

***

## Variable Length Allocation

This is the most important one here.

If you do:

```c
int n = 5;                // Known at compile-time
int arr[n];

int m;                    // Not known at compile-time
scanf("%d", &m);
int arr[m];
```

Both are identified as variable length allocation, even though `n` is known at compile time, the compiler triggers code for VLA.

What makes VLA different is that you have to calculate the total bytes required to be allocated on stack.

* As of now (_September 2, 2025_) I don't know why the compiler emitted code for VLA when `n` is known at compile-time.
* Although the idea remains the same in both the cases, I'd suggest to keep the "**not known at compile-time**" case in reference because it would not make any sense in the other one.

***

Since `n` is not known beforehand, we can't allocate stack in one single instruction. We follow a structured process to allocate stack.

### Steps In VLA

1. Allocate space for things defined at compile-time.
2. Ensure `n` is populated, either at compile-time or runtime.
3. Calculate the bytes required by `type arr[n]` declaration.
4. Calculate the padding required for 16-bytes alignment for `rsp`.
5. Allocate space for the array.
6. Align the base address of the array, `arr[0]` to be 4-bytes.

### Example

```c
#include <stdio.h>

int main(void){
  int n;                // Not known at compile-time
  scanf("%d", &n);

  int arr[n];
  printf("%d", arr[0]);
}
```

Normally integer is sized 4-bytes, so the total requirement is given by `n*4` bytes.

Now we have to calculate padding. Lets see how much padding is required for `n ∈ {1....8}`

<table><thead><tr><th width="246">Value of n</th><th>Bytes required</th><th>Padding Bytes</th></tr></thead><tbody><tr><td>1</td><td>1*4 = 4</td><td>16 - 4 = 12</td></tr><tr><td>2</td><td>2*4 = 8</td><td>16 - 8 = 8</td></tr><tr><td>3</td><td>3*4 = 12</td><td>16 - 12 = 4</td></tr><tr><td>4</td><td>4*4 = 16</td><td>16 - 16 = 0</td></tr><tr><td>5</td><td>5*4 = 20</td><td>32 - 20 = 12</td></tr><tr><td>6</td><td>6*4 = 24</td><td>32 - 24 = 8</td></tr><tr><td>7</td><td>7*4 = 28</td><td>32 - 28 = 4</td></tr><tr><td>8</td><td>8*4 = 32</td><td>32 - 32 = 0</td></tr></tbody></table>

This shows that the value for padding for a 4-byte integer belongs to `{0, 4, 8, 12}` . Plus, when the total bytes required are greater than the closest 16-divisible digit, we take the next 16-divisible digit.

From this information, we can create a simple program to calculate the total bytes required.

```c
#include <stdio.h>

int main(void){
  int n;
  printf("Enter n: ");
  scanf("%d", &n);

  int l, u;
  int bytes = n * sizeof(int);

  if (bytes % 16 == 0){
    printf("Voila... It is a multiple of 16!\n");
    return 0;
  }
  else if (bytes % 16 > 8){
    u = bytes + ((bytes % 16) - 8);
    l = u - 16;
  }
  else{
    l = bytes - ((bytes % 16));
    u = l + 16;
  }

  printf("u: %d\n", u);
  printf("l: %d\n", l);
  printf("\n Allocate %d bytes on stack.\n", u);
}
```

This program "efficiently" calculates how much `n*sizeof(int)` defers from a multiple of 16. And that's basically the "intent" behind variable length allocation. _We have to calculate how far we are from the next multiple of 16. Once we get this value, we can allocate space on stack._

By the way, this is just one way to do it. Let's see how the compiler does it.

```nasm
	.text
	.section	.rodata
.LC0:
	.string	"%d"
	.text
	.globl	main
	.type	main, @function
main:
	; init
	push	rbp
	mov	rbp, rsp
	push	rbx
	sub	rsp, 40
	mov	rax, rsp
	mov	rbx, rax				; save rsp in rbx

	; scanf("%d", &n)
	lea	rax, -36[rbp]				; &n
	mov	rsi, rax				; arg2 = &n
	lea	rax, .LC0[rip]				; "%d"
	mov	rdi, rax				; arg1 = "%d"
	mov	eax, 0
	call	__isoc99_scanf@PLT

	; calculate total bytes required
	mov	eax, DWORD PTR -36[rbp]
	movsx	rdx, eax
	sub	rdx, 1
	mov	QWORD PTR -24[rbp], rdx
	cdqe
	lea	rdx, 0[0+rax*4]

	; calculate padding required for 16-bytes alignment of rsp
	mov	eax, 16
	sub	rax, 1
	add	rax, rdx
	mov	ecx, 16
	mov	edx, 0
	div	rcx
	imul	rax, rax, 16

	; reserve space for array
	sub	rsp, rax

	; Make the base address of array (arr[0]) 4-byte aligned, if not
	mov	rax, rsp
	add	rax, 3
	shr	rax, 2
	sal	rax, 2

	; printf()
	mov	QWORD PTR -32[rbp], rax
	mov	rax, QWORD PTR -32[rbp]
	mov	eax, DWORD PTR [rax]
	mov	esi, eax				; &arr[0]
	lea	rax, .LC0[rip]				; arg2
	mov	rdi, rax				; arg1 = arr[0]
	mov	eax, 0
	call	printf@PLT

	; restore rsp and return
	mov	rsp, rbx
	mov	eax, 0
	mov	rbx, QWORD PTR -8[rbp]
	leave
	ret
```

The compiler has employed another strategy to do this calculation.

* Add 15 to the bytes required, we get `(n + 15)`.
* Divide this by 16 and focus on quotient, we have to do `(n+15)//16` .
* Multiply the quotient with 16 and you get the total bytes required.

For example, take n = 5.

* `n*sizeof(int)` = `5*4 = 20`&#x20;
* `20+15 = 35`&#x20;
* `35//16 = 2`&#x20;
* `2*16 = 32`

If you have trouble making sense of this, remember the `ceil()` and `floor()` functions.

* `ceil` rounds up to the next integer while `floor` rounds down to the previous integer.
* `ceil(5.6)` would give 6 while `floor(5.6)` would give 5.
* If you notice, we are rounding in terms of 1.
* The algorithm above does the same thing except it rounds integers to the next multiple of 16.&#x20;

***

### Questions Time

**Q1. What's the purpose of saving `rsp` in `rbx` ? And why we are pushing `rbx` on stack?**

* `rbx` is a callee-saved register. If the callee function want to use `rbx`, it has to preserve the state of `rbx` and return `rbx` in the same state to the caller function. That's why it is pushed on stack.
* We are using it to preserve the state of `rsp` after reserving 40 bytes. Later it used in cleanup.

**Q2. Why inconsistent use of registers? When you need sign-extended value, why you are using `eax`? just use `rax` directly?**

* Compiler optimization.

**Q3. How stack is cleaned up after usage?**

* It doesn't. There are millions of processes and they use it very fast and dump it. And the next process overwrites the stack memory.
* Just reduce `rsp` and you are done. We just have to make memory inaccessible. That's it.
* This is the reason why we sometimes get exactly what we expect but the next moment it vanishes because the stack memory mistakenly had that exact value from a previous process but soon someone else override it. An undefined behavior, basically.

### Static && Extern VLA

Both are possible but require **compile-time constant declaration**. Because storage with static duration must be determined fully at compile time as memory layout is fixed before runtime.

Simply put,

```c
// Outisde Functions
int n = 5;

int arr1[n];
static int arr2[n];

func(){
  int m = 5;
  static int arr3[m];
}
```

all of these are invalid.

The valid ones are these:

```c
// Outisde Functions
const int n = 5;

int arr1[n];
static int arr2[n];

func(){
  const int m = 5;
  static int arr3[m];
}
```

## Conclusion

Arrays are contiguous memory blocks.

What changes is **how** the compiler allocates, aligns, and initializes them — influenced by constants, optimization flags, and ABI rules.

Optimizations vary, but the core intent stays constant: manage memory predictably and efficiently.

Thank you.
