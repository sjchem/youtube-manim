"""Smooth rotating CO2/H2O models and a clear molecular-geometry cliffhanger.

Rigid coordinates use measured C=O (116 pm), O-H (96 pm), H-O-H (104.5 deg)
and O=C=O (180 deg) data at one scale. Smooth projected spheres match Scene
16. Purple ellipsoids are schematic lone-pair hints, not computed orbitals.
"""

from manim_scenes.common import *

PM = 1 / 60
CO2_AT = np.array([-3.55, 0.65, 0])
H2O_AT = np.array([3.55, 0.95, 0])
CARBON, OXYGEN, HYDROGEN = "#9AA8B5", cfg.RED, cfg.WHITE


class Scene17GeometryTeaser(ThreeDScene):
    def construct(self) -> None:
        play_scene(self)


class GeometryMolecule(ProjectedMolecule):
    """A rigid model with an attached projected angle arc and soft LP lobes.

    Rotation is bounded to keep the molecular shape legible. The updater runs
    during narration holds, so movement never stops when a caption appears.
    """

    def __init__(self, kind: str) -> None:
        self.kind = kind
        if kind == "CO2":
            length = bd.MOLECULE_BOND_PM["C=O in CO2"] * PM
            sites = np.array([[-length, 0, 0], [0, 0, 0], [length, 0, 0]])
            symbols, bonds, centre = ["O", "C", "O"], [(0, 1, 2), (1, 2, 2)], CO2_AT
            angles = np.linspace(0, PI, 56)
        else:
            length = bd.MOLECULE_BOND_PM["O-H in H2O"] * PM
            half = np.radians(bd.BOND_ANGLE_DEG["H2O"] / 2)
            sites = np.array([[0, 0, 0], [-length * np.sin(half), -length * np.cos(half), 0],
                              [length * np.sin(half), -length * np.cos(half), 0]])
            symbols, bonds, centre = ["O", "H", "H"], [(0, 1, 1), (0, 2, 1)], H2O_AT
            angles = np.linspace(-PI / 2 - half, -PI / 2 + half, 56)
        super().__init__(sites, symbols, bonds, {"O": 0.48, "C": 0.42, "H": 0.31},
                         {"O": OXYGEN, "C": CARBON, "H": HYDROGEN}, centre)
        self.angle_sites = np.column_stack([0.74 * np.cos(angles), 0.74 * np.sin(angles), np.zeros_like(angles)])
        self.angle_arc = VMobject(stroke_color=cfg.GOLD, stroke_width=5, stroke_opacity=0)
        self.lobe_amount = ValueTracker(0)
        self.lobes = []
        self.lobe_templates = []
        self.lobe_alphas = []
        self.lobe_directions = []
        if kind == "H2O":
            for sign in (-1, 1):
                direction = np.array([0, np.cos(55 * DEGREES), sign * np.sin(55 * DEGREES)])
                lobe = polished_ball(1, cfg.PURPLE, layers=24)
                lobe[0].set_fill(cfg.PURPLE)
                self.lobes.append(lobe)
                self.lobe_templates.append([part.points.copy() for part in lobe])
                # Compensate for overlapping shading contours: the lobe stays
                # translucent instead of becoming an opaque stack of ellipses.
                self.lobe_alphas.append([0.22 if i == 0 else float(part.get_fill_opacity()) * (0.018 if i < 25 else 0.28)
                                         for i, part in enumerate(lobe)])
                self.lobe_directions.append(direction)
        self.remove(self.rods, self.atoms)
        self.display = VGroup(self.rods, *self._all_atoms, *self.lobes)
        self.add(self.display, self.angle_arc)
        self.rotation_time = 0.0
        self._advance_rotation(0)
        self.add_updater(lambda m, dt: m._advance_rotation(dt))

    def _advance_rotation(self, dt: float) -> None:
        self.rotation_time += dt
        t = self.rotation_time
        phase = 0.45 if self.kind == "CO2" else -0.65
        self.set_pose(0.62 * np.sin(0.24 * t + phase), 0.15 + 0.08 * np.sin(0.19 * t + phase))

    def _place(self) -> None:
        super()._place()
        if not hasattr(self, "display"):
            return  # The base constructor places the atom/bond geometry first.
        points, _, _ = self._project(self.angle_sites)
        self.angle_arc.set_points_smoothly(points)
        rotation = mu.rotation_x(self.tilt) @ mu.rotation_y(self.yaw)
        depths = (self.sites @ rotation.T)[:, 2]
        layers = list(zip(depths, self._all_atoms))
        for lobe, templates, alphas, direction in zip(self.lobes, self.lobe_templates, self.lobe_alphas, self.lobe_directions):
            centre, scale, depth = self._project(np.array([direction * 0.85]))
            axes = np.column_stack([RIGHT * 0.33, np.cross(direction, RIGHT) * 0.33, direction * 0.78])
            projected_axes = (rotation @ axes)[:2]
            covariance = projected_axes @ projected_axes.T
            values, vectors = np.linalg.eigh(covariance)
            # The positive matrix square root avoids eigenvector-sign flips in
            # the soft shading as a rotating lobe changes its projected axes.
            projection = vectors @ np.diag(np.sqrt(np.maximum(values, 0))) @ vectors.T * scale[0]
            for part, template, alpha in zip(lobe, templates, alphas):
                points = template.copy()
                points[:, :2] = template[:, :2] @ projection.T + centre[0, :2]
                points[:, 2] = 0
                part.points = points
                part.set_fill(opacity=alpha * self.lobe_amount.get_value(), family=False)
            layers.append((depth[0], lobe))
        self.display.submobjects = [self.rods] + [part for _, part in sorted(layers, key=lambda item: item[0])]


