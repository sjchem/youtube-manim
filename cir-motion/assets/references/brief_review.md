# Review of the Episode 02 brief — Circular Motion

The brief's teaching order, derivations and worked numbers are sound, and all
33 checklist topics are covered across 26 scenes in the brief's 7 chapters.
Every number below is recomputed by `python -m utils.physics_models` and every
spoken one by `python -m utils.circle_data`.

The complete scientific brief and the accompanying visual instructions were
reviewed for this revision. The seven chapters, coverage checklist, pacing
priorities and reference particle are retained. See `../../review_notes.md`
for the scene-by-scene visual corrections and validation results.

## Corrections and clarifications made in the film

| Brief | Film |
|---|---|
| 3.1: Δv "points increasingly close to the direction toward the centre" as Δt shrinks | Made precise: for uniform motion, Δv over *any* interval points exactly at the centre as seen from the midpoint of the arc. Seen from the first moment it is off by Δθ/2, which goes to zero in the limit. Scene 07 shows both, and `physics_models.verify` checks it. |
| 3.2: \|Δv\| = 2v sin(Δθ/2), then ≈ vΔθ | Kept, with the ratio 2 sin(Δθ/2)/Δθ tabulated from the model at 90°, 45°, 20° and 5° (0.9003 → 0.9997). A second derivation is added: the velocity arrow's tip moves round a circle of radius v at the rate v/r, so a = v·(v/r). |
| 1: a car on "a circular track at 20 m/s" (radius not given) | The track radius is set to 80 m, so the car needs 5 m/s². That stays under the 5.88 m/s² that friction (μ_s = 0.6) supplies in chapter 5. A 50 m track would have contradicted the friction scene, since 20 m/s there needs 8 m/s². |
| 5.3: the car that exceeds the friction limit | With friction at its limit, the tightest bend at 20 m/s is r = v²/(μ_s g) ≈ 68 m, so the car follows a wider circle and drifts off the road. In a real skid, kinetic friction is smaller, so the path would be wider still; the narration says only "drifts wide". |
| 5.4: orbit formulas without a worked example | A circular orbit 400 km up is added (NASA GM and mean radius): v ≈ 7.67 km/s, T ≈ 92 minutes, and gravity there is still ≈ 8.7 m/s², which supports the brief's point that satellites orbit *because* gravity acts. Newton's cannon is integrated numerically (RK4); its mountain is exaggerated (0.12 Earth radii) so the shots are visible. |
| 5.5: the centrifugal force | Demonstrated with one simulation shown in both frames. The passenger slides freely until the door reaches them (seat friction is ignored), and the contact time is computed, not chosen. |
| 6.2: the brief's α = 0.5 rad/s² at v = 4 m/s | The worked numbers use exactly that instant (8, 1, √65 ≈ 8.06 m/s², 7.1° tilt). The 3D demonstration uses the same α at lower speeds (ω from 0.6 to 1.6 rad/s), so both components are visible at one common arrow scale. |
| Topic 5.2: vertical circle | Shown as a small inset: after release, gravity bends the path into a parabola. |

## Additional scientific corrections in this review

* Scene 11: the polygon's **vertices** stay on the circle; its straight chords
  pass inside it. Both the narration and scene description now distinguish these.
* Scene 19: the straight-line coasting reference uses distance `r × angle`
  at the same elapsed time, rather than the unrelated `r × tan(angle)`.
  The gravity equation is highlighted without striking through whole fractions.
* Scene 20: a passenger moving relative to the rotating car also requires a
  Coriolis term in that frame. The narration now says this explicitly; the
  diagram transforms the same ground-frame trajectory into car coordinates.
* Scene 25: acceleration and net force point wholly inward in **uniform**
  circular motion. Changing speed adds a tangential component.

Reference checks: [OpenStax, circular motion](https://openstax.org/books/university-physics-volume-1/pages/4-4-uniform-and-nonuniform-circular-motion),
[MIT, rotating frames](https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/mit8_01scs22_chapter31.pdf),
[NGA, WGS 84 constants](https://earth-info.nga.mil/index.php?action=wgs84&dir=wgs84).

## Runtime

Recommended 35–38 minutes. The film is planned at the length in
`config.SCENE_DURATIONS` (see `python main.py list`). The brief's chapter
times are a guide; chapter 3, the brief's "most important" chapter, runs
longest.
