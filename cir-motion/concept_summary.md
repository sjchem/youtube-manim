# Concept summary — Circular Motion

**Central question:** how can an object accelerate continuously when its speed
never changes?

**Central idea:** acceleration is the rate of change of the *velocity vector*.
Velocity can change in length, in direction, or both. In uniform circular
motion only the direction changes; that change always points to the centre,
so uniform circular motion needs an inward acceleration of v²/r, and therefore an
inward net force supplied by something real (tension, friction, gravity).
The chain the film teaches is *changing direction → changing velocity →
acceleration → net force*.

## One reference particle

Every mathematical chapter reuses the brief's particle
(`utils/physics_models.REFERENCE`), so the formulas read as descriptions of
one motion rather than separate facts:

| Quantity | Value | From |
|---|---|---|
| mass, radius, speed | 2 kg, 2 m, 4 m/s | given |
| angular speed | 2 rad/s | \|ω\| = v / r |
| period | π s ≈ 3.14 s | T = 2πr / v |
| frequency | ≈ 0.318 Hz | f = 1 / T |
| centripetal acceleration | 8 m/s² | a_c = v² / r |
| inward net force | 16 N | F_c = m v² / r = m r ω² |

## The science, chapter by chapter

| Chapter | Ideas | Worked numbers (all from `utils/physics_models.py`) |
|---|---|---|
| 1 Introduction | a = dv/dt; velocity changes in magnitude, direction or both; constant speed ≠ constant velocity | a car at 20 m/s on a straight road (a = 0) and on an 80 m circular track (a ≠ 0) |
| 2 Velocity and direction | v = \|v⃗\|; Δv⃗ = v⃗₂ − v⃗₁; velocity is tangent, v⃗ ⊥ r⃗; r⃗ = r cos θ î + r sin θ ĵ, θ = ωt + θ₀; v⃗ = −rω sin θ î + rω cos θ ĵ; v = r\|ω\|; one lap: distance 2πr, displacement 0, average velocity 0, average speed 2πr/T | 5î and 5ĵ: \|Δv⃗\| = 5√2 ≈ 7.07 m/s |
| 3 Why acceleration | Δv⃗ between nearby moments points inward; limit: centripetal (centre-seeking) acceleration; v⃗·a⃗ = 0; \|Δv⃗\| = 2v sin(Δθ/2) ≈ vΔθ; Δs = rΔθ = vΔt; a_c = v²/r (also from the velocity circle); doubling v quadruples a, doubling r halves it; Newton's coast-and-nudge polygon; a⃗ = −ω² r⃗ = −(v²/r) r̂, constant magnitude, turning direction | 2 sin(x/2)/x: 0.9003, 0.9745, 0.9949, 0.9997 at 90°, 45°, 20°, 5°; 4²/2 = 8 m/s²; 8 m/s → 32 m/s²; 4 m radius → 4 m/s² |
| 4 Angular motion | θ = s / r (radians), 2π rad = 360°; angular position vs displacement, counterclockwise positive; ω = dθ/dt, θ(t) = θ₀ + ωt; v = r\|ω\|; T, f = 1/T, \|ω\| = 2π/T = 2πf, v = 2πr/T; α = dω/dt; α = 0 in uniform motion while a_c ≠ 0 | turntable at 2 rad/s: 1 m → 2 m/s, 2 m → 4 m/s; T = π s, f ≈ 0.318 Hz |
| 5 Force | In uniform circular motion, F_net = m a⃗ points inward: F_c = mv²/r = mrω², a job not a new force; tension (T = mv²/r; the string snaps → tangent, Newton's first law; on a vertical circle a projectile); static friction on a level curve (v_max = √(μ_s g r), mass cancels); gravity (GMm/r² = mv²/r, v = √(GM/r), T = 2π√(r³/GM), satellites fall continuously); centrifugal force m ω² r is fictitious, belonging to the rotating frame | 16 N; r = 50 m, μ_s = 0.6: v_max ≈ 17.15 m/s ≈ 61.7 km/h (15 m/s needs 4.5 ≤ 5.88 m/s² and holds; 20 m/s needs 8 and drifts wide, on a circle no tighter than ≈ 68 m); 400 km orbit: v ≈ 7.67 km/s, g ≈ 8.7 m/s², T ≈ 92 min |
| 6 Nonuniform | uniform: v and \|ω\| constant, α = 0, acceleration purely radial; speeding up or slowing down adds a_t = dv/dt, a_θ = rα; a⃗ = −rω² r̂ + rα θ̂; \|a⃗\| = √(a_r² + a_t²); four cases: nothing, speed, direction, both | v = 4 m/s, α = 0.5 rad/s²: a_r = 8, a_t = 1, \|a⃗\| = √65 ≈ 8.06 m/s², tipped 7.1° forward of the centre |
| 7 Challenges & synthesis | the string breaks; constant speed still accelerates; double v → 4a; a satellite accelerates; α = 0 with a_c ≠ 0 | — |

## Assumptions stated on screen or in narration

* Uniform circular motion unless stated; counterclockwise is positive.
* The ball on a string: smooth horizontal table, taut massless string, the
  tension is the only horizontal force.
* The flat curve: level road, N = mg, static friction supplies the inward
  force; an idealized model, not a guide to safe driving speeds.
* The orbit: ideal circular orbit around a spherically symmetric Earth
  (GM = 3.986004418 × 10¹⁴ m³/s², mean radius 6371 km).
* The centrifugal demonstration: the passenger slides freely until the door
  reaches them (seat friction is ignored, to isolate inertia). In the rotating
  frame, centrifugal and Coriolis terms are needed while the passenger slides.

## Sources

OpenStax *University Physics Volume 1*: §4.4 (uniform circular motion,
nonuniform circular motion), §6.3 (centripetal force, banked and unbanked
curves), §10.1–10.3 (rotational variables), §13.4 (satellite orbits). NASA
Earth Fact Sheet (GM, mean radius). Newton's polygon construction:
*Principia*, Book I, Proposition 1, as presented in standard mechanics texts.
