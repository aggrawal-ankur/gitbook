---
title: Why arrays in C follow 0-based indexing?
weight: 7
---

## Premise

When we do counting, we start from 1, not 0. So why do computers count from 0? Or, why does C count from 0, instead 1?

There exist various programming languages which use 1-based indexing as well.

This question always arises when someone studies arrays, but rarely get answered properly. At least I wasn't answered when I was learning arrays.&#x20;

Let’s try to understand it properly this time.

## Why?

Lets have a look at this code.

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

This program creates an integer array of size 5.&#x20;

Then it uses a for-loop to iterate over it.

* While iterating over each element, it uses pointer dereferencing directly rather than subscripting the array variable using square brackets, like this `array_ptr[i]` .
* But it doesn't matter.

We are iterating from 0 to 4, not 1 to 5, why?

When we are counting on fingers, we can simply point at `{0, 4, 7, 6, -2}` by 1, 2, 3, 4 and 5. But how a computer is supposed to do this? That's where the problem lies.

Suppose the array is loaded at address 1000 (in decimals). That means,

* 1000 stores 0,
* 1001 stores 4,
* 1002 stores 7,
* 1003 stores 6, and
* 1004 stores -2

Assume memory addresses increase by 1 unit just for simplicity. In practice, an `int` usually occupies 4 bytes on 64-bit systems, so addresses jump accordingly.

Now, `array[1]` would ideally refer to the first element in terms of normal mathematics. And `array[5]` would ideally refer to the fifth element.

But, we know that arrays are just pointers in C.

* The variable name itself refers to the starting point of the array, which is the first element in the array in terms of normal mathematics.
* And internally the system uses pointer dereferencing to obtain the value stored at a memory address. So, `array[i]` gets translated to `*(array + i)`.

Now if we want to access the first element, in terms of normal mathematics, the value of `i` is going to be `1` , isn't it?

* But the variable `array` itself points to the first element in the array!
* That's the issue we are dealing with.

The computer requires a consistent way to obtain consecutive addresses. And normal mathematics collide with how memory works.

If you were to use the normal way, you can't generalize a formula to obtain the consecutive address because of how we treat the first element and how the computer sees it.

But, it we point the first element by 0, the problem is solved. Because, we are not adding anything to base address, yet it works. It helps in generalizing a formula which we know as this:

```
address of element ith = base_address_of_array + (i-1)*sizeof(data_type)

base address = 1000, i = 4, data type is INT, sizeof(INT) is 4
=> address of 4th element = 1000 + (4-1)*4 = 1000 + 12 = 1012
where 4th is in terms of normal mathematics
```

***

That is why 0-based indexing is used by computers.
