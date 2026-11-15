# System of Particles & Rotational Motion — From Forces to Rotation

*Visualized Physics — Episode 03* · a visual lesson for students, teachers, and
curious viewers. It develops the major ideas in the NCERT chapter through
physical examples, essential derivations, and worked problems in about 40 minutes.

**Central question:** why can the same force make one object move in a straight
line, another rotate, and a third do both? The film answers it in 30 scenes
grouped into the brief's 11 YouTube chapters: centre of mass → its motion and
momentum → the cross product → torque and equilibrium → moment of inertia →
rotational kinematics → τ = Iα, work and energy → angular momentum → rolling →
a side-by-side synthesis of translation and rotation.

| File | What it is |
|---|---|
| [concept_summary.md](concept_summary.md) | The science in one page, with simplifications and metaphors named |
| [animation_plan.md](animation_plan.md) | Scene-by-scene visual plan with film timestamps (generated from the scene docstrings) |
| [narration_script.md](narration_script.md) | Full timestamped narration, clean prose (generated) |
| [narration_script_tagged.md](narration_script_tagged.md) | The same with sparse ElevenLabs v3/v4 delivery tags (generated) |
| [narration_cues.md](narration_cues.md) | Per-scene timing plan: word count, estimated speech, visual pause per beat (generated) |
| [youtube_package.md](youtube_package.md) | Titles, description with chapters, tags, thumbnail, pinned comment |

## Why Manim Community Edition, not ManimGL

The brief prefers ManimGL for 3D. ManimGL is installed (in the `youtube` pyenv
env), but the shared `../themes/oceanic_next.py` that gives every video on the
channel its look is written against Manim CE (`manim_themes`), and one
`FullVideo` render cannot mix engines. So this film is built on **Manim CE
0.22**, and its 3D comes from the projected 3D engine in
`manim_scenes/stage3d.py`: real rotating geometry with depth sorting,
perspective, lit spheres, lit boxes, lit cylinders (`Drum`) whose caps carry a
turning sector pattern, and tube-shaded rings (`Hoop`) — drawn as smooth 2D
shapes inside an ordinary `Scene`. This avoids `ThreeDScene`'s pitfalls
(faceted surfaces, fixed-in-frame text glitches) and keeps every caption crisp.

No Manim plugin is used: the wheels, doors, seesaw, skater and ramp are
simple enough that the shared stage engine draws them more cleanly than
`manim-physics` would, and every motion here is closed-form or a tiny seeded
integrator in `utils/physics_models.py`.

## Setup

```bash
# from the repository root (one level up)
pyenv activate youtube            # or any Python 3.10+ env with Manim CE 0.19–0.22
pip install -r system-particle-motion/requirements.txt
cd system-particle-motion
```

System requirements (ffmpeg, LaTeX + dvisvgm, cairo/pango, the Lato font) are
listed at the top of [requirements.txt](requirements.txt). `config.py` adds the
repository root to `sys.path`, so `themes/` imports work from this sub-folder.

## Commands

```bash
python main.py list                 # all 30 scenes with film timestamps and lengths
python main.py chapters             # the 11 YouTube chapter markers
python main.py preview 11           # fast 480p15 preview of one scene
python main.py scene 11             # one scene at 1080p30
python main.py preview all          # every scene as separate previews
python main.py preview full         # the whole film at preview quality
python main.py render               # the whole film at 1080p30 (FullVideo)
python main.py check                # every audit (see Validation)
python main.py export               # regenerate scripts, ElevenLabs text, cue sheets, animation plan
python main.py audio-check          # recorded narration vs scene lengths
```

**Final 1080p render** (one file, the whole film):

```bash
python -m manim -qh --fps 30 -r 1920,1080 manim_scenes/full_video.py FullVideo
```

Render output goes to `media/` (ignored by git); `output/` holds storyboards
and audit logs. A full 1080p render takes hours on a laptop; preview single
scenes first.

### Individual scenes — 480p previews (854 × 480, 15 fps)

