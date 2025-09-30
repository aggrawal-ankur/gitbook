---
id: fe6eda248c6a44d8bfb318ee01ce17fa
title: Examples
---


Let's see how if, else if and else, for loop, while loop and do while loop exist.

## Example 1: if-else

```c
#include <stdio.h>

int main(void) {
  int a = 5, b = 6;
  if (a > b){
    printf("Yes, 5 > 6.\n");
  }
  else{
    printf("No, 5 < 6.\n");
  }
}
```

Assembly:

```nasm
	.text
	.section	.rodata
.LC0:
	.string	"Yes, 5 > 6."
.LC1:
	.string	"No, 5 < 6."

	.text
	.globl	main
	.type	main, @function
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16

	mov	DWORD PTR -4[rbp], 5              ; a
	mov	DWORD PTR -8[rbp], 6              ; b

	mov	eax, DWORD PTR -4[rbp]
	cmp	eax, DWORD PTR -8[rbp]            ; if (a > b)
	jle	.L2

	; if block
	lea	rax, .LC0[rip]
	mov	rdi, rax
	call	puts@PLT
	jmp	.L3

; else block
.L2:
	lea	rax, .LC1[rip]
	mov	rdi, rax
	call	puts@PLT

; return
.L3:
	mov	eax, 0
	leave
	ret
```

***

## Example 2: if- else if -else

```c
#include <stdio.h>

int main(void) {
  int a = 5, b = 6;
  if (a == b){
    printf("Yes, a > b.\n");
  }
  else if (a == b){
    printf("Actually, a == b.\n");
  }
  else{
    printf("No, a < b.\n");
  }
}
```

Assembly:

```nasm
	.text
	.section	.rodata
.LC0:
	.string	"Yes, a > b."

.LC1:
	.string	"Actually, a == b."

.LC2:
	.string	"No, a < b."
	.text
	.globl	main
	.type	main, @function

main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16

	mov	DWORD PTR -4[rbp], 5		; a
	mov	DWORD PTR -8[rbp], 6		; b

	mov	eax, DWORD PTR -4[rbp]
	cmp	eax, DWORD PTR -8[rbp]		; if (a > b)
	jne	.L2

	; if block
	lea	rax, .LC0[rip]
	mov	rdi, rax
	call	puts@PLT
	jmp	.L3

; else if block 
.L2:
	mov	eax, DWORD PTR -4[rbp]
	cmp	eax, DWORD PTR -8[rbp]		; if (a == b)
	jne	.L4
	lea	rax, .LC1[rip]
	mov	rdi, rax
	call	puts@PLT
	jmp	.L3

; else block
.L4:
	lea	rax, .LC2[rip]
	mov	rdi, rax
	call	puts@PLT

; return
.L3:
	mov	eax, 0
	leave
	ret
```

## Example 3: Switch Case

```c
#include <stdio.h>

int main(void) {
  int choice = 5;

  switch(choice){
    case 0:
      printf("Yes, equal to zero.\n");
      break;
    case 5:
      printf("No, not 1.\n");
      break;
    default:
      printf("No case matched. It is 5.\n");
  }
}
```

Assembly:

```nasm
	.text
	.section	.rodata
.LC0:
	.string	"Yes, equal to zero."
.LC1:
	.string	"No, not 1."
.LC2:
	.string	"No case matched. It is 5."

	.text
	.globl	main
	.type	main, @function
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16
	mov	DWORD PTR -4[rbp], 5          ; choice

	cmp	DWORD PTR -4[rbp], 0          ; case 0
	je	.L2
	cmp	DWORD PTR -4[rbp], 5          ; case 1
	je	.L3
	jmp	.L7                           ; default

; case 0
.L2:
	lea	rax, .LC0[rip]
	mov	rdi, rax
	call	puts@PLT
	jmp	.L5

; case 1
.L3:
	lea	rax, .LC1[rip]
	mov	rdi, rax
	call	puts@PLT
	jmp	.L5

; default
.L7:
	lea	rax, .LC2[rip]
	mov	rdi, rax
	call	puts@PLT

; return
.L5:
	mov	eax, 0
	leave
	ret
```

Notice that for default case we are using unconditional jump.

* Although `.L7` is not strictly required but the semantics of switch cases require you to create a separate label for each. The compiler may optimize it at higher levels.

## Example 4: Importance of break;

This code doesn't use `break;` in case 5. We know that if break is not present, the cases after it are executed without any check. Let's see.

```c
#include <stdio.h>

int main(void) {
  int choice = 5;

  switch(choice){
    case 0:
      printf("Yes, equal to zero.\n");
      break;
    case 5:
      printf("No, not 1.\n");
    default:
      printf("No case matched. It is 5.\n");
  }
}

```

Assembly:

```nasm
	.text
	.section	.rodata
.LC0:
	.string	"Yes, equal to zero."
.LC1:
	.string	"No, not 1."
.LC2:
	.string	"No case matched. It is 5."
	.text
	.globl	main
	.type	main, @function

main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16
	mov	DWORD PTR -4[rbp], 5

	cmp	DWORD PTR -4[rbp], 0       ; case 0
	je	.L2
	cmp	DWORD PTR -4[rbp], 5       ; case 5
	je	.L3
	jmp	.L4

; case 0
.L2:
	lea	rax, .LC0[rip]
	mov	rdi, rax
	call	puts@PLT
	jmp	.L5

; case 5
.L3:
	lea	rax, .LC1[rip]
	mov	rdi, rax
	call	puts@PLT		   ; Notice, no jmp to .L5 

; case default
.L4:
	lea	rax, .LC2[rip]
	mov	rdi, rax
	call	puts@PLT

; return
.L5:
	mov	eax, 0
	leave
	ret
```

