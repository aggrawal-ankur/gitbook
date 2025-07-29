# Magic Verification API

## Problem Statement

The first step in parsing an ELF is to verify if the file loaded is an ELF or not.

How can we do that? By verifying the magic bytes (or numbers) in the file headers.

## What are magic numbers?

Magic numbers can take multiple forms in computer programming. In our case, it is a constant stream of characters, used to identify a file format.

While statically analyzing the hello world binary, we had started by analyzing the file headers. The readelf output started like this:

```
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
```

The first 4 hexadecimal numbers represent the magic number.

But `readelf` refers all the pairs as magic?

* Actually, only the first 4 pairs form the magic number. Rest are the values in the `e_ident[]` array, which is a part of the file headers.

Remember, each pair is hexadecimal so they are 1 byte in size.

### Does this magic number hold any meaning?

Yes. `0x7f` = DEL, `0x45` = E, `0x4c` = L and `0x46` = F

### Why \`0x7f\` ?

A random text file may start with `45 4c 46` bytes, but it is very unlikely for a text file to start with `0x7f 45 4c 46` . That is why a random character is used.

## Reading The Magic

To mark a file as a valid ELF, the first 4 bytes must be `0x7F 0x45 0x4C 0x46` . We will use `fread()` to read those bytes.

It is provided by the C standard I/O library (`stdio.h`). The signature of `fread()` is as follows.

```c
// General Signature
fread(dest_ptr, size_each_element, n_elements, file_ptr);

// From Manual
size_t fread(void ptr[restrict .size * .nmemb], size_t size, size_t nmemb, FILE *restrict stream);
```

`fread` requires 4 arguments.

* `dest_ptr` is where the raw bytes would be stored after extraction.
* `n_elements` is the total number of elements we are extracting.
* `size_each_element` is self-explanatory.
* `file_ptr` has access to the file's raw bytes. This is how we are going to read the file.

It reads N number of elements each of size S from the file pointer and stores them in the destination pointer.

### Return Value

If reading was successful, it returns the number of items read.

### Why fread is like this?

Why we can't just pass the number of bytes we've to read?

The answer is rather simple. C is strictly-typed. It has data types for everything. But the key lies in how those data types are translated at memory level as there exist only raw bytes.

So, how those data types are translated at memory level?

* Lets take an example of storing 42.&#x20;
* The data type is `int`, which takes 4-bytes on 64-bit systems.
* But what is 42 at binary level? `00101010`&#x20;
* What if we prefix it with 24 zeroes, like this: `00000000000000000000000000101010` ? It is still 42, isn't it? What has changed is that this is a 4-byte representation of a decimal value 42 and `00101010` was a 1-byte representation of the decimal value 42.
* Suppose 42 is stored at a memory `0x1000`. We use the move operation to load it in the accumulator, like this: `mov eax, [0x1000]` , intel syntax. What does this instruction really mean?
* It means, go on offset `0x1000`, read 4 consecutive bytes from there, `0x1000, 0x1001, 0x1002, 0x1003` , sort them from little-endian to big-endian, combine them and put them into the accumulator.
* And what is there on these offsets? Since computers prefer little-endian system, the order of bits would be reversed. `0x1000 = 0x2A (42), 0x1001 = 0x00, 0x1002 = 0x00, 0x1003 = 0x00` .

How does this relate with `fread`?

* Interpretation is where the problem is.
* Raw bytes are raw because they can be interpreted as the programmer wants. For a `char` type value, 42 is `*`. For an integer it is `0d42`. In hex system, it is `0x2A`. In octal system, it is `0o52`. Who will account for these interpretations?
* For `char`, `0x1000, 0x1001, 0x1002, 0x1003` are logically distinct locations. For `int32` , `0x1000, 0x1001, 0x1002, 0x1003` is an array of two values (42 and 0). For `int64`, it is one-single value, 42.
* This is why `fread` needs to know which data type we are interpreting (though size of each entry argument) and the number of elements of such data type.

***

For more information on `fread`, visit its man page.

* `man fread`&#x20;
* [man7 online](https://man7.org/linux/man-pages/man3/fread.3.html)

## Verifying It Is ELF Or Not!

```c
#include <stdio.h>
#include "verify_elf.h"

int verify_elf(FILE* file_object){
  unsigned char magic_number[4];

  // Reading the first 4-bytes
  if (fread(&magic_number, 1, 4, file_object) != 4) {
    fprintf(stderr, "Error: `fread()`: Unable to read ELF magic bytes.\n");
    fclose(file_object);
    return -1;
  }

  if (magic_number[0] != 0x7f || magic_number[1] != 'E' || magic_number[2] != 'L' || magic_number[3] != 'F'){
    fprintf(stderr, "Error: Unexpected magic bytes returned.\n  Expected: `0x7F, E, L, F`\n  Found: %c, %c, %c, %c\n", magic_number[0], magic_number[1], magic_number[2], magic_number[3]);
    fclose(file_object);
    return -1;
  }

  return 0;
}
```

### Why unsigned char?

`char` is 1-byte, so it is appropriate to store magic bytes. But `char` can be signed (-128 to 127) or unsigned (0-255).&#x20;

We have to make sure that it is unsigned because the magic bytes for an ELF are unsigned.

***

We are passing a reference of the `magic_number` array because `fread` expects a pointer.

We are reading 4 elements, each of size 1-byte.

And we are done. But there are two more questions I would like to ask here.

### Why we are not using \`read\`?

If you have taken a C tutorial, you know that in the file I/O section, we use the `read()` and `write()` functions to operate on files.

`fread` belongs to the standard I/O library. It is designed to aid in file operation.

`read` , on the other hand, belong to the UNIX standard library, or `unistd.h` . It provides access to the POSIX operating system API.

The signature for `read` is:

```c
ssize_t read(int fd, void *buf, size_t count);
```

In simplest terms, `fread` provides a healthy abstraction where we don't have to manage extraction of bytes and their interpretation. Otherwise, if we chose to go with `read`, we have to manage all that ourselves. Plus, `fread` is portable as well and `read` is UNIX-dependent.&#x20;

### Why we are using \`fprint\` when we have \`printf\`?

In assembly, the `exec` syscall is the main one and `execve`, `execvp` are just wrappers around it. The same is with `*printf*` functions, just remove the idea of syscall.

If we open the `man 3` entry for `printf`, we can find a big list of `*printf*` function.

```
printf,   fprintf,  dprintf,  sprintf, 
snprintf, vprintf,  vfprintf, vdprintf, 
vsprintf, vsnprintf
```

Why `man 3`?

* The `3` corresponds to **library calls** (functions in program libraries) section. If you do `man printf`, you will find the entry for `printf` as a **user command**.

Only the `v*` variants of `printf` are the real workers. Everything else is just a wrapper around them.

For example, `printf` is a shorthand for `fprintf(stdout, const char*, format);` .&#x20;

Clearly, `fprintf` lets us choose the output stream. It can be `stdout`, `stderr` or even a `FILE*` . We are using `stderr` as it keeps errors separate from the standard output and they can be directed elsewhere.

## Conclusion

And we have managed to verify if the file passed to our program is an ELF or not.

Next, we will parse the file headers.
