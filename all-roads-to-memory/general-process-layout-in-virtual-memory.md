# General Process Layout In Virtual Memory

## A Big Picture Layout Of The Virtual Address Space

```
High Address
                    Top Of Virtual Address Space

0xFFFFFFFFFFFFFFFF *-----------------------------* End Of Kernel Space ↓
                   |                             |
                   |        Kernel Space         |
                   |                             |
                   |       Size: ~128 TiB        |
                   |                             |
                   |         Upper Half          |
                   |                             |
0xFFFF800000000000 *-----------------------------* Start Of Kernel Space ↑
                   |                             |
                   |    Unused / Guard Space     |
                   |                             |
0x0000800000000000 *-----------------------------* End of User Space ↓
                   |                             |
                   |         User Space          |
                   |                             |
                   |       Size: ~128 TiB        |
                   |                             |
                   |         Lower Half          |
                   |                             |
0x0000000000400000 *-----------------------------* Start Of User Space ↑
                   |                             |
                   |     Reserved / Unmapped     |
                   |                             |
0x0000000000000000 *-----------------------------*

                   Bottom Of Virtual Address Space
Low Address
```

## User Space Layout

```
0x0000800000000000 *-----------------------------* End of User Space ↓
                   |    Stack (grows downward)   |
                   *-----------------------------*
                   |    Memory-Mapped Region     |
                   |  (shared libs, mmap, ....)  |
                   *-----------------------------*
                   |     Heap (grows upward)     |
                   *-----------------------------*
                   |  Static && Global Variables |
                   |       (.bss / .data)        |
                   *-----------------------------*
                   |            .text            |
0x0000000000400000 *-----------------------------* Start Of User Space ↑
```

* `.bss` and `.data` lives together because they are functionally the same thing, they just differ in initialization.
