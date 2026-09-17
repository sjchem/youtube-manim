# Permutations & Combinations Explained Visually

A 27½-minute visual mathematics film built with **Manim Community Edition**,
answering one question: *when I rearrange the same objects, have I created
something new?*

See [review_notes.md](review_notes.md) for the storytelling and accuracy review,
and [narration_script.md](narration_script.md) for the continuous recording script.

It starts with an order-sensitive combination lock, builds up to 2,598,960
poker hands, and returns to the lock beside an unchanged team. Pictures lead
the formulas, and each chapter has a continuous spoken narration passage.

* **Runtime:** 26:45 across 14 chapters
* **Theme:** local Oceanic Next (`themes/oceanic_next.py` in the repo root)
* **3D chapters:** 01 (padlock), 04 (podium), 11 (card cloud) — real
  `ThreeDScene` geometry and camera motion
* **Renderer:** Manim CE 0.19.2, Cairo

> **Why Manim CE and not ManimGL?** The repo's Oceanic Next theme imports
> `manim` (Community Edition) and is shared with every other project here, and
> `manimlib` is not importable in this environment. The three-dimensional
> chapters therefore use CE's `ThreeDScene` with genuine 3D mobjects — a
> `Prism` padlock body, `Cylinder` digit wheels, a half-`Torus` shackle,
> `Prism` podium blocks, and a depth-sorted card cloud — rather than painted
> fakes.

---

## Setup

```bash
# from the repository root
python -m venv .venv && source .venv/bin/activate
pip install -r permu-combi/requirements.txt
```

Manim also needs system packages that pip cannot install — `ffmpeg`, a LaTeX
distribution with `dvisvgm`, and the cairo/pango headers. On Debian, Ubuntu or
WSL:

```bash
sudo apt install ffmpeg libcairo2-dev libpango1.0-dev texlive texlive-latex-extra dvisvgm
```

Imports work from inside the project folder: `config.py` puts both the project
directory and the repository root on `sys.path`, so `from themes.oceanic_next
import ...` resolves without installing anything.

---

## Commands

```bash
cd permu-combi

python main.py list               # every chapter, its start time and duration
python main.py preview 6          # fast 480p draft of chapter 6
python main.py preview scene_04   # same, by name
python main.py preview all        # draft of every chapter, in order
python main.py preview full       # draft of the whole film
python main.py scene 9            # chapter 9 at final quality
python main.py render             # all scenes together, 2K at 30 FPS
```

### 480p previews — 15 FPS

All fourteen scene preview commands are grouped below. `-pql` renders at 480p
and opens the finished preview in your video player. Run from `permu-combi/`.

```bash
python -m manim -pql --fps 15 manim_scenes/scene_01_lock_paradox.py Scene01LockParadox
python -m manim -pql --fps 15 manim_scenes/scene_02_choices_multiply.py Scene02ChoicesMultiply
python -m manim -pql --fps 15 manim_scenes/scene_03_factorial.py Scene03Factorial
python -m manim -pql --fps 15 manim_scenes/scene_04_permutations.py Scene04Permutations
python -m manim -pql --fps 15 manim_scenes/scene_05_order_matters.py Scene05OrderMatters
python -m manim -pql --fps 15 manim_scenes/scene_06_block_gap.py Scene06BlockGap
python -m manim -pql --fps 15 manim_scenes/scene_07_combinations.py Scene07Combinations
python -m manim -pql --fps 15 manim_scenes/scene_08_quiz.py Scene08Quiz
python -m manim -pql --fps 15 manim_scenes/scene_09_alike_geometry.py Scene09AlikeGeometry
python -m manim -pql --fps 15 manim_scenes/scene_10_symmetry.py Scene10Symmetry
python -m manim -pql --fps 15 manim_scenes/scene_11_poker.py Scene11Poker
python -m manim -pql --fps 15 manim_scenes/scene_12_zero_factorial.py Scene12ZeroFactorial
python -m manim -pql --fps 15 manim_scenes/scene_13_finale.py Scene13Finale
python -m manim -pql --fps 15 manim_scenes/scene_14_subscribe.py Scene14Subscribe
```

To preview all scenes together as one continuous video:

```bash
python -m manim -pql --fps 15 manim_scenes/full_video.py FullVideo
```

### 2K renders — 2560 × 1440, 30 FPS

All fourteen individual scene render commands are grouped below. The explicit
resolution overrides the `-qh` preset.

```bash
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_01_lock_paradox.py Scene01LockParadox
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_02_choices_multiply.py Scene02ChoicesMultiply
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_03_factorial.py Scene03Factorial
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_04_permutations.py Scene04Permutations
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_05_order_matters.py Scene05OrderMatters
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_06_block_gap.py Scene06BlockGap
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_07_combinations.py Scene07Combinations
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_08_quiz.py Scene08Quiz
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_09_alike_geometry.py Scene09AlikeGeometry
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_10_symmetry.py Scene10Symmetry
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_11_poker.py Scene11Poker
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_12_zero_factorial.py Scene12ZeroFactorial
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_13_finale.py Scene13Finale
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_14_subscribe.py Scene14Subscribe
```

