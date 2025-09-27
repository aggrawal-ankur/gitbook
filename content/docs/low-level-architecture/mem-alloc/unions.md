---
title: Unions
weight: 7
---

_**September 07, 2025**_

***

## Introduction

Unions are like structures syntactically but they differ in terms of memory allocation.

Unions are based on the concept of unified memory where the size of the union is the size of the biggest member it contains.

Every member access the same memory and only one allocation can last at a time.

Unions are best understood with an example.

```c
#include <stdio.h>

union Point { int x; int y; };

int main() {
  union Point u;
  u.x = 2;
  u.y = 3;
  printf("%d, %d\n", u.x, u.y);
  printf("sizeof union `u`: %d\n", sizeof(u));
}
```

This is the assembly.

```nasm
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16

	mov	DWORD PTR -4[rbp], 2		; stack usage only 4 bytes
	mov	DWORD PTR -4[rbp], 3		; same memory is updated

	mov	edx, DWORD PTR -4[rbp]
	mov	eax, DWORD PTR -4[rbp]
	mov	esi, eax
	lea	rax, .LC0[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT

	mov	esi, 4				; size of union is 4 , not 8
	lea	rax, .LC1[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT

	mov	eax, 0
	leave
	ret
```

Here, we updated the same location when we try to populate `u.y`. The size of the union is also 4 bytes only.

Let's take another example.

```c
#include <stdio.h>

union Point { int x; int y; int* ptr; };

int main() {
  int num = 5;

  union Point u;
  u.x = 2;
  u.y = 3;
  u.ptr = &num;

  printf("%d, %d, %d\n", u.x, u.y, u.ptr);
  printf("sizeof union `u`: %d\n", sizeof(u));
}
```

Since the last update to the union's memory is a pointer, we expect the output to be a random memory address. And the size of the union would be 8 bytes because of pointer variable.

```nasm
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16

	mov	DWORD PTR -4[rbp], 5		; num

	mov	DWORD PTR -16[rbp], 2		; u.x
	mov	DWORD PTR -16[rbp], 3		; u.y

	lea	rax, -4[rbp]			; &num
	mov	QWORD PTR -16[rbp], rax		; u.ptr

	mov	rcx, QWORD PTR -16[rbp]
	mov	edx, DWORD PTR -16[rbp]
	mov	eax, DWORD PTR -16[rbp]
	mov	esi, eax
	lea	rax, .LC0[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT

	mov	esi, 8
	lea	rax, .LC1[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT
	mov	eax, 0

	leave
	ret
```

Indeed.

Basically, every member of a union is just an alias to the union's memory.

## What's The Use Of Unions?

There can be multiple use cases but the best one and the most easily comprehensible one is **memory critical systems**.

If you have to use multiple temporary variables, they take a lot of space, which might be bad on a low memory system like embedded systems. If we are sure that we have one time use case of temporary variables, we can create a union instead.

* You may ask, if the variable has to be used once per context only, why can't we reuse that variable?
* Nice question. And the answer is we can. No problem. But when you follow standard coding practices or a team is working on that project, you'd prefer stricter naming rules so that no one accidentally creates a problem. That's it.
* You can use `temp` everywhere but `temp.ptr`, `temp.num` etc makes the `temp` variable more specific without costing any extra space.

## Conclusion

Only the _last written member_ is valid — reading another member is undefined behavior.
