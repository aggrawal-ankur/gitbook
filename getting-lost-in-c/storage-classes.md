---
layout:
  width: wide
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
---

# Storage Classes

_**August 14 and 15, 2025**_

***

## Introduction

In simple words, storage classes guide the compiler to manage the allocation of variables in the memory.

There are primarily 4 thing associated to a variable which are needed to managed.

1. Where in the memory the variable would be stored (**location**)?
   1. Registers?
   2. Stack?
   3. Heap?
   4. .data?
   5. .bss?
2. How long the variable should exist and be accessible (**lifetime**)?
3. Who can access that variable? Where that variable can be accessed from (**scope**)?
4. Whether the variable has a default initial value when uninitialized or it will be garbage?

## Storage Classes

<table><thead><tr><th width="138">Storage Class</th><th width="199">Scope &#x26;&#x26; Lifetime</th><th width="134">Default Value (when undeclared)</th><th width="156">Storage Location</th><th>Notes</th></tr></thead><tbody><tr><td><strong>auto</strong></td><td>The block it is declared in (local)<br><br>Until the block ends</td><td>Garbage (undefined)</td><td>Stack</td><td>Default for local variables; no need to mention explicitly.</td></tr><tr><td><strong>register</strong></td><td>The block it is declared in (local)<br><br>Until the block ends</td><td>Garbage</td><td>CPU register (if available)</td><td>Hint to store in CPU register for faster access (compiler may ignore it). Cannot take address with <code>&#x26;</code>.</td></tr><tr><td><strong>static</strong></td><td>File Scope<br><br>Until the program exists in the memory</td><td>0</td><td><code>.data</code> (if initialized)<br><br><code>.bss</code> (if uninitialized or 0 initialized)</td><td>Local static: retains value between function calls. Global static: limits scope to file (internal linkage).</td></tr><tr><td><strong>extern</strong></td><td>File/global<br><br>Until the program exists in the memory</td><td>0</td><td><code>.data</code> (if initialized)<br><br><code>.bss</code> (if uninitialized or 0 initialized)</td><td>Declares a variable that’s defined elsewhere; used for sharing globals across files.</td></tr></tbody></table>

You may ask why the default storage class stores variables on stack. What's the logic behind it?

* The answer lies in how function calls exist and managed at low level.
* In simple words, each function call gets a stack frame in the stack region for that process.
* These frames are stacked over each other. You would not appreciate a function accessing a variable defined in another function without receiving it in its own arguments.
* Those rights are enforced by stack frames and that is why the `auto` storage class or the default storage class makes the variables inside a function call or block stack allocated because it protects them.
* For a more deep dive, explore the article where I have discussed stack as a memory management approach. [Link](../approaches-to-memory-management/stack.md).
