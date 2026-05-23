from __future__ import annotations

from manim import *


BACKGROUND_COLOR = "#050608"
TEXT_COLOR = "#EAEAEA"
MUTED_TEXT = "#9AA0A6"
BLUE_GLOW = "#4CC9F0"
PURPLE_GLOW = "#B517F1"
GOLD_GLOW = "#FFD166"
GREEN_GLOW = "#06D6A0"
RED_GLOW = "#EF476F"

FONT = "Sans"
TITLE_SIZE = 58
SUBTITLE_SIZE = 30
BODY_SIZE = 26
LABEL_SIZE = 20
SMALL_SIZE = 16


def set_scene_style(scene: Scene) -> None:
    """Apply the dark cinematic house style to a scene."""
    scene.camera.background_color = BACKGROUND_COLOR


def glow_text(mobject: Mobject, color: str = BLUE_GLOW, scale: float = 1.03, opacity: float = 0.25) -> VGroup:
    """Return a glowing copy stack behind the original mobject."""
    outer = mobject.copy().scale(scale).set_stroke(color, width=10, opacity=opacity * 0.55)
    middle = mobject.copy().scale((1 + scale) / 2).set_stroke(color, width=5, opacity=opacity)
    for item in (outer, middle):
        item.set_fill(opacity=0)
    return VGroup(outer, middle, mobject)


def cinematic_title(title: str, subtitle: str | None = None, color: str = TEXT_COLOR) -> VGroup:
    title_mob = Text(title, font_size=TITLE_SIZE, color=color, weight=BOLD)
    title_group = glow_text(title_mob, BLUE_GLOW, opacity=0.18)
    if subtitle:
        sub = Text(subtitle, font_size=SUBTITLE_SIZE, color=MUTED_TEXT)
        sub.next_to(title_group, DOWN, buff=0.28)
        return VGroup(title_group, sub)
    return title_group


def small_label(text: str, color: str = MUTED_TEXT, size: int = LABEL_SIZE) -> Text:
    return Text(text, font_size=size, color=color)


def soft_panel(width: float, height: float, stroke_color: str = BLUE_GLOW, fill_opacity: float = 0.05) -> RoundedRectangle:
    return RoundedRectangle(
        corner_radius=0.08,
        width=width,
        height=height,
        stroke_color=stroke_color,
        stroke_width=1.5,
        fill_color=stroke_color,
        fill_opacity=fill_opacity,
    )


def glowing_line(start: np.ndarray, end: np.ndarray, color: str = BLUE_GLOW, width: float = 3) -> VGroup:
    core = Line(start, end, color=color, stroke_width=width)
    halo = Line(start, end, color=color, stroke_width=width * 4, stroke_opacity=0.18)
    return VGroup(halo, core)

