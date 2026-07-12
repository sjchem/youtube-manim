# Statistics for ML - Part 1, Chapter 4

**Video:** Probability Basics Every ML Learner Must Know

This is a Manim Community Edition project for a cinematic probability-basics chapter. It uses
the repository-level Oceanic Next theme and native Manim objects for all visuals. The planned
cut is about 11-12 minutes.

Scene timing is narration-aware: each scene pads to its configured duration in `config.py`, and
shared animation pacing is slowed through `TIMING["pace_scale"]`.

## Setup

From this folder:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The Oceanic theme lives at the repository root in `themes/`. `config.py` adds the repo root to
`sys.path` so scene imports work from this subfolder.

## List Scenes

```bash
python main.py list
```

## Quick Preview

```bash
python main.py preview 01
python main.py preview 04
python main.py preview 07
python main.py preview full
```

## Render Individual Scenes

```bash
python main.py render 01 --quality high
python main.py render 04 --quality high
python main.py render 07 --quality high
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
manim -pql manim_scenes/scene_01_uncertainty.py Scene01Uncertainty --fps 15
manim -pql manim_scenes/scene_02_probability_scale.py Scene02ProbabilityScale --fps 15
manim -pql manim_scenes/scene_03_random_variables.py Scene03RandomVariables --fps 15
manim -pql manim_scenes/scene_04_conditional_probability.py Scene04ConditionalProbability --fps 15
manim -pql manim_scenes/scene_05_independence.py Scene05Independence --fps 15
manim -pql manim_scenes/scene_06_joint_marginal.py Scene06JointMarginal --fps 15
manim -pql manim_scenes/scene_07_bayes_theorem.py Scene07BayesTheorem --fps 15
manim -pql manim_scenes/scene_08_ml_connections.py Scene08MLConnections --fps 15
manim -pql manim_scenes/scene_09_synthesis.py Scene09Synthesis --fps 15
manim -pql manim_scenes/scene_10_subscribe.py Scene10Subscribe --fps 15
manim -pql manim_scenes/full_video.py FullVideo --fps 15
```

High quality format:

```bash
manim -pqh manim_scenes/scene_01_uncertainty.py Scene01Uncertainty --fps 30
manim -pqh manim_scenes/scene_02_probability_scale.py Scene02ProbabilityScale --fps 30
manim -pqh manim_scenes/scene_03_random_variables.py Scene03RandomVariables --fps 30
manim -pqh manim_scenes/scene_04_conditional_probability.py Scene04ConditionalProbability --fps 30
manim -pqh manim_scenes/scene_05_independence.py Scene05Independence --fps 30
manim -pqh manim_scenes/scene_06_joint_marginal.py Scene06JointMarginal --fps 30
manim -pqh manim_scenes/scene_07_bayes_theorem.py Scene07BayesTheorem --fps 30
manim -pqh manim_scenes/scene_08_ml_connections.py Scene08MLConnections --fps 30
manim -pqh manim_scenes/scene_09_synthesis.py Scene09Synthesis --fps 30
manim -pqh manim_scenes/scene_10_subscribe.py Scene10Subscribe --fps 30
manim -pqh manim_scenes/full_video.py FullVideo --fps 30
```

## Files

- `concept_summary.md` - scientific summary and scene plan.
- `narration_script.md` - timestamped narration script.
- `youtube_package.md` - title, description, tags, and thumbnail ideas.
- `manim_scenes/common.py` - shared Manim helpers, including probability bars, Venn
  diagrams, joint-probability grids, and a prior-evidence-posterior flow for Bayes' theorem.
- `utils/math_utils.py` - deterministic probability utilities (conditional, joint, marginal,
  Bayes posterior).
- `utils/physics_models.py` - motion helpers for belief-shift and bar-scaling animations.
- `utils/render_helpers.py` - scene registry and Manim command builder.

## Validation

```bash
python -m compileall .
python main.py list
```

All ten scenes have been rendered at low quality (`-ql`) to confirm they run end-to-end
without errors.
