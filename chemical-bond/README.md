# Chemical Bonding, Explained Visually

**Why do atoms stick together — and what decides whether they share, transfer,
or delocalise electrons?** An 18-chapter Manim film (planned running time
**28:10**, 28:00 of story plus a subscribe card), *Chemical Bonding · Part 1*,
following [`../periodic-trend`](../periodic-trend) ("Periodic Trends, Explained
Visually"). Next in the series: *Molecular Geometry, Explained Visually*.

The film never starts from "atoms want eight electrons". It starts from two
hydrogen atoms and one number — the total energy — and builds covalent, ionic
and metallic bonding, valence bond theory (σ and π), polarity, bond length and
strength, and the limits of the octet rule from the same principle:
**E_together < E_apart**.

- [`concept_summary.md`](concept_summary.md) — the science, the models and where they stop being literal, sources
- [`animation_plan.md`](animation_plan.md) — chapter-by-chapter visuals
- [`narration_script.md`](narration_script.md) — full timestamped script (3,470 words); beat timings in [`narration_cues.md`](narration_cues.md)
- [`youtube_package.md`](youtube_package.md) — titles, description, chapters, tags, thumbnail idea

## Visual continuity and 3D

The film uses Manim Community Edition and the shared Oceanic Next theme,
matching the periodic-table and periodic-trends films. Lato stays large and
bright on the navy background. Short captions identify what is moving;
continuous narration carries the explanation. Opening headings clear after
the first few seconds, and replacement captions fade in after the old words clear.

Four scenes use `ThreeDScene`: the energy landscape (04), sigma overlap (08),
pi overlap (09), and the molecular-geometry teaser (17). Electron clouds,
crystal assembly, and the metal's moving electron density connect the other scenes.

See [`revision_review.md`](revision_review.md) for the editorial and science
review, preview artifacts, and the scope of validation.

## Setup

From this folder:

```bash
pip install -r requirements.txt
```

You also need FFmpeg/ffprobe, LaTeX with dvisvgm, Cairo/Pango and the Lato font
(see `requirements.txt`), plus the repository's shared `themes/` folder one
level up. `config.py` adds the repository root to `sys.path`, so the theme
imports from inside this sub-folder. Checked with Manim CE 0.22.0; the declared dependency range also includes 0.19.

## Preview and render

```bash
python main.py list                # chapter names, start times and durations
python main.py preview 04          # one chapter at 854×480, 15 fps
python main.py preview all         # separate previews of all 18 chapters
python main.py preview full        # the full film at preview quality
python main.py scene 04            # one chapter at 1920×1080, 30 fps
python main.py render              # FullVideo at 1920×1080, 30 fps (final)
```

### Each chapter as a 480p preview (854×480, 15 fps)

Each line also works on its own. Add `-p` to open the result when it finishes.

```bash
python -m manim -ql -r 854,480 --fps 15 manim_scenes/scene_01_invisible_force.py Scene01InvisibleForce
python -m manim -ql -r 854,480 --fps 15 manim_scenes/scene_02_promise.py Scene02Promise
python -m manim -ql -r 854,480 --fps 15 manim_scenes/scene_03_pushes_and_pulls.py Scene03PushesAndPulls
python -m manim -ql -r 854,480 --fps 15 manim_scenes/scene_04_energy_landscape.py Scene04EnergyLandscape
python -m manim -ql -r 854,480 --fps 15 manim_scenes/scene_05_stable_bond.py Scene05StableBond
python -m manim -ql -r 854,480 --fps 15 manim_scenes/scene_06_valence_lewis.py Scene06ValenceLewis
python -m manim -ql -r 854,480 --fps 15 manim_scenes/scene_07_covalent.py Scene07Covalent
python -m manim -ql -r 854,480 --fps 15 manim_scenes/scene_08_sigma_overlap.py Scene08SigmaOverlap
python -m manim -ql -r 854,480 --fps 15 manim_scenes/scene_09_pi_bonds.py Scene09PiBonds
python -m manim -ql -r 854,480 --fps 15 manim_scenes/scene_10_electron_transfer.py Scene10ElectronTransfer
python -m manim -ql -r 854,480 --fps 15 manim_scenes/scene_11_ionic_lattice.py Scene11IonicLattice
python -m manim -ql -r 854,480 --fps 15 manim_scenes/scene_12_polarity.py Scene12Polarity
python -m manim -ql -r 854,480 --fps 15 manim_scenes/scene_13_metallic.py Scene13Metallic
python -m manim -ql -r 854,480 --fps 15 manim_scenes/scene_14_length_strength.py Scene14LengthStrength
python -m manim -ql -r 854,480 --fps 15 manim_scenes/scene_15_octet_limits.py Scene15OctetLimits
python -m manim -ql -r 854,480 --fps 15 manim_scenes/scene_16_big_picture.py Scene16BigPicture
python -m manim -ql -r 854,480 --fps 15 manim_scenes/scene_17_geometry_teaser.py Scene17GeometryTeaser
python -m manim -ql -r 854,480 --fps 15 manim_scenes/scene_18_subscribe.py Scene18Subscribe
```


### Each scene at 2K/QHD (2560×1440, 30 fps)

Run these from `chemical-bond/`. Each command renders one scene; the full
block renders all 18 separately. Add `-p` to open a render automatically.

```bash
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_01_invisible_force.py Scene01InvisibleForce
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_02_promise.py Scene02Promise
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_03_pushes_and_pulls.py Scene03PushesAndPulls
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_04_energy_landscape.py Scene04EnergyLandscape
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_05_stable_bond.py Scene05StableBond
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_06_valence_lewis.py Scene06ValenceLewis
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_07_covalent.py Scene07Covalent
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_08_sigma_overlap.py Scene08SigmaOverlap
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_09_pi_bonds.py Scene09PiBonds
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_10_electron_transfer.py Scene10ElectronTransfer
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_11_ionic_lattice.py Scene11IonicLattice
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_12_polarity.py Scene12Polarity
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_13_metallic.py Scene13Metallic
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_14_length_strength.py Scene14LengthStrength
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_15_octet_limits.py Scene15OctetLimits
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_16_big_picture.py Scene16BigPicture
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_17_geometry_teaser.py Scene17GeometryTeaser
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/scene_18_subscribe.py Scene18Subscribe
```

### The whole film as one video

```bash
# Final: complete film at 1920×1080, 30 fps (same as python main.py render)
python -m manim -qh -r 1920,1080 --fps 30 manim_scenes/full_video.py FullVideo

# 2K/QHD: complete film at 2560×1440, 30 fps
python -m manim -qh -r 2560,1440 --fps 30 manim_scenes/full_video.py FullVideo

# Quick full-length preview
python -m manim -ql -r 854,480 --fps 15 manim_scenes/full_video.py FullVideo
```

Video goes to `media/`. Expect the final render to take hours: every frame
redraws the turning electron clouds, and Cairo shades every 3D face in Python.
The 3D chapters are the slowest (chapter 09's N₂ shot draws about 2,000 shaded
faces per frame while the camera moves).

## Narration and your voice

`narration.py` is the single source of the spoken script and its beat times;
scenes hold on each beat with `beat(scene, t, i)`.

- `narration_script.md` — the readable master script, chapter by chapter, with timestamps.
- [`narration_script_tagged.md`](narration_script_tagged.md) — the same continuous script with light voice-performance tags for ElevenLabs v3/v4.
- `assets/narration/scene_01.txt` … `scene_18.txt` — continuous prose to paste into a TTS tool or read aloud.
- `assets/narration/elevenlabs/scene_01.txt` … `scene_18.txt` — tagged, paste-ready text for your cloned voice, one paragraph per scene.
- `narration_cues.md`, `assets/narration/cue_sheet.json` — beat-by-beat timing targets.

In ElevenLabs, select your cloned voice and a model that supports audio tags
(v3 or v4). Paste the tagged scene text without its Markdown heading. The cues
set a warm conversational tone, invite curiosity at questions, and leave brief
thinking pauses at selected reveals. Their effect depends on the voice and
model; audition scene 01 before generating the remaining clips. For a
Professional Voice Clone, ElevenLabs currently recommends v4 over v3.
For Multilingual v2 or Flash v2.5, use the clean scene files instead.
See [ElevenLabs tag and voice guidance](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices).

Spoken wording and visual cue times stay in `narration.py`; delivery cues live
in `narration_delivery.py`. The exporter regenerates both versions. Tags guide
performance rather than exact timing, so compare the resulting audio with
`narration_cues.md` before the final render. No SSML break tags are mixed into
the v3/v4 scripts.

Save recordings as `assets/audio/scene_01.wav` (or `.mp3`/`.m4a`), one per
chapter. Renders attach them automatically; a clip longer than its chapter
stops the render rather than spilling into the next chapter.

```bash
python main.py audio-check            # missing / too-long clips
python -m utils.narration_export      # regenerate the script files after editing narration.py
```

## Checks (no video rendering needed)

```bash
python main.py check                  # models, narration, both frame rates, full film, motion layouts
python -m utils.math_utils            # colour scale, rotations, density helpers
python -m utils.physics_models        # the computed periodic table and cloud sampler
python -m utils.bond_models           # Morse curve and terms, Coulomb, Madelung 1.7476, lattice shells, LCAO surfaces
python -m utils.bond_data             # every stated pattern + all 31 spoken numbers/claims against the data
python -m utils.narration_audit       # no beat faster than 2.75 words/s
python -m utils.timing_audit          # every chapter lands on its planned second (15 fps)
python -m utils.timing_audit --fps 30 # the same at production frame rate
python -m utils.timing_audit --full   # FullVideo end to end: chapters chain, nothing left behind
python -m utils.layout_audit          # no text off-frame, overlapping or crowding (--motion: mid-animation too)
python -m utils.storyboard 04 --every 3   # PNG stills of key layouts to output/storyboard/
python -m utils.contact_sheet scene_04    # tile those stills into one review sheet
```

## Design rules

- **No number is typed in a scene.** Bond lengths and energies, ionization and
  electron affinity, lattice energies, electronegativities and geometries live
  in `utils/bond_data.py` with sources; neighbour counts, the Madelung constant,
  the reaction ledger and the ion-pair estimate are computed. `python -m
  utils.bond_data` fails if a spoken number or a stated trend disagrees with the data.
- **Pictures are models, and say so.** The energy curve is a schematic Morse model scaled to H₂ bond enthalpy; clouds are seeded probability samples; orbital surfaces are illustrative
  LCAO density isosurfaces; the electron sea is a simplified picture. Each is labelled
  on screen where it first appears, and the limits are listed in `concept_summary.md`.
- **Colour is meaning.** Orange nuclei, cyan electrons, teal attraction and
  energy released, red repulsion, orange energy required, gold energy, purple
  cations / δ+ / π, green anions / δ− / confirmed results, blue σ, copper metal cores.
- **Live objects move themselves.** Clouds, crystals and the electron sea
  redraw every frame; move them with `Glide` or their own tweens (`share_to`,
  `lean_to`, `assemble`, `drift_to`, `morph_to`), never `.animate`/`Transform`.
- **Mobile-first type.** Nothing a viewer must read is smaller than 30 pt on the
  16 × 9 canvas; `utils.layout_audit` enforces no overlaps and a breathing gap.
- **3D HUD rule.** In 3D chapters, captions are pinned with `hud()` and enter
  with `FadeIn`/`Write` only; shots are recentred by moving content, never the
  camera's `frame_center`.

## Project layout

```
chemical-bond/
├── main.py, config.py, narration.py, requirements.txt
├── README.md, concept_summary.md, animation_plan.md, youtube_package.md
├── narration_script.md, narration_cues.md          (generated from narration.py)
├── manim_scenes/   common.py, full_video.py, scene_01_… … scene_18_subscribe.py
├── utils/          bond_data.py, bond_models.py, physics_models.py, math_utils.py,
│                   render_helpers.py, narration_*.py, timing_audit.py, layout_audit.py,
│                   storyboard.py, contact_sheet.py, voiceover.py
├── assets/         audio/ images/ references/ sounds/ textures/ narration/
├── media/          (render output, not committed)
└── output/         (storyboards and review stills, not committed)
```
