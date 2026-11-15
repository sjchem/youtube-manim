"""Scene 27 — the energy of rolling. A solid cylinder and a copper ring roll
side by side along the bottom of the frame (no slipping). Above them the
kinetic energy builds: 1/2 M v_cm^2 + 1/2 I_cm omega^2, omega = v_cm / R,
and K = 1/2 M v_cm^2 (1 + I_cm / M R^2), boxed. Two stacked bars split each
body's energy into translation (gold) and rotation (cyan) from
``physics_models.kinetic_share``: the cylinder's rotation is a third, the
ring's a half.
"""

from manim_scenes.common import *

R = 0.6


class Scene27RollingEnergy(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "27", "The energy of rolling")
    stage = Stage((0.0, -3.15, 0.0), zoom=1.05, yaw=-0.1, pitch=0.18, sway=0.01)
    road = Grid((0, 0, 0), (1, 0, 0), (0, 0, 1), (-8.5, 8.5), (-1.6, 1.6), step=0.5, major=4, color=cfg.GRID, opacity=0.3,
                fill="#1B2A38", fill_opacity=0.5)
    stage.add_body(road)
    x = Knob(0.0)
    drive(stage, x, 0.22)
    travel = lambda: 4.2 * np.sin(0.35 * x.value)
    cyl = Drum(lambda: np.array([travel() + 1.1, R, -0.7]), R, 0.35, cfg.DISC_BODY, spin=lambda: -travel() / R,
               stripe=cfg.DISC_STRIPE, sectors=6)
    ring = Hoop(lambda: np.array([travel() - 1.1, R, 0.8]), R, cfg.RING_BODY, spin=lambda: -travel() / R, width=14)
    stage.add_body(cyl, ring)
    show(scene, stage, 0.8)
    two = caption("two kinds of kinetic energy", cfg.WHITE)
    scene.play(FadeIn(two), run_time=0.6)

    # --- 2. Translation + rotation about the centre of mass ------------------------------------------------------------------
    beat(scene, t, 1)
    K = eq([r"K", "=", r"\tfrac12 M v_{\mathrm{cm}}^2", "+", r"\tfrac12 I_{\mathrm{cm}}\omega^2"], cfg.FONT["section"], cfg.WHITE)
    K[2].set_color(cfg.VELOCITY)
    K[4].set_color(cfg.OMEGA)
    K[0].set_color(cfg.ENERGY)
    K.move_to([0, 2.9, 0])
    scene.play(FadeOut(two), Write(K[:3]), run_time=1.4)
    scene.play(Write(K[3:]), run_time=1.4)
    tags = VGroup(txt("translation", cfg.FONT["tiny"], cfg.VELOCITY).next_to(K[2], DOWN, buff=0.2),
                  txt("rotation about the centre", cfg.FONT["tiny"], cfg.OMEGA).next_to(K[4], DOWN, buff=0.2))
    fit_width(tags[1], K[4].width + 0.6)
    scene.play(FadeIn(tags), run_time=0.7)

    # --- 3. omega = v_cm / R ----------------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    sub = eq(r"\omega = {v_{\mathrm{cm}} \over R}", cfg.FONT["section"], cfg.OMEGA).move_to([0, 1.3, 0])
    scene.play(FadeOut(tags), run_time=0.4)
    scene.play(Write(sub), run_time=0.8)

    # --- 4. K = 1/2 M v^2 (1 + I / M R^2) -----------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    full = eq(r"K = \tfrac12 M v_{\mathrm{cm}}^2 \left(1 + {I_{\mathrm{cm}} \over M R^2}\right)", cfg.FONT["section"], cfg.ENERGY)
    full_box = boxed(full, cfg.RESULT).move_to([0, 2.4, 0])
    scene.play(FadeOut(sub), run_time=0.4)
    scene.play(ReplacementTransform(K, full), run_time=1.2)
    scene.play(Create(full_box.frame), run_time=0.6)

    # --- 5. Shares: cylinder 1/3 rotation, ring 1/2 -----------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(VGroup(full_box, full).animate.scale(0.75).move_to([0, 3.15, 0]), run_time=0.7)

    def stacked_bar(c, name: str, at, color: str) -> VGroup:
        share = pm.kinetic_share(c)
        h = 2.6
        frame = RoundedRectangle(width=1.2, height=h + 0.1, corner_radius=0.08, stroke_color=cfg.MUTED, stroke_width=2.5,
                                 fill_color=cfg.PANEL, fill_opacity=0.85).move_to(at)
        bottom = frame.get_bottom()[1] + 0.05
        trans = Rectangle(width=1.1, height=h * (1 - share), stroke_width=0, fill_color=cfg.VELOCITY, fill_opacity=0.95)
        trans.move_to([at[0], bottom + h * (1 - share) / 2, 0])
        rot = Rectangle(width=1.1, height=h * share, stroke_width=0, fill_color=cfg.OMEGA, fill_opacity=0.95)
        rot.move_to([at[0], bottom + h * (1 - share) + h * share / 2, 0])
        label = txt(name, cfg.FONT["label"], color).next_to(frame, DOWN, buff=0.18)
        frac = eq(ftex(pm.shape("cylinder" if c == 0.5 else "ring").coefficient / (1 + pm.shape("cylinder" if c == 0.5 else "ring").coefficient))
                  or "1", cfg.FONT["body"], cfg.OMEGA).next_to(rot, RIGHT, buff=0.25)
        group = VGroup(frame, trans, rot, label, frac)
        group.trans, group.rot, group.frac = trans, rot, frac
        return group

    c_cyl = float(pm.shape("cylinder").coefficient)
    c_ring = float(pm.shape("ring").coefficient)
    bars = VGroup(stacked_bar(c_cyl, "cylinder", np.array([-2.4, 0.2, 0]), cfg.DISC_STRIPE),
                  stacked_bar(c_ring, "ring", np.array([2.4, 0.2, 0]), cfg.RING_BODY))
    ratios = VGroup(eq(rf"{{I \over MR^2}} = {ftex(pm.shape('cylinder').coefficient)}", cfg.FONT["body"], cfg.DISC_STRIPE),
                    eq(rf"{{I \over MR^2}} = 1", cfg.FONT["body"], cfg.RING_BODY))
    ratios[0].next_to(bars[0], LEFT, buff=0.6)
    ratios[1].next_to(bars[1], RIGHT, buff=1.2)
    for bar, ratio in zip(bars, ratios):
        scene.play(FadeIn(bar[0]), FadeIn(bar[3]), FadeIn(ratio), run_time=0.7)
        scene.play(GrowFromEdge(bar.trans, DOWN), run_time=0.7)
        scene.play(GrowFromEdge(bar.rot, DOWN), FadeIn(bar.frac), run_time=0.8)
    legend = VGroup(txt("translation", cfg.FONT["tiny"], cfg.VELOCITY), txt("rotation", cfg.FONT["tiny"], cfg.OMEGA))
    legend.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([5.7, 1.9, 0])
    normalised = txt("fractions of each total K", cfg.FONT["small"], cfg.MUTED).move_to([0, 1.95, 0])
    scene.play(FadeIn(legend), FadeIn(normalised), run_time=0.6)

    # --- 6. Consequence on a slope ----------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    slope = caption("same mass, same radius, same speed: different shares", cfg.WHITE, cfg.FONT["small"])
    scene.play(FadeIn(slope), run_time=0.8)
    finish(scene, t, stage)