This code lacks an unconditional jump to `.L5`, the return label, which is why the case after it is executed without any check as the check is performed before.

## Example 5: for loop

```c
#include <stdio.h>

int main(void) {
  for (int i = 0; i < 5; i++){
    printf("i: %d\n", i);
  }
}
```

Assembly:

```nasm
	.text
	.section	.rodata
.LC0:
	.string	"i: %d\n"

	.text
	.globl	main
	.type	main, @function
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16
	mov	DWORD PTR -4[rbp], 0          ; i = 0
	jmp	.L2

.L3:
	mov	eax, DWORD PTR -4[rbp]        ; load i
	mov	esi, eax                      ; esi = i (arg 2)
	lea	rax, .LC0[rip]
	mov	rdi, rax                      ; edi = addr(str)
	mov	eax, 0
	call	printf@PLT
	add	DWORD PTR -4[rbp], 1          ; update local instance of i

; body
.L2:
	cmp	DWORD PTR -4[rbp], 4        ; check i < 4 
	jle	.L3

	; otherwise, return
	mov	eax, 0
	leave
	ret
```

Notice that `.L2` is present after `.L3` , so `.L2` need not to make any jump to it. That's compiler optimization at bare minimum.

Even if you declare `i` outside of loop, nothing will change.

## Example 6: Infinite for loop

```c
#include <stdio.h>

int main(void) {
  int i = 0;
  for (;;){
    printf("i: %d\n", i);
  }
}
```

Assembly:

```nasm
	.text
	.section	.rodata
.LC0:
	.string	"i: %d\n"

	.text
	.globl	main
	.type	main, @function
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16

	mov	DWORD PTR -4[rbp], 0
.L2:
	mov	eax, DWORD PTR -4[rbp]
	mov	esi, eax
	lea	rax, .LC0[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT
	jmp	.L2
```

Unless the source has an explicit break condition, it will run until it eats up all the resources.

## Example 7: while loop

Although this is an infinite while loop, but it will not run.

```c
#include <stdio.h>

int main(void) {

  int i = 0;
  while (i){
    printf("i: %d\n", i);
  }
}
```

Assembly:

```nasm
	.text
	.section	.rodata
.LC0:
	.string	"i: %d\n"

	.text
	.globl	main
	.type	main, @function
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16
	mov	DWORD PTR -4[rbp], 0
	jmp	.L2
.L3:
	mov	eax, DWORD PTR -4[rbp]
	mov	esi, eax
	lea	rax, .LC0[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT
.L2:
	cmp	DWORD PTR -4[rbp], 0
	jne	.L3
	mov	eax, 0
	leave
	ret
```

Notice the condition in `.L2`. It jumps to `.L3` when the comparison is not equal to zero.

## Example 8: Infinite while loop

```c
#include <stdio.h>

int main(void) {

  int i = 1;
  while (i){
    printf("i: %d\n", i);
  }
}
```

Assembly:

```nasm
	.text
	.section	.rodata
.LC0:
	.string	"i: %d\n"

	.text
	.globl	main
	.type	main, @function
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16

 	mov	DWORD PTR -4[rbp], 1
	jmp	.L2
.L3:
	mov	eax, DWORD PTR -4[rbp]
	mov	esi, eax
	lea	rax, .LC0[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT
.L2:
	cmp	DWORD PTR -4[rbp], 0
	jne	.L3
	mov	eax, 0
	leave
	ret
```

If you notice, infinite while loop and infinite for loop matches instruction by instruction except the `.L2` label in while loop, which basically checks for true/false.

## Example 9: Finite while loop

```c
#include <stdio.h>

int main(void) {

  int i = 0;
  while (i < 5){
    printf("i: %d\n", i);
  }
}
```

Assembly:

```nasm
	.text
	.section	.rodata
.LC0:
	.string	"i: %d\n"

	.text
	.globl	main
	.type	main, @function
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16
	mov	DWORD PTR -4[rbp], 0
	jmp	.L2

.L3:
	mov	eax, DWORD PTR -4[rbp]
	mov	esi, eax
	lea	rax, .LC0[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT
	add	DWORD PTR -4[rbp], 1

.L2:
	cmp	DWORD PTR -4[rbp], 4
	jle	.L3

	; return
	mov	eax, 0
	leave
	ret
```

Again, it is exactly same as finite for loop.

This proves that for and while is just syntactic sugar.

## Example 10: do while loop

```c
#include <stdio.h>

int main(void) {
  int i = 0;
  do {
    printf("i: %d\n", i);
    i++ ;
  } while (i < 5);
}
```

Assembly:

```nasm
	.text
	.section	.rodata
.LC0:
	.string	"i: %d\n"

	.text
	.globl	main
	.type	main, @function
main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16
	mov	DWORD PTR -4[rbp], 0

.L2:
	mov	eax, DWORD PTR -4[rbp]
	mov	esi, eax
	lea	rax, .LC0[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT
	add	DWORD PTR -4[rbp], 1

	cmp	DWORD PTR -4[rbp], 4          ; while (i < 5) check
	jle	.L2

	; return
	mov	eax, 0
	leave
	ret
```

## Conclusion

This is how control flow looks like.