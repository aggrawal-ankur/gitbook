# Step 2: Analyzing Program Headers Table

## Introduction To Program Headers

Program headers are a set of structures in an ELF file that describe how to create a process image in memory. These are used by the runtime dynamic linker/loader program (or, the interpreter program).

## Setup

```
Program Headers:
  Type           Offset              VirtAddr            PhysAddr             FileSiz              MemSiz              Flags  Align
  PHDR           0x0000000000000040  0x0000000000000040  0x0000000000000040   0x0000000000000310   0x0000000000000310  R      0x8
  INTERP         0x0000000000000394  0x0000000000000394  0x0000000000000394   0x000000000000001c   0x000000000000001c  R      0x1
              └─ [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
  LOAD           0x0000000000000000  0x0000000000000000  0x0000000000000000   0x0000000000000628   0x0000000000000628  R      0x1000
  LOAD           0x0000000000001000  0x0000000000001000  0x0000000000001000   0x000000000000015d   0x000000000000015d  R E    0x1000
  LOAD           0x0000000000002000  0x0000000000002000  0x0000000000002000   0x000000000000010c   0x000000000000010c  R      0x1000
  LOAD           0x0000000000002dd0  0x0000000000003dd0  0x0000000000003dd0   0x0000000000000248   0x0000000000000250  RW     0x1000
  DYNAMIC        0x0000000000002de0  0x0000000000003de0  0x0000000000003de0   0x00000000000001e0   0x00000000000001e0  RW     0x8
  NOTE           0x0000000000000350  0x0000000000000350  0x0000000000000350   0x0000000000000020   0x0000000000000020  R      0x8
  NOTE           0x0000000000000370  0x0000000000000370  0x0000000000000370   0x0000000000000024   0x0000000000000024  R      0x4
  NOTE           0x00000000000020ec  0x00000000000020ec  0x00000000000020ec   0x0000000000000020   0x0000000000000020  R      0x4
  GNU_PROPERTY   0x0000000000000350  0x0000000000000350  0x0000000000000350   0x0000000000000020   0x0000000000000020  R      0x8
  GNU_EH_FRAME   0x0000000000002014  0x0000000000002014  0x0000000000002014   0x000000000000002c   0x000000000000002c  R      0x4
  GNU_STACK      0x0000000000000000  0x0000000000000000  0x0000000000000000   0x0000000000000000   0x0000000000000000  RW     0x10
  GNU_RELRO      0x0000000000002dd0  0x0000000000003dd0  0x0000000000003dd0   0x0000000000000230   0x0000000000000230  R      0x1

 Section to Segment mapping:
  Segment Sections...
   00     
   01    .interp 
   02    .note.gnu.property .note.gnu.build-id .interp .gnu.hash .dynsym .dynstr .gnu.version .gnu.version_r .rela.dyn .rela.plt 
   03    .init .plt .plt.got .text .fini 
   04    .rodata .eh_frame_hdr .eh_frame .note.ABI-tag 
   05    .init_array .fini_array .dynamic .got .got.plt .data .bss 
   06    .dynamic 
   07    .note.gnu.property 
   08    .note.gnu.build-id 
   09    .note.ABI-tag 
   10    .note.gnu.property 
   11    .eh_frame_hdr 
   12
   13    .init_array .fini_array .dynamic .got
```

## Understanding The Attributes

Each program header maps to a segment. `Type` refers to the type of that segment.

* `PHDR`: Program header table
* `LOAD`: Loadable segment
* `DYNAMIC`: Dynamic linking info, where is the dynamic section in the binary
* `INTERP`: Path to dynamic linker
* `NOTE`: Auxiliary information (e.g., build ID, security notes)
* `GNU_STACK`: Stack permissions
* `GNU_RELRO`: Read-only after relocation
* `GNU_EH_FRAME`: Exception handling info

`Offset` is the location of this segment within the ELF binary.

`VirtualAddr` is the virtual memory address where the segment should be mapped in memory during execution.

`PhysAddr` is usually ignored by modern OS. Same as `VirtAddr` or meaningless.

`FileSize` is the size of the segment in the binary.

`MemSize` is the size of the segment in memory after loading.

`Flags` refer to memory access permissions.

* `R`: Readable
* `W`: Writable
* `E`: Executable

`Align` refers to the required alignment for the segment in memory and in the file.

## How Program Headers Are Read?

So far, the kernel has verified that the ELF has necessary information required to be executed.

Now the kernel is at the program headers table.&#x20;

### Setup Virtual Address Space (Process Image)

It is looking for all the entries of type `LOAD`, so that it can map those segments into the virtual address space.

Each entry in the program headers table map exactly in the same order with the entries inside the **section to segment mapping**.

The `LOAD` segments are at indices 2, 3, 4 and 5. The segments corresponding to them are these:

```
02    .note.gnu.property .note.gnu.build-id .interp .gnu.hash .dynsym .dynstr .gnu.version .gnu.version_r .rela.dyn .rela.plt 
03    .init .plt .plt.got .text .fini 
04    .rodata .eh_frame_hdr .eh_frame .note.ABI-tag 
05    .init_array .fini_array .dynamic .got .got.plt .data .bss 
```

***

Is there any logic behind such segmentation of sections? Yes. If we have a look at the section headers table, we can find that:

* section 1-10 have the same flags, `A` except the 10th one, which had `I` as well. And they are made in one segment. These include read-only metadata.
* section 11-15 are all `AX`, which are allocated and executable,
* section 16-19 are all with `A` flag. These include read-only data, and
* section 20-26 are with `WX` flags. These include writable and allocated data.

Every segment is carefully containing sections with same permissions. Also, each segment is page-aligned (typically 4 KB) to simplify mapping and protect boundaries.

***

### "Is any dynamic interpreter required?"

After loading all the `LOAD` segments, the kernel looks if there is a requirement for a dynamic linker program. Since our binary is linked dynamically, it contains an `INTERP` entry.

This `INTERP` segment points to the **path of the interpreter**, which is stored as a string in the `.interp` section of the ELF file. The kernel reads the interpreter path from there, locates the dynamic linker program on the disk and loads it as a separate ELF, repeating the entire ELF loading process for it.

After the interpreter (dynamic linker) is loaded, the kernel sets up the process stack and transfers control to the dynamic linker's entry point, not the main program.

* The process stack setup includes argv, envp, and auxv (auxiliary vectors with ELF info).
* We need not to worry about it.

Now the kernel gives control to the entry point of the dynamic linker (or the interpreter) program.

***

### Introducing The Interpreter

First of all, the **interpreter program** and the **dynamic linker/loader** are the same thing. And we use it interchangeably. _So, don't get confused_.

The name of this program is `ld-linux`.

Anyways, the interpreter looks for the dynamic section within the program headers table of our binary. Since the binary is already mapped into the memory, all the access is via the virtual address space. So, the interpreter goes to `0x3de0` address in the virtual address space of our binary to find the `dynamic` section.

Here comes the crazy part. Now sit tight and read carefully, otherwise you might end up glossing over something and it will not settle properly.

* Our binary and the interpreter program, both share the same virtual address space.
* Although the interpreter program is loaded as a separate ELF and it undergoes everything separately, it is not a separate process.
* Although the `execve` syscall starts by loading our binary, but when the kernel finds out that it requires an interpreter, it shifts to loading the interpreter instead.
* And by that time, the loadable segments are already mapped out in the virtual address space.
* So, everything that is required is practically loaded already. And the interpreter just have to act on it.

### What does the interpreter program do?

Now the interpreter went on the `0x3de0` location within the virtual address space and found the dynamic section there.













