"""Project-wide visual and render settings for Chapter 2."""

from manim import *

PROJECT_TITLE = "The World Is Bigger Than the Dataset"

COLORS = {
    "background": "#070A12",
    "background_2": "#101725",
    "panel": "#111827",
    "panel_alt": "#172033",
    "line": "#334155",
    "text": "#F8FAFC",
    "muted": "#94A3B8",
    "blue": "#38BDF8",
    "green": "#4ADE80",
    "yellow": "#FACC15",
    "red": "#FB7185",
    "purple": "#A78BFA",
    "orange": "#FB923C",
    "teal": "#2DD4BF",
    "warning": "#F43F5E",
}

FONT_SIZES = {
    "title": 44,
    "subtitle": 28,
    "equation": 46,
    "label": 24,
    "small": 18,
    "tiny": 14,
}

TIMING = {
    "pace_scale": 9.8,
    "quick": 0.35,
    "normal": 0.75,
    "slow": 1.15,
    "pause": 0.5,
    "scene_hold": 0.9,
}

VISUAL = {
    "corner_radius": 0.12,
    "dot_radius": 0.035,
    "stroke_width": 3,
    "arrow_stroke": 6,
}

RENDER = {
    "preview_quality": "l",
    "youtube_quality": "qh",
    "fps": 30,
    "resolution": "1920,1080",
}

BG = COLORS["background"]
TEXT = COLORS["text"]
MUTED = COLORS["muted"]
BLUE = COLORS["blue"]
GREEN = COLORS["green"]
YELLOW = COLORS["yellow"]
RED = COLORS["red"]
PURPLE = COLORS["purple"]
ORANGE = COLORS["orange"]
TEAL = COLORS["teal"]
WARNING = COLORS["warning"]
CYAN = BLUE
GOLD = YELLOW
WHITE = TEXT
