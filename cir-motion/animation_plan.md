# Animation plan — Circular Motion

26 scenes in the brief's 7 chapters, 37:40 in total. Generated from each scene module's docstring, so the plan cannot drift from the code. 3D scenes are drawn on the projected stage (`manim_scenes/stage3d.py`).

| Scene | Start | Length | Title | 3D |
|---|---|---|---|---|
| 01 | 00:00 | 82s | Can you accelerate without speeding up? | yes |
| 02 | 01:22 | 74s | What is acceleration? |  |
| 03 | 02:36 | 92s | Speed vs velocity |  |
| 04 | 04:08 | 68s | Which way is it moving? | yes |
| 05 | 05:16 | 91s | Velocity in components | yes |
| 06 | 06:46 | 80s | One full lap | yes |
| 07 | 08:06 | 111s | Where does delta v point? |  |
| 08 | 09:57 | 97s | The velocity triangle |  |
| 09 | 11:34 | 111s | Deriving v squared over r |  |
| 10 | 13:25 | 65s | Speed and radius | yes |
| 11 | 14:30 | 107s | Why doesn't it fall inward? |  |
| 12 | 16:17 | 108s | Angles and radians |  |
| 13 | 18:05 | 112s | Angular velocity | yes |
| 14 | 19:56 | 94s | Period and frequency |  |
| 15 | 21:30 | 58s | Angular acceleration |  |
| 16 | 22:28 | 83s | Centripetal force |  |
| 17 | 23:50 | 92s | A ball on a string | yes |
| 18 | 25:23 | 132s | Why cars need friction | yes |
| 19 | 27:34 | 124s | Why satellites orbit | yes |
| 20 | 29:38 | 93s | Is there a centrifugal force? |  |
| 21 | 31:12 | 37s | Uniform circular motion |  |
| 22 | 31:48 | 110s | Speeding up on a circle | yes |
| 23 | 33:39 | 44s | Speed, direction, or both? |  |
| 24 | 34:24 | 110s | Test your intuition |  |
| 25 | 36:14 | 77s | One chain of reasoning | yes |
| 26 | 37:30 | 10s | Stay curious |  |

## Can you accelerate without speeding up?

### 01 · Can you accelerate without speeding up? · 00:00 · 82s · 3D

`manim_scenes/scene_01_hook.py` — Scene 01 — the hook. One 3D ground holds a straight road and a circular
track. A car drives the road at a steady 20 m/s: its gold velocity arrow
never changes, so a = 0. The same car then laps the track
(``physics_models.HOOK_TRACK``) at the same 20 m/s, read off the same
speedometer, while its velocity arrow keeps turning and frozen copies are
left behind. An orange arrow toward the centre answers the hook before it
is explained. Both cars run in real time, so equal speeds cover equal
distances. The title closes the scene.

### 02 · What is acceleration? · 01:22 · 74s

`manim_scenes/scene_02_acceleration.py` — Scene 02 — what acceleration means in physics. A speedometer sweeps from
20 to 60 km/h (the everyday picture), then a = dv/dt replaces it. Velocity
is an arrow, so it can change three ways, shown in three panels: its length
grows, it turns at fixed length, or both. Then the opening's two cars return
as small diagrams: on the straight road the arrow never changes (a = 0); on
the track it keeps turning (a != 0). The key idea closes the scene.

## Velocity and direction

### 03 · Speed vs velocity · 02:36 · 92s

`manim_scenes/scene_03_speed_velocity.py` — Scene 03 — speed is the length of the velocity arrow. Two velocities from
``physics_models``: v1 = 5 i and v2 = 5 j, the same speed, different
vectors. Delta v = v2 - v1 is built tip to tail (reverse v1, add it to v2)
and measured: (-5, 5), |delta v| = 5 root 2 = 7.07 m/s. The speed changed
by nothing; the velocity by more than seven metres per second. The scene
closes on a ring of equal arrows: the same change, happening continuously.

### 04 · Which way is it moving? · 04:08 · 68s · 3D

`manim_scenes/scene_04_tangent.py` — Scene 04 — which way is it moving? The reference particle circles on a
turning 3D ground (``physics_models.REFERENCE``, played at 0.35x real time
so the eye can follow). The teal position vector runs from the centre; the
gold velocity lies along the dashed tangent, with a right-angle mark: v is
perpendicular to r. Red arrows rule out "inward" and "outward". Then the
particle keeps moving, leaving frozen velocity copies every eighth of a
lap: same speed · turning velocity.

### 05 · Velocity in components · 05:16 · 91s · 3D

`manim_scenes/scene_05_components.py` — Scene 05 — velocity in components, and the space-time helix.

