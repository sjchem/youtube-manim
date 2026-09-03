# Scene-by-Scene Animation Plan — Visual Calculus, Part 3

Sixteen chapters, 19:51 total. The render behaves as one film, not sixteen clips: the title card arrives *inside* Chapter 1 only after the opening question has been asked, and no later chapter reopens with a numbered title.

Colour carries meaning throughout: **cyan/blue** for ordinary state and stable motion, **white** for the central object, **green** for a confirmed result, **red/orange** for restoring forces and warnings, **purple** for limits and abstraction, **muted grey** for guides.

| # | Chapter | Window | Camera | Dominant visual |
|---:|---|---|---|---|
| 01 | The reverse problem | 0:00–1:00 | flat | receding road, speedometer, twin panels |
| 02 | The missing constant | 1:00–1:45 | flat | three parabolas, parallel tangents |
| 03 | An equation about change | 1:45–2:50 | flat | three slope probes |
| 04 | The slope field | 2:50–4:26 | flat | field reveal, flowing curves |
| 05 | Exponential growth | 4:26–5:55 | flat | petri dish, growth ladder |
| 06 | Exponential decay | 5:55–7:16 | flat | vanishing particles, half-life |
| 07 | Newton's law of cooling | 7:16–8:42 | flat | mug, twin thermometers, shrinking gap |
| 08 | Separating the variables | 8:42–9:58 | flat | split screen algebra, protected equilibrium |
| 09 | Which universe are we in? | 9:58–10:52 | flat | family of curves collapsing to one |
| 10 | F = ma, and a spring | 10:52–12:42 | **3D** | spring rig, initial state, triple sync, phase helix |
| 11 | From area to volume | 12:42–14:14 | **3D** | revolution, disk stack, sphere |
| 12 | One idea, many costumes | 14:14–15:08 | flat | five differentials, one shape |
| 13 | From an equation to a future | 15:08–16:50 | **3D** | logistic field, numerical step, orbit |
| 14 | The language of modern science | 16:50–17:54 | flat | four great equations, neural ODE |
| 15 | The final revelation | 17:54–19:36 | flat | initial-value integral, the arc, the sentence |
| 16 | Subscribe | 19:36–19:51 | flat | closing card |

---

## 01 — The Reverse Problem (0:00–1:00)

**Beat 1.** A stylised night road recedes to a glowing horizon; a car drives away and shrinks into it. A speedometer fades up, its needle sweeping through most of a half-turn, captioned *ALL YOU CAN SEE*. The question **WHERE HAS IT BEEN?** lands on top.

**Beat 2.** Two x-aligned panels. Top: `v(t) = 2t` in cyan, tagged **KNOWN**. Bottom: empty, tagged **UNKNOWN**, `s(t) = ?` in gold.

**Beat 3.** A single `ValueTracker` drives three things at once: the shaded area under the velocity, the position curve drawing itself below, and a live area readout in metres. This is the film's thesis in one shot.

**Beat 4.** The panels shrink upward; three steps appear left to right — `ds/dt = 2t` → `s(t) − s(0) = ∫₀ᵗ2τ dτ` → `s(t) = s(0) + t²`. This distinguishes displacement from absolute position before naming the missing starting value as `C`.

**Beat 5.** A three-chip chain (rate of change → accumulation → the motion itself), then the hero title card.

## 02 — The Missing Constant (1:00–1:45)

`y = x²` in white; `+4` in gold and `−3` in cyan grow out of it. A dashed vertical guide drops at one `x`; three dots land on the three curves; three tangent lines are drawn — visibly parallel. Arrows from all three tags converge on a single `dy/dx = 2x`, which is pulsed. A caption asks which curve we started from; the answer transforms into `y = x² + C`, and four faint purple ghosts join the family. Then `y(0) = 3` appears with a gold marker at `(0,3)`, the family dims to 16% opacity, and one green curve survives as `y = x² + 3`.

## 03 — An Equation About Change (1:45–2:50)

