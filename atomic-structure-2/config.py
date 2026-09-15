"""Project-wide settings for *Why Electrons Don't Orbit the Nucleus* (Part 2).

Part 1 established a visual contract: a fixed 16-by-9 logical canvas, an
Oceanic palette in which a colour always means the same thing, one type scale,
and narration windows that the animation is written against. This sequel keeps
that contract and adds the vocabulary the quantum chapters need -- a sign
convention for a real wave function, and a colour for a rejected arrangement.

The film is deliberately self-contained. It shares Part 1's palette and
conventions but does not import Part 1's ``config`` or the repository's
``themes`` package, so the folder renders on its own without module collisions.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from manim import config as manim_config

PROJECT_ROOT = Path(__file__).resolve().parent
ROOT = PROJECT_ROOT  # retained: utils and scenes address assets through cfg.ROOT

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

PROJECT_TITLE = "Why Electrons Don't Orbit the Nucleus"
PROJECT_PART = "Part 2"
PROJECT_SLUG = "why-electrons-dont-orbit-the-nucleus-part2"
SERIES_LABEL = "Visualized Science"
VIDEO_SUBTITLE = "The orbit disappears, and a quantum state takes its place."
TITLE = PROJECT_TITLE  # retained for older call sites

FRAME_WIDTH = 16
FRAME_HEIGHT = 9
SAFE_WIDTH = 14.2
SAFE_HEIGHT = 7.6

# A true 16-by-9 logical canvas, not merely a 16:9 pixel aspect ratio.
manim_config.frame_width = FRAME_WIDTH
manim_config.frame_height = FRAME_HEIGHT

# Oceanic palette, carried over from Part 1. A colour always carries the same
# meaning across the film.
#   cyan / blue  -> the normal, stable, currently trusted state
#   white        -> the central object or the main equation
#   green        -> a confirmed result, a selected ground-state arrangement
#   red / orange -> a contradiction, a rejected arrangement, a warning
#   purple       -> abstraction, quantum strangeness, the opposite wave sign
#   gold         -> the narrator's own emphasis: headings, questions, captions
#   muted / gray -> scaffolding, analogies, secondary structure
BG = "#041A2F"
PANEL = "#0A2540"
PANEL_2 = "#0D2B4A"
WHITE = "#F4FAFF"
MUTED = "#9DB5CA"
CYAN = "#8ED4FF"
BLUE = "#42C6FF"
GREEN = "#86E3A0"
GOLD = "#FFD166"
ORANGE = "#FF9F43"
RED = "#FF737A"
PURPLE = "#B69CFF"
GRAY = "#78909C"

# Recurring physical objects keep one colour for the whole film, so the eye
# never has to re-learn what it is looking at.
NUCLEUS_COLOR = RED
PROTON_COLOR = ORANGE
ELECTRON_COLOR = CYAN
PHOTON_COLOR = GOLD

# The two signs of a real spatial wave function. These are signs of amplitude.
# They are never a statement about electric charge, and the film says so on
# screen the first time both colours appear together.
PHASE_POS = CYAN
PHASE_NEG = PURPLE

# Lighting for the calculated isosurfaces. The shadow floor is deliberately
# lighter than BG: a face in full shadow must still separate from the
# background, otherwise a concave pinch reads as a hole through the atom.
SURFACE_SHADOW = "#16344F"
SURFACE_AMBIENT = 0.30

FONT: dict[str, int] = {
    "hero": 76,
    "title": 60,
    "section": 50,
    "body": 42,
    "label": 38,
    "small": 34,
    # 30 is the smallest authored size for anything a viewer must actually read.
    # At 1080p this stays legible on a phone without crowding the frame.
    "tiny": 30,
}

TIMING: dict[str, float] = {
    "quick": 0.45,
    "normal": 0.85,
    "slow": 1.4,
    "hold": 1.0,
    "transition": 0.55,
}

# Chapter registry: key, module slug, working title, planned seconds. The
# narration script carries the matching windows, and utils/audit.py refuses to
# pass if the two ever disagree.
SCENES: list[tuple[str, str, str, int]] = [
    ("01", "where_is_it", "Where is the electron?", 40),
    ("02", "what_survives", "What survived the orbit", 50),
    ("03", "bohr_numbers", "Everything is fixed", 100),
    ("04", "matter_waves", "Momentum becomes wavelength", 150),
    ("05", "one_at_a_time", "One electron at a time", 90),
    ("06", "waves_that_fit", "Waves that fit", 75),
    ("07", "uncertainty", "The price of locating a wave", 200),
    ("08", "allowed_states", "Which waves can exist?", 140),
    ("09", "born_probability", "From amplitude to detections", 175),
    ("10", "orbit_to_orbital", "A state replaces a path", 70),
    ("11", "orbital_shapes", "Shapes and missing probability", 225),
    ("12", "quantum_address", "An address for a quantum state", 260),
    ("13", "energy_landscape", "Other electrons change the energies", 150),
    ("14", "building_atoms", "Hydrogen, helium, lithium", 80),
    ("15", "filling_p", "Carbon and the capacity of p", 110),
    ("16", "chemistry", "Neon to sodium: a bridge to chemistry", 75),
    ("17", "potassium", "Potassium breaks the order", 80),
    ("18", "answer", "The answer to the opening question", 35),
    ("19", "subscribe", "Stay curious", 15),
]
DURATIONS: dict[str, int] = {key: seconds for key, _, _, seconds in SCENES}

# Chapters that open the 3D camera. Listed for the CLI and for reviewers; the
# camera helpers in common.py degrade safely wherever this is out of date.
THREE_D_SCENES: frozenset[str] = frozenset({"01", "02", "03", "08", "11", "12", "18"})

# The visual spine. Part 2 is one long transformation, and these are its
# stations; common.spine_strip() draws them and lights the current one.
SPINE: tuple[str, ...] = ("ORBIT", "WAVE", "PROBABILITY", "ORBITAL", "ATOM", "CHEMISTRY")

RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "h",
    "preview_fps": 15,
    "fps": 30,
    "resolution": "2560,1440",
}

SEED = 20260913

# Compression is for visual review only. Production keeps all narration windows.
SPEED = float(os.environ.get("ATOM_REVIEW_SPEED", "1"))
if SPEED <= 0:
    raise ValueError("ATOM_REVIEW_SPEED must be positive")


def total_seconds() -> int:
    """The planned running time, which the narration windows must agree with."""
    return sum(DURATIONS.values())


def apply_project_theme(scene, *, background: bool = True) -> None:
    """Set the film's ground colour and the shading model the surfaces expect.

    ``should_apply_shading`` is switched off deliberately. Manim's built-in 3D
    shading recolours a face from its own start and end corner normals, which
    fights the per-face lighting the orbitals compute for themselves and shows
    up as dark wedges across an otherwise smooth lobe.
    """
    if background:
        scene.camera.background_color = BG
    scene.camera.should_apply_shading = False
