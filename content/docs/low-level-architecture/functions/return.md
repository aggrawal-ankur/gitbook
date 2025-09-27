---
title: Return Management?
weight: 4
---

**5,&#x20;**_**6 September 2025**_

***

## Premise

Returns can be classified into 3 types:

1. **Primitives** (int, char, float, double): the return is in register (`rax` for int and char, `xmm0` for floats)
2. **Arrays**: they can't be returned. Period. You pass a reference to a modifiable memory from the caller itself. To return a local declaration, you make it block static.
3. **Structures/Unions**: this is where the problem is.

## Returning Structures/Unions <= 16 Bytes

System V ABI decides return strategy based on size and fields.

1. If the return size is <= 16 bytes, it is returned in registers.
2. If the return size is > 16 bytes, it is complicated.

***

### 8-byte Struct

```c
#include <stdio.h>

struct Pair { int x; int y; };

struct Pair make_pair(int a, int b) {
  struct Pair p;
  p.x = a;
  p.y = b;
  return p;
}

int main() {
  struct Pair q = make_pair(2, 3);
  return q.x + q.y;
}
```

_Feels like we have implemented a class in C huh?_

This is the assembly:

```nasm
make_pair:
	push	rbp
	mov	rbp, rsp

	; create a local copy of args (2, 3)
	mov	DWORD PTR -20[rbp], edi
	mov	DWORD PTR -24[rbp], esi

	; Load the local copy at a different place for operation
	; as the primary local copy is kept untouched unless specified
	mov	eax, DWORD PTR -20[rbp]
	mov	DWORD PTR -8[rbp], eax
	mov	eax, DWORD PTR -24[rbp]
	mov	DWORD PTR -4[rbp], eax

	; The most important line
	; We are loading 8-bytes in rax starting from -8[rbp] to -1[rbp]
	mov	rax, QWORD PTR -8[rbp]

	pop	rbp
	ret

main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16

	mov	esi, 3
	mov	edi, 2
	call	make_pair

	; Unpacking the 8-bytes into two separate 4-byte integers
	mov	QWORD PTR -8[rbp], rax
	mov	edx, DWORD PTR -8[rbp]        ; -8, -7, -6, -5 represent 2
	mov	eax, DWORD PTR -4[rbp]        ; -4, -3, -2, -1 represent 3

	; return
	add	eax, edx

	leave
	ret
```

This would be the state of `make_pair` stack frame:

```asciidoc
    rbp
 -4[rbp]  <-> 3
 -8[rbp]  <-> 2
-12[rbp]  <->
-16[rbp]  <->
-20[rbp]  <-> 2
-24[rbp]  <-> 3
```

The trick is that we load both the values in one single register. The question is how? Remember, interpretation rules memory access. As long as you interpret the right way, even garbage is gold.

Lets modify this program to see what is returned in `rax` .

```c
#include <stdio.h>
#include <stdint.h>

struct Pair { int x; int y; };

union PairBits {
  struct Pair p;
  unsigned long long bits;
};

struct Pair make_pair(int a, int b) {
  struct Pair tmp = {a, b};
  return tmp;
}

void print_binary64(uint64_t val) {
  for (int i = 63; i >= 0; i--) {
    putchar((val >> i) & 1 ? '1' : '0');
    if (i % 8 == 0) putchar(' ');  // group by bytes
  }
  putchar('\n');
}

int main() {
  union PairBits u;
  u.p = make_pair(2, 3);
  
  printf("sizeof union `u`: %d\n", sizeof(u));

  printf("rax (hex) = 0x%016llx\n", u.bits);
  printf("rax (bin) = ");

  print_binary64(u.bits);
  printf("q.x = %d, q.y = %d\n", u.p.x, u.p.y);
}
```

Lets understand this program first.

We can't capture `rax`  directly because it exist in only. But there are two way ways to do it:

1. Using union.
2. Inline assembly.

We are implementing the union way because we are not known to inline assembly yet.

The idea is simple, all the members in a union share the same memory starting at offset 0. So, `u.p` struct and `u.bits` are just two aliases for the same memory and the `sizeof` printf confirms that.

Let's talk about `0x%016llx` .

* `0x` : literally prints `0x` in front.
* `%` : start of format specifier.
* `0` : pad with zeroes instead of space.
* `16` : total width of output is 16 characters. Every hex bit represents 4 binary bits so 64 binary bits require 16 hex digits.
* `ll` : length modifier: long long (for 64-bit).
* `x` : print in hexadecimal lowercase.

Since there is no builtin way to print binary bits, we created our own.

Let's run the program, we get:

```bash
$ gcc main.c
$ ./a.out

sizeof union `u`: 8
rax (hex) = 0x0000000300000002
rax (bin) = 00000000 00000000 00000000 00000011 00000000 00000000 00000000 00000010 
q.x = 2, q.y = 3
```

This is the proof that the compiler packed both the members of the struct in `rax` only.

### 12-byte Struct

