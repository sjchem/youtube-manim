"""Scene 27 — layers that drag. A liquid between two steel plates on a turning
3D stage: the bottom plate is held still, the top one slides. The liquid is
drawn as six translucent layers, each carrying a row of marker molecules that
flow at its own speed, u = U z / h (the liquid touching each plate moves with
it). Gold arrows at the side show the linear velocity profile; a dashed line
through their tips and a small rise-over-run triangle give the velocity
gradient du/dz.

Then the molecular picture: molecules hop from layer to layer carrying their
momentum (gold arcs), and green links represent forces transferring momentum between neighbouring
layers. This is viscous shear, not dry friction. An orange force arrow keeps the top plate moving; the plate's area A
is outlined, and Newton's law of viscosity F/A = η du/dz is boxed, with η in
pascal seconds: a Newtonian liquid.
"""

from manim_scenes.common import *
from manim_scenes.kit_d import at_word
from manim_scenes.kit_g import FlowDots, hop_path

STAGE_AT = (-2.45, -0.6, 0.0)
HALF_X, HALF_Z = 2.4, 1.15
GAP = 2.4                     # liquid depth h between the plates (stage units)
N_LAYERS = 6
PER_LAYER = 9
U_TOP = 1.1                   # top plate speed, stage units per second
COL_X = 4.9


class Scene27Viscosity(Scene):
    def construct(self) -> None:
        play_scene(self)


def layer_y(k: float) -> float:
    return -GAP / 2 + (k + 0.5) * GAP / N_LAYERS


