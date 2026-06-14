from __future__ import annotations

import manim as m

from themes import (
    apply_dracula_theme,
    apply_molokai_theme,
    apply_oceanic_next_theme,
    oceanic_bubbles,
)


class ThemeDemoScene(m.Scene):
    def __init__(self, theme_func, theme_name, **kwargs):
        super().__init__(**kwargs)
        self.theme_func = theme_func
        self.theme_name = theme_name

    def setup(self) -> None:
        self.theme_func(self)

    def construct(self) -> None:
        if self.theme_name == "Oceanic Next":
            self.add(oceanic_bubbles())

        title = m.Text(f"{self.theme_name} Theme", font_size=48)
        subtitle = m.Text("Manim Themes Demo", font_size=30)
        square = m.Square(side_length=1.7, color=m.BLUE)
        circle = m.Circle(radius=0.95, color=m.YELLOW)
        line = m.Line(m.LEFT * 2.6, m.RIGHT * 2.6, color=m.GREEN)
        group = m.VGroup(title, subtitle, square, circle, line)
        group.arrange(m.DOWN, buff=0.4).scale_to_fit_height(6.2).move_to(m.ORIGIN)

        self.play(m.Write(title), m.FadeIn(subtitle))
        self.play(m.DrawBorderThenFill(square), m.Create(circle), m.Create(line))
        self.wait(1.5)


class MolokaiThemeDemo(ThemeDemoScene):
    def __init__(self, **kwargs):
        super().__init__(apply_molokai_theme, "Molokai", **kwargs)


class OceanicNextThemeDemo(ThemeDemoScene):
    def __init__(self, **kwargs):
        super().__init__(apply_oceanic_next_theme, "Oceanic Next", **kwargs)


class DraculaThemeDemo(ThemeDemoScene):
    def __init__(self, **kwargs):
        super().__init__(apply_dracula_theme, "Dracula", **kwargs)
