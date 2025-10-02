---
id: 32490ce1c9a646d2a505ee9bc1b0cda6
title: Practical GDB
weight: 4
---

_**25 September 2025**_

***

I started my low level journey on *May 01, 2025*. It is *September 25, 2025, ~5 months*. In these 5 months, I have understood lot of theoretical concepts. I tried to visualize them using ASCII and other mechanisms but I have not seen them practically.

The idea is to go through each concept once again with the lens of gdb.

For every such exploration, the setup is going to be very simple. 

- We will create a simple C program.
- Compile it with debug information.
- Open it with gdb.

This will benefit us in two ways:

1. Our mental model will get strengthen as we no longer stand on theory which is not verified.
2. Each exploration would require us to use a different part of gdb, enabling us to understand its commands even further with proper context instead of rote learning.

We have not explored "position-independent code" (or PIC) and "address-space layout randomization" (or ASLR) yet, so we will keep our exploration limited to position dependent code.

- Does that limit us? Yes, it does.
- But ASLR being disabled is a boon to us, not a problem as we are in the process of forming our mental model for debugging. We are still learning debugging and ASLR is a complexity creator. So avoiding it right now is a good decision.

Once we establish a baseline mental model for debugging, we will explore ASLR as well.

---

Below is the list of all the "theory" we are going to relive/verify with gdb. **Note: The list is updated progressively with each exploration.**

1. {{< doclink "7b2345107d0e4d3ab0e3369174a52eb1" "Memory is a flat-array of byte addressable blocks." >}}

{{< doclink "7b2345107d0e4d3ab0e3369174a52eb1" "" >}}
{{< doclink "53c4e11979834a43bdeac95f8827400e" "" >}}
{{< doclink "a91507ff9bbf4fbe82ffe1633e869b6b" "" >}}