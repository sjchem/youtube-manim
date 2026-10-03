# The Periodic Table, Explained Visually

**Why does the periodic table have this strange shape?** Atomic Structure, Part 3.

A 16-scene Manim film connects the orbitals in [Part 2](../atomic-structure-2/) to electron configurations, block widths, repeating groups, and chemical behaviour. The planned running time is **22:43**; the final pacing should be checked against your recorded voice.

## Preview and render

From this folder, install `requirements.txt`. The project also uses the repository's shared `themes/oceanic_next.py`, FFmpeg/ffprobe, LaTeX/dvisvgm, Cairo/Pango, and the Lato font.

```bash
python main.py list                # scene names, start times and durations
python main.py preview 06          # one scene at 854×480, 15 fps
python main.py preview all         # separate previews of all 16 scenes
python main.py preview full        # the full film at preview quality
python main.py scene 06            # one scene at 1920×1080, 30 fps
python main.py render              # FullVideo at 1920×1080, 30 fps
```

## Direct Manim commands for every scene

Run these commands from `periodic-table/`. Each command includes the complete Python filename and scene class, so Manim renders the intended scene without asking you to select it.

Paste a whole block to render all 16 scenes sequentially as separate video files. `-p` opens each finished video in your default player; use `-ql` or `-qp` instead of `-pql` or `-pqp` to render without opening the player.

### All scenes at 480p — 854×480, 15 fps

```bash
python -m manim -pql --fps 15 manim_scenes/scene_01_hook.py Scene01Hook
python -m manim -pql --fps 15 manim_scenes/scene_02_atomic_number.py Scene02AtomicNumber
python -m manim -pql --fps 15 manim_scenes/scene_03_electrons.py Scene03Electrons
python -m manim -pql --fps 15 manim_scenes/scene_04_four_shapes.py Scene04FourShapes
python -m manim -pql --fps 15 manim_scenes/scene_05_period_one.py Scene05PeriodOne
python -m manim -pql --fps 15 manim_scenes/scene_06_period_two.py Scene06PeriodTwo
python -m manim -pql --fps 15 manim_scenes/scene_07_groups.py Scene07Groups
python -m manim -pql --fps 15 manim_scenes/scene_08_group_chemistry.py Scene08GroupChemistry
python -m manim -pql --fps 15 manim_scenes/scene_09_period_four.py Scene09PeriodFour
python -m manim -pql --fps 15 manim_scenes/scene_10_filling_order.py Scene10FillingOrder
python -m manim -pql --fps 15 manim_scenes/scene_11_f_block.py Scene11FBlock
python -m manim -pql --fps 15 manim_scenes/scene_12_four_blocks.py Scene12FourBlocks
python -m manim -pql --fps 15 manim_scenes/scene_13_periods.py Scene13Periods
python -m manim -pql --fps 15 manim_scenes/scene_14_trends.py Scene14Trends
python -m manim -pql --fps 15 manim_scenes/scene_15_reconstruction.py Scene15Reconstruction
python -m manim -pql --fps 15 manim_scenes/scene_16_subscribe.py Scene16Subscribe
```

### All scenes at 2K / 1440p — 2560×1440, 30 fps

Here “2K” means the 2560×1440 format commonly used for 1440p video. Manim uses `-qp` for this resolution; the first `p` in `-pqp` enables the player preview.

```bash
python -m manim -pqp --fps 30 manim_scenes/scene_01_hook.py Scene01Hook
python -m manim -pqp --fps 30 manim_scenes/scene_02_atomic_number.py Scene02AtomicNumber
python -m manim -pqp --fps 30 manim_scenes/scene_03_electrons.py Scene03Electrons
python -m manim -pqp --fps 30 manim_scenes/scene_04_four_shapes.py Scene04FourShapes
python -m manim -pqp --fps 30 manim_scenes/scene_05_period_one.py Scene05PeriodOne
python -m manim -pqp --fps 30 manim_scenes/scene_06_period_two.py Scene06PeriodTwo
python -m manim -pqp --fps 30 manim_scenes/scene_07_groups.py Scene07Groups
python -m manim -pqp --fps 30 manim_scenes/scene_08_group_chemistry.py Scene08GroupChemistry
python -m manim -pqp --fps 30 manim_scenes/scene_09_period_four.py Scene09PeriodFour
python -m manim -pqp --fps 30 manim_scenes/scene_10_filling_order.py Scene10FillingOrder
python -m manim -pqp --fps 30 manim_scenes/scene_11_f_block.py Scene11FBlock
python -m manim -pqp --fps 30 manim_scenes/scene_12_four_blocks.py Scene12FourBlocks
python -m manim -pqp --fps 30 manim_scenes/scene_13_periods.py Scene13Periods
python -m manim -pqp --fps 30 manim_scenes/scene_14_trends.py Scene14Trends
python -m manim -pqp --fps 30 manim_scenes/scene_15_reconstruction.py Scene15Reconstruction
python -m manim -pqp --fps 30 manim_scenes/scene_16_subscribe.py Scene16Subscribe
```

