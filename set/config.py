"""Project-wide settings for 'Set Theory: From Sets to De Morgan's Laws'."""

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

PROJECT_TITLE = "Set Theory: From Sets to De Morgan's Laws"
PROJECT_PART = "The Mathematics of Sorting"
PROJECT_SLUG = "set-theory-from-sets-to-de-morgans-laws"
SERIES_LABEL = "Visualized Mathematics"
VIDEO_SUBTITLE = "One pizza. Two friends. A little mathematics."

FONT_FAMILY = "Nimbus Sans"  # Local Arial-compatible font (fc-match Arial).

FRAME_WIDTH = 16
FRAME_HEIGHT = 9
SAFE_WIDTH = 14.2
SAFE_HEIGHT = 7.6

# A true 16-by-9 logical canvas, not only a 16:9 pixel aspect ratio.
manim_config.frame_width = FRAME_WIDTH
manim_config.frame_height = FRAME_HEIGHT

# Oceanic palette. A colour always carries the same meaning across the film.
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

# Semantic roles. The whole film teaches through one visual grammar:
#   object -> rule -> region -> notation.
# A colour is a claim about a region, never decoration.
OBJECT = CYAN         # a card on the board: one element, not yet sorted
SET_A = BLUE          # the first rule's boundary  (set A, mammals, dairy, primes)
SET_B = ORANGE        # the second rule's boundary (set B, egg-layers, meat, evens)
UNIVERSE = MUTED      # the enclosing rectangle U: everything under discussion
INSIDE = GREEN        # membership confirmed, a region that survives a rule
OUTSIDE = RED         # membership refused, a contradiction, a counterexample
COMPLEMENT = PURPLE   # the NOT region, abstraction, the void beyond U
RESULT = WHITE        # the central equation, the headline answer
HIGHLIGHT = GOLD      # the region currently under the spotlight

FONT: dict[str, int] = {
    "hero": 54,
    "title": 40,
    "section": 36,
    "body": 32,
    "label": 30,
    "small": 28,
    # Compact labels leave the diagram dominant; check legibility at delivery size.
    "tiny": 24,
}

TIMING: dict[str, float] = {
    "quick": 0.45,
    "normal": 0.85,
    "slow": 1.4,
    "hold": 1.0,
    "transition": 0.55,
}

# Programme target: 1316 seconds; scene timings follow the spoken story.
# Verify pacing without rendering frames:  python -m utils.timing_audit
SCENE_DURATIONS: dict[str, float] = {
    "01": 48.0,
    "02": 139.0,
    "03": 117.0,
    "04": 74.0,
    "05": 100.0,
    "06": 143.0,
    "07": 101.0,
    "08": 112.0,
    "09": 108.0,
    "10": 139.0,
    "11": 102.0,
    "12": 84.0,
    "13": 40.0,
    "14": 9.0,
}

RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "h",
    "fps": 30,
    "preview_fps": 15,
    "preview_resolution": "854,480",
    "resolution": "2560,1440",
}

SEED = 20260923


def _restore_arc_defaults() -> None:
    """Undo the one theme adjustment that would repaint every set boundary white.

    ``manim_themes`` pins ``Arc.set_default(stroke_color=WHITE)``. Manim then
    binds that as a forced keyword on ``Arc.__init__``, and because ``Circle``
    forwards its ``color=`` argument down to ``Arc``, the pinned
    ``stroke_color`` wins — so ``Circle(color=SET_A)`` would come out white.
    Every set boundary, every region outline and every icon ring in this film
    is a circle or an arc, so the defaults are reset here and each stroke
    colour is stated explicitly at the point of use instead.
    """
    from manim import AnnotationDot, Arc

    Arc.set_default()
    AnnotationDot.set_default()


def apply_project_theme(scene, bubbles: bool = True) -> None:
    """Apply the local Oceanic Next theme and optional subtle bubbles."""
    apply_oceanic_next_theme(scene)
    _restore_arc_defaults()
    from manim import Text
    Text.set_default(font=FONT_FAMILY)
    scene.camera.background_color = BG
    if bubbles:
        scene.add(oceanic_bubbles())
