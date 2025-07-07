# Macro Level Understanding

Now we can start understanding the low level architecture fueling `Hello, World!\n`.

This is the source we are going to analyze \~

```c
#include<stdio.h>

int main(void){
  printf("Hello, World!\n");
}
```

We are going to have a look at the:

1. generated assembly (x86\_64 Intel syntax),
2. object code,
   1. elf headers, and
   2. disassembly.
3. linked code (elf binary)
   1. elf headers, and
   2. disassembly.
4. Whole runtime picture (the real danger)

[The source can be found here](https://github.com/hi-anki/rev-eng/blob/main/program1/hello.c)
