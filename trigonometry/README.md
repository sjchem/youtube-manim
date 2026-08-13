# Visual Trigonometry — From Triangles to Euler’s Formula

A complete Manim Community Edition project for a connected 45-minute visual trigonometry course. It begins with a heartbeat, a pendulum, and sound revealing the same repeating wave, then follows that wave back to a circle, a triangle, and trigonometry. From there it develops coordinates, Pythagoras, SOH–CAH–TOA, all six functions, special angles, the unit circle, graphs, inverse functions, identities, non-right triangles, sound, Fourier analysis, and Euler’s formula.

The complete render behaves as one film rather than seventeen presentations. One animated Oceanic background survives chapter boundaries, foreground constructions transition over it, and short corner labels replace repeated centered title cards.

## Requirements

- Python 3.12 or another version supported by Manim Community Edition
- Manim Community Edition 0.20.x
- A working LaTeX installation for `MathTex`
- FFmpeg for video output

Install from this directory:

```bash
python -m pip install -r requirements.txt
```

## Course timeline

| Chapter | Source scene | Topic | Timeline | Duration |
|---:|---|---|---|---:|
| 01 | `scene_01` | Repetition leads to trigonometry | 0:00–1:35 | 1:35 |
| 02 | `scene_02` | Angles, degrees, and radians | 1:35–3:05 | 1:30 |
| 03 | `scene_03` | Cartesian coordinates and Pythagoras | 3:05–6:05 | 3:00 |
| 04 | `scene_04` | Similar triangles and invariant ratios | 6:05–8:25 | 2:20 |
| 05 | `scene_05` | SOH–CAH–TOA and all six functions | 8:25–11:25 | 3:00 |
| 06 | `scene_06` | Exact special angles | 11:25–15:25 | 4:00 |
| 07 | `scene_07` | The complete unit-circle bridge | 15:25–17:30 | 2:05 |
| 08 | `scene_08` | Sine and cosine graphs | 17:30–20:15 | 2:45 |
| 09 | `scene_09` | Amplitude, frequency, phase, and shift | 20:15–22:10 | 1:55 |
| 10 | `scene_10` | Inverse trigonometric functions | 22:10–25:40 | 3:30 |
| 11 | `scene_11` | Identity toolkit | 25:40–30:40 | 5:00 |
| 12 | `scene_12` | Laws of sines and cosines | 30:40–34:40 | 4:00 |
| 13 | `scene_13` | Trigonometry becomes sound | 34:40–36:30 | 1:50 |
| 14 | `scene_14` | Fourier components and spectra | 36:30–41:00 | 4:30 |
| 15 | `scene_15` | Euler’s formula | 41:00–44:00 | 3:00 |
| 16 | `scene_16` | Complete synthesis | 44:00–45:00 | 1:00 |
| 17 | `scene_17` | Subscribe card | 45:00–45:15 | 0:15 |
|  |  | **Complete course** | **0:00–45:15** | **45:15** |

## Optional two-part publishing edit

The existing seventeen teaching scenes remain unchanged. Two standalone bridge clips are available for publishing the course as two shorter videos:

| Video | Edit order | Published title |
|---|---|---|
| Part 1 | Scenes 01–09, then `Scene09Part1Ending` | **Visual Trigonometry: From Triangles to Waves** |
| Part 2 | `Scene10Part2Opening`, then Scenes 10–17 | **Visual Trigonometry: From Inverse Functions to Euler’s Formula** |

The bridge clips are intentionally excluded from `full_video.py`, `main.py list`, and the seventeen-scene timing audit. Insert them manually in the two-part edit. Their clone-voice text is kept separately in `split_narration.md`.

At 15 FPS, the Part 1 ending is approximately 12.7 seconds and the Part 2 opening is approximately 16.6 seconds. These durations leave room for the supplied narration at the project’s recommended delivery speed.

Preview the two bridge clips at low quality and 15 FPS:

```bash
python -m manim -pql --fps 15 --disable_caching manim_scenes/scene_09_part_1_ending.py Scene09Part1Ending
python -m manim -pql --fps 15 --disable_caching manim_scenes/scene_10_part_2_opening.py Scene10Part2Opening
```

Render the final QHD/2K bridge clips at 2560×1440 and 30 FPS:

```bash
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_09_part_1_ending.py Scene09Part1Ending
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_10_part_2_opening.py Scene10Part2Opening
```

List the same render map from the command line:

```bash
python main.py list
```

## Fast preview rendering — `-pql`, 15 FPS

Use these commands for layout and timing checks. Remove `-p` on a headless machine. Add `--disable_caching` after changing animation timing.

