"""Brief historical introductions using credited photographs, not generated faces."""

from __future__ import annotations

from manim import DOWN, Group, ImageMobject, RoundedRectangle

import config as cfg
from manim_scenes.common import outlined_text


def scientist_portrait(filename: str, name: str, center=(-4.5, 0.15, 0)) -> Group:
    """Frame the original photograph proportionally and name its subject below.

    Return Group because photographs are ImageMobjects. Call scene.pin() when
    presenting the group; scene.drop() fades it before releasing the camera pin.
    """
    photo = ImageMobject(str(cfg.ROOT / "assets/images" / filename)).set_height(3.25)
    border = RoundedRectangle(
        width=photo.width + 0.12, height=photo.height + 0.12,
        corner_radius=0.08, stroke_color=cfg.CYAN, stroke_width=2.5,
    ).move_to(photo)
    nameplate = outlined_text(name, 32, cfg.GOLD, limit=4.2).next_to(border, DOWN, buff=0.28)
    return Group(photo, border, nameplate).move_to(center)
