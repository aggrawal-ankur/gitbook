---
title: Memory Is Byte Addressable
weight: 6
---

_**26 September 2025**_

***

The first idea that we are going to verify is:

&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; "_memory is a flat array of byte addressable blocks_".

## Setup

Take this program.

```c
#include <stdio.h>

int main() {
  int x = 0x12345678;
  return 0;
}
```

Compile with debug information:

```bash
gcc -g main.c -o binary
```

Open inside gdb.

```
$ gdb ./binary
(gdb)
```

Clear the window with `CTRL+L` .

***

## Exploration Begins

### Command Background

GDB allows us to inspect individual memory locations via the examine command.

We can open its help page by doing:

```
(gdb) help x
```

The examine command has the following syntax:

```
(gdb) x/FORMAT ADDRESS
```

* FORMAT specifies how we want to inspect memory.
* ADDRESS refers to the memory location we want to inspect.

FORMAT is made up of three arguments.

The third argument specifies how much memory we want to inspect.


| Description | Argument |
| :--- | :--- |
| To inspect only one block in the memory, or only the address passed as argument. | b |
|  |  |
|  |  |