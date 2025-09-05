# Orientation

## The Rules The Make Assembly Slightly Easier

Assembly is not a high-level language, therefore, the usual mental models of learning a programming language will not help. Below are a few rules that I have learned throughout this journey.

1. C is not spared of abstractions. Its abstractions are revealed when you look at assembly.
2. Context and Interpretation are paramount while managing data in memory.
3. Assembly is bare-metal. It knows no bounds. At one moment, your program might run perfectly. And the next moment, it might run into an issue.
4. The most straightforward way to improve your understanding of assembly is by doing. You do, you fail, you understand, you don't repeat. That's it.
5. Your code is just one step away from "undefined behavior" territory.
   1. Sometimes, swapping two lines and bringing them at their original position changes the result. And I am not joking.
   2. Just writing a character and then backspacing it changes the outcome. And I am not joking.
6. Progressive learning is the key. As long as you don't hurry and move progressively, you will live a happy life.
7. Intent is more important than learning every single way of doing something. Understand what you want to achieve, then map how the generated assembly does that.
8. What seems like an overwhelming incomprehensible black magic is just logic and compiler optimizations, where the logic becomes primitive as you go deep into trenches & understand what we are trying to do and the compiler optimizations, which are just decades of work done by intelligent beings to make code efficient stops haunting you because you understand that an **intent can be fulfilled in `n` number of ways**.
