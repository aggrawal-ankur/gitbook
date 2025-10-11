---
id: 1b8476a12a9a485caeadf2c5d56c379b
title: Linux Processes
weight: 6
---

When we execute a program, what really happens?

```bash
$ whoami
my_username_is_amazing
```

That's what we are going to find now.

## A Wedding Ceremony

Everyone is familiar with wedding ceremonies. Although marriages vary a lot based on culture and traditions, but a few things are similar across every marriage event.

- The venue.
- Even planning (decoration, lighting etc....)
- Food menu.
- A return gift for the closed ones.

A marriage is a complete process and the act of marriage (the ceremonial part) is only a small part of it when considered everything that goes behind.

***

If that makes sense, you have already understood processes at a higher level.

## Linux Processes

A process is an isolated event created by the OS that has everything execute a binary. It includes:

1. Virtual address space -> _the marriage venue_.
2. Segments -> _the preparations_.
3. Program headers -> _the schedule, the invitation card_, informing the guests about your schedule.
4. A dynamic interpreter -> *the event organizer*.
5. Relocations -> _the event-day preparations_.
6. Execution -> *the day of marriage*.
7. At last, cleanup.

If you have not noticed already, everything except virtual address space belongs to ELF, which we have explored previously, {{< doclink "13e94d7a205c4b309f82d234663a8b8d" "introduction to ELF" >}}