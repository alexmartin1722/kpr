# Claim proposal — LucasLehmerRiesel test
*100 facts proposed for addition from non-English editions (it, ja, ko, nl, ru); 6 knowledge conflicts.*

## Proposed additions (ABSENT facts, routed to a section)

### Finding the starting value
- If k equals 1 and n is prime, then u_0 can be taken as 4  
  _[it]_ ← "Se k = 1 e n è primo, allora ci troviamo di fronte ad un numero di Mersenne e possiamo prendere u₀ = 4."
- If n is congruent to 3 modulo 4, then u_0 can be taken as 3  
  _[it]_ ← "Se n \equiv 3 \pmod{4}, allora possiamo prendere u_0 = 3."
- The value of v_n is 2 when n equals 0  
  _[ja]_ ← "v_{n} = \begin{cases} 2 & \text{if } n = 0 \\ 4 & \text{if } n = 1 \\ 4v_{n-1} - v_{n-2} & \text{if } n \ge 2 \end{cases}"
- The value of v_n is 4 when n equals 1  
  _[ja]_ ← "v_{n} = \begin{cases} 2 & \text{if } n = 0 \\ 4 & \text{if } n = 1 \\ 4v_{n-1} - v_{n-2} & \text{if } n \ge 2 \end{cases}"
- For n greater than or equal to 2, the value of v_n is calculated as 4 times v_{n-1} minus v_{n-2}  
  _[ja]_ ← "v_{n} = \begin{cases} 2 & \text{if } n = 0 \\ 4 & \text{if } n = 1 \\ 4v_{n-1} - v_{n-2} & \text{if } n \ge 2 \end{cases}"
- Lucas sequences are used to find the initial value from the value of n  
  _[ja]_ ← "の値から初期値 を見出すには、リーゼルや Rodseth が示すようにリュカ数列を用いる。"
- When k equals 1, s₀ equals 4  
  _[ko]_ ← "k = 1인 경우에는 s₀ = 4가 된다."
- If k equals 1 and n is congruent to 3 modulo 4, s₀ can be set to 3  
  _[ko]_ ← "이때 뤼카-레머-리젤 소수판별법은 뤼카-레머 소수판별법과 완전히 똑같아지며, k = 1이면서 n ≡ 3 (mod 4)인 경우 s₀ = 3으로 해도 된다."
- The parentheses denote the Jacobi symbol  
  _[ko]_ ← "여기서 괄호 표시는 야코비 기호이며, 만약 3 ∤ k인 경우 P=4를 이용하면 된다."
- A Lucas sequence is defined with an initial value V_0 equal to 2  
  _[ko]_ ← "V_0=2, V_1=P, V_k=PV_{k-1}-QV_{k-2} 3. 위에서 구한 값 P와 Q=1을 이용하여 Vₖ의 값을 구한다."
- The Lucas sequence has an initial value V_1 equal to P  
  _[ko]_ ← "V_0=2, V_1=P, V_k=PV_{k-1}-QV_{k-2} 3. 위에서 구한 값 P와 Q=1을 이용하여 Vₖ의 값을 구한다."
- The recurrence relation for the sequence is V_k = P * V_{k-1} - Q * V_{k-2}  
  _[ko]_ ← "V_0=2, V_1=P, V_k=PV_{k-1}-QV_{k-2} 3. 위에서 구한 값 P와 Q=1을 이용하여 Vₖ의 값을 구한다."
- The value of Q used in the calculation is 1  
  _[ko]_ ← "V_0=2, V_1=P, V_k=PV_{k-1}-QV_{k-2} 3. 위에서 구한 값 P와 Q=1을 이용하여 Vₖ의 값을 구한다."
- The value of s₀ is equal to Vₖ  
  _[ko]_ ← "이때, s₀=Vₖ가 된다."
- The value of P that satisfies the condition is 8  
  _[ko]_ ← "P=5, 8, 9, 11 중 조건을 만족하는 값을 찾으면 P=8이고 (\left ( \frac{6}{2303} \right )=1이고 \left ( \frac{10}{2303} \right )=-1이다), Vₖ의 값을 구할 때에는 다음 두 효율적인 공식을 보통 많이 사용한다."
