# Function Arguments

A variety of arguments can be passed to functions. Let's see how the function deals with them.

## Arrays

Take this simple code:

```c
#include <stdio.h>

void takeArray(int arr[]){}

int main(){
  int arr[] = {41, 23, 94, 55};
  takeArray(arr);
}
```

A plain function that just receives an array. This is the assembly:

```nasm
takeArray:
	push	rbp
	mov	rbp, rsp
	mov	QWORD PTR -8[rbp], rdi			; A pointer

	nop
	pop	rbp
	ret

main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16

	mov	DWORD PTR -16[rbp], 41
	mov	DWORD PTR -12[rbp], 23
	mov	DWORD PTR -8[rbp], 94
	mov	DWORD PTR -4[rbp], 55

	lea	rax, -16[rbp]
	mov	rdi, rax
	call	takeArray

	mov	eax, 0
	leave
	ret
```

Lets introduce array decay.

_Array decay is an automatic internal process that converts the array into a pointer to its first element. This conversion leads to the loss of the array's original size and dimension information._

* This is essential for passing arrays to a function.
* Here, the procedure `takeArray` receives `arr` as a pointer.

***

Another example:

```c
#include <stdio.h>

void takeArray(int* arr){}

int main(){
  int arr[] = {41, 23, 94, 55};
  takeArray(arr);
}
```

This is the assembly:

```nasm
takeArray:
	push	rbp
	mov	rbp, rsp
	mov	QWORD PTR -8[rbp], rdi

	nop
	pop	rbp
	ret

main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16

	mov	DWORD PTR -16[rbp], 41
	mov	DWORD PTR -12[rbp], 23
	mov	DWORD PTR -8[rbp], 94
	mov	DWORD PTR -4[rbp], 55

	lea	rax, -16[rbp]
	mov	rdi, rax
	call	takeArray

	mov	eax, 0
	leave
	ret
```

There is no difference, which proves that `int arr[]` and `int* arr` are the same things when present in a function's parameter.

***

Let's take another example:

```c
int main(){
  int arr[] = {41, 23, 94, 55};
  printf("%d\n", arr);
  printf("%d\n", &arr[0]);

  printf("%d\n", *arr);
  printf("%d\n", arr[0]);
}
```

The first two `printf` prints the address while the last two `printf` prints the value on that address. But we never declared `arr` as a pointer. This proves the presence of array decay.

***

