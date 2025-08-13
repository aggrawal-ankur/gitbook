# How an uninitialized character buffer exist and managed at low level?

## Premise

This article explores these low level concepts, based on the following source.

1. How storage class affects memory allocation?
2. How memory is managed via stack?
3. How local variables exist
4. How are format specifiers interpreted?

```c
#include <stdio.h>

int main(void){
  char NAME_BUFF[100];

  printf("Enter your name: ");
  scanf("%s", NAME_BUFF);

  printf("Hello, %s!\n", NAME_BUFF);
}
```

