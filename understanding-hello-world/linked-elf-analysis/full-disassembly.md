# Full Disassembly

## Premise

While analyzing the object code, we have checked out full disassembly of the compiled file. We can do it here as well.

```bash
objdump linked_elf -D -M intel
```

Shocked, right! The generated assembly is 800 lines long. The first and the immediate question is **WHERE ALL THIS ASSEMBLY IS COMING FROM?**

## The Big Picture

Our source code is a tiny part of the a bigger picture.

There exist a complete infrastructure that runs this hello world thing. And the compilation and linking process is what that constructs this infrastructure.

The whole **build process** enables a binary to have everything that is required to run the source.

It is all compiler (`gcc`) generated.

### What to do with this disassembly?

This disassembly exposes almost everything, therefore, it is a roadmap for us. But to read that roadmap, we have to understand the things it points to.

There is no meaning in reading it line by line. We will use it in the process to make sense of what we are doing and why we are doing it.

Although I could have avoid it now because we are going to visit it anyway in the end where we would be summarizing how everything fits in the bigger picture, but I thought that if someone visited it earlier, it would mess with their mind. This is the reason why I decided to left an explanation before it consumes that learner.

With that in mind, we can move to step 2.

