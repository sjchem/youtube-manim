# Concept Summary

A short, accurate statement of the mathematics the film teaches, and of the
places where the film uses a metaphor rather than a proof.

## The one question

> When I rearrange the same objects, have I created something new?

If yes, the arrangement is part of the outcome and you are counting
**permutations**. If no, only the selection matters and you are counting
**combinations**. Every formula below is a consequence of that single question.

## 1. The multiplication principle

If a process happens in stages, and stage *i* offers $k_i$ choices
regardless of what was chosen earlier, the number of complete outcomes is

$$k_1 \times k_2 \times \cdots \times k_m.$$

The film establishes this with a branching tree (3 shirts × 2 trousers = 6
outfits) before any notation appears. **Equal branch counts matter**: the rule as
stated needs the *number* of options at each stage to be fixed, even when the
identity of those options depends on earlier choices — which is exactly the
situation in the factorial and permutation chapters. Statistical independence
is not required. If counts vary across branches, count each branch and add.

## 2. Factorials

Arranging all *n* distinct objects in *n* ordered positions is a staged process
whose available choices shrink by exactly one each time:

$$n! = n \times (n-1) \times (n-2) \times \cdots \times 2 \times 1.$$

So $4! = 24$. The film's framing — *a factorial is what multiplication looks
like when every position costs one choice* — is a description of the mechanism,
not a separate theorem.

Growth is superexponential: $8! = 40{,}320$ and $12! = 479{,}001{,}600$. The
narration says "nearly half a billion", which is accurate for $12!$.

The companion **addition principle** is also shown: mutually exclusive
alternatives add. Three bus routes or two train routes give $3+2=5$ journeys,
whereas a shirt and a pair of trousers are successive stages and multiply.

## 3. Permutations: ordered selections

Filling *r* ordered positions from *n* distinct objects stops the shrinking
product early:

$$n(n-1)\cdots(n-r+1) = \frac{n!}{(n-r)!} = {}_nP_r.$$

The unwanted tail $(n-r)!$ is precisely the arrangements of the objects that
were *not* placed, so dividing by it removes distinctions the problem never
asked about. Worked example: ${}_5P_3 = 5!/2! = 60$ podiums from five runners.

Requires $0 \le r \le n$, and requires the objects to be **distinguishable**
and drawn **without replacement**. The PIN example explicitly contrasts this
with reuse: four positions, each allowing any of ten digits including leading
zero, give $10^4=10{,}000$ codes, not ${}_{10}P_4$.

## 4. Combinations: unordered selections

Any group of *r* chosen objects can be internally rearranged in $r!$ ways, and
${}_nP_r$ counts every one of those rearrangements separately. Dividing by that
overcount gives

$$\binom{n}{r} = \frac{{}_nP_r}{r!} = \frac{n!}{r!\,(n-r)!}.$$

Worked example: $\binom{5}{3} = 60/6 = 10$ science teams. The central sentence
of the film — *a combination is a permutation with the unnecessary order
divided away* — is exactly this identity, read aloud.

## 5. The symmetry

$$\binom{n}{r} = \binom{n}{n-r}.$$

Choosing which *r* objects go in is the same act as choosing which $n-r$ stay
out, so the two counts are the same list read from opposite sides. This is a
**bijection argument**, not an algebraic coincidence, and the film shows it as
one: the highlight inverts, and nothing else moves. Example:
$\binom{10}{3} = \binom{10}{7} = 120$.

Laying out the whole row $\binom{10}{0}, \dots, \binom{10}{10}$ gives
$1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1$ — row 10 of Pascal's triangle,
symmetric about its centre, summing to $2^{10}$.

## 6. Scale: poker hands

A five-card hand is unordered, so

$$\binom{52}{5} = \frac{52!}{5!\,47!}
= \frac{52\cdot51\cdot50\cdot49\cdot48}{120}
= \frac{311{,}875{,}200}{120} = 2{,}598{,}960.$$

This counts hands as *sets of cards*, which is the standard convention for
poker hand enumeration; it says nothing about hand rankings or probabilities,
and the film does not claim otherwise.

## 7. Why $0! = 1$

$\binom{5}{5} = 1$ — there is one way to take everybody. The formula gives
$\binom{5}{5} = 5!/(5!\,0!)$, which equals 1 only if $0! = 1$. The value is
therefore the definition that **preserves consistency** at this boundary. The combinatorial
reading agrees: there is exactly one arrangement of the empty set — the empty
arrangement.

## 8. Restricted arrangements

The block method turns objects that must remain together into one temporary
object. For MATH with A and T adjacent, the objects M, [AT], H have $3!$
orders, while the block has $2!$ internal orders, giving $3!2!=12$.

The gap method first arranges the objects that separate the others. Three
distinct boys create four gaps; placing two distinct girls in different gaps
gives

$$3!\binom42 2!=72.$$

Both are applications of the multiplication principle, not independent
formulas.

## 9. Alike objects and geometrical counting

If $n$ objects contain groups of $p,q,r,\ldots$ identical objects, distinct
linear arrangements number

$$\frac{n!}{p!q!r!\cdots}.$$

For LEVEL this is $5!/(2!2!)=30$. The divisors remove swaps that make no
visible change.

Every pair of an $n$-gon's vertices determines a segment. Removing its $n$
sides leaves

$$\binom n2-n$$

diagonals. Thus a hexagon has $15-6=9$. Likewise, $n$ points with no three
collinear determine $\binom n3$ triangles.

## Metaphors, marked as metaphors

* **"Permutation lock."** Real padlocks are called combination locks by long
  convention. The film's point is linguistic, not a claim that manufacturers are
  wrong about their own products: a mathematical code is an ordered sequence.
  With repeats allowed, it is not counted by the
  no-replacement permutation formula. The hook uses rearrangements of three
  distinct digits to isolate what order means.
* **"The pool shrinks."** A visual stand-in for sampling without replacement.
* **"Order divided away."** Dividing by $r!$ is a genuine identity, but the
  phrase "divided away" is informal language for collapsing an equivalence class
  of size $r!$ onto one representative.

## Deliberate scope limits

The main factorial formulas cover distinguishable objects chosen without
replacement. A short PIN example introduces ordered sequences with repetition
($n^r$) to prevent a misleading use of $nPr$. The film does **not** develop
combinations with repetition (stars and bars), circular permutations,
derangements, distributions, divisor counting, or the binomial theorem. The symmetry
chapter is chosen partly because it hints at Pascal's triangle without spending
the binomial theorem, which is a separate film.

## Verification

The principal counts are checked against exact arithmetic and small enumerations:

```
python -m utils.math_utils        # exact counts, checked against brute force
python -m utils.counting_models   # Pascal rows, overcount maps, Monte-Carlo check
```

## Reference

[OpenStax, Contemporary Mathematics §7.2](https://openstax.org/books/contemporary-mathematics/pages/7-2-permutations)
defines permutations here as ordered lists without repeated items, derives the
factorial quotient from sequential choices, and explains the boundary value
$0!=1$. This is the convention used for the film's permutation formula.
