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













