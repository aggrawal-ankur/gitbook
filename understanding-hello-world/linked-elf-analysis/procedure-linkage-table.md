# Procedure Linkage Table

The Procedure Linkage Table is a section in an ELF binary used to support dynamic function calls to external (shared library) functions. It acts as an indirect jump table, allowing a program to call shared library functions whose actual memory addresses are not known until runtime, typically resolved through lazy binding.

## Meaning of PLT

A table of stubs that handle runtime linkage of procedures (functions) in a dynamically linked environment.
