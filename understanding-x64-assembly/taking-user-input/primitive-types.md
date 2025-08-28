# Primitive Types

## Note

We have 4 primitive data types: `char`, `int`, `float`, `double`. But we will talk only about `char` and `int`. The same rules apply to `float` and `double` .

## Theoretical View

Broadly, we can classify memory allocation in terms of function scope and file scope.

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

### Outside Function Declarations

```c
#include <stdio.h>

int PI = 3.14;            // extern, by default
auto int PI = 3.14;       // Not allowed
static int PI = 3.14;     // Makes the variable File Scoped.
extern int PI = 3.14;     // Raises a warning, but no problem

int main(void);
```

### Inside Function Declarations

```c
// main.c
#include <stdio.h>

int main(void){
  int PI = 3.14;            // auto, by default
  auto int PI = 3.14;
  static int PI = 3.14;     // Lifetime is changed to "until the program exist"
                            // Scope is still block-level

  extern int PI = 3.14;     // Raises error; A block scope declaration can't be made extern

  // But, we can refer to an already existing variable with external linkage/global visibility
  extern int global_PI;     // refers to the declaration in another.c
}
```

```c
// another.c

int global_PI = 3.14;       // extern, by default
```

***

#### What is the use of \`static\` in block scope?

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
  return -1
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

