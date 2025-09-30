---
id: 22f99fb0de5843079c208e3ff1d107f7
title: Data Types
weight: 1
---

How the illusion of data types is created?

_**August 18, 2025**_

***

## General Knowledge

C has the following types:

| Class | Types |
| :--- | :--- |
| Primitive | char, int, float, double, void |
| Derived | array, pointer, function |
| User-defined (Complex) | struct, union, enum, typedef |


Note: `void` is only meaningful in functions and pointers.

### How Much Do They Weigh?

Size is architecture specific and we are talking about 64-bit only.

| Data Type | Size |
| :--- | :--- |
| char | 1-byte |
| int | 4-byte |
| float | 4-byte |
| double | 8-byte |
| array | sizeof(data_type) * number_of_blocks |
| pointer | size of the address on an architecture, 8-byte here. |

`char` is generally 1-byte across all architectures and implementations while `int` is implementation depended. Although the common size of `int` is 4-bytes on 64-bit but there is a complete header file called `inttypes.h` which provides so many int.

## How Data Types Are Translated?

A `char` is 1-byte so it aligns perfectly with the idea of **byte-addressable memory**. The problem comes with `int float double` etc.

A single byte can represent 256 combination of numbers.

* Signed: `-128 to +127`
* Unsigned: `0 to 255`

A group of 4 bytes means 32-bits together, which can represent a large sum of values.

If we have to store 6, how it is stored?

* A single byte is more than enough to represent 6. It would be `00000110`.
* What about other 3 bytes? Just zero them and you get a 32-bit wide value for 6. Something like this: `00000000000000000000000000000110` .

***

What does this imply?

This implies that a general `int` requires 32-bits or 4-bytes of space. So, a variable declaration of type `int` would require 4-bytes to be reserved.

* But memory is byte addressable. That means, a continuous block of 4-bytes is required to store an integer. And you have to interpret those 4-byte together in order to interpret them rightly.

Same with float and double.

***

What about arrays?

An array is a buffer in real sense. You have a group of bytes that are distinct enough that they exist as individual units but they are a part of one single entity.

For example, take an array of 10 elements.

* In simple words, it is a group of 10 logical units where each logical unit is a sequence of bytes interpreted as one single entity.
* An array of 10 integers is a contiguous block of memory split into 10 logical units, where each unit is 4 bytes. Each 4-byte unit, when interpreted together as an `int`, they represent a single number.

Therefore, the size of an array is the size of the type of data it contains multiplied by the number of elements.

***

So, what are data types?

* _A data type is a contract between the programmer and the compiler that defines how a sequence of bits in memory should be interpreted and what operations are valid on it._

This is why interpretation is so important. A group of bytes can be represented in a variety of ways and each way changes the meaning. For example:

* 16 bytes can be interpreted as 16 distinct characters, 4 integers or 2 doubles. And these 16/4/2 can exist as distinct variables or a part of an array of the same type.

## Conclusion

This is all about primitive data types.

There are complex data types like enum, structure and union, which we will talk about later.