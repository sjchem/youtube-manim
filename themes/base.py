from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from manim_themes.manim_theme import apply_theme as _apply_theme

if TYPE_CHECKING:
    import manim as m

THEMES_DIR = Path(__file__).resolve().parent / "iTerm2Themes"
THEMES: dict[str, str] = {
    "molokai": "Molokai",
    "oceanic_next": "Oceanic Next",
    "dracula": "Dracula",
}


def apply_dark_theme(scene: "m.Scene", theme_name: str) -> None:
    """Apply a dark iTerm2 color theme to a Manim scene."""

    _apply_theme(
        manim_scene=scene,
        theme_name=theme_name,
        themes_dir=str(THEMES_DIR),
        light_theme=False,
    )


def available_themes() -> list[str]:
    """Return the available dark theme names."""

    return list(THEMES.values())
