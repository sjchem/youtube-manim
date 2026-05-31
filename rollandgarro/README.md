# The Hidden Science of Red Clay Tennis

A Manim educational video project answering:

**Why does the exact same tennis shot behave differently on red clay?**

The video explains how a tennis ball has two journeys: one through the air, shaped by gravity, drag, and Magnus force, and one through the court, shaped by restitution, friction, deformation, and spin transfer. The central idea is:

> Red clay changes tennis because it changes the physics of flight, bounce, spin, and time.

The project is structured to match the sibling `tennis_game_probability_video` project: scene modules live in `manim_scenes/`, utilities live in `utils/`, and the narration is separate in `narration_script.md`.

## Setup

From this folder:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Manim may require system dependencies such as Cairo, Pango, and FFmpeg.

## Render the Whole Video Together

The latest scientifically expanded combined render is [manim_scenes/full_video.py](/home/santanu/code/sjchem/youtube-manim/rollandgarro/manim_scenes/full_video.py). It stitches the separate scene files together, so edits in each scene are reflected in the combined render.

Fast preview of all chapters together:

```bash
manim -pql manim_scenes/full_video.py PreviewCompositeScene
```

Narration-paced preview, roughly 4.5 minutes:

```bash
manim -pql manim_scenes/full_video.py FinalCompositeScene
```

High quality:

```bash
manim -pqh manim_scenes/full_video.py FinalCompositeScene
```

1080p:

```bash
manim -p --format=mp4 -r 1920,1080 manim_scenes/full_video.py FinalCompositeScene
```

Legacy single-file command:

```bash
manim -pqh main.py FinalCompositeScene
```

`main.py` is kept as the original single-file draft. For the newest science-heavy scene edits, use `manim_scenes/`.

Fast structural preview using the `manim_scenes/` structure:

```bash
manim -pql manim_scenes/full_video.py PreviewCompositeScene
```

## Render Individual Scenes

High-definition render commands for each separate scene:

```bash
manim -pqh manim_scenes/scene_01_opening.py OpeningHookScene
manim -pqh manim_scenes/scene_02_air_forces.py AirForcesScene
manim -pqh manim_scenes/scene_03_spin_trajectory.py SpinTrajectoryScene
manim -pqh manim_scenes/scene_04_equation_build.py EquationBuildScene
manim -pqh manim_scenes/scene_05_bounce_physics.py BouncePhysicsScene
manim -pqh manim_scenes/scene_06_clay_friction.py ClayFrictionScene
manim -pqh manim_scenes/scene_07_rally_geometry.py RallyGeometryScene
manim -pqh manim_scenes/scene_08_living_clay.py LivingClayCourtScene
manim -pqh manim_scenes/scene_09_final_summary.py FinalSummaryScene
```

High-definition command block for rendering all separate scenes one after another:

```bash
manim -qh manim_scenes/scene_01_opening.py OpeningHookScene
manim -qh manim_scenes/scene_02_air_forces.py AirForcesScene
manim -qh manim_scenes/scene_03_spin_trajectory.py SpinTrajectoryScene
manim -qh manim_scenes/scene_04_equation_build.py EquationBuildScene
manim -qh manim_scenes/scene_05_bounce_physics.py BouncePhysicsScene
manim -qh manim_scenes/scene_06_clay_friction.py ClayFrictionScene
manim -qh manim_scenes/scene_07_rally_geometry.py RallyGeometryScene
manim -qh manim_scenes/scene_08_living_clay.py LivingClayCourtScene
manim -qh manim_scenes/scene_09_final_summary.py FinalSummaryScene
```

To print those commands from Python:

```bash
python -c "from utils.render_helpers import print_render_commands; print_render_commands()"
```

## Project Map