- Two efficient formulas are commonly used to calculate the value of V_k  
  _[ko]_ ← "P=5, 8, 9, 11 중 조건을 만족하는 값을 찾으면 P=8이고 (\left ( \frac{6}{2303} \right )=1이고 \left ( \frac{10}{2303} \right )=-1이다), Vₖ의 값을 구할 때에는 다음 두 효율적인 공식을 보통 많이 사용한다."
- The value of V at index 2i is equal to the square of the value of V at index i  
  _[ko]_ ← "V_{2i}=V_i^2"
- The value of V_{2i+1} is equal to the product of V_i and V_{i+1} minus P  
  _[ko]_ ← "-2 V_{2i+1}=V_iV_{i+1}-P"
- The value k must be converted into binary form  
  _[ko]_ ← "이 공식을 이용할 때에는 먼저 V₀으로 시작하고, k를 이진수 형태로 바꾼다."
- Therefore, Vi must be calculated simultaneously with Vi+1 in all processes  
  _[ko]_ ← "이 예시의 경우 맨 앞의 1을 제외하고 1이 한 군데 더 있으므로 (1001에서 맨 뒷쪽에 있다) 모든 과정에서 Vi를 계산하는 동시에 Vi+1도 계산해 주어야 한다.이 예시의 경우, k=9는 이진수로 바꾸면 1001₍₂₎가 된다."
- In this example, k equals 9  
  _[ko]_ ← "이 예시의 경우 맨 앞의 1을 제외하고 1이 한 군데 더 있으므로 (1001에서 맨 뒷쪽에 있다) 모든 과정에서 Vi를 계산하는 동시에 Vi+1도 계산해 주어야 한다.이 예시의 경우, k=9는 이진수로 바꾸면 1001₍₂₎가 된다."
- k=9 converts to 1001 in binary  
  _[ko]_ ← "이 예시의 경우 맨 앞의 1을 제외하고 1이 한 군데 더 있으므로 (1001에서 맨 뒷쪽에 있다) 모든 과정에서 Vi를 계산하는 동시에 Vi+1도 계산해 주어야 한다.이 예시의 경우, k=9는 이진수로 바꾸면 1001₍₂₎가 된다."
- If the leading bit is 0, use the first formula for Vi  
  _[ko]_ ← "여기서 맨 앞쪽 비트에 0이 나오면 Vi에 대해 (Vi+1이 아니다) 첫 번째 공식을 사용하고, 1이 나온 경우에는 두 번째 공식을 사용한 후 (여기서도 마찬가지로 Vi에 대해서만 계산한다."
- The first formula is not used for Vi+1 when the leading bit is 0  
  _[ko]_ ← "여기서 맨 앞쪽 비트에 0이 나오면 Vi에 대해 (Vi+1이 아니다) 첫 번째 공식을 사용하고, 1이 나온 경우에는 두 번째 공식을 사용한 후 (여기서도 마찬가지로 Vi에 대해서만 계산한다."
- If the bit is 1, use the second formula  
  _[ko]_ ← "여기서 맨 앞쪽 비트에 0이 나오면 Vi에 대해 (Vi+1이 아니다) 첫 번째 공식을 사용하고, 1이 나온 경우에는 두 번째 공식을 사용한 후 (여기서도 마찬가지로 Vi에 대해서만 계산한다."
- When using the second formula, only calculate Vi and leave Vi+1 unchanged  
  _[ko]_ ← "여기서 맨 앞쪽 비트에 0이 나오면 Vi에 대해 (Vi+1이 아니다) 첫 번째 공식을 사용하고, 1이 나온 경우에는 두 번째 공식을 사용한 후 (여기서도 마찬가지로 Vi에 대해서만 계산한다."
- The process should be repeated for all bits  
  _[ko]_ ← "Vi+1은 그대로 둔다) 맨 앞쪽의 비트를 지우고 이 과정을 모든 비트에 대해 반복하면 된다."
- Before repeating the process, the leading bit should be removed  
  _[ko]_ ← "Vi+1은 그대로 둔다) 맨 앞쪽의 비트를 지우고 이 과정을 모든 비트에 대해 반복하면 된다."
- The initial value V_0 is 2  
  _[ko]_ ← "V_0=2 이 과정에서는 V₁을 계산해야 하지만 V₁=P이므로 V₁=8이 되고, V₂=V₁²-2=62가 된다."
- V_1 must be calculated in this process  
  _[ko]_ ← "V_0=2 이 과정에서는 V₁을 계산해야 하지만 V₁=P이므로 V₁=8이 되고, V₂=V₁²-2=62가 된다."
