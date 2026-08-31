# Scene-by-Scene Animation Plan — Part 1

Target length: 17:48 (1068s). Nine scenes, one continuous Oceanic-themed film. Color meanings are fixed throughout: **cyan/blue** = normal state or given curve, **white** = the main object, **green** = confirmed/valid result, **red/orange** = undefined or discontinuous, **purple** = limit behavior, **gold** = the value or object currently in focus, **gray/muted** = guides.

## Scene 01 — Motion Hides a Question (0:00–2:20, `scene_01_moving_car.py`)

A car and its live position-time graph `s(t) = 0.55t² + 0.4t` open the film immediately. A speedometer icon dramatizes "instant" versus the two-point average-velocity formula. Only after that mystery is established does **Visual Calculus • Part 1 • From Limits to Derivatives** appear briefly, as part of the story rather than as a cold title card. A point `P` at `t=2` and a second point `Q` at `t+h` are then connected by a secant; `h` shrinks through six steps (`1 → 0.4 → 0.15 → ... → 0.0015`) while live `h` and slope readouts update. The secant settles toward a green tangent, and the formal limit definition of `v(t)` is written.

## Scene 02 — Getting Infinitely Close (2:20–4:15, `scene_02_limits.py`)

`f(x) = x²` is plotted. A cyan dot walks in from the left (`1, 1.5, 1.9, 1.99, 1.999`) and an orange dot walks in from the right (`3, 2.5, 2.1, 2.01`), each with dashed guide lines and a live `(x, f(x))` readout. Both converge on a dashed gold target ring at `(2, 4)`. `lim(x→2) x² = 4` is revealed, followed by the scene's thesis: a limit is about heading toward, not arriving at.

## Scene 03 — A Hole in the Graph (4:15–6:25, `scene_03_hole_in_graph.py`)

`f(x) = (x²-1)/(x-1)` is shown undefined at `x=1` (`0/0`, in red). The numerator is factored and the matching `(x-1)` terms are colored and cancelled, leaving `f(x) = x+1`. The simplified line is plotted with an explicit open (hollow) hole at `(1, 2)`. Two dots approach the hole from both sides, revealing `lim(x→1) f(x) = 2` even though `f(1)` does not exist.

## Scene 04 — When the Limit Meets the Function (6:25–8:20, `scene_04_continuity.py`)

The formal definition `f continuous at a ⇔ lim(x→a) f(x) = f(a)` appears, then three miniature graphs sit side by side: a smooth parabola (green, continuous), a line with a hole (orange, not continuous), and a step jump (red, not continuous). Each is called out in turn with a caption before the closing message that continuity becomes visually obvious.

## Scene 05 — A Beautiful Trigonometric Limit (8:20–10:50, `scene_05_trig_limit.py`)

A unit-circle construction (radius scaled for visibility) shows `sin x` (cyan vertical segment), the arc `x` (gold), and `tan x` (orange segment on the tangent line) for one shrinking angle. `sin x < x < tan x` is revealed, rearranged into `cos x < sin(x)/x < 1`, and a vertical "squeeze gauge" shows both bounds sliding together toward `1` as the angle tracker shrinks toward zero. `lim(x→0) sin(x)/x = 1` is revealed in green.

## Scene 06 — From Secant to Tangent (10:50–12:58, `scene_06_secant_to_tangent.py`)

Split composition: the left side shows `f(x) = x²` with points `P` and `Q` and a live secant; the right side stacks the algebra `[(x+h)²-x²]/h → (2xh+h²)/h → 2x+h` with a live numeric readout. Both sides animate together as `h` shrinks through six steps, ending with a green tangent and the reveal `d/dx(x²) = 2x`.

## Scene 07 — The Most Powerful Visual: Local Linearity (12:58–14:48, `scene_07_local_linearity.py`)

`f(x) = x³ - x` is plotted and a point is marked with a reticle. The whole axes+curve group is scaled around that anchor point (`5× → 20× → 100× → 1000×`) inside a fixed frame, which is mathematically equivalent to zooming into a shrinking neighborhood — the curvature visibly drains away. A pre-computed green tangent (invisible until this point) fades in, coinciding exactly with the flattened curve. The local-linear approximation formula is revealed.

## Scene 08 — Derivative as Instantaneous Change (14:48–17:33, `scene_08_derivative_meaning.py`)

"SLOPE" morphs into "INSTANTANEOUS CHANGE." Four icons (car, speedometer, thermometer, population bars) reveal `ds/dt=v`, `dv/dt=a`, `dT/dt`, `dP/dt` in turn. A hill curve shows a rising point (`f'>0`, green), a falling point (`f'<0`, red), and the peak (`f'=0`, gold). The film returns to the Scene 01 car and recap secant-to-tangent shrink, then reveals the formal definition `f'(x) = lim(h→0) [f(x+h)-f(x)]/h`. The synthesis resolves into the final bridge: **Next • Part 2 • From Derivatives to Integrals**.

## Scene 09 — Subscribe (17:33–17:48, `scene_09_subscribe.py`)

Standard closing card: "THANK YOU FOR WATCHING," "SUBSCRIBE," and the exact Part 2 title.
