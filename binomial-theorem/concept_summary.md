# Concept summary — Why Does Pascal's Triangle Know Algebra?

## The question

Expand $(a+b)^5$ and you get $a^5 + 5a^4b + 10a^3b^2 + 10a^2b^3 + 5ab^4 + b^5$.
Row 5 of Pascal's triangle (the top is row 0) — built only by adding neighbours — reads
1, 5, 10, 10, 5, 1. Why would a triangle of sums know an algebra problem?

## The answer in one line

Expanding a binomial *is* a counting problem. Pascal's triangle does not
predict the binomial theorem; both grow out of the same structure: counting
the ways to choose.

## The chain of ideas (the order the film builds them)

1. **Expansion is choosing.** $(a+b)^n$ is $n$ brackets multiplied together.
   Every product in the full expansion is made by picking one letter, $a$ or
   $b$, from each bracket. One complete set of picks is a *choice list* such
   as $aabab$, and it multiplies to $a^3b^2$. There are $2^n$ lists, the
   $2^n$ raw products that brute force produces before like terms are collected.
2. **Coefficients count lists.** Lists with the same number of $b$'s multiply
   to the same term. The coefficient of $a^{n-k}b^k$ is the number of lists
   with exactly $k$ $b$'s. For $n = 5$ the piles are 1, 5, 10, 10, 5, 1.
3. **Counting a pile is a combination.** A list with $k$ $b$'s is fixed by
   *which* $k$ brackets say $b$, so a pile is the set of $k$-element subsets of
   $n$ brackets: $\binom{n}{k} = \frac{n!}{k!\,(n-k)!}$. For $\binom52$: $5\cdot4$
   ordered picks, each pair counted twice, so $20/2 = 10$.
4. **The theorem.** For a nonnegative integer $n$,
   $(a+b)^n = \sum_{k=0}^{n}\binom{n}{k}a^{n-k}b^k$. Each
   symbol has a picture: $b^k$ is $k$ brackets saying $b$, $a^{n-k}$ is the
   rest, $\binom nk$ counts the ways, the sum collects every $k$.
5. **Opposite exponents and symmetry.** Every product has $n$ factors, so
   $(n-k)+k = n$; trading one $a$ for one $b$ steps along the expansion.
   Picking which $k$ say $b$ is picking which $n-k$ say $a$:
   $\binom nk = \binom n{n-k}$. Setting $a=b=1$: $\sum_k \binom nk = 2^n$.
6. **Pascal's rule, two ways.**
   - *Algebra:* $(a+b)^{n} = (a+b)^{n-1}\cdot a + (a+b)^{n-1}\cdot b$. The
     "times $b$" copy is the previous row slid one place along, so adding the
     copies adds neighbours.
   - *Counting:* look at the newest bracket. Either it says $b$ (choose $k-1$
     more from the other $n-1$) or it says $a$ (choose all $k$ from them):
     $\binom nk = \binom{n-1}{k-1} + \binom{n-1}{k}$. Every list lands in
     exactly one case. The two arguments are the same split.
7. **Paths.** In the triangle, step down-left for $a$ and down-right for $b$.
   A route of $n$ steps is a choice list; it ends $k$ places from the left
   when it took $k$ right steps. So the entry at $(n, k)$ counts routes, and
   routes into a cell come through one of its two parents (4 + 6 = 10).
8. **Chance.** Heads plays $a$, tails plays $b$. For independent flips of a fair coin all $2^n$
   sequences are equally likely, so $P(k \text{ tails}) = \binom nk / 2^n$;
   for five flips, $P(2\text{ tails}) = 10/32 \approx 0.31$. As $n$ grows the
   normalised row is approximated by a normal (bell) curve with mean $n/2$ and variance $n/4$
   (the de Moivre–Laplace theorem).

## Accuracy notes and honest metaphors

- **Choice machines are a metaphor** for "pick one term from each bracket" —
  the distributive law applied $n$ times. Nothing in the algebra has doors.
- **The finite theorem uses $n = 0,1,2,\ldots$ and $0 \le k \le n$.**
  The triangle's edges are 1; its interior entries add their two parents.
  When using Pascal's rule at an edge, out-of-range binomial coefficients are 0.
- **The area and volume pictures** (square and cube of side $a+b$) assume
  $a, b > 0$ so lengths make sense. The identities hold for any numbers.
- **The Galton board is idealised.** The film treats every bounce as an
  independent fair coin flip. A real board has momentum, imperfect pegs and
  correlated bounces, so the narration explicitly calls this an ideal board.
- **The 64-ball sample is genuinely random** (seeded, so renders are
  reproducible): it lands 1, 10, 19, 22, 11, 1 against an expected 2, 10, 20,
  20, 10, 2. The 1,024-ball comparison is rescaled to 64 balls so both are
  drawn on one axis; the chip says "scaled".
- **The bell curve** drawn over row 20 is $2^{20}\,\varphi(k)$ with
  $\mu = 10$, $\sigma = \sqrt{20}/2$; it is an approximation, and the film
  calls it an approximation. Each longer row is scaled to fit the frame;
  these shots compare shapes, rather than absolute bar heights across rows.
- **$11^n$ trick**: the digits of $11^n$ spell row $n$ only while every entry
  is a single digit ($n \le 4$). Row 5 contains 10s, which carry:
  $11^5 = 161051$. An arrow shows the coefficients producing the number
  through carrying; the binomial identity still holds.
- **Pascal's triangle predates Pascal** (Pingala, al-Karaji, Jia Xian, Yang
  Hui, Omar Khayyam, Tartaglia…). The film uses the familiar English name and
  makes no historical claim.

## How the film keeps itself honest

Every number on screen comes from `utils/math_utils.py`, which gets each
coefficient by literally expanding the brackets as choice lists and counting.
`python -m utils.math_utils` then verifies, for every $n \le 12$, that this
brute-force count equals `math.comb`, the factorial formula, Pascal's addition
rule, the path count, the symmetric row, the $2^n$ row sum, the last-bracket
split and the shifted-copy sum. No scene types a coefficient by hand.

## References

- R. L. Graham, D. E. Knuth, O. Patashnik, *Concrete Mathematics*, 2nd ed.,
  §5.1 (binomial coefficients, Pascal's rule, the binomial theorem).
- A. T. Benjamin, J. J. Quinn, *Proofs that Really Count* (2003) — counting
  ("combinatorial") proofs of binomial identities, the style used in chapter 9.
- W. Feller, *An Introduction to Probability Theory and Its Applications*,
  Vol. 1, Ch. VI–VII (binomial distribution; the normal approximation).
- F. Galton, *Natural Inheritance* (1889) — the quincunx (Galton board).
- A. W. F. Edwards, *Pascal's Arithmetical Triangle* (1987) — history.
