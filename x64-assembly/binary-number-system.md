---
layout:
  width: default
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
---

# Binary Number System

## Number System Refresher

Primarily we have 4 number systems. They are: binary, octal, decimal and hexadecimal.

Normally we use the decimal number system.

<table><thead><tr><th width="136">Property</th><th width="129">Binary System</th><th width="143">Octal System</th><th>Decimal System</th><th>Hexadecimal System</th></tr></thead><tbody><tr><td>Base</td><td>2 (<code>2^1</code>)</td><td>8 (<code>2^3</code>)</td><td>10</td><td>16 (<code>2^4</code>)</td></tr><tr><td>Allowed Digits</td><td>0, 1 <br>(called bits)</td><td>0, 1, 2, 3, 4, 5, 6, 7</td><td>0, 1, 2, 3, 4, 5, 6, 7, 8 9</td><td>0, 1, 2, 3, 4, 5, 6, 7, 8 9, A, B, C, D, E, F</td></tr><tr><td>Bits Required To Represent (derived from base)</td><td>1</td><td>3</td><td></td><td>4</td></tr><tr><td>Prefix</td><td>0b</td><td>0o</td><td>0d</td><td>0x</td></tr><tr><td>Example (11)</td><td>0b00001011</td><td>13</td><td>11</td><td>0xb</td></tr></tbody></table>

1 Byte = 8 Bits

Now it's time to dive into binary number system.

## Revision

Everyone learns number lines in elementary school.

* _A pictorial representation of numbers on a straight line._

That number line has a zero which separates negative numbers from positive numbers.

A whole number (-infinity to +infinity) with no fractional part is called an integer. A whole number with fractional part is a decimal.

***

In computer science, these numbers are called differently.

* Positive Integers -> Unsigned Integers
* Positive & Negative Integers together -> Signed Integers

Sadly, there is no name for negative integers in computer science.

Fractions are popularly known as **floating point integers**.

***

## Binary To Decimal System

Before we dive any further, it is important to understand how bits relate with decimals.





CONTINUE FROM HERE



***

In binary number system, there are 3 category of numbers that we have to understand.

1. Unsigned integers
2. Signed integers
3. Floating point values

### Unsigned Integers

All the positive integers are unsigned integers, and that includes 0 as well.

They start from 0 and go up to the maximum possible value based on the number of bits.

How bits relate to decimals is necessary

For instance:

* 1 byte is composed of 8-bits.

To obtain the unsigned range for n-bits, `[0, 2^n - 1]`

A 8-bit number can range from 0 to 255. Their representation is as follows:

```
0 => 0b00000000
255 => 0b11111111
```

### Signed Integers

Signed integers can be both positive and negative.

They are implemented using two's complement.

The most significant bit (MSB) is used as the sign bit:

* 0 = positive
* 1 = negative

A 8-bit number can range from -128 to +127. Their representation is as follows:

```
0 => 0b00000000
+127 => 0b01111111
-128 => 0b10000000
-1 => 0b11111111
```

### The standard rule to find the signed range of possible integers in n-bits is: `[(-2)^(n-1), 2^(n-1)-1]`

## Representing Negative Integers

In binary number system, + and - holds no meaning. Complements are how we represent negative numbers in binary system.

Complements mathematical transformations of binary numbers, specifically designed for how binary arithmetic works in computers

The most common ones are:

1. 1's Complement
2. 2's Complement

***

### Types Of Bits

Primarily, there are two types of bits.

1. Least Significant Bit (LSB) : It is the rightmost bit in the binary representation of the integer.
   * It is called least because setting this ON or OFF has the least impact on the magnitude of the value.
   * Ex: 15 is represented by 1111 in 4-bits. If you set the last bit (or LSB) to 0, we get 1110, which is 14. The magnitude is lowered by 1 only.
2. Most Significant Bit (MSB) : It is the leftmost bit in the binary representation of the integer.
   * It is called most because setting this ON or OFF has the largest possible impact on the magnitude of the value.
   * Ex: Take 15 again. If you set the leftmost bit (or MSB) to 0, we get 0111, which is 7. The magnitude is lowered by 8.

### 1's Complement

The value you must add to a number so the result is a string of 1s or the result is the maximum representable value.

To get the 1's complement of a binary number: Flip all bits (change 0s to 1s and 1s to 0s).

Example:

* 5 in binary is represented by: `0b00000101`
* 1's complement of 5 (= -5): `0b11111010`

The problem with 1's complement is that it has two representation of 0.

* +0 = `0b00000000`
* -0 = `0b11111111`

But 0 is one digit. + and - are insignificant for it.

### 2's Complement

Two's complement takes a different approach to manage -ve integers, which ensures that there is no opportunity for 2 representations of zero to exist.

In 2's complement, the number of possible combinations are divided into two halves.

