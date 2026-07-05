# Statistics for ML - Part 1, Chapter 3

**Video:** Mean, Median, Variance & Standard Deviation for ML

This is a Manim Community Edition project for a cinematic descriptive statistics chapter. It uses the repository-level Oceanic Next theme and native Manim objects for all visuals. The planned cut is about 12-13 minutes.

Scene timing is narration-aware: each scene pads to its configured duration in `config.py`, and shared animation pacing is slowed through `TIMING["pace_scale"]`.

## Setup

From this folder:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The Oceanic theme lives at the repository root in `themes/`. `config.py` adds the repo root to `sys.path` so scene imports work from this subfolder.

## List Scenes

```bash
python main.py list
```

## Quick Preview

```bash
python main.py preview 01
python main.py preview 04
python main.py preview 10
python main.py preview full
```

## Render Individual Scenes

```bash
python main.py render 01 --quality high
python main.py render 07 --quality high
python main.py render 11 --quality high
```

## Render Full Video

```bash
python main.py full --quality high
```

For a 4K render:

```bash
python main.py full --quality 4k
```

## Direct Manim Commands

Low preview format:

```bash
manim -pql manim_scenes/scene_01_data_first_look.py Scene01DataFirstLook --fps 15
manim -pql manim_scenes/scene_02_center.py Scene02Center --fps 15
manim -pql manim_scenes/scene_03_outliers.py Scene03Outliers --fps 15
manim -pql manim_scenes/scene_04_spread.py Scene04Spread --fps 15
manim -pql manim_scenes/scene_05_percentiles.py Scene05Percentiles --fps 15
manim -pql manim_scenes/scene_06_scaling.py Scene06Scaling --fps 15
manim -pql manim_scenes/scene_07_covariance_correlation.py Scene07CovarianceCorrelation --fps 15
manim -pql manim_scenes/scene_08_worked_mean_variance.py Scene08WorkedMeanVariance --fps 15
manim -pql manim_scenes/scene_09_distribution_shape.py Scene09DistributionShape --fps 15
manim -pql manim_scenes/scene_10_correlation_example.py Scene10CorrelationExample --fps 15
manim -pql manim_scenes/scene_11_ml_checklist.py Scene11MLChecklist --fps 15
manim -pql manim_scenes/scene_12_subscribe.py Scene12Subscribe --fps 15
manim -pql manim_scenes/full_video.py FullVideo --fps 15
```

High preview format:

```bash
manim -pqh manim_scenes/scene_01_data_first_look.py Scene01DataFirstLook --fps 30
manim -pqh manim_scenes/scene_02_center.py Scene02Center --fps 30
manim -pqh manim_scenes/scene_03_outliers.py Scene03Outliers --fps 30
manim -pqh manim_scenes/scene_04_spread.py Scene04Spread --fps 30
manim -pqh manim_scenes/scene_05_percentiles.py Scene05Percentiles --fps 30
manim -pqh manim_scenes/scene_06_scaling.py Scene06Scaling --fps 30
manim -pqh manim_scenes/scene_07_covariance_correlation.py Scene07CovarianceCorrelation --fps 30
manim -pqh manim_scenes/scene_08_worked_mean_variance.py Scene08WorkedMeanVariance --fps 30
manim -pqh manim_scenes/scene_09_distribution_shape.py Scene09DistributionShape --fps 30
manim -pqh manim_scenes/scene_10_correlation_example.py Scene10CorrelationExample --fps 30
manim -pqh manim_scenes/scene_11_ml_checklist.py Scene11MLChecklist --fps 30
manim -pqh manim_scenes/scene_12_subscribe.py Scene12Subscribe --fps 30
manim -pqh manim_scenes/full_video.py FullVideo --fps 30
```

## Files

- `concept_summary.md` - scientific summary and scene plan.
- `narration_script.md` - timestamped narration script.
- `youtube_package.md` - title, description, tags, and thumbnail ideas.
- `manim_scenes/common.py` - shared Manim helpers and statistics visuals.
- `utils/math_utils.py` - deterministic statistics utilities.
- `utils/render_helpers.py` - scene registry and Manim command builder.

## Validation

```bash
python -m compileall .
python main.py list
```
