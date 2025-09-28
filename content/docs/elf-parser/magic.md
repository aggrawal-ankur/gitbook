---
title: Magic Verification
weight: 3
---

## Problem Statement

The first step in parsing an ELF is to verify if the file passed in the argument is an ELF or not.

This is done by verifying the magic bytes (or numbers) present as the first thing in all kinds of binary files.

## What are magic numbers?

Magic numbers can take multiple forms in computer programming. In our case, it is a constant stream of characters, used to identify a file format.

From the static analysis of the hello world binary, we know that file headers are the first thing in an ELF. The output for readelf started like this:

```
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
```

The first 4 hexadecimal numbers represent the magic number.

But `readelf` refers all the pairs as magic?

* Only the first 4 pairs of hexadecimal values form the magic number. Rest are the values in the `e_ident[]` array, which is a part of the file headers.

_Remember, each pair is hexadecimal so they are 1 byte in size._

### Does this magic number hold any meaning?

Yes. `0x7f` = DEL, `0x45` = E, `0x4c` = L and `0x46` = F

### Why \`0x7f\` ?

A random text file may start with `45 4c 46` bytes, but it is very unlikely for a text file to start with `7f 45 4c 46` . That is why a random character is used.

## Reading The Magic

To mark a file as a valid ELF, the first 4 bytes must be `0x7F 0x45 0x4C 0x46` . We will use `fread()` to read those bytes.

It is provided by the C standard I/O library (`stdio.h`). The signature of `fread()` is as follows.

```c
// General Signature
fread(dest_ptr, size_each_element, n_ele, file_ptr);
```

`fread` requires 4 arguments.

* `dest_ptr` is where the raw bytes would be stored after extraction.
* `n_elements` is the total number of elements we are extracting.
* `size_each_element` is self-explanatory.
* `file_ptr` has access to the file's raw bytes. This is how we are going to read the file.

In simple words, _read N number of elements, each of size S, from the file pointer and store them in the destination pointer._

```c
// From Manual Entry
size_t fread(void ptr[restrict .size * .nmemb], size_t size, size_t nmemb, FILE *restrict stream);
```

* Lets discuss what `void ptr[restrict .size * .nmemb]` means.
* `nmemb` represents number of memory blocks to read.
* `size` represents the size of each memory block.
* `void *restrict stream` means the pointer can point to data of any type.
* `restrict` is a type qualifier introduced in the C99 standard. It tells the compiler that, _for the lifetime of this pointer, no other pointer will be used to access the object it points to._
* `ptr[restrict .size * .nmemb]` indicates that `ptr` is a pointer to a block of memory with a minimum size of `size * nmemb` bytes.

***

Those who have taken C tutorials can spot something here. So, its worth addressing.

* Depending on the time you have watched the **File I/O tutorials**, you may have seen a variety of functions to read a file. They may include `fscanf`, `fgets` etc.
* Those tutorials focused on text files. We are dealing with binary files, which need different handling.
* If you are known to assembly, you know that memory is a flat-array of bytes at low level. We have to interpret those bytes the right way to obtain the intended meaning. Either we do it ourselves or outsource it to some API. `fread` is that API.

### Return Value

If successful, it returns the number of items read. And this forms the basis for error handling.

***

_If you wonder why `fread` needs size and count of entries, instead of just byte count, remember, C is statically-typed and `fread` allows you to abstract away the complexity of parsing and interpreting raw bytes according to some data type. If you want to deal with raw bytes directly, use the UNIX system call API `read` ._

_If you are still unsure about it, and want to dive deep into it, I've written a short detour_ [_here_](https://ankuragrawal.gitbook.io/home/~/revisions/lowdzHlD13Xe1P8sFUmd/low-level-detours/why-c-is-statically-typed)_._

For more information on `fread`, visit its man page.

* `man fread`&#x20;
* [man7 online](https://man7.org/linux/man-pages/man3/fread.3.html)

***

## Verifying The Magic Bytes

{% code title="parser.c" %}
```c
int verify_elf(FILE* f_obj){
  unsigned char magic_bytes[4];

  if (fread(&magic_bytes, 1, 4, f_obj) != 4) {
    fprintf(stderr, "Error: `fread()`: Unable to read ELF magic bytes.\n");
    fclose(f_obj);
    return -1;
  }

  if (magic_bytes[0] != 0x7f || magic_bytes[1] != 'E' || magic_bytes[2] != 'L' || magic_bytes[3] != 'F'){
    fprintf(stderr, "Error: Unexpected magic bytes returned.\n  Expected: `0x7F, E, L, F`\n  Found: %02X, %02X, %02X, %02X\n", magic_bytes[0], magic_bytes[1], magic_bytes[2], magic_bytes[3]);
    fclose(f_obj);
    return -1;
  }

  return 0;
}
```
{% endcode %}

### Why unsigned char?

`char` is 1-byte, so it is appropriate to store magic bytes.

But `char` can be signed (-128 to 127) or unsigned (0-255). We have to make sure that it is unsigned because the magic bytes for an ELF are unsigned.

***

### Why \`fprintf\` not \`printf\`?

Lets make it clear. C does have abstraction. But those abstractions are usually a collection of very low level stuff.

`printf` defaults to printing at standard out (`stdout`). `fprintf` allows you to set the direction for the output stream. Therefore, the below two are the same.

```c
printf("Hi\n");
fprintf(stdout, "Hi\n");
```

Even these are just wrapper APIs. The actual heavy lifters are `v*` prefixed printfs. Checkout the library functions manual for `printf`.

* `man 3 printf`&#x20;
* [man7 online](https://man7.org/linux/man-pages/man3/printf.3.html)

`fprintf` lets us send error messages to `stderr` instead of mixing them with normal output.

***

We are passing a reference of the `magic_number` array as `fread` expects a pointer.

## Conclusion

And we have checked if the file passed to our program is an ELF or not.

Next we will parse the file headers.