The lower halve represents +ve integers while the upper halve represents -ve integers. The word "represents" is especially important here because at the end of the day, these are just pair of bits. They don't represent anything. We ourselves assign meaning to them.

So, to get the 2's complement of a number:

1. Start with the binary representation of the +ve number.
2. Get 1's complement.
3. Add 1 (0001) to the result.

Example:

* 5 in binary is represented by: `0b00000101`
* 1's complement of 5: `0b11111010`
* Add 1: `0b11111010` + `0b00000001` = `0b11111011`
* We get -5 in 2's complement as `0b11111011`
* (+5) + (-5) = `0b00000101` - `0b11111011` = `0b00000000`, Hence proved!

#### But how does this solves the problem?

Lets take an example using 4-bits, because combinations here are not too less, not too more.

* By default, 4-bits are meant to represent a total of 16 combinations of bits. Meaning, 16 integers in total, or better, **16 unsigned integers**.
* Total possible combinations = 2^n = 2^4 = 16, where n is the number of bits.
* These combinations are: 0000, 0001, 0010, 0011, 0100, 0101, 0110, 0111, 1000, 1001, 1010, 1011, 1100, 1101, 1110, 1111
* Now 2's complement divides these into two halves. Therefore, both of them will get 8-8 values.
* The lower halve or the left portion will represent +ve integers while the upper halve or right portion will represent -ve integers.
* Visually, \[0000, 0001, 0010, 0011, 0100, 0101, 0110, 0111] will represent +ve integers and \[1000, 1001, 1010, 1011, 1100, 1101, 1110, 1111] will represent equivalent -ve integers.
* The question is how! Let's look at that.
* By using the formula mentioned above, we get the possible integers in a 4-bit setting. \[(-2)^(4-1), 2^(4-1)-1] = \[(-2)^3, (2^3)-1] = \[-8, +7]
* Now mathematically, we know that the possible +ve integers in a 4-bit setting are \[0, 7] while the set of -ve integers is \[-8, -1]. Both contains 8 combinations in total.
* And clearly, there seems to have no place for two representations of 0.
* But how the upper halve will get mapped to the lower halve? Let's see.
* If you notice the upper halve, you'll find that all the combinations have the most significant bit (MSB) set to 1. And its obvious. To obtains integers from 8-15, you need the 4th bit, or the MSB here, to be 1.
* But this is not true with the lower halve. Lower halve has MSB set to 0 for all combinations.
* And this forms the distinction.
* In 2's complement, all the +ve integers have their "**MOST SIGNIFICANT BIT (MSB)**", set to 0. And the -ve integers have this bit set to 1.
*   To map them, take out the upper halve, and put it in the left of the lower halve. We'll get something like this:

    1000, 1001, 1010, 1011, 1100, 1101, 1110, 1111, 0000, 0001, 0010, 0011, 0100, 0101, 0110, 0111

    -8 -7 -6 -5 -4 -3 -2 -1 0 +1 +2 +3 +4 +5 +6 +7
* To obtain the -ve representations of 0, we need all the bits to be 0 while the MSB set to 1, right? This brings us to 1000. But this is -8.
* But this is just visually, isn't it? What about proving it mathemtically? Also, if there is -8, where is +8? Great, let's do that.
  * If you see the grid above, you can note that every -ve equivalent is of the form `-(2^n) + (+ve integer)`
  * Ex: -8 => -(2^4) + (+8) = -16 + 8 = -8 (1000)
  * Ex: -1 => -(2^4) + (+1) = -16 + 1 = -15 (1111)
  * lets do this for 0:
    * -0 => -(2^4) + (+0) = -16 + 0 = -16
    * But 16 as a combination is not possible using 4-bits.
    * I think, this is enough to prove that 2's complement by design has got no room for two representations of zero. And it is more accurate mathematically as well.

## Binary Arithmetic

### Unsigned Arithmetic

Just like normal addition, except that carrying and borrowing rules are different.

#### Addition

Carry, once the sum exceeds 1.

Example:

```
  0011 (3)
  1101 (13)
= 10000 (16)
We have to add a new bit because the result exceeded the bit-limit.

  0011 (3)
  0110 (6)
= 1001 (9)
```

#### Subtraction

We know that `10 - 8 = 2`. And we can do the same for any operands. But the problem is, this process has become so automatic that we know it subconsciously but we have forget it consciously.

To understand binary subtraction, we have to revisit how subtraction actually work.

All of use are using decimal number system since elementary school. And we know that every digit in a number has a _**position**_ attached to it.

For example: 49521

* Moving from right to left,
* 1 is the ones digit,
* 2 is the tens digit,
* 5 is the hundreds digit,
* 9 is the thousands digit, and
* 4 is the ten-thousands digit.

These positions aren't NPCs, they have a purpose.

