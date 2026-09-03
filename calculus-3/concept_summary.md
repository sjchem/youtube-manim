# Concept Summary — Visual Calculus: From Integrals to Differential Equations (Part 3)

## Main question

Suppose we never see a function — only how fast it is changing. Can calculus reconstruct it? And can that same idea describe how real systems evolve through time?

## Core idea

1. **Integration is reconstruction.** Given velocity `v(t) = 2t`, accumulated area is displacement, not absolute position: `s(t) − s(0) = ∫₀ᵗ2τ dτ = t²`, hence `s(t) = s(0) + t²`. Rate of change → accumulation → motion, once a starting value is known.
2. **A derivative discards a constant.** `y = x² − 3`, `y = x²`, and `y = x² + 4` all have derivative `2x`; their tangents at any fixed `x` are exactly parallel. Integration cannot recover which one we began with, and `+C` is the name of that missing information.
3. **An initial condition restores it.** For the well-behaved first-order examples in the film, a rule plus one value (`y(0) = 3`) selects a single curve. Higher-order equations require a complete initial state with more values.
4. **A differential equation constrains slope, not position.** `dy/dx = y` never names a function; it demands that the slope at every point equal the height there.
5. **A slope field makes the equation visible without solving it.** Drawing the demanded direction at every grid point turns `dy/dx = y` into a field: nearly flat near `y = 0`, steepening upward above and downward below. Release a point into that field and it traces a solution; release several and the family `y = Ce^x` appears. `y = 0` is the equilibrium solution.
6. **Proportional growth produces `e`.** `dP/dt = kP` means growth feeds on current size: 100 → 120 → 144 → 173 in equal steps of ratio 1.2, smoothing into `P(t) = P₀e^{kt}` with `k = ln 1.2`. The exponential is special because `d/dx e^x = e^x` — its rate of change is itself.
7. **One sign flip gives decay.** `dN/dt = −kN` has the identical structure and the opposite behaviour: `N(t) = N₀e^{−kt}`, with a constant half-life `t₁ᐟ₂ = ln 2 / k` independent of when you start counting.
8. **Newton's law of cooling is the same equation with an offset.** `dT/dt = −k(T − T_room)`: the *gap*, not the temperature, drives the process, so cooling is fast while the gap is wide and slow once it narrows. Solution: `T(t) = T_room + (T₀ − T_room)e^{−kt}`.
9. **Separation of variables is a rearrangement, not a trick.** For `y ≠ 0`, `dy/dx = ky` becomes `(1/y)dy = k dx`; both sides integrate to `ln|y| = kx + C`. Allowing `C = 0` in `y = Ce^{kx}` restores the equilibrium solution that division temporarily excluded.
10. **Initial-value problems.** Many curves satisfy `dy/dx = y`; specifying `y(0) = 2` selects exactly `y = 2e^x`. The equation supplies the law; the initial condition supplies which world the law is acting in.
11. **Newton's second law is a differential equation.** Because `a = d²x/dt²`, `F = ma` is `m d²x/dt² = F`. Physics is written as rules of evolution rather than formulas for position.
12. **A spring turns that rule into oscillation.** Hooke's law gives `d²x/dt² = −(k/m)x`. Because this is second order, its initial state requires both position and velocity. In the ideal undamped model, `x(t) = A cos(ωt + φ)` with `ω = √(k/m)`. Position, velocity, and time trace a helix; its position–velocity shadow is a closed ellipse.
13. **Integration also builds solids.** Rotating `y = √(1 − x²)` about the x-axis sweeps out a sphere; slicing it into disks of volume `dV = πy²dx` and substituting `y² = 1 − x²` gives `V = ∫₋₁¹ π(1 − x²)dx = 4π/3`.
14. **One idea in many costumes.** `dA = f(x)dx`, `dV = πr²dx`, `ds = v(t)dt`, `dm = ρ(x)dx`, `dP = p(x)dx` — the notation changes and the idea does not: break something into tiny pieces, understand one piece, add them all back.
15. **Local rules become global predictions.** The logistic rule `dy/dt = ry(1 − y/K)` becomes a slope field whose carrying-capacity ceiling is visible before solving. For well-behaved rules, a starting state picks a trajectory. When no tidy formula exists, numerical integration repeatedly accumulates `rate × time step`; the orbit is the film's computed example.
16. **The integral form unifies the film.** `y(t) = y₀ + ∫ₜ₀ᵗ f(y(τ),τ)dτ` says that the future equals its starting state plus every prescribed local change accumulated along the path.
17. **Modern science keeps the grammar.** Newton's laws, Maxwell's equations, the Schrödinger equation, and Navier–Stokes are built from equations of change — and a neural ODE (`dh/dt = f(h, t; θ)`) learns the right-hand side rather than being handed it.

