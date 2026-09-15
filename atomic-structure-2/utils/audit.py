"""Check scientific invariants, narration windows, animation budgets and layout.

The endpoint renderer runs the real animations and then jumps each one to its
final state, so a whole chapter is exercised without rasterizing every frame.
That catches the two failures that actually happen in a film this long: a
chapter that silently overruns its narration window, and a label that ends up
off the frame or on top of another label.

    python utils/audit.py                 # every chapter, standalone
    python utils/audit.py 09 10           # just these chapters
    python utils/audit.py --full          # the continuous film
    python utils/audit.py --storyboard    # also write rendered endpoint frames
    python utils/audit.py --science-only  # numbers and narration only, no render
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from manim import FadeOut, MathTex, Text, ThreeDCamera, config
from manim.renderer.cairo_renderer import CairoRenderer
from PIL import Image, ImageDraw
from scipy.constants import electron_mass
from scipy.integrate import quad

import config as cfg
from main import SCENE_MAP
from utils.narration_export import WORD, export, sections
from utils.physics_models import (
    madelung_order,
    most_probable_radius,
    occupancy,
    orbital_mesh,
    psi,
    radial,
    radial_distribution,
    sample_positions,
    sigma_p,
)

# The frame's outer limits for authored text, a little wider than the safe
# frame so a deliberate bleed is allowed but a genuine overflow is not.
TEXT_LIMIT_X = 7.75
TEXT_LIMIT_Y = 4.20
STORYBOARD_INTERVAL = 8.0


def _label_of(mob) -> str:
    return getattr(mob, "text", getattr(mob, "tex_string", "?"))


class EndpointRenderer(CairoRenderer):
    """Run every animation, but only ever look at where it ends up."""

    def __init__(self, storyboard: bool = False) -> None:
        super().__init__(camera_class=ThreeDCamera)
        self.check_lifetimes = True
        self.storyboard = storyboard
        self.frames: list[tuple[Image.Image, float, str]] = []
        self.issues: list[str] = []
        self.last_capture = -10.0

    def play(self, scene, *args, **kwargs) -> None:
        scene.compile_animation_data(*args, **kwargs)
        scene.begin_animations()
        duration = scene.get_run_time(scene.animations)
        self.time += len(np.arange(0, duration, 1 / self.camera.frame_rate)) / self.camera.frame_rate
        for animation in scene.animations:
            animation.update_mobjects(duration)
            animation.interpolate(1)
            animation.finish()
            animation.clean_up_from_scene(scene)
        scene.update_mobjects(duration)
        self.static_image = None
        self.num_plays += 1

        self._check_layout(scene)
        self._maybe_capture(scene)

    def _check_layout(self, scene) -> None:
        """Flag authored text that leaves the frame or lands on other text."""
        family = [part for top in scene.mobjects for part in top.get_family()]
        candidates = list(dict.fromkeys(m for m in family if isinstance(m, (Text, MathTex))))
        visible = []
        for mob in candidates:
            # A MathTex holds no points itself and reports zero fill opacity, so
            # asking the container directly silently excuses every equation in
            # the film from this check. Ask the glyphs instead.
            glyphs = mob.family_members_with_points()
            if not glyphs or max(part.get_fill_opacity() for part in glyphs) < 0.1:
                continue
            # A drop shadow is supposed to sit under its own glyphs.
            if getattr(mob, "_is_decorative", False):
                continue
            fixed = mob in scene.camera.fixed_in_frame_mobjects
            flat = abs(scene.camera.get_phi()) < 0.01
            # 3D labels are authored in screen space; geometry labels are only
            # meaningful to check while the camera is head-on.
            if not (fixed or flat):
                continue
            low = mob.get_corner(np.array([-1, -1, 0]))
            high = mob.get_corner(np.array([1, 1, 0]))
            if low[0] < -TEXT_LIMIT_X or high[0] > TEXT_LIMIT_X or low[1] < -TEXT_LIMIT_Y or high[1] > TEXT_LIMIT_Y:
                self.issues.append(f"{scene.key}: text bounds at {self.time:.1f}s: {_label_of(mob)}")
            visible.append((mob, low, high))

        for index, (first, first_low, first_high) in enumerate(visible):
            for second, second_low, second_high in visible[index + 1:]:
                if first in second.get_family() or second in first.get_family():
                    continue
                overlap_x = min(first_high[0], second_high[0]) - max(first_low[0], second_low[0])
                overlap_y = min(first_high[1], second_high[1]) - max(first_low[1], second_low[1])
                if overlap_x > 0.08 and overlap_y > 0.08:
                    self.issues.append(
                        f"{scene.key}: text overlap at {self.time:.1f}s: "
                        f"{_label_of(first)} / {_label_of(second)}"
                    )

    def _maybe_capture(self, scene) -> None:
        if not self.storyboard or not scene.anchor.get_family():
            return
        if self.time - self.last_capture < STORYBOARD_INTERVAL / cfg.SPEED:
            return
        if all(isinstance(animation, FadeOut) for animation in scene.animations):
            return
        self.update_frame(scene)
        self.frames.append((Image.fromarray(self.get_frame()).convert("RGB"), self.time, scene.key))
        self.last_capture = self.time


# ---------------------------------------------------------------------------
# Checks that need no renderer
# ---------------------------------------------------------------------------


def science() -> None:
    """Every number the film draws has to survive these."""
    for n, l in ((1, 0), (2, 0), (2, 1), (3, 2), (4, 3)):
        norm = quad(lambda r: float(radial(n, l, r)) ** 2 * r * r, 0, np.inf)[0]
        assert abs(norm - 1) < 1e-7, (n, l, norm)

    # The 2s radial node sits at r = 2 a0, and 2p vanishes in its nodal plane.
    assert abs(radial(2, 0, 2)) < 1e-14
    assert abs(psi(2, 1, 0, np.array([1.0, 0.0, 0.0]))) < 1e-14
    assert np.sign(psi(2, 1, 0, np.array([0.0, 0.0, 1.0]))) != np.sign(psi(2, 1, 0, np.array([0.0, 0.0, -1.0])))

    for width in (0.2, 0.5, 1, 3):
        assert abs(width * sigma_p(width) - 0.5) < 1e-12

    for z in range(19):
        slots = [slot for _, states in occupancy(z) for slot in states]
        assert sum(map(len, slots)) == z
        assert all(len(slot) <= 2 and (len(slot) < 2 or slot == [1, -1]) for slot in slots)
    assert occupancy(6)[2][1] == [[1], [1], []]     # carbon: Hund, not paired
    assert occupancy(8)[2][1] == [[1, -1], [1], [1]]  # oxygen: pairing begins
    assert occupancy(10)[2][1] == [[1, -1]] * 3       # neon: the set is closed

    radii = np.linalg.norm(sample_positions(count=30000), axis=1)
    assert abs(radii.mean() - 1.5) < 0.025, radii.mean()

    for n, l, m in ((1, 0, 0), (2, 1, 0), (3, 2, -2)):
        *_, fraction = orbital_mesh(n, l, m, resolution=33)
        assert 0.89 <= fraction <= 0.93, (n, l, m, fraction)

    from utils.quantum_examples import electron_wavelength, minimum_momentum_spread, hydrogen_energy

    assert np.isclose(electron_wavelength(1e6) * 1e9, 0.7273895, rtol=1e-6)
    assert np.isclose(electron_wavelength(2e6) / electron_wavelength(1e6), 0.5, rtol=1e-12)
    assert np.isclose(minimum_momentum_spread(100e-12) / 1e-25, 5.272859, rtol=1e-6)
    assert np.isclose(minimum_momentum_spread(50e-12) / minimum_momentum_spread(100e-12), 2)
    assert np.isclose(hydrogen_energy(1), -13.605693, rtol=1e-6)
    assert np.isclose(hydrogen_energy(2), hydrogen_energy(1) / 4)

    # An independent finite-difference Hamiltonian check links the displayed
    # energies to the actual wave functions, away from the Coulomb singularity.
    step = 1e-3
    point = np.array([0.7, 0.5, 1.1])
    for n, l, m in ((1, 0, 0), (2, 1, 0)):
        value = psi(n, l, m, point)
        laplacian = sum((psi(n, l, m, point + axis * step) - 2 * value
                         + psi(n, l, m, point - axis * step)) / step**2
                        for axis in np.eye(3))
        applied = -0.5 * laplacian - value / np.linalg.norm(point)
        assert np.isclose(applied, -value / (2 * n**2), rtol=2e-5, atol=1e-8)

    # Integrate the actual hydrogen wave function independently of the CDF.
    from utils.quantum_examples import (
        hydrogen_1s_cumulative, hydrogen_1s_probability_radius, two_slit_probability,
    )
    for radius in (0.0, 0.2, 1.0, 2.66, 8.0):
        integrated = quad(lambda r: float(radial_distribution(1, 0, r)), 0, radius)[0]
        assert np.isclose(hydrogen_1s_cumulative(radius), integrated, atol=1e-11)
    assert np.isclose(hydrogen_1s_cumulative(1), 0.323323584, atol=1e-9)
    r90 = hydrogen_1s_probability_radius()
    assert np.isclose(r90, 2.661160169, atol=1e-8)
    assert np.isclose(quad(lambda r: float(radial_distribution(1, 0, r)), 0, r90)[0], 0.9)
    # Reconstruct complex amplitudes rather than repeat the intensity formula.
    y = np.linspace(-4, 4, 201)
    envelope = np.exp(-y**2 / (2 * 1.75**2))
    a1 = np.sqrt(envelope / 2) * np.exp(1j * 3.2 * y)
    a2 = np.sqrt(envelope / 2) * np.exp(-1j * 3.2 * y)
    assert np.allclose(two_slit_probability(y), np.abs(a1 + a2)**2)
    assert np.allclose(two_slit_probability(y, 0), np.abs(a1)**2 + np.abs(a2)**2)
    dark = np.pi / (2 * 3.2)
    assert abs(two_slit_probability(dark)) < 1e-12 < two_slit_probability(dark, 0)
    for coherence in (0, 0.3, 1):
        assert np.all(two_slit_probability(y, coherence) >= 0)
    print("Science: spherical probability and coherent/incoherent slit amplitudes pass")

    # -- Chapter 3's banked numbers, and the chapters that spend them --------
    from utils.quantum_examples import (
        bohr_momentum,
        bohr_radius,
        bohr_speed,
        de_broglie_wavelength,
    )

    assert np.isclose(bohr_radius(1) * 1e10, 0.529177, rtol=1e-5)
    assert np.isclose(bohr_radius(2) * 1e10, 2.116709, rtol=1e-5)   # chapter 3 says 2.12
    assert np.isclose(bohr_speed(1) / 1e6, 2.187691, rtol=1e-5)     # chapter 3 says 2.19
    assert np.isclose(bohr_momentum(1) / 1e-24, 1.992852, rtol=1e-5)
    assert np.isclose(bohr_radius(3) / bohr_radius(1), 9.0)

    # Chapter 6 stands on this and nothing else: the de Broglie wavelength of
    # the first-shell electron IS the circumference of the first orbit, so
    # 2 pi r = n lambda is Bohr's postulate rather than a coincidence.
    circumference = 2 * np.pi * bohr_radius(1)
    matter_wave = de_broglie_wavelength(electron_mass, bohr_speed(1))
    assert np.isclose(matter_wave, circumference, rtol=1e-9), (matter_wave, circumference)
    assert np.isclose(matter_wave * 1e10, 3.324918, rtol=1e-6)      # chapter 4 says 3.3

    # Chapter 4's macroscopic example, and the gap the log ruler draws.
    ball = de_broglie_wavelength(0.160, 40.0)
    assert np.isclose(ball * 1e34, 1.035324, rtol=1e-5)
    assert 1e19 > 1e-15 / ball > 1e18                                # "nineteen powers of ten"

    # -- Chapter 11: the radial distribution, which is not the density -------
    for n, l in ((1, 0), (2, 0), (2, 1), (3, 2)):
        area = quad(lambda r: float(radial_distribution(n, l, r)), 0, 80)[0]
        assert abs(area - 1) < 1e-7, (n, l, area)
    # |psi_1s|^2 is largest at the nucleus; the radial distribution vanishes
    # there. The film shows both and says they answer different questions.
    assert radial_distribution(1, 0, 0.0) == 0.0
    assert psi(1, 0, 0, np.array([1e-9, 0.0, 0.0])) ** 2 > psi(1, 0, 0, np.array([1.0, 0.0, 0.0])) ** 2
    assert abs(most_probable_radius(1, 0) - 1.0) < 1e-3             # exactly a0
    # For the largest l in each shell the peak lands on Bohr's own n^2 a0.
    for n in (2, 3):
        assert abs(most_probable_radius(n, n - 1) - n * n) < 1e-3, n

    # -- Chapters 13 and 17: penetration, and the order it produces ----------
    # 3s has substantially more core probability than 3d. This is what the three
    # curves in chapter 13 are there to show.
    core = 1.5
    reach = {l: quad(lambda r: float(radial_distribution(3, l, r)), 0, core)[0] for l in (0, 1, 2)}
    assert reach[0] > reach[1] > reach[2], reach
    assert reach[2] < 1e-3 < reach[0]

    # The sharper statement, and the one chapter 13 actually draws: where each
    # curve's innermost lobe sits. 3s has one inside the core at 0.74 a0, 3p's
    # first is at 3 a0, and 3d's only lobe is out at 9 a0.
    grid = np.linspace(1e-6, 24.0, 24000)
    innermost = {}
    for l in (0, 1, 2):
        y = radial_distribution(3, l, grid)
        peaks = np.flatnonzero((y[1:-1] > y[:-2]) & (y[1:-1] > y[2:])) + 1
        innermost[l] = float(grid[peaks[0]])
    assert innermost[0] < core < innermost[1] < innermost[2], innermost
    assert abs(innermost[0] - 0.74) < 0.02, innermost[0]
    assert abs(innermost[1] - 3.00) < 0.02, innermost[1]
    assert abs(innermost[2] - 9.00) < 0.02, innermost[2]

    order = [label for label, *_ in madelung_order(10)]
    assert order == ["1s", "2s", "2p", "3s", "3p", "4s", "3d", "4p", "5s", "4d"], order
    totals = {label: total for label, _, _, total in madelung_order(10)}
    assert totals["4s"] == 4 < totals["3d"] == 5          # chapter 17's whole argument
    assert totals["2p"] == totals["3s"] == 3              # the tie, broken by smaller n
    assert order.index("2p") < order.index("3s")

    # -- Chapter 12: the counting that recovers Bohr's 2, 8, 18 --------------
    for n in (1, 2, 3, 4):
        assert sum(2 * l + 1 for l in range(n)) == n * n
        assert 2 * n * n in (2, 8, 18, 32)

    # The new crystal view must interfere coherently. A periodic row has
    # an exact first cancellation between its principal maxima; checking only
    # a plausible-looking histogram would miss a broken phase calculation.
    from manim_scenes.matter_wave_visuals import CrystalDiffraction
    diffraction = CrystalDiffraction()
    assert np.isclose(diffraction.intensity(0.0), 1.0)
    assert np.allclose(diffraction.profile, diffraction.profile[::-1], atol=1e-12)
    first_null = np.arcsin(diffraction.wavelength / (7 * diffraction.spacing))
    first_order = np.arcsin(diffraction.wavelength / diffraction.spacing)
    assert abs(diffraction.amplitude(first_null)) ** 2 < 1e-20
    assert abs(diffraction.amplitude(first_order)) ** 2 > 0.1
    assert len(diffraction.maxima) == 3
    print("Science: coherent crystal maxima, cancellation and symmetry pass")

    print("Science: Bohr's banked numbers, the 2-pi-r identity and Madelung order pass")
    print("Science: worked SI examples and hydrogen Hamiltonian pass")
    print("Science: radial normalization, nodes, Gaussian uncertainty, sampling, surfaces and occupancy pass")


def narration() -> None:
    """The script's windows, the config's durations and the exports must agree."""
    items = sections()
    assert [item["key"] for item in items] == list(SCENE_MAP)
    elapsed = 0
    words = 0
    for item in items:
        assert item["start"] == elapsed and item["end"] - item["start"] == cfg.DURATIONS[item["key"]], item["key"]
        elapsed = item["end"]
        count = len(WORD.findall(item["text"]))
        words += count
        rate = count * 60 / cfg.DURATIONS[item["key"]]
        # Allow a natural 150-wpm upper limit, including the revised opening.
        assert 80 <= rate <= 150, (item["key"], rate)
    export(check=True)
    print(f"Narration: {words} words; {elapsed // 60}:{elapsed % 60:02d}; all scene rates pass")


# ---------------------------------------------------------------------------
# Storyboard contact sheets
# ---------------------------------------------------------------------------


def write_storyboard(folder: Path, frames: list[tuple[Image.Image, float, str]]) -> None:
    columns, tile_width, tile_height = 3, 427, 264
    for index, (frame, moment, key) in enumerate(frames):
        frame.save(folder / f"scene_{key}_{index:03d}.png")
    for page, start in enumerate(range(0, len(frames), 18)):
        chunk = frames[start:start + 18]
        rows = (len(chunk) + columns - 1) // columns
        board = Image.new("RGB", (tile_width * columns, tile_height * rows), cfg.BG)
        for index, (frame, moment, key) in enumerate(chunk):
            tile = Image.new("RGB", (tile_width, tile_height), cfg.BG)
            tile.paste(frame.resize((tile_width, tile_height - 24)), (0, 24))
            ImageDraw.Draw(tile).text((8, 6), f"{key} / {moment:.1f}s", fill="white")
            board.paste(tile, ((index % columns) * tile_width, (index // columns) * tile_height))
        board.save(folder / f"board_{page + 1}.jpg", quality=93)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenes", nargs="*", help="chapter keys, for example 09 10")
    parser.add_argument("--storyboard", action="store_true", help="also write rendered endpoint frames")
    parser.add_argument("--full", action="store_true", help="audit the continuous film instead")
    parser.add_argument("--fps", type=int, default=15)
    parser.add_argument("--science-only", action="store_true")
    parser.add_argument("--output", default="output/review")
    args = parser.parse_args()

    config.pixel_width, config.pixel_height = 854, 480
    config.frame_rate = args.fps
    config.progress_bar = "none"

    science()
    narration()
    if args.science_only:
        return

    issues: list[str] = []
    records: list[dict] = []
    frames: list[tuple[Image.Image, float, str]] = []

    if args.full:
        from manim_scenes.full_video import FullVideo

        renderer = EndpointRenderer(args.storyboard)
        film = FullVideo(renderer=renderer)
        film.construct()
        drift = abs(film.time - cfg.total_seconds() / cfg.SPEED)
        assert drift <= 2 * len(cfg.SCENES) / config.frame_rate, drift
        issues += renderer.issues
        frames += renderer.frames
        records.append(dict(scene="full", seconds=film.time))
    else:
        for key in args.scenes or SCENE_MAP:
            key = key.zfill(2)
            module, class_name, _ = SCENE_MAP[key]
            renderer = EndpointRenderer(args.storyboard)
            chapter = getattr(importlib.import_module(module), class_name)(renderer=renderer)
            chapter.construct()
            target = cfg.DURATIONS[key] / cfg.SPEED
            assert abs(chapter.time - target) <= 2 / config.frame_rate, (key, chapter.time, target)
            issues += renderer.issues
            frames += renderer.frames
            records.append(dict(scene=key, seconds=chapter.time))
            print(f"{key}: {chapter.time:.2f}s / {target:.2f}s, {len(renderer.issues)} layout flags", flush=True)

    folder = PROJECT_ROOT / args.output
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "audit.json").write_text(json.dumps(dict(scenes=records, issues=sorted(set(issues))), indent=2))
    if frames:
        write_storyboard(folder, frames)
    if issues:
        raise AssertionError("\n".join(sorted(set(issues))))
    print("Animation windows and endpoint text checks pass")


if __name__ == "__main__":
    main()
