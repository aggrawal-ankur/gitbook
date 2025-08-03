# What's the point of having \`.c\` and \`.h\` files?

## Why?

`.c` files a re source files and `.h` files are header files.

The idea is to keep declarations and definitions separate. Why? For a variety of reasons.

1. **Cleanliness and Directness**. When something is used by multiple files, it is better to keep it in one file and reference that file instead of duplicating it, **reducing chaos and redundancy**.
2. **Modular code**. The files which require those definitions just have to include the header file, avoiding the need to include the complete source file.
3. **Compiler efficiency**. The most important one.

We know that when multiple files are passed to `gcc` , it generates object files for each source file and the `linker` program joins them together to form the final binary.

If the source file changes in the future, that's where this system shines.

* If the other files have included the declaration file only, they are not required to be recompiled. Only the corresponding source file needs recompilation. This leads to compiler efficiency.
* If the other files have included the source (full definition) itself, every other such file needs to be recompiled before linking.

You may ask why including header files doesn't demand full recompilation but including source files does. And the answer to this question lies in the build process.

* `include` preprocessing directive copies the file as it is, in the file it is called.
* Header files themselves don't generate any object code. They are an interface to how we access `glibc`, the standard C library, which is one-file that becomes `libc.so` .
* All these different header files are used to categorize the declarations used for different purposes. And they are expanded into the source file. The linker joins the object files with the shared object library and we are done.

Have a look at the `/build-steps` directory.

* If you open the `elfdump-mappings.i` file, along with `dump_structure/mappings.c` and `dump_structure/mappings.h`, you will find that it includes both of these files along with the the declarations from the `inttypes.h` file. Line 296 on wards.
* And these extended files are then compiled to object codes.

## Conclusion

Its a simple way to reduce redundancy and organize the code. That's it.
