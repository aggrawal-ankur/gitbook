---
id: 859c0974e319471ca2f0a27bfc393f9f
title: 0-based indexing
weight: 7
---

***Originally written in early July 2025.***

***Polished on October 04, 2025***

---

When we do counting, we start from 1, not 0. Why do computers count from 0? Why arrays in C index from 0?

There are programming languages which use 1-based indexing as well.

Look at this code.
```c
#include <stdio.h>

int main(void){
  int array_ptr[] = {0, 4, 7, 6, -2};
  for (int i = 0; i < 5; i++){
    printf("%d, ", *(array_ptr + i));
  }
}
```

This program creates an integer array of size 5 and a for-loop to iterate over it.

To display each element, it uses pointer dereferencing rather than subscripting the array variable using square brackets, like this `array_ptr[i]`.

Suppose the array is loaded at address 1000 (in decimals). That means,
  - 1000 stores 0,
  - 1004 stores 4,
  - 1008 stores 7,
  - 1012 stores 6,
  - 1016 stores -2

The variable name itself refers to the first element in the array.

`array[i]` is basically `*(array + i)`.

If we want to access the first element by normal mathematics, `i = 1`.
  - That'd be, `*(array + 1)`, which is `*(base_addr + 1*4)`

That's why, most general-purpose programming languages use 0-based indexing as it aligns perfectly with how memory is managed at low level.