"""Project-wide settings for *Why Does the Periodic Table Have This Shape?* (Part 3).

Part 3 is the payoff of Part 2. It keeps that film's visual contract — a true
16-by-9 logical canvas, the Oceanic palette in which a colour always means the
same thing, and one large, phone-readable type scale — and adds the one new
piece of vocabulary this story needs: a colour for each of the four blocks.

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

PROJECT_TITLE = "Why Does the Periodic Table Have This Shape?"
PROJECT_PART = "Atomic Structure · Part 3"
PROJECT_SLUG = "why-does-the-periodic-table-have-this-shape"
SERIES_LABEL = "Visualized Science"
VIDEO_SUBTITLE = "Build the whole table from one question: where can the next electron go?"

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
#   cyan / blue  -> the normal, stable state; an electron with spin up
#   white        -> the central object or the main equation
#   green        -> a confirmed result, a full (closed) subshell
#   red / orange -> a contradiction, a broken expectation, an exception
#   purple       -> abstraction; an electron with spin down
#   gold         -> the narrator's emphasis: headings, questions, key numbers
#   muted / gray -> scaffolding, guides, secondary structure
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

# Recurring physical objects keep Part 2's colours.
NUCLEUS_COLOR = RED
PROTON_COLOR = ORANGE
NEUTRON_COLOR = GRAY
ELECTRON_COLOR = CYAN
SPIN_UP = CYAN
SPIN_DOWN = PURPLE

# Signs of a real angular function (never electric charge), as in Part 2.
PHASE_POS = CYAN
PHASE_NEG = PURPLE

# The four blocks. These are the only new colour claims in Part 3, and each
# one is used for exactly one subshell family from the first frame to the last.
BLOCK_COLORS: dict[str, str] = {
    "s": BLUE,
    "p": GREEN,
    "d": GOLD,
    "f": PURPLE,
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
    "transition": 0.55,
}

# Each chapter lands on exactly this many seconds; the narration beats in
# narration.py are timed inside these windows. Check without rendering:
#   python -m utils.timing_audit       (animation lands on time)
#   python -m utils.narration_audit    (every beat can be spoken in its window)
SCENE_DURATIONS: dict[str, float] = {
    "01": 50.0,
    "02": 70.0,
    "03": 75.0,
    "04": 135.0,
    "05": 97.0,
    "06": 134.0,
    "07": 99.0,
    "08": 75.0,
    "09": 117.0,
    "10": 88.0,
    "11": 93.0,
    "12": 83.0,
    "13": 85.0,
    "14": 87.0,
    "15": 65.0,
    "16": 10.0,
}

# Chapters that move the camera off the flat front view or draw lit 3D surfaces.
THREE_D_SCENES: frozenset[str] = frozenset({"01", "04", "08", "12", "14", "15", "16"})

RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "h",
    "fps": 30,
    "preview_fps": 15,
    "preview_resolution": "854,480",
    "resolution": "1920,1080",
}

SEED = 20261002


def _restore_arc_defaults() -> None:
    """Undo the one theme adjustment that would repaint every circle white.

    ``manim_themes`` pins ``Arc.set_default(stroke_color=WHITE)``. Because
    ``Circle`` forwards its ``color=`` down to ``Arc``, the pinned stroke wins
    and ``Circle(color=BLUE)`` would render with a white outline. Nuclei,
    electrons, shells and halos in this film are all circles, so the defaults
    are reset here and every stroke colour is stated at the point of use.
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
