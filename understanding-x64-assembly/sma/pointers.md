# Pointers

## General Trivia

1. A pointer is a variable that stores a memory address.
2. The size of the pointer is architecture dependent. So, in 64-bit Linux, it is 8-bytes.
3.  The pointer’s **type** defines what it points to, not the storage size. For example:

    ```c
    int*  iptr;
    char* cptr;
    ```

    Both the integer and character pointers are sized 8-bytes but they point to different values. The integer pointer points to a 4-byte value (general) while the character pointer points to a 1-byte value.
4. The type of pointer decides how the memory would be interpreted.
5. At assembly level, there is no dedicated "pointer type". Every symbol you create becomes a reference in the memory at runtime.

### Example - Integer

```c
#include <stdio.h>

int main(){
  int a = 48;
  int* p = &a;
}
```

```nasm
	.text
	.globl	main
	.type	main, @function
main:
	push	rbp
	mov	rbp, rsp

	; int a
	mov	DWORD PTR -12[rbp], 48

	; int* p = &a
	lea	rax, -12[rbp]
	mov	QWORD PTR -8[rbp], rax

	mov	eax, 0
	pop	rbp
	ret
```

There is no stack reservation because `main()` is not calling any function so it is a leaf function here and by default, it receives a 128-bytes of red zone as per x68 System V ABI.

The same result is seen for char, float and double except that you can notice some extra scaffolding in case of float and double because they are pretty complex in themselves. But we need not to worry about that.
