"""Scene 02: Power ladder - going down means dividing."""

from __future__ import annotations

from manim import *

from config import ACCENT_BLUE, ACCENT_CYAN, ACCENT_TEAL, ACCENT_YELLOW, TEXT_COLOR, WORD_COLOR, WORD_FONT
from manim_scenes.common import (
    fit_to_safe_frame,
    glow_dot,
    highlight_box,
    keep_inside_frame,
    make_power_ladder,
    ocean_background,
    reset_camera,
    rule_badge,
    scene_setup,
    section_label,
    soft_arrow,
    with_glow,
)


class PowerLadderScene(MovingCameraScene):
    """Show that exponent steps reverse by division."""

    def construct(self) -> None:
        play_scene_02(self)


def _animate_ladder_descent(scene: MovingCameraScene, ladder, base: int, color: str) -> None:
    tracker = glow_dot(ladder.rows[0].get_left() + LEFT * 0.48, color=color, radius=0.045)
    divide = MathTex(rf"\div {base}", font_size=38, color=color)
    divide.next_to(ladder.group, RIGHT, buff=0.56)
    keep_inside_frame(divide)

    scene.play(FadeIn(tracker), FadeIn(divide), run_time=0.75)
    for index in range(len(ladder.rows) - 1):
        source = ladder.rows[index]
        target = ladder.rows[index + 1]
        pair_highlight = highlight_box(VGroup(source, target), color=color, buff=0.08)
        arrow = soft_arrow(source.get_bottom(), target.get_top(), rf"\div {base}", color=color)
        scene.play(Create(pair_highlight), FadeIn(arrow), run_time=0.7)
        scene.play(
            tracker.animate.move_to(target.get_left() + LEFT * 0.48),
            Indicate(target, color=color, scale_factor=1.04),
            run_time=1.1,
        )
        scene.play(FadeOut(pair_highlight), FadeOut(arrow), run_time=0.45)
        scene.wait(0.2)

    scene.play(FadeOut(tracker), FadeOut(divide), run_time=0.6)


def play_scene_02(scene: MovingCameraScene) -> None:
    scene_setup(scene)
    scene.add(ocean_background())

    label = section_label("Going down means dividing").to_edge(UP).shift(DOWN * 0.1)
    scene.play(FadeIn(label, shift=DOWN * 0.2), run_time=1.0)

    ladder_2 = make_power_ladder(2, highest=4, lowest=0)
    ladder_2.group.move_to(LEFT * 3.15 + DOWN * 0.05)

    up_badge = rule_badge("Up: multiply", color=ACCENT_TEAL, font_size=28)
    down_badge = rule_badge("Down: divide", color=ACCENT_CYAN, font_size=28)
    badges = VGroup(up_badge, down_badge).arrange(DOWN, buff=0.22).move_to(RIGHT * 3.35 + UP * 1.65)

    machine_box = RoundedRectangle(
        corner_radius=0.12,
        width=2.75,
        height=1.35,
        fill_color="#13202B",
        fill_opacity=0.78,
        stroke_color=ACCENT_BLUE,
        stroke_width=1.6,
    )
    machine_label = VGroup(
        MathTex(r"\times 2", font_size=42, color=ACCENT_TEAL),
        MathTex(r"\div 2", font_size=42, color=ACCENT_CYAN),
    ).arrange(DOWN, buff=0.12)
    machine = VGroup(machine_box, machine_label).move_to(RIGHT * 3.35 + DOWN * 0.5)
    machine_caption = Text("scale machine", font=WORD_FONT, font_size=24, color=WORD_COLOR).next_to(machine, DOWN, buff=0.15)
    fit_to_safe_frame(VGroup(ladder_2.group, badges, machine, machine_caption), max_width=11.9, max_height=5.8)
    keep_inside_frame(VGroup(ladder_2.group, badges, machine, machine_caption))

    scene.play(
        LaggedStart(*[FadeIn(row, shift=UP * 0.18) for row in ladder_2.rows], lag_ratio=0.12),
        FadeIn(badges, shift=LEFT * 0.2),
        FadeIn(machine, scale=0.95),
        FadeIn(machine_caption),
        run_time=2.4,
    )
    scene.wait(0.9)

    up_arrow = soft_arrow(
        ladder_2.rows[-1].get_right() + RIGHT * 0.28,
        ladder_2.rows[0].get_right() + RIGHT * 0.28,
        r"\times 2",
        color=ACCENT_TEAL,
    )
    down_arrow = soft_arrow(
        ladder_2.rows[0].get_left() + LEFT * 0.28,
        ladder_2.rows[-1].get_left() + LEFT * 0.28,
        r"\div 2",
        color=ACCENT_CYAN,
    )
    scene.play(Create(up_arrow), run_time=1.0)
    scene.wait(0.6)
    scene.play(Create(down_arrow), run_time=1.0)
    scene.wait(1.0)

    _animate_ladder_descent(scene, ladder_2, base=2, color=ACCENT_CYAN)
    scene.wait(0.8)

    landing = with_glow(MathTex(r"2^0=1", font_size=62, color=TEXT_COLOR), glow_color=ACCENT_YELLOW)
    landing.move_to(RIGHT * 2.95 + DOWN * 2.15)
    keep_inside_frame(landing)
    scene.play(FadeIn(landing, shift=UP * 0.2), run_time=1.0)
    scene.wait(1.4)

    ladder_3 = make_power_ladder(3, highest=3, lowest=0)
    ladder_3.group.move_to(LEFT * 0.3 + DOWN * 0.05)
    base_3_label = VGroup(
        Text("Try base", font=WORD_FONT, font_size=28, color=WORD_COLOR),
        MathTex("3", font_size=38, color=ACCENT_TEAL),
    ).arrange(RIGHT, buff=0.14)
    base_3_label.next_to(ladder_3.group, UP, buff=0.28)
    keep_inside_frame(VGroup(ladder_3.group, base_3_label))

    scene.play(
        FadeOut(up_arrow),
        FadeOut(down_arrow),
        FadeOut(machine),
        FadeOut(machine_caption),
        FadeOut(landing),
        ladder_2.group.animate.scale(0.78).to_edge(LEFT, buff=0.6),
        badges.animate.to_edge(RIGHT, buff=0.7),
        run_time=1.4,
    )
    keep_inside_frame(ladder_2.group)
    keep_inside_frame(badges)
    scene.play(FadeIn(base_3_label), LaggedStart(*[FadeIn(row) for row in ladder_3.rows], lag_ratio=0.12), run_time=2.0)
    _animate_ladder_descent(scene, ladder_3, base=3, color=ACCENT_TEAL)

    general = with_glow(MathTex(r"a^0=1", r"\quad", r"a\ne0", font_size=58, color=TEXT_COLOR), glow_color=ACCENT_YELLOW)
    general.to_edge(DOWN, buff=0.45)
    keep_inside_frame(general)
    scene.play(FadeIn(general, shift=UP * 0.2), run_time=1.1)
    scene.wait(2.2)
    reset_camera(scene, run_time=1.0)
