from __future__ import annotations

from typing import TYPE_CHECKING

from .base import THEMES, THEMES_DIR, apply_dark_theme, available_themes
from .oceanic_next import (
    OCEANIC_DEEP_BACKGROUND,
    add_oceanic_bubbles,
    apply_oceanic_next_scene,
    apply_oceanic_next_theme,
    oceanic_bubbles,
)

if TYPE_CHECKING:
    import manim as m


def apply_molokai_theme(scene: "m.Scene") -> None:
    """Apply the Molokai dark theme."""

    apply_dark_theme(scene, THEMES["molokai"])


def apply_dracula_theme(scene: "m.Scene") -> None:
    """Apply the Dracula dark theme."""

    apply_dark_theme(scene, THEMES["dracula"])
