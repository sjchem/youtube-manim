"""Project-wide visual and render settings."""

from manim import *

PROJECT_TITLE = "Why Two Negatives Make a Positive"

COLORS = {
    "background": "#080A12",
    "background_2": "#101624",
    "positive": "#31D7FF",
    "positive_alt": "#4EA3FF",
    "negative": "#FF3B6B",
    "negative_alt": "#D946EF",
    "zero": "#F8FAFC",
    "gold": "#F8C14A",
    "green": "#4ADE80",
    "warning": "#FF4D4D",
    "muted": "#94A3B8",
    "line": "#334155",
    "panel": "#111827",
}

FONT_SIZES = {
    "title": 48,
    "subtitle": 30,
    "equation": 54,
    "label": 26,
    "small": 20,
    "tiny": 16,
}

TIMING = {
    "pace_scale": 1.45,
    "quick": 0.35,
    "normal": 0.75,
    "slow": 1.25,
    "beat": 0.45,
    "pause": 0.6,
    "scene_hold": 1.0,
}

VISUAL = {
    "glow_opacity": 0.22,
    "glow_layers": 4,
    "stroke_width": 5,
    "particle_radius": 0.09,
    "arrow_stroke": 8,
    "corner_radius": 0.12,
}

RENDER = {
    "preview_quality": "l",
    "youtube_quality": "qh",
    "fps": 30,
    "resolution": "1920,1080",
}

NEGATIVE = COLORS["negative"]
POSITIVE = COLORS["positive"]
GOLD = COLORS["gold"]
ZERO = COLORS["zero"]
MUTED = COLORS["muted"]
BG = COLORS["background"]
