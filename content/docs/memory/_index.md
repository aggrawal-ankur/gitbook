---
title: All Roads To Memory
weight: 4
---

## Update Timeline 

_**August 9, 2025 (init write up)**_

_**September 13, 2025 (rewrite triggered by dynamic memory allocation, but didn't do anything)**_

**September 29, 2025 (another rewrite triggered by gdb sessions requiring polish of hello-world write ups where I found the void-main write up placed wrongly which I thought would be best explained alongside processes so I started polishing and that triggered the whole restructuring)**

---

Processes and virtual memory are two very interlinked concepts.

- Every time we execute a command, a binary is executed.
- To execute a binary, Linux kernel creates a process.
- A process is a running instance of a binary.
- What do you mean by "a running instance"? How that "running instance" looks like? The answer is virtual memory.

Obviously processes exist in physical RAM, but managing processes in physical RAM is not easy.

- So engineers created an abstraction called virtual memory and a procdure that maps virtual memory with physical memory.
- This way, we have delegated the messy task to an automated system and focus more on building stuff.

To understand Linux processes, we have to understand virtual address space/layout (VAS).

- A huge part of understanding virtual memory is restricted to VAS only.
- But virtual memory is incomplete without the procedure that maps it with physical memory.

So, without complicating it anymore, this is the roadmap of our exploration.

- We will start by understanding VAS.
- Then we will proceed to processes.
- After this we will explore the "mapping procedure".

Where I am gonna place dynamic memory allocation?

- Sigh! It's tough.
- Although it is a different thing and we can explore it once we are done with VAS, I genuinely have no idea where to place it.
- I know that there is a lot that goes in the "mapping procedure" and I have explored it on surface only, so I know that a dedicated place is required for it but that's a lot of work which is not required at this point.
- Right now I just want to manage this void-main and process stuff so that I can continue gdb-sessions.