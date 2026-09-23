# LucasLehmerRiesel test

In mathematics, the Lucas–Lehmer–Riesel test is a primality test for numbers of the form N = k ⋅ 2ⁿ − 1 with odd k < 2ⁿ. The test was developed by Hans Riesel and it is based on the Lucas–Lehmer primality test. It is the fastest deterministic algorithm known for numbers of that form. For numbers of the form N = k ⋅ 2ⁿ + 1 (Proth numbers), either application of Proth's theorem (a Las Vegas algorithm) or one of the deterministic proofs described in Brillhart–Lehmer–Selfridge 1975 (see Pocklington primality test) are used.

== History ==

The original algorithm was developed by Édouard Lucas.
Derrick Henry Lehmer improved the original algorithm.
Hans Riesel further improved the algorithm to apply it to more numbers.
Riesel and Rodseth have demonstrated this method.

The algorithm is very similar to the Lucas–Lehmer test, but with a variable starting point depending on the value of k.
If the value of k is even, divide k by 2 repeatedly until k becomes odd.
For a prime number n, the values are Mersenne numbers.
Define a sequence ui for all i > 0 by:
u_i = u_{i-1}^2-2. \,
Then N = k ⋅ 2ⁿ − 1, with k < 2ⁿ is prime if and only if it divides uₙ−₂.
Otherwise, if the condition is not met, N is a composite number.

The starting value u₀ is determined as follows.
If k ≡ 1 or 5 (mod 6): if 1 (mod 6) and n is even, or 5 (mod 6) and n is odd, then 3 divides N, and there is no need to test.
Otherwise, N ≡ 7 (mod 24) and the Lucas V(4,1) sequence may be used: we take u_0 = (2+\sqrt{3})^k+(2-\sqrt{3})^k, which is the kth term of that sequence.
This is a generalization of the ordinary Lucas–Lehmer test, and reduces to it when k = 1.
Otherwise, we are in the case where k is a multiple of 3, and it is more difficult to select the right value of u₀. It is known that if k = 3 and n ≡ 0 or 3 (mod 4), we can take u₀ = 5778.

An alternative method for finding the starting value u₀ is given in Rödseth 1994.
The selection method is much easier than that used by Riesel for the 3 divides k case.
First find a P value that satisfies the following equalities of Jacobi symbols:

\left(\frac{P-2}{N}\right)=1 \quad\text{and}\quad \left(\frac{P+2}{N}\right)=-1.

In practice, only a few P values need be checked before one is found (5, 8, 9, or 11 work in about 85% of trials).

To find the starting value u₀ from the P value we can use a Lucas(P,1) sequence, as shown in as well as page 124 of.
The latter explains that when 3 ∤ k, P=4 may be used as above, and no further search is necessary.

The starting value u₀ will be the Lucas sequence term Vₖ(P,1) taken mod N. This process of selection takes very little time compared to the main test.

== General Lucas Sequence Definitions ==

Lucas sequences are used to find the initial value from the value of n.
A Lucas sequence is defined with an initial value V_0 equal to 2 and an initial value V_1 equal to P.
The recurrence relation for the sequence is V_k = P * V_{k-1} - Q * V_{k-2}, where the value of Q used in the calculation is 1.
The value of s₀ is equal to Vₖ, and the value of P that satisfies the condition is 8.
The value of v_n is 2 when n equals 0, the value of v_n is 4 when n equals 1, and for n greater than or equal to 2, the value of v_n is calculated as 4 times v_{n-1} minus v_{n-2}.

== Starting Values for k = 1 ==

When k equals 1, s₀ equals 4 and 4 is a good starting value for odd n.
If k equals 1 and n is prime, then u_0 can be taken as 4, and if n is odd, the value u_0 is set to 4.
If n is congruent to 3 modulo 4, then u_0 can be taken as 3, and if k equals 1 and n is congruent to 3 modulo 4, s₀ can be set to 3.
The case being discussed is k = 1, the case considers n being odd, and the condition applies when k equals 1.
The condition applies when 3 does not divide N, and u_0 equals 3.

== Efficient Calculation Formulas ==

Two efficient formulas are commonly used to calculate the value of V_k.
The value of V at index 2i is equal to the square of the value of V at index i, and the value of V_{2i+1} is equal to the product of V_i and V_{i+1} minus P.
The value k must be converted into binary form.
Therefore, Vi must be calculated simultaneously with Vi+1 in all processes.

== Binary Exponentiation Algorithm ==