- V_1 is equal to P  
  _[ko]_ ← "V_0=2 이 과정에서는 V₁을 계산해야 하지만 V₁=P이므로 V₁=8이 되고, V₂=V₁²-2=62가 된다."
- Therefore, V_1 equals 8  
  _[ko]_ ← "V_0=2 이 과정에서는 V₁을 계산해야 하지만 V₁=P이므로 V₁=8이 되고, V₂=V₁²-2=62가 된다."
- V_2 is calculated as V_1 squared minus 2  
  _[ko]_ ← "V_0=2 이 과정에서는 V₁을 계산해야 하지만 V₁=P이므로 V₁=8이 되고, V₂=V₁²-2=62가 된다."
- The resulting value of V_2 is 62  
  _[ko]_ ← "V_0=2 이 과정에서는 V₁을 계산해야 하지만 V₁=P이므로 V₁=8이 되고, V₂=V₁²-2=62가 된다."
- The initial bit sequence is 001  
  _[ko]_ ← "001에서 맨 처음 비트가 0이므로 첫 번째 공식을 사용한다."
- The first bit in the sequence is 0  
  _[ko]_ ← "001에서 맨 처음 비트가 0이므로 첫 번째 공식을 사용한다."
- The first formula is used because the first bit is 0  
  _[ko]_ ← "001에서 맨 처음 비트가 0이므로 첫 번째 공식을 사용한다."
- The value of V_2 is equal to the value of V_{2*1}  
  _[ko]_ ← "V_{2\cdot1}=V_2"
- V1 squared minus 2 equals 62  
  _[ko]_ ← "=V_1^2-2=62가 되고, V_{2+1}=V_3=V_1V_2-8=488이 된다."
- V3 is equal to V1 multiplied by V2 minus 8  
  _[ko]_ ← "=V_1^2-2=62가 되고, V_{2+1}=V_3=V_1V_2-8=488이 된다."
- The value of V3 is 488  
  _[ko]_ ← "=V_1^2-2=62가 되고, V_{2+1}=V_3=V_1V_2-8=488이 된다."
- The leading zero is removed  
  _[ko]_ ← "맨 앞의 0을 지운다."
- The binary sequence is 01  
  _[ko]_ ← "01에서 맨 처음 비트가 0이므로 첫 번째 공식을 사용한다."
- The first bit of the sequence is 0  
  _[ko]_ ← "01에서 맨 처음 비트가 0이므로 첫 번째 공식을 사용한다."
- The first formula is used  
  _[ko]_ ← "01에서 맨 처음 비트가 0이므로 첫 번째 공식을 사용한다."
- V_4 is equal to V_{2*2}  
  _[ko]_ ← "V_{2\cdot2}=V_4"
- V_2 squared minus 2 equals 3842  
  _[ko]_ ← "=V_2^2-2=3842\equiv1539\pmod{2303}이 되고, V_{4+1}=V_5=V_2V_3-8=30248\equiv309\pmod{2303}이 된다."
- 3842 is congruent to 1539 modulo 2303  
  _[ko]_ ← "=V_2^2-2=3842\equiv1539\pmod{2303}이 되고, V_{4+1}=V_5=V_2V_3-8=30248\equiv309\pmod{2303}이 된다."
- V_{4+1} equals V_5  
  _[ko]_ ← "=V_2^2-2=3842\equiv1539\pmod{2303}이 되고, V_{4+1}=V_5=V_2V_3-8=30248\equiv309\pmod{2303}이 된다."
- V_5 equals V_2 multiplied by V_3 minus 8  
  _[ko]_ ← "=V_2^2-2=3842\equiv1539\pmod{2303}이 되고, V_{4+1}=V_5=V_2V_3-8=30248\equiv309\pmod{2303}이 된다."
- V_2 multiplied by V_3 minus 8 equals 30248  
  _[ko]_ ← "=V_2^2-2=3842\equiv1539\pmod{2303}이 되고, V_{4+1}=V_5=V_2V_3-8=30248\equiv309\pmod{2303}이 된다."
- 30248 is congruent to 309 modulo 2303  
  _[ko]_ ← "=V_2^2-2=3842\equiv1539\pmod{2303}이 되고, V_{4+1}=V_5=V_2V_3-8=30248\equiv309\pmod{2303}이 된다."
