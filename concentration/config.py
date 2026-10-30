"""Project-wide settings for *Concentration, Explained Visually*.

The film keeps the channel's visual contract: a true 16-by-9 logical canvas,
the Oceanic palette in which a colour always means the same thing, and one
large phone-readable type scale. Its own vocabulary is the brief's: solute
gold, solvent blue, the solution's volume purple, the things we count teal.

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

PROJECT_TITLE = "Concentration, Explained Visually"
PROJECT_PART = "Visual Chemistry"
PROJECT_SLUG = "concentration-explained-visually"
SERIES_LABEL = "Visualized Science"
VIDEO_SUBTITLE = "Molarity, Molality, Normality, Mole Fraction & More"

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
#   gold          -> the solute (glucose, acid, ethanol, a trace contaminant)
#   blue          -> the solvent (water) and its particles
#   cyan          -> the solvent's *mass* (a balance reading under molality)
#   purple        -> the solution's volume: outlines, flasks filled to the mark
#   rose          -> the solution's total mass (mass percent, density)
#   teal          -> what we count: moles, equivalents, mole fractions
#   green         -> a confirmed result
#   red / orange  -> a trap, a wrong denominator, heat
#   white         -> the main equation
#   muted / gray  -> scaffolding: axes, glass, guides
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

SOLUTE = GOLD
SOLUTE_DEEP = "#FFB13B"      # body colour of a glucose particle (gold, a touch warmer)
SOLVENT = BLUE
SOLVENT_MASS = CYAN
VOLUME = PURPLE
SOLUTION_MASS = ROSE
AMOUNT = TEAL
EQUIVALENT = TEAL
RESULT = GREEN
WARNING = RED
HEAT = ORANGE
GLASS = "#CFE8F7"
LIQUID = "#2E8FD0"
ETHANOL = "#FFE29A"

# Ball-and-stick colours, close to the conventional CPK scheme.
ELEMENT_COLORS: dict[str, str] = {
    "H": "#EEF4F8",
    "C": "#8E9BA8",
    "O": "#FF6B6B",
    "S": "#FFD84D",
    "Na": "#B69CFF",
}
# Display radii in screen units at stage scale 1 (not to scale).
ELEMENT_RADII: dict[str, float] = {"H": 0.2, "C": 0.32, "O": 0.33, "S": 0.42, "Na": 0.4}

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

# Each scene lands on exactly this many seconds; the narration beats in
# narration.py are timed inside these windows. The twelve YouTube chapters of
# the brief start at scenes 01, 02, 04, 06, 08, 10, 12, 14, 16, 17, 19, 20.
# Check without rendering:
#   python -m utils.timing_audit       (animation lands on time)
#   python -m utils.narration_audit    (every beat can be spoken in its window)
SCENE_DURATIONS: dict[str, float] = {
    "01": 105.0,   # 00:00 The mystery: one glass, four answers
    "02": 70.0,    # 01:45 Counting in moles
    "03": 65.0,    # 02:55 Mass adds, volume doesn't
    "04": 130.0,   # 04:00 Molarity: moles per litre of solution
    "05": 125.0,   # 06:10 Making a solution to the mark
    "06": 120.0,   # 08:15 Molality: swap the denominator
    "07": 105.0,   # 10:15 Where molality matters
    "08": 120.0,   # 12:00 The temperature experiment
    "09": 90.0,    # 14:00 Why chemists need both
    "10": 120.0,   # 15:30 Normality: counting equivalents
    "11": 120.0,   # 17:30 One acid, two normalities
    "12": 110.0,   # 19:30 Mole fraction: pick a molecule
    "13": 85.0,    # 21:20 Fractions add to one
    "14": 105.0,   # 22:45 Percent by mass, percent w/v
    "15": 90.0,    # 24:30 Percent by volume, grams per litre
    "16": 130.0,   # 26:00 One part per million
    "17": 95.0,    # 28:10 Density connects them
    "18": 90.0,    # 29:45 Dilution
    "19": 155.0,   # 31:15 Five concentration traps
    "20": 60.0,    # 33:50 The concentration map
    "21": 10.0,    # 34:50 Subscribe
}

# The twelve chapters of the brief, as YouTube chapter markers: (first scene, title).
YOUTUBE_CHAPTERS: list[tuple[str, str]] = [
    ("01", "The mystery of concentration"),
    ("02", "What are we actually measuring?"),
    ("04", "Molarity: counting moles in space"),
    ("06", "Molality: counting moles against mass"),
    ("08", "Molarity vs molality: the temperature experiment"),
    ("10", "Normality: when the reaction changes the answer"),
    ("12", "Mole fraction: a molecular population view"),
    ("14", "Three ways to say percent"),
    ("16", "ppm and ppb: chemistry at tiny scales"),
    ("17", "Conversions and dilution"),
    ("19", "Five concentration traps"),
    ("20", "The concentration map"),
]

RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "h",
    "fps": 30,
    "preview_fps": 15,
    "preview_resolution": "854,480",
    "resolution": "1920,1080",
}

# The only randomness — particle homes in every swarm and the random picks of
# the mole-fraction chapter — derives from this seed, so renders repeat.
SEED = 20261027


def _restore_arc_defaults() -> None:
    """Undo the one theme adjustment that would repaint every circle white.

    ``manim_themes`` pins ``Arc.set_default(stroke_color=WHITE)``. Because
    ``Circle`` forwards its ``color=`` down to ``Arc``, the pinned stroke wins
    and ``Circle(color=BLUE)`` would render with a white outline. Particles,
    rings and glows in this film are all circles, so the defaults are reset
    here and every stroke colour is stated at the point of use.
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
