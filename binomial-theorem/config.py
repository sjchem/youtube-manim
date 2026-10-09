"""Project-wide settings for *Why Does Pascal's Triangle Know Algebra?*

The film keeps the channel's visual contract — a true 16-by-9 logical canvas,
the Oceanic palette in which a colour always means the same thing, and one
large, phone-readable type scale — and adds the one piece of vocabulary this
story needs: a colour for each side of a binomial.

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

PROJECT_TITLE = "Why Does Pascal's Triangle Know Algebra?"
PROJECT_PART = "Binomial Theorem Visualized"
PROJECT_SLUG = "binomial-theorem-visualized"
SERIES_LABEL = "Visualized Mathematics"
VIDEO_SUBTITLE = "Pascal's Triangle, combinations and coefficients: one counting structure."

FONT_FAMILY = "Lato"  # Installed locally; open, clear letterforms at small sizes.

FRAME_WIDTH = 16
FRAME_HEIGHT = 9
SAFE_WIDTH = 14.2
SAFE_HEIGHT = 7.6

# A true 16-by-9 logical canvas, not only a 16:9 pixel aspect ratio.
manim_config.frame_width = FRAME_WIDTH
manim_config.frame_height = FRAME_HEIGHT

# Oceanic palette. A colour always carries the same meaning across the film:
#   cyan / blue  -> normal maths, stable structure
#   white        -> the main equation or central object
#   green        -> a confirmed result: "it checks out"
#   red / orange -> brute force, overload, a warning
#   purple       -> abstraction and limits: general n, the bell curve
#   gold         -> coefficients and counts — the numbers the film is about
#   muted / gray -> scaffolding, guides, secondary structure
BG = "#041A2F"
PANEL = "#0A2540"
PANEL_2 = "#0D2B4A"
WHITE = "#F4FAFF"
MUTED = "#C2D3DF"
CYAN = "#8ED4FF"
BLUE = "#67D5FF"
GREEN = "#78D98B"
GOLD = "#FFD166"
ORANGE = "#FF9F43"
RED = "#FF6B6B"
PURPLE = "#B69CFF"
GRAY = "#9FB6C4"
ROSE = "#FFA6CC"

# Keep supporting symbols readable while an active symbol is highlighted.
# Fades to zero still remove objects; this applies only to readable context.
CONTEXT_OPACITY = 0.8

# The two sides of the binomial. These are the film's only new colour claims,
# and they never change: every a, every left step and every head is blue;
# every b, every right step and every tail is rose. A mix of the two means
# "some of each" (the cube's slabs and beams).
A_COLOR = BLUE
B_COLOR = ROSE
COEF_COLOR = GOLD
LIMIT_COLOR = PURPLE

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
    "01": 64.0,
    "02": 96.0,
    "03": 102.0,
    "04": 115.0,
    "05": 128.0,
    "06": 131.0,
    "07": 99.0,
    "08": 101.0,
    "09": 111.0,
    "10": 110.0,
    "11": 116.0,
    "12": 100.0,
    "13": 10.0,
}

# Chapters that move the camera off the flat front view or draw lit 3D solids.
THREE_D_SCENES: frozenset[str] = frozenset({"03", "11"})

RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "h",
    "fps": 30,
    "preview_fps": 15,
    "preview_resolution": "854,480",
    "resolution": "1920,1080",
}

# Every random choice in the film (the Galton-board balls) comes from this seed,
# so a render is reproducible frame for frame.
SEED = 20261023


def _restore_arc_defaults() -> None:
    """Undo the one theme adjustment that would repaint every circle white.

    ``manim_themes`` pins ``Arc.set_default(stroke_color=WHITE)``. Because
    ``Circle`` forwards its ``color=`` down to ``Arc``, the pinned stroke wins
    and ``Circle(color=BLUE)`` would render with a white outline. Doors, coins,
    pegs and balls in this film are all circles, so the defaults are reset here
    and every stroke colour is stated at the point of use.
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