- The first bit of the number 1 is 1  
  _[ko]_ ← "1에서 맨 처음 비트가 1이므로 두 번째 공식을 사용한다."
- The second formula is used when the first bit is 1  
  _[ko]_ ← "1에서 맨 처음 비트가 1이므로 두 번째 공식을 사용한다."
- V_9 is equal to V_4 multiplied by V_5 minus 8  
  _[ko]_ ← "+1}=V_9=V_4V_5-8\equiv1133\pmod{2303}이 된다."
- The result of the calculation for V_9 is congruent to 1133 modulo 2303  
  _[ko]_ ← "+1}=V_9=V_4V_5-8\equiv1133\pmod{2303}이 된다."
- The leading 1 is removed.  
  _[ko]_ ← "맨 앞의 1을 지운다."
- The initial value s_0 is equal to V_k  
  _[ko]_ ← "따라서 s_0=V_k=V_9\equiv1133\pmod{2303}이 된다."
- V_k is equal to V_9  
  _[ko]_ ← "따라서 s_0=V_k=V_9\equiv1133\pmod{2303}이 된다."
- V_9 is congruent to 1133 modulo 2303  
  _[ko]_ ← "따라서 s_0=V_k=V_9\equiv1133\pmod{2303}이 된다."
- When k equals 1, 4 is a good starting value for odd n  
  _[nl]_ ← "Als k=1, is 4 een goede startwaarde voor oneven n;"
- u_0 equals 3  
  _[nl]_ ← "u_0 = 3."
- The condition applies when k equals 1  
  _[nl]_ ← "Als k=1 of k\equiv 5 \pmod 6 en 3 is geen deler van N, dan geldt"
- The condition applies when 3 does not divide N  
  _[nl]_ ← "Als k=1 of k\equiv 5 \pmod 6 en 3 is geen deler van N, dan geldt"
- The case being discussed is k = 1  
  _[ru]_ ← "Случай k = 1."
- The case considers n being odd  
  _[ru]_ ← "Если n — нечётно, то берётся значение u_0 = 4."
- If n is odd, the value u_0 is set to 4  
  _[ru]_ ← "Если n — нечётно, то берётся значение u_0 = 4."

### LLR software
- The software is Jean Penné's LLR Math::Prime::Util::GMP  
  _[ja]_ ← "Download Jean Penné's LLR Math::Prime::Util::GMP - Perl の ntheory モジュールの一部であり、LLR の基本的な実装とプロス数に対する Brillhart–Lehmer–Selfridge テストと同様のものが実装されている。"
- The software is part of the Perl ntheory module  
  _[ja]_ ← "Download Jean Penné's LLR Math::Prime::Util::GMP - Perl の ntheory モジュールの一部であり、LLR の基本的な実装とプロス数に対する Brillhart–Lehmer–Selfridge テストと同様のものが実装されている。"
- The software includes a basic implementation of LLR  
  _[ja]_ ← "Download Jean Penné's LLR Math::Prime::Util::GMP - Perl の ntheory モジュールの一部であり、LLR の基本的な実装とプロス数に対する Brillhart–Lehmer–Selfridge テストと同様のものが実装されている。"
- The software implements a test similar to the Brillhart–Lehmer–Selfridge test for Proth numbers  
  _[ja]_ ← "Download Jean Penné's LLR Math::Prime::Util::GMP - Perl の ntheory モジュールの一部であり、LLR の基本的な実装とプロス数に対する Brillhart–Lehmer–Selfridge テストと同様のものが実装されている。"
- The project stopped in 2010  
  _[nl]_ ← "In 2010 is het project gestopt."
- The module is written in Perl  
  _[ru]_ ← "Download Jean Penné's LLR Math::Prime::Util::GMP — Модуль на Perl, базовая реализация LLR и теста Прота, а также некоторые методы из статьи Брилхарта, Лемера и …"
- The module provides a basic implementation of the LLR test  
  _[ru]_ ← "Download Jean Penné's LLR Math::Prime::Util::GMP — Модуль на Perl, базовая реализация LLR и теста Прота, а также некоторые методы из статьи Брилхарта, Лемера и …"
- The module provides a basic implementation of the Proth test  
  _[ru]_ ← "Download Jean Penné's LLR Math::Prime::Util::GMP — Модуль на Perl, базовая реализация LLR и теста Прота, а также некоторые методы из статьи Брилхарта, Лемера и …"