def play_scene(scene: Scene) -> None:
    t, _ = start(scene, "27", TITLES["27"])
    stage = Stage(STAGE_AT, zoom=1.3, yaw=-0.45, pitch=0.3, sway=0.03)
    speed = Knob(0.0)            # top plate speed (0..U_TOP)
    offsets = np.zeros(N_LAYERS + 1)
    rng = np.random.default_rng(cfg.SEED + 270)
    base_x = np.array([np.linspace(-HALF_X, HALF_X, PER_LAYER, endpoint=False) + rng.uniform(0, 0.4) for _ in range(N_LAYERS)])
    base_z = rng.uniform(-0.75, 0.75, (N_LAYERS, PER_LAYER)) * HALF_Z
    clock = {"last": None}

    def advance() -> None:
        now = stage.clock
        dt = 0.0 if clock["last"] is None else min(max(now - clock["last"], 0.0), 0.3)
        clock["last"] = now
        for k in range(N_LAYERS):
            offsets[k] += speed.value * (layer_y(k) + GAP / 2) / GAP * dt
        offsets[N_LAYERS] += speed.value * dt

    def wrapped(k: int) -> np.ndarray:
        return (base_x[k] + offsets[k] + HALF_X) % (2 * HALF_X) - HALF_X

    def flow_points() -> np.ndarray:
        return np.array([[x, layer_y(k), z] for k in range(N_LAYERS) for x, z in zip(wrapped(k), base_z[k])])

    def flow_scale() -> np.ndarray:
        xs = np.concatenate([wrapped(k) for k in range(N_LAYERS)])
        return np.clip((HALF_X - np.abs(xs)) / 0.35, 0.0, 1.0)

    stage.add_body(Ticker(advance))
    bottom = Block(np.array([0.0, -GAP / 2 - 0.09, 0.0]), (2 * HALF_X + 0.4, 0.18, 2 * HALF_Z + 0.4), "#5A6B7A")
    top = Block(np.array([0.0, GAP / 2 + 0.09, 0.0]), (2 * HALF_X + 0.4, 0.18, 2 * HALF_Z + 0.4), cfg.STEEL)
    rivets = [Ball(lambda j=j: np.array([(j * 1.2 + offsets[N_LAYERS] + HALF_X) % (2 * HALF_X) - HALF_X, GAP / 2 + 0.2, 0.0]),
                   0.08, cfg.GOLD, layers=10) for j in range(4)]
    layers = []
    for k in range(N_LAYERS):
        y = layer_y(k)
        tone = mu.mix(cfg.LIQUID, cfg.LIQUID_EDGE, k / (N_LAYERS - 1))
        face = Face([np.array([-HALF_X, y, -HALF_Z]), np.array([HALF_X, y, -HALF_Z]), np.array([HALF_X, y, HALF_Z]),
                     np.array([-HALF_X, y, HALF_Z])], tone, opacity=0.1, edge_opacity=0.35)
        layers.append(face)
    dots = FlowDots(flow_points, mu.mix(cfg.LIQUID_EDGE, cfg.WHITE, 0.3), flow_scale, radius=0.1)
    dots.presence = 0.0
    stage.add_body(bottom, *layers, dots, top, *rivets)
    show(scene, stage, 1.0)

    # --- 0. Viscosity is about flow -----------------------------------------------------------------------------------
    tag = VGroup(txt("surface tension: the surface", cfg.FONT["small"], cfg.MUTED), txt("viscosity: the flow", cfg.FONT["section"], cfg.GOLD))
    tag.arrange(DOWN, buff=0.3).move_to([COL_X, 2.6, 0])
    scene.play(FadeIn(tag[0], shift=DOWN * 0.1), run_time=0.8)
    at_word(scene, t, 0, "Viscosity", lead=0.2)
    play_in(scene, t, 1, FadeIn(tag[1], shift=DOWN * 0.1), *stage.turn(yaw=-0.35), run_time=1.0)

    # --- 1. Hold the bottom plate, slide the top one ---------------------------------------------------------------------
    beat(scene, t, 1)
    still = Tag(txt("held still", cfg.FONT["small"], cfg.MUTED), np.array([0, -GAP / 2 - 0.2, HALF_Z + 0.2]), DOWN * 0.35)
    slide = Tag(txt("slides", cfg.FONT["small"], cfg.GOLD), np.array([0, GAP / 2 + 0.2, HALF_Z + 0.2]), UP * 0.45)
    still.presence = slide.presence = 0.0
    stage.add_overlay(still, slide)
    scene.play(stage.fade(still, 1.0), run_time=0.8)
    at_word(scene, t, 1, "slide", lead=0.3)
    play_in(scene, t, 2, stage.fade(slide, 1.0), speed.to(stage, U_TOP, rate_func=rush_into), run_time=2.4)

    # --- 2. Smooth layers, each a little faster: laminar flow ------------------------------------------------------------------
    beat(scene, t, 2)
    scene.play(stage.fade(dots, 1.0), *[set_attr(stage, f, "opacity", 0.16) for f in layers], run_time=1.2)
    profile_x = -HALF_X - 0.55
    arrows = []
    for k in range(N_LAYERS):
        y = layer_y(k)
        length = (y + GAP / 2) / GAP * 2.4
        v = Vector(np.array([profile_x, y, HALF_Z]), np.array([profile_x + length, y, HALF_Z]), cfg.VELOCITY, width=0.07, tip=0.2)
        v.presence = 0.0
        arrows.append(v)
    stage.add_overlay(*arrows)
    at_word(scene, t, 2, "between", lead=0.3)
    scene.play(LaggedStart(*[stage.fade(a, 1.0) for a in arrows], lag_ratio=0.25), run_time=2.4)
    at_word(scene, t, 2, "laminar", lead=0.3)
    laminar = result_label("laminar flow", cfg.CYAN, cfg.FONT["section"]).move_to([COL_X, 1.0, 0])
    play_in(scene, t, 3, FadeIn(laminar, shift=DOWN * 0.1), run_time=1.0)

    # --- 3. The velocity gradient du/dz --------------------------------------------------------------------------------------
    beat(scene, t, 3)
    tips = Curve(np.array([[profile_x + (layer_y(k) + GAP / 2) / GAP * 2.4, layer_y(k), HALF_Z] for k in (-0.5, N_LAYERS - 0.5)]),
                 cfg.WHITE, width=3, dashed=True)
    tips.presence = 0.0
    stage.add_body(tips)
    scene.play(stage.fade(tips, 1.0), run_time=1.0)
    grad = VGroup(eq(r"\frac{du}{dz}", cfg.FONT["title"], cfg.VELOCITY), txt("velocity gradient", cfg.FONT["label"], cfg.WHITE))
    grad.arrange(DOWN, buff=0.2).move_to([COL_X, -0.85, 0])
    at_word(scene, t, 3, "d", lead=0.3)
    scene.play(Write(grad[0]), run_time=1.2)
    play_in(scene, t, 4, FadeIn(grad[1:], shift=LEFT * 0.1), run_time=1.0)

    # --- 4. Molecules hop between layers, carrying momentum; attraction resists -----------------------------------------------------
    beat(scene, t, 4)
    hop = Knob(0.0)
    hops = []
    for k, (a, b) in enumerate(((0.6, 1), (-1.0, 3), (1.2, 4), (-0.2, 2))):
        start_pt = np.array([a, layer_y(b - 1), 0.4 * (k - 1.5)])
        end_pt = np.array([a + 0.9, layer_y(b), 0.4 * (k - 1.5)])
        path = hop_path(start_pt, end_pt, lift=0.35, samples=30)
        hops.append(path)
    hoppers = [Ball(lambda p=p: p[int(hop.value * (len(p) - 1))], 0.12, cfg.GOLD, layers=12) for p in hops]
    trails = [Curve(lambda p=p: p[: int(hop.value * (len(p) - 1)) + 1], cfg.GOLD, width=3.5) for p in hops]
    for b_ in (*hoppers, *trails):
        b_.presence = 0.0
        b_.bias = 50.0
    stage.add_body(*trails, *hoppers)
    scene.play(*fade_all(stage, [*hoppers, *trails], 1.0), run_time=0.6)
    at_word(scene, t, 4, "momentum", lead=0.4)
    momentum = txt("carry momentum", cfg.FONT["label"], cfg.GOLD).move_to([COL_X, -2.55, 0])
    scene.play(hop.to(stage, 1.0, rate_func=smooth), FadeIn(momentum, shift=UP * 0.1), run_time=2.0)
    at_word(scene, t, 4, "forces", lead=0.3)
    pairs = np.array([[x, layer_y(k), z] for k in (1, 2, 3, 4) for x, z in ((-1.4, -0.3), (0.2, 0.4), (1.5, -0.1))])
    seg = [Segment(pairs[i], pairs[i + 3], cfg.ATTRACT, width=4, opacity=0.85) for i in range(len(pairs) - 3)]
    for s_ in seg:
        s_.presence = 0.0
    stage.add_body(*seg)
    resist = txt("attraction resists sliding", cfg.FONT["label"], cfg.ATTRACT).move_to([COL_X, -3.25, 0])
    play_in(scene, t, 5, *fade_all(stage, seg, 1.0), FadeIn(resist, shift=UP * 0.1), run_time=1.2)

    # --- 5. A steady force keeps the plate moving: F/A = η du/dz ------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(*fade_all(stage, [*hoppers, *trails, *seg], 0.0), FadeOut(VGroup(momentum, resist, laminar, tag)), run_time=0.8)
    force = Vector(np.array([HALF_X + 0.3, GAP / 2 + 0.09, 0.0]), np.array([HALF_X + 1.2, GAP / 2 + 0.09, 0.0]), cfg.IMPULSE,
                   width=0.13, tip=0.34)
    force_tag = Tag(eq("F", cfg.FONT["title"], cfg.IMPULSE), np.array([HALF_X + 1.0, GAP / 2 + 0.09, 0.0]), UP * 0.55)
    area = Face([np.array([-HALF_X - 0.2, GAP / 2 + 0.19, -HALF_Z - 0.2]), np.array([HALF_X + 0.2, GAP / 2 + 0.19, -HALF_Z - 0.2]),
                 np.array([HALF_X + 0.2, GAP / 2 + 0.19, HALF_Z + 0.2]), np.array([-HALF_X - 0.2, GAP / 2 + 0.19, HALF_Z + 0.2])],
                cfg.GOLD, opacity=0.12, edge_opacity=0.95)
    area.bias = 300.0
    area_tag = Tag(eq("A", cfg.FONT["title"], cfg.GOLD), np.array([-HALF_X + 0.3, GAP / 2 + 0.2, -HALF_Z]), UP * 0.5)
    for thing in (force, force_tag, area, area_tag):
        thing.presence = 0.0
    stage.add_overlay(force, force_tag, area_tag)
    stage.add_body(area)
    scene.play(stage.glide([-3.1, -0.6, 0]), stage.zoom_to(1.12), stage.fade(force, 1.0), stage.fade(force_tag, 1.0), stage.fade(slide, 0.0), run_time=1.0)
    at_word(scene, t, 5, "area", lead=0.3)
    scene.play(stage.fade(area, 1.0), stage.fade(area_tag, 1.0), run_time=1.0)
    at_word(scene, t, 5, "proportional", lead=0.3)
    law = paint(eq([r"\frac{F}{A}", "=", r"\eta", r"\frac{du}{dz}"], cfg.FONT["title"]), {0: cfg.IMPULSE, 2: cfg.GOLD, 3: cfg.VELOCITY})
    law_box = boxed(law, cfg.GOLD, buff=0.24).move_to([COL_X, 1.2, 0])
    scene.play(fade_through(grad, law), run_time=1.2)
    scene.remove(grad)
    at_word(scene, t, 5, "eta", lead=0.3)
    play_in(scene, t, 6, Create(law_box.frame), Indicate(law[2], color=cfg.WHITE, scale_factor=1.3), run_time=1.4)

    # --- 6. η is the viscosity, in pascal seconds; Newtonian liquids ---------------------------------------------------------------
    beat(scene, t, 6)
    name = VGroup(eq(r"\eta", cfg.FONT["title"], cfg.GOLD), txt("viscosity", cfg.FONT["section"], cfg.WHITE)).arrange(RIGHT, buff=0.3)
    name.move_to([COL_X, -0.5, 0])
    unit = eq(r"\mathrm{Pa\,s}", cfg.FONT["section"], cfg.MUTED).next_to(name, DOWN, buff=0.3)
    scene.play(FadeIn(name, shift=UP * 0.1), run_time=0.9)
    at_word(scene, t, 6, "pascal", lead=0.3)
    scene.play(FadeIn(unit, shift=UP * 0.1), run_time=0.8)
    at_word(scene, t, 6, "Newtonian", lead=0.3)
    newton = chip("Newtonian liquid", cfg.CYAN, cfg.FONT["label"]).next_to(unit, DOWN, buff=0.35)
    scene.play(FadeIn(newton, scale=1.1), run_time=0.9)
    finish(scene, t, stage, drift=0.15)
