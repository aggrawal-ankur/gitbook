---
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

<table><thead style="text-align:left"><tr><th width="123">Storage Class</th><th width="201">Scope &#x26;&#x26; Lifetime</th><th width="179">Default Value (when uninitialized))</th><th>Location</th></tr></thead><tbody><tr><td>auto</td><td>Block scope<br><br>Until the block lives</td><td>Garbage (undefined)</td><td>Stack</td></tr><tr><td>register</td><td>Block scope<br><br>Until the block lives</td><td>Garbage (undefined)</td><td>CPU register (if available)</td></tr><tr><td>static</td><td>File Scope<br><br>Until the program exists in the memory</td><td>0</td><td><code>.data</code> (if initialized non-zero)<br><br><code>.bss</code> (if zero-initialized; or not initialized)</td></tr><tr><td>extern</td><td>Program scope<br><br>Until the program exists in the memory</td><td>0</td><td><code>.data</code> (if initialized non-zero)<br><br><code>.bss</code> (if zero-initialized; or not initialized)</td></tr></tbody></table>

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

<table><thead style="text-align:left"><tr><th width="94">Scope</th><th width="156">Default Storage Class</th><th width="147">Explicitly Mentioned</th><th width="145">Storage Location</th><th>Lifetime</th></tr></thead><tbody><tr><td>Block</td><td><code>auto</code></td><td>-</td><td>Stack</td><td>Block</td></tr><tr><td>Block</td><td>-</td><td><code>static</code></td><td><code>.data/.bss</code></td><td>Until the program dies</td></tr><tr><td>File</td><td>-</td><td><code>static</code></td><td><code>.data/.bss</code></td><td>Until the program dies</td></tr><tr><td>Global</td><td><code>extern</code></td><td>-</td><td><code>.data/.bss</code></td><td>Until the program dies</td></tr></tbody></table>
