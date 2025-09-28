---
title: Practical GDB
weight: 5
---

_**25 September 2025**_

***

Without wasting time, let's jump right into experiments.

## Setup

I started my low level journey on May 01, 2025. Today, it is September 25, 2025. It has been around 5 months. In these 5 months, I have understood lot of theoretical concepts. I tried to visualize them using ASCII and other mechanisms but I have not seen them practically.

The idea is to go through each concept once again with the lens of gdb.

For every such exploration, the setup is going to be very simple. 

- We will create a simple C program.
- Compile it with debug information.
- Open it with gdb.

This will benefit us in two ways:

1. Our mental model will get strengthen as we no longer stand on theory which is not verified.
2. Each exploration would require us to use a different part of gdb, enabling us to understand its commands even further with proper context instead of rote learning.

---

Below is the list of all the "theory" we are going to relive/verify with gdb. **Note: The list is updated progressively with each exploration.**

1. [Memory is a flat-array of byte addressable blocks](./memory-is-byte-addressable.md)