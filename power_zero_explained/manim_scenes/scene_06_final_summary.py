"""Scene 06: Final summary and caveat."""

from __future__ import annotations

from manim import *

from config import (
    ACCENT_BLUE,
    ACCENT_CYAN,
    ACCENT_RED,
    ACCENT_TEAL,
    ACCENT_YELLOW,
    PANEL_COLOR,
    QUESTION_COLOR,
    TEXT_COLOR,
    WORD_COLOR,
    WORD_FONT,
)
from manim_scenes.common import (
    fit_to_safe_frame,
    floating_orbit,
    glowing_equation,
    keep_inside_frame,
    make_factor_chips,
    make_power_ladder,
    ocean_background,
    reset_camera,
    rule_badge,
    scene_setup,
    section_label,
    soft_arrow,
    with_glow,
)


class FinalSummaryScene(MovingCameraScene):
    """Gather the three reasons and name the 0^0 caveat."""

    def construct(self) -> None:
        play_scene_06(self)


def _reason_panel(title: str, math_label: str, color: str) -> VGroup:
    title_mob = Text(title, font=WORD_FONT, font_size=24, color=WORD_COLOR)
    math_mob = MathTex(math_label, font_size=38, color=TEXT_COLOR)
    contents = VGroup(title_mob, math_mob).arrange(DOWN, buff=0.12)
    box = RoundedRectangle(
        corner_radius=0.1,
        width=2.8,
        height=1.25,
        fill_color=PANEL_COLOR,
        fill_opacity=0.62,
        stroke_color=color,
        stroke_width=1.5,
        stroke_opacity=0.75,
    )
    contents.move_to(box)
    return VGroup(box, contents)


def play_scene_06(scene: MovingCameraScene) -> None:
    scene_setup(scene)
    scene.add(ocean_background())

    label = section_label("The rule is inevitable").to_edge(UP).shift(DOWN * 0.12)
    scene.play(FadeIn(label, shift=DOWN * 0.2), run_time=1.0)

    orbit = floating_orbit(count=18, radius=2.25, color=ACCENT_BLUE)
    center_tex = MathTex(r"a^0", "=", "?", font_size=78, color=TEXT_COLOR)
    center_tex[2].set_color(QUESTION_COLOR)
    center_question = with_glow(center_tex, glow_color=QUESTION_COLOR)
    scene.play(FadeIn(orbit), FadeIn(center_question, scale=0.92), run_time=1.3)
    scene.play(Rotate(orbit, angle=PI / 5), run_time=2.0, rate_func=smooth)

    ladder_panel = _reason_panel("Power ladder", r"\div a", ACCENT_CYAN).move_to(LEFT * 3.75 + UP * 1.25)
    law_panel = _reason_panel("Exponent law", r"a^{m-m}", ACCENT_TEAL).move_to(RIGHT * 3.75 + UP * 1.25)
    empty_panel = _reason_panel("Empty product", r"\text{identity }1", ACCENT_YELLOW).move_to(DOWN * 2.05)
    panels = VGroup(ladder_panel, law_panel, empty_panel)
    fit_to_safe_frame(VGroup(center_question, panels), max_width=12.1, max_height=5.8)
    keep_inside_frame(VGroup(center_question, panels))

    arrows = VGroup(
        soft_arrow(ladder_panel.get_right(), center_question.get_left(), color=ACCENT_CYAN),
        soft_arrow(law_panel.get_left(), center_question.get_right(), color=ACCENT_TEAL),
        soft_arrow(empty_panel.get_top(), center_question.get_bottom(), color=ACCENT_YELLOW),
    )
    scene.play(LaggedStart(*[FadeIn(panel, scale=0.95) for panel in panels], lag_ratio=0.18), run_time=1.4)
    scene.play(LaggedStart(*[Create(arrow) for arrow in arrows], lag_ratio=0.15), run_time=1.2)
    scene.wait(0.8)

    result = glowing_equation(r"a^0=1,\quad a\ne0", font_size=68, glow_color=ACCENT_YELLOW)
    fit_to_safe_frame(result, max_width=7.8, max_height=1.25)
    scene.play(Transform(center_question, result), run_time=1.4)
    scene.wait(1.5)

    scene.play(
        FadeOut(panels),
        FadeOut(arrows),
        FadeOut(orbit),
        center_question.animate.move_to(UP * 1.35),
        run_time=1.0,
    )

    caveat = VGroup(
        MathTex(r"0^0", font_size=62, color=ACCENT_RED),
        rule_badge("Special case", color=ACCENT_RED, font_size=25),
    ).arrange(DOWN, buff=0.22)
    caveat.move_to(DOWN * 0.7)
    keep_inside_frame(caveat)
    scene.play(FadeIn(caveat, shift=UP * 0.15), run_time=1.0)
    scene.wait(1.5)

    scene.play(
        FadeOut(caveat),
        center_question.animate.move_to(UP * 1.1),
        run_time=1.2,
    )

    final_line_1 = Text("Zero power does not mean nothing.", font=WORD_FONT, font_size=38, color=WORD_COLOR)
    final_line_2 = Text("It means no scaling yet.", font=WORD_FONT, font_size=46, color=ACCENT_YELLOW)
    subscribe_line = Text("Subscribe for more visual math.", font=WORD_FONT, font_size=28, color=QUESTION_COLOR)
    final_lines = VGroup(final_line_1, final_line_2).arrange(DOWN, buff=0.24)
    final_lines.move_to(DOWN * 0.7)
    fit_to_safe_frame(final_lines, max_width=8.5, max_height=1.6)

    small_ladder = make_power_ladder(2, highest=2, lowest=0, font_size=30, row_width=2.25)
    small_ladder.group.scale(0.78).to_edge(LEFT, buff=0.8).shift(DOWN * 0.4)
    chips = make_factor_chips("a", 0, color=ACCENT_TEAL)
    chips.add(MathTex("1", font_size=38, color=ACCENT_TEAL))
    chips.move_to(RIGHT * 4.7 + DOWN * 0.45)
    subscribe_cta = with_glow(subscribe_line, glow_color=QUESTION_COLOR)
    subscribe_cta.to_edge(DOWN, buff=0.35)
    keep_inside_frame(VGroup(final_lines, small_ladder.group, chips, subscribe_cta))

    scene.play(FadeIn(final_lines, shift=UP * 0.2), FadeIn(small_ladder.group), FadeIn(chips), run_time=1.4)
    scene.wait(1.2)
    scene.play(FadeIn(subscribe_cta, shift=UP * 0.12), run_time=0.8)
    scene.wait(2.0)
    reset_camera(scene, run_time=0.6)
