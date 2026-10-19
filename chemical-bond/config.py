"""Project-wide settings for *Chemical Bonding, Explained Visually*.

This film follows *Periodic Trends, Explained Visually* (Atomic Structure,
Part 4) and opens the Chemical Bonding series. It keeps the channel's visual
contract — a true 16-by-9 logical canvas, the Oceanic palette in which a colour
always means the same thing, and one large phone-readable type scale — and adds
the vocabulary a bonding story needs: a colour for attraction versus
repulsion, one for energy, a pair for positive and negative ions, and one each
for sigma and pi overlap.

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

PROJECT_TITLE = "Chemical Bonding, Explained Visually"
PROJECT_PART = "Chemical Bonding · Part 1"
PROJECT_SLUG = "chemical-bonding-explained-visually"
SERIES_LABEL = "Visualized Science"
VIDEO_SUBTITLE = "Why atoms stick together — and why they share, transfer, or delocalise electrons."

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
#   cyan / blue  -> electrons and electron density, the normal stable state
#   teal         -> attraction, stabilisation, energy released
#   red / orange -> repulsion, a broken expectation, energy that must be supplied
#   gold         -> energy itself: curves, markers, the narrator's key numbers
#   white        -> the central object or the main equation
#   green        -> a confirmed result
#   purple       -> abstraction and model quantities; pi overlap
#   muted / gray -> scaffolding, guides, inner (core) electrons
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
COPPER = "#E9A178"

# Recurring physical objects.
NUCLEUS_COLOR = ORANGE          # warm nuclei, never mistaken for electron density
ELECTRON_COLOR = CYAN           # electron density, valence dots, the electron sea
CORE_COLOR = "#8AA4BC"          # inner electrons: background structure
ATTRACT = TEAL                  # attraction lines and stabilising arrows
REPEL = RED                     # repulsion lines and the steep wall
ENERGY = GOLD                   # the energy curve, its marker, energy numbers
RELEASED = TEAL                 # energy given out (bond forming, lattice forming)
REQUIRED = ORANGE               # energy that must be supplied (bond breaking, ionization)
CATION = PURPLE                 # positive ions and the delta-plus end of a polar bond
ANION = GREEN                   # negative ions and the delta-minus end
SIGMA_COLOR = BLUE              # head-on (sigma) overlap
PI_COLOR = PURPLE               # sideways (pi) overlap
PI_COLOR_2 = ROSE               # the second, perpendicular pi bond of N2
METAL_CORE = COPPER             # positive ion cores of a metal
SPIN_UP = CYAN
SPIN_DOWN = PURPLE

# The four blocks, exactly as the periodic-table films coloured them.
BLOCK_COLORS: dict[str, str] = {
    "s": BLUE,
    "p": GREEN,
    "d": GOLD,
    "f": PURPLE,
}

# Height colour for energy landscapes: deep (stable) is bright teal, the
# separated-atom plateau is deep blue, and the repulsive wall turns warm.
WELL_STOPS: tuple[str, ...] = ("#5FF3D6", "#2BB6C9", "#1F78B4", "#17406A", "#7A4A8C", "#FF9F43")

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
    "01": 50.0,    # 00:00 The invisible force
    "02": 50.0,    # 00:50 The promise
    "03": 75.0,    # 01:40 Pushes and pulls
    "04": 105.0,   # 02:55 The energy landscape (3D)
    "05": 95.0,    # 04:40 What is a stable bond?
    "06": 105.0,   # 06:15 Valence electrons and Lewis dots
    "07": 150.0,   # 08:00 Sharing electrons
    "08": 120.0,   # 10:30 Valence bond theory: overlap and sigma (3D)
    "09": 120.0,   # 12:30 Pi bonds and multiple bonds (3D)
    "10": 90.0,    # 14:30 Does electron transfer pay?
    "11": 90.0,    # 16:00 The crystal pays the bill
    "12": 120.0,   # 17:30 Bond polarity: a continuum
    "13": 90.0,    # 19:30 Metallic bonding
    "14": 150.0,   # 21:00 Bond length and strength
    "15": 90.0,    # 23:30 The octet rule's limits
    "16": 120.0,   # 25:00 Three bonds, one principle
    "17": 60.0,    # 27:00 Why does water bend? (3D)
    "18": 10.0,    # 28:00 Subscribe
}

# Chapters that move the camera off the flat front view or draw lit 3D solids.
THREE_D_SCENES: frozenset[str] = frozenset({"04", "08", "09", "17"})

RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "h",
    "fps": 30,
    "preview_fps": 15,
    "preview_resolution": "854,480",
    "resolution": "1920,1080",
}

# Every electron cloud and the electron sea are seeded random samples, so a
# render is reproducible frame for frame. Each cloud derives its own stream.
SEED = 20261016


def _restore_arc_defaults() -> None:
    """Undo the one theme adjustment that would repaint every circle white.

    ``manim_themes`` pins ``Arc.set_default(stroke_color=WHITE)``. Because
    ``Circle`` forwards its ``color=`` down to ``Arc``, the pinned stroke wins
    and ``Circle(color=BLUE)`` would render with a white outline. Nuclei, ions,
    electrons and cloud dots in this film are all circles, so the defaults are
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
