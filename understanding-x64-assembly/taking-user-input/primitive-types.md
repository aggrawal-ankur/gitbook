# Primitive Types

## Note

We have 4 primitive data types: `char`, `int`, `float`, `double`. But we will talk only about `char` and `int`. The same rules apply to `float` and `double` .

## Premise

Broadly we can classify memory allocation in terms of function scope and file scope.

```c
#include <stdio.h>

// FILE SCOPE

int another_function(){
  // FUNCTION SCOPE
  return something
}

int main(void){
  // FUNCTION SCOPE
}
```

In both of these scopes, we can have:

1.  Declaration + Initialization.

    ```c
    int num = 45;
    char gen = 'M';
    ```
2.  Declaration only.

    ```c
    int num;
    char gen;
    ```

    Here, the two locations can be populated either later in the program itself or via user-input.

***

We know that, the default storage class for function scope is `auto` . And for file scope, it is `extern`.

### What if I explicitly put \`auto\` in a file scope declaration?

```c
#include <stdio.h>

auto int PI = 3.14;

int main(void);
```

You will get this:

```
$ gcc ./main.c
./main.c:3:10: error: file-scope declaration of ‘PI’ specifies ‘auto’
```

A file scope variable can't be made block scoped.

So, at file-scope, you can only use `static`, and `extern` is the default.

***

### What about making a variable \`static\` in block scope?

```c
#include <stdio.h>

int main(void){
  static int PI = 3.14;
}
```

This increases the lifetime of a variable (PI, here) but it is still block scoped. It makes the variable a "**private global**".

Take this:

```c
#include <stdio.h>

int sq(int n, int flag){
  static int ncalls = 0;
  
  if (flag != 1){
    ncalls++ ;
    printf("sq(%d) = %d\n", n, n*n);
    return ncalls;
  }
  if (flag == 1){
    return ncalls;
  }

}

int main(){
  sq(2, 0);
  sq(3, 0);
  sq(4, 0);
  sq(5, 0);
  printf("Number of calls made to square function: %d\n", sq(1, 1));

  return 0;
}
```

Here, `ncalls` is a static variable, so, its state is retained in every function call, instead of being allocated every single time, which is why the printf in main prints 4.

### What about extern in block scope?

You can't make a block scope definition `extern`. But, you can use `extern` to refer to a global declaration.