## Learning outcomes

After watching, a beginner should be able to explain:

- why integrating a rate reconstructs the quantity, and why the reconstruction is only determined up to a constant;
- what a differential equation asserts, and why it constrains slope rather than position;
- how to read a slope field, and why solution curves flow along it;
- why exponential growth and decay are the same equation with opposite signs, and where `e` comes from;
- why Newton's law of cooling is driven by a temperature difference;
- how separation of variables works and why it is a rearrangement rather than a memorised rule;
- why an initial condition is needed to pick a single solution;
- why `F = ma` is a differential equation, and how a spring's restoring force produces oscillation;
- how the disk method turns a curve into the volume of a solid.

## Numbers used on screen, and where they come from

Every displayed value is computed in `utils/math_utils.py` or `utils/physics_models.py` rather than typed into a scene:

| Quantity | Value shown | Source |
|---|---|---|
| Velocity example | `v(t) = 2t`, area over `[0,4]` = 16 m | `AcceleratingCar.area_under_velocity` (exact) |
| Growth ladder | 100, 120, 144, 173 | `discrete_growth`, ratio 1.2 |
| Growth rate | `k = ln 1.2 ≈ 0.182` per generation | `GROWTH_RATE` (exact) |
| Decay half-life | 2 time units, `k = ln 2 / 2` | `DECAY_RATE`, `half_life` (exact) |
| Coffee | 90 °C in a 20 °C room, `k = 0.05 min⁻¹` | `CoolingCup`; the gap halves in `ln 2 / k ≈ 13.9` min |
| Spring | `m = 1 kg`, `k = 4 N/m`, so `ω = 2 rad/s`, period `π s` | `SpringOscillator` (exact) |
| Sphere | `V = 4π/3 ≈ 4.189`; 28-disk stack ≈ 4.191 | `sphere_volume`, `disk_sum_volume` |
| Orbit | integrated, not drawn as a decorative ellipse | `OrbitingBody.trajectory`, fixed-step RK4 |

## Honest limits, metaphors, and approximations

- **The cooling constant is illustrative.** `k = 0.05 min⁻¹` is a plausible one-significant-figure value for a mug in still air, chosen so the curve reads well over forty minutes. It is not a calibrated measurement, and the chapter's claim is about the *shape* of the curve, not the number.
- **The slope field is a metaphor when we call it a "wind field."** The narration says so explicitly. Nothing is flowing; the arrows are the slopes the equation demands, and a solution curve is tangent to them everywhere.
- **The orbit is numerical.** The displayed Euler update communicates the core idea of stepping forward by accumulating a local rate. The rendered orbit uses the more accurate fixed-step RK4 method (`dt = 0.004`) for `r'' = −μ r/|r|³`. Over the plotted arc the total energy `v²/2 − μ/r` drifts by about one part in 10¹², and the path closes to within 0.3% of its radius.
- **The disk stack is an approximation on purpose.** The on-screen tally (7, 14, 28 disks) is a genuine midpoint sum; the chapter shows it converging to `4π/3` rather than claiming the stack equals the sphere.
- **The colony is discrete, the model is continuous.** Real organisms divide in whole numbers; `P(t) = P₀e^{kt}` is the continuous idealisation the discrete ladder is converging to. The scene shows the ladder first for exactly this reason.
- **`ln|y|` keeps its absolute value.** Separation is performed only for `y ≠ 0`; the animation explicitly protects `y = 0` before division and restores it through `C = 0` afterward.

## References

- Gilbert Strang, *Calculus* (MIT OpenCourseWare) — antiderivatives, the constant of integration, and volumes of revolution.
- Morris W. Hirsch, Stephen Smale, Robert L. Devaney, *Differential Equations, Dynamical Systems, and an Introduction to Chaos* — slope fields, equilibria, and initial-value problems.
- V. I. Arnold, *Ordinary Differential Equations* — the geometric reading of a differential equation as a direction field.
- Isaac Newton, *Philosophiæ Naturalis Principia Mathematica* — the second law as a statement about change.
- R. T. Q. Chen et al., "Neural Ordinary Differential Equations", NeurIPS 2018 — the modern-AI connection in the closing chapter.
