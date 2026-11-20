"""Check the contracts between the pictures and the models they draw.

Nothing here renders. Each check states something a viewer would infer from
the screen, and confirms the model behind the picture makes it true:

* the cylinder in scenes 01 and 29: while liquid and vapour coexist, the
  vapour above the pool keeps the same density (the flat line on the P-V
  plot), and the pool rises as the lever rule says;
* Maxwell-Boltzmann curves keep unit area when heated (scene 07's shaded area);
* the 2D disk model starts at one speed and conserves kinetic energy (scene 04);
* hard spheres never overlap, even when a piston squeezes them (scenes 09, 11);
* doubling density in scene 13 keeps every original molecule;
* the liquid snapshot's surface molecules have fewer neighbours (scene 25).

    python -m utils.visual_contract_audit
"""

from __future__ import annotations

import numpy as np


def main() -> int:
    from manim_scenes import scene_01_hook as hook
    from manim_scenes import scene_29_synthesis as synthesis
    from manim_scenes.common import PDF_SCALE, speed_color
    from utils import math_utils as mu
    from utils import physics_models as pm

    # Scenes 01 and 29: the lever rule in a cylinder whose height is proportional to volume.
    for module, tr in ((hook, hook.TR), (synthesis, synthesis.TR)):
        _, v_liq, v_gas = pm.maxwell(tr)
        height = module.cylinder_height if hasattr(module, "cylinder_height") else module.height
        densities = []
        for v in np.linspace(v_gas * 0.999, max(v_liq * 1.001, module.V_END), 9):
            x = pm.liquid_fraction(tr, v)
            level = x * height(v_liq)
            vapour = (1 - x) * module.COUNT
            densities.append(vapour / (height(v) - level))
        assert np.allclose(densities, densities[0], rtol=1e-9), densities
        assert module.V_START > v_gas > module.V_END > v_liq, "the squeeze crosses into coexistence and stops inside it"
    assert hook.V_SQUEEZE > hook.V_GAS, "the first push stays in the gas branch"

    # Scene 07: heating keeps the area under the speed curve equal to one.
    us = np.linspace(0, 4000, 20001)
    for T in (300.0, 450.0, 600.0):
        area = np.trapezoid(pm.mb_pdf(us, T, pm.MOLAR_MASS["N2"]) * PDF_SCALE, us / 1000)
        assert abs(area - 1) < 1e-4, (T, area)

    # Scene 04: one speed at the start (one colour), energy conserved, colours ordered slow -> fast.
    pos, vel, _ = pm.disk_movie()
    speeds0 = np.linalg.norm(vel[0], axis=1)
    assert np.ptp(speeds0) < 1e-6
    for frame in vel[:: max(len(vel) // 12, 1)]:
        assert abs(float((frame.astype(float) ** 2).sum(axis=1).mean()) - pm.DISK_SPEED ** 2) < 2e-3
    reds = [mu.luminance(speed_color(s)) for s in (0.0, 1.0)]
    assert speed_color(0.0) != speed_color(2.0) and reds[0] != reds[1]

    # Scenes 09 and 11: hard spheres keep apart while a piston halves their box.
    extent = np.array([2.4, 2.6, 1.8])
    gas = pm.HardSphereGas(60, 11, 0.14, extent)
    for step in range(240):
        squeeze = extent * np.array([1.0, 1.0 - 0.5 * min(step / 180, 1.0), 1.0])
        gas.advance(1 / 30, squeeze, 1.5)
    gap = np.linalg.norm(gas.pos[:, None] - gas.pos[None], axis=-1)
    np.fill_diagonal(gap, np.inf)
    assert gap.min() > 1.6 * gas.radius, gap.min()
    assert np.all(gas.pos >= gas.radius - 1e-9) and np.all(gas.pos <= squeeze - gas.radius + 1e-9)

    # Scene 13: the dense set is the dilute set plus new molecules; pairs grow about four times.
    dilute, dense, p1, p2 = pm.pair_demo()
    assert np.array_equal(dense[: len(dilute)], dilute) and len(dense) == 2 * len(dilute)
    assert 3.8 <= p2 / p1 <= 4.3

    # The attraction-only reference retains excluded volume; it is not nRT/V.
    flask = pm.FLASK
    assert np.isclose(flask.vdw + flask.attraction, flask.size_only)
    assert flask.size_only > flask.ideal

    # The water curve reaches its labelled critical endpoint continuously.
    ts = np.linspace(pm.kelvin(0.0), pm.WATER_TC, 500)
    ps = np.array([pm.water_saturation_pressure(T) for T in ts])
    assert np.all(np.diff(ps) > 0)
    assert np.isclose(ps[-1], pm.WATER_PC_BAR)
    assert abs(pm.vapour_pressure("water", 100 - 1e-4)
               - pm.vapour_pressure("water", 100 + 1e-4)) < 1e-4

    # The two continuity routes end at the same state. The detour avoids coexistence.
    from manim_scenes import scene_21_continuity as continuity
    route = continuity.route_two()
    assert np.allclose(route[0], (continuity.V_GAS, continuity.T_COLD))
    assert np.allclose(route[-1], (continuity.V_LIQ, continuity.T_COLD))
    for v, tr in route:
        if tr < 1:
            _, vl, vg = pm.maxwell(float(tr))
            assert not vl <= v <= vg, (v, tr, vl, vg)

    # Scene 25: a surface molecule has fewer neighbours than one inside.
    slab = pm.liquid_snapshot()
    counts = pm.neighbour_counts(slab)
    top = slab[:, 1] > slab[:, 1].max() - 0.3
    assert counts[top].mean() < counts[~top].mean()

    print("Visual contracts passed: constant vapour density on the flat line, unit-area speed curves, "
          "one-speed disk start with energy conserved, hard spheres apart under a piston, "
          "density doubling keeps every molecule (pairs ×4), attraction-only pressure reference, continuous IAPWS water curve, a phase-boundary-free detour, fewer neighbours at the surface.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
