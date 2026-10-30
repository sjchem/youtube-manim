# Concentration, Explained Visually

**How can one solution have so many different concentrations?** A Manim film
(planned running time **35:00**) on molarity, molality, normality,
mole fraction, percentages, ppm/ppb, density conversions and dilution — built
as 21 scenes that map onto the brief's **12 YouTube chapters**.

One glass drives the whole film: **18.0 g glucose in 180.0 g water, measured
final volume 191.0 mL**. It is 0.524 M, 0.556 m, x = 0.00990 and 9.09 % by
mass — four correct answers — and each chapter changes only *what the glucose
is compared with*. Three reveals carry the story: the same solution has many
correct values; heating changes molarity but not molality; normality depends
on the reaction.

- [`revision_review.md`](revision_review.md) — review findings, corrections, visual previews and validation
- [`concept_summary.md`](concept_summary.md) — the science, the model's limits, sources
- [`animation_plan.md`](animation_plan.md) — scene-by-scene visuals
- [`narration_script.md`](narration_script.md) — full timestamped script; ElevenLabs-tagged version in [`narration_script_tagged.md`](narration_script_tagged.md); per-scene, per-beat timing plan in [`narration_cues.md`](narration_cues.md)
- [`youtube_package.md`](youtube_package.md) — titles, description, chapters, tags, thumbnail idea

## Why Manim CE (and not ManimGL)

The brief prefers ManimGL for 3D. This film is built on **Manim Community
Edition** on purpose:

* the channel's shared Oceanic Next theme (`../themes/oceanic_next.py`) is
  written against CE through `manim_themes`, so a ManimGL scene could not use
  the house look that ties the videos together;
* the one-scene full-film render (`FullVideo`) needs a single engine;
* ManimGL is installed only in a separate Python env here.

The 3D comes from the projection engine shared with the previous films
([`manim_scenes/stage3d.py`](manim_scenes/stage3d.py)), extended for this film
with **`Glassware`** (beakers, graduated cylinders and volumetric flasks as
solids of revolution with liquid inside, layered reflections, double rims and shaded liquid) and **`Swarm`** (hundreds of solvent
and solute particles with depth shading and highlights, jiggling inside a glass or a cube). Every glass, molecule
and litre cube slowly turns, so no shot is static, while captions stay ordinary
2D text.

## Everything on screen is computed

* **The reference solution** (`utils/physics_models.py`): `Solution` derives
  molarity, molality, mole fractions, mass percent, % (w/v), mass
  concentration and density from three measurements and two molar masses. No
  scene types one of those numbers; on-screen strings come from the model.
* **Glassware**: a `Profile` integrates π r(y)² so liquid rises by *volume*
  through the real shape — fast in a flask's thin neck, slow in its bulb.
* **Heating** (scene 08): the closed sample, with expansion headspace, is assumed to expand like pure
  water from 20 to 70 °C (CRC densities), taking 191.0 mL to 195 mL; two live
  meters read the cylinder's own volume every frame.
* **Molecules**: β-D-glucopyranose as an ideal ⁴C₁ chair (all substituents
  equatorial, C₆H₁₂O₆ checked), water at 104.5°, tetrahedral H₂SO₄ with its two
  acidic hydrogens. In scene 11 the protons really travel on the 3D stage.
* **Spoken numbers** (`utils/concentration_data.py`): `python -m
  utils.concentration_data` recomputes every number the narrator says (64
  claims), converts it to words ("zero point five two four") and checks the
  phrase still appears in `narration.py`.
* **ppm**: scene 16 renders a real 1000 × 1000 field of dots live at every zoom
  level, from one gold dot to the whole million.

Pictures that are metaphors are labelled on screen ("a picture, not to
scale"): the packing of ethanol and water, the freezing lattices, one bead per
0.0100 mol in the dilution. Particle swarms that claim a ratio keep the true
1 glucose : 100 water molecule ratio.

## Setup

From this folder, in the repository's `youtube` pyenv environment (Manim CE
0.22; the default `python` here is a different env):

```bash
pip install -r requirements.txt
```

You also need FFmpeg/ffprobe, LaTeX with dvisvgm, Cairo/Pango and the Lato font
(see `requirements.txt`), plus the repository's shared `themes/` folder one
level up. `config.py` adds the repository root to `sys.path`, so the theme
imports from inside this sub-folder.

## Preview and render

```bash
python main.py list                # scene names, start times and durations
python main.py chapters            # the 12 YouTube chapter markers
python main.py preview 08          # one scene at 854×480, 15 fps
python main.py preview all         # separate previews of all 21 scenes
python main.py preview full        # the full film at preview quality
python main.py scene 08            # one scene at 1920×1080, 30 fps
python main.py render              # FullVideo at 1920×1080, 30 fps (final)
python main.py check               # model, spoken numbers, narration, timing and layout audits
python main.py audio-check         # recorded narration clips vs scene lengths
```

