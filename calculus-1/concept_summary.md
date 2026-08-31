# Concept Summary — Visual Calculus: From Limits to Derivatives (Part 1)

## Main question

How can mathematics measure what is happening at one exact instant, when every ordinary measurement needs an interval to compare two moments against each other?

## Core idea

Calculus bridges the gap between average change and instantaneous change by asking what an average keeps approaching as its interval shrinks toward zero:

1. Average velocity needs two moments: `Δx / Δt`.
2. Connecting those two moments on a graph draws a secant line.
3. Shrinking the interval `h` rotates the secant toward one special line: the tangent.
4. Formalizing "shrinks toward zero" is the idea of a **limit**.
5. A limit describes the value a function is heading toward — it does not require the function to be defined, or even continuous, at that exact point (the removable hole in `(x²-1)/(x-1)`).
6. **Continuity** is the special case where the limit and the function's actual value agree from both sides.
7. The squeeze theorem proves `lim(x→0) sin(x)/x = 1` by trapping the ratio between `cos x` and `1`.
8. Repeating the secant-to-tangent construction algebraically on `f(x) = x²` produces the derivative `2x` — the same idea, now built by hand.
9. **Local linearity**: zooming into any differentiable curve makes it visually indistinguishable from its tangent line. That line is the local linear model; the derivative is its slope.
10. The derivative is not fundamentally a slope; slope is its picture. The same construction gives velocity, acceleration, rates of temperature change, and rates of population growth.

## Learning outcomes

After watching, a beginner should be able to explain:

- why average velocity cannot answer "how fast right now?" without first taking a limit;
- what a secant line is, and how shrinking `h` turns it into a tangent line;
- that a limit describes the value a function approaches, not necessarily its value at that point;
- how to evaluate a limit at a removable discontinuity by factoring and canceling;
- the three-part condition for continuity at a point, and how to recognize a smooth curve, a hole, and a jump;
- how the squeeze theorem proves `lim(x→0) sin(x)/x = 1` from `sin x < x < tan x`;
- how to derive `d/dx(x²) = 2x` from the secant-slope definition;
- why local linearity — "every smooth curve looks straight if you zoom in far enough" — is the geometric meaning of a derivative;
- that a derivative is instantaneous change in general, with slope, velocity, acceleration, and growth rate as its many disguises;
- the formal definition `f'(x) = lim(h→0) [f(x+h) - f(x)] / h`.

## Accuracy boundaries

- The car's motion model, `s(t) = 0.55t² + 0.4t`, is a simplified illustrative model of gentle constant acceleration, not a measured real-world trajectory.
- The `sin x < x < tan x` comparison is the standard first-quarter geometric argument (valid for `0 < x < π/2`); it is not extended here to negative or non-acute angles, since `sin(x)/x` is an even function and the same limit follows by symmetry.
- The local-linearity zoom scales an already-plotted curve uniformly about a fixed anchor point inside a fixed-size viewing frame; this is mathematically equivalent to zooming into a shrinking neighborhood, since the curve's quadratic (curvature) term shrinks relative to its linear term as the scale factor grows.
- "Derivative as instantaneous change" is presented through several classic modeling metaphors (velocity, acceleration, temperature, population); these illustrate the mathematical pattern `dQ/dt` and are not drawn from measured data.
- This is Part 1 of a planned series. Part 2, **From Derivatives to Integrals**, continues into accumulation, area, antiderivatives, and the Fundamental Theorem of Calculus.
