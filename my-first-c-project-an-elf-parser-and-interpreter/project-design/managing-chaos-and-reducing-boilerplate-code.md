# Managing Chaos & Reducing Boilerplate Code

As I started creating APIs to extract raw bytes, I observed that each API needs at least two things.

1. File object
2. File headers

I thought that it would be better to open the file once in the main program and pass it to each API call. Same idea with file headers.

***

## Return Problem

When the APIs grew in size, I spotted another problem.

In C, you can only return one thing. But the API parsing section header string table requires to export/return 4 things.

1. Formatted array of strings.
2. Count of total string in formatted array.
3. Raw array of strings.
4. Total number of bytes in the raw array.

```c
int parse_shstrtab(FILE* f_obj, Elf64_Ehdr* ehdr, char** out_raw_shstrtab, char*** out_shstrtab, int* entry_count, int* raw_c);
```

I am using heap-allocated pointers to export these values.

Although the problem of returning multiple values is solved, another problem was created.

Function declarations were exceeding my display width. It felt uneasy both to see the declarations like this and manage the flow of arguments.

On one hand, passing the dependencies and return pointers as arguments was making the APIs do only what they are designed for, which make them easier to debug. But I was required to manage those pointers in the main program, which is a pain.

If I choose to make APIs self-contained, meaning, I call every API it depends on inside itself, I have to write a lot of boilerplate code, making the code redundant and less modular.

So, what's the solution?

## \`struct\` Based Design

The idea is to pack every API call in one struct and instead of passing the dependencies one-by-one, pass the complete struct itself.

### How Is It Better?

1. I have to write less boilerplate code both in the main section and in the individual APIs.
2. Size of function declarations would be minimized.
3. Keeps the APIs modular and to-the-point.
4. Variable management chaos is reduced.

### What Are The Drawbacks?













