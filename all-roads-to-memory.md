# All Roads To Memory

_**August 9, 2025**_

***

Understanding memory is very important.

Assembly told us that memory is a flat-array, made up of continuous blocks of 1-byte.

Static analysis of the hello world binary gave us a glimpse about how an ELF is mapped into memory.

The ELF dump project further proved that memory is flat.

***

In this journey, we have read things like `offset`, `virtual address`, `physical address` etc.

* We have seen that the assembler patches the labels with some sort of offset or virtual address.
* We have seen all the 3 phrases together in the readelf output for our binary.

***

Offsets refer to a location inside the ELF itself. These offsets are calculated based on the base address of the binary. The base address of the binary is where the binary is loaded.

We know that virtual address space exists to isolate processes. And the virtual memory address we see belongs to this space.

The virtual address is mapped into physical memory space, which is the actual hardware memory.

***

These series of articles attempt to understand the memory in depth. There are so many things and I'll try my best.

When I learn something, I try to explore it from history.

* For example, I started understanding memory from yesterday.
* I started from the evolution of computer memory. Everything from Sir Charles Babbage's Analytical Engine to Williams Tube to Punched Cards and all the way up to Semiconductor Memory.
* If you ask me today, I don't remember anything of it.
* I visit history to ground myself, not to remember it by words.
* Reading the history of something shows its complete evolution and you feel respect for all the contributors. That's the goal of this process.

Next I explored the evolution of semiconductor memory, because this is what we are using.

After this history class, which lasted around 1 hour, I was done and prepared to actually take memory lessons.

You are not going to find any history here.

Enough. Lets start exploring memory.