```text
rollandgarro/
|-- main.py                         # complete single-file Manim implementation
|-- config.py                       # shared visual and physics constants
|-- narration_script.md             # full timestamped voiceover script
|-- requirements.txt
|-- README.md
|-- manim_scenes/
|   |-- common.py
|   |-- full_video.py
|   |-- scene_01_opening.py
|   |-- scene_02_air_forces.py
|   |-- scene_03_spin_trajectory.py
|   |-- scene_04_equation_build.py
|   |-- scene_05_bounce_physics.py
|   |-- scene_06_clay_friction.py
|   |-- scene_07_rally_geometry.py
|   |-- scene_08_living_clay.py
|   `-- scene_09_final_summary.py
|-- utils/
|   |-- colors.py
|   |-- physics_models.py
|   `-- render_helpers.py
|-- assets/
|   |-- audio/
|   |-- fonts/
|   |-- images/
|   |-- references/
|   |-- sounds/
|   `-- textures/
|-- media/
`-- output/
```

Each file in `manim_scenes/` now contains its own scene class and animation code, with shared visual helpers imported from `manim_scenes/common.py`. The older `constants.py`, `helpers.py`, `physics_models.py`, and `scenes/` files are lightweight compatibility/refactor helpers from the first draft. The recommended render path is now `main.py` or `manim_scenes/`.

## Video Concept

Core idea: a tennis shot is not finished when the racket hits the ball. It first travels through air, where gravity, drag, and spin-induced Magnus force reshape its arc. Then it hits the court, where coefficient of restitution, friction impulse, clay deformation, energy loss, and spin transfer rewrite the bounce.

Central metaphor:

> The ball has two journeys: one through the air, and one through the earth.

Scientific payoff: the viewer learns to see the court not as a passive floor, but as an invisible player.

Tennis payoff: clay slows the ball, raises the bounce, rewards topspin, enables sliding, lengthens rallies, and rewards tactical construction.

## Scene Breakdown

1. `OpeningHookScene`: same shot on hard court and clay, with different outcomes.
2. `AirForcesScene`: gravity, drag, velocity, and Magnus arrows around a spinning ball.
3. `SpinTrajectoryScene`: topspin, flat, and backspin trajectories.
4. `EquationBuildScene`: force model with visual term-by-term explanation.
5. `BouncePhysicsScene`: hard court vs clay collision, restitution, and friction impulse.
6. `ClayFrictionScene`: close-up topspin kick with dust and grip arrows.
7. `RallyGeometryScene`: top-down tactical geometry, sliding, angles, and patience.
8. `LivingClayCourtScene`: moisture, rolling, dryness, and loose particles.
9. `FinalSummaryScene`: AIR, SPIN, FRICTION, CLAY final synthesis.

The `manim_scenes/` versions now include extra scientific overlays: clay layer structure, friction and speed-retention coefficients, drag/lift coefficient bars, boundary-layer airflow lines, Magnus-force direction labels, contact impulse diagrams, spin-transfer notes, sliding mechanics, and moisture/maintenance effects.

## Physics Model

The code uses a simplified but directionally correct visual model:

```text
m dv/dt = mg + F_d + F_M
F_d = -1/2 rho C_d A |v| v
F_M ~= S (omega x v)
```

Bounce model:

```text
v_y_after = -e v_y_before
v_x_after = alpha v_x_before
omega_after = beta omega_before + gamma v_x_before
```

For clay, `alpha` is smaller, meaning more horizontal speed loss. Clay also uses more dust particles and a stronger topspin kick visual.

## Visual Design

- Background: near black / deep navy
- Clay: burnt red / terracotta
- Hard court: blue-green
- Ball: neon yellow-green
- Gravity: white
- Drag: red
- Magnus: cyan
- Friction: orange
- Velocity: yellow
- Equation text: off-white
- Highlights: gold

The design uses procedural Manim primitives only. No copyrighted footage or external media is required.

## References

- AMbelievable, "The Science and Secrets of Red Clay Courts": https://www.ambelievable.com/blog/tennis-dampener-the-blog-1/the-science-and-secrets-of-red-clay-courts-27
- Tennis Warehouse University, "The Physics of Tennis: Tennis Ball Trajectories": https://twu.tennis-warehouse.com/learning_center/aerodynamics2.php

## Quality Checklist

- Drag opposes velocity.
- Magnus force depends on spin and velocity.
- Bounce separates normal restitution and tangential friction.
- Clay shows more horizontal speed loss than hard court.
- Topspin kick is visually connected to clay grip.
- Equations appear after the intuition.
- Labels remain readable.
- The complete video can be checked with `FinalCompositeScene`.
