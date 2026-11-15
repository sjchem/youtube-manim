"""Scene 16 — radius of gyration. A solid disc turns on a 3D stage. Its mass
is imagined gathered into a thin copper ring that grows outward from the
axis; a live readout of the ring's I / M R^2 climbs until it equals the
disc's one half, at k = R / sqrt 2. I = M k^2 and k = sqrt(I / M) are
written. For a thin ring k = R (the ring already sits at the rim); for the
disc k is about 0.71 R. The two k's are compared as teal radii.
"""

from manim_scenes.common import *

R = 2.0
K_DISC = pm.GYRATION.disc


class Scene16Gyration(Scene):
    def construct(self) -> None:
        play_scene(self)


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "16", "Radius of gyration")
    stage = Stage((-2.6, -0.6, 0.0), zoom=1.6, yaw=-0.25, pitch=0.5, sway=0.02)
    spin = Knob(0.0)
    drive(stage, spin, 0.7)
    disc = Drum(ORIGIN, R, 0.1, cfg.DISC_BODY, axis=(0, 1, 0), spin=lambda: spin.value, stripe=cfg.DISC_STRIPE, sectors=8)
    axis = axis_line(stage, [0, -1.4, 0], [0, 1.9, 0], cfg.ANGLE, 0.9)
    stage.add_body(disc)
    show(scene, stage, 1.0)
    one = caption("one length to sum up a whole mass distribution?", cfg.WHITE)
    scene.play(FadeIn(one), run_time=0.8)

    # --- 2. Gather the mass into a ring at k ----------------------------------------------------------------------------------
    beat(scene, t, 1)
    k = Knob(0.05)
    ring = Hoop(lambda: np.array([0.0, 0.32, 0.0]), lambda: k.value * R, cfg.RING_BODY, axis=(0, 1, 0),
                spin=lambda: spin.value, width=16)
    ring.presence = 0.0
    stage.add_body(ring)
    k_vec = Segment(lambda: np.array([0.0, 0.34, 0.0]), lambda: np.array([k.value * R, 0.34, 0.0]), cfg.POSITION, width=6,
                    opacity=1.0)
    k_vec.bias = 45.0
    k_vec.presence = 0.0
    k_lab = Tag(eq("k", cfg.FONT["section"], cfg.POSITION), lambda: np.array([k.value * R / 2, 0.34, 0.0]), UP * 0.42)
    k_lab.presence = 0.0
    stage.add_body(k_vec)
    stage.add_overlay(k_lab)
    scene.play(stage.fade(disc, 0.25), stage.fade(ring, 1.0), stage.fade(k_vec, 1.0), stage.fade(k_lab, 1.0), FadeOut(one),
               run_time=1.0)
    ring_I = readout(r"\text{ring at }k:\ I/MR^2 =", lambda: k.value ** 2, 2, "", cfg.RING_BODY, size=46)
    disc_I = eq(rf"\text{{disc}}:\ I/MR^2 = {fx(float(pm.shape('disc').coefficient), 2)}", cfg.FONT["body"], cfg.DISC_STRIPE)
    panel_group = VGroup(disc_I, ring_I).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([4.3, 2.6, 0])
    scene.play(FadeIn(panel_group), run_time=0.7)
    scene.play(k.to(stage, 1.0), run_time=2.4)
    scene.play(k.to(stage, K_DISC), run_time=2.4)
    match = caption("same I at radius k", cfg.POSITION)
    matched = glow_frame(ring_I, cfg.BALANCED)
    scene.play(FadeIn(match), Create(matched), run_time=1.0)

    # --- 3. I = M k^2 ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    laws = VGroup(eq(r"I = M k^2", cfg.FONT["title"], cfg.WHITE), eq(r"k = \sqrt{I \over M}", cfg.FONT["title"], cfg.POSITION))
    laws.arrange(DOWN, buff=0.45).move_to([4.3, -0.6, 0])
    scene.play(Write(laws[0]), FadeOut(match), run_time=1.2)
    scene.play(Write(laws[1]), run_time=1.2)

    # --- 4. Thin ring: k = R ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 3)
    ring_case = eq(r"\text{thin ring: } k = R", cfg.FONT["section"], cfg.RING_BODY).move_to([0, -3.6, 0])
    scene.play(k.to(stage, 1.0), stage.fade(disc, 0.0), FadeIn(ring_case), FadeOut(matched), run_time=1.6)

    # --- 5. Disc: k = R / sqrt 2 ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    disc_case = eq(rf"\text{{disc: }} k = {{R \over \sqrt 2}} \approx {fx(K_DISC, 2)}\,R", cfg.FONT["section"], cfg.DISC_STRIPE)
    disc_case.move_to(ring_case)
    scene.play(k.to(stage, K_DISC), stage.fade(disc, 0.3), fade_through(ring_case, disc_case), run_time=1.8)
    rim = Hoop(np.array([0.0, 0.3, 0.0]), R, cfg.MUTED, axis=(0, 1, 0), width=5, stripes=0)
    rim.presence = 0.0
    stage.add_body(rim)
    scene.play(stage.fade(rim, 0.7), run_time=0.8)

    # --- 6. Bookkeeping, but telling ------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    note = caption("k: an effective distance from the axis", cfg.WHITE)
    scene.play(fade_through(disc_case, note), run_time=0.9)
    finish(scene, t, stage)
