# Static Memory Allocation

## The Problem

We only have one memory, but how it is managed decides where the space would be allocated.

Mainly we have `.data`, `.bss`, stack and heap for memory allocation.

* From [common-terminologies.md](../common-terminologies.md "mention"), we know that `.data` is for initialized static/globals and `.bss` is for uninitialized static/globals.
* We have not explored stack and heap yet, and we neither need to. Just remember that heap is used in dynamic memory allocation and stack is for static memory allocation.
* Heap is an advanced thing, so we are going to avoid it.

***

The question is, who will decide where the memory is going to be allocated?

* Storage classes.

## The Solution

**Storage classes** guide the compiler to manage static memory allocation.

There are primarily 4 thing associated with a variable which are needed to managed.

1. Where in the memory the variable would be stored (**location**)?
   1. Registers?
   2. Stack?
   3. Heap?
   4. .data?
   5. .bss?
2. How long the variable should exist and be accessible (**lifetime**)?
3. Who can access that variable? And where that variable can be accessed from (**scope**)?
4. Whether the variable has a default initial value when uninitialized or it will be garbage?

<table><thead><tr><th width="123">Storage Class</th><th width="220">Scope &#x26;&#x26; Lifetime</th><th width="147">Default Value (when uninitialized))</th><th>Location</th></tr></thead><tbody><tr><td>auto</td><td>The block it is declared in (local)<br><br>Until the block ends</td><td>Garbage (undefined)</td><td>Stack</td></tr><tr><td>register</td><td>The block it is declared in (local)<br><br>Until the block ends</td><td>Garbage (undefined)</td><td>CPU register (if available)</td></tr><tr><td>static</td><td>File Scope<br><br>Until the program exists in the memory</td><td>0</td><td>.data (if initialized non-zero)<br><br><code>.bss</code> (if zero-initialized; or not initialized)</td></tr><tr><td>extern</td><td>File/global<br><br>Until the program exists in the memory</td><td>0</td><td>.data (if initialized non-zero)<br><br><code>.bss</code> (if zero-initialized; or not initialized)</td></tr></tbody></table>

Every variable has a storage class associated to it, just that it is not visible.

## The Concept Of Scope

Local and global scopes are kinda unclear when you do big projects with lots of source files.

In simple words, scope defines where a declaration of an identifier can be referenced (used).

Primarily, there are 3 scopes.

1. Block Scope (Local scope).
2. Internal Linkage (File scope)
3. External Linkage (Global scope)

### Block Scope (Local)

As named, any declaration inside `{ }` is block scoped.

Example: functions, if-else and loops.

The default storage class for block scoped declarations is `auto`.

***

What is linkage?

* If I use the same identifier name in multiple scopes or translation units (technical name for a source file), do they refer to the same object, or to different ones?
* This is defined by linkage.

### External Linkage (Global)

The name refers to the same object across the entire program (all .c files compiled together).

When a declaration is placed outside of any function, by default, it has the `extern` storage class.

`extern` makes a declaration accessible to the entire project.

```c
int PI = 3.14;

int circumference(int r) {
  return 2 * PI * r;
}
```

### Internal Linkage (File)

In the current file scope, **X** refers to the same thing when called from anywhere. Example

```c
static int PI = 3.14;

int circumference(int r) {
  return 2 * PI * r;
}

int area(int r){
  return PI*r*r;
}
```

Here, `PI` has internal linkage. Both the function access the same object when referencing `PI`.

### No Linkage?

The name refers to an entity **only in its scope**. Example, any declaration inside a function scope.

### Final Mental Model

<table><thead><tr><th width="115">Scope</th><th width="175">Default Storage Class</th><th width="169">Explicitly Mentioned</th><th>Storage Location</th></tr></thead><tbody><tr><td>Local</td><td><code>auto</code></td><td>-</td><td>Stack</td></tr><tr><td>File</td><td>-</td><td><code>static</code></td><td>.data (if initialized non-zero)<br><br><code>.bss</code> (if zero-initialized; or not initialized)</td></tr><tr><td>Global</td><td><code>extern</code></td><td>-</td><td>.data (if initialized non-zero)<br><br><code>.bss</code> (if zero-initialized; or not initialized)</td></tr></tbody></table>

So, what do you mean by static/global?

* Static variables have file scope. Static doesn't mean there value is fixed, that is done by `const` and that's a completely different story. They are always zero-initialized at runtime if not initialized in the program.
* Global variables have program scope.

### A Healthy Note

Every language is setup differently, so, every language implements the concept of **Scope** differently. What applies here is not necessary to be exact in other languages.

But every language follows a similar structure.

***

## What's Next?

Now we understand how storage classes are paramount to memory allocation. And we are ready to understand how static memory allocation is carried out.

For better clarity, we can divide static memory allocation into:

1. [primitive-types.md](primitive-types.md "mention"): char, int, float and double.
2. [complex-types.md](complex-types.md "mention"): array, pointer, struct, union, enum and type definition.
