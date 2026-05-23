# The Calculus of Genius

A complete Manim Community Edition project for a cinematic 5-6 minute educational YouTube video:

**The calculus of genius**  
**Thesis:** Genius is not lightning from nowhere. It is probability, recombination, time, and controlled chaos.

The project uses a dark scientific visual style: glowing particles, equations, probability graphics, Zipf-like bars, combinatorial networks, compounding curves, and native fallback particle simulations. It tries to import `manim-physics` through `utils/particles.py`; if unavailable, the project continues with native Manim systems.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Render Individual Scene

```bash
manim -pqh scenes/scene_02_probability.py ProbabilityScene
```

## Render All Scenes

```bash
manim -pqh main.py CombinedScene
```

## High Quality Render

```bash
manim -p -r 1920,1080 --fps 60 main.py CombinedScene
```

## Batch Render Individual Scenes

```bash
chmod +x render.sh
./render.sh
```

Optional knobs:

```bash
QUALITY=qm FPS=30 ./render.sh
QUALITY=qh FPS=60 ./render.sh
```

## Scene Classes

- `TitleScene`
- `HookScene`
- `ProbabilityScene`
- `ZipfScene`
- `CombinatorialScene`
- `CompoundTimeScene`
- `EdgeOfChaosScene`
- `DiminishingReturnsScene`
- `FinalFormulaScene`
- `CombinedScene`

## Notes

- Run commands from the project root: `CALCULUS-OF-GENIUS/`.
- No paid assets or external images are required.
- `assets/audio`, `assets/images`, and `assets/fonts` are placeholders for optional production additions.
- The narration and shot plan live in `scripts/voiceover_script.md` and `scripts/shot_list.md`.
- If `manim-physics` fails to install on your system, remove it from `requirements.txt`; the project will still render with native fallback particles.