```c
#include <stdio.h>
#include <stdint.h>

struct Point { int x; int y; int z;};

struct Point make_pair(int a, int b, int c) {
  struct Point p;
  p.x = a;
  p.y = b;
  p.z = c;
  return p;
}

int main() {
  struct Point p = make_pair(2, 3, 4);

  printf("sizeof struct `p`: %d\n", sizeof(p));
}
```

This is the assembly.

```nasm
make_pair:
	push	rbp
	mov	rbp, rsp

	; make a local copy of args (2, 3, 4)
	mov	DWORD PTR -36[rbp], edi
	mov	DWORD PTR -40[rbp], esi
	mov	DWORD PTR -44[rbp], edx

	; Copy them again
	mov	eax, DWORD PTR -36[rbp]
	mov	DWORD PTR -24[rbp], eax

	mov	eax, DWORD PTR -40[rbp]
	mov	DWORD PTR -20[rbp], eax

	mov	eax, DWORD PTR -44[rbp]
	mov	DWORD PTR -16[rbp], eax

	; Copy them again which is used in return
	mov	rax, QWORD PTR -24[rbp]
	mov	QWORD PTR -12[rbp], rax

	mov	eax, DWORD PTR -16[rbp]
	mov	DWORD PTR -4[rbp], eax

	mov	rax, QWORD PTR -12[rbp]          ; (2, 3) in rax
	mov	ecx, DWORD PTR -4[rbp]           ; 4 in rdx
	mov	rdx, rcx

	pop	rbp
	ret

.LC0:
	.string	"sizeof struct `p`: %d\n"

main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16

	mov	edx, 4
	mov	esi, 3
	mov	edi, 2
	call	make_pair

	; Unpack
	mov	QWORD PTR -12[rbp], rax
	mov	eax, DWORD PTR -4[rbp]
	and	eax, 0
	or	eax, edx
	mov	DWORD PTR -4[rbp], eax

	mov	esi, 12
	lea	rax, .LC0[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT
	mov	eax, 0
	leave
	ret
```

This time, `rax` alone can't help as it has already contained the two ints. So we use `rdx` to return the third int. The extra copying behavior is due to `-00`.

This would be the state of `make_pair` stack frame.

```
    rbp
 -4[rbp]  <-> 4
 -8[rbp]  <->
-12[rbp]  <-> 2, 3

-16[rbp]  <-> 4
-20[rbp]  <-> 3
-24[rbp]  <-> 2
-28[rbp]  <->
-32[rbp]  <->
-36[rbp]  <-> 2
-40[rbp]  <-> 3
-44[rbp]  <-> 4
```

### 16-byte Struct

```c
#include <stdio.h>
#include <stdint.h>

struct Point { int x; int y; int z; int s;};

struct Point make_pair(int a, int b, int c, int d) {
  struct Point p;
  p.x = a;
  p.y = b;
  p.z = c;
  p.s = d;
  return p;
}

int main() {
  struct Point p = make_pair(2, 3, 4, 5);

  printf("sizeof struct `p`: %d\n", sizeof(p));
}
```

This is the assembly:

```nasm
make_pair:
	push	rbp
	mov	rbp, rsp

	; local copy of args (2, 3, 4, 5)
	mov	DWORD PTR -20[rbp], edi
	mov	DWORD PTR -24[rbp], esi
	mov	DWORD PTR -28[rbp], edx
	mov	DWORD PTR -32[rbp], ecx

	; copy them for return
	mov	eax, DWORD PTR -20[rbp]
	mov	DWORD PTR -16[rbp], eax
	mov	eax, DWORD PTR -24[rbp]
	mov	DWORD PTR -12[rbp], eax
	mov	eax, DWORD PTR -28[rbp]
	mov	DWORD PTR -8[rbp], eax
	mov	eax, DWORD PTR -32[rbp]
	mov	DWORD PTR -4[rbp], eax

	; export two 8-byte pointers
	mov	rax, QWORD PTR -16[rbp]
	mov	rdx, QWORD PTR -8[rbp]

	pop	rbp
	ret

.LC0:
	.string	"sizeof struct `p`: %d\n"

main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 16

	mov	ecx, 5
	mov	edx, 4
	mov	esi, 3
	mov	edi, 2
	call	make_pair

	mov	QWORD PTR -16[rbp], rax
	mov	QWORD PTR -8[rbp], rdx

	mov	esi, 16
	lea	rax, .LC0[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT

	mov	eax, 0
	leave
	ret
```

Now we are smart enough to recognize that export two 8-byte pointers and unpack them in main is the strategy for 16-byte structs. Perfect.

***

Time for final boss, structs ≥ 16 bytes.

## Returning Structs/Unions > 16 Bytes

For structs greater than 16 bytes in size, the caller must allocate space for the return object and pass a hidden pointer to it as the first argument.

The callee writes the struct into that space and returns (with `rax` typically holding that pointer back again).

Basically, we came back to square one. The caller has to pass a pointer, either pass it directly or indirectly.

***

Like every single time, the caller would reserve space on stack, what changes is that this time, the caller will pass address to the start of memory reserve for stack in caller's stack frame. The callee will use that pointer to populate the caller's stack frame directly. And the callee returns the same address again. That's it.