Final 1080p film, directly with Manim:

```bash
python -m manim -qh --fps 30 -r 1920,1080 manim_scenes/full_video.py FullVideo
```

Output: `media/videos/full_video/1080p30/FullVideo.mp4`.

### All 21 scenes at 1440p (2560 × 1440), in one batch

Run this from the `concentration` directory in the same Python environment.
It renders a separate file for every scene, in order, at 30 fps:

```bash
python - <<'PYRENDER'
import subprocess
import sys
from main import SCENE_MAP

for module, scene_class, _ in SCENE_MAP.values():
    subprocess.run([
        sys.executable, "-m", "manim", "-qh", "--fps", "30",
        "-r", "2560,1440", module.replace(".", "/") + ".py", scene_class,
    ], check=True)
PYRENDER
```

Each file lands under `media/videos/<scene_module>/1440p30/`.
For a single joined 1440p film instead:

```bash
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/full_video.py FullVideo
```

### Each scene at 2K / 1440p (2560 × 1440, 30 fps)

Run any command below from the `concentration` directory, or paste the whole
block to render all scenes in sequence.

```bash
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_01_mystery.py Scene01Mystery
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_02_counting_moles.py Scene02CountingMoles
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_03_volume_not_additive.py Scene03VolumeNotAdditive
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_04_molarity.py Scene04Molarity
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_05_volumetric_flask.py Scene05VolumetricFlask
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_06_molality.py Scene06Molality
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_07_colligative.py Scene07Colligative
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_08_temperature.py Scene08Temperature
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_09_both_measures.py Scene09BothMeasures
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_10_normality.py Scene10Normality
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_11_two_reactions.py Scene11TwoReactions
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_12_mole_fraction.py Scene12MoleFraction
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_13_sum_to_one.py Scene13SumToOne
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_14_percent_mass.py Scene14PercentMass
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_15_percent_volume.py Scene15PercentVolume
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_16_ppm.py Scene16Ppm
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_17_density_bridge.py Scene17DensityBridge
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_18_dilution.py Scene18Dilution
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_19_traps.py Scene19Traps
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_20_finale.py Scene20Finale
python -m manim -qh --fps 30 -r 2560,1440 manim_scenes/scene_21_subscribe.py Scene21Subscribe
```

### Each scene as a 480p preview

```bash
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_01_mystery.py Scene01Mystery
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_02_counting_moles.py Scene02CountingMoles
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_03_volume_not_additive.py Scene03VolumeNotAdditive
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_04_molarity.py Scene04Molarity
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_05_volumetric_flask.py Scene05VolumetricFlask
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_06_molality.py Scene06Molality
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_07_colligative.py Scene07Colligative
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_08_temperature.py Scene08Temperature
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_09_both_measures.py Scene09BothMeasures
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_10_normality.py Scene10Normality
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_11_two_reactions.py Scene11TwoReactions
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_12_mole_fraction.py Scene12MoleFraction
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_13_sum_to_one.py Scene13SumToOne
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_14_percent_mass.py Scene14PercentMass
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_15_percent_volume.py Scene15PercentVolume
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_16_ppm.py Scene16Ppm
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_17_density_bridge.py Scene17DensityBridge
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_18_dilution.py Scene18Dilution
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_19_traps.py Scene19Traps
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_20_finale.py Scene20Finale
python -m manim -ql --fps 15 -r 854,480 manim_scenes/scene_21_subscribe.py Scene21Subscribe
```

### Review without rendering video

```bash
python -m utils.storyboard 08 --every 3     # still frames of a scene's key layouts
python -m utils.contact_sheet scene_08      # tile them into one sheet
python -m utils.timing_audit                # every scene lands on its duration
python -m utils.layout_audit --motion       # no text leaves the frame or collides
```

## Scenes

