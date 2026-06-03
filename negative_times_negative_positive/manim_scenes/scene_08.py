from manim import *

import config as cfg
from manim_scenes.common import cinematic_background, create_number_line, create_vector_arrow, narration_wait, paced_play, scene_transition


def _panel(label: str, icon: Mobject, color: str) -> VGroup:
    frame = RoundedRectangle(corner_radius=0.12, width=3.15, height=2.05, stroke_color=color, fill_color="#111827", fill_opacity=0.78)
    title = Text(label, font_size=22, color=color).next_to(frame.get_top(), DOWN, buff=0.18)
    icon.scale_to_fit_width(2.3)
    icon.move_to(frame.get_center() + DOWN * 0.25)
    return VGroup(frame, title, icon)


def play_scene(scene: Scene) -> None:
    scene.add(cinematic_background())
    title = Text("The hidden logic", font_size=44, color=cfg.ZERO).to_edge(UP)
    paced_play(scene, FadeIn(title))

    line = create_number_line(-4, 4, unit_size=0.22)
    particle = Dot(line.n2p(-2), color=cfg.GOLD, radius=0.07)
    p1 = _panel("motion", VGroup(line, particle), cfg.POSITIVE)

    arrows = VGroup(
        create_vector_arrow(LEFT * 0.55, RIGHT * 0.55, cfg.POSITIVE),
        create_vector_arrow(RIGHT * 0.55 + DOWN * 0.48, LEFT * 0.55 + DOWN * 0.48, cfg.NEGATIVE),
    )
    p2 = _panel("reversal", arrows, cfg.NEGATIVE)

    table = VGroup(
        MathTex(r"1(-4)=-4", font_size=24),
        MathTex(r"0(-4)=0", font_size=24),
        MathTex(r"-1(-4)=+4", font_size=24),
    ).arrange(DOWN, buff=0.12)
    for row in table:
        row.set_color_by_tex("-", cfg.NEGATIVE)
        row.set_color_by_tex("+", cfg.GOLD)
    p3 = _panel("pattern", table, cfg.GOLD)

    proof = VGroup(
        MathTex(r"-15+x=0", font_size=28),
        MathTex(r"x=+15", font_size=30),
    ).arrange(DOWN, buff=0.25)
    for row in proof:
        row.set_color_by_tex("-", cfg.NEGATIVE)
        row.set_color_by_tex("+", cfg.GOLD)
    p4 = _panel("structure", proof, cfg.COLORS["green"])

    panels = VGroup(p1, p2, p3, p4).arrange_in_grid(2, 2, buff=0.35).move_to(ORIGIN + DOWN * 0.15)
    paced_play(scene, LaggedStart(*[FadeIn(panel, shift=UP * 0.18) for panel in panels], lag_ratio=0.12), run_time=1.3)
    narration_wait(scene, 0.35)

    final = MathTex(r"(-a)(-b)=ab", font_size=76)
    final.set_color_by_tex("-", cfg.NEGATIVE)
    final.set_color_by_tex("ab", cfg.GOLD)
    final.move_to(UP * 0.25)
    paced_play(scene, LaggedStart(*[panel.animate.scale(0.1).move_to(final.get_center()).set_opacity(0) for panel in panels], lag_ratio=0.05), run_time=0.95)
    paced_play(scene, Write(final), run_time=0.95)

    message = VGroup(
        Text("Two reversals restore direction.", font_size=30, color=cfg.POSITIVE),
        Text("Consistency forces the rule.", font_size=30, color=cfg.GOLD),
    ).arrange(DOWN, buff=0.25).next_to(final, DOWN, buff=0.55)
    paced_play(scene, FadeIn(message, shift=UP * 0.15), Flash(final, color=cfg.GOLD), run_time=1.0)

    thanks = Text("Thank you for watching", font_size=34, color=cfg.ZERO)
    subscribe_box = RoundedRectangle(
        corner_radius=0.12,
        width=3.2,
        height=0.76,
        fill_color=cfg.NEGATIVE,
        fill_opacity=0.92,
        stroke_color=cfg.GOLD,
        stroke_width=2,
    )
    subscribe_text = Text("SUBSCRIBE", font_size=28, color=cfg.ZERO, weight=BOLD).move_to(subscribe_box)
    more = Text("for more visual math", font_size=24, color=cfg.MUTED)
    subscribe = VGroup(thanks, VGroup(subscribe_box, subscribe_text), more).arrange(DOWN, buff=0.22)
    subscribe.move_to(DOWN * 0.2)
    paced_play(scene, FadeOut(message), final.animate.shift(UP * 0.85).scale(0.78), FadeIn(subscribe, shift=UP * 0.2), run_time=1.0)
    paced_play(scene, Flash(subscribe_box, color=cfg.GOLD, flash_radius=1.65), run_time=0.8)
    narration_wait(scene, 1.5)
    scene_transition(scene)


class Scene08FinalSynthesis(Scene):
    def construct(self) -> None:
        play_scene(self)
