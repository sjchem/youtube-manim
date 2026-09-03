# Concept Summary — Visual Calculus: From Derivatives to Integrals (Part 2)

## Main question

A derivative measures how fast something is changing. An integral measures how much has accumulated. These look like two unrelated ideas — so why does calculus insist they are opposite views of the same process?

## Core idea

1. Distance is the area under a velocity graph — exactly, when velocity is constant; approximately, via rectangles, when it is not.
2. Splitting time into more and thinner rectangles (a Riemann sum) makes the approximation converge on the true area. The limit of that process is the integral, `∫f(x)dx`.
3. The differential `dx` is not decoration: it is the width of one infinitesimally thin rectangular strip, `dA = f(x)dx`.
4. The **accumulation function** `A(x) = ∫ₐˣ f(t)dt` grows as `x` moves right; its instantaneous growth rate equals `f(x)`. That is the **Fundamental Theorem of Calculus**: `A'(x) = f(x)`.
5. `f(x) = x` makes the theorem concrete: the area under the line is `x²/2`, and differentiating `x²/2` returns exactly `x`.
6. A derivative is not merely a slope at one point — sweeping a tangent across `f(x) = x²` and plotting its slope everywhere produces an entirely new function, `f'(x) = 2x`.
7. A curve's maxima and minima occur exactly where its derivative changes sign — where change itself reverses direction.
8. Optimization puts that to work: for a fenced garden with a fixed perimeter, the area function has a single interior maximum, found by setting its derivative to zero.
9. Differentiation is not perfectly reversible: many functions (`t² + C` for any `C`) share the same derivative, since a derivative discards information about a fixed vertical offset. That is the meaning of the integration constant `+C`.
10. Integration by substitution is a change of coordinates (`u = g(x)`) that makes a complicated integrand look simple; integration by parts (`∫u dv = uv − ∫v du`) falls directly out of the product rule applied to a growing rectangle's area.
11. The area between two curves is the integral of their difference, `∫ₐᵇ[f(x) − g(x)]dx` — another instance of "add up infinitely many thin strips."
12. The same motion, viewed through differentiation (position → velocity) and through integration (velocity → accumulated displacement), demonstrates the Fundamental Theorem's two equivalent statements: `d/dx(∫ₐˣ f(t)dt) = f(x)` and `∫ₐᵇ f(x)dx = F(b) − F(a)` whenever `F' = f`.

## Learning outcomes

After watching, a beginner should be able to explain:

- why distance is the area under a velocity-time graph;
- how a Riemann sum of rectangles converges to an integral as the rectangle count grows;
- the geometric meaning of `dx` as the width of an infinitesimally thin strip;
- the Fundamental Theorem of Calculus, both as `A'(x) = f(x)` and as `∫ₐᵇf(x)dx = F(b) − F(a)`;
- why a derivative is a whole new function, not a single number;
- how the sign of a derivative identifies rising, falling, and stationary points, and how that locates maxima and minima;
- how to set up and solve a constrained optimization problem (the fenced-garden example) using a derivative;
- why every indefinite integral carries an arbitrary constant `+C`;
- why substitution is a coordinate change and why integration by parts follows from the product rule;
- how to set up the integral for the area between two curves;
- that differentiation and integration are inverse operations applied to the same underlying motion.

## Accuracy boundaries

- The car's velocity model, `v(t) = 2.0 + 0.9 sin(1.1t) + 0.35t`, is an illustrative curve chosen to have a closed-form antiderivative, not a measured real-world trajectory; every distance and area figure shown for it is computed exactly from that antiderivative, never approximated silently.
- The accumulation-function integrand in scene 04, `f(x) = 0.5x + 1.6 sin(0.9x) + 2.4`, was likewise chosen with an exact closed-form antiderivative so the synchronized accumulation curve is exact, not numerically estimated.
- "Thousands of thin strips" (scene 03) is a narration metaphor; the rendered strip count is tuned for visual clarity and render performance, not a literal thousand.
- The fenced-garden model assumes a straight river edge and a perfectly rectangular plot — a standard textbook simplification, not a real surveying scenario.
- `f(x) = x²`, the hill curve `f(x) = −0.35x² + 3`, and the two area-between-curves functions are chosen for clean, exact derivatives and intersections, not fitted to any measured data.
- This is Part 2 of a planned series. Part 1, **From Limits to Derivatives**, covers the material this film assumes as background: limits, continuity, and the definition of the derivative.