In this example, k equals 9 and converts to 1001 in binary.
If the leading bit is 0, the first formula is used for Vi, but the first formula is not used for Vi+1.
If the bit is 1, the second formula is used, and when using the second formula, only Vi is calculated while Vi+1 is left unchanged.
The process should be repeated for all bits, and before repeating the process, the leading bit should be removed.

== Step-by-Step Example for k = 9 ==

The initial value V_0 is 2, and V_1 must be calculated in this process as P, which equals 8.
V_2 is calculated as V_1 squared minus 2, resulting in a value of 62, which is equal to V_{2*1}.
The initial bit sequence is 001, where the first bit is 0, so the first formula is used.
V_3 is equal to V_1 multiplied by V_2 minus 8, yielding a value of 488.
The leading zero is removed to leave the binary sequence 01, where the first bit is 0, so the first formula is used again.
V_4 is equal to V_{2*2}, calculated as V_2 squared minus 2, which equals 3842.
The value 3842 is congruent to 1539 modulo 2303.

V_{4+1} equals V_5, which equals V_2 multiplied by V_3 minus 8, a value that equals 30248 and is congruent to 309 modulo 2303.
The first bit of the number 1 is 1, so the second formula is used.
V_9 is equal to V_4 multiplied by V_5 minus 8, and the result of this calculation is congruent to 1133 modulo 2303.
The leading 1 is removed.
The initial value s_0 is equal to V_k, where V_k is equal to V_9, which is congruent to 1133 modulo 2303.
The parentheses denote the Jacobi symbol.

The Lucas–Lehmer–Riesel test is a particular case of group-order primality testing; we demonstrate that some number is prime by showing that some group has the order that it would have were that number prime, and we do this by finding an element of that group of precisely the right order.

For Lucas-style tests on a number N, we work in the multiplicative group of a quadratic extension of the integers modulo N; if N is prime, the order of this multiplicative group is N² − 1, it has a subgroup of order N + 1, and we try to find a generator for that subgroup.

We start off by trying to find a non-iterative expression for the u_i. Following the model of the Lucas–Lehmer test, put u_i = a^{2^i} + a^{-2^i}, and by induction we have u_i = u_{i-1}^2 - 2.

So we can consider ourselves as looking at the 2ⁱth term of the sequence v(i) = a^i + a^{-i}. If a satisfies a quadratic equation, this is a Lucas sequence, and has an expression of the form v(i) = \alpha v(i-1) + \beta v(i-2). Really, we're looking at the k ⋅ 2ⁱth term of a different sequence, but since decimations (take every kth term starting with the zeroth) of a Lucas sequence are themselves Lucas sequences, we can deal with the factor k by picking a different starting point.

== Special cases and examples ==

If k equals 1 and n is prime, then we are facing a Mersenne number.
When k equals 3, if n is congruent to 1 modulo 4, then N is congruent to 0 modulo 5.
If N is not equal to 5 under these conditions, N is a composite number.
N is not divisible by 3.
47 is equal to 3 multiplied by 2 to the power of 4 minus 1.
The value of k is 3.
The value of n is 4.
2303 is equal to 9 multiplied by 2 to the power of 8 minus 1.
In this example, there is one additional '1' bit besides the leading '1'.
The additional '1' bit is located at the end of 1001.
2303 is a composite number.
s_8-2 equals s_6.
Dividing 2303 by the result of s_8-2 (which is s_6) leaves a remainder that is not zero.
The remainder when dividing 2303 by s_6 is 692.
2303 can be factored into 7 squared multiplied by 47.

== Applications ==

The primality test is mainly used when the number to be tested has more than 10 million digits.
In such cases, the efficiency of this primality test greatly surpasses that of other primality tests.

LLR is a program that can run the LLR tests.
The program was developed by Jean Penné.
Vincent Penné has modified the program so that it can obtain tests via the Internet.
The software is both used by individual prime searchers and some distributed computing projects including Riesel Sieve and PrimeGrid.
A revised version, LLR2 was deployed in 2020.
This generates a "proof of work" certificate which allows the computation to be verified without needing a full double-check.
A further update, PRST uses an alternate certificate scheme which takes longer to verify but is faster to generate for some forms of prime.
The software is Jean Penné's LLR Math::Prime::Util::GMP.
The software is part of the Perl ntheory module.
The software includes a basic implementation of LLR.
The software implements a test similar to the Brillhart–Lehmer–Selfridge test for Proth numbers.
The project stopped in 2010.
The module is written in Perl.
The module provides a basic implementation of the LLR test.
The module provides a basic implementation of the Proth test.
The module includes some methods from the Brillhart, Lehmer, and Selfridge article.

Riesel number
