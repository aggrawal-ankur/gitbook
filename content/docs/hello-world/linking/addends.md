---
id: 98544af1a04a454ba453a9b6eb7e7f7c
title: What Are Addends?
weight: 8
---

An addend is a constant value added to the symbol's address during relocation.

* When this constant is stored in the relocation entry itself, we call it `RELA`, which means, "Relocation with Addend".
* When this constant is embedded in the section being relocated, we call it `REL`, which means, "Relocation without Addend".

To understand the logic behind addend, lets have a look at this example.

## Example C Program

This program creates an integer array of size 5. Then it uses a for-loop to iterate over it. While iterating over each element, it uses pointer dereferencing directly rather than subscripting the array variable using square brackets, like this `array_ptr[i]` .

```c
#include <stdio.h>

int main(void){
  int array_ptr[] = {0, 4, 7, 6, -2};
  for (int i = 0; i < 5; i++)
  {
    printf("%d, ", *(array_ptr + i));
  }
}
```

## Problem Statement

We need to focus on the `*(array_ptr + i)` part.

To access the 4th element (index = 3), either we do `array_ptr[3]` or `*(array_ptr + 3)`. In both the cases, it resolves to the latter one, we know that.

The thing is, this is not a direct access to the 4th element? Think about it.

* We are using the base address at which the array is loaded in the memory and from there we are counting 4 boxes. Right?

On 64-bit systems, an integer is made up of 4-bytes.

* But memory doesn't exist in chunks of 4. It is 1-1-1-1. But we're accessing it in the form of 4. The `4` here is a beautiful abstraction. And beneath that lies the mess.

We are adding \[0, 1, 2, 3, 4] to the base pointer to obtain the address of the next consecutive elements in the array, but effectively we need \[0, 4, 8, 12, 16] to reach those positions, right? How is that managed?

## The Solution? Introduce Addends!

Effectively, we are doing `*(array_ptr + 0/4/8/12/16)`, and this `0, 4, 8, 12, 16` is what the addend conceptually is. It is what we are adding to obtain the desired element from the base offset.

The base address of the symbol is resolved by the `array_ptr` part and the addend is calculated via the formula `i * sizeof(int)`

Therefore, an addend is a constant value that is required to obtain the final runtime address of a symbol correctly.

## How does that relate with symbol resolution?

We are going to find this in the next article when we explore how relocations actually happen.

***

Take rest.