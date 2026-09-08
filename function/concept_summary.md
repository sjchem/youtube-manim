# Concept summary — What Does a Function Actually Do?

## The one idea

A **function** is a rule that assigns to each allowed input **exactly one** output.
Everything else in the film is a consequence of that sentence.

```
x  ──►  f  ──►  f(x)
```

`f(x)` is not a product. It is a name for *the thing f returns when it is handed x*.

## The chain of consequences

| Idea | Statement | Why it follows |
|---|---|---|
| Single-valuedness | one input ↦ one output | otherwise "the answer" is not defined |
| Many-to-one is fine | `f(2) = f(-2) = 4` | nothing forbids two inputs sharing an answer |
| Domain | the set of allowed inputs | some inputs are meaningless or undefined |
| Range | the set of outputs actually produced | determined by the rule *and* the domain |
| Graph | the set `{(x, f(x))}` | a picture of every input–output pair |
| Vertical line test | each vertical line meets the graph at most once | a second crossing is a second output for one input |
| Transformations | `a·f(x − h) + k` | edits to the rule become translations, scaling or reflection |
| Composition | `(g ∘ f)(x) = g(f(x))` | machines wired in series; order matters |
| Inverse | `f⁻¹(f(x)) = x` | reverses the assignment; exists from its range back to its domain when `f` is one-to-one |
| Reflection in `y = x` | `(a, b) ↦ (b, a)` | the inverse swaps the roles of input and output |
| Restriction | `x² on x ≥ 0` has inverse `√x` | narrowing the domain removes the ambiguity |
| More inputs | `z = f(x, y)` | the graph becomes a surface; the definition is unchanged |

## Precise statements used in the film

**Definition.** A function `f : A → B` assigns to every `a ∈ A` exactly one `f(a) ∈ B`.
`A` is the **domain**; `{f(a) : a ∈ A} ⊆ B` is the **range** (image).

**Vertical line test.** A subset `S ⊆ ℝ²` is the graph of a function of `x`
if and only if for every `x` there is at most one `y` with `(x, y) ∈ S`.
The on-screen circle `x² + y² = 4` fails this at every `|x| < 2`. The domain of a graph is its horizontal projection, so a vertical line outside that domain has no crossing.

**Transformations.** For the parabola `f(x) = x²`:

- `f(x) + k` translates the graph vertically by `k`;
- `f(x − h)` translates it horizontally by `+h` — the rule now needs `x = h`
  to reproduce what `x = 0` used to do, which is why "minus" moves it right;
- `a·f(x)` scales every output by `a` (a reflection in the x-axis when `a < 0`).

**Composition is not commutative.** With `f(x) = x + 2` and `g(x) = x²`:

```
g(f(x)) = (x + 2)²      g(f(3)) = 25
f(g(x)) = x² + 2        f(g(3)) = 11
```

**Inverses.** `f : A → B` has an inverse from its range `f(A)` back to `A` if and only if it is injective (one-to-one). An inverse defined on all of the stated codomain `B` also requires surjectivity, so `f : A → B` must be bijective. `f(x) = 2x` is injective on ℝ, so `f⁻¹(x) = x/2`.
`f(x) = x²` is not injective on ℝ, because `f(2) = f(−2) = 4`; restricted to
`x ≥ 0` it becomes injective, with inverse `√x`.

Reflecting a graph in `y = x` sends `(a, b)` to `(b, a)`, which is exactly the
swap that turns "x in, y out" into "y in, x out". Hence the graph of `f⁻¹` is
the mirror image of the graph of `f` in the line `y = x`.

## Where the film uses a metaphor, and where it does not

- **Metaphor:** the *machine*. Nothing physically enters a box. It is a picture
  of the assignment `x ↦ f(x)`, used because the assignment is the whole content
  of the definition.
- **Metaphor:** the *loss landscape* in chapter 11. The surface
  `z = f(x, y)` used on screen is invented, not fitted to a real model. What it
  illustrates is real: a machine-learning loss is a genuine function of the
  parameters, and suitably chosen gradient-descent steps seek lower loss. Real training need not find a global minimum.
- **Not a metaphor:** everything about graphs, the vertical line test,
  transformations, composition, and inverses is stated exactly as it is true.

## Modelling details

A vending-machine selection, with its working state fixed, determines a drink; money alone need not. A fixed deterministic image model maps an image to scores. Age alone does not determine a person's height, so the examples use Celsius-to-Fahrenheit conversion instead. The radius restriction comes from the physical model, not from an inability to square a negative number.

In the probability example, `P(Y=1 | x)` is the probability of a specified event, not an unspecified random variable. Differentiation is shown as an operator on suitable functions. The 3D input `(x,y)` is one element of a product domain and produces one scalar output.

The squaring rule is continuous on the real numbers; the finite samples illustrate it but do not determine it uniquely. Inverse graph reflections use equal x/y units so swapping coordinates is a geometric reflection in `y=x`. Inverse notation is not reciprocal notation.

## References

- [OpenStax: Functions and Function Notation](https://openstax.org/books/precalculus-2e/pages/1-1-functions-and-function-notation) — definition, tables and mappings.
- [OpenStax: Inverse Functions](https://openstax.org/books/precalculus/pages/1-7-inverse-functions) — one-to-one functions, domain restriction and square roots.
- [Manim configuration](https://docs.manim.community/en/stable/guides/configuration.html) — explicit render resolution and frame-rate overrides.
