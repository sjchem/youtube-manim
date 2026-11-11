"""Project-wide settings for *The Molecular Dance*.

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

PROJECT_TITLE = "The Molecular Dance"
VIDEO_SUBTITLE = "From Invisible Forces to the Gas Laws"
PROJECT_PART = "States of Matter — Part 1"
PROJECT_SLUG = "molecular-dance"
SERIES_LABEL = "Visual Chemistry · States of Matter"
EPISODE_LABEL = "Part 1"

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
#   cyan          -> a gas molecule; normal, stable motion
#   gold          -> velocity (and the molecule we follow)
#   orange        -> momentum handed to a wall: impulse, push, force on the wall
#   teal          -> pressure (gauges, the pressure axis)
#   blue          -> volume
#   hot (coral)   -> temperature and heating
#   rose          -> amount of gas, n
#   green         -> attraction, a confirmed result
#   red           -> repulsion, a trap or a wrong prediction
#   purple        -> limits and extrapolation: absolute zero, "ideal" assumptions
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

MOLECULE = CYAN
FOLLOWED = GOLD
VELOCITY = GOLD
IMPULSE = ORANGE
PRESSURE = TEAL
VOLUME = BLUE
TEMPERATURE = HOT_COLOR
AMOUNT = ROSE
ATTRACT = GREEN
REPEL = RED
RESULT = GOLD
WARNING = RED
LIMIT = PURPLE
X_COLOR = BLUE
Y_COLOR = ROSE
Z_COLOR = PURPLE
GLASS = "#9FD8F5"
GRID = "#2C5A7A"
STEEL = "#8FA6B8"
DELTA_PLUS = BLUE        # electron-poor end
DELTA_MINUS = RED        # electron-rich end
CLOUD = "#7FC8F8"        # electron clouds

# Two gases sharing a box (Dalton) and the gases compared in Avogadro's chapter.
N2_COLOR = BLUE
O2_COLOR = ROSE
HE_COLOR = GOLD
CO2_COLOR = GREEN

# Atom colours (CPK-like, tuned to the Oceanic background).
ATOM: dict[str, str] = {
    "H": "#EEF4F8",
    "O": "#FF5D5D",
    "N": "#5B8CFF",
    "Cl": "#7BE07B",
    "S": "#F2D25C",
    "He": "#F6C177",
    "Ne": "#FF8FA3",
    "Ar": "#9D8CFF",
    "Kr": "#6FD3E8",
    "Xe": "#5BA8FF",
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
    ("01", "The invisible world of gases"),
    ("03", "Intermolecular forces"),
    ("08", "Thermal energy and states of matter"),
    ("10", "Where gas pressure comes from"),
    ("15", "Boyle's law"),
    ("18", "Charles' law and absolute zero"),
    ("21", "Gay-Lussac's law"),
    ("23", "Avogadro's law"),
    ("25", "The ideal gas equation"),
    ("28", "Dalton's law of partial pressures"),
    ("30", "When the ideal gas model stops working"),
]

RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "h",
    "fps": 30,
    "preview_fps": 15,
    "preview_resolution": "854,480",
    "resolution": "1920,1080",
}

SEED = 20261109


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
