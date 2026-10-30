"""Scene 16 — one part per million, made visible: a real 1000 x 1000 field of
dots (one of them gold), rendered live at every zoom level from a single dot
to the whole million, then a 3D cube of a thousand such squares for one part
per billion. Then the basis: mass ppm, mg/L in water, molecule-count ppm in air.
"""

from manim_scenes.common import *

N = 1000                          # dots per side: one million in all
GOLD_RC = (377, 613)              # row, column of the single gold dot
SIDE = 6.4                        # screen size of the square
CENTRE = np.array([-3.0, -0.4, 0.0])
RX = 4.5
PIXELS = 540


class Scene16Ppm(Scene):
    def construct(self) -> None:
        play_scene(self)


class DotField(ImageMobject):
    """A 1000 x 1000 grid of particles drawn for the current view: ``span``
    dots across. Far out, dots blend into an even blue; close in, each dot is
    a disc and the gold one glows."""

    def __init__(self) -> None:
        self.span = 1.4
        self.blue = np.array(ManimColor(cfg.SOLVENT).to_rgb())
        self.gold = np.array(ManimColor(cfg.SOLUTE).to_rgb())
        self.bg = np.array(ManimColor(cfg.PANEL).to_rgb())
        super().__init__(self._render(), scale_to_resolution=1080)
        self.set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])
        self.height = SIDE
        self.move_to(CENTRE)

    def centre(self) -> np.ndarray:
        gold = np.array([GOLD_RC[1] + 0.5, GOLD_RC[0] + 0.5])
        mid = np.array([N / 2, N / 2])
        w = np.clip((np.log(self.span) - np.log(30.0)) / (np.log(N) - np.log(30.0)), 0, 1)
        w = w * w * (3 - 2 * w)
        return gold * (1 - w) + mid * w

    def _render(self) -> np.ndarray:
        cx, cy = self.centre()
        s = self.span
        step = s / PIXELS
        u = cx - s / 2 + (np.arange(PIXELS) + 0.5) * step
        v = cy - s / 2 + (np.arange(PIXELS) + 0.5) * step
        U, V = np.meshgrid(u, v)
        inside = (U >= 0) & (U < N) & (V >= 0) & (V < N)
        col, row = np.floor(U), np.floor(V)
        d = np.hypot(U - col - 0.5, V - row - 0.5)
        r = 0.32
        disc = np.clip((r - d) / max(step, 1e-6) + 0.5, 0, 1)
        is_gold = (col == GOLD_RC[1]) & (row == GOLD_RC[0])
        glow = np.exp(-np.hypot(U - GOLD_RC[1] - 0.5, V - GOLD_RC[0] - 0.5) ** 2 / 0.9) * (s < 60)
        coverage = np.pi * r * r
        blend = np.clip((step - 0.12) / 0.3, 0, 1)        # 0: draw discs, 1: average density
        dot_alpha = disc * (1 - blend) + coverage * blend
        # Light each resolved disc as a sphere; distant dots retain their exact
        # grid coverage rather than turning into an invented particle texture.
        nx, ny = (U-col-0.5)/r, (V-row-0.5)/r
        nz = np.sqrt(np.clip(1-nx*nx-ny*ny,0,1))
        shade = 0.4 + 0.6*np.clip(-0.4*nx+0.55*ny+0.7*nz,0,1)
        specular = np.exp(-((nx+.32)**2+(ny-.42)**2)/.028)
        blue_tone = np.clip(self.blue[None,None,:]*(blend+(1-blend)*shade[...,None])
                            + .32*specular[...,None]*(1-blend),0,1)
        rgb = self.bg[None,None,:]*(1-dot_alpha[...,None])+blue_tone*dot_alpha[...,None]
        aura = .28*glow*(1-blend)
        rgb = rgb*(1-aura[...,None])+self.gold[None,None,:]*aura[...,None]
        gold_alpha = np.where(is_gold,disc,0.0)*(1-blend)
        gold_tone = np.clip(self.gold[None,None,:]*shade[...,None]+.48*specular[...,None],0,1)
        rgb = rgb*(1-gold_alpha[...,None])+gold_tone*gold_alpha[...,None]
        out = np.zeros((PIXELS, PIXELS, 4), dtype=np.uint8)
        out[..., :3] = np.clip(rgb * 255, 0, 255).astype(np.uint8)
        out[..., 3] = np.where(inside, 255, 0).astype(np.uint8)
        return out[::-1]

    def set_span(self, span: float) -> None:
        self.span = float(span)
        self.pixel_array = self._render()
        self.orig_alpha_pixel_array = self.pixel_array[:, :, 3].copy()

    def zoom(self, span: float, **kwargs) -> Param:
        """Zoom in log space so every decade takes the same time."""
        return Param(self, lambda: np.log(self.span), lambda v: self.set_span(np.exp(v)), np.log(span), **kwargs)