Flat first: the reference particle's position r cos(theta) i + r sin(theta) j
with its blue and rose projections, and theta = omega t + theta0. Then time
becomes a third axis (as in Episode 01's space-time curve): every moment is
a point (r cos theta, r sin theta, t) and the circle stretches into a helix,
first seen face-on down the time axis, then from the side. Its shadow on the
floor is the cosine wave x(t) (blue), on the back wall the sine wave y(t)
(rose). Back to the flat view for the derivative: the velocity's blue and
rose components keep changing while its length stays r|omega|.

Stage scales: 1.25 units per metre across, 1.7 units per second along time.

### 06 · One full lap · 06:46 · 80s · 3D

`manim_scenes/scene_06_one_lap.py` — Scene 06 — one lap: distance 2 pi r, displacement zero. A runner (the
reference particle: radius 2 m, 4 m/s, a lap in pi seconds) circles a 3D
running track once. A live distance counter climbs to 2 pi r = 12.57 m
while the teal displacement arrow from the start grows, swings round and
shrinks back to nothing. Average velocity over the lap is zero; average
speed is 2 pi r / T = v. Frozen velocity arrows show the velocity turning
at every instant of the lap.

## Why circular motion requires acceleration

### 07 · Where does delta v point? · 08:06 · 111s

`manim_scenes/scene_07_delta_v.py` — Scene 07 — which way does delta v point? Two moments on the reference
circle, theta1 fixed and theta2 = theta1 + gap. Their equal-length velocities
slide to a shared tail on a workbench, and delta v runs tip to tip. Carried
back to the circle from the arc's midpoint it aims exactly at the centre
(``physics_models.verify`` checks this for any gap). Then the second moment
closes in on the first: the average acceleration delta v / delta t, drawn
from the first moment at its true size, swings onto the radius and settles
at v^2 / r. Centripetal = centre-seeking; v . a = 0.

### 08 · The velocity triangle · 09:57 · 97s

`manim_scenes/scene_08_velocity_triangle.py` — Scene 08 — the velocity triangle. On the left, the reference circle: in a
short time the radius turns through delta theta, and because v is always
perpendicular to r, the velocity turns through the same angle. On the right,
every velocity arrow is moved to one shared tail: their tips trace a circle
of radius v (the hodograph), and the live arrow goes round it in step with
the particle. Two velocities and delta v make an isosceles triangle; split
in half, |delta v| = 2 v sin(delta theta / 2). The ratio 2 sin(x/2) / x is
tabulated from ``physics_models.chord_ratio`` as the angle shrinks to 5 deg.

### 09 · Deriving v squared over r · 11:34 · 111s

`manim_scenes/scene_09_derivation.py` — Scene 09 — a = v^2 / r, derived two ways.

First by the chain in the brief: a_avg = |delta v| / delta t ~ v delta theta /
delta t; the arc delta s = r delta theta = v delta t gives delta theta /
delta t = v / r; so a = v^2 / r, toward the centre. The arc and its length
are drawn on the circle as each step is written.

Then by the velocity circle: the position arrow sweeps a circle of radius r
and its tip moves at v; the velocity arrow sweeps a circle of radius v at the
same angular rate v / r, so its tip moves at v (v / r). The orange arrow at
the velocity's tip is parallel to the inward acceleration on the left: the
speed of the velocity's tip *is* the acceleration. Finally the reference
particle's numbers: 4^2 / 2 = 8 m/s^2, at a constant 4 m/s.

### 10 · Speed and radius · 13:25 · 65s · 3D

`manim_scenes/scene_10_speed_radius.py` — Scene 10 — speed enters squared, the radius underneath. Two circuits on
one 3D ground share one clock (0.4x real time) and one scale (0.75 stage
units per metre; arrows at true magnitude). The right circuit becomes the
doubled speed (``physics_models.DOUBLE_SPEED``: 8 m/s, 32 m/s^2, four times
the orange arrow), then the doubled radius (``DOUBLE_RADIUS``: 4 m, 4 m/s^2,
half). Ghost velocity arrows after equal times show why: on the wider
circle the velocity turns more gently.

### 11 · Why doesn't it fall inward? · 14:30 · 107s

`manim_scenes/scene_11_falling_around.py` — Scene 11 — why doesn't it fall inward? Newton's construction: coast in a
straight line, then a brief nudge toward the centre, again and again. The
vertices and nudge sizes come from ``physics_models.newton_polygon`` (8, 16
and 64 sides): every vertex stays on the circle, so the vertices keep
the same radius; each intervening chord lies inside the circle, and in the limit the
polygon is the circle. Then a = -omega^2 r = -(v^2 / r) r-hat, with the
outward unit vector, and ghost copies showing that the acceleration vector
itself turns: constant magnitude, changing direction.

## Angular motion

### 12 · Angles and radians · 16:17 · 108s

`manim_scenes/scene_12_radians.py` — Scene 12 — angles and radians. A ruler measures distance on a line; on a
circle the radius sweeps an angle from a fixed direction. One radian is
built literally: a copy of the radius lifts onto the rim and bends along it.
Then theta = s / r, a full turn is 2 pi radians (six whole radii and a bit
laid round the rim), pi and pi / 2 marked, angular position vs angular
displacement, the counterclockwise-positive convention, and an accumulated
angle counter that reaches 2 pi after one lap although the particle faces
the same way it started.

### 13 · Angular velocity · 18:05 · 112s · 3D

`manim_scenes/scene_13_angular_velocity.py` — Scene 13 — angular velocity. omega = d theta / dt beside v = dr / dt, its
unit and sign, and theta(t) = theta0 + omega t drawn live as a straight line
on a small theta-t graph. Differentiating s = r theta gives v = r|omega|.
Then a 3D turntable spinning at ``physics_models.TURNTABLE_OMEGA`` (2 rad/s,
played at 0.3x): two markers 1 m and 2 m from the axis finish every turn
together, but the outer one traces the longer path. Their velocity arrows
are drawn at true length: 2 m/s and 4 m/s. The outer marker is the
reference particle: 4 / 2 = 2 rad/s.

### 14 · Period and frequency · 19:56 · 94s

`manim_scenes/scene_14_period.py` — Scene 14 — period and frequency. The reference particle laps its circle in
real time while a lap timer resets every revolution and a lap counter
climbs. T (seconds per lap) and f (laps per second, hertz) are reciprocals;
one lap sweeps 2 pi rad and covers 2 pi r, so omega = 2 pi / T = 2 pi f and
v = 2 pi r / T. For the particle: T = 2 pi (2) / 4 = pi s ~ 3.14 s (the
timer stops on it), f = 1 / pi ~ 0.318 Hz, and 2 pi f = 2 rad/s. Four tiles
close the scene: four descriptions of one motion.

### 15 · Angular acceleration · 21:30 · 58s

`manim_scenes/scene_15_angular_accel.py` — Scene 15 — angular acceleration. An omega gauge reads the reference
particle's 2 rad/s. alpha = d omega / dt; in uniform motion the needle never
moves, so alpha = 0 — yet the particle beside it carries an 8 m/s^2 orange
arrow toward the centre. Two cards separate the ideas (alpha tracks the
turning rate; a_c turns the velocity), and the needle finally starts to
climb: what happens when the particle speeds up is the next chapter.

## Centripetal acceleration and force

### 16 · Centripetal force · 22:28 · 83s

`manim_scenes/scene_16_centripetal_force.py` — Scene 16 — centripetal force. Newton's second law turns the inward
acceleration into an inward net force (green, drawn on the reference
particle beside its orange acceleration): F_c = m v^2 / r = m r omega^2,
2 (4^2) / 2 = 16 N for the 2 kg particle. Then the most important point: it
is a job, not a new force. Three small panels show who does the job:
tension (a ball on a string), friction (a car on a flat curve), gravity (a
satellite) — the same green arrow toward the centre in each.

### 17 · A ball on a string · 23:50 · 92s · 3D

`manim_scenes/scene_17_string.py` — Scene 17 — a ball on a string, on a smooth 3D table. The reference ball
(0.35x real time) circles a post; the string's green tension is the only
horizontal force, so T = m v^2 / r. Three predictions for the moment the
string snaps — straight out, keep circling, along the tangent — are drawn as
guides. Then it snaps: tension vanishes, and the ball keeps the velocity it
had at that instant, so it travels the tangent in a straight line, covering
equal distances in equal times (strobe ghosts). A 2D inset closes the scene:
on a vertical circle, gravity still acts after release, so the path is a
projectile's parabola (g = 9.8 m/s^2, from the release velocity).

### 18 · Why cars need friction · 25:23 · 132s · 3D

`manim_scenes/scene_18_car_friction.py` — Scene 18 — why cars need friction. A car laps a flat circular road of
radius 50 m (``physics_models.CURVE_RADIUS``) on a 3D ground; static
friction (green, toward the centre) is the only horizontal force. The
derivation runs down the left: N = mg, f_s <= mu_s m g, m v^2 / r <= mu_s m g,
the mass cancels, v_max = sqrt(mu_s g r) ~ 17.15 m/s ~ 61.7 km/h.

A meter compares the acceleration needed with the most friction can give
(mu_s g = 5.88 m/s^2). At 15 m/s (4.5 needed) car A holds the curve. At
20 m/s (8 needed) car B cannot: with friction at its limit, the tightest
bend it can make is r = v^2 / (mu_s g) ~ 68 m, so from its first moment on
the curve it follows that wider circle and drifts off the road. Both cars
run at 2x real time. An idealized model — not a safe-speed guide.

### 19 · Why satellites orbit · 27:34 · 124s · 3D

`manim_scenes/scene_19_satellite.py` — Scene 19 — why satellites orbit. A turning 3D Earth (a polished globe with
a meridian grid that hides behind it). Newton's cannon fires horizontally
from a tall mountain at four speeds; each path is integrated with RK4 under
inverse-square gravity (``physics_models.cannon_shot``): the first three
land farther and farther round, the fourth (circular speed) never lands.

On that orbit the satellite carries a gold tangent velocity and a green
gravity arrow; beside a dashed straight line it shows how far it has fallen.
Gravity supplies the centripetal force: GMm/r^2 = m v^2/r, the mass cancels,
v = sqrt(GM/r), and a small satellite and a big station share one orbit at
one speed. The real 400 km orbit is then drawn to scale (it hugs the
planet): v ~ 7.67 km/s, gravity still ~ 8.7 m/s^2, T ~ 92 minutes.

### 20 · Is there a centrifugal force? · 29:38 · 93s

`manim_scenes/scene_20_centrifugal.py` — Scene 20 — is there a centrifugal force? One simulation, two frames.

A car starts round a circular road; its passenger starts at the middle of
the car, moving with it. With no force on the passenger, the passenger
coasts in a straight line (inertia) until the outer door reaches them; from
then on the door pushes inward and the passenger turns with the car. The
contact moment is found numerically, not chosen.

Left: seen from the ground (not rotating) — a straight dashed path, then a
green inward push. No outward force anywhere. Right: the same numbers
transformed into the car's rotating frame — the road stands still, the
landmarks wheel round, and the passenger appears thrown outward, as if by a
centrifugal force m omega^2 r that exists only in this frame.

## Uniform vs nonuniform circular motion

### 21 · Uniform circular motion · 31:12 · 37s

`manim_scenes/scene_21_uniform.py` — Scene 21 — uniform circular motion, summarised on the reference particle:
constant speed, constant |omega|, alpha = 0, and an acceleration that is
entirely radial (v^2 / r inward) with no tangential part. Live readouts
show the speed and omega holding still while the arrows turn.

### 22 · Speeding up on a circle · 31:48 · 110s · 3D

`manim_scenes/scene_22_nonuniform.py` — Scene 22 — speeding up on a circle (3D), then the brief's numbers.

A car on a 3D track of radius 2 m speeds up with the brief's alpha = 0.5
rad/s^2 (``physics_models.SpeedingUp``), from omega = 0.6 to 1.6 rad/s,
played at 0.3x: the orange radial part grows with v^2 / r, the purple
tangential part r alpha stays fixed along the motion, and their white sum
tips forward. Slowing down (alpha = -0.5) flips the purple arrow backward.
Every arrow uses one scale, so the parallelogram is the true vector sum.

Then the brief's instant, flat: v = 4 m/s on 2 m (a_r = 8), alpha = 0.5
(a_t = 1), |a| = sqrt(65) ~ 8.06 m/s^2, tipped 7.1 degrees forward of the
centre (``physics_models.total_accel_tilt_deg``).

### 23 · Speed, direction, or both? · 33:39 · 44s

`manim_scenes/scene_23_table.py` — Scene 23 — speed, direction, or both? The brief's comparison table, one
row per beat, each with a small live icon: a straight line at constant
velocity, a straight line speeding up, uniform circular motion, and
circular motion speeding up. Columns: tangential and radial acceleration,
then what changes (nothing, speed, direction, both). One principle closes
it: a = dv/dt.

## Thought experiments and conclusion

### 24 · Test your intuition · 34:24 · 110s

`manim_scenes/scene_24_challenges.py` — Scene 24 — five conceptual challenges, each with a 3-2-1 countdown and an
animated answer: (1) the string breaks: along the tangent; (2) constant
speed round a circle: still accelerating; (3) double the speed on the same
circle: four times the acceleration (arrows at true length from
``physics_models.DOUBLE_SPEED``); (4) a satellite in an ideal circular
orbit: accelerating toward Earth's centre; (5) alpha = 0 while
a_c = v^2 / r is not.

### 25 · One chain of reasoning · 36:14 · 77s · 3D

`manim_scenes/scene_25_synthesis.py` — Scene 25 — one chain of reasoning. The opening question returns with a
constant-speed particle; then the chain builds: changing direction ->
changing velocity -> acceleration -> net force, toward the centre. The
reference particle's five descriptions are tiled round it (4 m/s, 2 rad/s,
pi s, 8 m/s^2, 16 N); the three providers of the inward force return from
scene 16; and the film closes where it began, on a 3D track, with the car's
velocity and acceleration arrows turning together.

### 26 · Stay curious · 37:30 · 10s

`manim_scenes/scene_26_subscribe.py` — Scene 26 — the channel's closing card.
