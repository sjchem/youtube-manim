# The World Is Bigger Than The Dataset

A Manim Community Edition project for Chapter 2 of the statistics/ML series. The video explains population, sample, representativeness, IID assumptions, and distribution shift using generated geometry only: dot clouds, dataset cards, road scenes, probability curves, and model icons.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Manim also needs FFmpeg and a LaTeX installation for `MathTex`.

## List Scenes

```bash
python main.py list
```

## Preview

```bash
python main.py preview 01
python main.py preview 11
python main.py preview full
```

## Quick Low-Resolution Checks

Use these while editing. `-pql` renders low resolution and opens the result.

```bash
manim -pql manim_scenes/scene_01_world_dataset.py Scene01WorldDataset --fps 15
manim -pql manim_scenes/scene_02_population.py Scene02Population --fps 15
manim -pql manim_scenes/scene_03_sample.py Scene03Sample --fps 15
manim -pql manim_scenes/scene_04_data_process.py Scene04DataProcess --fps 15
manim -pql manim_scenes/scene_05_representative_bias.py Scene05RepresentativeBias --fps 15
manim -pql manim_scenes/scene_06_self_driving_shift.py Scene06SelfDrivingShift --fps 15
manim -pql manim_scenes/scene_07_train_validation_test.py Scene07TrainValidationTest --fps 15
manim -pql manim_scenes/scene_08_iid.py Scene08IID --fps 15
manim -pql manim_scenes/scene_09_distribution_shift.py Scene09DistributionShift --fps 15
manim -pql manim_scenes/scene_10_final_question.py Scene10FinalQuestion --fps 15
manim -pql manim_scenes/scene_11_subscribe.py Scene11Subscribe --fps 15
```

Full-video low-resolution check:

```bash
manim -pql manim_scenes/full_video.py FullVideo --fps 15
```

## High-Resolution Renders

Use these for final scene renders. `-pqh` renders high quality, opens the result, and `--fps 30` keeps the video at YouTube-friendly frame rate.

```bash
manim -pqh manim_scenes/scene_01_world_dataset.py Scene01WorldDataset --fps 30
manim -pqh manim_scenes/scene_02_population.py Scene02Population --fps 30
manim -pqh manim_scenes/scene_03_sample.py Scene03Sample --fps 30
manim -pqh manim_scenes/scene_04_data_process.py Scene04DataProcess --fps 30
manim -pqh manim_scenes/scene_05_representative_bias.py Scene05RepresentativeBias --fps 30
manim -pqh manim_scenes/scene_06_self_driving_shift.py Scene06SelfDrivingShift --fps 30
manim -pqh manim_scenes/scene_07_train_validation_test.py Scene07TrainValidationTest --fps 30
manim -pqh manim_scenes/scene_08_iid.py Scene08IID --fps 30
manim -pqh manim_scenes/scene_09_distribution_shift.py Scene09DistributionShift --fps 30
manim -pqh manim_scenes/scene_10_final_question.py Scene10FinalQuestion --fps 30
manim -pqh manim_scenes/scene_11_subscribe.py Scene11Subscribe --fps 30
```

Full-video high-resolution render:

```bash
manim -pqh manim_scenes/full_video.py FullVideo --fps 30
```

CLI equivalents:

```bash
python main.py render 05 --quality high
python main.py full --quality high
```

## Scene Map

- `01`: The world is bigger than the dataset
- `02`: Population as all cases we care about
- `03`: Sample as a small window into reality
- `04`: Hidden data-generating process
- `05`: Representative sample vs biased sample
- `06`: Self-driving car in the wrong world
- `07`: Training, validation, and test sets
- `08`: IID assumption
- `09`: Distribution shift
- `10`: Does the sample represent reality?
- `11`: Subscribe card and next chapter teaser

Adjust global pacing in `config.py` with `TIMING["pace_scale"]`. The first ten explainer scenes are paced for a roughly 10-minute narration; the subscribe card keeps its own shorter timing.