The equation arrives alone, framed in purple, read aloud as *the slope equals the height*. It then shrinks to the top-left corner and axes appear. Three probes fire in sequence at heights 1, 2 and −1: a dashed guide from the axis, a glowing dot, an oversized slope tick, and a `slope = …` tag placed to the right so nothing can collide with the y-axis label. Closing couplet: *it never says where the curve is / it says how the curve is allowed to move*.

## 04 — The Slope Field (2:50–4:26)

**Beat 1.** 15 × 15 direction ticks appear one horizontal band at a time (`LaggedStart`, bottom row first), tick colour keyed to steepness. The field then dims to 30% and three individual bands are re-lit in turn — flat, steeper up, steeper down — each with its own annotation in a dedicated right-hand column.

**Beat 2.** One glowing dot is released at the left edge and `MoveAlongPath`s along the exact solution through its start point while that curve is drawn under it.

**Beat 3.** Four more seeds, four more curves, staggered. Then the equilibrium `y = 0` is drawn as a straight grey line.

**Beat 4.** Only now does `y = Ce^x` appear on a plate, followed by the wind-field line across the top (the corner equation steps aside to make room).

## 05 — Exponential Growth (4:26–5:55)

A petri dish fills with exactly 100 dots. `dP/dt = kP` writes itself on the right. The generation ladder 100 → 120 → 144 → 173 advances in step with new dots appearing in the dish, so the number and the picture are never out of sync. The dish shrinks left, axes come in, the four discrete points are marked, and the smooth `P(t) = P₀e^{kt}` is drawn through them. Everything clears for the punchline: `d/dx e^x = e^x`, framed in purple, captioned *its rate of change is itself*.

## 06 — Exponential Decay (5:55–7:16)

`+kP` and `−kN` sit side by side with a red box around the sign. Sixty particles are given individual expiry times computed from the exact solution, so the visible thinning *is* `N₀e^{−kt}` rather than an eyeballed fade. A live counter and a tracer dot run the curve alongside. Dashed half-life markers step down 60 → 30 → 15, with `t₁ᐟ₂ = ln2/k`. Three chips name the same curve in three different sciences.

## 07 — Newton's Law of Cooling (7:16–8:42)

Mug with rising steam at 90 °C, room label at 20 °C. Two thermometers whose mercury columns are redrawn from the model each frame. `dT/dt = −k(T − T_room)` writes itself, captioned *driven by the gap*. Over eleven seconds the coffee curve draws itself, a gold bar spans the shrinking gap, and a live `T − T_room` readout counts down. Two tangents — red and steep at 2 minutes, green and gentle at 30 — make the point geometrically before the closed-form solution appears.

## 08 — Separating the Variables (8:42–9:58)

`dy/dx = ky` first protects the equilibrium `y = 0`, then morphs into `(1/y)dy = k dx` for nonzero solutions. A divider separates the `y` and `x` sides; both integrate to `ln|y| = kx + C`, and `y = Ce^{kx}` emerges on a green plate. Finally `C = 0 ⇒ y = 0` visibly restores the divided-out equilibrium.

## 09 — Which Universe Are We In? (9:58–10:52)

Eight members of the family are drawn in cyan, `y = Ce^x` in the top-right corner. `y(0) = 2` appears with dashed guides and a gold marker. The family drops to 13% opacity while one green curve is drawn on top, and the corner tag transforms into `y = 2e^x`. Two lines close the chapter.

## 10 — F = ma, and a Spring (10:52–12:42) · **3D**

**Beats 1–3, flat.** `F = ma` → `a = d²x/dt²` → `m d²x/dt² = F`, framed in gold. A wall, a zig-zag spring, and a labelled mass are driven by one clock; a red arrow under the mass grows and flips with the restoring force. `F = −kx` → `m x'' = −kx` → `x'' = −(k/m)x`. The second-order equation then reveals the complete initial state: `x(0) = x₀` and `x′(0) = v₀`.

**Beat 4, flat.** One `ValueTracker` runs three synchronised views for three full periods: the sliding mass, the position–time wave, and a point circling the phase ellipse.

