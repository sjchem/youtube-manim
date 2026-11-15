"""Project-wide settings for *System of Particles & Rotational Motion*.

The film keeps the channel's visual contract: a true 16-by-9 logical canvas,
the Oceanic palette in which a colour always means the same thing, and one
large phone-readable type scale. It speaks Episodes 01 and 02's vocabulary
(position teal, velocity gold, acceleration orange, force green, angular
quantities cyan) and adds the colours of rotation: torque purple, angular
momentum rose, mass and moment of inertia periwinkle, energy coral, and a
glowing checkered target for every centre of mass.

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

PROJECT_TITLE = "System of Particles & Rotational Motion"
VIDEO_SUBTITLE = "From Forces to Rotation"
PROJECT_PART = "Visualized Physics — Episode 03"
PROJECT_SLUG = "rotational-motion"
SERIES_LABEL = "Visualized Physics — From Motion to the Quantum World"
EPISODE_LABEL = "Episode 03"

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
#   teal          -> position r, radius, lever arm (where something is)
#   gold          -> velocity and linear momentum; a confirmed result (boxed)
#   orange        -> (radial) acceleration
#   blue          -> tangential acceleration (this film only: purple is torque)
#   green         -> force; also "conserved / balanced" checks
#   purple        -> torque (r x F): the turning effect
#   cyan          -> angles and angular quantities: theta, omega, alpha, axes of spin
#   rose          -> angular momentum L
#   periwinkle    -> mass and moment of inertia (what resists)
#   coral         -> energy and work
#   red           -> a trap, a wrong prediction, a broken balance
#   white         -> the main equation; the centre-of-mass target
#   muted / gray  -> scaffolding: grids, guides, ground, axes of rotation
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
PERIWINKLE = "#8FA8FF"
CORAL = "#FF7A59"

POSITION = TEAL
VELOCITY = GOLD
MOMENTUM = GOLD
ACCEL = ORANGE
TANGENTIAL = BLUE
FORCE = GREEN
TORQUE = PURPLE
ANGLE = CYAN
OMEGA = CYAN
ANG_MOMENTUM = ROSE
MASS = PERIWINKLE
INERTIA = PERIWINKLE
ENERGY = CORAL
RESULT = GOLD
BALANCED = GREEN
WARNING = RED
COM_GLOW = "#FFE9A8"     # the warm halo around every centre-of-mass target
X_COLOR = BLUE
Y_COLOR = ROSE
Z_COLOR = PURPLE
GRID = "#2C5A7A"

# Materials of the 3D props (not meanings: just things).
STEEL = "#8FA6B8"
DISC_BODY = "#3E7CA6"     # solid discs and cylinders
DISC_STRIPE = "#9FD3F2"
RING_BODY = "#E0A26A"     # thin rings (copper)
WOOD = "#9A6A44"
WOOD_DARK = "#5E3E27"
ICE = "#BFE7FF"
BALL = "#FF8A5B"
SKIN = "#F2C29B"
SUIT = "#5E7CE2"

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
    ("01", "From particles to rigid bodies"),
    ("03", "Centre of mass"),
    ("06", "Motion of the centre of mass and momentum"),
    ("09", "The vector product"),
    ("11", "Torque and equilibrium"),
    ("14", "Moment of inertia"),
    ("18", "Rotational kinematics"),
    ("21", "Rotational dynamics, work and energy"),
    ("24", "Angular momentum and its conservation"),
    ("26", "Rolling motion"),
    ("29", "Linear and rotational motion, side by side"),
]

RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "h",
    "fps": 30,
    "preview_fps": 15,
    "preview_resolution": "854,480",
    "resolution": "1920,1080",
}

SEED = 20261113


def _restore_arc_defaults() -> None:
    """Undo the one theme adjustment that would repaint every circle white.

    ``manim_themes`` pins ``Arc.set_default(stroke_color=WHITE)``. Because
    ``Circle`` forwards its ``color=`` down to ``Arc``, the pinned stroke wins
    and ``Circle(color=BLUE)`` would render with a white outline. In a film
    full of wheels, rings and angle arcs that would erase colour-as-meaning,
    so the defaults are reset here and every stroke colour is stated at the
    point of use.
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
