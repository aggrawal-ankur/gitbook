# After Relocation

After `.rela.dyn` entries are processed, the interpreter looks at the PLT entries. Since lazy binding is enabled by default, relocations for `.rela.plt` are deferred.

The interpreter now sets up the PLT stubs to point to the dynamic resolver (`_dl_runtime_resolve`) via the global offset table, skips `JMPREL` and leaves the `.got.plt` entries unresolved.

`.init_array` is a section used to store pointers to initialization functions (constructors) that run before `main()`. It's mostly relevant in C++ or programs with global constructors. For simple C programs like `hello world`, it's typically unused or trivial, and doesn't affect the understanding of relocations, GOT/PLT, or dynamic linking — so it's safe to skip for now.

Now the interpreter program calls the `INIT` function (from `INIT` dynamic tag).

After it is done with `INIT`, it transfers the control to the program's entry point which `_start` .

* `_start` calls \``` __libc_start_main()` `` , which calls `main` .

`main` does its work and return the exit code in the accumulator register. Remember this instruction?&#x20;

```
114c:	b8 00 00 00 00       	mov    eax,0x0
```

The control is given back to the \``` __libc_start_main()` `` function, which receives the exit code and calls the `exit(return_value)` function from `libc`.

`exit()` runs, calls destructors from `.fini-array` and finally, the exit syscall comes in effect to terminate the program.

The kernel receives the control back, does some cleanup and sends `SIGCHLD` to the parent process.



## Conclusion

Ladies and gentlemen, this marks the end of statically analyzing the hello world binary. \~35 days of chaos, but worth it.