### All scenes together as one complete video

These commands render `FullVideo`, which plays all 16 scenes in order and writes one combined movie.

```bash
# 480p, 15 fps
python -m manim -pql --fps 15 manim_scenes/full_video.py FullVideo

# 2K / 1440p, 30 fps
python -m manim -pqp --fps 30 manim_scenes/full_video.py FullVideo
```

Video output goes to `media/`. Orbital surfaces and camera moves use Manim CE's Cairo 3D renderer; these scenes take longer to render than the flat diagrams. The backdrop is faint and static so it supports the subject and lets narration holds render efficiently.

## Your voice in ElevenLabs

Use the **continuous** files `assets/narration/scene_01.txt` through `scene_16.txt`. Each contains only spoken prose, joined as a paragraph. `narration_script.md` is the readable master. `assets/narration/full_narration.txt` combines all scenes.

Timing is separate: `narration_cues.md` and `assets/narration/cue_sheet.json` carry the visual cue targets. They do not insert pauses into the TTS text. See [voiceover_guide.md](voiceover_guide.md) for recording and alignment.

Save your clips as `assets/audio/scene_01.wav`, etc. MP3/M4A also work. Keep one format per scene. Renders automatically include available clips from the start of each scene; missing clips leave that scene silent.

```bash
python main.py audio-check         # missing/duplicate clips and duration checks
python -m utils.narration_export  # regenerate prose and cue sheets after editing narration.py
```

Audio longer than its scene stops the render to prevent spill into the next scene. A length check cannot guarantee that words match the visual cues: listen to a preview, adjust beat times/durations if needed, and check again before rendering the full film.

## Checks and visual review

```bash
python main.py check                  # model, spoken pace, 15 fps timing, text layout
python -m utils.timing_audit --fps 30  # production timing
python -m utils.layout_audit --motion # also inspect intermediate animation layouts
python -m utils.storyboard 04 --every 4
```

Storyboards capture end states of selected animations and always include the final composition. They go to `output/storyboard/`. They help review content and spacing but do not replace watching actual motion. The project audits flag out-of-frame text and collisions; small element symbols in a whole-table overview remain reference detail, while teaching moments use larger tiles, counts and orbital boxes.

## Design and science

- Lato headings and labels on deep navy, with restrained outlines and strong contrast.
- Consistent block colours: s blue, p green, d gold, f purple. Spin up/down remains cyan/purple as in Part 2.
- Short screen labels and equations. Explanations live in the continuous narration.
- Real 3d/4s occupations from scandium to zinc, including chromium and copper.
- A schematic filling sequence, with an explicit explanation that orbital energies vary with occupancy and ionization.
- Fourteen-position f strips and a disclosed Sc–Y–Lu–Lr layout convention.
- Period lengths explained by subshell recipes, with closed outer s/p sets distinguished from complete principal shells.
- Covalent-size comparisons on a consistent scale, with text kept readable as spheres shrink.

[concept_summary.md](concept_summary.md) records the scientific assumptions and references. [animation_plan.md](animation_plan.md) describes all 16 scenes. [youtube_package.md](youtube_package.md) contains the publication copy and chapters.

## Source files

`config.py` owns the palette, fonts and planned durations. `narration.py` owns the spoken prose and beat times. `manim_scenes/common.py` owns the reusable tiles, orbitals, labels and scene lifecycle. `utils/physics_models.py` owns the idealized filling grid, selected configuration exceptions and radius data. `manim_scenes/full_video.py` plays the scenes in order.

The layout model uses Madelung counting and stated diagram conventions; it is a teaching model, not a full calculation or database of every atom's actual ground state. Edit source files, regenerate the narration exports, and run the checks after changes.

## Validation from this review

All 16 scenes passed the text-layout audit, and all 16 passed production timing at 30 fps. Narration pace and the model checks passed. Scene 06 was rendered as a 134-second 480p preview and inspected at representative motion frames. The optional voice-file handling was checked with temporary audio for missing, valid, duplicate and oversized clips.

See `output/validation_summary.txt`, `output/storyboard_review.png`, and `media/videos/scene_06_period_two/480p15/Scene06PeriodTwo.mp4`. No voice recordings were supplied, so the preview is silent. The full 1080p render and word-level alignment should follow recording.
