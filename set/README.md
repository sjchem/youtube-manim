# Set Theory — the pizza story

A friendly, visual Manim film: two friends want one pizza, one without meat
and one without dairy. Ingredients, fruit baskets, animal habitats, lunchboxes,
and a sorting conveyor introduce the ideas before the notation appears.

- **Planned runtime:** 21:56, across 14 chapters; the pizza opening is 48 seconds.
- **Theme:** the repository’s local `themes.oceanic_next`, using both
  `apply_oceanic_next_theme` and `oceanic_bubbles`, plus the supplied Oceanic aliases.
- **Font:** Nimbus Sans, the installed Arial substitute. Labels and equations
  share this sans-serif style. Scene 1’s closing title uses bold Nimbus Roman
  to match the supplied gold serif reference. Set `FONT_FAMILY` in `config.py`
  to Arial if installed.
- **3D chapters:** 01 (pizza), 03 (nested lunchboxes), 08 (kitchen shelf),
  and 10 (matching stencils), with real geometry and camera movement.
- **Renderer:** Manim Community Edition 0.21.0, Cairo. All illustrations are procedural.
- **Audio:** continuous scripts are ready; ElevenLabs voice generation and synchronization remain pending.

The shared visual helpers are in `manim_scenes/story_world.py`. Headings stay
above the action and one short caption occupies the bottom. Worked examples
lead to a spacious, typeset mathematical statement, following the teaching
rhythm used by the local `permu-combi` project. Scene 12 connects the subset,
union, intersection and complement rules through one membership test before
the pizza finale. Labels, captions and equations were enlarged for mobile
screens; long screen copy was shortened.

## Setup

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r set/requirements.txt
```

On Debian/Ubuntu/WSL, install the required system dependencies if needed:

```bash
sudo apt install ffmpeg libcairo2-dev libpango1.0-dev texlive texlive-latex-extra dvisvgm
```

Keep the sibling `themes/` directory in place. `config.py` adds the repository
root to the import path. `skia-pathops`, listed in requirements, supplies the
boolean region operations used in the Venn diagrams.

## Commands

```bash
cd set

python main.py list               # every chapter, its start time and duration
python main.py preview 6          # fast 480p draft of chapter 6
python main.py preview scene_10   # same, by name
python main.py preview all        # draft of every chapter, in order
python main.py preview full       # draft of the whole film
python main.py scene 10           # chapter 10 at final quality
python main.py render             # all scenes together, 2K at 30 FPS
```

### 480p previews — 15 FPS

`-pql` renders at 480p and opens the result in your player. Run from `set/`.

```bash
python -m manim -pql manim_scenes/scene_01_hook.py                Scene01Hook
python -m manim -pql manim_scenes/scene_02_what_is_a_set.py       Scene02WhatIsASet
python -m manim -pql manim_scenes/scene_03_subsets.py             Scene03Subsets
python -m manim -pql manim_scenes/scene_04_empty_set.py           Scene04EmptySet
python -m manim -pql manim_scenes/scene_05_venn.py                Scene05Venn
python -m manim -pql manim_scenes/scene_06_union_intersection.py  Scene06UnionIntersection
python -m manim -pql manim_scenes/scene_07_numbers_challenge.py   Scene07NumbersChallenge
python -m manim -pql manim_scenes/scene_08_complement.py          Scene08Complement
python -m manim -pql manim_scenes/scene_09_pizza_challenge.py     Scene09PizzaChallenge
python -m manim -pql manim_scenes/scene_10_de_morgan_one.py       Scene10DeMorganOne
python -m manim -pql manim_scenes/scene_11_de_morgan_two.py       Scene11DeMorganTwo
python -m manim -pql manim_scenes/scene_12_why_it_matters.py      Scene12WhyItMatters
python -m manim -pql manim_scenes/scene_13_finale.py              Scene13Finale
python -m manim -pql manim_scenes/scene_14_subscribe.py           Scene14Subscribe
```

### 2K renders — 2560 × 1440 at 30 FPS

Run from `set/`. Copy the whole block to render all 14 scenes sequentially,
or run any line to render just that scene. Each command saves a separate video.

```bash
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_01_hook.py                Scene01Hook
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_02_what_is_a_set.py       Scene02WhatIsASet
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_03_subsets.py             Scene03Subsets
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_04_empty_set.py           Scene04EmptySet
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_05_venn.py                Scene05Venn
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_06_union_intersection.py  Scene06UnionIntersection
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_07_numbers_challenge.py   Scene07NumbersChallenge
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_08_complement.py          Scene08Complement
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_09_pizza_challenge.py     Scene09PizzaChallenge
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_10_de_morgan_one.py       Scene10DeMorganOne
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_11_de_morgan_two.py       Scene11DeMorganTwo
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_12_why_it_matters.py      Scene12WhyItMatters
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_13_finale.py              Scene13Finale
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_14_subscribe.py           Scene14Subscribe
```

To render every scene sequentially with one command:

```bash
python main.py scene all
```

### Final render

```bash
# the whole film, 1080p at 30 FPS
python -m manim -qh --fps 30 -r 1920,1080 manim_scenes/full_video.py FullVideo

# or the project's 2K default, via main.py
python main.py render
```

Chapters 01, 03, 08 and 10 carry real 3D geometry and are the slowest to
render. Budget accordingly, and prefer `-ql` while iterating.

---

## Reviewing and checking

Current ready-made reviews:

- `output/pizza_story_visual_review.mp4` — all 14 scenes, accelerated and silent.
- `output/math_recap_720p.mp4` — the connected mathematical recap at its planned pace.
- `output/math_visual_storyboard.pdf` — each concrete example beside its rule.

```bash
# Silent, accelerated review: narration holds are removed
python -m manim -ql --fps 15 -r 854,480 manim_scenes/review_video.py ReviewVideo

# Scheduled durations and visible text at animation endpoints
python -m utils.timing_audit
python -m utils.layout_audit --motion

# Actual still frames from chapter 5
python -m utils.storyboard 5 --every 3 --out output/storyboard
```

The checks detect text collisions, clipping, and timing drift. `--motion` also
samples quarter, half, and three-quarter animation states. They cannot
establish speech alignment or certify every intermediate motion frame;
inspect the rendered review as well. `ReviewVideo` is only a visual review,
not a reference for voiceover timing.

## Narration

[narration_script.md](narration_script.md) contains the spoken master: 2,644 words,
with continuous narration for each scene. The 14 files in
[assets/audio/scripts](assets/audio/scripts) contain only spoken prose and can
be pasted individually into ElevenLabs with your cloned voice.

```bash
python -m utils.export_narration
```

The pacing CSV estimates speech at 135 words per minute. Generate and listen
to the recordings, then align the scene cues to them before the final narrated
render. Audio is not embedded automatically by the current scene code.

## Companion files

- [animation_plan.md](animation_plan.md): scene actions and planned timing.
- [concept_summary.md](concept_summary.md): mathematical examples and caveats.
- [youtube_package.md](youtube_package.md): draft title, description, and chapters.
- [review_notes.md](review_notes.md): current review deliverables and checks.

The original source and documents from before this redesign are backed up in
`output/before_story_redesign.zip`. Earlier videos and storyboards in `output/`
predate the pizza redesign; use the files named `pizza_*` for this version.