### All scenes together — one 2K video

Render all fourteen scenes in story order into a single `FullVideo.mp4`:

```bash
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/full_video.py FullVideo
```

Or use the project shortcut, which uses the same 2560 × 1440, 30 FPS settings:

```bash
python main.py render
```

The combined video is written under `media/videos/full_video/1440p30/`.
Expect a long render for the full 26:45 film, including its three 3D chapters.

For a still image, replace `-pql` with `-ql -s`, or add `-s` to a 2K command.

---

## Checking the film without rendering it

These checks verify arithmetic, chapter duration and text bounds. Storyboard
stills support visual review; they do not replace watching motion with the
recorded narration.

```bash
python -m utils.math_utils        # every count, checked against brute force
python -m utils.counting_models   # Pascal rows, overcount maps, Monte-Carlo check
python -m utils.timing_audit      # each chapter lands exactly on its target second
python -m utils.layout_audit      # nothing leaves the frame, no text overlaps text
python -m utils.narration_export  # per-scene narration files and words-per-minute
python -m utils.narration_export --check  # validate ranges and catch stale exports
python -m utils.storyboard 6      # PNG stills of chapter 6's distinct layouts
```

`timing_audit` and `layout_audit` drive the real scenes through a renderer that
advances Manim's clock and mobject state without rasterising frames, so a
27½-minute film can be checked without encoding a video. The first run may take
longer while LaTeX builds its cache. The layout audit checks animation end
states, not every intermediate frame or projected 3D occlusion.

---

## Layout of the project

```
permu-combi/
├── main.py                     # list / preview / scene / render
├── config.py                   # palette, fonts, frame, durations, theme hook
├── requirements.txt
├── README.md
├── concept_summary.md          # the mathematics, and where metaphors are metaphors
├── animation_plan.md           # chapter-by-chapter plan and the visual grammar
├── narration_script.md         # continuous prose with chapter time ranges
├── youtube_package.md          # title, description, chapters, tags, thumbnail
├── manim_scenes/
│   ├── common.py               # the shared visual language (chips, slots, rings)
│   ├── props_3d.py             # padlock, podium, card cloud
│   ├── full_video.py           # the fourteen chapters, chained in story order
│   └── scene_01..scene_14      # one sequential module per chapter; subscribe is 14
├── utils/
│   ├── math_utils.py           # exact counts, verified
│   ├── counting_models.py      # Pascal rows, growth, overcount maps, sampler
│   ├── render_helpers.py       # safe-frame and layout helpers
│   ├── timing_audit.py         # pacing, without rendering frames
│   ├── layout_audit.py         # overlap and frame-boundary checks
│   ├── storyboard.py           # still frames of each composition
│   └── narration_export.py     # per-scene narration + words per minute
├── assets/{audio,images,references,sounds,textures}/
├── media/                      # Manim's render output (git-ignored)
└── output/                     # storyboards and exports (git-ignored)
```

---

## Adding narration audio

1. Record or synthesise each chapter from `assets/audio/scripts/scene_XX.txt`
   (regenerate those with `python -m utils.narration_export`).
2. Drop the results in `assets/audio/` using the matching scene numbers.
3. Re-run `python -m utils.narration_export`. It reports each file's real
   duration against the chapter budget and flags anything too long.
4. Align the recording to the cue windows in `animation_plan.md`, keeping the
   quiz countdowns silent. Word counts estimate pace; they cannot verify that
   a spoken phrase coincides with a particular animation.
5. Add these recordings in your video editor or mux them with `ffmpeg` at the
   chapter start times. The current scenes do not automatically load audio.
   Word-level synchronisation would need a separate voiceover integration.

The chapter durations in `config.SCENE_DURATIONS` are the contract: `end_scene`
raises rather than let a chapter drift past its slot. Match the recorded
phrases to the scene cues separately; chapter length alone cannot guarantee
speech-to-animation synchronization.

---

## Mathematics covered

Addition and multiplication principles · `4! = 24` · `nPr = n!/(n−r)!` ·
block and gap methods · `nCr = n!/(r!(n−r)!)` · alike objects · polygon
diagonals · `10C3 = 10C7 = 120` · `52C5 = 2,598,960` · `0! = 1`

The PIN example briefly contrasts repetition (`10^4`) with a shrinking pool.
Deliberately out of scope, each worth its own film: combinations with
repetition, circular arrangements, derangements, distributions, divisor
counting, and the binomial theorem. See `concept_summary.md` for the full
statement of what is proved, what is shown, and what is only a metaphor.