```bash
python -m manim -pql --fps 15 manim_scenes/scene_01_hook.py Scene01Hook
python -m manim -pql --fps 15 manim_scenes/scene_02_angles.py Scene02Angles
python -m manim -pql --fps 15 manim_scenes/scene_03_coordinates_pythagoras.py Scene03CoordinatesPythagoras
python -m manim -pql --fps 15 manim_scenes/scene_04_ratios.py Scene04Ratios
python -m manim -pql --fps 15 manim_scenes/scene_05_six_functions.py Scene05SixFunctions
python -m manim -pql --fps 15 manim_scenes/scene_06_special_angles.py Scene06SpecialAngles
python -m manim -pql --fps 15 manim_scenes/scene_07_unit_circle.py Scene07UnitCircle
python -m manim -pql --fps 15 manim_scenes/scene_08_unrolling.py Scene08Unrolling
python -m manim -pql --fps 15 manim_scenes/scene_09_wave_controls.py Scene09WaveControls
python -m manim -pql --fps 15 manim_scenes/scene_10_inverse_trig.py Scene10InverseTrig
python -m manim -pql --fps 15 manim_scenes/scene_11_identities.py Scene11Identities
python -m manim -pql --fps 15 manim_scenes/scene_12_non_right_triangles.py Scene12NonRightTriangles
python -m manim -pql --fps 15 manim_scenes/scene_13_real_sound.py Scene13RealSound
python -m manim -pql --fps 15 manim_scenes/scene_14_fourier.py Scene14Fourier
python -m manim -pql --fps 15 manim_scenes/scene_15_euler.py Scene15Euler
python -m manim -pql --fps 15 manim_scenes/scene_16_synthesis.py Scene16Synthesis
python -m manim -pql --fps 15 manim_scenes/scene_17_subscribe.py Scene17Subscribe
```

Render the connected course at preview quality:

```bash
python -m manim -pql --fps 15 --disable_caching manim_scenes/full_video.py FullVideo
```

## YouTube QHD/“2K” — 2560×1440, 30 FPS

The recommended final master is QHD at 30 FPS:

```bash
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/full_video.py FullVideo
```

Render each chapter separately at QHD/2K and 30 FPS with the following commands. Remove `-p` when rendering on a headless machine:

```bash
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_01_hook.py Scene01Hook
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_02_angles.py Scene02Angles
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_03_coordinates_pythagoras.py Scene03CoordinatesPythagoras
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_04_ratios.py Scene04Ratios
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_05_six_functions.py Scene05SixFunctions
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_06_special_angles.py Scene06SpecialAngles
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_07_unit_circle.py Scene07UnitCircle
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_08_unrolling.py Scene08Unrolling
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_09_wave_controls.py Scene09WaveControls
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_10_inverse_trig.py Scene10InverseTrig
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_11_identities.py Scene11Identities
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_12_non_right_triangles.py Scene12NonRightTriangles
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_13_real_sound.py Scene13RealSound
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_14_fourier.py Scene14Fourier
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_15_euler.py Scene15Euler
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_16_synthesis.py Scene16Synthesis
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_17_subscribe.py Scene17Subscribe
```

Rendered files are written below `media/videos/`, grouped by source file and resolution.

## Clone-voice narration workflow

1. Open `narration_script.md` and generate one audio file from each uninterrupted chapter block.
2. Do not synthesize the Markdown heading or clip instructions.
3. Use an accessible average delivery near 104 words per minute. The opening and closing may be slightly faster or slower for emphasis.
4. Do not add an artificial ending pause to clips 01–16; each last sentence is a verbal handoff.
5. Place the clips at the exact timeline boundaries in the course table.
6. If a generated clip differs materially, adjust `SCENE_DURATIONS` in `config.py`; motion pacing recalculates automatically.

## Project structure

```text
trigonometry/
├── main.py
├── config.py
├── README.md
├── concept_summary.md
├── animation_plan.md
├── narration_script.md
├── split_narration.md
├── youtube_package.md
├── manim_scenes/
│   ├── common.py
│   ├── full_video.py
│   ├── scene_09_part_1_ending.py
│   ├── scene_10_part_2_opening.py
│   └── scene_01_*.py ... scene_17_*.py
└── utils/
```

## Validation

Run source checks without producing the full video:

```bash
python -m compileall .
python main.py list
python utils/timing_audit.py --fps 15
python utils/timing_audit.py --fps 30
git diff --check
```

The timing audit advances Manim's animation clock and final mobject states without drawing video frames. It detects both narration overruns and excessive end padding much faster than rendering the complete 45-minute course.