```bash
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_01_hook.py Scene01Hook
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_02_rigid_bodies.py Scene02RigidBodies
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_03_two_masses.py Scene03TwoMasses
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_04_where_com.py Scene04WhereCom
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_05_many_particles.py Scene05ManyParticles
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_06_internal_forces.py Scene06InternalForces
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_07_firework.py Scene07Firework
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_08_momentum.py Scene08Momentum
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_09_cross_product.py Scene09CrossProduct
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_10_angular_velocity.py Scene10AngularVelocity
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_11_torque_door.py Scene11TorqueDoor
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_12_couple.py Scene12Couple
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_13_equilibrium.py Scene13Equilibrium
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_14_inertia.py Scene14Inertia
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_15_shapes.py Scene15Shapes
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_16_gyration.py Scene16Gyration
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_17_axis_theorems.py Scene17AxisTheorems
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_18_angular_equations.py Scene18AngularEquations
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_19_spin_up.py Scene19SpinUp
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_20_particle_motion.py Scene20ParticleMotion
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_21_tau_i_alpha.py Scene21TauIAlpha
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_22_disc.py Scene22Disc
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_23_energy.py Scene23Energy
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_24_angular_momentum.py Scene24AngularMomentum
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_25_skater.py Scene25Skater
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_26_rolling.py Scene26Rolling
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_27_rolling_energy.py Scene27RollingEnergy
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_28_race.py Scene28Race
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_29_synthesis.py Scene29Synthesis
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_30_subscribe.py Scene30Subscribe
```

### Individual scenes — 2K / 1440p (2560 × 1440, 30 fps)

```bash
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_01_hook.py Scene01Hook
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_02_rigid_bodies.py Scene02RigidBodies
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_03_two_masses.py Scene03TwoMasses
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_04_where_com.py Scene04WhereCom
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_05_many_particles.py Scene05ManyParticles
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_06_internal_forces.py Scene06InternalForces
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_07_firework.py Scene07Firework
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_08_momentum.py Scene08Momentum
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_09_cross_product.py Scene09CrossProduct
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_10_angular_velocity.py Scene10AngularVelocity
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_11_torque_door.py Scene11TorqueDoor
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_12_couple.py Scene12Couple
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_13_equilibrium.py Scene13Equilibrium
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_14_inertia.py Scene14Inertia
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_15_shapes.py Scene15Shapes
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_16_gyration.py Scene16Gyration
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_17_axis_theorems.py Scene17AxisTheorems
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_18_angular_equations.py Scene18AngularEquations
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_19_spin_up.py Scene19SpinUp
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_20_particle_motion.py Scene20ParticleMotion
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_21_tau_i_alpha.py Scene21TauIAlpha
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_22_disc.py Scene22Disc
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_23_energy.py Scene23Energy
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_24_angular_momentum.py Scene24AngularMomentum
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_25_skater.py Scene25Skater
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_26_rolling.py Scene26Rolling
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_27_rolling_energy.py Scene27RollingEnergy
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_28_race.py Scene28Race
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_29_synthesis.py Scene29Synthesis
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_30_subscribe.py Scene30Subscribe
```

For 1080p30 replace `-ql --fps 15 -r 854,480` with `-qh --fps 30 -r 1920,1080`
(or use `python main.py scene NN`).

## How the project is organised

```
system-particle-motion/
├── main.py                # CLI: list, chapters, preview, scene, render, check, export, audio-check
├── config.py              # palette (colour = meaning), fonts, render settings; durations come from narration.py
├── narration.py           # the script: (spoken text, visual hold) beats → beat times and scene lengths
├── narration_delivery.py  # sparse ElevenLabs delivery tags (each anchor must occur once in its scene)
├── manim_scenes/
│   ├── common.py          # the visual grammar: lifecycle, type, arrows, plots, bars, COM target, turn arrows,
│   │                      #   wheels, rim beads, the skater, closing card
│   ├── stage3d.py         # projected 3D engine: Stage, Ball, Rod, Block, Drum, Hoop, Solid, Grid, Curve, Dots, Vector, Tag
│   ├── scene_01_hook.py … scene_30_subscribe.py
│   └── full_video.py      # FullVideo: all 30 scenes in order, one deterministic render
├── utils/
│   ├── physics_models.py  # every worked example, the spring cluster, firework, carts, I by integration, skater, race
│   ├── rotation_data.py   # every spoken number recomputed, turned into words, found in the script
│   ├── visual_contract_audit.py  # drawn geometry obeys the physics (rolling contact at rest, v = ω × r, …)
│   ├── math_utils.py      # vectors, rotations, projection, colour
│   ├── render_helpers.py  # safe-frame fitting
│   ├── timing_audit.py    # every scene lands on its exact length (no frames rendered)
│   ├── layout_audit.py    # text collisions, frame edges, title expiry (optionally mid-animation)
│   ├── narration_audit.py # every beat is speakable in its window
│   └── narration_export.py, voiceover.py, storyboard.py, contact_sheet.py
└── assets/ (audio, images, narration, references, sounds, textures), media/, output/
```

### Rules that keep picture, voice and model in agreement

