# Magic Verification API

## Problem Statement

How we will know if the file passed to our program is an ELF? We have to verify the magic number in the file headers.

## What are magic numbers?

A magic can take multiple forms in computer programming. In our case, a magic number is a constant stream of characters which are used to identify a file format.

While statically analyzing the hello world binary, we have analyzed the file headers. The readelf output started like this:

```
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
```

The first 4 hexadecimal numbers represent the magic number.

But readelf refers all the pairs as magic?

* Actually, only the first 4 pairs form the magic number. Rest are the values in the `e_ident[]` array.
* We will see it very soon.

Each pair is 1 byte in size.

### Does this magic number hold any meaning?

Yes.

`0x7f` = DEL, `0x45` = E, `0x4c` = L and `0x46` = F

### Why \`0x7f\` ?

A random text file may start with `45 4c 46` bytes, but it is very unlikely to start with `0x7f 45 4c 46` . This is the reason behind why a radon character is used.

## Verifying File Headers

So, to verify that a file is a valid ELF, the first 4 bytes must be `0x7F 45 4C 46` .

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

  // We know that an ELF binary start with 4 magic bytes. These are `0x7f`, `E`, `L`, `F`.
  // Lets verify this.
  if (magic_number[0] != 0x7f || magic_number[1] != 'E' || magic_number[2] != 'L' || magic_number[3] != 'F'){
    fprintf(stderr, "Error: Unexpected magic bytes returned.\n  Expected: `0x7F, E, L, F`\n  Found: %c, %c, %c, %c\n", magic_number[0], magic_number[1], magic_number[2], magic_number[3]);
    fclose(file_object);
    return -1;
  }

  return 0;
}
```

`char` is 1-byte, so it is appropriate to store the magic bytes. Why `unsigned char`?

* `char` can be signed (-128 to 127) or unsigned (0-255).
* We have to make sure that it is unsigned because the magic bytes for an ELF are unsigned.















