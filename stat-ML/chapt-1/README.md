# Statistics for Machine Learning — Part 1, Chapter 1
## Why Statistics Matters in Machine Learning

A cinematic Manim animation in the style of 3Blue1Brown.
Built with the Oceanic Next theme from this repository.

---

## Setup

This project requires the `youtube` pyenv environment which has `manim-themes` installed.

```bash
# Activate the correct environment
pyenv activate youtube          # or: pyenv shell 3.12.9/envs/youtube

# Verify manim is working
manim --version
python main.py list
```

If `manim_themes` is missing, install it:
```bash
pip install manim-themes
```

---

## List all scenes

```bash
cd stat-ML/chapt-1
python main.py list
```

---

## Preview a single scene (fast, low quality — opens player)

```bash
python main.py preview scene_01        # opening
python main.py preview scene_02        # uncertain world
python main.py preview scene_03        # signal vs noise
python main.py preview scene_04        # population vs sample
python main.py preview scene_05        # patterns & prediction
python main.py preview scene_06        # overfitting
python main.py preview scene_07        # bias-variance
python main.py preview scene_08        # statistics layer
python main.py preview scene_09        # subscribe card
```

Or using manim directly (`-pql` = preview + low quality):

```bash
manim -pql manim_scenes/scene_01_opening.py              Scene01Opening          --fps 30
manim -pql manim_scenes/scene_02_uncertain_world.py      Scene02UncertainWorld   --fps 30
manim -pql manim_scenes/scene_03_signal_noise.py         Scene03SignalNoise      --fps 30
manim -pql manim_scenes/scene_04_population_sample.py    Scene04PopulationSample --fps 30
manim -pql manim_scenes/scene_05_patterns_prediction.py  Scene05PatternsPrediction --fps 30
manim -pql manim_scenes/scene_06_overfitting.py          Scene06Overfitting      --fps 30
manim -pql manim_scenes/scene_07_bias_variance.py        Scene07BiasVariance     --fps 30
manim -pql manim_scenes/scene_08_statistics_layer.py     Scene08StatisticsLayer  --fps 30
manim -pql manim_scenes/scene_09_subscribe.py            Scene09Subscribe        --fps 30
```

---

## Render individual scene at YouTube quality (1080p — opens player)

```bash
python main.py scene scene_01
python main.py scene scene_02
python main.py scene scene_03
python main.py scene scene_04
python main.py scene scene_05
python main.py scene scene_06
python main.py scene scene_07
python main.py scene scene_08
python main.py scene scene_09
```

Or using manim directly (`-pqh` = preview + high quality):

```bash
manim -pqh manim_scenes/scene_01_opening.py              Scene01Opening          --fps 30
manim -pqh manim_scenes/scene_02_uncertain_world.py      Scene02UncertainWorld   --fps 30
manim -pqh manim_scenes/scene_03_signal_noise.py         Scene03SignalNoise      --fps 30
manim -pqh manim_scenes/scene_04_population_sample.py    Scene04PopulationSample --fps 30
manim -pqh manim_scenes/scene_05_patterns_prediction.py  Scene05PatternsPrediction --fps 30
manim -pqh manim_scenes/scene_06_overfitting.py          Scene06Overfitting      --fps 30
manim -pqh manim_scenes/scene_07_bias_variance.py        Scene07BiasVariance     --fps 30
manim -pqh manim_scenes/scene_08_statistics_layer.py     Scene08StatisticsLayer  --fps 30
manim -pqh manim_scenes/scene_09_subscribe.py            Scene09Subscribe        --fps 30
```

---

## Render full video (all scenes, 1080p 30fps — opens player)

```bash
python main.py render
# or directly:
manim -pqh manim_scenes/full_video.py FullVideo --fps 30
```

Output lands in `media/videos/full_video/1080p30/FullVideo.mp4`

---

## Project structure

```
chapt-1/
├── main.py                    CLI entry point
├── config.py                  Colours, fonts, timing, durations
├── requirements.txt
├── narration_script.md        Full timestamped voiceover script
├── animation_plan.md          Scene-by-scene visual breakdown
├── concept_summary.md         Scientific background and key concepts
├── youtube_package.md         Titles, description, tags, thumbnail ideas
├── manim_scenes/
│   ├── common.py              Shared helpers (theme, background, glow, text)
│   ├── full_video.py          Combines all scenes into one render
│   ├── scene_01_opening.py    Grand series opener
│   ├── scene_02_uncertain_world.py
│   ├── scene_03_signal_noise.py
│   ├── scene_04_population_sample.py
│   ├── scene_05_patterns_prediction.py
│   ├── scene_06_overfitting.py
│   ├── scene_07_bias_variance.py
│   ├── scene_08_statistics_layer.py
│   └── scene_09_subscribe.py
├── utils/
│   ├── math_utils.py          Noisy sine, regression, polynomial fit, Gaussian
│   ├── physics_models.py      Bias-variance shots, pipeline stages, course parts
│   └── render_helpers.py      Subprocess render + ffmpeg stitch helpers
└── assets/
    ├── audio/   (voiceover files — add your own)
    ├── images/
    ├── references/
    ├── sounds/
    └── textures/
```

---

## Scene durations

| Scene | Topic | Duration |
|-------|-------|----------|
| 01 | Series opening | ~55 s |
| 02 | The uncertain world | ~65 s |
| 03 | Signal vs Noise | ~68 s |
| 04 | Population vs Sample | ~67 s |
| 05 | Patterns & Prediction | ~78 s |
| 06 | Overfitting | ~78 s |
| 07 | Bias-Variance tradeoff | ~77 s |
| 08 | Statistics as the thinking layer | ~77 s |
| 09 | Subscribe card | ~17 s |
| **Total** | | **~9 min 42 sec** |

---

## Theme

Uses the **Oceanic Next** dark theme from `themes/oceanic_next.py`.
Colour roles:
- **Cyan** — signal, statistics, models
- **Green** — correct, generalising, truth
- **Orange** — observations, raw data
- **Red** — error, overfitting, noise
- **Purple** — unseen / test data, limits
- **Gold** — highlight, confidence intervals
- **Muted grey** — population, background structure
