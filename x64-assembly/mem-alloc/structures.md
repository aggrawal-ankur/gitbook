# Structures

_**2,3 September 2025**_

***

## Introduction To Structures

A structure is just a contiguous block of memory that groups different variables under one name.

```c
#include <stdio.h>

struct Point {
  int x;
  int y;
};

int main(void){
  struct Point p1;               // No Initialization
  p1.x = 6;
  p1.y = 5;
  
  struct Point p2 = {6, 6};      // Complete Initialization
  
  struct Point p3 = {};          // Empty Initialization: Zero-initialize
  
  struct Point p4 = {7};         // Incomplete Initialization: The rest is automatically zeroed.
}
```

The `struct` declaration alone doesn't reserve space. It exist compilation level only. When you create a variable out of it, that's when storage is reserved.

Let's setup the old baseline, before we move any further.

### Auto

```c
#include <stdio.h>

struct Point {
  int x;
  int y;
};

int main(void){
  struct Point p1;               // No Initialization
  p1.x = 6;
  p1.y = 5;
  
  printf("Hello.\n");
}
```

This is the assembly.

```nasm
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16

	mov	DWORD PTR -8[rbp], 6
	mov	DWORD PTR -4[rbp], 5

	lea	rax, .LC0[rip]
	mov	rdi, rax
	call	puts@PLT
	mov	eax, 0
	leave
	ret
```

### Block Static

```c
#include <stdio.h>

struct Point {
  int x;
  int y;
};

int main(void){
  static struct Point p1;
  p1.x = 6;
  p1.y = 5;

  printf("Hello.\n");
}
```

```nasm
main:
	push	rbp
	mov	rbp, rsp

	mov	DWORD PTR p1.0[rip], 6
	mov	DWORD PTR p1.0[rip+4], 5

	lea	rax, .LC0[rip]
	mov	rdi, rax
	call	puts@PLT
	mov	eax, 0
	pop	rbp
	ret

	.local	p1.0
	.comm	p1.0,8,8
```

### File Static

```c
#include <stdio.h>

struct Point {
  int x;
  int y;
};

static struct Point p1;

int main(void){
  p1.x = 6;
  p1.y = 5;

  printf("Hello.\n");
}
```

```nasm
	.text
	.local	p1
	.comm	p1,8,8
	.section	.rodata
.LC0:
	.string	"Hello."
	.text
	.globl	main
	.type	main, @function
main:
	push	rbp
	mov	rbp, rsp
	mov	DWORD PTR p1[rip], 6
	mov	DWORD PTR p1[rip+4], 5
	lea	rax, .LC0[rip]
	mov	rdi, rax
	call	puts@PLT
	mov	eax, 0
	pop	rbp
	ret
```

### Extern

```c
#include <stdio.h>

struct Point {
  int x;
  int y;
};

struct Point p1;

int main(void){
  p1.x = 6;
  p1.y = 5;

  printf("Hello.\n");
}
```

```nasm
	.text
	.globl	p1
	.bss
	.align 8
	.type	p1, @object
	.size	p1, 8
p1:
	.zero	8
	.section	.rodata
.LC0:
	.string	"Hello."
	.text
	.globl	main
	.type	main, @function
main:
	push	rbp
	mov	rbp, rsp
	mov	DWORD PTR p1[rip], 6
	mov	DWORD PTR p1[rip+4], 5
	lea	rax, .LC0[rip]
	mov	rdi, rax
	call	puts@PLT
	mov	eax, 0
	pop	rbp
	ret
```

## Padding

Padding and alignment is very important to understand in structures.

So far, we only had integer members in the structure. When we add more members, of different types, the dynamics change.

For example:

```c
struct Point {
  int x;
  int y;
  char gen;
  int* memo;
};

int main(){
  int num = 88;

  struct Point P;
  P.x = 4;
  P.y = 5;
  P.gen = 'M';
  P.memo = &num;

  printf("Hello\n");
}
```

The assembly is this:

```nasm
.LC0:
	.string	"Hello"

main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 32

	mov	DWORD PTR -4[rbp], 88		; num

	mov	DWORD PTR -32[rbp], 4		; P.x
	mov	DWORD PTR -28[rbp], 5		; P.y
	mov	BYTE PTR -24[rbp], 77		; P.gen (ASCII value of 'M')

	lea	rax, -4[rbp]			; addr of -4[rbp], which is n
	mov	QWORD PTR -16[rbp], rax		; P.memo

	lea	rax, .LC0[rip]
	mov	rdi, rax
	call	puts@PLT

	mov	eax, 0
	leave
	ret
```

We need 21 bytes so 32 are reserved on stack.

Let's have a look at stack layout.

```asciidoc
                       rbp
                    *---------*
-04, -03, -02, -01  | num 88  |
                    *---------*
-08, -07, -06, -05, | Empty   |
                    | Padding |
                    *---------*
-16, -15, -14, -13, | P.memo  | -16[rbp] (8-byte)
-12, -11, -10, -09  *---------*
                    *---------*
-24, -23, -22, -21, | P.gen   | -24[rbp] (1-byte + 7-byte for padding)
-20, -19, -18, -17  *---------*
                    *---------*
-28, -27, -26, -25  | P.y     | -28[rbp] (4-byte)
                    *---------*
-32, -31, -30, -29  | P.x     | -32[rbp] (4-byte)
                    *---------*
```

If we print the size of struct, it is 24 bytes.

* 4 (x), 4(y), 8(memo) and 8 (gen).
* The padding within the struct is measured according to the biggest type member. Here, it is pointer, which requires 8-bytes of space. x and y together keeps it 8-byte aligned but gen breaks that so 7-bytes of padding is given to it.



