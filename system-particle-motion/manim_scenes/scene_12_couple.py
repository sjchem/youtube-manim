"""Scene 12 — a couple: turning without moving. A bar lies on 3D ice, its
centre-of-mass target glowing. Two equal and opposite green forces act at
its ends along parallel lines. A 2D tip-to-tail inset shows they add to zero,
so the target stays put; but both torques turn the bar the same way and it
spins in place. A brace marks the separation d: tau = F d. Then a steering
wheel (a copper hoop with spokes, two hands pushing) and a jar lid (a drum
twisted by two forces) turn by couples.
"""

from manim_scenes.common import *

BAR_L = 4.6
F_LEN = 1.5


def couple_force_direction(angle: float, side: float) -> np.ndarray:
    """Tangential unit forces whose combined torque points along positive y."""
    return mu.rotation_y(angle) @ np.array([0.0, 0.0, -side])


class Scene12Couple(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "12", "A couple: turning without moving")
    stage = Stage((-1.6, -1.2, 0.0), zoom=1.3, yaw=-0.2, pitch=0.72, sway=0.025)
    ice = Grid((0, -0.12, 0), (1, 0, 0), (0, 0, 1), (-4.5, 4.5), (-3.0, 3.0), step=0.5, major=4, color=cfg.ICE,
               opacity=0.18, fill=cfg.ICE, fill_opacity=0.06)
    stage.add_body(ice)
    psi = Knob(0.0)

    def pose() -> np.ndarray:
        return mu.rotation_y(psi.value)

    def end(sign: float) -> np.ndarray:
        return pose() @ np.array([sign * BAR_L / 2, 0.1, 0.0])

    def push_dir(sign: float) -> np.ndarray:
        return couple_force_direction(psi.value, sign)

    bar = Block(lambda: np.zeros(3), (BAR_L, 0.22, 0.4), "#5E8FB0", pose=pose)
    stage.add_body(bar)
    target = com_tag(lambda: np.array([0.0, 0.2, 0.0]), 0.2)
    stage.add_overlay(target)
    show(scene, stage, 1.0)
    q = caption("zero net force, and yet it turns?", cfg.WHITE)
    scene.play(FadeIn(q), run_time=0.8)

    # --- 2. Equal, opposite, along different lines --------------------------------------------------------------------
    beat(scene, t, 1)
    f1 = Vector(lambda: end(-1) - push_dir(-1) * F_LEN, lambda: end(-1), cfg.FORCE, width=0.1, tip=0.32)
    f2 = Vector(lambda: end(1) - push_dir(1) * F_LEN, lambda: end(1), cfg.FORCE, width=0.1, tip=0.32)
    l1 = Segment(lambda: end(-1) - push_dir(-1) * 3.0, lambda: end(-1) + push_dir(-1) * 2.0, cfg.FORCE, width=2.5,
                 opacity=0.7, dashed=True)
    l2 = Segment(lambda: end(1) - push_dir(1) * 3.0, lambda: end(1) + push_dir(1) * 2.0, cfg.FORCE, width=2.5,
                 opacity=0.7, dashed=True)
    labs = [Tag(eq(r"\vec F", cfg.FONT["body"], cfg.FORCE), lambda s=s: end(s) - push_dir(s) * F_LEN * 0.6, LEFT * 0.45 * s)
            for s in (-1, 1)]
    hidden(f1, f2, l1, l2, *labs)
    stage.add_body(l1, l2)
    stage.add_overlay(f1, f2, *labs)
    scene.play(FadeOut(q), stage.fade(f1, 1.0), stage.fade(f2, 1.0), *[stage.fade(x, 1.0) for x in labs], run_time=1.0)
    scene.play(stage.fade(l1, 1.0), stage.fade(l2, 1.0), run_time=0.8)

    # --- 3. They cancel: the centre stays put -------------------------------------------------------------------------
    beat(scene, t, 2)
    inset_c = np.array([5.1, 1.6, 0.0])
    a1 = Arrow(inset_c + LEFT * 0.4 + DOWN * 1.0, inset_c + LEFT * 0.4 + UP * 1.0, buff=0, stroke_color=cfg.FORCE,
               stroke_width=7, max_tip_length_to_length_ratio=0.2)
    a2 = Arrow(inset_c + RIGHT * 0.4 + UP * 1.0, inset_c + RIGHT * 0.4 + DOWN * 1.0, buff=0, stroke_color=cfg.FORCE,
               stroke_width=7, max_tip_length_to_length_ratio=0.2)
    box = panel(3.4, 3.6, cfg.MUTED, 0.75).move_to(inset_c + DOWN * 0.15)
    sum_eq = eq(r"\sum \vec F = 0", cfg.FONT["section"], cfg.BALANCED).next_to(box, DOWN, buff=0.25)
    scene.play(FadeIn(box), GrowArrow(a1), run_time=0.8)
    scene.play(GrowArrow(a2), run_time=0.7)
    scene.play(a2.animate.shift(LEFT * 0.8), run_time=0.8)   # tip to tail: back to the start
    scene.play(Write(sum_eq), run_time=1.0)
    still = caption("the centre of mass doesn't accelerate", cfg.BALANCED)
    scene.play(FadeIn(still), run_time=0.6)

    # --- 4. Both torques turn it the same way: it spins in place ---------------------------------------------------------
    beat(scene, t, 3)
    curl = turn_arrow_3d(stage, np.array([0.0, 0.5, 0.0]), (0, 1, 0), 1.0, 0.3, np.radians(250), cfg.TORQUE, width=6)
    hidden(*curl.parts)
    spins = caption("both forces turn it the same way: it spins in place", cfg.TORQUE)
    scene.play(*[stage.fade(p, 1.0) for p in curl.parts], fade_through(still, spins), stage.fade(l1, 0.0),
               stage.fade(l2, 0.0), *stage_fade(stage, labs, 0.0), run_time=1.0)
    scene.play(psi.to(stage, 2.6, rate_func=rate_functions.ease_in_quad), run_time=4.0)

    # --- 5. tau = F d ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    scene.play(psi.to(stage, np.pi), *[stage.fade(p, 0.0) for p in curl.parts],
               stage.fade(l1, 1.0), stage.fade(l2, 1.0), run_time=1.6)
    d_seg = Segment(lambda: end(-1) + np.array([0, 0.35, 0]), lambda: end(1) + np.array([0, 0.35, 0]), cfg.POSITION,
                    width=6, opacity=1.0)
    d_seg.bias = 5.0
    d_lab = Tag(eq("d", cfg.FONT["section"], cfg.POSITION), lambda: np.array([0, 0.4, 0]), UP * 0.5 + RIGHT * 0.3)
    hidden(d_seg, d_lab)
    stage.add_body(d_seg)
    stage.add_overlay(d_lab)
    scene.play(stage.fade(d_seg, 1.0), stage.fade(d_lab, 1.0), run_time=0.9)
    law = eq(r"\tau_{\text{couple}} = F\,d", cfg.FONT["title"], cfg.TORQUE)
    law_box = boxed(law, cfg.RESULT).move_to([4.6, -2.65, 0])
    scene.play(FadeOut(spins), Write(law), run_time=1.4)
    scene.play(Create(law_box.frame), run_time=0.6)
    anywhere = txt("about any point", cfg.FONT["small"], cfg.MUTED).next_to(law_box, DOWN, buff=0.15)
    scene.play(FadeIn(anywhere), run_time=0.6)

    # --- 6. Steering wheel and jar lid --------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    hide(scene, stage, 0.8, FadeOut(box), FadeOut(a1), FadeOut(a2), FadeOut(sum_eq),
         VGroup(law_box, anywhere).animate.scale(0.8).move_to([0, 3.0, 0]))
    stage2 = Stage((0.0, -0.3, 0.0), zoom=1.25, yaw=-0.25, pitch=0.25, sway=0.03)
    turn = Knob(0.0)
    drive(stage2, turn, 0.9)
    wc = np.array([-2.9, 0.0, 0.0])
    wheel_pose = lambda: mu.rotation_x(0.25)  # noqa: E731
    rim = Hoop(wc, 1.5, "#3D4A57", pose=wheel_pose, spin=lambda: turn.value, width=22, stripes=2, stripe=cfg.GOLD)
    hub = Ball(wc, 0.25, cfg.STEEL, layers=14)
    spokes = []
    for k in range(3):
        tip_ball = Ball(lambda k=k: rim.point(np.pi / 2 + k * 2 * np.pi / 3), 0.05, "#3D4A57", layers=4)
        spokes += [tip_ball, Rod(hub, tip_ball, width=12, dark="#2A3440", light="#9FB3C4")]
    def hand_force(a: float) -> np.ndarray:
        phi = a + turn.value
        return rim.axes() @ np.array([-np.sin(phi), np.cos(phi), 0.0])

    hand_l = Vector(lambda: rim.point(np.pi) - hand_force(np.pi), lambda: rim.point(np.pi), cfg.FORCE, width=0.1, tip=0.3)
    hand_r = Vector(lambda: rim.point(0.0) - hand_force(0.0), lambda: rim.point(0.0), cfg.FORCE, width=0.1, tip=0.3)
    jc = np.array([2.9, -0.3, 0.0])
    jar = Drum(jc + np.array([0, -0.9, 0]), 0.95, 0.9, "#7FB8D9", axis=(0, 1, 0), sectors=2, opacity=0.55)
    lid = Drum(jc + np.array([0, 0.18, 0]), 1.02, 0.18, cfg.RED, axis=(0, 1, 0), spin=lambda: turn.value, stripe="#FFB3B3",
               sectors=12)
    twist_a = Vector(lambda: jc + np.array([-1.05, 0.2, -1.4]), lambda: jc + np.array([-1.05, 0.2, 0.0]), cfg.FORCE,
                     width=0.1, tip=0.3)
    twist_b = Vector(lambda: jc + np.array([1.05, 0.2, 1.4]), lambda: jc + np.array([1.05, 0.2, 0.0]), cfg.FORCE,
                     width=0.1, tip=0.3)
    stage2.add_body(rim, *spokes, hub, jar, lid)
    stage2.add_overlay(hand_l, hand_r, twist_a, twist_b)
    show(scene, stage2, 1.0)
    names = VGroup(txt("steering wheel", cfg.FONT["label"], cfg.WHITE).move_to([-4.2, -3.4, 0]),
                   txt("jar lid", cfg.FONT["label"], cfg.WHITE).move_to([4.2, -3.4, 0]))
    scene.play(FadeIn(names), run_time=0.8)

    # --- 7. Force and torque ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    both = VGroup(eq(r"\sum\vec F = 0", cfg.FONT["body"], cfg.BALANCED), txt("but", cfg.FONT["small"], cfg.MUTED),
                  eq(r"\sum\vec\tau \neq 0", cfg.FONT["body"], cfg.TORQUE)).arrange(RIGHT, buff=0.4)
    both.move_to(DOWN * 3.75)
    scene.play(fade_through(names, both), run_time=1.0)
    need = txt("we need both force and torque", cfg.FONT["body"], cfg.WHITE).move_to([0, 2.0, 0])
    scene.play(FadeIn(need), run_time=0.8)
    finish(scene, t, stage2)
