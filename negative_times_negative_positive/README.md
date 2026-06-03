# Why Two Negatives Make a Positive

A cinematic Manim Community Edition project explaining why multiplying two negative numbers gives a positive result. The video moves from intuition to structure:

- negative signs as direction reversal
- multiplication patterns continuing through zero
- the distributive law forcing `(-a)(-b)=ab`

The project avoids external image dependencies and uses generated equations, particles, arrows, number lines, graph lines, mirrors, and a balance-scale proof.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Manim also needs a working LaTeX installation and FFmpeg. On Ubuntu/Debian:

```bash
sudo apt install ffmpeg texlive texlive-latex-extra texlive-fonts-extra
```

## List Scenes

```bash
python main.py list
```

## Quick Preview

```bash
python main.py preview 01
python main.py preview 06
python main.py preview full
```

## Render One Scene

```bash
python main.py render 03 --quality high
```

Equivalent direct Manim command:

```bash
manim -qh manim_scenes/scene_03.py Scene03NegativeAsReversal
```

## Render All Individual Scenes

```bash
manim -qh manim_scenes/scene_01.py Scene01ColdOpen
manim -qh manim_scenes/scene_02.py Scene02MultiplicationAsMotion
manim -qh manim_scenes/scene_03.py Scene03NegativeAsReversal
manim -qh manim_scenes/scene_04.py Scene04MirrorRoom
manim -qh manim_scenes/scene_05.py Scene05PatternThroughZero
manim -qh manim_scenes/scene_06.py Scene06DistributiveLawMachine
manim -qh manim_scenes/scene_07.py Scene07BrokenUniverse
manim -qh manim_scenes/scene_08.py Scene08FinalSynthesis
```

## Final 1080p Render

```bash
python main.py full --quality high
```

Direct command:

```bash
manim -qh manim_scenes/full_video.py FullVideo
```

For 4K production:

```bash
python main.py full --quality production
```

## Adjusting Narration Pace

The project uses `TIMING["pace_scale"]` in `config.py` to slow down or speed up scene animation timing globally. Increase it for more narration room, or decrease it for a tighter edit.

## Project Structure

```text
negative_times_negative_positive/
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── narration_script.md
├── concept_summary.md
├── animation_plan.md
├── youtube_package.md
├── manim_scenes/
├── utils/
├── assets/
├── media/
└── output/
```

## Adding Narration And Audio

Record voiceover from `narration_script.md`, then place WAV or MP3 files in `assets/audio/`. The scene files include natural pause points where sound cues can be added later with Manim's `self.add_sound(...)`.

Suggested workflow:

1. Render the full silent video.
2. Record narration scene by scene.
3. Edit timing in a video editor or add scene-level `add_sound` calls.
4. Add subtle low-volume music and short sign-change sound cues.

## Troubleshooting

- `ModuleNotFoundError: manim`: activate the virtual environment and reinstall requirements.
- LaTeX errors: install a fuller TeX distribution such as `texlive-latex-extra`.
- Slow render: use `--quality preview` while editing.
- Font differences: Manim uses system fonts; visual spacing can shift slightly across machines.
