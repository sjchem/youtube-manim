# Scene-by-Scene Animation Plan — Part 2

Target length: 17:34 (1054s). Fourteen scenes, one continuous Oceanic-themed film. Color meanings are fixed throughout: **cyan/blue** = normal state or given curve, **white** = the main object, **green** = confirmed/valid result, **red/orange** = undefined, warning, or a poor extreme, **purple** = limit/infinity/abstraction, **gold** = the value or object currently in focus, **gray/muted** = guides.

Motion rule: important constructions unfold across the narration instead of appearing in a one-second burst. Long explanation beats use slow focus passes over recent objects, live trackers, progressive strip builds, or continuous graph tracing; no chapter ends on a dead static hold. The garden uses restrained isometric depth while graph-based arguments remain in an undistorted 2D coordinate view.

## Scene 01 — Velocity Becomes Distance (0:00–1:29, `scene_01_velocity_to_distance.py`)

A rear-view car recedes along a cinematic perspective road while the question "HOW FAR DID IT GO?" appears. A flat `v = 20` velocity graph is shaded into a rectangle whose area (`20×5=100`) reveals **distance = area under the velocity graph**. The line is then morphed into a continuously wandering velocity curve, and the episode's central question appears as an unresolved integral. Only then does the title card arrive as the payoff to the hook.

## Scene 02 — Rectangles Become the Integral (1:29–2:53, `scene_02_riemann_sums.py`)

Left-endpoint Riemann rectangles are built under the velocity curve at `n = 4, 10, 50, 200`, each count replacing the last via `ReplacementTransform`. The visible gaps between rectangle and curve shrink as `n` grows; a numeric distance readout confirms convergence. `∫ₐᵇf(x)dx` is introduced and boxed as "the sum of infinitely many tiny pieces."

## Scene 03 — What dx Really Means (2:53–3:49, `scene_03_what_is_dx.py`)

One thin rectangular strip is pulled out and labeled: width `dx`, height `f(x)`, area `dA = f(x)dx`. The same curve is then filled with dozens of these strips using a dense Riemann-rectangle rendering, and the integral is restated as "add every `f(x)dx` from `a` to `b`."

## Scene 04 — The Fundamental Theorem, Revealed (3:49–5:41, `scene_04_fundamental_theorem.py`)

Two stacked, x-aligned axes: the top plots `f(x)`, the bottom plots the accumulation function `A(x) = ∫ₐˣf(t)dt`. A `ValueTracker` sweeps `x` from left to right; the area under the top curve grows via `always_redraw`, while a point on the bottom axes traces `A(x)` in lockstep. A zoomed-in thin strip shows `dA ≈ f(x)dx`, divided by `dx` and taken to the limit: `A'(x) = f(x)`, boxed in green.

## Scene 05 — f(x) = x, and a Loop That Closes (5:41–6:46, `scene_05_beautiful_example.py`)

The simplest possible worked example: the triangular area under `f(x) = x` is built with braces on its base and height, yielding `A(x) = x²/2`. Differentiating that result returns exactly `x`, and the scene closes on a three-term chain `x → x²/2 → x` with "integrate" and "differentiate" arrows.

## Scene 06 — A Derivative Is a New Function (6:46–7:57, `scene_06_derivative_new_function.py`)

A tangent line sweeps continuously along `f(x) = x²` on a top axes while a `TracedPath` draws the matching slope on a bottom axes in real time. Five marked stops (`x = −2, −1, 0, 1, 2`) read off slopes `−4, −2, 0, 2, 4`, revealing `f'(x) = 2x` as an entire function, not a single number.

## Scene 07 — Maxima and Minima (7:57–8:53, `scene_07_maxima_minima.py`)

A point crosses a hill-shaped curve `f(x) = −0.35x² + 3` while its tangent color-codes the sign of the slope (green rising, gold flat, red falling). The derivative graph beneath crosses zero at the exact instant the curve above peaks, boxed as **maximum ⇔ change switches direction**.

## Scene 08 — The Fenced-Garden Optimization (8:53–10:29, `scene_08_optimization_garden.py`)

A rectangular garden beside a river, fenced on three sides with 100 m of fencing, redraws continuously as its width `x` changes (`always_redraw`), visibly shrinking in area at both extremes. The area function `A(x) = x(100−2x)` is plotted, its derivative `A'(x) = 100−4x` is revealed, and solving `A'(x)=0` locates the maximum at `x = 25`.

## Scene 09 — Reversing the Derivative, and +C (10:29–11:43, `scene_09_reverse_problem.py`)

Given `v(t) = 2t`, integrating produces `s(t) = t² + C`. Three curves — `t²−2`, `t²`, `t²+3` — are plotted together; a vertical guide line shows all three sharing an identical slope at any chosen `t`, only their height differing. The scene closes on why differentiation destroys, and integration alone cannot recover, a function's vertical starting position.

## Scene 10 — Substitution as New Coordinates (11:43–12:53, `scene_10_substitution.py`)

`∫2x cos(x²)dx` has its `x²` term highlighted, then substituted via `u = x²`, `du = 2x dx`, collapsing into `∫cos u \, du`. A visual pairs an x-number-line with a u-number-line, connecting equally spaced x-samples to their unevenly spaced `u = x²` images — showing substitution as a nonlinear stretch of the coordinate itself.

## Scene 11 — Integration by Parts, Geometrically (12:53–14:08, `scene_11_integration_by_parts.py`)

A rectangle of sides `u` and `v` grows a thin strip on its right (`v du`) and on its top (`u dv`), plus a negligible corner (`du dv`). That geometric picture yields `d(uv) = u dv + v du`, rearranged and integrated into the boxed identity `∫u dv = uv − ∫v du`.

## Scene 12 — Area Between Curves (14:08–15:09, `scene_12_area_between_curves.py`)

Two curves `f(x)` and `g(x)` bound a region; a brace measures the vertical gap `f(x)−g(x)` at one sample point, then dense vertical strips (built via `get_riemann_rectangles` with a `bounded_graph`) fill the entire region, leading to `A = ∫ₐᵇ[f(x)−g(x)]dx`.

## Scene 13 — The Deep Connection and Final Revelation (15:09–17:19, `scene_13_synthesis.py`)

One motion, `s(t) = 0.4t² + t`, viewed two directions at once on stacked axes: a swept tangent reveals `v(t) = s'(t)`, then a growing shaded area under `v(t)` reveals accumulated displacement. Two boxed arrow-statements ("Position → differentiate → Velocity" and "Velocity → integrate → Position change") lead into both forms of the Fundamental Theorem, the closing idea ("derivatives look locally; integrals rebuild globally"), and a seven-box visual story arc from **Changing Motion** to **Fundamental Theorem**.

## Scene 14 — Subscribe (17:19–17:34, `scene_14_subscribe.py`)

Standard closing card: "THANK YOU FOR WATCHING," "SUBSCRIBE," and the tagline "Two sides of the same idea."
