---
id: 81155967a75e4f4486d83c8e6b2e14f7
title: Memory Allocation
weight: 2
---

## Premise

Memory for storage can be divided into 3:

1. Stack: the most straightforward thing you'll ever come across.
2. Static: `.data/.bss`
3. Heap: for dynamic allocation.

As long as we are talking about **stack** and **static** memory, we have to consult **storage classes** to find the appropriate place for allocation.

## Storage Classes

_**Storage classes** guide the compiler to manage static memory allocation._

Primarily there are 4 things associated with a variable.

1. **Location:** Where in the memory the variable would be stored? Our options: stack, registers, `.data` and `.bss`.
2. **Lifetime:** How long the variable should exist (or be accessible)?
3. **Scope:** Where that variable can be accessed from?
4. **Default State:** Whether the variable has a default initial value when uninitialized or a garbage value?

Storage class answers all of this.


| Storage Class | Scope && Lifetime | Default Value (when uninitialized)) | Location |
| :--- | :--- | :--- | :--- |
| auto | Block scopeUntil the block lives | Garbage (undefined) | Stack |
| register | Block scopeUntil the block lives | Garbage (undefined) | CPU register (if available) |
| static | File ScopeUntil the program exists in the memory | 0 | .data(if initialized non-zero).bss(if zero-initialized; or not initialized) |
| extern | Program scopeUntil the program exists in the memory | 0 | .data(if initialized non-zero).bss(if zero-initialized; or not initialized) |


Every variable has a storage class associated with it, but usually it is not visible.

## The Concept Of Scope

Local and global scopes are too shallow to understand scope.

_In simple words, scope defines where a declaration of an identifier can be referenced from (used)._

Primarily there are 3 scopes.

1. Block Scope
2. File Scope
3. Global scope

### Block Scope

Any declaration inside a `{ }` block is block scoped. Example: functions, if-else and loops.

The default storage class for block scoped declarations is `auto`.

It kinda resembles with **local scope** but that is too shallow because a block itself can contain other blocks. Examples:

* A function is a block that can contain an if block, which can contain another series of conditional blocks.
* A function can contain a for loop, which may contain nested if-else blocks.

All in all, local scope is not a resilient mental model for low level work. **That's my opinion.**

***

### **File Scope**

_A declaration which is globally accessible within one translation unit only is considered to be a file scoped declaration._

From build process, we know that the first step in processing a C source code is to expand preprocessing directives, where the toolchain (gcc, clang etc) just copies the headers files recursively until there is none.

* _The result of this process is what a translation unit is._
* Therefore, a TU is not something magical, just a sugar coating.

For example, `pie` is a file scoped declaration.

```c
#include <stdio.h>

static float pie = 3.14;

int main(void);
```

**Note: Don't think about this code. The next write up would explore it in enough depth.**

***

### Program Scope

_When a declaration exist until the program exist in memory and is available to be referenced by every translation unit, the declaration is program scoped._

Example:

```c
#include <stdio.h>

float pie = 3.14;

int main(void);
```

**Note: Again, don't focus on the code.**

***

The concept of scope is language enforced, which is why you will find different implementations of "scope". What scope implies in C isn't the same with Python because both the languages work differently.

How scopes behave in C is largely limited to C only and when you cross that boundary, the scenario changes. And we will see this practically as well.

At assembly level, the "concept of linkage" seems to be more prominent. Lets explore that.

***

## The Concept Of Linkage

_If I use the same identifier name in multiple scopes or translation units, do they refer to the same object, or different ones?_

* This is defined by linkage.

### External Linkage

The name refers to the same object across all the translation units.

When a declaration is placed outside of any function, by default, it has the `extern` storage class, which makes a declaration accessible to the entire project (all the .c files).

```c
int PI = 3.14;

int circumference(int r) {
  return 2 * PI * r;
}
```

### Internal Linkage

In this translation unit, anyone referring to **X** would be referring to the **X** declared in file scope.

```c
static int PI = 3.14;

int circumference(int r) {
  return 2 * PI * r;
}

int area(int r){
  return PI*r*r;
}
```

Here, `PI` has internal linkage. Both the functions access the same object when referencing `PI`.

### No Linkage?

The name refers to an entity **only in its scope**. Example: any declaration inside a function scope.

***

If you use `readelf` and inspect the ELF structure of a binary, either you are going to find `GLOBAL` linkage or `LOCAL` linkage, which are external and internal linkages respectively. There is nothing as `NO LINKAGE`. And this is the reason why understanding a block scope static is so confusing. We are going to explore that in the next write up.

### Final Mental Model

| Scope | Default Storage Class | Explicitly Mentioned | Storage Location | Lifetime |
| :--- | :--- | :--- | :--- | :--- |
| Block | auto | - | Stack | Block |
| Block | - | static | .data/.bss | Until the program dies |
| File | - | static | .data/.bss | Until the program dies |
| Global | extern | - | .data/.bss | Until the program dies |

{{< doclink "22f99fb0de5843079c208e3ff1d107f7" "" >}}
{{< doclink "bab39b08c80046e387d7f34d6394e070" "" >}}
{{< doclink "ba0ff614609d4707932bbe9eb1fbbdd9" "" >}}
{{< doclink "29652748a2bc49739d1a5e4eb7dcc475" "" >}}
{{< doclink "133c28b7762348618fddc238b6563a35" "" >}}
{{< doclink "25c9ecebcb0e4f528ae02375a2b61a9e" "" >}}
{{< doclink "15fbe373203b4dc59cbb32bf23b459cf" "" >}}
{{< doclink "583d6b17c3a346c59d56e98e9eb2488e" "" >}}