We also know that decimal system is a base-10 system. But what does that actually mean?

Every position has a _**weight**_ attached to it. _**Weights**_ are indices raised to the power of base.

_**Indices**_ refers to a numerical identity, given to a position. These **indices** start from 0 and go till (number of digits - 1).

* The ones position carries a weight of 10^0 = 1.
* The tens position carries a weight of 10^1 = 10
* The hundreds position carries a weight of 10^2 = 10
* The thousands position carries a weight of 10^3 = 10000
* The ten-thousands position carries a weight of 10^4 = 10000

In division, we use the terms dividend and divisor, which, in simple terms, dissolve to numerator and denominator, respectively. In subtraction, we have _**minuend**_ and _**subtrahend**_. I can't remember if I have heard these words before. I also read them first when I had this task. Anyways.

To keep things simple, if we have `op1 - op2` operation, op1 is the _**minuend**_ while op2 is the _**subtrahend**_.

There are multiple techniques to do subtraction.

* In school, we have learned _**column-based subtraction**_, which involves borrwoing from the left digits.
* We can add equal numbers to both the minuend and subtrahend and make the subtrahend end with zero. Visually, it realives a lot of strain.
* Subtraction by complement. A quite easy way to do subtraction. Computers use 2's complement.
* Most simplest way, counting.
* One way that I like and find myself using quite often is decomposition, where we break numbers in pairs of 10s. Like 4215 can be broken into 4200 + 15. 2307 can be broken into 2300 + 7. 4200 - 2300 is simple, 1900. So as 15 - 7, 8. Add at last, 1900 + 8, result = 1908.
* And yes, I didn't forget calculator!

When doing column-based subtraction, we subtract digits at corresponding positions in minuend and subtrahend. For example: 4215 and 2307. The digit at ones position (7) will be subtracted from the digit at ones position (5) only.

Sometimes, we get stuck when the corresponding minuend is lesser than the subtrahend. In that case, we _**borrow**_ from the left side. That's where things get intersting.

When we do `10 - 4`, borrowing is inevitable here.

We are taught that when we borrow, reduce the one from the lender and add 10 to the borrower. 0 borrowing from 1 and it becomes 10. Now it can subtract. Similariy, in `20 - 4`, we just need 10, not the entire 20, but it is 20. Upon looking closely, 20 is just 10+10. Problem solved. Take out one 10 and give it to 0.

But why 10 only? Why not 5? The answer is weight.

* Treat positions like containers, where every container has a limit on how much it can accomodate.
* The ones position has a weight 10^0 or 1. It can't accomodate more than that. And 1 here represents the base value, which is 10.
* That is why we have never borrowed more than 10.

I think that all we need to remember about subtraction.

Lets tackle binary subtraction now.......

There are 4 rules, 3 of them are simple and straightforward. And one is the rebel.

* `0 - 0 = 0`
* `1 - 1 = 0`
* `1 - 0 = 1`
* `0 - 1 = 1`, this is where the problem is.

Take this:

```
_ 0110 (6)
  0100 (4)
= 0010 (2)
```

> Simple.

And these?

```
_ 0100 (4)
  0001 (1)
= 0011


_ 1010 (10)
  0011 (3)
= 0111
```

If you are questioning _what and how_, then we are on the same page. I have also wasted hours figuring out the same.

