---
id: 243880d83f464517a201007716ffc581
title: Understanding Hello World
weight: 2
---

***Originally written between late june and early july 2025***

***Polished on October 03, 2025***

---

Everyone starts their coding journey with `Hello, World!`. It takes only 4 lines in C:

```c {filename="hello.c"}
#include<stdio.h>

int main(void){
  printf("Hello, World!\n");
}
```

But how does it really work? We are going to find that out.

**Note: It's a complete rabbit hole. And this exploration will prove that *hello-ing* the world is not that easy.**

The journey is long and can be divided can into 4 phases.

- {{< doclink "3ae550fdab0b4a9194d68d355610326b" "Orientation" >}}
- {{< doclink "42957ab7594145f0b492a14d2f38a783" "Preprocessing" >}}
- {{< doclink "9d652181ee714f7988c5ed164e4cae4e" "Compilation" >}}
- {{< doclink "203d1929b23e43889ec4efc90aa826bd" "Assembling" >}}
- {{< doclink "2dd6b2a9670b44fe85f22ce6ab568565" "Linking" >}}