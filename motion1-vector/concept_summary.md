# Concept summary — Vectors & Projectile Motion

**Central question:** how can vectors and the laws of motion predict an
object's position, velocity and trajectory in two dimensions?

**Central idea:** a complicated 2D motion splits into two coordinate directions,
each governed by simple equations, sharing one clock. The method the film
teaches is *Motion → Vectors → Components → Equations → Prediction*.

## Teaching sequence, per topic

Physical question → intuition → definition → derivation → worked example →
physical interpretation (and the conditions under which the result applies).

## The science, chapter by chapter

| Chapter | Ideas | Worked numbers (all from `utils/physics_models.py`) |
|---|---|---|
| 1 Introduction | position, velocity, acceleration; speed ≠ velocity | two cars at 10 m/s, east and north |
| 2 Scalars & vectors | scalar = numerical value + unit (value may be negative); vector = magnitude + direction + vector addition; notation A⃗, \|A⃗\|, A_x î + A_y ĵ; distance vs displacement | 100 m / 10 s = 10 m/s; 3 m E + 4 m N: distance 7 m, displacement 5 m at 53.1° N of E; 400 m lap: displacement 0 |
| 3 Addition & subtraction | resultant; commutative, associative; triangle and parallelogram laws; R = √(A² + B² + 2AB cos φ); A⃗ − B⃗ = A⃗ + (−B⃗); Δv⃗ = v⃗_f − v⃗_i | 6 m E + 8 m N → 10 m at 53.13°; (5, 3) − (2, 1) = (3, 2); 15 m/s E → 15 m/s N: \|Δv⃗\| = 21.2 m/s, north-west |
| 4 Scalar multiple & unit vectors | k > 1, 0 < k < 1, k < 0, k = 0; F⃗ = m a⃗ (m > 0 keeps direction); Â = A⃗ / \|A⃗\| | 2(3î + 4ĵ) = 6î + 8ĵ; Â = (3/5)î + (4/5)ĵ |
| 5 Components | resolution is one vector described twice; A_x = A cos θ, A_y = A sin θ (θ from +x, signs automatic); A = √(A_x² + A_y²), θ = atan2(A_y, A_x); add by components | 10 at 30° → 8.66î + 5ĵ; (−3, 4): arctan gives −53°, atan2 gives 126.9°; (4, 3) + (−2, 5) = (2, 8), \|R\| = √68 ≈ 8.25 |
| 6 Kinematics | r⃗ = xî + yĵ; Δr⃗ unchanged by shifting the origin with fixed axes; v⃗_avg = Δr⃗/Δt, v⃗ = dr⃗/dt (tangent), speed = \|v⃗\|; a⃗ = dv⃗/dt = d²r⃗/dt² (speeding up, braking, turning); v = v₀ + at, x = x₀ + v₀t + ½at² (signed area under v–t), v² = v₀² + 2a(x − x₀); the same equations per axis | constant speed round a roundabout: velocity still changes |
| 7 Projectile motion | assumptions; a⃗ = −g ĵ (a_x = 0, a_y = −g); v₀ₓ = v₀ cos θ, v₀ᵧ = v₀ sin θ; x = v₀ cos θ t; y = v₀ sin θ t − ½gt², v_y = v₀ sin θ − gt; the top: v_y = 0 but v_x ≠ 0 and a⃗ ≠ 0; y = x tan θ − gx²/(2v₀² cos² θ) | 20 m/s at 45°: 14.14 and 14.14 m/s; x(1) = 14.14 m, x(2) = 28.28 m; y = 14.14t − 4.9t²; speed at the top 14.14 m/s (the slowest of the flight) |
| 8 Time, height, range | T = 2v₀ sin θ / g (T = 0 is the launch); rise = fall; t_H = v₀ sin θ / g; H = v₀² sin² θ / 2g; R = v₀² sin 2θ / g; maximum at 45°; complementary angles share a range | T = 2.89 s, t_H = 1.44 s, H = 10.20 m, R = 40.82 m; 30° / 45° / 60°: H 5.10 / 10.20 / 15.31 m, T 2.04 / 2.89 / 3.53 s, R 35.35 / 40.82 / 35.35 m |
| 9 Challenges & synthesis | five conceptual questions; the method generalises (orbits, fields, fluids, engineering); teaser: circular motion | dropped vs sideways from 19.6 m: both land after 2.00 s; doubling v₀ quadruples R (40.82 → 163.27 m) |

## The space-time picture (scene 23)

Plotting the flight as the curve (x(t), y(t), t) makes "eliminating t" a
camera move: seen from above it is x against t, a straight line (constant
v_x); from the side, y against t, a parabola in time (constant a_y); down the
time axis, y against x — the path. The algebra then does the same thing:
t = x / (v₀ cos θ) substituted into y(t) gives y = Ax − Bx², a quadratic in x.
The parabola is a consequence, not an assumption. (On screen y is drawn at
0.30 stage units per metre and x at 0.16, so the height reads at that size.)

## Where the ideal results stop applying

* **45° is not universal.** It maximises range only for equal launch and
  landing heights, constant g and no air.
* **Air resistance** — a foam ball (m = 0.1 kg, d = 0.1 m, C_d = 0.47,
  ρ = 1.2 kg/m³, k ≈ 0.022 m⁻¹), integrated with RK4: at 45° it lands at
  25.0 m, not 40.8 m, falls more steeply than it rises, and its best angle is
  about 41°. Only "lands short, lopsided, best angle below 45°" is spoken.
* **A 10 m ledge** — tan θ* = v₀ / √(v₀² + 2gh) gives θ* = 39.3° for
  v₀ = 20 m/s (checked against a numerical scan).
* g is treated as constant: a throw rises about 10 m, against Earth's radius
  of about 6 400 km.

## Sources

* OpenStax, *University Physics Volume 1*: ch. 2 (vectors), 3.4 (constant
  acceleration), 4.3 (projectile motion), 6.4 (drag).
* D. B. Lichtenberg and J. G. Wills, "Maximizing the range of the shot put",
  *Am. J. Phys.* 46, 546 (1978) — optimum angle from a height.
* World Athletics, *Track and Field Facilities Manual* (2019) — the 400 m track
  (84.39 m straights) used in scene 05.