This is the source:

```c
#include <stdio.h>
#include <stdint.h>

struct Point { int x; int y; int z; int r; int s;};

struct Point make_pair(int a, int b, int c, int d, int e) {
  struct Point p;
  p.x = a;
  p.y = b;
  p.z = c;
  p.r = d;
  p.s = e;
  return p;
}

int main() {
  struct Point p = make_pair(2, 3, 4, 5, 6);

  printf("sizeof struct `p`: %d\n", sizeof(p));
}
```

And the assembly:

```nasm
make_pair:
	push	rbp
	mov	rbp, rsp

	; local copy of arguments (2, 3, 4, 5, 6)
	mov	QWORD PTR -40[rbp], rdi
	mov	DWORD PTR -44[rbp], esi
	mov	DWORD PTR -48[rbp], edx
	mov	DWORD PTR -52[rbp], ecx
	mov	DWORD PTR -56[rbp], r8d
	mov	DWORD PTR -60[rbp], r9d

	; another copy for return mgmt
	mov	eax, DWORD PTR -44[rbp]
	mov	DWORD PTR -32[rbp], eax
	mov	eax, DWORD PTR -48[rbp]
	mov	DWORD PTR -28[rbp], eax
	mov	eax, DWORD PTR -52[rbp]
	mov	DWORD PTR -24[rbp], eax
	mov	eax, DWORD PTR -56[rbp]
	mov	DWORD PTR -20[rbp], eax
	mov	eax, DWORD PTR -60[rbp]
	mov	DWORD PTR -16[rbp], eax

	; Updating the memory in main's stack frame (via rdi)
	mov	rcx, QWORD PTR -40[rbp]			; save the address in caller's stack in rcx for easy access
	mov	rax, QWORD PTR -32[rbp]			; load 8-bit pointers to 2 and 4
	mov	rdx, QWORD PTR -24[rbp]			; load 8-bit pointers to 2 and 4
	mov	QWORD PTR [rcx], rax 			; dereference and populate
	mov	QWORD PTR 8[rcx], rdx			; dereference and populate
	mov	eax, DWORD PTR -16[rbp]			; load 6
	mov	DWORD PTR 16[rcx], eax			; copy 6

	mov	rax, QWORD PTR -40[rbp]			; prepare rax for return
	pop	rbp
	ret

.LC0:
	.string	"sizeof struct `p`: %d\n"

main:
	push	rbp
	mov	rbp, rsp
	sub	rsp, 32

	lea	rax, -32[rbp]		; address of struct on main's stack frame

	mov	r9d, 6
	mov	r8d, 5
	mov	ecx, 4
	mov	edx, 3
	mov	esi, 2
	mov	rdi, rax            	; the address is passed in rdi as the 1st arg
	call	make_pair

	; printf
	mov	esi, 20
	lea	rax, .LC0[rip]
	mov	rdi, rax
	mov	eax, 0
	call	printf@PLT

	mov	eax, 0
	leave
	ret

```

The state of stack:

```
make_pair:

    rbp
 -4[rbp]  <->
 -8[rbp]  <->
-12[rbp]  <->
-16[rbp]  <-> 6
-20[rbp]  <-> 5
-24[rbp]  <-> 4
-28[rbp]  <-> 3
-32[rbp]  <-> 2
-36[rbp]  <->
-40[rbp]  <-> 3960

-44[rbp]  <-> 2
-48[rbp]  <-> 3
-52[rbp]  <-> 4
-56[rbp]  <-> 5
-60[rbp]  <-> 6


main:

3992  <->      rbp
3988  <->   -4[rbp]  <->
3984  <->   -8[rbp]  <->
3980  <->  -12[rbp]  <->
3976  <->  -16[rbp]  <-> 6
3972  <->  -20[rbp]  <-> 5
3968  <->  -24[rbp]  <-> 4
3964  <->  -28[rbp]  <-> 3
3960  <->  -32[rbp]  <-> 2
```

## Conclusion

What did we learn?

1. `-O0` is best to study the fundamentals, the bookish behavior. It is not for shipping the final product. In any of the cases, just change `-O0` to 1 or 2 and you'll start to notice how dangerous the assembly gets. Dangerous in terms of optimization. It shows that a group of assembly instructions can be replaced by one single assembly instruction as well.
2. A lot of times, the most "complex looking things" boils down to simple hacks.

***


| Struct Size / Type | Registers Used | Notes / ABI Behavior |
| :--- | :--- | :--- |
| Scalar / int / pointer | rax | Single value returned directly. |
| 2×int / 8-byte struct | rax | Packed intorax. |
| 3×int / 12-byte struct | rax+rdx | First 8 bytes →rax, last 4 bytes →rdx. |
| 4×int / 16-byte struct | rax+rdx | Two 8-byte halves →rax/rdx. |
| >16 bytes | Caller allocates storage; pointer passed inrdi(sret) | Callee fills struct in caller-provided memory.raxmay return the pointer. |


And we are done with returning complex data.