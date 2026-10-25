# Molecular Orbital Theory, Explained Visually

**How can electrons hold atoms together, weaken bonds, and even make a
molecule magnetic?** A 23-chapter Manim film (planned running time **34:10**,
34:00 of story plus a subscribe card), *Chemical Bonding · Part 3*, following
[`../chemical-bond`](../chemical-bond) and
[`../molecular-geometry`](../molecular-geometry).

One mystery drives the whole film: oxygen's Lewis structure shows every
electron paired, yet liquid oxygen hangs between the poles of a magnet. The
story runs **atomic waves → wave combinations (LCAO) → MO energies → electron
filling → bond order and magnetism**, and the answer arrives in chapter 16,
when oxygen's twelve Lewis electrons fly into its molecular orbitals and the
last two land, unpaired, in π\*.

- [`concept_summary.md`](concept_summary.md) — the science, the model's limits, sources
- [`animation_plan.md`](animation_plan.md) — chapter-by-chapter visuals
- [`narration_script.md`](narration_script.md) — full timestamped script; ElevenLabs-tagged version in [`narration_script_tagged.md`](narration_script_tagged.md); per-scene and per-beat timing plan in [`narration_cues.md`](narration_cues.md)
- [`revision_review.md`](revision_review.md) — review findings, changes and previews
- [`youtube_package.md`](youtube_package.md) — titles, description, chapters, tags, thumbnail idea

## Why Manim CE (and not ManimGL)

The brief prefers ManimGL for 3D. This film is built on **Manim Community
Edition** on purpose:

* the channel's shared Oceanic Next theme (`../themes/oceanic_next.py`) is
  written against CE through `manim_themes`, so a ManimGL scene could not use
  the house look that ties the series together;
* the single-scene full-film render (`FullVideo`) needs one engine;
* ManimGL is installed only in a separate Python env here.

The 3D comes from the projection engine shared with the previous film
([`manim_scenes/stage3d.py`](manim_scenes/stage3d.py)): bodies keep true 3D
coordinates and each frame a `Stage` turns, projects and depth-sorts them, so
orbitals stay smooth in Cairo, captions stay ordinary 2D text, and every model
can keep turning.

## Everything on screen is computed

* **Orbital surfaces** (`utils/orbital_models.py`): normalised LCAO
  combinations ψ = (φA + c φB)/√(1 + c² + 2cS) of hydrogen-like 1s and 2p
  functions; each |ψ| = level surface is extracted with marching cubes and
  split into signed lobes (blue +, rose −). Nuclei sliding together and a
  phase coefficient sliding from +1 to −1 are recomputed frame by frame. The
  check confirms bonding density between the nuclei, antibonding nodes, and the
  lobe counts of σ, σ\*, π and π\*.
* **MO diagrams and filling** (`utils/mo_models.py`): every arrow comes from
  Aufbau + Pauli + Hund placements; bond orders, unpaired counts and
  configurations are read from the filling. Energies are schematic; orderings
  are the standard ones (s–p mixed for B₂, C₂, N₂).
* **Physics** (`utils/physics_models.py`): the LCAO energy curves of H₂⁺
  (minimum 2.49 bohr, 1.76 eV — vs the exact 2.00 bohr, 2.79 eV), Hückel
  chains (N in → N out), the seeded magnet pour (a ∇(B²) pull on a
  paramagnetic liquid), and spins in a field.
* **Data and spoken claims** (`utils/mo_data.py`): measured bond lengths, D₀,
  orbital energies and the helium dimer, with sources. `python -m
  utils.mo_data` checks all 52 spoken claims in `narration.py` and that the
  model reproduces 12 literature bond orders and unpaired counts.

## Setup

