# Relocation - Part 2

## Premise

So far, we are done relocating the `.rela.dyn` section, which utilizes eager binding.

* Eager binding involves relocating a symbol right away, before it is even required.

Now we are at the `.rela.plt` section, which utilizes lazy binding.

* Lazy binding involves relocating a symbol only when it is called the first time.

This part has puzzled me the most. It is technically dense and requires knowledge of multiple things. The problem lies in how to introduce them.

* One way is the reckless way to just introduce them and let the reader wonder what is it and why it is.
* The other way is to introduce it thoughtfully, in a way it actually makes sense.
* The second option requires a problem statement before I introduce the concept. But the problem makes more sense when `.rela.plt` section is well understood. But we don't understand it yet.
* And this had me perplexed for more than 3 days. I was just trying to find one compelling case which I can use to weave a story which can create a powerful need for the presence of GOT and PLT.
* Their was a blurry story in my mind but I lacked the starting point, which was blocking me from doing anything.
* This morning, 21/07/25, finally my subconscious suggested me something which can help me out.

Now its time to unpack this.

## What we are going to be studying?

1. Global offset table
2. Procedure linkage table
3. Lazy binding

These are the big names we are going to explore. I thought it is right to establish what we don't know before we go about knowing them.

It is going to be lengthy because it is complex and confusing.

Sit tight and enjoy.

***
