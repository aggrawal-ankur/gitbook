# Stripping ELF

## How to strip a binary?

Using `strip` utility.

```bash
$ strip dynamically_linked -o dynamically_linked_strip
$ strip statically_linked  -o statically_linked_strip

$ ls -l *_linked* 
-rwxrwxr-x 1 kali kali  15952 Aug  6 14:18 dynamically_linked
-rwxrwxr-x 1 kali kali  14472 Aug  6 14:18 dynamically_linked_strip
-rwxrwxr-x 1 kali kali 758424 Aug  4 10:27 statically_linked
-rwxrwxr-x 1 kali kali 676288 Aug  6 14:17 statically_linked_strip

$ ls -l *_linked* -h
-rwxrwxr-x 1 kali kali  16K Aug  6 14:18 dynamically_linked
-rwxrwxr-x 1 kali kali  15K Aug  6 14:18 dynamically_linked_strip
-rwxrwxr-x 1 kali kali 741K Aug  4 10:27 statically_linked
-rwxrwxr-x 1 kali kali 661K Aug  6 14:17 statically_linked_strip
```

## What gets stripped?

Lets analyze `readelf` to find that out.

For both the elfs, `.symtab` and `.strtab` are missing in the section headers.

Stripping removes only non-essential symbol information used for debugging and linking, not for execution.

If a section is not referenced by runtime execution and not marked `SHF_ALLOC`, it can be stripped.










