---
title: Full Disassembly
weight: 2
---

While analyzing the object code, we have checked out full disassembly of the compiled file. We can do that here as well.

```bash
objdump linked_elf -D -M intel
```

Shocked, right! The disassembly is 800 lines long. The first and the immediate question is **WHERE ALL THIS ASSEMBLY IS COMING FROM?**

## The Big Picture

Our source code is a tiny part of the bigger picture.

There exist a complete infrastructure that runs this _hello world_ thing. And the build process is what that constructs this infrastructure, step-by-step.

In short, it is all compiler (`gcc`) generated.

## What is this infrastructure really about? What does it look like?

That's a very important question to ask, not a idea to gloss over just because it is complex to answer.

At the end of the day, everything is just code. There are bunch of object files that makes up the invisible infrastructure.

The next question would be, _how does all of this code become one single entity?_

* That's the job of linking. It's not the only thing that the linker do, but one of the things.

Each object code has its own ELF structure. When the linker combines them, a unified structure comes out, which is our final binary.

## What to do with this disassembly?

This disassembly exposes almost everything, therefore, it is a roadmap for us. But to read that roadmap, we have to understand the things it points to.

There is no meaning in reading it line by line. We will use it in the process to make sense of what we are doing and why we are doing it.

Although I could have avoid it now because we are going to visit it anyway, but I don't want to make those visits look strange.&#x20;

* It is possible that someone had visited it earlier, it would mess with their mind. This is the reason why I decided to left an explanation before it consumes that learner.
* Throughout the process, we are going to use the **full disassembly**. It's an incredible tool at our disposal.

With that in mind, we can move now.