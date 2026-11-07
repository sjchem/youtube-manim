"""Project-wide settings for *Circular Motion*.

The film keeps the channel's visual contract: a true 16-by-9 logical canvas,
the Oceanic palette in which a colour always means the same thing, and one
large phone-readable type scale. It speaks Episode 01's vocabulary (position
teal, velocity gold, acceleration orange, x blue, y rose) and adds three
colours of its own: net force green, tangential acceleration purple, and
angles and angular quantities cyan.

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

PROJECT_TITLE = "Circular Motion"
PROJECT_PART = "Visualized Physics — Episode 02"
PROJECT_SLUG = "circular-motion"
SERIES_LABEL = "Visualized Physics — From Motion to the Quantum World"
VIDEO_SUBTITLE = "Why Changing Direction Means Acceleration"
EPISODE_LABEL = "Episode 02"

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
#   teal          -> position r, the radius, displacement
#   gold          -> velocity (always tangent to the path)
#   orange        -> acceleration toward the centre, and every delta v
#   purple        -> tangential acceleration; time when it becomes an axis
#   green         -> net force (tension, friction, gravity doing the job)
#   cyan          -> angles and angular quantities: theta, omega, alpha, arcs
#   blue / rose   -> x and y components, as in Episode 01
#   red           -> a trap, a wrong prediction
#   white         -> the main equation
#   muted / gray  -> scaffolding: grids, guides, ground, the path
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
POSITION = TEAL
VELOCITY = GOLD
ACCEL = ORANGE
DELTA_V = ORANGE
TANGENTIAL = PURPLE
FORCE = GREEN
ANGLE = CYAN
TIME = PURPLE
RESULT = GOLD
WARNING = RED
BALL = "#FF8A5B"        # the particle: a warm ball that reads against every colour above
CAR = "#4FB3E8"
GROUND = "#3E6B5A"
GRID = "#2C5A7A"
ROAD = "#3A4A58"
EARTH = "#2F7FD1"

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
# narration.py are timed inside these windows. The seven chapters of the brief
# start at scenes 01, 03, 07, 12, 16, 21 and 24.
# Check without rendering:
#   python -m utils.timing_audit       (animation lands on time)
#   python -m utils.narration_audit    (every beat can be spoken in its window)
SCENE_DURATIONS: dict[str, float] = {
    "01": 82.0,    # Can you accelerate without speeding up?
    "02": 74.5,    # What is acceleration?
    "03": 91.5,    # Speed vs velocity
    "04": 67.5,    # Which way is it moving?
    "05": 91.0,    # Velocity in components (3D helix)
    "06": 79.5,    # One full lap (3D track)
    "07": 111.0,   # Where does delta v point?
    "08": 97.0,    # The velocity triangle
    "09": 111.0,   # Deriving v squared over r
    "10": 65.0,    # Speed and radius (3D tracks)
    "11": 107.0,   # Why doesn't it fall inward? (Newton's polygon)
    "12": 108.0,   # Angles and radians
    "13": 111.5,   # Angular velocity (3D turntable)
    "14": 93.5,    # Period and frequency
    "15": 57.5,    # Angular acceleration
    "16": 83.0,    # Centripetal force
    "17": 92.5,    # A ball on a string (3D table)
    "18": 131.5,   # Why cars need friction (3D curve)
    "19": 124.0,   # Why satellites orbit (3D Earth)
    "20": 93.0,    # Is there a centrifugal force?
    "21": 37.0,    # Uniform circular motion
    "22": 110.5,   # Speeding up on a circle (3D)
    "23": 44.5,    # Speed, direction, or both?
    "24": 110.0,   # Five challenges
    "25": 77.0,    # One chain of reasoning
    "26": 9.5,    # Subscribe
}

# The seven chapters of the brief, as YouTube chapter markers: (first scene, title).
YOUTUBE_CHAPTERS: list[tuple[str, str]] = [
    ("01", "Can you accelerate without speeding up?"),
    ("03", "Velocity and direction"),
    ("07", "Why circular motion requires acceleration"),
    ("12", "Angular motion"),
    ("16", "Centripetal acceleration and force"),
    ("21", "Uniform vs nonuniform circular motion"),
    ("24", "Thought experiments and conclusion"),
]

RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "h",
    "fps": 30,
    "preview_fps": 15,
    "preview_resolution": "854,480",
    "resolution": "1920,1080",
}

SEED = 20261105


def _restore_arc_defaults() -> None:
    """Undo the one theme adjustment that would repaint every circle white.

    ``manim_themes`` pins ``Arc.set_default(stroke_color=WHITE)``. Because
    ``Circle`` forwards its ``color=`` down to ``Arc``, the pinned stroke wins
    and ``Circle(color=BLUE)`` would render with a white outline. In a film
    about circles that would erase colour-as-meaning, so the defaults are
    reset here and every stroke colour is stated at the point of use.
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
