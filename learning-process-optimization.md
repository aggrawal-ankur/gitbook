# Learning Process Optimization

_**Got the idea to manage this on 17 September 2025, 5:30 PM**_

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
* [How stack frame looks like?](https://ankuragrawal.gitbook.io/home/x64-assembly/functions/stack#how-is-a-stack-frame-structured)

[Virtual memory layout](https://ankuragrawal.gitbook.io/home/all-roads-to-memory/virtual-memory-layout)

**You absolutely don't need fancy tools to draw theory. Theory shouldn't be daunting.**

***

_**September 17, 2025**_

The best way to represent "type" related information is a table. A table can consolidate huge amounts of information in a very small form factor.

It reduce the mental overhead of "too much information, not my cup of tea". Plus, a table looks prettier than a dense paragraph.

That's why if there is a possibility to explain something using a table, I am always up for that and it is very much reflected in my notes.

* [Doug Lea's memory model](https://ankuragrawal.gitbook.io/home/all-roads-to-memory/dynamic-memory-allocation/doug-leas-memory-model)
* [Types of bins](https://ankuragrawal.gitbook.io/home/all-roads-to-memory/dynamic-memory-allocation/chunk-management#types-of-bins)
