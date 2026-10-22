"""Project-wide settings for *Molecular Geometry, Explained Visually*.

This film follows *Chemical Bonding, Explained Visually* (Chemical Bonding,
Part 1) and keeps the channel's visual contract: a true 16-by-9 logical
canvas, the Oceanic palette in which a colour always means the same thing,
and one large phone-readable type scale. It adds the vocabulary a geometry
story needs: one colour for bonding electron regions, one for lone pairs, one
for angles, a pair for orbital phase, and a pair for bond and molecular
dipoles.

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

PROJECT_TITLE = "Molecular Geometry, Explained Visually"
PROJECT_PART = "Chemical Bonding · Part 2"
PROJECT_SLUG = "molecular-geometry-explained-visually"
SERIES_LABEL = "Visualized Science"
VIDEO_SUBTITLE = "Why CO₂ is straight, H₂O is bent, and CH₄ is a tetrahedron."

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
#   cyan / blue  -> bonding electron regions, the normal stable state
#   purple       -> lone pairs: present, space-filling, never an atom
#   gold         -> angles: arcs, degree values, the narrator's key numbers
#   white        -> the central object or the main equation
#   green        -> a confirmed result (a shape revealed, a vector sum found)
#   red / orange -> repulsion and crowding, a wrong guess; orange bond dipoles
#   rose         -> the negative phase of an orbital wave function
#   muted / gray -> scaffolding, guides, the cube, historical labels
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

# Recurring ideas.
DOMAIN_COLOR = CYAN        # a bonding electron region (single, double or triple bond)
LONE_PAIR_COLOR = PURPLE   # a lone pair on the central atom, in 2D dots and 3D lobes
ANGLE_COLOR = GOLD         # angle arcs and degree values
REPEL = RED                # crowding: 90-degree contacts, the flat-square guess
RESULT = GREEN             # a shape name revealed, a vector sum found
PHASE_PLUS = BLUE          # orbital lobes where the wave function is positive
PHASE_MINUS = ROSE         # orbital lobes where it is negative
UNHYBRID = PURPLE          # p orbitals left out of the mix (ready for pi bonds)
PI_COLOR = PURPLE          # sideways (pi) overlap, as in Part 1
SIGMA_COLOR = BLUE         # head-on (sigma) overlap, as in Part 1
H_ORBITAL = TEAL           # a hydrogen 1s orbital arriving to overlap
BOND_DIPOLE = ORANGE       # one bond's dipole arrow (points to the stronger pull)
NET_DIPOLE = GREEN         # the vector sum: the molecule's overall dipole
DELTA_PLUS = PURPLE        # partial charges, coloured as in Part 1
DELTA_MINUS = GREEN

# Ball-and-stick colours, close to the conventional CPK scheme so a chemistry
# teacher recognises them, nudged to read on the navy background.
ELEMENT_COLORS: dict[str, str] = {
    "H": "#EEF4F8",
    "B": "#F5A97F",
    "C": "#9AA8B5",
    "N": "#5B8DEF",
    "O": "#FF6B6B",
    "F": "#A6E07A",
    "P": "#FF9F43",
    "S": "#F2D45C",
    "Cl": "#4CC38A",
    "Br": "#C2583F",
    "Xe": "#5FD0D6",
    "A": "#F4FAFF",        # a generic central atom in the VSEPR chapters
}

# Display radii in screen units at stage scale 1. Not to scale: they are
# chosen so a central atom reads clearly and never hides its bonds.
ELEMENT_RADII: dict[str, float] = {
    "H": 0.34, "B": 0.5, "C": 0.52, "N": 0.52, "O": 0.52, "F": 0.45,
    "P": 0.6, "S": 0.6, "Cl": 0.52, "Br": 0.57, "Xe": 0.64, "A": 0.42,
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
    "01": 50.0,    # 00:00 The shape mystery
    "02": 85.0,    # 00:50 Lewis structures are flat
    "03": 80.0,    # 02:15 Electron regions push apart
    "04": 55.0,    # 03:35 Counting regions
    "05": 75.0,    # 04:30 Linear and trigonal planar
    "06": 90.0,    # 05:45 The tetrahedron
    "07": 105.0,   # 07:15 Ammonia: one lone pair
    "08": 125.0,   # 09:00 Water: two lone pairs
    "09": 75.0,    # 11:05 Five electron regions
    "10": 100.0,   # 12:20 One family, four shapes
    "11": 60.0,    # 14:00 Six electron regions
    "12": 90.0,    # 15:00 Flat from six
    "13": 90.0,    # 16:30 Mixing orbitals
    "14": 100.0,   # 18:00 sp, sp2 and sp3
    "15": 80.0,    # 19:40 Methane and ethene
    "16": 60.0,    # 21:00 Two models, one molecule
    "17": 80.0,    # 22:00 Bond dipoles
    "18": 85.0,    # 23:20 Symmetry decides polarity
    "19": 105.0,   # 24:45 Predict the shape
    "20": 55.0,    # 26:30 Molecules live in 3D
    "21": 25.0,    # 27:25 Why is oxygen magnetic?
    "22": 10.0,    # 27:50 Subscribe
}

RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "h",
    "fps": 30,
    "preview_fps": 15,
    "preview_resolution": "854,480",
    "resolution": "1920,1080",
}

# The only randomness — the starting jitter of the repulsion demo and the
# liquid-oxygen droplets — derives from this seed, so renders are repeatable.
SEED = 20261020


def _restore_arc_defaults() -> None:
    """Undo the one theme adjustment that would repaint every circle white.

    ``manim_themes`` pins ``Arc.set_default(stroke_color=WHITE)``. Because
    ``Circle`` forwards its ``color=`` down to ``Arc``, the pinned stroke wins
    and ``Circle(color=BLUE)`` would render with a white outline. Atoms, lobes
    and rims in this film are all drawn from circles, so the defaults are
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
