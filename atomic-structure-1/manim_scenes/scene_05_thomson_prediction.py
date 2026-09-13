"""Scene 05: if every atom holds electrons, why is a lump of matter not negative?"""

from __future__ import annotations

import numpy as np
from manim import *

import config as cfg
from manim_scenes.common import (
    add_cinematic_background,
    begin_scene,
    check_mark,
    electron,
    end_scene,
    eq,
    fit_width,
    glowing_sphere,
    hide_background,
    move_3d_view,
    narration_wait,
    orbit_hold,
    outlined_text,
    paced_play,
    pin_to_frame,
    restore_background,
    set_3d_view,
    stage_banner,
    top_caption,
    unpin_from_frame,
)

from manim_scenes.common import (
    add_cinematic_background,
    alpha_particle,
    begin_scene,
    bottom_caption,
    chip,
    end_scene,
    eq,
    glow_line,
    narration_wait,
    outlined_text,
    paced_play,
    polyline,
    stage_banner,
    thomson_atom,
    top_caption,
)
from utils.physics_models import ThomsonAtom
from utils.render_helpers import lattice_points

MODEL = ThomsonAtom(radius=1.55, max_deflection_degrees=0.9)
# The true prediction is under one degree, far too small to see. The close-up
# draws it twelve times larger and says so on screen.
EXAGGERATION = 12.0


def _predicted_path(impact_parameter: float, x_start: float, x_end: float, exaggeration: float = 1.0) -> np.ndarray:
    points = MODEL.path_points(impact_parameter, x_start, x_end)
    baseline = np.full(points.shape[0], impact_parameter)
    points[:, 1] = baseline + (points[:, 1] - baseline) * exaggeration
    return points



ELECTRON_SEATS = (
    (0.00, 0.00, 0.00),
    (0.92, 0.34, 0.46),
    (-0.78, 0.61, -0.35),
    (0.26, -0.95, 0.52),
    (-0.55, -0.64, 0.71),
    (0.68, 0.72, -0.62),
    (-0.98, -0.18, 0.44),
    (0.14, 0.88, 0.63),
)


