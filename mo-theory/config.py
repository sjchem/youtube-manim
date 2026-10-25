"""Project-wide settings for *Molecular Orbital Theory, Explained Visually*.

This film follows *Molecular Geometry, Explained Visually* (Chemical Bonding,
Part 2) and keeps the channel's visual contract: a true 16-by-9 logical
canvas, the Oceanic palette in which a colour always means the same thing,
and one large phone-readable type scale. It adds the vocabulary a molecular
orbital story needs: a pair of colours for the sign (phase) of a wave
function, one for electron density, one for bonding and one for antibonding
levels, and gold for the unpaired electrons the whole film is hunting for.

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

PROJECT_TITLE = "Molecular Orbital Theory, Explained Visually"
PROJECT_PART = "Chemical Bonding · Part 3"
PROJECT_SLUG = "molecular-orbital-theory-explained-visually"
SERIES_LABEL = "Visualized Science"
VIDEO_SUBTITLE = "Why is oxygen attracted to a magnet?"

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
#   blue / rose  -> the sign (phase) of a wave function: + and -, never charge
#   cyan         -> electron density |psi|^2, bonding levels, the stable state
#   orange / red -> antibonding levels and electrons, contradictions, warnings
#   gold         -> unpaired electrons and the narrator's key numbers
#   green        -> a confirmed result: a bond order, a prediction that holds
#   purple       -> the abstract and the extreme: N orbitals, the model's limits
#   white        -> the central object or the main equation
#   muted / gray -> scaffolding: axes, correlation lines, guides
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
PHASE_PLUS = BLUE          # where the wave function is positive
PHASE_MINUS = ROSE         # where it is negative
DENSITY = CYAN             # electron density, |psi| squared
BONDING = CYAN             # bonding MO levels and their electrons
ANTIBONDING = ORANGE       # antibonding MO levels and their electrons
ELECTRON = CYAN            # a paired electron (spin arrow)
UNPAIRED = GOLD            # an unpaired electron: the film's quarry
RESULT = GREEN             # a bond order found, a prediction confirmed
NODE = WHITE               # nodal planes and points (psi = 0)
AO_LEVEL = MUTED           # atomic orbital levels on the sides of a diagram
LIQUID_O2 = "#A9DDFF"      # liquid oxygen really is pale blue
LIQUID_N2 = "#E3EEF5"      # liquid nitrogen is colourless; drawn pale grey-white
PARAMAGNETIC = GOLD        # drawn into a magnetic field
DIAMAGNETIC = MUTED        # weakly pushed out of one

# Ball-and-stick colours, close to the conventional CPK scheme so a chemistry
# teacher recognises them, nudged to read on the navy background.
ELEMENT_COLORS: dict[str, str] = {
    "H": "#EEF4F8",
    "He": "#7FE3F0",
    "B": "#F5A97F",
    "C": "#9AA8B5",
    "N": "#5B8DEF",
    "O": "#FF6B6B",
    "F": "#A6E07A",
}

# Display radii in screen units at stage scale 1. Not to scale.
ELEMENT_RADII: dict[str, float] = {"H": 0.34, "He": 0.4, "B": 0.5, "C": 0.52, "N": 0.52, "O": 0.52, "F": 0.45}

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
    "01": 55.0,    # 00:00 Why is oxygen magnetic?
    "02": 95.0,    # 00:55 Two pictures of a bond
    "03": 80.0,    # 02:30 Waves add or cancel
    "04": 110.0,   # 03:50 Adding atomic waves (LCAO)
    "05": 85.0,    # 05:40 Bonding and antibonding shapes
    "06": 75.0,    # 07:05 Two energies
    "07": 80.0,    # 08:20 H2+: one electron, half a bond
    "08": 70.0,    # 09:40 H2: a full bond
    "09": 130.0,   # 10:50 Helium: when electrons cancel
    "10": 90.0,    # 13:00 Sigma from p orbitals
    "11": 90.0,    # 14:30 Pi orbitals come in pairs
    "12": 130.0,   # 16:00 Building the energy diagram
    "13": 120.0,   # 18:10 Two orderings
    "14": 95.0,    # 20:10 Filling nitrogen
    "15": 75.0,    # 21:45 Nitrogen's triple bond
    "16": 150.0,   # 23:00 Oxygen: where are they?
    "17": 120.0,   # 25:30 Mystery solved
    "18": 80.0,    # 27:30 Take one electron away
    "19": 80.0,    # 28:50 Add electrons instead
    "20": 75.0,    # 30:10 Boron and fluorine
    "21": 45.0,    # 31:25 Read the diagram
    "22": 110.0,   # 32:10 From waves to chemistry
    "23": 10.0,    # 34:00 Subscribe
}

RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "h",
    "fps": 30,
    "preview_fps": 15,
    "preview_resolution": "854,480",
    "resolution": "1920,1080",
}

# The only randomness — droplets in the liquid-oxygen pour and the jiggle of
# spins in a magnetic field — derives from this seed, so renders repeat.
SEED = 20261024


def _restore_arc_defaults() -> None:
    """Undo the one theme adjustment that would repaint every circle white.

    ``manim_themes`` pins ``Arc.set_default(stroke_color=WHITE)``. Because
    ``Circle`` forwards its ``color=`` down to ``Arc``, the pinned stroke wins
    and ``Circle(color=BLUE)`` would render with a white outline. Atoms,
    droplets and glows in this film are all drawn from circles, so the
    defaults are reset here and every stroke colour is stated at the point of use.
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