Anyone who has spend time with binary knows about "8 4 2 1". Some might know it by name, others use it as is. I fall in the others category. My search brought me to this YouTube video: [Binary Addition and Subtraction Explained (with Examples)](https://www.youtube.com/watch?v=AE-27BSbkJ4\&t=629s\&pp=ygUSYmluYXJ5IHN1YnRyYWN0aW9u). And the first time, I got introduced to the term weights.

Therefore, 8 4 2 1 are basically weights in binary number system.

General Formula: `Weight For Position i = (base)^i`

Lets look at the minuend, 1010. The weights attached to each digit are: \[2^3:1, 2^2:0, 2^1:1, 2^0:0]

To convert binary representation into decimal, we have to multiply the digit with its weight and sum-up the result. For example, 1010. The weights are 8421. We get `8 + 2 = 10`.

From this, we can say that a 1 at 0th bit position represents 2^0? A 1 at position 3 represents 2^3? And a 1 at position _i_ represents _2^i_.A bit at index 3 is basically inside a container which can hold upto "2^3 size in decimals", in binary it is still only about 0 and 1.

I think `10 - 3` is a really complex binary subtraction primarily because of how borrowing works.

To visualise borrowing, lets take a simple example.

```
8 - 3 = 5

_ 1000 (Minuend, 8)
  0011 (Subtrahend, 3)

= ____
```

Subtraction process starts the same, from right towards left.

Here is a simple table to condense this information.

| Attribute  | Value At Bit | Value At Bit | Value At Bit | Value At Bit |
| ---------- | ------------ | ------------ | ------------ | ------------ |
| Index      | 3            | 2            | 1            | 0            |
| Weight     | 2^3 = 8      | 2^2 = 4      | 2^1 = 2      | 2^0 = 1      |
| Minuend    | 1            | 0            | 0            | 0            |
| Subtrahend | 0            | 0            | 1            | 1            |

Now lets understand _**borrowing**_.

* bit-0 subtraction needs borrowing. It goes to bit-1.
* bit-1 also needs borrowing. It goes to bit-2.
* bit-2 also needs borrowing. It goes to bit-3.
* bit-3 is 1, so it can lend. The weight attached to bit 3 is 8.
* bit-2 has come to ask for lending from bit-3. But the maximum that bit-2 can contain is 2^2. But bit-3 can lend 2^3 only. Because in binary, either you have 0 or you have 1.
* So bit-3 breaks itself as 4+4, which is same as 2 units of 2^2. And notice, 2^2 is exactly what bit-2 can hold at max. But there are two units. Lets not go any further and assume it can hold it. Lending successful.
* Status:
  * bit-3 = 0
  * bit-2 = something that 2\*(2^2) might refer to.
* Now bit-2 lends to bit-1. It has got two units of 2^2.
* But again, bit-1 can hold upto 2^1 only. So bit-2 breaks one of its units 2^2 as 2 \* (2^1). And lends it to bit-1. Lending successful.
* Status:
  * bit-3: 0
  * bit-2: something that 2^2 might refer to. One unit is now given to bit-1.
  * bit-1: something that 2\*(2^1) might refer to.
* Now bit-1 lends to bit-0. It has got two units of 2^1.
* But once again, bit-0 can only hold upto 2^0. So bit-1 breaks one of its units 2^1 as 2 \* (2^0), And lends it to bit-0. Lending successful.
* Status:
  * bit-3: 0
  * bit-2: something that 2^2 might refer to.
  * bit-1: something that 2^1 might refer to. One unit is now given to bit-0.
  * bit-0: something that 2\*(2^0) might refer to.

Now, no more lending or borrowing.

What is this "something that \_\_ might refer to"? What do they actually refer to?

* Just look at them, you'll find your answer.
* bit-3 is already zerod, so no confusion.
* bit-2 is 2^2, from the table above, it is exactly the weight it can contain, that means, a 1.
* bit-1 is 2^1, from the table above, it is exactly the weight it can contain, that means, a 1.
* bit-0 is 2 units of 2^0 or better, 2 units of 1.

Now lets do the subtraction.

```
_ 1 0 0 0
  0 0 1 1

can be written as

_ 0 1 1 (1+1)
  0 0 1  1

I don't think its tough anymore.
The answer is 0101, precisely what we needed.

Lets tackle the boss now, which spiraled me to understand subtraction from its roots.

_ 1 0 1 0 (10)
  0 0 1 1 (3)

can be written as

_ 0 1 (1+1) (1+1)
  0 0  1     1

= 0 1 1 1 (7)
```

_**And, we are done!**_

It was damnn confusing and frustrating, but this is the best I can do. I have employed multiple ways to understand the whole system of borrowing and this is the best I can comprehend. Hopefully it helps.

I have used ChatGPT to understand borrowing, but I stuck at the last bit. Then I opened a Youtube video, which introduced to weights. I have used them a lot, but never knew they are such significant. Also they said that borrowing is in terms of base, which is something so important. Subconsciously we do it but never realise it. But still it remain mysterious, I kept wondering the same thing and one new item added to it, why 2!. Then later next day I watched another video and it said two 1's are borrowed, [video](https://www.youtube.com/watch?v=h_fY-zSiMtY). One more mysterious object dropped into my mind. And after that I decided to go into the depths of my mind again and here we are.

I still accept it myself that it might not be the best explanation in terms of how terminologies and analogies are used, but it is from a beginner to a beginner.

In the end, binary subtraction is mysterious because of the fundamentals not being right. Most of the people who says "Your fundamentals have to be extremely strong and grounded" might not even understand the depth of their statement. It can easily turn into a rabbit hole because of our incomplete understanding and things becoming automatic (subconscious).

### Signed Arithmetic

Computers use 2's complement so it is pretty straightforward.

`A - B` becomes `A + (-B)`

We obtain `-B` using 2's complement.

Example:

```
A = 0101 (5)
B = 0011 (3)

5 - 3 = 2

A - B => A + (-B)

-B = 1's complement (B) + 0011
   = 1100 + 0001
   = 1101

A - B = A + (-B)
      = 0101 + 1101
      = 10010 (discard carry)
      = 0010
      = 2
      Hence Proved
```

## Conclusion

It is no black magic, first of all.

Second, signed numbers and floats is where the problem starts.
