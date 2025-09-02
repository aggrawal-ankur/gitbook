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

To avoid mentioning red zone every time, we will use a printf to make `main` a non-leaf function.

## Starters

We re already familiar with these concepts, we just have to reinforce them for arrays.

### Example 1: Declaration Only

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

### Example 2 - Declare and Use (No init)

If you run a for loop on the previous program to print all the values, you will find garbage values.

***

### Example 3 - Declaration + Initialization

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

### Example 5 - Incomplete Initialization

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

When you initialize the array completely along the length, there is no need for zeroing out. Here, we are doing partial initialization, which is why we need to zero-initialize the array so that each element has a proper value, then we are initializing the initial positions with specified values.

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

The point is that `n` would be initialized at runtime, so, instead of setting up stack just after function frame setup, we defer it until `n` is known. We only reserve enough space for defined operations and defer the rest.

We have to keep the allocation 16-bytes aligned. The question is, how can we calculate the right value? Let's do some math here.

We have to reserve space for `int arr[n]` .

* Size of integer is 4 so the total requirement is given by `n*4` bytes.

This value of n will decide how much extra padding we need to keep `rsp` 16-bytes aligned.

| Value of n | Bytes required | Padding      |
| ---------- | -------------- | ------------ |
| 1          | 1\*4 = 4       | 16 - 4 = 12  |
| 2          | 2\*4 = 8       | 16 - 8 = 8   |
| 3          | 3\*4 = 12      | 16 - 12 = 4  |
| 4          | 4\*4 = 16      | 16 - 16 = 0  |
| 5          | 5\*4 = 20      | 32 - 20 = 12 |
| 6          | 6\*4 = 24      | 32 - 24 = 8  |
| 7          | 7\*4 = 28      | 32 - 28 = 4  |
| 8          | 8\*4 = 32      | 32 - 32 = 0  |

This shows that the value for padding for a 4-byte integer belongs to `{0, 4, 8, 12}` . Plus, when the total bytes required are greater than the closest 16-divisible digit, we take the next 16-divisible digit.

From this information, we can create a simple program to calculate the total bytes required to allocate on stack.

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

By the way, this is just one way to do it.

Let's see how the compiler implements this.

### Example 1

```c
#include <stdio.h>

int main(void){
  int n;
  printf("%d is n\n", n);

  int arr[n];
  for (int i = 0; i < 5; i++){
    scanf("%d", &arr[i]);
  }
}
```

When you run the binary, you will see a garbage value and a segfault.

```bash
$ gcc ./main.c
$ ./a.out

2085013376 is n
zsh: segmentation fault  ./a.out
```

This one was pretty much expected as stack is limited and `2085013376` bytes is definitely a big number.

### Example 2: Init n

This time we are initializing `n`. And it works perfectly.

```c
#include <stdio.h>

int main(void){
  int n = 5;

  int arr[n];
  for (int i = 0; i < 5; i++){
    scanf("%d", &arr[i]);
  }
  for (int i = 0; i < 5; i++){
    printf("%d, ", arr[i]);
  }
}
```





## Example 3: n Not Known At Compile Time

This is the most important one here.

```c
#include <stdio.h>

int main(void){
  int n;
  scanf("%d", &n);

  int arr[n];
  for (int i = 0; i < 5; i++){
    scanf("%d", &arr[i]);
  }
  for (int i = 0; i < 5; i++){
    printf("%d, ", arr[i]);
  }
}
```

In this code, `n` is not known at compile time. The idea is simple. We need to calculate how much space we have to allocate on stack, which can only be done once `n` is initialized at runtime.

The assembly looks crazy, but it's not.

```
```

Here we are applying a different trick.

Suppose, n is 5. So, we need 5\*4 = 20 bytes.

* We have to find padding now.
* We are adding 15 to 20, which makes 35.
* Now we divide 35 by 16 and keep the quotient with us. 35//16 = 2.
* At last, we multiple it by 16 to obtain 32.
* The question is, why 15?
*









