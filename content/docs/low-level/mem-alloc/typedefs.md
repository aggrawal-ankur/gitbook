---
id: 583d6b17c3a346c59d56e98e9eb2488e
title: Type Definition
weight: 8
---

_**September 07, 2025**_

***

Type definitions are used to create alias for existing data types. That's it. Nothing fancy.

For example:

```c
#include <stdio.h>

typedef long long int LLint;

int main() {
  LLint num = 5;
  long long int num1 = 5;
}
```

This is the assembly.

```nasm
main:
	push	rbp
	mov	rbp, rsp
	mov	QWORD PTR -8[rbp], 5
	mov	QWORD PTR -16[rbp], 5
	mov	eax, 0
	pop	rbp
	ret
```

Both takes 8 bytes of space.

As you have guessed already, type definitions exist during compilation only.