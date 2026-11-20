"""Project-wide settings for *Beyond Ideal Gases*.

The film keeps the channel's visual contract: a true 16-by-9 logical canvas,
the Oceanic palette in which a colour always means the same thing, and one
large phone-readable type scale.

Scene lengths are not typed here. They are derived from the narration
(``narration.py``): each beat lasts as long as its words take to say at the
narrator's pace, plus a stated visual hold. So the script and the picture can
never drift apart, and ``python -m utils.timing_audit`` checks that every
scene lands exactly on its derived length.

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

import narration  # noqa: E402

PROJECT_TITLE = "Beyond Ideal Gases"
VIDEO_SUBTITLE = "How Molecules Become Liquids"
PROJECT_PART = "States of Matter — Part 2"
PROJECT_SLUG = "beyond-ideal-gases"
SERIES_LABEL = "Visual Chemistry · States of Matter · Part 2"
EPISODE_LABEL = "Part 2"

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
#   cyan          -> a gas (vapour) molecule; normal, stable motion
#   deep blue     -> liquid (the pool, its molecules, liquid regions of diagrams)
#   gold          -> velocity, the molecule we follow, a confirmed result
#   orange        -> momentum handed to a wall: wall hits, pressure pushes
#   teal          -> pressure (gauges, the pressure axis)
#   blue          -> volume
#   hot (coral)   -> temperature and heating
#   green         -> attraction (the a term); a valid result, a check mark
#   red           -> size and repulsion (the b term); a warning, a wrong idea
#   purple        -> limits and extremes: the critical point, supercritical fluid,
#                    idealised assumptions
#   white         -> the main equation
#   muted / gray  -> scaffolding: glass, grids, axes, guides
BG = "#041A2F"
PANEL = "#0A2540"
PANEL_2 = "#0D2B4A"
WHITE = "#F4FAFF"
MUTED = "#A7BCCB"
CYAN = "#8ED4FF"
BLUE = "#42C6FF"
TEAL = "#4FE0C8"
GREEN = "#78D98B"
GOLD = "#FFD166"
ORANGE = "#FF9F43"
RED = "#FF6B6B"
PURPLE = "#B69CFF"
ROSE = "#F78FB3"
GRAY = "#78909C"
HOT_COLOR = "#FF7A59"
COLD_COLOR = "#7FB8FF"

MOLECULE = CYAN
VAPOUR = CYAN
LIQUID = "#2F7FD8"
LIQUID_EDGE = "#7CC6FF"
COEXIST = "#7A9CF0"           # gas + liquid together (between the two phase colours)
FOLLOWED = GOLD
VELOCITY = GOLD
IMPULSE = ORANGE
PRESSURE = TEAL
VOLUME = BLUE
TEMPERATURE = HOT_COLOR
AMOUNT = ROSE
ATTRACT = GREEN
REPEL = RED
SIZE = RED
RESULT = GOLD
WARNING = RED
LIMIT = PURPLE
CRITICAL = PURPLE
SUPERCRITICAL = PURPLE
EVAPORATE = GOLD              # a molecule leaving the liquid
CONDENSE = LIQUID_EDGE        # a molecule captured by the liquid
GLASS = "#9FD8F5"
GRID = "#2C5A7A"
STEEL = "#8FA6B8"
SLOW = "#4F8DFF"              # speed colour scale: slow ...
FAST = "#FF8A3D"              # ... to fast

# Categorical colours for gases on charts (one per substance, film-wide).
GAS_COLORS: dict[str, str] = {
    "He": GOLD,
    "H2": "#EEF4F8",
    "N2": BLUE,
    "O2": ROSE,
    "CH4": ORANGE,
    "CO2": "#9BE7C4",
    "NH3": "#D7A6FF",
    "H2O": "#5BA8FF",
    "Cl2": "#C5E35A",
}

# Atom colours (CPK-like, tuned to the Oceanic background).
ATOM: dict[str, str] = {
    "H": "#EEF4F8",
    "C": "#5E6B78",
    "O": "#FF5D5D",
    "N": "#5B8CFF",
    "Cl": "#7BE07B",
    "He": "#F6C177",
}

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
    "transition": narration.TRANSITION,
    "title_hold": 3.0,
    "title_fade": 0.7,
}

# Each scene lands on exactly this many seconds, derived from its narration.
#   python -m utils.timing_audit       (animation lands on time)
#   python -m utils.narration_audit    (every beat can be spoken in its window)
SCENE_DURATIONS: dict[str, float] = dict(narration.DURATIONS)

# The eleven chapters of the brief, as YouTube chapter markers: (first scene, title).
YOUTUBE_CHAPTERS: list[tuple[str, str]] = [
    ("01", "The failure of the ideal gas"),
    ("03", "Maxwell–Boltzmann: why molecules have different speeds"),
    ("08", "Kinetic molecular theory"),
    ("10", "Real gas deviations"),
    ("13", "The van der Waals equation"),
    ("16", "The compressibility factor Z"),
    ("18", "Liquefaction and the critical point"),
    ("23", "Vapour pressure and boiling"),
    ("25", "Surface tension"),
    ("27", "Viscosity"),
    ("29", "Conclusion: the same molecules"),
]

RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "h",
    "fps": 30,
    "preview_fps": 15,
    "preview_resolution": "854,480",
    "resolution": "1920,1080",
}

SEED = 20261115


def _restore_arc_defaults() -> None:
    """Undo the one theme adjustment that would repaint every circle white.

    ``manim_themes`` pins ``Arc.set_default(stroke_color=WHITE)``. Because
    ``Circle`` forwards its ``color=`` down to ``Arc``, the pinned stroke wins
    and ``Circle(color=BLUE)`` would render with a white outline, erasing
    colour-as-meaning. The defaults are reset here and every stroke colour is
    stated at the point of use.
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