def billion_cube(at) -> Stage:
    """A cube split 10 x 10 x 10: a thousand million-dot squares."""
    stage = Stage(at, zoom=1.35, yaw=0.6, pitch=0.42, spin=0.2, sway=0.06)
    h = 1.6
    ticks = np.linspace(-h, h, 11)
    corners = [np.array([x, y, z]) for x in (-h, h) for y in (-h, h) for z in (-h, h)]
    for i, p in enumerate(corners):
        for q in corners[i + 1:]:
            if np.sum(np.abs(p - q) > 1e-9) == 1:
                stage.add_body(Segment(p, q, cfg.CYAN, 3.0, 0.9))
    for a in ticks[1:-1]:
        for axis in range(3):
            for other in range(3):
                if other == axis:
                    continue
                for side in (-h, h):
                    p = np.zeros(3)
                    q = np.zeros(3)
                    p[axis] = q[axis] = a
                    third = 3 - axis - other
                    p[third] = q[third] = side
                    p[other], q[other] = -h, h
                    stage.add_body(Segment(p, q, cfg.SOLVENT, 1.4, 0.35))
    for normal in range(3):
        for side in (-h, h):
            pts = []
            for s1, s2 in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                p = np.zeros(3)
                p[normal] = side
                others = [k for k in range(3) if k != normal]
                p[others[0]], p[others[1]] = s1 * h, s2 * h
                pts.append(p)
            stage.add_body(Face(pts, cfg.SOLVENT, opacity=0.05, edge_opacity=0.0))
    gold = Ball(np.array([0.48, 0.16, -0.8]), 0.09, cfg.SOLUTE)
    stage.add_body(gold, Halo(gold, cfg.SOLUTE, reach=4.0, peak=0.35))
    return stage