1. **No number is typed in a scene.** `utils/physics_models.py` holds every
   worked example (2 kg + 6 kg → 3 m; carts → 0.6 m/s; door 16 / 4 N m;
   seesaw 200 / 200 / 300; dumbbell 2 → 8 kg m²; wheel 8 rad/s, 16 rad,
   2.55 rev; disc I = 0.5, α = 2, K = W = 16 J; skater 4 → 2, 2 → 4 rad/s,
   8 → 16 J; ramp 3.27 / 2.45 / 4.9 m/s²). `python -m utils.rotation_data`
   checks 67 spoken numbers and 21 claims against it.
2. **Motion is the model.** The spring cluster is a velocity-Verlet run whose
   centre provably accelerates at F/M; the carts collide through a spring
   bumper and come out at −1.8 and 2.2 m/s; the firework's fragments carry
   kicks that sum to zero; the race distances are ½at² with the model's a;
   rolling bodies spin at −x/R, so the contact point really is at rest.
3. **Narration drives timing.** Each beat's window is its words at 2.65 words/s
   plus a scaled visual hold (`HOLD_SCALE`); scenes wait on
   `beat(scene, t, i)` and end with `finish()`, which keeps something moving
   to the last frame.
4. **Live objects are never `.animate`d.** Stages and the bodies on them change
   through `Param` tweens (`stage.fade`, `knob.to`, `stage.turn`) or motors
   (`drive`), never Transform copies.

## Recording the narration (ElevenLabs v4, cloned voice)

1. `python main.py export` writes `assets/narration/elevenlabs/scene_XX.txt`
   (tagged) and `assets/narration/scene_XX.txt` (clean), plus
   `narration_cues.md` and `assets/narration/cue_sheet.json`.
2. Generate one clip per scene and save it as `assets/audio/scene_XX.wav`
   (or `.mp3`), or record beats separately (`python -m utils.narration_export
   --beats`, then `assets/audio/scene_XX/beat_001.wav`, …) for cue-exact placement.
3. `python main.py audio-check` compares each clip with its scene; a clip
   longer than its window is refused rather than stretched. To retime, edit the
   holds in `narration.py` (or `HOLD_SCALE`); scene lengths and cue sheets follow.

**Pacing:** 5,476 words over 40:01 (≈ 137 words per finished minute). The brief
asks for 140–150, with fewer words where 3D, derivations or calculations need
viewing time — most chapters here do, and the 4-second live spin-up, the race
and the prediction countdown are deliberately quiet. Most scenes run at
129–141 wpm (`python -m utils.narration_audit`). `narration_cues.md` lists every beat's estimated speech and the
visual pause after it; tags such as `[pause]` guide delivery but do not fix
durations in v4, so measure the real audio and adjust holds before the final render.

## Validation

```bash
python -m compileall .              # syntax
python main.py check                # maths, physics model, spoken numbers, visual contracts, narration pace,
                                    # timing at 15 and 30 fps, FullVideo end to end, layout (mid-animation sampled)
python -m utils.storyboard 25 --every 4 && python -m utils.contact_sheet scene_25
```

## Scientific notes

* Simplifications are stated in the narration where they matter: no air
  resistance (hammer, firework), frictionless track/axle/ice, negligible seesaw
  weight, rolling without slipping, a symmetry axis whenever L = Iω is used as
  a vector (scene 24 shows the general case, where only the axial component
  equals Iω).
* The skater's arms are modelled as two 2 kg point masses plus a 1 kg m² body,
  chosen so I = 4 → 2 kg m² as in the brief; the work done by the arms is
  checked by integrating the inward pull (8 J).
* Illustrative values with no spoken numbers (the spring cluster, the scene 20
  spin-up shown in slow motion, the hammer's mass split) are labelled
  illustrative in the code.
* Sources: NCERT Physics Class XI Part I, "System of Particles and Rotational
  Motion"; Kleppner & Kolenkow, *An Introduction to Mechanics*; H. C. Verma,
  *Concepts of Physics* Vol. 1, Ch. 10. The brief is kept in
  [assets/references/brief_system_particles.txt](assets/references/brief_system_particles.txt).


## Review of this edition

The [scene review](assets/references/scene_review.md) records the scientific,
narration, and composition changes for all 30 scenes. Short diagram labels
leave explanations to the voice. Introductory scene titles fade after three
seconds. The shape gallery uses separate views, acceleration arrows focus on
one particle, and moving props and vectors are included in the frame audit.

The supplied 11-chapter outline is retained. These are editorial timings
derived from the current narration; actual voice recordings must be measured
and matched before a final render. This is a comprehensive conceptual lesson
with selected derivations, rather than every textbook exercise or derivation.
