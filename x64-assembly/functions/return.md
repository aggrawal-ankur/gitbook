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
