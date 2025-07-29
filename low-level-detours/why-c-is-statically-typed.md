# Why C Is Statically Typed?

Why we can't just pass the number of bytes we've to read?

The answer is rather simple. C is strictly-typed. It has data types for everything. But the key lies in how those data types are translated at memory level as there exist only raw bytes.

So, how those data types are translated at memory level?

* Lets take an example of storing 42.&#x20;
* The data type is `int`, which takes 4-bytes on 64-bit systems.
* But what is 42 at binary level? `00101010`&#x20;
* What if we prefix it with 24 zeroes, like this: `00000000000000000000000000101010` ? It is still 42, isn't it? What has changed is that this is a 4-byte representation of a decimal value 42 and `00101010` was a 1-byte representation of the decimal value 42.
* Suppose 42 is stored at a memory `0x1000`. We use the move operation to load it in the accumulator, like this: `mov eax, [0x1000]` , intel syntax. What does this instruction really mean?
* It means, go on offset `0x1000`, read 4 consecutive bytes from there, `0x1000, 0x1001, 0x1002, 0x1003` , sort them from little-endian to big-endian, combine them and put them into the accumulator.
* And what is there on these offsets? Since computers prefer little-endian system, the order of bits would be reversed. `0x1000 = 0x2A (42), 0x1001 = 0x00, 0x1002 = 0x00, 0x1003 = 0x00` .

How does this relate with `fread`?

* Interpretation is where the problem is.
* Raw bytes are raw because they can be interpreted as the programmer wants. For a `char` type value, 42 is `*`. For an integer it is `0d42`. In hex system, it is `0x2A`. In octal system, it is `0o52`. Who will account for these interpretations?
* For `char`, `0x1000, 0x1001, 0x1002, 0x1003` are logically distinct locations. For `int32` , `0x1000, 0x1001, 0x1002, 0x1003` is an array of two values (42 and 0). For `int64`, it is one-single value, 42.
* This is why `fread` needs to know which data type we are interpreting (though size of each entry argument) and the number of elements of such data type.
