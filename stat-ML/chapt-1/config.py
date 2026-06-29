"""Project-wide settings for Statistics for ML — Part 1, Chapter 1."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent          # stat-ML/chapt-1/
REPO_ROOT    = PROJECT_ROOT.parent.parent               # youtube-manim/

for _p in (str(PROJECT_ROOT), str(REPO_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from themes.oceanic_next import apply_oceanic_next_theme, oceanic_bubbles  # noqa: E402

# ── Identity ────────────────────────────────────────────────────────────────
PROJECT_TITLE  = "Why Statistics Matters in Machine Learning"
PROJECT_SLUG   = "stat-ml-ch01"
SERIES_LABEL   = "Statistics for Machine Learning"
SERIES_PART    = "Part 1 · Foundations"
CHAPTER_NUMBER = "Chapter 1"

# ── Frame ───────────────────────────────────────────────────────────────────
FRAME_WIDTH  = 16
FRAME_HEIGHT = 9
SAFE_WIDTH   = 14.0
SAFE_HEIGHT  = 7.5

# ── Oceanic Next colour palette ──────────────────────────────────────────────
COLORS: dict[str, str] = {
    "background":  "#041A2F",
    "background2": "#071E35",
    "panel":       "#0A2540",
    "panel2":      "#0D2B4A",
    "line":        "#1A3550",
    "line_soft":   "#254865",
    "cyan":        "#5FB3B3",
    "blue":        "#6699CC",
    "green":       "#99C794",
    "orange":      "#F99157",
    "red":         "#EC5F67",
    "purple":      "#C594C5",
    "white":       "#D8DEE9",
    "muted":       "#65737E",
    "gold":        "#FAC863",
    "teal":        "#4ECDC4",
}

CYAN   = COLORS["cyan"]
BLUE   = COLORS["blue"]
GREEN  = COLORS["green"]
ORANGE = COLORS["orange"]
RED    = COLORS["red"]
PURPLE = COLORS["purple"]
WHITE  = COLORS["white"]
MUTED  = COLORS["muted"]
GOLD   = COLORS["gold"]
TEAL   = COLORS["teal"]
BG     = COLORS["background"]

# ── Font sizes (mobile-first — must stay readable on a 375 px-wide phone) ───
FONT: dict[str, int] = {
    "hero":     76,    # main video title
    "title":    60,    # scene-level titles
    "section":  50,    # sub-headings
    "body":     40,    # on-screen explanation text
    "label":    36,    # axis / diagram labels
    "small":    30,    # secondary annotations
    "tiny":     24,    # footnotes / extreme-secondary
}

# ── Timing ───────────────────────────────────────────────────────────────────
TIMING: dict[str, float] = {
    "pace_scale":  1.10,
    "quick":       0.35,
    "normal":      0.75,
    "slow":        1.30,
    "hold":        0.80,
    "scene_hold":  1.10,
}

# ── Scene target durations (seconds) — animation + narration ─────────────────
SCENE_DURATIONS: dict[str, float] = {
    "01": 55.0,   # Series opening
    "02": 65.0,   # The uncertain world
    "03": 68.0,   # Signal vs noise
    "04": 67.0,   # Population vs sample
    "05": 78.0,   # Patterns & prediction
    "06": 78.0,   # Why models fail – overfitting
    "07": 77.0,   # Bias-variance tradeoff
    "08": 77.0,   # Statistics as the thinking layer
    "09": 17.0,   # Subscribe card
}

# ── Visual parameters ────────────────────────────────────────────────────────
VISUAL: dict[str, float] = {
    "glow_opacity":  0.18,
    "glow_layers":   4,
    "stroke_width":  4.5,
    "arrow_stroke":  6.0,
    "dot_radius":    0.07,
    "signal_stroke": 5.0,
}

# ── Render presets ───────────────────────────────────────────────────────────
RENDER: dict[str, object] = {
    "preview_quality": "l",
    "youtube_quality": "qh",
    "fps":             30,
    "resolution":      "1920,1080",
}
