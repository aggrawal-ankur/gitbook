# After Relocation

After `.rela.dyn` entries are processed, the interpreter looks at the PLT entries. Since lazy binding is enabled by default, relocations for `.rela.plt` are deferred.

The interpreter sets up the PLT stubs to point to the dynamic resolver (`_dl_runtime_resolve`) via the GOT, skips JMPREL and leaves the rest of the got entries unresolved.

`.init_array` is a section used to store pointers to initialization functions (constructors) that run before `main()`. It's mostly relevant in C++ or programs with global constructors. For simple C programs like `hello world`, it's typically unused or trivial, and doesn't affect understanding of relocations, GOT/PLT, or dynamic linking — so it's safe to skip for now.

Calls the `INIT` function (from `INIT` dynamic tag), if present.

Then **transfers control to the program's entry point** (usually `_start`).
