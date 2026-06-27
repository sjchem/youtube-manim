# Manim Dark Theme Demos

This folder contains reusable dark Manim theme helpers and a small demo scene for
previewing each theme.

The helpers wrap `manim-themes`, which loads iTerm2 color schemes and applies
them to a Manim scene.

## Available themes

- `Molokai`
- `Oceanic Next` with a deeper custom background
- `Dracula`

## Requirements

Install the theme dependency in the same environment where Manim is installed:

```bash
pip install manim manim-themes
```

On the first render for a theme, `manim-themes` downloads that theme's
`.itermcolors` file from the iTerm2 color schemes repository. Downloaded files
are cached in `themes/iTerm2Themes/`.

## Usage

Import and apply one of the wrapper functions in your scene's `setup` method:

```python
from manim import *

from themes import apply_molokai_theme

class MyScene(Scene):
    def setup(self):
        apply_molokai_theme(self)

    def construct(self):
        text = Text("Dark theme example")
        self.play(FadeIn(text))
```

For the Oceanic Next look you use most often, import from the dedicated module:

```python
from manim import *

from themes.oceanic_next import apply_oceanic_next_theme, oceanic_bubbles

class MyScene(Scene):
    def setup(self):
        apply_oceanic_next_theme(self)

    def construct(self):
        self.add(oceanic_bubbles())
        text = Text("Oceanic Next example")
        self.play(FadeIn(text))
```

If you want the theme and bubble background every time, use the convenience
helper in `setup`:

```python
from manim import *

from themes.oceanic_next import apply_oceanic_next_scene

class MyScene(Scene):
    def setup(self):
        apply_oceanic_next_scene(self)

    def construct(self):
        text = Text("Ready to animate")
        self.play(FadeIn(text))
```

If you prefer a different theme name, use `apply_dark_theme` directly:

```python
from manim import *

from themes import apply_dark_theme

class MyScene(Scene):
    def setup(self):
        apply_dark_theme(self, "Dracula")
```

## Demo Scene

The demo scene in `themes/demo_themes.py` renders a title, subtitle, and a few
colored mobjects using the selected theme. The Oceanic Next demo also adds a
subtle layer of faded light grey bubbles over the darker background.

Run one demo scene from the repository root with:

```bash
python -m manim -pql themes/demo_themes.py MolokaiThemeDemo
python -m manim -pql themes/demo_themes.py OceanicNextThemeDemo
python -m manim -pql themes/demo_themes.py DraculaThemeDemo
```

If your terminal is already in this `themes/` directory, include the parent
folder on `PYTHONPATH` and use the local file path:

```bash
PYTHONPATH=.. python -m manim -pql demo_themes.py MolokaiThemeDemo
PYTHONPATH=.. python -m manim -pql demo_themes.py OceanicNextThemeDemo
PYTHONPATH=.. python -m manim -pql demo_themes.py DraculaThemeDemo
```

To render without opening the preview player, drop `-p`:

```bash
python -m manim -ql themes/demo_themes.py MolokaiThemeDemo
```

Rendered videos are written under `media/videos/demo_themes/`.

This workspace includes a small root-level `manim_data_structures` compatibility
shim. The installed `manim-data-structures==0.1.4` package can fail during Manim
0.20.x plugin discovery on Python 3.12, and this project does not use that
plugin. Remove the shim if the upstream plugin is updated and imports cleanly.

## Demo scene classes

- `MolokaiThemeDemo`
- `OceanicNextThemeDemo`
- `DraculaThemeDemo`

## Theme storage

Themes are downloaded into `themes/iTerm2Themes` inside this folder, so each
scene can reuse the same cached theme assets.
