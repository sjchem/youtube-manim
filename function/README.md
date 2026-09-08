# What Does a Function Actually Do?

A visual introduction to functions, with 14 Manim chapters and a **19:34 picture target**, including the 15-second end card. The central progression is:

```text
machine → flowing numbers → table → ordered pairs → graph
        → transformations → composition → inverse → input pairs and a 3D surface
```

The 66-second opening starts with large calculus expressions, then Maxwell equations, then neural networks and AI. A stronger cyan–violet nebula fills the background as these systems collapse into a glowing **3D gateway**. A rough shape passes through its moving mechanism; a vending machine, temperature gauge and neural network then show the same input–rule–output action. The gate unfolds into a table and graph before the title card: **What Does a Function Actually Do?** The applications appear at 00:25–00:29, and return in chapter 12.

Watch the [new opening preview](media/videos/scene_01_everyday_machines/480p15/Scene01EverydayMachines.mp4) or browse its [visual storyboard](output/review/gateway/index.html). The previous opening and assembled cut are preserved in `output/archive/gateway_revision/`.

## Setup

Run the commands below from this `function/` directory. The shared `../themes/` folder must also be present from the parent repository.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

You need FFmpeg and a working LaTeX installation with `standalone`, `amsmath` and `dvisvgm`. The revisions were checked with locally installed Manim Community **0.21.0**; requirements retain the existing 0.19 minimum and allow 0.21. See the [official installation guide](https://docs.manim.community/en/stable/installation.html).

## Render every scene: 480p preview and 2K final

**Preview:** 854 × 480, 15 fps. **Final:** 2560 × 1440, 30 fps, 16:9. Here “2K” means the commonly requested YouTube 1440p/QHD delivery. Cinema 2K is a different format; for a 16:9 image with 2048-pixel width, use `-r 2048,1152` instead.

Run the per-scene commands below from this `function/` directory. The 2K commands use `-p` to open the finished video and `--disable_caching` to render without reusing cached animations.

The wrapper passes resolution and frame rate explicitly. `-qh` alone would not select this 1440p final size. Manim documents these overrides in its [configuration guide](https://docs.manim.community/en/stable/guides/configuration.html).

| Scene | Start | Duration | 480p preview |
|---|---:|---:|---|
| 01 · Universal translator (3D) | 00:00 | 66 s | `python main.py preview 1` |
| 02 · Input, rule, output | 01:06 | 95 s | `python main.py preview 2` |
| 03 · Exactly one output | 02:41 | 88 s | `python main.py preview 3` |
| 04 · Domain and range | 04:09 | 82 s | `python main.py preview 4` |
| 05 · Machine to graph | 05:31 | 105 s | `python main.py preview 5` |
| 06 · Vertical line test | 07:16 | 65 s | `python main.py preview 6` |
| 07 · Transformations | 08:21 | 125 s | `python main.py preview 7` |
| 08 · Composition | 10:26 | 105 s | `python main.py preview 8` |
| 09 · Inverse | 12:11 | 115 s | `python main.py preview 9` |
| 10 · Restricting the domain | 14:06 | 80 s | `python main.py preview 10` |
| 11 · 3D input pairs and height | 15:26 | 95 s | `python main.py preview 11` |
| 12 · Applications | 17:01 | 88 s | `python main.py preview 12` |
| 13 · Payoff | 18:29 | 50 s | `python main.py preview 13` |
| 14 · End card | 19:19 | 15 s | `python main.py preview 14` |

For YouTube-style **2K output (2560 × 1440) at 30 FPS**, render every scene separately with:

```bash
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_01_everyday_machines.py Scene01EverydayMachines
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_02_the_rule.py Scene02TheRule
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_03_one_output.py Scene03OneOutput
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_04_domain_range.py Scene04DomainRange
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_05_machine_to_graph.py Scene05MachineToGraph
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_06_vertical_line_test.py Scene06VerticalLineTest
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_07_transformations.py Scene07Transformations
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_08_composition.py Scene08Composition
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_09_inverse.py Scene09Inverse
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_10_no_inverse.py Scene10NoInverse
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_11_higher_dimensions.py Scene11HigherDimensions
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_12_why_it_matters.py Scene12WhyItMatters
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_13_finale.py Scene13Finale
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_14_subscribe.py Scene14Subscribe
```

Render all chapters as separate files:

```bash
python main.py preview all
python main.py scene all
```

Once all 480p chapters exist, join them without rendering again:

```bash
python -m utils.assemble_preview
```

This verifies each chapter's size, frame rate and duration, normalizes up to three frames of encoder rounding with FFmpeg, then creates `output/function_480p_review.mp4`. It is a silent review cut assembled from standalone chapters. The generated [preview gallery](output/preview_index.html) provides individual chapter playback and narration links; open it in a browser.

Render the complete film directly as a single file:

```bash
python main.py preview full
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/full_video.py FullVideo
```

Outputs:

```text
media/videos/<scene_file_stem>/480p15/<SceneClass>.mp4
media/videos/<scene_file_stem>/1440p30/<SceneClass>.mp4
media/videos/full_video/480p15/FullVideo.mp4
media/videos/full_video/1440p30/FullVideo.mp4
```

For example, chapter 05 previews to `media/videos/scene_05_machine_to_graph/480p15/Scene05MachineToGraph.mp4`. `python main.py list` shows all class names.

Equivalent direct commands:

```bash
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_05_machine_to_graph.py Scene05MachineToGraph
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/scene_05_machine_to_graph.py Scene05MachineToGraph
python -m manim -p --resolution 2560,1440 --fps 30 --disable_caching manim_scenes/full_video.py FullVideo
```

Chapter 01 uses procedural 3D solids, a translucent gateway, rotating gears, a modelled soda bottle and a camera push toward the coin mechanism. Chapter 11 uses a real Manim `Surface`, a camera reveal, and a moving point on an illustrative loss landscape. Cairo rendering of that surface is slower than the flat chapters. No external 3D assets or plugins are required.

## Narration for ElevenLabs

Read [narration_script.md](narration_script.md) for the full script. Copy each corresponding `assets/audio/scripts/scene_XX.txt` file into your voice-generation workflow. These exports contain only spoken prose: no scene headings, LaTeX, timestamps or animation instructions. Mathematical notation is written as spoken words, such as “f of x” and “f inverse.”

1. Generate one audio file per scene using your cloned voice. Listen to scene 01 first, including its short examples and the final title question, before generating the rest.
2. Save the results as `assets/audio/scene_01.wav` through `scene_14.wav` (MP3 and M4A also work for the duration audit).
3. Run the command below to compare the actual audio durations with the picture targets. A shorter file still needs paragraph-level alignment; a duration match does not prove synchronization.
4. In your editor, align the first words of each paragraph with the matching beat in [animation_plan.md](animation_plan.md). Use pauses around predictions, coordinate swaps and the camera reveal. If speech outruns a demonstration, shorten the prose or retime the relevant scene waits.
5. Render the final picture after this audio pass, then mix the voice and music in your editor.

```bash
python -m utils.narration_export
python -m utils.narration_export --check
```

The first command refreshes the plain-text files after script edits and reports word counts, pace and any supplied audio durations. The second checks that the exports still match. **The render commands produce silent picture; they do not generate, upload or automatically attach voice audio.** The 19:34 duration is a picture target, not a claim that an unmeasured cloned voice will fit it automatically.

## Checks

```bash
python -m compileall -q main.py config.py manim_scenes utils
python -m utils.timing_audit --fps 15
python -m utils.timing_audit --fps 30
python -m utils.layout_audit --fps 15
python -m utils.narration_export --check
```

The timing audit checks authored content and the actual closing wait/fade. Large unused gaps, overruns and duration mismatches fail. Chapters end on a frame boundary so standalone and full-video cuts share the same targets.

The layout audit checks readable text bounds and overlaps at animation endpoints. It does not inspect every in-between frame, projected 3D geometry or voice synchronization; watch the preview clips for those. A last-frame render with `-s` is generally blank because these scenes end with a fade. Extract a meaningful frame from an MP4 instead:

```bash
ffmpeg -ss 27 -i media/videos/scene_01_everyday_machines/480p15/Scene01EverydayMachines.mp4 -frames:v 1 output/opening-applications.png
```

## Editorial files

- [animation_plan.md](animation_plan.md): visual beats, chapter connections and audio alignment notes.
- [narration_script.md](narration_script.md): continuous spoken script for each scene.
- [review_notes.md](review_notes.md): findings, changes and validation limits.
- [concept_summary.md](concept_summary.md): mathematical definitions and references.
- [youtube_package.md](youtube_package.md): description, chapter timestamps and clip ideas.

Gold identifies inputs, cyan the rule, and green outputs. Text, arrows and labels carry the same meaning so colour is not the only cue. Scenes introduce a concrete example before the notation and return to familiar machines after each abstraction.
