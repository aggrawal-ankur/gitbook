# How returns are managed?

## Premise

Returns can be classified into 3 types:

1. **Primitives** (int, char, float, double): the return is in register (`rax` for int and char, `xmm0` for floats)
2. **Arrays**: they can't be returned. Period. You pass a reference to a modifiable memory from the caller itself. To return a local declaration, you make it block static.
3. **Structures/Unions**: this is where the problem is.

## Returning Structures/Unions

System V ABI decides return strategy based on size and fields.

1. If the return size is <= 16 bytes, it is returned in registers.
2. If the return size is > 16 bytes, it is complicated.

***

So far, we have seen that simple computational results are returned in accumulator. What about complex data types like array, pointer, structure and union? Let's talk about them.

Returns can be divided into 3 types:

1. Primitives (int, float, char, double): registers (`rax`, `xmm0` for floats)
2. Arrays
3. Structures

C can't return arrays. Period.

* If you want to return an array declared in an upper stack frame to the lower one, the only way is to make it a block static declaration.
* Otherwise, use heap. Simple.

Structures are a little complex.

* System V ABI decides the return strategy based on size and fields.