**Beat 5, 3D.** Everything clears, the flat background is detached, and the camera opens to `phi = 68°`. Position, velocity and time become three axes and the trajectory is drawn as a helix. `x(t) = A cos(ωt + φ)` and `ω = √(k/m)` are pinned to the frame while the camera glides through 57° of azimuth.

## 11 — From Area to Volume (12:42–14:14) · **3D**

**Beat 1, flat.** `y = √(1 − x²)` plotted and shaded.

**Beat 2, 3D.** The camera opens; the arc rotates a full turn about the x-axis, and the sphere fades in behind it. *Note:* the surface is sampled through a cosine substitution in `x`, because uniform sampling of a profile with vertical end tangents leaves one enormous band of near-edge-on quads that the Cairo renderer draws as radiating slivers.

**Beat 3.** The sphere becomes a stack of 7 gold disks; `dV = πy²dx` pins to the top. The stack refines to 14 then 28, with a corner tally showing the *actual* midpoint-sum volume at each stage.

**Beat 4.** `y² = 1 − x²` pins to the bottom, then the full integral replaces the disk rule at the top.

**Beat 5.** `V = 4π/3 ≈ 4.189`; the disks fade back into a green sphere while the camera swings to `theta = −140°`.

## 12 — One Idea, Many Costumes (14:14–15:08)

Five rows, each an icon plus a differential plus a name: area (a shaded strip), volume (a stacked cylinder), distance (an arrow over a line), mass (six dots), probability (a bell curve). Rows appear one at a time; then a gold box snaps around every formula at once and the heading transforms from *the notation changes* to *the idea does not*. Closes on `∫(tiny piece) = the whole thing`.

## 13 — From an Equation to a Future (15:08–16:50) · **3D**

**Beat 1, flat.** `dy/dt = f(y,t)` transforms into the explicit logistic rule `dy/dt = ry(1 − y/K)` in the corner.

**Beat 2, flat.** A logistic slope field fills the panel; a gold seed at `y(0)` releases a green rider that draws the S-curve while a dashed ceiling marks the carrying capacity.

**Beat 3, flat.** Four mini-panels (logistic population, cooling, oscillation, decay) fade in. The population panel matches the saturating curve just constructed.

**Beat 4, flat.** `yₙ₊₁ = yₙ + f(yₙ,tₙ)Δt` shows numerical accumulation: add the current rate times a tiny time step.

**Beat 5, 3D.** The camera opens on tilted space axes with a gold star at the origin. Initial position and velocity appear below the gravitational law. The planet follows a path **integrated with RK4 from `r'' = −μr/|r|³`**, not a decorative ellipse.

**Beat 6, flat.** *local rule → global prediction*, framed in gold.

## 14 — The Language of Modern Science (16:50–17:54)

Four cards in a 2 × 2 grid: Newton, Maxwell, Schrödinger, Navier–Stokes. Each fades up in turn; then all four are pulsed together as the heading becomes *every one of them: an equation of change*. Cut to a small feed-forward network beside `dh/dt = f(h, t; θ)`, captioned *the network learns f*.

## 15 — The Final Revelation (17:54–19:36)

The opening question returns, answered with a qualified green **yes**. The local rule `dy/dt = f(y,t)` and starting state `y(t₀) = y₀` feed into `y(t) = y₀ + ∫ₜ₀ᵗ f(y(τ),τ)dτ`: the future equals its starting state plus accumulated change. The four-chip arc assembles, three closing sentences appear, and everything clears for the final punchline and sign-off.

## 16 — Subscribe (19:36–19:51)

Thank-you line, oversized SUBSCRIBE in gold, rule, tagline, and a weekly-cadence line, with two pulses so the card is alive rather than frozen.

---

## Pacing and verification

Every chapter ends with `end_scene(scene, started, cfg.SCENE_DURATIONS[key])`, which pads or warns against the authored narration window. Three frame-free audits verify the plan without rendering video:

```bash
python utils/narration_audit.py       # 85–112 wpm per chapter, windows vs SCENE_DURATIONS
python utils/timing_audit.py --fps 15 # every chapter lands on its window
python utils/layout_audit.py --fps 5  # no text leaves frame, no text-on-text collision
```