| # | Starts | Length | Class | What happens |
|---|---|---|---|---|
| 01 | 00:00 | 105s | `Scene01Mystery` | Hook: glucose dissolves (3D); four answers |
| 02 | 01:45 | 70s | `Scene02CountingMoles` | Masses add on a balance; n = m / M |
| 03 | 02:55 | 65s | `Scene03VolumeNotAdditive` | 50 + 50 mL -> 96.5 mL; four quantities |
| 04 | 04:00 | 130s | `Scene04Molarity` | Glucose lit, volume outlined (3D); c = n / V |
| 05 | 06:10 | 125s | `Scene05VolumetricFlask` | Wrong way vs filling to the mark (3D) |
| 06 | 08:15 | 120s | `Scene06Molality` | Solvent lit and weighed; denominator swaps |
| 07 | 10:15 | 105s | `Scene07Colligative` | Freezing-point drop from molality |
| 08 | 12:00 | 120s | `Scene08Temperature` | Heat a closed cylinder: M falls, m holds (3D) |
| 09 | 14:00 | 90s | `Scene09BothMeasures` | Bench vs physical chemistry; M vs m plot |
| 10 | 15:30 | 120s | `Scene10Normality` | H2SO4 molecule (3D); N = M f; deprecation |
| 11 | 17:30 | 120s | `Scene11TwoReactions` | One proton vs two: 0.500 N vs 1.00 N |
| 12 | 19:30 | 110s | `Scene12MoleFraction` | 101-molecule crowd (3D); random picks |
| 13 | 21:20 | 85s | `Scene13SumToOne` | x's add to one; Raoult's law |
| 14 | 22:45 | 105s | `Scene14PercentMass` | % w/w on a balance; % w/v in a flask |
| 15 | 24:30 | 90s | `Scene15PercentVolume` | % v/v to the mark; grams per litre |
| 16 | 26:00 | 130s | `Scene16Ppm` | One gold dot in a million; ppm and ppb bases |
| 17 | 28:10 | 95s | `Scene17DensityBridge` | One-litre cube (3D): density links M and m |
| 18 | 29:45 | 90s | `Scene18Dilution` | Particles conserved into a bigger flask (3D) |
| 19 | 31:15 | 155s | `Scene19Traps` | Five traps with countdowns |
| 20 | 33:50 | 60s | `Scene20Finale` | The concentration map around the glass (3D) |
| 21 | 34:50 | 10s | `Scene21Subscribe` | Subscribe card |

YouTube chapters (from `config.YOUTUBE_CHAPTERS`):

- 00:00 The mystery of concentration
- 01:45 What are we actually measuring?
- 04:00 Molarity: counting moles in space
- 08:15 Molality: counting moles against mass
- 12:00 Molarity vs molality: the temperature experiment
- 15:30 Normality: when the reaction changes the answer
- 19:30 Mole fraction: a molecular population view
- 22:45 Three ways to say percent
- 26:00 ppm and ppb: chemistry at tiny scales
- 28:10 Conversions and dilution
- 31:15 Five concentration traps
- 33:50 The concentration map

## Narration and voice

`narration.py` holds the spoken prose as timed beats; each scene waits on its
beats with `beat(scene, t, i)`, so picture and voice stay aligned. 3,936
words over 35 minutes (the brief's 3,500–4,000), with each beat checked
against the natural voice pace of about 100 words in 35 seconds; the rest is deliberate looking time on 3D shots, calculations and
the traps' countdowns.

```bash
python -m utils.narration_audit            # every beat fits its window
python -m utils.narration_export --beats   # regenerate scripts, cue sheets, per-beat texts
```

Exports land in `narration_script.md`, `narration_script_tagged.md`
(sparse ElevenLabs v3/v4 tags such as `[short pause]`, `[pause]`, `[long
pause]` from `narration_delivery.py`), `narration_cues.md`, and
`assets/narration/` (clean and tagged per-scene and per-beat texts, plus
`cue_sheet.json`).

To add the recorded voice, put either one clip per scene
(`assets/audio/scene_08.wav`) or one clip per beat
(`assets/audio/scene_08/beat_001.wav`, …) in place; every render attaches them
at their cues, and `python main.py audio-check` reports any clip that is
longer than its window. Beat clips keep your voice's natural pace. They are the preferred option for
this film: the editor inserts the cue-sheet holds between clips. A single
continuous clip per scene must already include those internal holds to match
the pictures; pause tags alone do not guarantee the timing.

## Project layout

```
concentration/
├── main.py                  # list / chapters / preview / scene / render / check / audio-check
├── config.py                # canvas, palette and meanings, fonts, durations, theme + repo path
├── narration.py             # timed narration beats (the timing source)
├── narration_delivery.py    # ElevenLabs delivery tags, kept out of the prose
├── manim_scenes/
│   ├── common.py            # lifecycle, type, glows, instruments, fractions, subscribe card
│   ├── stage3d.py           # projected 3D: balls, rods, glassware, swarms
│   ├── full_video.py        # FullVideo: every scene in order
│   └── scene_01 … scene_21  # one file per scene
├── utils/
│   ├── physics_models.py    # solution, conversions, glassware profiles, molecules, motion
│   ├── concentration_data.py# measured data, sources, spoken-number check
│   ├── math_utils.py        # rotations, projection, hulls, colour
│   ├── render_helpers.py    # safe-frame fitting
│   └── *_audit.py, storyboard.py, contact_sheet.py, narration_export.py, voiceover.py
└── assets/  media/  output/
```

No plugins are used: core Manim plus the models above draw everything, which
keeps the science checkable and the project easy to install.
