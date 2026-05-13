# The Math Behind Winning a Tennis Game

A Manim educational video project answering:

**How does a 70.4% chance of winning a single service point become about a 90.6% chance of winning the whole service game?**

The project builds a 6-8 minute YouTube-ready explainer using Bernoulli trials, binomial path counting, deuce recursion, and a 2024 Alexander Zverev serving example inspired by Pratish Patel's article, "Random Musings: The Math Behind Winning a Tennis Game."

## Setup

From this folder:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Manim may require system dependencies such as Cairo, Pango, and FFmpeg.

## Check the Math

```bash
python main.py --probabilities
python main.py --probabilities --simulate
python utils/math_utils.py
```

Expected headline values:

- Point win probability from the Zverev serve split: about `0.7046`
- Closed-form service-game win probability at `p = 0.7046`: about `0.906`
- `G(0.5) = 0.5`

## Render Manim Scenes

Example:

```bash
manim -pqh manim_scenes/scene_06_full_formula.py FullFormulaScene
```

All scene commands:

```bash
manim -qh manim_scenes/scene_01_hook.py HookScene
manim -qh manim_scenes/scene_02_service_point.py ServicePointProbabilityScene
manim -qh manim_scenes/scene_03_bernoulli.py BernoulliTrialScene
manim -qh manim_scenes/scene_04_paths_before_deuce.py PathsBeforeDeuceScene
manim -qh manim_scenes/scene_05_deuce_recursion.py DeuceRecursionScene
manim -qh manim_scenes/scene_06_full_formula.py FullFormulaScene
manim -qh manim_scenes/scene_07_graph.py GraphScene
manim -qh manim_scenes/scene_08_zverev_case_study.py ZverevCaseStudyScene
manim -qh manim_scenes/scene_09_outro.py OutroScene
```

For 1080p production output:

```bash
manim -qk --fps 60 manim_scenes/scene_06_full_formula.py FullFormulaScene
```

## Project Map

- `utils/math_utils.py`: exact probabilities, deuce recursion, Monte Carlo simulation
- `utils/tennis_scoring.py`: tennis score labels, path generation, score-state graph
- `manim_scenes/`: nine animated mathematical scenes
- `narration_script.md`: scene-synchronized voiceover
- `output/`: generated frames and renders

## Mathematical Formula

The service point probability is:

```text
P(W) = P(S1)P(W|S1) + (1 - P(S1))P(S2)P(W|S2)
```

The service-game win probability is:

```text
G(p) = p^4
     + 4p^4(1-p)
     + 10p^4(1-p)^2
     + 20p^3(1-p)^3 * p^2 / (p^2 + (1-p)^2)
```

For the Zverev branch total `p = 0.7046`, this gives about `90.6%`.
