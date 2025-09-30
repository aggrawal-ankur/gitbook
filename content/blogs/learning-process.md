---
id: c3f2f51ba3c54daf8f0ac0c1daa8c5a4
title: Learning Process Optimization
sidebar:
  exclude: true
---

_**Got the idea to write this on 17 September 2025, 5:30 PM**_

***

My gitbook is the proof of all the low level knowledge and understanding I have about computers.

I write everything I learn in a teaching format so that I can find patches in my understanding. This helps in strengthening my overall understanding of a topic.

In this rigorous process, I invest a lot of time and energy in optimizing my write ups so that I can understand to the best of my capabilities. Often this comes at a cost of time and cognition.

Just to refine my understanding more and more to the point that I can say "I really understand it", I do end up investing a lot more time and energy than probably required.

For many it is a waste, but not for me. Such pursuits always reveal something about the process that I can optimize next. Each such exploration becomes a tool which is going to save a lot of my time and energy in future explorations.

And this is where I am listing all those tools with some examples in my own write ups.

Hope they help you as well.

***

_**September 14, 2025**_

Searching for in-depth information on google is sometimes a nightmare.

In my journey, I try to avoid google searches and stick to formal documentations and ChatGPT because they save my time and energy.

I ask ChatGPT to introduce me to a concept and then I ask for documents if any. I ask it if I can write some code myself to try it out. This way, I am able to build a deeper understanding of the concept, rather than reading half-baked articles claiming for an in-depth dive.

Many articles on internet aren't even exactly for the thing you search for. Take `dlmalloc`.

* When I was understanding allocators, I can't find anything relevant but heap exploitation.
* Let me understand heap before I understand its exploitation? And the information shared there about dlmalloc is literally of no use to me. And I have wasted almost 4-5 days in them.
* Then I started understanding the dlmalloc annotations and asking ChatGPT what I don't understand. Once I start to feel confident, I document my understanding here. Then I polish them.

In this process, I have found that the images tab in google search is a goldmine for websites that can't make up on the first page. I have found so many websites with great content (obviously not related to the current pursuit but something later).

So, image tab is always worth a try.

***

_**September 15, 2025**_

ASCII art is a very great tool for visualizing boring theoretical concepts.

Why theory is hated is because you can't visualize it. While I was learning low level stuff, I was basically studying a lot of theoretical concepts which I can't see properly.

Take stack. You can use `gdb` to look for a process's running stack but it is just addresses. But if you map that theory in an ASCII diagram, you get exactly how a stack of plates looks like.

* Everyone just says that a process's stack is just like a stack of plates, but can you prove that? Without any cryptic looking addresses which just haunt beginners?
* Why not? You can absolutely do that. And you don't need fancy canvas tools to draw stack. Just use ASCII. And by the way, just open VS Code and paste any ASCII art from my write ups, it looks absolutely gorgeous.

* {{< doclink "3a6396d0fd41408ab6f4e7cc0b452d38" "How the stack frame looks like?" >}}
* {{< doclink "632446e0d44244308a8146eabf6433b3" "Virtual memory layout" >}}

**You absolutely don't need fancy tools to draw theory. Theory shouldn't be daunting.**

***

_**September 17, 2025**_

The best way to represent "type" related information is a table. A table can consolidate huge amounts of information in a very small form factor.

It reduce the mental overhead of "too much information, not my cup of tea". Plus, a table looks prettier than a dense paragraph.

That's why if there is a possibility to explain something using a table, I am always up for that and it is very much reflected in my notes.

* {{< doclink "68860c0125cc44f0bb05de46ee9fb6c3" "Doug Lea's memory model" >}}
* {{< doclink "5b14ef9b921c4b3b839676cc42601d21" "Types of bins" >}}

***

_**September 21, 2025**_

How to ensure that my approach positions me better in the future?

There can be multiple answers to this question but almost all of them boils down to one thing — **prioritize long term over short term, my short term must align with my long term goals.**

And a few moments before, I found a way to implement it.

Recently I finished the theoretical part of understanding dlmalloc, which itself is a part of understand dynamic memory allocation. Now I want to verify all the theory I was learning since 2 weeks.

* For this I have to use dlmalloc as the memory allocator for my experimental programs and inspect the process as a sentinel being.
* I already got dlmalloc setup and running inside a VM, I didn't expect a 13 years code to run without any compilation errors, so a big thank you to Professor Doug Lea for maintaining the code quality to such a level.

Now this inspection can only be done via debugger. GDB is quite popular on Linux so that's my choice. Now there are two ways to approach this.

1. I just use and memorize gdb commands and do the inspection. That ensures speed.
2. Or I take a long road to understand the "fundamentals of debugging" and then learn how gdb implements them.

As you have guessed, I am more of type 2. And this is exactly what I did with dynamic memory allocation. I didn't read some articles on heap exploitation which touched dlmalloc on surface, I chose to explore dlmalloc myself. And there is a long way to go before I can say "I am done with dynamic memory for the time being."

Why the 2nd approach?

* The second approach maximizes learning the fundamental concepts on which everything is built.
* It is like maximizing for transferable skills, which remain consistent across different systems and architectures.

This approach ensures that I understand what the debugger is actually doing and it doesn't seem like black magic.

***

_**September 24, 2025**_

Never ever disrespect theory. If you disrespect theory, you will pay for it, in hefty sums.

Right now I am learning GDB so that I can verify all the theory I have understood about dlmalloc. As usual, before learning the main thing, I learn the peripherals. But now I am at the commands.

For everyone, these commands are just another commands. But the way I am seeing them is a treasure.

I have been diving into theory since May 2025. I started with x64 assembly, then hello world exploration for 35 days, ELF internals, more assembly, C to assembly mapping, virtual memory, dynamic memory allocation and then dlmalloc.

Up until this time, there was no way for me to testify my understanding. But now, I feel like I have found a cave full of treasure. It's like I have found they key to Ali Baba and the Forty Thieves cave.

I am not even doing any practical work here, I am just exploring what is all that can be done with gdb and while learning stack management, I found that local variables are present exactly the same way I learned about them. Registers are managed the same way I understood.

I am so excited that my own internal instruction pointer is lost right now. I am not able to understand which theory I should verify first.

If you have asked me this in August itself, I was literally going through agitation, frustration, and anger. There was no day when I would say "I am done with this." Now, you can feel how happy I am.

That's why I am telling YOU, don't ever escape theory, never ever despise it. It's brutal, it's boring, it's non-interesting, everything bad that you can think about; but it is the only thing that makes the future interesting and incredibly rewarding.

I feel proud of myself that in all those days of anger, frustration, agitation, I didn't chose to quit.

* I did stopped a lot. But I can't prove much of it. Only my mother can prove that because she has seen me packing my laptop and keyboard and putting them aside in another room and sitting alone at my place for multiple days doing nothing, just because he's so tired of doing it.
* And she has also seen days when I go to her and say "today I learned for 8 hours".

And now, I don't need anyone to rely on for this, because I myself am the proof that I did that, and the universe rewarded me later.

**So, never ever think about skipping theory.**

***