class Scene05ThomsonPrediction(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    started = begin_scene(scene, "05")
    add_cinematic_background(scene)

    # -- Beat 1: a contradiction hiding in plain sight ------------------------
    heading = top_caption("EVERY ATOM CONTAINS ELECTRONS", cfg.CYAN)
    paced_play(scene, FadeIn(heading), run_time=0.8)

    beads = VGroup(*[electron(0.24) for _ in range(6)])
    beads.arrange(RIGHT, buff=0.62).move_to([0, 0.75, 0])
    paced_play(scene, LaggedStart(*[FadeIn(bead, scale=1.5) for bead in beads], lag_ratio=0.25), run_time=2.2)
    total = eq(r"\text{total charge}\;<\;0", cfg.RED, cfg.FONT["section"]).move_to([0, -0.85, 0])
    paced_play(scene, FadeIn(total, shift=UP * 0.15), run_time=0.9)
    narration_wait(scene, 2.8)
    paced_play(scene, FadeOut(heading), run_time=0.6)

    question = outlined_text("so why is a lump of matter neutral?", cfg.FONT["body"], cfg.ORANGE)
    question.move_to([0, -2.55, 0])
    paced_play(scene, FadeIn(question, shift=UP * 0.15), run_time=0.9)
    narration_wait(scene, 4.6)

    # -- Beat 2: something positive has to be in there too --------------------
    # Match the six visible electrons with equal positive charge. Full-sized
    # signed terms and plain labels are easier to read than Q subscripts.
    positive = eq(r"+6e", cfg.ORANGE, cfg.FONT["title"])
    negative = eq(r"(-6e)", cfg.CYAN, cfg.FONT["title"])
    answer = VGroup(positive, eq("+", cfg.WHITE), negative,
                    eq("=", cfg.WHITE), eq("0", cfg.GREEN, cfg.FONT["title"]))
    answer.arrange(RIGHT, buff=0.90).move_to([0, -0.85, 0])
    charge_labels = VGroup(
        outlined_text("positive", cfg.FONT["tiny"], cfg.ORANGE).next_to(positive, DOWN, buff=0.45),
        outlined_text("negative", cfg.FONT["tiny"], cfg.CYAN).next_to(negative, DOWN, buff=0.45),
    )
    positive_region = RoundedRectangle(width=beads.width+0.55, height=1.3, corner_radius=0.4,
                                      color=cfg.ORANGE, fill_color=cfg.ORANGE,
                                      fill_opacity=0.12, stroke_width=2).move_to(beads)
    beads.set_z_index(2)
    paced_play(scene, FadeOut(question, total), FadeIn(positive_region),
               FadeIn(answer, charge_labels), run_time=1.3)
    narration_wait(scene, 5.2)
    paced_play(scene, FadeOut(answer, charge_labels, positive_region, beads), run_time=0.7)

    # -- Beat 3: Thomson's picture, in three dimensions -----------------------
    background = hide_background(scene)
    set_3d_view(scene, phi=68 * DEGREES, theta=-58 * DEGREES)

    cloud = VGroup()
    preview = config.pixel_height <= 480
    for index in range(3):
        shell = Sphere(radius=1.55 + 0.26 * index,
                       resolution=(12, 24) if preview else (16, 32), stroke_width=0)
        shell.set_color(cfg.POSITIVE_CLOUD)
        shell.set_opacity(0.16 - 0.045 * index)
        cloud.add(shell)
    seats = VGroup()
    for x, y, z in ELECTRON_SEATS:
        bead = glowing_sphere(0.13, cfg.ELECTRON_COLOR,
                              resolution=(6, 12) if preview else (12, 24), shells=1)
        bead.move_to(np.array([x, y, z]) * 1.30)
        seats.add(bead)

    banner = stage_banner("THOMSON'S MODEL")
    banner.to_edge(UP, buff=0.36)
    positive_label = outlined_text("+ positive cloud", cfg.FONT["small"], cfg.ORANGE).move_to([-3.1,-3.2,0])
    negative_label = outlined_text("− electrons", cfg.FONT["small"], cfg.CYAN).move_to([3.1,-3.2,0])
    pin_to_frame(scene, banner, positive_label, negative_label)
    scene.remove(positive_label, negative_label)
    paced_play(scene, FadeIn(banner, shift=DOWN * 0.15), run_time=0.9)
    paced_play(scene, FadeIn(cloud, scale=1.2), FadeIn(positive_label), run_time=1.6)
    paced_play(
        scene,
        LaggedStart(*[FadeIn(seat, scale=1.6) for seat in seats], lag_ratio=0.18),
        FadeIn(negative_label),
        run_time=2.8,
    )
    orbit_hold(scene, 2.0, rate=0.09)
    paced_play(scene, FadeOut(banner, positive_label, negative_label), run_time=0.6)
    unpin_from_frame(scene, banner, positive_label, negative_label)
    orbit_hold(scene, 5.4, rate=0.09)
    move_3d_view(scene, phi=52 * DEGREES, theta=-24 * DEGREES, run_time=3.4)
    orbit_hold(scene, 8.0, rate=0.08)

    paced_play(scene, FadeOut(cloud, seats), run_time=0.9)
    restore_background(scene, background)

    # -- Beat 4: for one moment, everything fits -------------------------------
    flat_cloud = VGroup()
    for index in range(5):
        flat_cloud.add(
            Circle(
                radius=1.75 - 0.16 * index,
                color=cfg.POSITIVE_CLOUD,
                stroke_width=0,
                fill_color=cfg.POSITIVE_CLOUD,
                fill_opacity=0.06,
            )
        )
    flat_cloud.add(Circle(radius=1.75, color=cfg.POSITIVE_CLOUD, stroke_width=3.2, stroke_opacity=0.8, fill_opacity=0))
    flat_beads = VGroup()
    for x, y, _z in ELECTRON_SEATS[:6]:
        flat_beads.add(electron(0.15).move_to(np.array([x, y, 0.0]) * 1.30))
    atom = VGroup(flat_cloud, flat_beads).move_to([0, 0.95, 0])
    paced_play(scene, FadeIn(atom, scale=1.1), run_time=1.2)

    size = eq(r"r \sim 10^{-10}\ \text{m}", cfg.MUTED, cfg.FONT["body"])
    size.move_to([0, -1.45, 0])
    paced_play(scene, FadeIn(size), run_time=0.8)
    narration_wait(scene, 3.6)

    tick = VGroup(
        check_mark(0.24, cfg.GREEN),
        outlined_text("explains electrical neutrality", cfg.FONT["body"], cfg.GREEN),
    ).arrange(RIGHT, buff=0.38)
    tick.move_to([0, -2.85, 0])
    paced_play(scene, FadeIn(tick, shift=UP * 0.18), run_time=0.9)
    narration_wait(scene, 5.4)

    paced_play(scene, FadeOut(atom, size, tick), run_time=0.8)

    # -- Beat 1: meet the projectile ------------------------------------------
    heading = top_caption("A NEW KIND OF PROBE", cfg.GOLD)
    paced_play(scene, FadeIn(heading), run_time=0.8)

    projectile = alpha_particle(0.30).move_to([-3.4, 0.45, 0])
    name = outlined_text("ALPHA PARTICLE", cfg.FONT["body"], cfg.ALPHA_COLOR).move_to([1.9, 0.45, 0])
    paced_play(scene, FadeIn(projectile, scale=1.6), run_time=0.9)
    paced_play(scene, FadeIn(name, shift=RIGHT * 0.2), run_time=0.8)

    traits = VGroup(
        chip("positive", cfg.ORANGE, cfg.FONT["small"]),
        chip("heavy", cfg.GOLD, cfg.FONT["small"]),
        chip("very fast", cfg.RED, cfg.FONT["small"]),
    ).arrange(RIGHT, buff=0.75).move_to([0, -1.65, 0])
    paced_play(scene, LaggedStart(*[FadeIn(item, scale=1.1) for item in traits], lag_ratio=0.4), run_time=2.2)
    narration_wait(scene, 1.2)
    paced_play(scene, FadeOut(heading), run_time=0.6)
    narration_wait(scene, 4.6)
    paced_play(scene, FadeOut(traits, name), run_time=0.6)

    # -- Beat 2: aim one at Thomson's atom ------------------------------------
    atom, beads = thomson_atom(radius=MODEL.radius, electron_count=6, electron_radius=0.13)
    atom.move_to([1.1, 0.15, 0])
    paced_play(scene, FadeIn(atom, scale=1.1), projectile.animate.scale(0.5).move_to([-6.4, 0.55, 0]), run_time=1.3)

    banner = stage_banner("PREDICTION", "only a small deflection")
    banner.to_edge(UP, buff=0.32)
    paced_play(scene, FadeIn(banner, shift=DOWN * 0.15), run_time=1.0)
    narration_wait(scene, 2.4)
    ceiling = int(np.ceil(MODEL.max_deflection_degrees))
    angle_note = eq(rf"\theta < {ceiling}^{{\circ}}", cfg.GREEN, cfg.FONT["section"]).move_to([4.2, -2.15, 0])
    disclaimer = outlined_text(
        f"illustrative bend: {EXAGGERATION:.0f}x", cfg.FONT["tiny"], cfg.MUTED
    ).next_to(angle_note, DOWN, buff=0.28)
    paced_play(scene, FadeOut(banner), FadeIn(disclaimer), run_time=0.6)
    narration_wait(scene, 3.6)

    lane = _predicted_path(0.40, -7.5, 5.8, EXAGGERATION)
    lane += np.array([1.1, 0.15])
    track = polyline(lane, cfg.ALPHA_COLOR, stroke_width=3.4).set_stroke(opacity=0.55)
    projectile.move_to([lane[0][0], lane[0][1], 0.0])
    paced_play(scene, MoveAlongPath(projectile, track), Create(track), run_time=3.2, rate_func=linear)
    narration_wait(scene, 3.6)

    paced_play(scene, FadeIn(angle_note, scale=1.1), run_time=0.9)
    narration_wait(scene, 0.6)
    narration_wait(scene, 6.4)

    # -- Beat 3: now a whole foil of them ------------------------------------
    paced_play(scene, FadeOut(projectile, track, angle_note, disclaimer, atom), run_time=0.7)

    foil = VGroup()
    for x, y in lattice_points(rows=5, columns=4, spacing=1.10, jitter=0.04):
        blob = Circle(
            radius=0.44,
            color=cfg.POSITIVE_CLOUD,
            stroke_width=2.0,
            stroke_opacity=0.55,
            fill_color=cfg.POSITIVE_CLOUD,
            fill_opacity=0.10,
        ).move_to([x + 1.5, y, 0])
        foil.add(blob)
    foil_label = outlined_text("A sheet of Thomson atoms", cfg.FONT["small"], cfg.MUTED).move_to([0, 3.45, 0])
    paced_play(scene, FadeIn(foil_label),
               LaggedStart(*[FadeIn(blob) for blob in foil], lag_ratio=0.05), run_time=2.0)
    narration_wait(scene, 0.7)
    paced_play(scene, FadeOut(foil_label), run_time=0.6)

    beam_lines = VGroup()
    beads_flying = VGroup()
    heights = np.linspace(-2.2, 2.2, 7)
    for height in heights:
        beam_lines.add(glow_line([-7.2, height, 0], [7.2, height, 0], cfg.ALPHA_COLOR, width=2.6).set_opacity(0.55))
        beads_flying.add(alpha_particle(0.10).move_to([-7.2, height, 0]))
    paced_play(
        scene,
        LaggedStart(
            *[
                AnimationGroup(Create(line), bead.animate.move_to([7.2, line.get_center()[1], 0]))
                for line, bead in zip(beam_lines, beads_flying)
            ],
            lag_ratio=0.14,
        ),
        run_time=5.0,
        rate_func=linear,
    )
    paced_play(scene, FadeOut(beads_flying), run_time=0.5)
    narration_wait(scene, 5.6)

    # -- Beat 4: state the prediction plainly ---------------------------------
    paced_play(scene, FadeOut(foil, beam_lines), run_time=0.7)

    rows = VGroup()
    for index in range(5):
        arrows = VGroup()
        for column in range(6):
            tilt = 5 * DEGREES if (index == 2 and column == 4) else 0.0
            arrow = Arrow(
                LEFT * 0.42, RIGHT * 0.42,
                color=cfg.GOLD if tilt == 0 else cfg.ORANGE,
                stroke_width=5,
                buff=0,
                max_tip_length_to_length_ratio=0.34,
            ).rotate(tilt)
            arrows.add(arrow)
        arrows.arrange(RIGHT, buff=0.60)
        rows.add(arrows)
    rows.arrange(DOWN, buff=0.60).move_to([0, 0.30, 0])

    title = outlined_text("PREDICTION", cfg.FONT["title"], cfg.BLUE).move_to([0, 2.95, 0])
    paced_play(scene, FadeIn(title, shift=DOWN * 0.15), run_time=0.9)
    paced_play(scene, LaggedStart(*[GrowArrow(arrow) for row in rows for arrow in row], lag_ratio=0.03), run_time=3.0)
    summary = bottom_caption("essentially everything sails straight through", cfg.GOLD)
    paced_play(scene, FadeIn(summary), run_time=0.8)
    narration_wait(scene, 4.7)

    end_scene(scene, started, cfg.SCENE_DURATIONS["05"])