- The module includes some methods from the Brillhart, Lehmer, and Selfridge article  
  _[ru]_ ← "Download Jean Penné's LLR Math::Prime::Util::GMP — Модуль на Perl, базовая реализация LLR и теста Прота, а также некоторые методы из статьи Брилхарта, Лемера и …"

### The algorithm
- Otherwise, if the condition is not met, N is a composite number.  
  _[ko]_ ← "아닌 경우, N은 합성수가 된다."
- If the value of k is even, divide k by 2 repeatedly until k becomes odd  
  _[ko]_ ← "만약 k의 값이 짝수일 경우, k가 홀수가 될 때까지 k를 2로 나눠 나간다."
- For a prime number n, the values are Mersenne numbers.  
  _[ru]_ ← "Для простого n — это числа Мерсенна."

### History  *(new section)*
- Riesel and Rodseth have demonstrated this method  
  _[ja]_ ← "の値から初期値 を見出すには、リーゼルや Rodseth が示すようにリュカ数列を用いる。"
- The original algorithm was developed by Édouard Lucas  
  _[ko]_ ← "에두아르 뤼카 (Édouard Lucas)의 원래 알고리즘을 데릭 레머 (Derrick Henry Lehmer)가 개량한 알고리즘인 뤼카-레머 소수판별법을 더 많은 수들에 대해 적용할 수 있도록 수학자 한스 리젤 (Hans Riesel)이 한번 더 개량한 알고리즘이다."
- Derrick Henry Lehmer improved the original algorithm  
  _[ko]_ ← "에두아르 뤼카 (Édouard Lucas)의 원래 알고리즘을 데릭 레머 (Derrick Henry Lehmer)가 개량한 알고리즘인 뤼카-레머 소수판별법을 더 많은 수들에 대해 적용할 수 있도록 수학자 한스 리젤 (Hans Riesel)이 한번 더 개량한 알고리즘이다."
- Hans Riesel further improved the algorithm to apply it to more numbers  
  _[ko]_ ← "에두아르 뤼카 (Édouard Lucas)의 원래 알고리즘을 데릭 레머 (Derrick Henry Lehmer)가 개량한 알고리즘인 뤼카-레머 소수판별법을 더 많은 수들에 대해 적용할 수 있도록 수학자 한스 리젤 (Hans Riesel)이 한번 더 개량한 알고리즘이다."

### Special cases and examples  *(new section)*
- If k equals 1 and n is prime, then we are facing a Mersenne number  
  _[it]_ ← "Se k = 1 e n è primo, allora ci troviamo di fronte ad un numero di Mersenne e possiamo prendere u₀ = 4."
- When k equals 3, if n is congruent to 1 modulo 4, then N is congruent to 0 modulo 5  
  _[ko]_ ← "k = 3인 경우, n ≡ 1 (mod 4)인 경우에는 N ≡ 0 (mod 5)가 되어 N의 값이 5인 경우를 제외하면 N이 합성수가 된다."
- If N is not equal to 5 under these conditions, N is a composite number  
  _[ko]_ ← "k = 3인 경우, n ≡ 1 (mod 4)인 경우에는 N ≡ 0 (mod 5)가 되어 N의 값이 5인 경우를 제외하면 N이 합성수가 된다."
- N is not divisible by 3  
  _[ko]_ ← "k ≡ 1 또는 5 (mod 6)이고 3\nmid N인 경우, s_0=(2+\sqrt3)^{k}+(2-\sqrt3)^{k}=\lceil(2+\sqrt3)^{k}\rceil이다."
- 47 is equal to 3 multiplied by 2 to the power of 4 minus 1  
  _[ko]_ ← "47=3 ⋅ 2⁴ - 1이므로 k=3, n=4이다."
- The value of k is 3  
  _[ko]_ ← "47=3 ⋅ 2⁴ - 1이므로 k=3, n=4이다."
- The value of n is 4  
  _[ko]_ ← "47=3 ⋅ 2⁴ - 1이므로 k=3, n=4이다."
- 2303 is equal to 9 multiplied by 2 to the power of 8 minus 1  
  _[ko]_ ← "2303 = 9 ⋅ 2⁸ - 1이므로 k=9, n=8이다."
