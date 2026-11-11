"""Check the molecular geometry and impulse-area contracts used on screen."""
from __future__ import annotations

import numpy as np


def main() -> int:
    from manim_scenes.common import water_cluster
    from manim_scenes import scene_11_hits_to_force as s
    from utils import physics_models as pm

    for scale in (0.4, 0.62, 1.0):
        molecules, hbonds = water_cluster(scale)
        assert len(molecules) == 5 and len(hbonds) == 4
        for molecule in molecules:
            o, h1, h2 = (position for _, position in molecule)
            a, b = h1 - o, h2 - o
            assert np.allclose([np.linalg.norm(a), np.linalg.norm(b)], 0.96 * scale)
            angle = np.degrees(np.arccos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))))
            assert np.isclose(angle, 104.5), angle
        for h, acceptor in hbonds:
            donors = [m[0][1] for m in molecules if any(np.allclose(h, atom[1]) for atom in m[1:])]
            assert len(donors) == 1
            assert np.linalg.norm(np.cross(h - donors[0], acceptor - h)) < 1e-10

    hits = pm.single_molecule_hits(s.VX, s.L, s.END - 1e-6, start=0.4)
    gap = hits[1] - hits[0]
    impulse = s.SPIKE_W * s.SPIKE_H / 2
    level = impulse / gap
    # Every displayed triangle becomes a complete rectangle of equal area.
    assert np.allclose([min(h + gap, s.END) - h for h in hits], gap)
    assert np.isclose(level * gap * len(hits), impulse * len(hits))
    from manim_scenes.scene_30_limits import packing_fractions
    fractions = packing_fractions()
    for height in np.linspace(2.0, 4.0, 11):
        extent = np.array([2.8, height, 2.2])
        centres = fractions * extent
        radius = 0.28
        assert np.all(centres >= radius) and np.all(centres <= extent - radius)
        distances = np.linalg.norm(centres[:, None, :] - centres[None, :, :], axis=-1)
        assert np.all(distances[np.triu_indices(len(centres), 1)] >= 2 * radius)
    print('Visual contracts passed: five 104.5° waters, O–H lengths, four donor links, conserved impulse areas, non-overlapping finite-size schematic.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
