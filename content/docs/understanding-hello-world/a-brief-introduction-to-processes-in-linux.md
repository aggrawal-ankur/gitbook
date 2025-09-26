# A Brief Introduction To Processes In Linux

## Premise

When we execute a program, what really happens?

```bash
$ whoami
my_username_is_amazing
```

That's what we are going to find now.

## A Wedding Ceremony

Everyone is familiar with wedding ceremonies. It is a high chance that you have witnessed a marriage in your own family.

Although marriages vary a lot based on culture and traditions, but a few things are consistent across everything.

You have to decide the venue where everyone in your family would come together and the act of marriage would happen. It might be an open garden, a banquet hall or something else.

Next you have to decide what kind of decoration you want to have at the venue. Flower decoration, color choices, ceiling decoration, stage background, lights etc....

A meal is also offered to everyone who comes to bless the bride and the groom. So you decide the menu.

A return gift is also offered to the closed ones so you have to decide on that.

Depending on culture and traditions, this thing can go long or short. But every wedding does at least this as a bare minimum.

A marriage is a complete process, isn't it? And the act of marriage (the ceremonial part) is only a small part when compared to everything that goes behind. Only that is shown to everyone but when you count what enables it, you know that the act of marriage is just a tiny part of the whole process.

***

If that makes sense, you have already understood processes at a higher level. You only lack terminologies and the nuances, which we are going to be exploring very soon.

## Introducing Processes In Linux

A process is a container created by the operating system that holds all the necessary resources to execute a program.

What are these necessities?

1. Virtual address space, or _the marriage venue_.
2. Segments, a.k.a _the preparations_.
3. Program headers, or _the schedule, the invitation card_.
4. A dynamic interpreter, a.k.a the not necessary, but very common person these days, a wedding anchor.
5. Relocations, or _the event-day preparations_.
6. Execution, a.k.a the day of marriage.
7. At last, cleanup.

## Virtual Address Space

There are thousands of processes running normally. The number rises when we multitask.

Just imagine how crazy and chaotic it would get to manage millions of process inside the RAM, with all demanding various services like stack and heap.

This is why an abstraction known as virtual address space (or VAS) exist. Every process is executed in an isolated environment called virtual address space.

A process image is the complete in-memory layout of a program after it has been loaded into memory by the OS.

It is the answer to the question, "What the process looks like in the RAM?" A process image is the memory representation of a program at runtime.

It includes code, data, stack, heap, environment, memory-mapped regions, loaded libraries etc....

It is created by the kernel based on the ELF layout.

## Segments

Segments are logical grouping of multiple sections.

## Program Headers

Program headers are a set of structures in an ELF file that describe how to create a process image in the memory.

It describes how the operating system should load the ELF binary into the memory. It maps parts of the binary into memory regions with specific permissions and purposes.

***

That's all we need to know about processes for now.

**Note: This is just the start. We will explore processes in real depth when the time comes. Until then, lets move on to the next thing.**
