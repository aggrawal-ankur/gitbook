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

A random text file may start with `45 4c 46` bytes, but it is very unlikely for a text file to start with `7f 45 4c 46` . That is why a random character is used.

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

Those who have taken C tutorials can spot something here. So, its worth addressing.

* Depending on the time you have watched that tutorial and the creator of it, you may have seen different functions to read a file. They may include `fscanf`, `fgets` etc.
* The key lies in parsing those raw bytes. Those tutorials focused on text files. We are dealing with binary files, which need different handling.
* We have to work on interpreting those bytes the right way. Either we do it ourselves or outsource it some API. `fread` is that API.

### Return Value

If reading was successful, it returns the number of items read. This is what we use to verify if `fread` was successful or not.

If fewer than 4 bytes are read, the file is too short to be a valid ELF.

***

_If you wonder why `fread` needs size and count of entries, instead of just byte count, remember, C is statically-typed and `fread` allows you to abstract away the complexity of parsing and interpreting raw bytes according to some data type. If you want to deal with raw bytes directly, use the UNIX system call API `read` ._

_If you are still unsure about it, and want to dive deep into it, I've written a short detour_ [_here_](https://ankuragrawal.gitbook.io/home/~/revisions/lowdzHlD13Xe1P8sFUmd/low-level-detours/why-c-is-statically-typed)_._

For more information on `fread`, visit its man page.

* `man fread`&#x20;
* [man7 online](https://man7.org/linux/man-pages/man3/fread.3.html)

***

## Verifying The Magic Bytes

```c
#include <stdio.h>
#include "verify_elf.h"

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

### Why unsigned char?

`char` is 1-byte, so it is appropriate to store magic bytes. But `char` can be signed (-128 to 127) or unsigned (0-255).&#x20;

We have to make sure that it is unsigned because the magic bytes for an ELF are unsigned.

***

### Why \`fprintf\` not \`printf\`?

Lets make it clear. C does have abstraction. But those abstractions are usually a collection of very low level stuff.

`printf` defaults to printing at standard out `stdout`. `fprintf` allows you to set the direction for the output stream.

Even these are just wrapper APIs. The actual heavy lifters are `v*` prefixed printfs.

`fprintf` lets us send error messages to `stderr` instead of mixing them with normal output.

***

We are passing a reference of the `magic_number` array because `fread` expects a pointer.

## Conclusion

And we have checked if the file passed to our program is an ELF or not.

Next we will parse the file headers.
