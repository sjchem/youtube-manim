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
OCEANIC_DEEP_BACKGROUND = "#061018"


def apply_dark_theme(scene: "m.Scene", theme_name: str) -> None:
    """Apply a dark iTerm2 color theme to a Manim scene."""

    _apply_theme(
        manim_scene=scene,
        theme_name=theme_name,
        themes_dir=str(THEMES_DIR),
        light_theme=False,
    )


def apply_molokai_theme(scene: "m.Scene") -> None:
    """Apply the Molokai dark theme."""

    apply_dark_theme(scene, THEMES["molokai"])


def apply_oceanic_next_theme(scene: "m.Scene") -> None:
    """Apply the Oceanic Next dark theme."""

    apply_dark_theme(scene, THEMES["oceanic_next"])
    scene.camera.background_color = OCEANIC_DEEP_BACKGROUND


def apply_dracula_theme(scene: "m.Scene") -> None:
    """Apply the Dracula dark theme."""

    apply_dark_theme(scene, THEMES["dracula"])


def available_themes() -> list[str]:
    """Return the available dark theme names."""

    return list(THEMES.values())
