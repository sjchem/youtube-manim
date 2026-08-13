"""Scene 11: build the identity toolkit from three memorable visual moves."""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    bottom_caption,
    color_formula_parts,
    end_scene,
    eq,
    glow_dot,
    narration_wait,
    outlined_text,
    paced_play,
    section_tag,
)


class Scene11Identities(Scene):
    def construct(self) -> None:
        play_scene(self)


def _segmented_formula(parts: tuple[str, ...], colors: tuple[str, ...], font_size: int) -> MathTex:
    formula = MathTex(*parts, font_size=font_size)
    for part, color in zip(formula, colors, strict=True):
        part.set_color(color)
    formula.set_stroke(cfg.BG, width=3, opacity=0.92, background=True)
    return formula


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "11")
    add_cinematic_background(scene)
    tag = section_tag("11", "Build identities instead of memorizing them")
    paced_play(scene, FadeIn(tag, shift=RIGHT * 0.12), run_time=0.55)

    # Begin with the intimidating formula wall, then collapse it into three moves.
    storm = VGroup(
        color_formula_parts(eq(r"\sin^2\theta+\cos^2\theta=1", cfg.WHITE, cfg.FONT["body"])),
        color_formula_parts(eq(r"1+\tan^2\theta=\sec^2\theta", cfg.WHITE, cfg.FONT["body"])),
        color_formula_parts(eq(r"\cot^2\theta+1=\csc^2\theta", cfg.WHITE, cfg.FONT["body"])),
        color_formula_parts(eq(r"\sin(\alpha+\beta)=\sin\alpha\cos\beta+\cos\alpha\sin\beta", cfg.WHITE, cfg.FONT["small"])),
        color_formula_parts(eq(r"\sin(2\alpha)=2\sin\alpha\cos\alpha", cfg.WHITE, cfg.FONT["body"])),
        color_formula_parts(eq(r"\sin^2\frac\alpha2=\frac{1-\cos\alpha}{2}", cfg.WHITE, cfg.FONT["body"])),
    )
    storm[0].move_to([-4.5, 2.0, 0])
    storm[1].move_to([0.0, 2.0, 0])
    storm[2].move_to([4.5, 2.0, 0])
    storm[3].move_to([-4.5, -1.65, 0])
    storm[4].move_to([0.4, -1.65, 0])
    storm[5].move_to([4.9, -1.65, 0])
    paced_play(
        scene,
        FadeOut(tag),
        LaggedStart(*[FadeIn(item, shift=UP * 0.12) for item in storm], lag_ratio=0.12),
        run_time=1.4,
    )
    question = outlined_text("Can one picture generate all of these?", cfg.FONT["section"], cfg.GOLD, BOLD)
    question.move_to(ORIGIN)
    paced_play(scene, storm.animate.set_opacity(0.18), FadeIn(question, scale=1.06), run_time=1.0)

    move_names = VGroup(
        outlined_text("1  RESIZE", cfg.FONT["label"], cfg.CYAN, BOLD),
        outlined_text("2  COMBINE TURNS", cfg.FONT["label"], cfg.GREEN, BOLD),
        outlined_text("3  REUSE OR REVERSE", cfg.FONT["label"], cfg.PURPLE, BOLD),
    ).arrange(RIGHT, buff=0.75).move_to(DOWN * 0.75)
    paced_play(
        scene,
        FadeOut(VGroup(storm, question)),
        LaggedStart(*[FadeIn(name, shift=RIGHT * 0.15) for name in move_names], lag_ratio=0.2),
        run_time=1.2,
    )

    # Move 1: dividing an identity simply rescales the same right triangle.
    left = np.array([-5.8, -1.75, 0.0])
    right = np.array([-1.8, -1.75, 0.0])
    top = np.array([-1.8, 1.25, 0.0])
    triangle_sides = VGroup(
        Line(left, right, color=cfg.GREEN, stroke_width=8),
        Line(right, top, color=cfg.CYAN, stroke_width=8),
        Line(left, top, color=cfg.WHITE, stroke_width=8),
    )
    right_mark = Polygon(
        right,
        right + LEFT * 0.28,
        right + LEFT * 0.28 + UP * 0.28,
        right + UP * 0.28,
        color=cfg.GOLD,
        stroke_width=3,
        fill_opacity=0,
    )
    original_labels = VGroup(
        eq(r"\cos\theta", cfg.GREEN, cfg.FONT["section"]).next_to(triangle_sides[0], DOWN, buff=0.18),
        eq(r"\sin\theta", cfg.CYAN, cfg.FONT["section"]).next_to(triangle_sides[1], RIGHT, buff=0.18),
        eq("1", cfg.WHITE, cfg.FONT["section"]).move_to(triangle_sides[2].get_center() + UL * 0.38),
    )
    identity = color_formula_parts(eq(r"\cos^2\theta+\sin^2\theta=1", cfg.WHITE, cfg.FONT["hero"]))
    identity.move_to([3.1, 1.35, 0])
    move_one = outlined_text("MOVE 1  ·  RESIZE THE TRIANGLE", cfg.FONT["small"], cfg.CYAN, BOLD)
    move_one.next_to(identity, UP, buff=0.28)
    paced_play(
        scene,
        FadeOut(move_names),
        Create(triangle_sides),
        FadeIn(right_mark),
        FadeIn(original_labels),
        FadeIn(move_one),
        Write(identity),
        run_time=1.4,
    )
    narration_wait(scene, 0.9)

    divider = eq(r"\div\cos^2\theta", cfg.GREEN, cfg.FONT["section"]).move_to([3.1, 0.15, 0])
    paced_play(
        scene,
        FadeIn(divider, shift=DOWN * 0.12),
        VGroup(triangle_sides, right_mark, original_labels).animate.scale(1.06),
        run_time=0.9,
    )
    tan_labels = VGroup(
        eq("1", cfg.GREEN, cfg.FONT["section"]).move_to(original_labels[0]),
        eq(r"\tan\theta", cfg.CYAN, cfg.FONT["section"]).move_to(original_labels[1]),
        eq(r"\sec\theta", cfg.WHITE, cfg.FONT["section"]).move_to(original_labels[2]),
    )
    tan_identity = color_formula_parts(eq(r"1+\tan^2\theta=\sec^2\theta", cfg.WHITE, cfg.FONT["hero"]))
    tan_identity.move_to([3.1, -1.05, 0])
    paced_play(
        scene,
        TransformMatchingTex(identity.copy(), tan_identity),
        ReplacementTransform(original_labels, tan_labels),
        VGroup(triangle_sides, right_mark).animate.scale(1 / 1.06),
        run_time=1.4,
    )

    sin_divider = eq(r"\div\sin^2\theta", cfg.CYAN, cfg.FONT["section"]).move_to(divider)
    paced_play(scene, ReplacementTransform(divider, sin_divider), Indicate(identity, color=cfg.WHITE), run_time=0.9)
    cot_labels = VGroup(
        eq(r"\cot\theta", cfg.GREEN, cfg.FONT["section"]).move_to(tan_labels[0]),
        eq("1", cfg.CYAN, cfg.FONT["section"]).move_to(tan_labels[1]),
        eq(r"\csc\theta", cfg.WHITE, cfg.FONT["section"]).move_to(tan_labels[2]),
    )
    cot_identity = color_formula_parts(eq(r"\cot^2\theta+1=\csc^2\theta", cfg.WHITE, cfg.FONT["hero"]))
    cot_identity.move_to(tan_identity)
    paced_play(
        scene,
        TransformMatchingTex(tan_identity, cot_identity),
        ReplacementTransform(tan_labels, cot_labels),
        run_time=1.3,
    )

    definitions = VGroup(
        color_formula_parts(eq(r"\tan\theta=\frac{\sin\theta}{\cos\theta}", cfg.WHITE, cfg.FONT["label"])),
        color_formula_parts(eq(r"\cot\theta=\frac{\cos\theta}{\sin\theta}", cfg.WHITE, cfg.FONT["label"])),
        color_formula_parts(eq(r"\sec\theta=\frac1{\cos\theta}", cfg.WHITE, cfg.FONT["label"])),
        color_formula_parts(eq(r"\csc\theta=\frac1{\sin\theta}", cfg.WHITE, cfg.FONT["label"])),
    ).arrange_in_grid(rows=2, cols=2, buff=(0.75, 0.35)).move_to([3.1, -2.45, 0])
    paced_play(
        scene,
        LaggedStart(*[FadeIn(item, shift=UP * 0.1) for item in definitions], lag_ratio=0.16),
        run_time=1.2,
    )
    narration_wait(scene, 0.8)
    first_move = VGroup(
        triangle_sides,
        right_mark,
        cot_labels,
        identity,
        move_one,
        sin_divider,
        cot_identity,
        definitions,
    )
    paced_play(scene, FadeOut(first_move), run_time=0.8)

    # Move 2: the second rotation is resolved along and across the first ray.
    center = np.array([-3.7, -0.25, 0.0])
    radius = 2.35
    axes = VGroup(
        Line(center + LEFT * 2.75, center + RIGHT * 2.75, color=cfg.MUTED, stroke_width=2),
        Line(center + DOWN * 2.75, center + UP * 2.75, color=cfg.MUTED, stroke_width=2),
    )
    circle = Circle(radius=radius, color=cfg.MUTED, stroke_width=4).move_to(center)
    alpha = ValueTracker(0.0)
    beta = ValueTracker(0.0)
    ray_alpha = always_redraw(
        lambda: Line(
            center,
            center + radius * np.array([np.cos(alpha.get_value()), np.sin(alpha.get_value()), 0]),
            color=cfg.GREEN,
            stroke_width=7,
        )
    )
    ray_sum = always_redraw(
        lambda: Line(
            center,
            center + radius * np.array(
                [np.cos(alpha.get_value() + beta.get_value()), np.sin(alpha.get_value() + beta.get_value()), 0]
            ),
            color=cfg.GOLD,
            stroke_width=8,
        )
    )
    alpha_arc = always_redraw(
        lambda: Arc(radius=0.66, start_angle=0, angle=alpha.get_value(), arc_center=center, color=cfg.GREEN, stroke_width=5)
    )
    beta_arc = always_redraw(
        lambda: Arc(
            radius=0.94,
            start_angle=alpha.get_value(),
            angle=beta.get_value(),
            arc_center=center,
            color=cfg.PURPLE,
            stroke_width=5,
        )
    )
    endpoint = always_redraw(
        lambda: glow_dot(
            center + radius * np.array(
                [np.cos(alpha.get_value() + beta.get_value()), np.sin(alpha.get_value() + beta.get_value()), 0]
            ),
            cfg.GOLD,
            0.09,
        )
    )
    move_two = outlined_text("MOVE 2  ·  COMBINE TWO TURNS", cfg.FONT["small"], cfg.GREEN, BOLD).move_to([3.15, 2.8, 0])
    paced_play(scene, Create(axes), Create(circle), FadeIn(move_two), run_time=1.0)
    scene.add(ray_alpha, ray_sum, alpha_arc, beta_arc, endpoint)
    alpha_label = eq(r"\alpha", cfg.GREEN, cfg.FONT["section"]).move_to(center + [0.95, 0.35, 0])
    paced_play(scene, alpha.animate.set_value(PI / 5), FadeIn(alpha_label), run_time=2.0, rate_func=smooth)
    beta_label = eq(r"\beta", cfg.PURPLE, cfg.FONT["section"]).move_to(center + [0.70, 1.12, 0])
    paced_play(scene, beta.animate.set_value(PI / 6), FadeIn(beta_label), run_time=2.0, rate_func=smooth)
    angle_sum = eq(r"\alpha+\beta", cfg.GOLD, cfg.FONT["section"]).move_to(center + [-0.65, 2.70, 0])
    paced_play(scene, FadeIn(angle_sum), run_time=0.6)

    alpha_value = alpha.get_value()
    beta_value = beta.get_value()
    u_alpha = np.array([np.cos(alpha_value), np.sin(alpha_value), 0])
    v_alpha = np.array([-np.sin(alpha_value), np.cos(alpha_value), 0])
    along_end = center + radius * np.cos(beta_value) * u_alpha
    final_end = along_end + radius * np.sin(beta_value) * v_alpha
    along_component = Arrow(center, along_end, buff=0, color=cfg.GREEN, stroke_width=6, max_tip_length_to_length_ratio=0.10)
    sideways_component = Arrow(
        along_end,
        final_end,
        buff=0,
        color=cfg.PURPLE,
        stroke_width=6,
        max_tip_length_to_length_ratio=0.18,
    )
    projection_lines = VGroup(
        DashedLine(final_end, [final_end[0], center[1], 0], color=cfg.CYAN, stroke_width=3),
        DashedLine(final_end, [center[0], final_end[1], 0], color=cfg.GREEN, stroke_width=3),
    )
    component_labels = VGroup(
        outlined_text("along the first ray", cfg.FONT["tiny"], cfg.GREEN, BOLD).next_to(along_component, DOWN, buff=0.12),
        outlined_text("sideways", cfg.FONT["tiny"], cfg.PURPLE, BOLD).next_to(sideways_component, RIGHT, buff=0.12),
    )
    paced_play(
        scene,
        GrowArrow(along_component),
        GrowArrow(sideways_component),
        Create(projection_lines),
        FadeIn(component_labels),
        run_time=1.2,
    )

    sine_add = _segmented_formula(
        (r"\sin(\alpha+\beta)", "=", r"\sin\alpha\cos\beta", "+", r"\cos\alpha\sin\beta"),
        (cfg.CYAN, cfg.WHITE, cfg.GREEN, cfg.WHITE, cfg.PURPLE),
        cfg.FONT["label"],
    )
    cosine_add = _segmented_formula(
        (r"\cos(\alpha+\beta)", "=", r"\cos\alpha\cos\beta", "-", r"\sin\alpha\sin\beta"),
        (cfg.GREEN, cfg.WHITE, cfg.GREEN, cfg.RED, cfg.PURPLE),
        cfg.FONT["label"],
    )
    addition = VGroup(
        outlined_text("READ THE VERTICAL PIECES", cfg.FONT["tiny"], cfg.CYAN, BOLD),
        sine_add,
        outlined_text("READ THE HORIZONTAL PIECES", cfg.FONT["tiny"], cfg.GREEN, BOLD),
        cosine_add,
    ).arrange(DOWN, buff=0.28).move_to([3.15, 0.25, 0])
    paced_play(scene, FadeIn(addition[0]), TransformFromCopy(projection_lines[0], sine_add), run_time=1.2)
    paced_play(scene, FadeIn(addition[2]), TransformFromCopy(projection_lines[1], cosine_add), run_time=1.2)
    minus_note = outlined_text("The sideways horizontal piece points left: minus.", cfg.FONT["small"], cfg.RED, BOLD)
    if minus_note.width > cfg.SAFE_WIDTH - 0.5:
        minus_note.scale_to_fit_width(cfg.SAFE_WIDTH - 0.5)
    minus_note.to_edge(DOWN, buff=0.30)
    paced_play(scene, FadeIn(minus_note), Indicate(cosine_add[3], color=cfg.WHITE), run_time=0.8)
    narration_wait(scene, 0.8)

    reverse_prompt = outlined_text("What if the second turn runs backward?", cfg.FONT["label"], cfg.GOLD, BOLD)
    reverse_prompt.to_edge(DOWN, buff=0.25)
    paced_play(
        scene,
        FadeOut(VGroup(along_component, sideways_component, component_labels, projection_lines, minus_note)),
        FadeIn(reverse_prompt),
        run_time=0.7,
    )
    negative_beta = eq(r"-\beta", cfg.PURPLE, cfg.FONT["section"]).move_to(beta_label)
    negative_sum = eq(r"\alpha-\beta", cfg.GOLD, cfg.FONT["section"]).move_to(angle_sum)
    paced_play(
        scene,
        beta.animate.set_value(-PI / 6),
        ReplacementTransform(beta_label, negative_beta),
        ReplacementTransform(angle_sum, negative_sum),
        run_time=2.0,
        rate_func=smooth,
    )
    sine_sub = _segmented_formula(
        (r"\sin(\alpha-\beta)", "=", r"\sin\alpha\cos\beta", "-", r"\cos\alpha\sin\beta"),
        (cfg.CYAN, cfg.WHITE, cfg.GREEN, cfg.RED, cfg.PURPLE),
        cfg.FONT["label"],
    ).move_to(sine_add)
    cosine_sub = _segmented_formula(
        (r"\cos(\alpha-\beta)", "=", r"\cos\alpha\cos\beta", "+", r"\sin\alpha\sin\beta"),
        (cfg.GREEN, cfg.WHITE, cfg.GREEN, cfg.WHITE, cfg.PURPLE),
        cfg.FONT["label"],
    ).move_to(cosine_add)
    paced_play(
        scene,
        TransformMatchingTex(sine_add, sine_sub),
        TransformMatchingTex(cosine_add, cosine_sub),
        reverse_prompt.animate.set_color(cfg.PURPLE),
        run_time=1.2,
    )
    narration_wait(scene, 0.8)
    rotation_group = VGroup(
        axes,
        circle,
        ray_alpha,
        ray_sum,
        alpha_arc,
        beta_arc,
        endpoint,
        move_two,
        alpha_label,
        negative_beta,
        negative_sum,
        addition[0],
        addition[2],
        sine_sub,
        cosine_sub,
        reverse_prompt,
    )
    paced_play(scene, FadeOut(rotation_group), run_time=0.8)

    # Move 3: equal turns create double angles; reversing that step creates half angles.
    move_three = outlined_text("MOVE 3  ·  REUSE OR REVERSE A TURN", cfg.FONT["small"], cfg.PURPLE, BOLD)
    move_three.to_edge(UP, buff=0.45)
    source = _segmented_formula(
        (r"\sin(\alpha+\beta)", "=", r"\sin\alpha\cos\beta", "+", r"\cos\alpha\sin\beta"),
        (cfg.CYAN, cfg.WHITE, cfg.GREEN, cfg.WHITE, cfg.PURPLE),
        cfg.FONT["body"],
    ).move_to(UP * 1.55)
    paced_play(scene, FadeIn(move_three), Write(source), run_time=1.0)
    equal_prompt = outlined_text("What if both turns are equal?", cfg.FONT["label"], cfg.GOLD, BOLD)
    equal_chip = eq(r"\beta=\alpha", cfg.GOLD, cfg.FONT["section"])
    equal_group = VGroup(equal_prompt, equal_chip).arrange(RIGHT, buff=0.45).move_to(UP * 0.45)
    paced_play(scene, FadeIn(equal_group, shift=UP * 0.12), run_time=0.8)

    double_sine = color_formula_parts(eq(r"\sin(2\alpha)=2\sin\alpha\cos\alpha", cfg.WHITE, cfg.FONT["hero"]))
    double_sine.move_to(DOWN * 0.65)
    paced_play(scene, TransformFromCopy(source, double_sine), FadeOut(equal_group), run_time=1.3)
    double_cos = color_formula_parts(eq(r"\cos(2\alpha)=\cos^2\alpha-\sin^2\alpha", cfg.WHITE, cfg.FONT["section"]))
    double_cos.next_to(double_sine, DOWN, buff=0.45)
    paced_play(scene, FadeIn(double_cos, shift=UP * 0.12), run_time=1.0)
    alternatives = VGroup(
        eq(r"=1-2\sin^2\alpha", cfg.CYAN, cfg.FONT["body"]),
        eq(r"=2\cos^2\alpha-1", cfg.GREEN, cfg.FONT["body"]),
    ).arrange(RIGHT, buff=0.8).next_to(double_cos, DOWN, buff=0.40)
    equivalence = outlined_text("Use  sin²α + cos²α = 1", cfg.FONT["small"], cfg.WHITE, BOLD)
    equivalence.next_to(alternatives, DOWN, buff=0.25)
    paced_play(
        scene,
        LaggedStart(*[TransformFromCopy(double_cos, item) for item in alternatives], lag_ratio=0.3),
        FadeIn(equivalence),
        run_time=1.1,
    )
    narration_wait(scene, 0.9)

    reverse = VGroup(
        outlined_text("RUN THE DOUBLE-ANGLE STEP BACKWARD", cfg.FONT["small"], cfg.PURPLE, BOLD),
        eq(r"2\left(\frac\alpha2\right)=\alpha", cfg.GOLD, cfg.FONT["section"]),
        Arrow(UP * 0.35, DOWN * 0.35, color=cfg.PURPLE, stroke_width=5, buff=0),
    ).arrange(DOWN, buff=0.18).move_to(UP * 0.45)
    paced_play(
        scene,
        FadeOut(VGroup(source, alternatives, equivalence, double_sine)),
        double_cos.animate.scale(0.72).move_to(UP * 2.25),
        FadeIn(reverse),
        run_time=0.9,
    )
    half = VGroup(
        color_formula_parts(eq(r"\sin^2\frac\alpha2=\frac{1-\cos\alpha}{2}", cfg.WHITE, cfg.FONT["section"])),
        color_formula_parts(eq(r"\cos^2\frac\alpha2=\frac{1+\cos\alpha}{2}", cfg.WHITE, cfg.FONT["section"])),
    ).arrange(DOWN, buff=0.55).move_to(DOWN * 1.45)
    paced_play(
        scene,
        LaggedStart(*[TransformFromCopy(double_cos, item) for item in half], lag_ratio=0.35),
        run_time=1.7,
    )
    sign_warning = bottom_caption("Taking a square root? The quadrant decides + or −.", cfg.RED)
    paced_play(scene, FadeIn(sign_warning), Indicate(half, color=cfg.WHITE, scale_factor=1.02), run_time=1.0)

    paced_play(
        scene,
        FadeOut(VGroup(move_three, double_cos, reverse, half, sign_warning)),
        run_time=0.8,
    )
    summary = VGroup()
    summary_data = (
        ("RESIZE", "Pythagorean family", cfg.CYAN),
        ("COMBINE", "addition & subtraction", cfg.GREEN),
        ("REUSE / REVERSE", "double & half angles", cfg.PURPLE),
    )
    for title, meaning, color in summary_data:
        box = RoundedRectangle(
            width=4.35,
            height=2.2,
            corner_radius=0.18,
            color=color,
            fill_color=cfg.PANEL,
            fill_opacity=0.88,
        )
        content = VGroup(
            outlined_text(title, cfg.FONT["label"], color, BOLD),
            outlined_text(meaning, cfg.FONT["tiny"], cfg.WHITE, BOLD),
        ).arrange(DOWN, buff=0.28)
        for line in content:
            if line.width > box.width - 0.34:
                line.scale_to_fit_width(box.width - 0.34)
        content.move_to(box)
        summary.add(VGroup(box, content))
    summary.arrange(RIGHT, buff=0.40).move_to(UP * 0.25)
    final_caption = bottom_caption("Choose the move. Rebuild the identity.", cfg.GOLD)
    paced_play(
        scene,
        LaggedStart(*[FadeIn(card, shift=UP * 0.18) for card in summary], lag_ratio=0.2),
        FadeIn(final_caption),
        run_time=1.4,
    )
    narration_wait(scene, 1.4)
    end_scene(scene, started, cfg.SCENE_DURATIONS["11"])
