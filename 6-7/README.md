# Why 6 Is Perfect and 7 Is Mysterious

A complete Manim Community Edition project for a cinematic scientific YouTube animation about 6 as visible mathematical order and 7 as hidden cyclic mystery.

## Setup

From this folder:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The project uses the local repository Oceanic theme from `../themes`.

## List Scenes

```bash
python main.py --list
```

## Preview One Scene

```bash
python main.py hook -q l
python main.py hexagon -q l
python main.py cyclic -q l
```

Add `-p` to open the render after Manim finishes:

```bash
python main.py decimal -q l -p
```

## Render Individual Scenes

Use `-ql` for fast low-definition previews and `-qh` for high-definition renders.

Low definition:

```bash
python -m manim -ql manim_scenes/scene_01_hook.py Scene01Hook
python -m manim -ql manim_scenes/scene_02_perfect_six.py Scene02PerfectSix
python -m manim -ql manim_scenes/scene_03_hexagon_order.py Scene03HexagonOrder
python -m manim -ql manim_scenes/scene_04_prime_outsider.py Scene04PrimeOutsider
python -m manim -ql manim_scenes/scene_05_heptagon_impossibility.py Scene05HeptagonImpossibility
python -m manim -ql manim_scenes/scene_06_decimal_cycle.py Scene06DecimalCycle
python -m manim -ql manim_scenes/scene_07_cyclic_number.py Scene07CyclicNumber
python -m manim -ql manim_scenes/scene_08_synthesis.py Scene08Synthesis
python -m manim -ql manim_scenes/scene_09_subscribe.py Scene09Subscribe
```

High definition:

```bash
python -m manim -qh manim_scenes/scene_01_hook.py Scene01Hook
python -m manim -qh manim_scenes/scene_02_perfect_six.py Scene02PerfectSix
python -m manim -qh manim_scenes/scene_03_hexagon_order.py Scene03HexagonOrder
python -m manim -qh manim_scenes/scene_04_prime_outsider.py Scene04PrimeOutsider
python -m manim -qh manim_scenes/scene_05_heptagon_impossibility.py Scene05HeptagonImpossibility
python -m manim -qh manim_scenes/scene_06_decimal_cycle.py Scene06DecimalCycle
python -m manim -qh manim_scenes/scene_07_cyclic_number.py Scene07CyclicNumber
python -m manim -qh manim_scenes/scene_08_synthesis.py Scene08Synthesis
python -m manim -qh manim_scenes/scene_09_subscribe.py Scene09Subscribe
```

## Render Full Video

Fast preview:

```bash
python main.py full -q l
```

Final 1080p render:

```bash
python main.py full -q h --fps 30 -o why_6_is_perfect_and_7_is_mysterious
```

Equivalent direct command:

```bash
python -m manim -qh --fps 30 manim_scenes/full_video.py FullVideo -o why_6_is_perfect_and_7_is_mysterious
```

## Project Files

- `concept_summary.md`: scientific explanation and references.
- `narration_script.md`: timestamped narration, starting with the required 6-7 trend line.
- `youtube_package.md`: titles, description, tags, hashtags, thumbnail ideas, pinned comment, and social post.
- `manim_scenes/`: all individual scenes plus the combined `FullVideo`.
- `utils/`: math helpers, motion helpers, and render CLI helpers.

## Scientific Notes

- `6` is perfect because its proper divisors are `1`, `2`, and `3`, and `1 + 2 + 3 = 6`.
- Regular hexagons tile the Euclidean plane because three 120-degree angles meet exactly at a point.
- `7` is prime and the regular heptagon is not compass-straightedge constructible.
- `1/7` produces the repeating cycle `142857`; multiplying `142857` by `1` through `6` rotates the digits.
- `7! = 5040`, which equals the number of minutes in half of a 7-day week, not a full week.