- In this example, there is one additional '1' bit besides the leading '1'  
  _[ko]_ ← "이 예시의 경우 맨 앞의 1을 제외하고 1이 한 군데 더 있으므로 (1001에서 맨 뒷쪽에 있다) 모든 과정에서 Vi를 계산하는 동시에 Vi+1도 계산해 주어야 한다.이 예시의 경우, k=9는 이진수로 바꾸면 1001₍₂₎가 된다."
- The additional '1' bit is located at the end of 1001  
  _[ko]_ ← "이 예시의 경우 맨 앞의 1을 제외하고 1이 한 군데 더 있으므로 (1001에서 맨 뒷쪽에 있다) 모든 과정에서 Vi를 계산하는 동시에 Vi+1도 계산해 주어야 한다.이 예시의 경우, k=9는 이진수로 바꾸면 1001₍₂₎가 된다."
- 2303 is a composite number  
  _[ko]_ ← "s₈₋₂=s₆이 2303으로 나눴을 때 나머지가 0이 아니므로 (692이다), 2303은 합성수가 된다."
- s_8-2 equals s_6  
  _[ko]_ ← "s₈₋₂=s₆이 2303으로 나눴을 때 나머지가 0이 아니므로 (692이다), 2303은 합성수가 된다."
- Dividing 2303 by the result of s_8-2 (which is s_6) leaves a remainder that is not zero  
  _[ko]_ ← "s₈₋₂=s₆이 2303으로 나눴을 때 나머지가 0이 아니므로 (692이다), 2303은 합성수가 된다."
- The remainder when dividing 2303 by s_6 is 692  
  _[ko]_ ← "s₈₋₂=s₆이 2303으로 나눴을 때 나머지가 0이 아니므로 (692이다), 2303은 합성수가 된다."
- 2303 can be factored into 7 squared multiplied by 47  
  _[ko]_ ← "실제로 2303=7²⋅47이다."

### Applications  *(new section)*
- The primality test is mainly used when the number to be tested has more than 10 million digits  
  _[ko]_ ← "하지만 테스트할 수가 1000만 자리가 넘어가는 경우에서는 이 소수판별법의 효율이 다른 소수판별법들을 크게 뛰어넘기 때문에 이 소수판별법을 주로 사용한다."
- In such cases, the efficiency of this primality test greatly surpasses that of other primality tests  
  _[ko]_ ← "하지만 테스트할 수가 1000만 자리가 넘어가는 경우에서는 이 소수판별법의 효율이 다른 소수판별법들을 크게 뛰어넘기 때문에 이 소수판별법을 주로 사용한다."

## Knowledge conflicts (CONTRADICTED — human adjudication queue)

- **Non-English claim** _[ko]_: The Lucas-Lehmer-Riesel primality test is identical to the Lucas-Lehmer primality test
  - English says: The algorithm is very similar to the Lucas–Lehmer test, but with a variable starting point depending on the value of k.
  - Proposed reconciliation: 2024-01-14T11:56:58Z

- **Non-English claim** _[ko]_: s₀ equals the ceiling of (2 + √3)^k
  - English says: we take u_0 = (2+\sqrt{3})^k+(2-\sqrt{3})^k, which is the kth term of that sequence.
  - Proposed reconciliation: 2024-01-14T11:56:58Z

- **Non-English claim** _[nl]_: When k equals 3, u_0 must equal 5778
  - English says: It is known that if k = 3 and n ≡ 0 or 3 (mod 4), we can take u₀ = 5778.
  - Proposed reconciliation: 2024-01-14T11:56:58Z

- **Non-English claim** _[nl]_: The value of u_0 is equal to (2 plus the square root of 3) raised to the power of h, plus (2 minus the square root of 3) raised to the power of h
  - English says: we take u_0 = (2+\sqrt{3})^k+(2-\sqrt{3})^k, which is the kth term of that sequence.
  - Proposed reconciliation: 2024-01-14T11:56:58Z

- **Non-English claim** _[ru]_: If n is congruent to 3 modulo 4, then u_0 is set to 3
  - English says: It is known that if k = 3 and n ≡ 0 or 3 (mod 4), we can take u₀ = 5778.
  - Proposed reconciliation: 2024-01-14T11:56:58Z

- **Non-English claim** _[ru]_: Jean Penné created the LLR Math::Prime::Util::GMP module
  - English says: LLR is a program that can run the LLR tests. The program was developed by Jean Penné.
  - Proposed reconciliation: 2024-01-14T11:56:58Z
