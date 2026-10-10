"""Project-wide settings for *Periodic Trends, Explained Visually* (Part 4).

Part 4 continues Part 3 (*Why Does the Periodic Table Have This Shape?*). It
keeps that film's visual contract — a true 16-by-9 logical canvas, the Oceanic
palette in which a colour always means the same thing, one large phone-readable
type scale, and the four block colours — and adds the vocabulary this story
needs: a colour for inner (core) electrons, a colour for energy released versus
energy required, and one cool-to-warm scale for every heat map.

Importing this module also makes the repository root importable, so the shared
``themes`` package works from inside this sub-folder.
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import config as manim_config

PROJECT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_ROOT.parent

for _path in (str(PROJECT_ROOT), str(REPO_ROOT)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from themes.oceanic_next import apply_oceanic_next_theme, oceanic_bubbles  # noqa: E402

PROJECT_TITLE = "Periodic Trends, Explained Visually"
PROJECT_PART = "Atomic Structure · Part 4"
PROJECT_SLUG = "periodic-trends-explained-visually"
SERIES_LABEL = "Visualized Science"
VIDEO_SUBTITLE = "Why atoms shrink across the table, grow down it, and behave the way they do."

FONT_FAMILY = "Lato"  # Installed locally; open, clear letterforms at small sizes.
TITLE_FONT = "Lato"

FRAME_WIDTH = 16
FRAME_HEIGHT = 9
SAFE_WIDTH = 14.2
SAFE_HEIGHT = 7.6

# A true 16-by-9 logical canvas, not only a 16:9 pixel aspect ratio.
manim_config.frame_width = FRAME_WIDTH
manim_config.frame_height = FRAME_HEIGHT

# Oceanic palette. A colour always carries the same meaning across the film:
#   cyan / blue  -> outer (valence) electrons, the normal stable state
#   white        -> the central object or the main equation
#   green        -> a confirmed result; energy released; a closed shell
#   red / orange -> a broken expectation, an exception; energy required
#   purple       -> abstraction: Z_eff, the "felt" charge, model quantities
#   gold         -> the narrator's emphasis: headings, key numbers, the pull
#   muted / gray -> scaffolding, guides, inner (core) electrons
BG = "#041A2F"
PANEL = "#0A2540"
PANEL_2 = "#0D2B4A"
WHITE = "#F4FAFF"
MUTED = "#A7BCCB"
CYAN = "#8ED4FF"
BLUE = "#42C6FF"
GREEN = "#78D98B"
GOLD = "#FFD166"
ORANGE = "#FF9F43"
RED = "#FF6B6B"
PURPLE = "#B69CFF"
GRAY = "#78909C"

# Recurring physical objects keep Part 2 and Part 3's colours.
NUCLEUS_COLOR = RED
PROTON_COLOR = ORANGE
ELECTRON_COLOR = CYAN           # outer electrons: the ones every trend is about
CORE_COLOR = "#8AA4BC"          # inner electrons: background structure that shields
PULL_COLOR = GOLD               # the nucleus's attraction
ZEFF_COLOR = PURPLE             # the effective (felt) nuclear charge, a model quantity
SPIN_UP = CYAN
SPIN_DOWN = PURPLE
RELEASED = GREEN                # energy given out (negative enthalpy change)
REQUIRED = ORANGE               # energy that must be supplied
CATION = GOLD                   # the "+" badge of a positive ion
ANION = CYAN                    # the "−" badge of a negative ion

# The four blocks, exactly as Part 3 coloured them.
BLOCK_COLORS: dict[str, str] = {
    "s": BLUE,
    "p": GREEN,
    "d": GOLD,
    "f": PURPLE,
}

# One cool-to-warm scale for every heat map: low values deep and cool, high
# values warm and bright. The same stops are used for all four properties, so a
# switch of tab changes the data, never the meaning of a colour.
HEAT_STOPS: tuple[str, ...] = ("#17406A", "#1F78B4", "#42C6FF", "#8EE3C8", "#FFD166", "#FF9F43")
NO_DATA = "#2A4058"
TREND_ARROW = "#F38DFF"  # direction overlays stay distinct from property colours

FONT: dict[str, int] = {
    "hero": 76,
    "title": 60,
    "section": 50,
    "body": 42,
    "label": 38,
    "small": 34,
    # 30 is the smallest authored size for anything a viewer must actually read.
    "tiny": 30,
}

TIMING: dict[str, float] = {
    "quick": 0.45,
    "normal": 0.85,
    "slow": 1.4,
    "hold": 1.0,
    "transition": 0.55,
}

# Each chapter lands on exactly this many seconds; the narration beats in
# narration.py are timed inside these windows. Check without rendering:
#   python -m utils.timing_audit       (animation lands on time)
#   python -m utils.narration_audit    (every beat can be spoken in its window)
SCENE_DURATIONS: dict[str, float] = {
    "01": 62.0,
    "02": 75.0,
    "03": 65.0,
    "04": 85.0,
    "05": 91.0,
    "06": 80.0,
    "07": 74.0,
    "08": 51.0,
    "09": 74.0,
    "10": 68.0,
    "11": 85.0,
    "12": 62.0,
    "13": 66.0,
    "14": 62.0,
    "15": 64.0,
    "16": 84.0,
    "17": 74.0,
    "18": 145.0,
    "19": 43.0,
    "20": 10.0,
}

# Chapters that move the camera off the flat front view or draw lit 3D solids.
THREE_D_SCENES: frozenset[str] = frozenset({"06", "10", "15", "18"})

RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "h",
    "fps": 30,
    "preview_fps": 15,
    "preview_resolution": "854,480",
    "resolution": "1920,1080",
}

# Every electron cloud is a seeded random sample, so a render is reproducible
# frame for frame. Each cloud derives its own stream from this seed.
SEED = 20261009


def _restore_arc_defaults() -> None:
    """Undo the one theme adjustment that would repaint every circle white.

    ``manim_themes`` pins ``Arc.set_default(stroke_color=WHITE)``. Because
    ``Circle`` forwards its ``color=`` down to ``Arc``, the pinned stroke wins
    and ``Circle(color=BLUE)`` would render with a white outline. Nuclei,
    electrons, cloud dots, contours and ions in this film are all circles, so
    the defaults are reset here and every stroke colour is stated at the point
    of use.
    """
    from manim import AnnotationDot, Arc

    Arc.set_default()
    AnnotationDot.set_default()


def apply_project_theme(scene, bubbles: bool = False) -> None:
    """Apply the local Oceanic Next theme and optional subtle bubbles."""
    apply_oceanic_next_theme(scene)
    _restore_arc_defaults()
    from manim import Text

    Text.set_default(font=FONT_FAMILY)
    scene.camera.background_color = BG
    if bubbles:
        scene.add(oceanic_bubbles())
