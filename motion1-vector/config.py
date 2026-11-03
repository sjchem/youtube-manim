"""Project-wide settings for *Vectors & Projectile Motion*.

The film keeps the channel's visual contract: a true 16-by-9 logical canvas,
the Oceanic palette in which a colour always means the same thing, and one
large phone-readable type scale. Its own vocabulary: horizontal is blue,
vertical is rose, velocity is gold, acceleration (gravity) is orange.

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

PROJECT_TITLE = "Vectors & Projectile Motion"
PROJECT_PART = "Visualized Physics — Episode 01"
PROJECT_SLUG = "vectors-and-projectile-motion"
SERIES_LABEL = "Visualized Physics — From Motion to the Quantum World"
VIDEO_SUBTITLE = "The Geometry of 2D Motion"

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
#   blue          -> horizontal: the x-axis, i-hat, A_x, v_x, the floor shadow
#   rose          -> vertical: the y-axis, j-hat, A_y, v_y, the wall shadow
#   gold          -> velocity, and the first vector A of a sum
#   purple        -> the second vector B of a sum; time as an axis
#   green         -> a resultant, a confirmed result
#   teal          -> position and displacement
#   orange        -> acceleration and gravity
#   red           -> a trap, a wrong answer
#   white         -> the main equation
#   muted / gray  -> scaffolding: grids, guides, ground
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

X_COLOR = BLUE
Y_COLOR = ROSE
VELOCITY = GOLD
VEC_A = GOLD
VEC_B = PURPLE
RESULT = GREEN
POSITION = TEAL
ACCEL = ORANGE
TIME = PURPLE
WARNING = RED
BALL = "#FF8A5B"        # the projectile: a warm ball that reads against every colour above
GROUND = "#3E6B5A"
GRID = "#2C5A7A"

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
    "title_hold": 3.0,
    "title_fade": 0.7,
}

# Each scene lands on exactly this many seconds; the narration beats in
# narration.py are timed inside these windows. The nine chapters of the brief
# start at scenes 01, 03, 06, 09, 11, 14, 18, 24 and 27.
# Check without rendering:
#   python -m utils.timing_audit       (animation lands on time)
#   python -m utils.narration_audit    (every beat can be spoken in its window)
SCENE_DURATIONS: dict[str, float] = {
    "01": 80.0,    # 00:00 Can we predict a flight?
    "02": 70.0,    # 01:20 Position, velocity, acceleration
    "03": 90.0,    # 02:30 Scalars
    "04": 95.0,    # 04:00 Vectors
    "05": 110.0,   # 05:35 Distance vs displacement
    "06": 100.0,   # 07:25 Why add vectors?
    "07": 135.0,   # 09:05 Triangle and parallelogram laws (drone)
    "08": 120.0,   # 11:20 Vector subtraction, delta v
    "09": 95.0,    # 13:20 Scalar multiplication
    "10": 85.0,    # 14:55 Unit vectors
    "11": 85.0,    # 16:20 Why resolve a vector?
    "12": 110.0,   # 17:45 Components from sine and cosine
    "13": 100.0,   # 19:35 Adding by components
    "14": 80.0,    # 21:15 Position and displacement
    "15": 100.0,   # 22:35 Velocity
    "16": 85.0,    # 24:15 Acceleration
    "17": 95.0,    # 25:40 Equations of motion
    "18": 70.0,    # 27:15 What is projectile motion?
    "19": 65.0,    # 28:25 Launch velocity
    "20": 70.0,    # 29:30 Horizontal motion
    "21": 67.0,    # 30:40 Vertical motion (3D shadows)
    "22": 65.0,    # 31:47 The highest point
    "23": 95.0,    # 32:52 Why a parabola? (space-time 3D)
    "24": 100.0,   # 34:27 Flight time and maximum height
    "25": 80.0,    # 36:07 Range
    "26": 95.0,    # 37:27 Why 45 degrees, and when it fails
    "27": 100.0,   # 39:02 Five conceptual challenges
    "28": 50.0,    # 40:42 Motion -> prediction, and what's next
    "29": 10.0,    # 41:32 Subscribe
}

# The nine chapters of the brief, as YouTube chapter markers: (first scene, title).
YOUTUBE_CHAPTERS: list[tuple[str, str]] = [
    ("01", "Can we predict a flying ball?"),
    ("03", "Scalars and vectors"),
    ("06", "Vector addition and subtraction"),
    ("09", "Scalar multiplication and unit vectors"),
    ("11", "Vector components and resolution"),
    ("14", "Kinematics in 1D and 2D"),
    ("18", "Projectile motion"),
    ("24", "Flight time, maximum height and range"),
    ("27", "Conceptual challenges and conclusion"),
]

RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "h",
    "fps": 30,
    "preview_fps": 15,
    "preview_resolution": "854,480",
    "resolution": "1920,1080",
}

SEED = 20261031


def _restore_arc_defaults() -> None:
    """Undo the one theme adjustment that would repaint every circle white.

    ``manim_themes`` pins ``Arc.set_default(stroke_color=WHITE)``. Because
    ``Circle`` forwards its ``color=`` down to ``Arc``, the pinned stroke wins
    and ``Circle(color=BLUE)`` would render with a white outline. Unit
    circles, angle arcs and the running track are all arcs, so the defaults
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
