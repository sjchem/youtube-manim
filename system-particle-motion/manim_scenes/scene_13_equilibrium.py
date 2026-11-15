"""Scene 13 — equilibrium: the balanced seesaw. Two condition cards: the sum
of external forces is zero (translational), the sum of external torques is
zero (rotational). A puck gliding at constant velocity and a disc spinning
steadily show that equilibrium need not mean rest. Then a 3D seesaw: a 100 N
child 2 m left of the pivot, a 200 N child 1 m right. Purple turning arrows
carry 200 N m counterclockwise and 200 N m clockwise; the net torque is zero.
The weights add to 300 N down; the pivot pushes 300 N up; the net force is
zero. Finally the light child slides to 1.5 m and the plank tips.
"""

from manim_scenes.common import *

SW = pm.SEESAW
S = 1.75                    # screen units per metre along the plank
H = 1.0                     # pivot height
F_PER_N = 0.006             # arrow length per newton
MOVED = 1.5                 # metres: where the light child slides to


class Scene13Equilibrium(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "13", "Equilibrium: the balanced seesaw")
    cards = VGroup(
        on_panel(VGroup(txt("translational", cfg.FONT["label"], cfg.FORCE),
                        eq(r"\sum \vec F_{\text{ext}} = 0", cfg.FONT["section"], cfg.WHITE),
                        txt("no acceleration of the centre", cfg.FONT["tiny"], cfg.FORCE)).arrange(DOWN, buff=0.25), cfg.FORCE),
        on_panel(VGroup(txt("rotational", cfg.FONT["label"], cfg.TORQUE),
                        eq(r"\sum \vec \tau_{\text{ext}} = 0", cfg.FONT["section"], cfg.WHITE),
                        txt("no change in the rotation", cfg.FONT["tiny"], cfg.TORQUE)).arrange(DOWN, buff=0.25), cfg.TORQUE),
    ).arrange(RIGHT, buff=1.0).move_to(UP * 0.6)
    for card in cards:
        card.body[2].set_opacity(0)
    two = caption("two separate conditions", cfg.WHITE)
    scene.play(FadeIn(two), run_time=0.8)

    # --- 2/3. The two conditions -------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    scene.play(FadeIn(cards[0], shift=UP * 0.2), run_time=1.0)
    scene.play(cards[0].body[2].animate.set_opacity(1), run_time=0.7)
    beat(scene, t, 2)
    scene.play(FadeIn(cards[1], shift=UP * 0.2), run_time=1.0)
    scene.play(cards[1].body[2].animate.set_opacity(1), run_time=0.7)

    # --- 4. Not necessarily at rest -------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    scene.play(FadeOut(two), cards.animate.scale(0.72).move_to(UP * 2.85), run_time=1.0)
    demo = Stage((0.0, -1.6, 0.0), zoom=1.25, yaw=-0.2, pitch=0.35, sway=0.02)
    floor(demo, 0.0, reach=6.0, opacity=0.2)
    glide, spin = Knob(-5.0), Knob(0.0)
    drive(demo, spin, 2.2)
    puck = Drum(lambda: np.array([glide.value, 0.15, 1.0]), 0.45, 0.15, cfg.ORANGE, axis=(0, 1, 0), sectors=2)
    v_puck = Vector(lambda: np.array([glide.value, 0.6, 1.0]), lambda: np.array([glide.value + 1.3, 0.6, 1.0]), cfg.VELOCITY,
                    width=0.08, tip=0.26)
    top = Drum(np.array([2.8, 0.9, -0.6]), 1.0, 0.1, cfg.DISC_BODY, axis=(0, 0, 1), spin=lambda: spin.value, sectors=8,
               stripe=cfg.DISC_STRIPE)
    post = Drum(np.array([2.8, 0.4, -0.75]), 0.08, 0.45, cfg.STEEL, axis=(0, 1, 0), sectors=2)
    demo.add_body(post, puck, top)
    demo.add_overlay(v_puck)
    show(scene, demo, 0.9)
    scene.play(glide.to(demo, 0.5, rate_func=linear), run_time=4.0)
    labels = VGroup(txt("constant velocity", cfg.FONT["small"], cfg.VELOCITY).move_to([-2.2, -3.2, 0]),
                    txt("steady spin", cfg.FONT["small"], cfg.OMEGA).move_to([3.4, -3.2, 0]))
    scene.play(FadeIn(labels), glide.to(demo, 1.6, rate_func=linear), run_time=1.0)
    rest = caption("equilibrium need not mean rest; starting at rest, it stays at rest: static", cfg.WHITE,
                   cfg.FONT["small"])
    scene.play(glide.to(demo, 4.0, rate_func=linear), FadeOut(labels), run_time=2.2)
    scene.play(FadeIn(rest), run_time=0.8)

    # --- 5. The seesaw ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    hide(scene, demo, 0.8, FadeOut(rest))
    stage = Stage((0.0, -2.85, 0.0), zoom=1.15, yaw=-0.18, pitch=0.28, sway=0.025)
    floor(stage, 0.0, reach=7.0, opacity=0.2)
    tilt, d_left = Knob(0.0), Knob(SW.d_left)

    def on_plank(x_m: float, lift: float = 0.0) -> np.ndarray:
        return np.array([0.0, H, 0.0]) + mu.rotation_z(tilt.value) @ np.array([x_m * S, 0.1 + lift, 0.0])

    plank = Block(lambda: np.array([0.0, H + 0.05, 0.0]), (2.6 * S * 2, 0.12, 0.8), cfg.WOOD, pose=lambda: mu.rotation_z(tilt.value))
    verts, faces = prism([[-0.55, 0.0], [0.55, 0.0], [0.0, H - 0.02]], 0.5)
    wedge = Solid(verts, faces, cfg.STEEL)
    kid_l = Block(lambda: on_plank(-d_left.value, 0.42), (0.55, 0.8, 0.55), cfg.CYAN, pose=lambda: mu.rotation_z(tilt.value))
    kid_r = Block(lambda: on_plank(SW.d_right, 0.55), (0.75, 1.05, 0.75), cfg.ORANGE, pose=lambda: mu.rotation_z(tilt.value))
    stage.add_body(wedge, plank)
    hidden(kid_l, kid_r)
    stage.add_body(kid_l, kid_r)
    show(scene, stage, 1.0)
    w_l = Vector(lambda: on_plank(-d_left.value, 1.0), lambda: on_plank(-d_left.value, 1.0) - np.array([0, SW.w_left * F_PER_N, 0]),
                 cfg.FORCE, width=0.09, tip=0.28)
    w_l_lab = Tag(txt(f"{fx(SW.w_left)} N", cfg.FONT["label"], cfg.FORCE), lambda: on_plank(-d_left.value, 0.6), LEFT * 1.3)
    m_l = Tag(txt(f"{fx(SW.d_left)} m", cfg.FONT["label"], cfg.POSITION), lambda: on_plank(-d_left.value / 2), DOWN * 0.55)
    hidden(w_l, w_l_lab, m_l)
    stage.add_overlay(w_l, w_l_lab, m_l)
    scene.play(stage.fade(kid_l, 1.0), run_time=0.8)
    scene.play(stage.fade(w_l, 1.0), stage.fade(w_l_lab, 1.0), stage.fade(m_l, 1.0), run_time=0.9)

    # --- 6. The heavier child ------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    w_r = Vector(lambda: on_plank(SW.d_right, 1.3), lambda: on_plank(SW.d_right, 1.3) - np.array([0, SW.w_right * F_PER_N, 0]),
                 cfg.FORCE, width=0.09, tip=0.28)
    w_r_lab = Tag(txt(f"{fx(SW.w_right)} N", cfg.FONT["label"], cfg.FORCE), lambda: on_plank(SW.d_right, 0.8), RIGHT * 1.4)
    m_r = Tag(txt(f"{fx(SW.d_right)} m", cfg.FONT["label"], cfg.POSITION), lambda: on_plank(SW.d_right / 2), DOWN * 0.55)
    hidden(w_r, w_r_lab, m_r)
    stage.add_overlay(w_r, w_r_lab, m_r)
    scene.play(stage.fade(kid_r, 1.0), run_time=0.8)
    scene.play(stage.fade(w_r, 1.0), stage.fade(w_r_lab, 1.0), stage.fade(m_r, 1.0), run_time=0.9)

    # --- 7. The two torques ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 6)
    torques = VGroup(
        eq(rf"{fx(SW.w_left)}\times{fx(SW.d_left)} = {fx(SW.tau_ccw)}\ \mathrm{{N\,m}}\ \circlearrowleft", cfg.FONT["body"],
           cfg.TORQUE),
        eq(rf"{fx(SW.w_right)}\times{fx(SW.d_right)} = {fx(SW.tau_cw)}\ \mathrm{{N\,m}}\ \circlearrowright", cfg.FONT["body"],
           cfg.TORQUE),
    ).arrange(RIGHT, buff=1.0)
    fit_width(torques, 13.6)
    torques.move_to(UP * 3.3)
    scene.play(FadeOut(cards), run_time=0.6)
    scene.play(Write(torques[0]), run_time=1.6)
    scene.play(Write(torques[1]), run_time=1.6)

    # --- 8. Net torque zero ---------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 7)
    net_tau = eq(rf"\sum\tau = {fx(SW.tau_ccw)} - {fx(SW.tau_cw)} = {fx(SW.net_torque)}", cfg.FONT["body"], cfg.TORQUE)
    net_tau.move_to(UP * 2.5)
    scene.play(Write(net_tau), run_time=1.4)
    tick = check_mark(0.3, cfg.BALANCED).next_to(net_tau, RIGHT, buff=0.35)
    scene.play(Create(tick), run_time=0.6)

    # --- 9. Forces: the pivot pushes up ----------------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    N = Vector(np.array([0.0, H + 0.2, 0.5]), np.array([0.0, H + 0.2 + SW.pivot * F_PER_N, 0.5]), cfg.FORCE, width=0.11,
               tip=0.32)    # the pivot's push on the plank, drawn at the pivot
    N_lab = Tag(txt(f"{fx(SW.pivot)} N", cfg.FONT["label"], cfg.FORCE), np.array([0.0, H + 0.2 + SW.pivot * F_PER_N, 0.5]),
                UP * 0.35)
    hidden(N, N_lab)
    stage.add_overlay(N, N_lab)
    down = caption(f"{fx(SW.pivot)} N down in total", cfg.FORCE)
    scene.play(FadeIn(down), run_time=0.6)
    scene.play(stage.fade(N, 1.0), stage.fade(N_lab, 1.0), run_time=1.0)
    up = caption(f"so the pivot pushes up with {fx(SW.pivot)} N", cfg.FORCE)
    scene.play(fade_through(down, up), run_time=0.8)

    # --- 10. Net force zero: mechanical equilibrium --------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    net_F = eq(rf"\sum F_y = {fx(SW.pivot)} - {fx(SW.w_left)} - {fx(SW.w_right)} = 0", cfg.FONT["body"], cfg.FORCE)
    net_F.move_to(UP * 1.35)
    tick2 = check_mark(0.3, cfg.BALANCED).next_to(net_F, RIGHT, buff=0.35)
    scene.play(FadeOut(up), stage.fade(N_lab, 0.0), run_time=0.35)
    scene.play(Write(net_F), run_time=1.05)
    scene.play(Create(tick2), run_time=0.5)
    mech = result_label("mechanical equilibrium", cfg.BALANCED, cfg.FONT["section"]).move_to(DOWN * 3.6)
    scene.play(FadeIn(mech, scale=1.08), run_time=0.8)

    # --- 11. Move the light child: it tips -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    scene.play(FadeOut(VGroup(mech, torques, net_tau, tick, net_F, tick2)),
               stage.fade(N, 0.0), stage.fade(m_l, 0.0), run_time=0.5)
    moved_tau = eq(rf"\tau_{{\mathrm{{net}}}} = {fx(SW.w_left)}\times{fx(MOVED, 1)} - {fx(SW.tau_cw)}"
                   rf" = {fx(SW.w_left * MOVED - SW.tau_cw)}\ \mathrm{{N\,m}}", cfg.FONT["body"], cfg.WARNING)
    moved_tau.move_to(UP * 2.8)
    scene.play(d_left.to(stage, MOVED), Write(moved_tau), run_time=1.6)
    scene.play(tilt.to(stage, -0.2, rate_func=rate_functions.ease_in_quad), Indicate(moved_tau, color=cfg.WARNING), run_time=1.6)
    finish(scene, t, stage)
