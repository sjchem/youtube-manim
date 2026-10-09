# Binomial Theorem Visualized

**Why does Pascal's triangle know algebra?** A 13-chapter Manim film (planned
running time **21:23**) that turns the expansion of $(a+b)^n$ into a counting
problem: each bracket chooses $a$ or $b$, each coefficient counts the choice
lists, and those counts are combinations, binomial coefficients and the
entries of Pascal's triangle all at once.

## Why Manim Community Edition, not ManimGL

The brief asked to prefer ManimGL. In this environment ManimGL is only
installed in the separate `youtube` pyenv environment, and the channel's shared
theme (`../themes/oceanic_next.py`, built on `manim-themes`) only works with
Manim CE. A ManimGL scene could not use the house Oceanic theme, and mixing
engines would stop `full_video.py` from rendering the film as one scene. So the
whole film uses Manim CE, with real 3D from `ThreeDScene` in chapter 3 (the
cube of $a+b$) and chapter 11 (the histogram rising out of the triangle).

## Setup

From this folder:

```bash
pip install -r requirements.txt
```

You also need FFmpeg/ffprobe, LaTeX with dvisvgm, Cairo/Pango and the Lato font
(see `requirements.txt`), plus the repository's shared `themes/` folder one
level up. `config.py` adds the repository root to `sys.path`, so the theme
imports from inside this sub-folder.

## Preview and render

```bash
python main.py list                # chapter names, start times and durations
python main.py preview 05          # one chapter at 854×480, 15 fps
python main.py preview all         # separate previews of all 13 chapters
python main.py preview full        # the full film at preview quality
python main.py scene 05            # one chapter at 1920×1080, 30 fps
python main.py render              # FullVideo at 1920×1080, 30 fps (final)
```

### Render each scene at 2K / QHD (2560×1440, 30 fps)

Run from `binomial-theorem/`. Run one line for a single scene, or paste the
whole block to render all 13 scenes sequentially as separate videos.
The explicit `-r 2560,1440` selects 2K / QHD; add `-p` to open the result.
The `main.py scene` and `main.py render` shortcuts above still use 1080p.

```bash
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_01_mystery.py Scene01Mystery
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_02_start_small.py Scene02StartSmall
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_03_cube.py Scene03Cube
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_04_triangle_builds.py Scene04TriangleBuilds
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_05_choice_machines.py Scene05ChoiceMachines
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_06_combinations.py Scene06Combinations
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_07_theorem.py Scene07Theorem
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_08_exponents.py Scene08Exponents
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_09_pascal_rule.py Scene09PascalRule
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_10_paths.py Scene10Paths
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_11_coin_flips.py Scene11CoinFlips
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_12_payoff.py Scene12Payoff
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_13_subscribe.py Scene13Subscribe
```

### Render all scenes together as one 2K video

`FullVideo` renders all 13 scenes in order into one continuous 21:23 video.

```bash
# Complete film at 2560×1440, 30 fps
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/full_video.py FullVideo

# Quick full-length preview
python -m manim -ql --fps 15 manim_scenes/full_video.py FullVideo
```

Video goes to `media/`. The two 3D chapters render slower than the flat ones
(Cairo shades each face in Python), but they use simple boxes, so the cost is
modest.

## Narration and your voice

`narration.py` is the single source of the spoken script and its beat times;
scenes hold on each beat with `beat(scene, t, i)`.

- `narration_script.md` — the readable master script, chapter by chapter, with timestamps.
- `assets/narration/scene_01.txt` … `scene_13.txt` — continuous prose to paste into a TTS tool or read aloud.
- `narration_cues.md`, `assets/narration/cue_sheet.json` — beat-by-beat timing targets.

Save recordings as `assets/audio/scene_01.wav` (or `.mp3`/`.m4a`), one per
chapter. Renders attach them automatically; a clip longer than its chapter
stops the render rather than spilling into the next chapter.

```bash
python main.py audio-check            # missing / too-long clips
python -m utils.narration_export      # regenerate the script files after editing narration.py
```

## Checks (no video rendering needed)

```bash
python main.py check                  # everything below, in order
python -m utils.math_utils            # every identity the film states, verified for n <= 12
python -m utils.physics_models        # the seeded Galton sample and the bell-curve approximation
python -m utils.narration_audit       # no beat faster than 2.75 words/s
python -m utils.timing_audit          # every chapter lands on its planned second (15 fps)
python -m utils.timing_audit --fps 30 # the same at production frame rate
python -m utils.timing_audit --full   # FullVideo end to end: chapters chain, nothing left behind
python -m utils.layout_audit          # no text off-frame, overlapping or crowding (--motion: mid-animation too)
python -m utils.storyboard 05 --every 4   # PNG stills of key layouts to output/storyboard/
```

## Design rules

- **Colour is meaning.** a = blue, b = rose, coefficients and triangle entries = gold, confirmed results = green, brute force = orange, general $n$ and the bell curve = purple, guides = muted. Heads plays a (blue), tails plays b (rose).
- **Intuition before formula.** The theorem appears at 10:36, after every symbol in it has a picture.
- **Mobile-first type.** A true 16×9 logical frame; captions, labels and equations are 30 pt Lato or larger (TeX is scaled up 1.35× to match), short, and clear of the action. The one exception is deliberate: in the 32-list grids and piles the letter cells are small pattern icons, read by their colour (rose = b), not by their letters.
- **Bright supporting text.** Highlighted equations and inactive door labels retain 80% opacity. Blue and rose symbols use brighter colours, and both letters in choice tiles have the same size. Captions stay short; explanations stay in the voiceover.
- **Nothing is typed by hand.** Every coefficient comes from `utils/math_utils.py`, which expands the brackets as choice lists and counts, and is cross-checked against `math.comb`, Pascal's rule and path counts.

## Files

```
binomial-theorem/
├── main.py                  CLI: list / preview / scene / render / check / audio-check
├── config.py                palette, fonts, frame, durations, theme setup, seed
├── narration.py             spoken script + beat times (timing source)
├── manim_scenes/
│   ├── common.py            visual grammar: machines, lists, terms, triangle, paths, coins, 3D blocks
│   ├── full_video.py        FullVideo: all 13 chapters in order
│   └── scene_01_… scene_13_ one chapter per file, each with play_scene(scene)
├── utils/
│   ├── math_utils.py        exact combinatorics + self-check
│   ├── physics_models.py    seeded coin flips / Galton board + normal approximation
│   ├── render_helpers.py    safe-frame fitting and layout grids
│   ├── timing_audit.py      layout_audit.py  storyboard.py
│   └── narration_audit.py   narration_export.py  voiceover.py
├── concept_summary.md       the mathematics, accuracy notes, references
├── animation_plan.md        chapter-by-chapter visual plan
├── narration_script.md      generated master script
├── youtube_package.md       titles, description, chapters, tags
└── assets/ media/ output/   inputs and (git-ignored) render output
```

No Manim plugin is used. Every diagram here is native Manim, and the plugins on
offer (physics, chemistry, ML, data structures) add nothing to this topic.
