# Understanding \`Hello, World!\`

Everyone starts their coding journey with a `Hello, World!\n` program.

It takes only 4 lines to do this in C:

{% code title="hello.c" %}
```c
#include<stdio.h>

int main(void){
  printf("Hello, World!\n");
}
```
{% endcode %}

But how does it really work? This is what we are going to explore here.

## Expectations

It's a complete rabbit hole. And this exploration will prove that _hello-ing the world_ is not that easy.
