"""Scene 01 — one push, three motions. A 3D stage holds a box on ice, a door in
its frame and a cylinder on the floor. The same green push slides the box,
swings the door about its hinges, and rolls the cylinder (its cap sectors
turn, so the spin is visible). A single particle on a circle (Episode 02)
multiplies into a wheel of particles; the central question; four chips name
the new ideas; the title card.
"""

from manim_scenes.common import *

PUSH_LEN = 1.3
BOX_X0, DOOR_HINGE, CYL_X0 = -5.0, np.array([-1.0, 0.0, 0.0]), 2.5
CYL_R = 0.55
DOOR_W, DOOR_H = 1.7, 2.7
PSI0 = -0.6          # the doorway faces the viewer at an angle, so the push is not foreshortened
FRAME = mu.rotation_y(PSI0)


class Scene01Hook(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "01")
    stage = Stage((0.0, -2.3, 0.0), zoom=1.3, yaw=-0.3, pitch=0.3, sway=0.03)
    floor(stage, 0.0, reach=7.0, opacity=0.24)
    box_x, door_phi, cyl_x = Knob(BOX_X0), Knob(0.0), Knob(CYL_X0)

    # --- the props -----------------------------------------------------------------------------------
    ice = Face([[-6.4, 0.01, -1.1], [-2.4, 0.01, -1.1], [-2.4, 0.01, 1.1], [-6.4, 0.01, 1.1]], cfg.ICE, opacity=0.22,
               edge_opacity=0.5)
    ice.bias = -500
    box = Block(lambda: np.array([box_x.value, 0.36, 0.0]), (0.9, 0.72, 0.8), "#C98A4B")
    pose = lambda: mu.rotation_y(PSI0 + door_phi.value)  # noqa: E731
    door = Block(lambda: DOOR_HINGE + pose() @ np.array([DOOR_W / 2, DOOR_H / 2, 0.0]), (DOOR_W, DOOR_H, 0.09),
                 cfg.WOOD, pose=pose)
    knob = Ball(lambda: DOOR_HINGE + pose() @ np.array([DOOR_W - 0.18, 1.2, 0.09]), 0.07, cfg.GOLD, layers=10)
    post = Block(DOOR_HINGE + FRAME @ np.array([-0.08, DOOR_H / 2 + 0.05, 0.0]), (0.12, DOOR_H + 0.1, 0.2), cfg.WOOD_DARK,
                 pose=lambda: FRAME)
    lintel = Block(DOOR_HINGE + FRAME @ np.array([DOOR_W / 2, DOOR_H + 0.12, 0.0]), (DOOR_W + 0.3, 0.12, 0.2), cfg.WOOD_DARK,
                   pose=lambda: FRAME)
    far_post = Block(DOOR_HINGE + FRAME @ np.array([DOOR_W + 0.08, DOOR_H / 2 + 0.05, 0.0]), (0.12, DOOR_H + 0.1, 0.2),
                     cfg.WOOD_DARK, pose=lambda: FRAME)
    hinge_axis = Segment(DOOR_HINGE + np.array([0, -0.1, 0.12]), DOOR_HINGE + np.array([0, DOOR_H + 0.4, 0.12]),
                         cfg.ANGLE, width=3, opacity=0.8, dashed=True)
    cyl = Drum(lambda: np.array([cyl_x.value, CYL_R, 0.0]), CYL_R, 0.55, cfg.DISC_BODY, axis=(0, 0, 1),
               spin=lambda: -(cyl_x.value - CYL_X0) / CYL_R, stripe=cfg.DISC_STRIPE, sectors=6)
    stage.add_body(ice, box, post, far_post, lintel, door, knob, cyl)
    hinge_axis.presence = 0.0
    stage.add_body(hinge_axis)

    def push(at, direction):
        tail = lambda: at() - np.asarray(direction() if callable(direction) else direction) * PUSH_LEN  # noqa: E731
        return Vector(tail, at, cfg.FORCE, width=0.11, tip=0.32)

    box_push = push(lambda: np.array([box_x.value - 0.47, 0.36, 0.0]), (1, 0, 0))
    door_push = push(lambda: DOOR_HINGE + pose() @ np.array([DOOR_W - 0.18, 1.2, 0.07]), lambda: pose() @ np.array([0, 0, -1.0]))
    cyl_push = push(lambda: np.array([cyl_x.value - CYL_R - 0.02, CYL_R, 0.0]), (1, 0, 0))
    hidden(box_push, door_push, cyl_push)
    stage.add_overlay(box_push, door_push, cyl_push)
    show(scene, stage, 1.2)

    # --- 1. The box slides ---------------------------------------------------------------------------
    word = caption("slides", cfg.VELOCITY, cfg.FONT["section"])
    scene.play(stage.fade(box_push, 1.0), run_time=0.5)
    scene.play(box_x.to(stage, BOX_X0 + 0.5, rate_func=rate_functions.ease_in_quad), run_time=0.8)
    scene.play(stage.fade(box_push, 0.0), box_x.to(stage, BOX_X0 + 2.0, rate_func=linear), FadeIn(word), run_time=2.0)
    scene.play(box_x.to(stage, BOX_X0 + 2.35, rate_func=rate_functions.ease_out_sine), run_time=0.8)

    # --- 2. The door swings ---------------------------------------------------------------------------
    beat(scene, t, 1)
    word2 = caption("turns", cfg.ANGLE, cfg.FONT["section"])
    scene.play(stage.fade(door_push, 1.0), stage.fade(hinge_axis, 1.0), swap_anim(word, word2), run_time=0.7)
    scene.play(door_phi.to(stage, 0.35, rate_func=rate_functions.ease_in_quad), run_time=1.0)
    scene.play(stage.fade(door_push, 0.0), door_phi.to(stage, 1.25, rate_func=rate_functions.ease_out_sine),
               run_time=2.2)

    # --- 3. The cylinder rolls ------------------------------------------------------------------------
    beat(scene, t, 2)
    word3 = caption("moves and spins", cfg.TORQUE, cfg.FONT["section"])
    scene.play(stage.fade(cyl_push, 1.0), swap_anim(word2, word3), run_time=0.7)
    scene.play(cyl_x.to(stage, CYL_X0 + 0.5, rate_func=rate_functions.ease_in_quad), run_time=1.0)
    scene.play(stage.fade(cyl_push, 0.0), cyl_x.to(stage, CYL_X0 + 1.9, rate_func=rate_functions.ease_out_sine),
               run_time=3.2)

    # --- 4. Same push, three motions --------------------------------------------------------------------
    beat(scene, t, 3)
    chips = VGroup(chip("slides", cfg.VELOCITY), chip("turns", cfg.ANGLE), chip("both", cfg.TORQUE))
    chips.arrange(RIGHT, buff=0.9).move_to(UP * 3.0)
    same = caption("same push", cfg.FORCE, cfg.FONT["section"])
    scene.play(FadeOut(word3), run_time=0.4)
    scene.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in chips], lag_ratio=0.3), FadeIn(same), run_time=1.4)
    scene.play(*stage.turn(yaw=-0.12, pitch=0.42), run_time=1.6)

    # --- 5. Not particles: many particles moving together ---------------------------------------------
    beat(scene, t, 4)
    hide(scene, stage, 0.8, FadeOut(chips), FadeOut(same))
    centre = np.array([0.0, -0.3, 0.0])
    angle = Knob(0.0)
    orbit = Circle(radius=2.2, stroke_color=cfg.MUTED, stroke_width=2.5, stroke_opacity=0.5).move_to(centre)
    lone = glow_dot(centre + RIGHT * 2.2, cfg.BALL, 0.13)
    lone.add_updater(lambda m: m.move_to(centre + 2.2 * np.array([np.cos(angle.value), np.sin(angle.value), 0])))
    scene.play(Create(orbit), FadeIn(lone), run_time=1.0)
    drive(orbit, angle, 1.6)
    scene.wait(1.6)
    rings = [(0.55, 6), (1.1, 12), (1.65, 18), (2.2, 24)]
    dots = VGroup()
    for r, n in rings:
        for k in range(n):
            dots.add(glow_dot(ORIGIN, cfg.CYAN if r < 2.2 else cfg.BALL, 0.07, reach=2.4))
    base = [(r, 2 * np.pi * k / n) for r, n in rings for k in range(n)]

    def place(m):
        for d, (r, a) in zip(m, base):
            d.move_to(centre + r * np.array([np.cos(a + angle.value), np.sin(a + angle.value), 0.0]))

    place(dots)
    dots.add_updater(place)
    many = txt("an extended body: countless particles, one rotation", cfg.FONT["small"], cfg.WHITE).move_to(DOWN * 3.7)
    fit_width(many, 13.4)
    scene.play(FadeIn(dots, lag_ratio=0.02), FadeOut(lone), run_time=2.0)
    scene.play(FadeIn(many), run_time=0.8)

    # --- 6. The question ----------------------------------------------------------------------------------
    beat(scene, t, 5)
    q = VGroup(txt("Same force.", cfg.FONT["title"], cfg.FORCE),
               txt("Why three different motions?", cfg.FONT["title"], cfg.WHITE)).arrange(DOWN, buff=0.3)
    fit_width(q, 13.0)
    shade = Rectangle(width=16, height=9, stroke_width=0, fill_color=cfg.BG, fill_opacity=0.7)
    for mob in (dots, orbit):
        mob.clear_updaters()
    scene.play(FadeOut(many), FadeOut(dots), FadeOut(orbit), FadeIn(shade), FadeIn(q, scale=0.95), run_time=1.2)
    scene.remove(dots, orbit)

    # --- 7. Four new ideas ------------------------------------------------------------------------------------
    beat(scene, t, 6)
    ideas = VGroup(
        VGroup(com_target(0.24, glow=False), txt("centre of mass", cfg.FONT["small"], cfg.WHITE)).arrange(DOWN, buff=0.22),
        VGroup(eq(r"\vec\tau", cfg.FONT["title"], cfg.TORQUE), txt("torque", cfg.FONT["small"], cfg.TORQUE)).arrange(DOWN, buff=0.18),
        VGroup(eq("I", cfg.FONT["title"], cfg.INERTIA), txt("moment of inertia", cfg.FONT["small"], cfg.INERTIA)).arrange(DOWN, buff=0.18),
        VGroup(eq(r"\vec L", cfg.FONT["title"], cfg.ANG_MOMENTUM), txt("angular momentum", cfg.FONT["small"], cfg.ANG_MOMENTUM)).arrange(DOWN, buff=0.18),
    ).arrange(RIGHT, buff=0.75)
    fit_width(ideas, 13.8)
    ideas.move_to(DOWN * 0.4)
    scene.play(q.animate.scale(0.62).move_to(UP * 2.9), run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(i, shift=UP * 0.2) for i in ideas], lag_ratio=0.25), run_time=1.8)

    # --- 8. Title ------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    card = title_card("System of Particles", "& Rotational Motion")
    sub = txt(cfg.VIDEO_SUBTITLE, cfg.FONT["body"], cfg.WHITE)
    group = VGroup(card, sub).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
    clear(scene, shade, run_time=0.8)
    scene.play(FadeIn(card.shadow), FadeIn(card.glow), Write(card.title), run_time=1.6)
    scene.play(FadeIn(sub, shift=UP * 0.15), run_time=0.9)
    finish(scene, t, fill=lambda s: [card.glow.animate.set_opacity(0.05)])


def swap_anim(old: Mobject, new: Mobject) -> Animation:
    return fade_through(old, new)
