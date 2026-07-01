"""Scene 08 — Statistics: The Thinking Layer of Machine Learning.

Synthesis scene.  The full ML pipeline is revealed step by step,
with the Statistics layer expanding to show its roles:
uncertainty, signal extraction, estimation, generalization, evaluation,
and inference.

Narration cue: ~77 seconds
"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    begin_scene, bottom_caption, cinematic_background, end_scene,
    eq, glow_dot, label, narration_wait, paced_play,
)
from utils.physics_models import pipeline_stages, stat_tools


class Scene08StatisticsLayer(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    scene_start = begin_scene(scene)
    scene.add(cinematic_background(show_bubbles=True))

    # ── Phase 1: Empty pipeline skeleton ────────────────────────────────────
    stages = pipeline_stages()
    stage_colors = [s["color"] for s in stages]
    stage_labels = [s["label"] for s in stages]

    # Box positions: 4 stages across the screen
    n  = len(stages)
    xs = np.linspace(-4.8, 4.8, n)
    y  = 0.5

    boxes   = VGroup()
    s_texts = VGroup()
    arrows  = VGroup()

    for i, (x, stage) in enumerate(zip(xs, stages)):
        is_stats = i == 1
        col = stage["color"]
        box = RoundedRectangle(
            corner_radius=0.18,
            width=2.35, height=1.45,
            fill_color=cfg.COLORS["panel2"] if is_stats else cfg.COLORS["panel"],
            fill_opacity=0.85,
            stroke_color=col,
            stroke_width=3.5 if is_stats else 2.2,
        ).move_to([x, y, 0])
        txt = Text(stage["label"], font_size=cfg.FONT["small"], color=col, weight=BOLD)
        txt.set_stroke(cfg.BG, width=3, background=True)
        if txt.width > 2.1:
            txt.scale_to_fit_width(2.1)
        txt.move_to([x, y, 0])
        boxes.add(box)
        s_texts.add(txt)
        if i < n - 1:
            arr = Arrow(
                [x + 1.25, y, 0], [xs[i + 1] - 1.25, y, 0],
                buff=0, color=cfg.MUTED, stroke_width=3.5,
                max_tip_length_to_length_ratio=0.30,
            )
            arr.set_stroke(opacity=0.0)
            arrows.add(arr)

    cap_pipeline = bottom_caption("The Machine Learning pipeline.", color=cfg.WHITE)

    paced_play(
        scene,
        LaggedStart(*[FadeIn(b, scale=0.85) for b in boxes], lag_ratio=0.18),
        run_time=1.5,
    )
    paced_play(
        scene,
        LaggedStart(*[FadeIn(t) for t in s_texts], lag_ratio=0.18),
        run_time=1.0,
    )
    for arr in arrows:
        paced_play(scene, arr.animate.set_stroke(opacity=0.70), run_time=0.35)
    paced_play(scene, FadeIn(cap_pipeline, shift=UP * 0.1), run_time=0.5)
    narration_wait(scene, 0.6)

    full_steps = [
        ("World", cfg.GREEN),
        ("Population", cfg.MUTED),
        ("Sample", cfg.GOLD),
        ("Data", cfg.ORANGE),
        ("Model", cfg.BLUE),
        ("Evaluate", cfg.PURPLE),
        ("Predict", cfg.GREEN),
        ("Monitor", cfg.CYAN),
    ]
    full_nodes = VGroup()
    for text, col in full_steps:
        node = RoundedRectangle(
            corner_radius=0.10, width=1.35, height=0.55,
            fill_color=cfg.COLORS["panel"], fill_opacity=0.86,
            stroke_color=col, stroke_width=1.5,
        )
        node_text = Text(text, font_size=16, color=col, weight=BOLD)
        node_text.set_stroke(cfg.BG, width=2, background=True)
        if node_text.width > 1.12:
            node_text.scale_to_fit_width(1.12)
        node_text.move_to(node.get_center())
        full_nodes.add(VGroup(node, node_text))
    full_nodes.arrange(RIGHT, buff=0.20)
    if full_nodes.width > cfg.SAFE_WIDTH - 0.6:
        full_nodes.scale_to_fit_width(cfg.SAFE_WIDTH - 0.6)
    full_nodes.to_edge(DOWN, buff=1.03)
    full_arrows = VGroup()
    for left, right in zip(full_nodes[:-1], full_nodes[1:]):
        full_arrows.add(Arrow(
            left.get_right(), right.get_left(), buff=0.06,
            color=cfg.MUTED, stroke_width=2.0,
            max_tip_length_to_length_ratio=0.35,
        ))
    full_pipeline = VGroup(full_nodes, full_arrows)
    paced_play(
        scene,
        FadeOut(cap_pipeline),
        LaggedStart(*[FadeIn(n, scale=0.94) for n in full_nodes], lag_ratio=0.08),
        LaggedStart(*[GrowArrow(a) for a in full_arrows], lag_ratio=0.08),
        run_time=1.25,
    )
    narration_wait(scene, 1.0)

    # ── Phase 2: Zoom on the Statistics box ─────────────────────────────────
    stat_box  = boxes[1]
    stat_text = s_texts[1]

    cap_stats = bottom_caption("Statistics is the thinking layer.", color=cfg.CYAN)

    paced_play(
        scene,
        stat_box.animate.set_stroke(color=cfg.CYAN, width=5),
        stat_box.animate.set_fill(color=cfg.COLORS["panel2"], opacity=0.95),
        FadeOut(full_pipeline),
        FadeIn(cap_stats, shift=UP * 0.1),
        run_time=0.8,
    )
    paced_play(
        scene,
        Indicate(stat_box, color=cfg.CYAN, scale_factor=1.06),
        run_time=0.7,
    )
    narration_wait(scene, 0.4)

    # ── Phase 3: Expand statistics box — show 5 roles ────────────────────────
    tools   = stat_tools()
    n_tools = len(tools)

    # Fade non-stats pipeline elements
    non_stat = VGroup(
        *[b for i, b in enumerate(boxes) if i != 1],
        *[t for i, t in enumerate(s_texts) if i != 1],
        arrows,
    )
    paced_play(
        scene,
        non_stat.animate.set_fill(opacity=0.12).set_stroke(opacity=0.22),
        stat_box.animate.scale(1.35).move_to([xs[1], y, 0]),
        run_time=0.75,
    )

    # Tool bubbles arranged around the stats box
    angles = np.array([35, -25, -85, -145, -180, -215])[:n_tools] * PI / 180
    radius = 2.45
    bubble_r = 0.46
    centre = np.array([xs[1], y, 0])

    tool_mobs = VGroup()
    connectors = VGroup()
    for i, (ang, tool) in enumerate(zip(angles, tools)):
        tx = centre[0] + radius * np.cos(ang)
        ty = centre[1] + radius * np.sin(ang)

        bubble = Circle(radius=bubble_r, color=tool["color"],
                        stroke_width=2.8, fill_color=cfg.COLORS["panel"],
                        fill_opacity=0.82)
        bubble.move_to([tx, ty, 0])

        t_lbl = Text(tool["text"], font_size=cfg.FONT["tiny"],
                     color=tool["color"], weight=BOLD)
        t_lbl.set_stroke(cfg.BG, width=3, background=True)
        if t_lbl.width > 1.6:
            t_lbl.scale_to_fit_width(1.6)
        # Place label below the bubble so it never overflows the circle
        t_lbl.next_to(bubble, DOWN, buff=0.10)

        # Line from stats box edge to bubble edge
        direction = np.array([tx - centre[0], ty - centre[1], 0])
        direction /= np.linalg.norm(direction)
        p_start = centre + direction * 0.88
        p_end   = np.array([tx, ty, 0]) - direction * (bubble_r + 0.05)
        conn = Line(p_start, p_end, color=tool["color"],
                    stroke_width=2.0, stroke_opacity=0.60)

        tool_mobs.add(VGroup(bubble, t_lbl))
        connectors.add(conn)

    cap_tools = bottom_caption("Uncertainty · Signal · Estimation · Generalization · Evaluation · Inference",
                                color=cfg.CYAN)

    paced_play(
        scene,
        LaggedStart(*[Create(c) for c in connectors], lag_ratio=0.14),
        run_time=1.0,
    )
    paced_play(
        scene,
        LaggedStart(*[FadeIn(t, scale=0.6) for t in tool_mobs], lag_ratio=0.15),
        FadeOut(cap_stats), FadeIn(cap_tools, shift=UP * 0.1),
        run_time=1.8,
    )
    narration_wait(scene, 0.6)

    without_box = RoundedRectangle(
        corner_radius=0.14, width=4.8, height=2.15,
        fill_color=cfg.COLORS["panel"], fill_opacity=0.92,
        stroke_color=cfg.RED, stroke_width=2.2,
    )
    without_text = VGroup(
        Text("Without statistics", font_size=cfg.FONT["tiny"], color=cfg.RED, weight=BOLD),
        Text("pattern-matching", font_size=24, color=cfg.WHITE),
        Text("in the dark", font_size=24, color=cfg.MUTED),
    ).arrange(DOWN, buff=0.08)
    with_box = RoundedRectangle(
        corner_radius=0.14, width=4.8, height=2.15,
        fill_color=cfg.COLORS["panel2"], fill_opacity=0.94,
        stroke_color=cfg.CYAN, stroke_width=2.4,
    )
    with_text = VGroup(
        Text("With statistics", font_size=cfg.FONT["tiny"], color=cfg.CYAN, weight=BOLD),
        Text("why it predicts", font_size=22, color=cfg.WHITE),
        Text("how reliable", font_size=22, color=cfg.GOLD),
        Text("when to trust", font_size=22, color=cfg.GREEN),
    ).arrange(DOWN, buff=0.04)
    for mob in (*without_text, *with_text):
        mob.set_stroke(cfg.BG, width=2, background=True)
    without_text.move_to(without_box.get_center())
    with_text.move_to(with_box.get_center())
    trust_panels = VGroup(
        VGroup(without_box, without_text),
        VGroup(with_box, with_text),
    ).arrange(RIGHT, buff=0.85).move_to(ORIGIN + DOWN * 0.10)

    current_pipeline = VGroup(boxes, s_texts, arrows, connectors, tool_mobs)
    paced_play(
        scene,
        FadeOut(cap_tools),
        current_pipeline.animate.set_opacity(0.10),
        LaggedStart(*[FadeIn(panel, shift=UP * 0.12) for panel in trust_panels], lag_ratio=0.20),
        run_time=1.0,
    )
    narration_wait(scene, 1.6)

    # ── Phase 4: Final synthesis text ────────────────────────────────────────
    synthesis = Text(
        "Statistics is how machines learn to think.",
        font_size=cfg.FONT["body"],
        color=cfg.WHITE,
        weight=BOLD,
    )
    synthesis.set_stroke(cfg.BG, width=6, background=True)
    synthesis.scale_to_fit_width(cfg.SAFE_WIDTH - 0.5)
    synthesis.to_edge(UP, buff=0.40)

    paced_play(
        scene,
        FadeOut(trust_panels),
        Write(synthesis),
        run_time=1.2,
    )
    next_line = Text(
        "Next: data types · distributions · uncertainty · evaluation",
        font_size=cfg.FONT["tiny"], color=cfg.CYAN,
    )
    next_line.set_stroke(cfg.BG, width=3, background=True)
    if next_line.width > cfg.SAFE_WIDTH - 0.8:
        next_line.scale_to_fit_width(cfg.SAFE_WIDTH - 0.8)
    next_line.next_to(synthesis, DOWN, buff=0.28)
    paced_play(scene, FadeIn(next_line, shift=UP * 0.08), run_time=0.7)
    narration_wait(scene, 1.5)

    end_scene(scene, scene_start, cfg.SCENE_DURATIONS["08"])