def play_scene(scene: Scene) -> None:
    t, head = start(scene, "16", "One part per million")
    uses = VGroup(*[chip(w, c) for w, c in (("lead in drinking water", cfg.MUTED), ("pollutants in air", cfg.MUTED),
                                             ("trace metals in a chip", cfg.MUTED))]).arrange(DOWN, buff=0.35)
    uses.move_to([0, 0.3, 0])
    scene.play(LaggedStart(*[FadeIn(u, shift=UP * 0.2) for u in uses], lag_ratio=0.35), run_time=1.8)

    # --- 2. ppm and ppb -------------------------------------------------------------------------------------------
    beat(scene, t, 1)
    units = VGroup(eq(r"1\ \mathrm{ppm} = 10^{-6}", cfg.FONT["title"], cfg.WHITE),
                   eq(r"1\ \mathrm{ppb} = 10^{-9}", cfg.FONT["title"], cfg.WHITE)).arrange(DOWN, buff=0.5).move_to([0, 0.3, 0])
    scene.play(FadeOut(uses), run_time=0.5)
    scene.play(Write(units[0]), run_time=1.1)
    scene.play(Write(units[1]), run_time=1.1)

    # --- 3. One gold particle ------------------------------------------------------------------------------------------
    beat(scene, t, 2)
    field = DotField()
    frame = SurroundingRectangle(field, buff=0.04, color=cfg.MUTED, stroke_width=2)
    scene.play(FadeOut(units), FadeIn(field), Create(frame), run_time=1.2)
    one = txt("one gold particle", cfg.FONT["body"], cfg.GOLD).move_to([RX, 1.6, 0])
    scene.play(FadeIn(one), run_time=0.6)

    # --- 4. Surround it with a thousand -------------------------------------------------------------------------------------
    beat(scene, t, 3)
    count = txt("1 in 1 000", cfg.FONT["section"], cfg.WHITE).move_to([RX, 0.3, 0])
    scene.play(field.zoom(31.6), run_time=3.2)
    scene.play(FadeIn(count), run_time=0.6)

    # --- 5. Zoom out: one million -----------------------------------------------------------------------------------------------
    beat(scene, t, 4)
    million = txt("1 in 1 000 000", cfg.FONT["section"], cfg.WHITE).move_to(count)
    scene.play(field.zoom(N * 1.02), fade_through(count, million), run_time=5.0, rate_func=smooth)
    scene.remove(count)
    where = txt("somewhere in here…", cfg.FONT["label"], cfg.MUTED).move_to([RX, -0.9, 0])
    scene.play(FadeIn(where), run_time=0.7)

    # --- 6. Zoom in: there it is ---------------------------------------------------------------------------------------------------
    beat(scene, t, 5)
    scene.play(field.zoom(6.0), FadeOut(where), run_time=4.6, rate_func=smooth)
    ppm = boxed(eq(r"1\ \mathrm{ppm} = 10^{-6}", cfg.FONT["section"], cfg.RESULT)).move_to([RX, -1.1, 0])
    scene.play(FadeIn(ppm, scale=1.06), Indicate(one, color=cfg.WHITE), run_time=1.0)

    # --- 7. One part per billion: a thousand squares ----------------------------------------------------------------------------------
    beat(scene, t, 6)
    scene.play(field.zoom(N * 1.02), run_time=1.6)
    scene.play(FadeOut(VGroup(one, million, ppm)), Group(field, frame).animate.scale(0.16).move_to([-5.9, 2.3, 0]),
               run_time=1.0)
    cube = billion_cube([-2.4, -0.5, 0])
    show(scene, cube, 1.2)
    thousand = txt("× 1 000 squares", cfg.FONT["body"], cfg.CYAN).move_to([RX - 0.4, 1.2, 0])
    ppb = boxed(eq(r"1\ \mathrm{ppb} = 10^{-9}", cfg.FONT["section"], cfg.RESULT)).move_to([RX - 0.4, -0.4, 0])
    scene.play(FadeIn(thousand), run_time=0.6)
    scene.play(FadeIn(ppb, scale=1.06), run_time=0.8)

    # --- 8. A second in 11.5 days; a second in 32 years ----------------------------------------------------------------------------------
    beat(scene, t, 7)
    hide(scene, cube, 0.6, FadeOut(VGroup(thousand, ppb)), FadeOut(Group(field, frame)))
    days = pm.seconds_to_days(1e6)
    years = pm.seconds_to_years(1e9)
    rows = VGroup(
        VGroup(txt("1 ppm", cfg.FONT["section"], cfg.GOLD), txt("≈ 1 second in", cfg.FONT["body"], cfg.WHITE),
               txt(f"{round(days * 2) / 2:g} days", cfg.FONT["section"], cfg.CYAN)).arrange(RIGHT, buff=0.35),
        VGroup(txt("1 ppb", cfg.FONT["section"], cfg.GOLD), txt("≈ 1 second in", cfg.FONT["body"], cfg.WHITE),
               txt(f"{years:.0f} years", cfg.FONT["section"], cfg.CYAN)).arrange(RIGHT, buff=0.35),
    ).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to([0, 0.3, 0])
    scene.play(FadeIn(rows[0], shift=RIGHT * 0.2), run_time=1.0)
    narration_wait(scene, 3.5)
    scene.play(FadeIn(rows[1], shift=RIGHT * 0.2), run_time=1.0)

    # --- 9. A ratio needs a basis: by mass ----------------------------------------------------------------------------------------------------
    beat(scene, t, 8)
    basis = txt("on what basis?", cfg.FONT["body"], cfg.GOLD).move_to([0, 2.4, 0])
    mass = eq(r"1\ \mathrm{ppm\ (mass)} = 1\ \mathrm{mg/kg}", cfg.FONT["section"], cfg.WHITE).move_to([0, 0.9, 0])
    scene.play(FadeOut(rows), FadeIn(basis), run_time=0.8)
    scene.play(Write(mass), run_time=1.4)

    # --- 10. ppb by mass ---------------------------------------------------------------------------------------------------------------------------
    beat(scene, t, 9)
    mass_b = eq(r"1\ \mathrm{ppb\ (mass)} = 1\ \mu\mathrm{g/kg}", cfg.FONT["section"], cfg.WHITE).move_to([0, -0.3, 0])
    scene.play(Write(mass_b), run_time=1.3)

    # --- 11. In dilute water, mg/L is close to ppm ------------------------------------------------------------------------------------------------
    beat(scene, t, 10)
    water = eq([r"1\ \mathrm{mg/L}", r"\approx", r"1\ \mathrm{ppm}"], cfg.FONT["section"]).move_to([0, -1.6, 0])
    water[1].set_color(cfg.GOLD)
    because = txt("in dilute water: 1 L ≈ 1 kg", cfg.FONT["small"], cfg.CYAN).next_to(water, DOWN, buff=0.25)
    scene.play(Write(water), run_time=1.3)
    scene.play(FadeIn(because), run_time=0.7)

    # --- 12. An approximation, not a definition ------------------------------------------------------------------------------------------------------
    beat(scene, t, 11)
    warn = chip("an approximation, not a definition", cfg.WARNING, cfg.FONT["label"]).move_to([0, -3.3, 0])
    scene.play(FadeIn(warn, shift=UP * 0.15), Indicate(water[1], color=cfg.WARNING, scale_factor=1.4), run_time=1.2)

    # --- 13. In air: counted by molecules -------------------------------------------------------------------------------------------------------------
    beat(scene, t, 12)
    scene.play(FadeOut(VGroup(mass, mass_b, water, because, warn)), run_time=0.7)
    air = VGroup(eq(r"\mathrm{CO_2}\ \text{in air} > 400\ \mathrm{ppm}", cfg.FONT["section"], cfg.WHITE),
                 txt("counted by molecules, not by mass", cfg.FONT["body"], cfg.AMOUNT)).arrange(DOWN, buff=0.4)
    air.move_to([0, 0.4, 0])
    scene.play(Write(air[0]), run_time=1.4)
    scene.play(FadeIn(air[1], shift=UP * 0.15), run_time=0.8)

    # --- 14. The same question as always ---------------------------------------------------------------------------------------------------------------
    beat(scene, t, 13)
    scene.play(FadeOut(VGroup(air, basis)), run_time=0.7)
    question = result_label("What are we comparing with what?", cfg.GOLD, cfg.FONT["title"]).move_to([0, 0.3, 0])
    fit_width(question, 13.6)
    scene.play(FadeIn(question, scale=0.95), run_time=1.2)
    scene.play(question.animate.scale(1.04), run_time=7.5)
    scene.play(Circumscribe(question, color=cfg.GOLD, buff=0.2), run_time=7.5)
    end_scene(scene, t, cfg.SCENE_DURATIONS["16"])
