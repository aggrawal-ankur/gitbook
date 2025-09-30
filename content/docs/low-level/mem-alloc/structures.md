---
id: 25c9ecebcb0e4f528ae02375a2b61a9e
title: Structures
weight: 6
---

_**2,3, 5, 22 September 2025**_

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

## Internal Padding In Structs

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

* 4 (x), 4(y), 8(memo) and 8(gen).
* The padding within the struct is measured according to the biggest type member. Here, it is pointer, which requires 8-bytes of space. x and y together keeps it 8-byte aligned but gen breaks that so 7-bytes of padding is given to it.

## Struct In Function Arguments

Unlike arrays, a struct doesn't decay into a pointer when passed to a function. Take this:

```c
#include <stdio.h>

struct Point {
  int x;
  int y;
};

void taketPointPtr(struct Point *p){}

void takePoint(struct Point p){}

int main() {
  struct Point p = {10, 20};
  printPoint(p);
  printPointPtr(&p);
}
```

This is the assembly, which is same for both the functions.

```nasm
takePointPtr:
	push	rbp
	mov	rbp, rsp
	mov	QWORD PTR -8[rbp], rdi
	nop
	pop	rbp
	ret

takePoint:
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
	mov	DWORD PTR -8[rbp], 10
	mov	DWORD PTR -4[rbp], 20

	mov	rax, QWORD PTR -8[rbp]		; loading a QWORD value
	mov	rdi, rax
	call	takePoint

	lea	rax, -8[rbp]			; loading an address
	mov	rdi, rax
	call	takePointPtr

	mov	eax, 0
	leave
	ret
```

## Pointer To Struct

```c
#include <stdio.h>

struct Point {
  int x;
  int y;
};

int main() {
  struct Point p = {10, 20};
  struct Point *ptr = &p;

  ptr->x = 30;
  ptr->y = 40;

  printf("%d %d\n", p.x, p.y);
}
```

This is the assembly:

```nasm
.LC0:
	.string	"%d %d\n"

main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16

	mov	DWORD PTR -16[rbp], 10
	mov	DWORD PTR -12[rbp], 20

	lea	rax, -16[rbp]
	mov	QWORD PTR -8[rbp], rax

	mov	rax, QWORD PTR -8[rbp]
	mov	DWORD PTR [rax], 30

	mov	rax, QWORD PTR -8[rbp]
	mov	DWORD PTR 4[rax], 40

	mov	edx, DWORD PTR -12[rbp]
	mov	eax, DWORD PTR -16[rbp]
	mov	esi, eax
	lea	rax, .LC0[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT

	mov	eax, 0
	leave
	ret
```

Lets draw the initial state of stack.

```asciidoc
3992 <->     rbp  <->
3988 <->  -4[rbp] <->
3984 <->  -8[rbp] <->
3980 <-> -12[rbp] <-> 20        p.y
3972 <-> -16[rbp] <-> 10        p.x
```

Let's go instruction by instruction as too much movement in close proximity is happening.

These two instructions setup our struct pointer `ptr` which goes at `-8[rbp]` .&#x20;

```
lea rax, -16[rbp]                    ; obtain the address of p.x
mov QWORD PTR -8[rbp], rax           ; save it at -8[rbp]
```

*   State of stack:

    ```
    3992 <->     rbp  <->
    3988 <->  -4[rbp] <->
    3984 <->  -8[rbp] <-> 3972    ptr
    3980 <-> -12[rbp] <-> 20      p.y
    3972 <-> -16[rbp] <-> 10      p.x
    ```

These two instructions obtain the address of `p.x` and update the value at it with 30.

```
mov rax, QWORD PTR -8[rbp]
mov DWORD PTR [rax], 30
```

*   State of stack:

    ```
    3992 <->     rbp  <->
    3988 <->  -4[rbp] <->
    3984 <->  -8[rbp] <-> 3972    ptr
    3980 <-> -12[rbp] <-> 20      p.y
    3972 <-> -16[rbp] <-> 30      p.x
    ```

These two instructions obtain the address of `p.y` and update the value at it with 40.

```
mov rax, QWORD PTR -8[rbp]
mov DWORD PTR 4[rax], 40
```

*   State of stack:

    ```
    3992 <->     rbp  <->
    3988 <->  -4[rbp] <->
    3984 <->  -8[rbp] <-> 3972    ptr
    3980 <-> -12[rbp] <-> 40      p.y
    3972 <-> -16[rbp] <-> 30      p.x
    ```

And we are done.

## Struct Types As Functions

A struct definition like this:

```c
struct Point{
  int x;
  int y;
};
```

can be used to create a function of its type like this:

```c
struct Point takePoint(struct Point P){}
```

If you want to avoid writing `struct` every time, use a type definition instead.

```c
typedef struct{
  int x;
  int y;
} Point;

Point takePoint(Point P);
```

The reason is simple, a type definition helps you create user defined types, on the other hand, normal struct declarations are just variables, so they can't be used in place of types.&#x20;

## Conclusion

At the end of the day, everything boils down to stack discipline. Once you understand stack management, everything else just builds upon that.