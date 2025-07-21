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

## Setup

Lazy binding is not something that is mandatory. It is preferred.

This means, we can tell the compiler to use eager binding for all kinds of symbols.

And we are going to tell the compiler to do this.

```c
gcc ./hello.c -o elf_bin -Wl,-z,now -fno-plt
```

You may ask why we are doing this? How can we learn lazy binding from this?

* I am not going to dodge this question as this shows the pain that I went through to understand relocation and the most important part, to find a way to introduce it in an article.
* We know that after the runtime address of a symbol is resolved, it is put into global offset table. We don't know what it is but it exist.
* There are various reasons for the existence of the global offset table, but those reasons aren't compelling enough to form a case for eager binding.
* I may have told you the reasons directly but that takes the fun out of understanding. **The joy of finding it out** would die, and it would become non-interesting.
* Global offset table becomes inevitable when it comes to functions requiring lazy binding. The tradeoff become more comprehensible and sensible. But to understand lazy binding, we need to understand global offset table and procedure linkage table, which makes no sense to me for eager binding.
* _**By the way, this is my perspective only!**_

The only way I found that can create a compelling case for the existence of global offset table is by this method. By deliberately using eager binding, I hope I can create a compelling problem statement for the existence of GOT.

We need not to know anything about the options used in the command above. Just know that this would generate a binary which would not use lazy binding.

That's enough. Lets move to the problem statement.

## Problem Statement

We can use `readelf` to generate the elf headers for this newly created binary.

```bash
readelf ./elf -a
```

Complete headers can be found at [GitHub](https://github.com/hi-anki/reverse-engineering/blob/main/program1/assets/complete_elf_headers_2nd_elf).

We only need to focus on the relocation entries. Rest is almost the same.

```
Relocation section '.rela.dyn' at offset 0x550 contains 9 entries:
  Offset          Info           Type           Sym. Value    Sym. Name + Addend
000000003de8  000000000008 R_X86_64_RELATIVE                    1120
000000003df0  000000000008 R_X86_64_RELATIVE                    10e0
000000004008  000000000008 R_X86_64_RELATIVE                    4008
000000003fd0  000100000006 R_X86_64_GLOB_DAT 0000000000000000 __libc_start_main@GLIBC_2.34 + 0
000000003fd8  000200000006 R_X86_64_GLOB_DAT 0000000000000000 _ITM_deregisterTM[...] + 0
000000003fe0  000300000006 R_X86_64_GLOB_DAT 0000000000000000 puts@GLIBC_2.2.5 + 0
000000003fe8  000400000006 R_X86_64_GLOB_DAT 0000000000000000 __gmon_start__ + 0
000000003ff0  000500000006 R_X86_64_GLOB_DAT 0000000000000000 _ITM_registerTMCl[...] + 0
000000003ff8  000600000006 R_X86_64_GLOB_DAT 0000000000000000 __cxa_finalize@GLIBC_2.2.5 + 0
```

We can find `puts` on row 6. Since we already have relocated `R_X86_64_GLOB_DAT` entries, we will not talk about how `puts` would be relocated.

Tell me, how a relocation entry is read?

* _Replace the runtime address of the symbol with placeholder address at the offset in the corresponding LOAD segment._

When we are talking about **replacing** aren't we talking about updating something preexisting?

* Isn't **update** categorized by **writing**?

To write something, we must have such permissions. Isn't it?

How do we know if we have the necessary permissions?

* The offset value here is `3fe0`.
* `3fe0` corresponds to&#x20;



















***