def carbon_dioxide() -> GeometryMolecule:
    return GeometryMolecule("CO2")


def water() -> GeometryMolecule:
    return GeometryMolecule("H2O")


def play_scene(scene: ThreeDScene) -> None:
    t, head = start(scene, "17", "Why does water bend?")
    # The molecules project their own rigid 3D coordinates, matching Scene 16's
    # smooth materials while keeping a front camera and crisp screen text.
    scene.set_camera_orientation(phi=0, theta=-PI / 2, zoom=1)

    understand = caption("Bonds explain the distance", cfg.CYAN, cfg.FONT["label"], y=-3.5)
    hud(scene, understand)
    scene.play(FadeIn(understand), run_time=0.8)
    dismiss_opening_title(scene, t, head)

    beat(scene, t, 1)
    co2 = carbon_dioxide()
    scene.play(FadeOut(understand), FadeIn(co2), run_time=1.2)
    co2_tag = VGroup(eq(r"\mathrm{CO_2}", cfg.FONT["body"], cfg.WHITE),
                     txt(f"straight · {bd.BOND_ANGLE_DEG['CO2']:.0f}°", cfg.FONT["label"], cfg.GOLD)).arrange(DOWN, buff=0.15)
    co2_tag.move_to([-3.55, -2.35, 0])
    hud(scene, co2_tag)
    scene.play(co2.angle_arc.animate.set_stroke(opacity=1), FadeIn(co2_tag), run_time=1.0)

    beat(scene, t, 2)
    h2o = water()
    scene.play(FadeIn(h2o), run_time=1.2)
    h2o_tag = VGroup(eq(r"\mathrm{H_2O}", cfg.FONT["body"], cfg.WHITE),
                     txt(f"bent · {bd.BOND_ANGLE_DEG['H2O']}°", cfg.FONT["label"], cfg.GOLD)).arrange(DOWN, buff=0.15)
    h2o_tag.move_to([3.55, -2.35, 0])
    hud(scene, h2o_tag)
    scene.play(h2o.angle_arc.animate.set_stroke(opacity=1), FadeIn(h2o_tag), run_time=1.0)

    beat(scene, t, 3)
    three = caption("Three atoms. Different shapes.", cfg.WHITE, cfg.FONT["label"], y=3.2)
    hud(scene, three)
    scene.play(FadeIn(three), run_time=0.8)
    scene.play(Indicate(co2_tag[1], color=cfg.WHITE, scale_factor=1.0), run_time=1.4)
    scene.play(Indicate(h2o_tag[1], color=cfg.WHITE, scale_factor=1.0), run_time=1.4)

    beat(scene, t, 4)
    angles = caption("What sets the bond angles?", cfg.GOLD, cfg.FONT["body"], y=3.2)
    hud(scene, angles)
    scene.play(*fade_labels(three, angles), run_time=0.9)
    # Animate each attached arc directly. Wrapping model children in a new
    # group would dismantle their live parent models when Manim adds it.
    scene.play(Indicate(co2.angle_arc, color=cfg.WHITE, scale_factor=1.0),
               Indicate(h2o.angle_arc, color=cfg.WHITE, scale_factor=1.0), run_time=1.6)

    beat(scene, t, 5)
    lone_tag = txt("lone pairs?", cfg.FONT["label"], cfg.PURPLE).move_to([3.55, 3.3, 0])
    hud(scene, lone_tag)
    scene.play(FadeOut(angles), h2o.lobe_amount.animate.set_value(1), run_time=1.4)
    scene.play(FadeIn(lone_tag), run_time=0.7)
    scene.play(Indicate(lone_tag, color=cfg.WHITE, scale_factor=1.0), run_time=1.6)

    beat(scene, t, 6)
    card = title_card("MOLECULAR GEOMETRY", "NEXT:", small_first=True)
    card.scale(0.84).move_to([0, -1.55, 0])
    tagline = txt("Explained Visually", cfg.FONT["body"], cfg.CYAN).next_to(card, DOWN, buff=0.25)
    hero_names = VGroup(eq(r"\mathrm{CO_2}", cfg.FONT["body"], cfg.WHITE).move_to([-3.65, 0.3, 0]),
                        eq(r"\mathrm{H_2O}", cfg.FONT["body"], cfg.WHITE).move_to([3.65, 0.3, 0]))
    hud(scene, card, tagline, hero_names)
    # Keep the models fully visible, turning in their own space above the card.
    scene.play(FadeOut(VGroup(co2_tag, h2o_tag, lone_tag)),
               co2.anchor.animate.move_to([-3.65, 1.85, 0]),
               h2o.anchor.animate.move_to([3.65, 2.35, 0]), run_time=1.4)
    scene.play(FadeIn(card, shift=DOWN * 0.15), FadeIn(hero_names), run_time=1.2)
    scene.play(FadeIn(tagline, shift=UP * 0.1), run_time=0.8)
    scene.play(Indicate(card.title[1], color=cfg.WHITE, scale_factor=1.02), run_time=1.4)
    scene.play(card.animate.scale(1.02), tagline.animate.scale(1.02), run_time=3.6, rate_func=smooth)
    scene.play(Indicate(tagline, color=cfg.WHITE, scale_factor=1.0), run_time=1.0)
    end_scene(scene, t, cfg.SCENE_DURATIONS["17"])
