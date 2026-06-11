from __future__ import annotations

import manim as m

from themes import apply_dracula_theme, apply_molokai_theme, apply_oceanic_next_theme


def oceanic_bubbles() -> m.VGroup:
    bubble_specs = [
        ((-5.7, 2.7, 0), 0.42, 0.035),
        ((-3.9, -2.2, 0), 0.28, 0.028),
        ((-1.2, 2.9, 0), 0.18, 0.025),
        ((2.5, -2.7, 0), 0.34, 0.028),
        ((4.8, 1.9, 0), 0.52, 0.032),
        ((5.9, -0.8, 0), 0.22, 0.024),
    ]
    bubbles = m.VGroup()
    for point, radius, opacity in bubble_specs:
        bubble = m.Circle(
            radius=radius,
            color=m.LIGHT_GREY,
            stroke_width=0,
            stroke_opacity=0,
            fill_opacity=opacity,
        ).move_to(point)
        bubbles.add(bubble)
    return bubbles


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