From this folder, in the repository's `youtube` pyenv environment (Manim CE
0.22):

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
python main.py preview 16          # one chapter at 854×480, 15 fps
python main.py preview all         # separate previews of all 23 chapters
python main.py preview full        # the full film at preview quality
python main.py scene 16            # one chapter at 1920×1080, 30 fps
python main.py render              # FullVideo at 1920×1080, 30 fps (final)
python main.py check               # every model, data, narration, timing and layout audit
python main.py audio-check         # recorded narration clips vs chapter lengths
```

Final 1080p film, directly with Manim:

```bash
python -m manim -qh --fps 30 -r 1920,1080 manim_scenes/full_video.py FullVideo
```

Output: `media/videos/full_video/1080p30/FullVideo.mp4`.



### 2K / 1440p: all 23 chapters in one batch

```bash
set -e
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_01_oxygen_mystery.py Scene01OxygenMystery
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_02_two_pictures.py Scene02TwoPictures
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_03_waves.py Scene03Waves
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_04_lcao.py Scene04Lcao
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_05_bonding_antibonding.py Scene05BondingAntibonding
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_06_two_energies.py Scene06TwoEnergies
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_07_h2_plus.py Scene07H2Plus
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_08_hydrogen.py Scene08Hydrogen
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_09_helium.py Scene09Helium
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_10_sigma_p.py Scene10SigmaP
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_11_pi.py Scene11Pi
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_12_build_diagram.py Scene12BuildDiagram
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_13_orderings.py Scene13Orderings
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_14_fill_nitrogen.py Scene14FillNitrogen
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_15_nitrogen_bond.py Scene15NitrogenBond
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_16_oxygen_reveal.py Scene16OxygenReveal
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_17_mystery_solved.py Scene17MysterySolved
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_18_remove_electron.py Scene18RemoveElectron
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_19_add_electrons.py Scene19AddElectrons
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_20_boron_fluorine.py Scene20BoronFluorine
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_21_challenge.py Scene21Challenge
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_22_final.py Scene22Final
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_23_subscribe.py Scene23Subscribe
```

### Each chapter as a 480p preview

```bash
manim -ql --fps 15 -r 854,480 manim_scenes/scene_01_oxygen_mystery.py Scene01OxygenMystery
manim -ql --fps 15 -r 854,480 manim_scenes/scene_02_two_pictures.py Scene02TwoPictures
manim -ql --fps 15 -r 854,480 manim_scenes/scene_03_waves.py Scene03Waves
manim -ql --fps 15 -r 854,480 manim_scenes/scene_04_lcao.py Scene04Lcao
manim -ql --fps 15 -r 854,480 manim_scenes/scene_05_bonding_antibonding.py Scene05BondingAntibonding
manim -ql --fps 15 -r 854,480 manim_scenes/scene_06_two_energies.py Scene06TwoEnergies
manim -ql --fps 15 -r 854,480 manim_scenes/scene_07_h2_plus.py Scene07H2Plus
manim -ql --fps 15 -r 854,480 manim_scenes/scene_08_hydrogen.py Scene08Hydrogen
manim -ql --fps 15 -r 854,480 manim_scenes/scene_09_helium.py Scene09Helium
manim -ql --fps 15 -r 854,480 manim_scenes/scene_10_sigma_p.py Scene10SigmaP
manim -ql --fps 15 -r 854,480 manim_scenes/scene_11_pi.py Scene11Pi
manim -ql --fps 15 -r 854,480 manim_scenes/scene_12_build_diagram.py Scene12BuildDiagram
manim -ql --fps 15 -r 854,480 manim_scenes/scene_13_orderings.py Scene13Orderings
manim -ql --fps 15 -r 854,480 manim_scenes/scene_14_fill_nitrogen.py Scene14FillNitrogen
manim -ql --fps 15 -r 854,480 manim_scenes/scene_15_nitrogen_bond.py Scene15NitrogenBond
manim -ql --fps 15 -r 854,480 manim_scenes/scene_16_oxygen_reveal.py Scene16OxygenReveal
manim -ql --fps 15 -r 854,480 manim_scenes/scene_17_mystery_solved.py Scene17MysterySolved
manim -ql --fps 15 -r 854,480 manim_scenes/scene_18_remove_electron.py Scene18RemoveElectron
manim -ql --fps 15 -r 854,480 manim_scenes/scene_19_add_electrons.py Scene19AddElectrons
manim -ql --fps 15 -r 854,480 manim_scenes/scene_20_boron_fluorine.py Scene20BoronFluorine
manim -ql --fps 15 -r 854,480 manim_scenes/scene_21_challenge.py Scene21Challenge
manim -ql --fps 15 -r 854,480 manim_scenes/scene_22_final.py Scene22Final
manim -ql --fps 15 -r 854,480 manim_scenes/scene_23_subscribe.py Scene23Subscribe
```

Rendering cost: chapters with live orbital surfaces (05, 10, 11, 15, 16, 22)
recompute marching cubes while a surface changes; expect them to be the
slowest. Static surfaces are cached.

## Narration and voice

* `narration.py` holds the spoken text as timed beats; scenes hold on each beat
  with `beat(scene, t, i)`.
* `python -m utils.narration_audit` checks that every beat fits its window at
  the cloned voice's pace (≤ 2.85 words/s).
* `python -m utils.narration_export --beats` regenerates the clean script, the
  ElevenLabs-tagged script (`narration_delivery.py` holds sparse delivery
  tags), per-scene text files, per-beat files and the JSON/Markdown cue sheets.
* Drop recordings in `assets/audio/` — either one clip per chapter
  (`scene_16.wav`) or cue-aligned beats (`scene_16/beat_001.wav`, …); they are
  attached automatically and `python main.py audio-check` reports fit. Beats
  keep the voice's natural speed; breathing room is silence, never stretching.

The reviewed script has **4,684 spoken words** over **34:10** (about **137
words per finished minute**). Most explanation scenes use 140–150 words per
minute; dense orbital views, the oxygen reveal, the prediction challenge and
the closing card use less. At your measured voice pace (100 words in 35
seconds), the estimated speech is **27:19**, leaving **6:51** distributed through
the edit for viewing, movement, breathing and the closing fade.

ElevenLabs v4 pause tags guide delivery; they do not guarantee timed silence.
Generate the numbered beat clips, measure them, and keep each clip at its cue.
Hold the corresponding animation until the next cue instead of compressing
the video to the length of one uninterrupted TTS file. `narration_cues.md`
shows the suggested pauses; the JSON cue sheet also includes their estimated
start times. Replace estimates with the actual recording lengths before the
final render. See the [visual and narration review](revision_review.md) for
changes, scene previews and validation limits.

## Checking without rendering

```bash
python -m utils.timing_audit           # each chapter lands on its configured second
python -m utils.timing_audit --full    # FullVideo chains all chapters, 0 stray mobjects
python -m utils.layout_audit --motion  # no text overlaps or off-frame text, mid-animation too
python -m utils.storyboard 16 --every 3 && python -m utils.contact_sheet scene_16
```

## Project layout

```
mo-theory/
├── main.py, config.py, narration.py, narration_delivery.py, requirements.txt
├── README.md, concept_summary.md, animation_plan.md, youtube_package.md
├── narration_script.md, narration_script_tagged.md, narration_cues.md   (generated)
├── manim_scenes/   common.py (visual grammar), stage3d.py (3D engine), full_video.py, scene_01 … scene_23
├── utils/          orbital_models, mo_models, mo_data, physics_models, math_utils, render_helpers,
│                   narration_audit/export, timing_audit, layout_audit, storyboard, contact_sheet, voiceover
├── assets/         audio/, images/, narration/ (generated texts), references/, sounds/, textures/
├── media/          (render output, not committed)
└── output/         (storyboards, not committed)
```
