"""Every molecule in the film, built from the VSEPR model plus measured data.

A molecule is a central atom and a list of *sites*, one per electron region,
index-aligned with ``physics_models.IDEAL[n]``. A site is either a bonded
atom (kind "X") or a lone pair (kind "E"). Because the sites of PCl5, SF4,
ClF3 and XeF2 line up index for index, a chapter can morph one into the next
by turning single sites from atoms into lone pairs.

How each molecule is built — nothing here is a typed coordinate:

1. the number of lone pairs comes from the central atom's valence electrons
   (``geometry_data.lone_pairs_on``);
2. the ideal directions come from the repulsion model;
3. the lone-pair sites are chosen for continuity between chapters, and are
   *asserted* to be among VSEPR's optimal placements;
4. the bonded directions are then opened or closed, symmetrically, to the
   measured angles in ``geometry_data``. Lone-pair lobes are schematic: their
   directions are not measurable, so they stay ideal (in water they open by as
   much as the bonds close, a drawing convention).

``python -m utils.molecule_library`` builds them all and checks the measured
angles, the derived lone-pair counts and the shape names.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations

import numpy as np

from utils import geometry_data as gd
from utils import math_utils as mu
from utils import physics_models as pm


@dataclass
class Site:
    kind: str                       # "X" (bonded atom) or "E" (lone pair)
    direction: np.ndarray
    symbol: str | None = None
    length_pm: float | None = None
    order: int = 1


@dataclass
class Molecule:
    key: str
    formula: str                    # LaTeX, e.g. r"\mathrm{NH_3}"
    name: str
    central: str
    sites: list[Site]
    extra: dict = field(default_factory=dict)

    @property
    def bonds(self) -> list[Site]:
        return [s for s in self.sites if s.kind == "X"]

    @property
    def lone_pairs(self) -> list[Site]:
        return [s for s in self.sites if s.kind == "E"]

    @property
    def regions(self) -> int:
        return len(self.sites)

    @property
    def axe(self) -> str:
        return pm.axe_label(len(self.bonds), len(self.lone_pairs))

    @property
    def electron_geometry(self) -> str:
        return pm.ELECTRON_GEOMETRY[self.regions]

    @property
    def shape(self) -> str:
        return pm.classify(np.array([s.direction for s in self.bonds]))

    def bond_angle(self, i: int, j: int) -> float:
        return mu.angle_deg(self.bonds[i].direction, self.bonds[j].direction)

    def lone_pair_indices(self) -> frozenset[int]:
        return frozenset(i for i, s in enumerate(self.sites) if s.kind == "E")


def _assemble(key: str, formula: str, name: str, central: str, ligand: str, order: int,
              lone_sites: tuple[int, ...], lengths: dict[int, float] | float) -> Molecule:
    """Ideal sites for a central atom with identical ligands.

    ``lone_sites`` only says *where* the lone pairs go; *how many* there are
    is derived from the valence electrons, and the two must agree.
    """
    bonds = _LIGAND_COUNT[key]
    lone = gd.lone_pairs_on(central, [order] * bonds)
    if lone != len(lone_sites):
        raise ValueError(f"{key}: valence electrons give {lone} lone pairs, layout has {len(lone_sites)}")
    regions = bonds + lone
    optimal = pm.best_lone_pair_sites(regions, lone)
    if frozenset(lone_sites) not in optimal:
        raise ValueError(f"{key}: lone pairs at {lone_sites} are not a VSEPR-optimal placement")
    sites = []
    for index, direction in enumerate(pm.ideal_directions(regions)):
        if index in lone_sites:
            sites.append(Site("E", direction))
        else:
            length = lengths[index] if isinstance(lengths, dict) else lengths
            sites.append(Site("X", direction, ligand, float(length), order))
    return Molecule(key, formula, name, central, sites)


_LIGAND_COUNT = {"CO2": 2, "BF3": 3, "SO2": 2, "CH4": 4, "NH3": 3, "H2O": 2, "PF3": 3, "PCl5": 5,
                 "SF4": 4, "ClF3": 3, "BrF3": 3, "XeF2": 2, "SF6": 6, "BrF5": 5, "XeF4": 4}


def _set_bond_pair(mol: Molecule, i: int, j: int, angle: float) -> None:
    a, b = pm.set_pair_angle(mol.sites[i].direction, mol.sites[j].direction, angle)
    mol.sites[i].direction, mol.sites[j].direction = a, b


def carbon_dioxide() -> Molecule:
    return _assemble("CO2", r"\mathrm{CO_2}", "carbon dioxide", "C", "O", 2, (), gd.BOND_LENGTH_PM["C=O in CO2"])


def boron_trifluoride() -> Molecule:
    return _assemble("BF3", r"\mathrm{BF_3}", "boron trifluoride", "B", "F", 1, (), gd.BOND_LENGTH_PM["B-F in BF3"])


def sulfur_dioxide() -> Molecule:
    mol = _assemble("SO2", r"\mathrm{SO_2}", "sulfur dioxide", "S", "O", 2, (0,), gd.BOND_LENGTH_PM["S=O in SO2"])
    _set_bond_pair(mol, 1, 2, gd.BOND_ANGLE_DEG["SO2"])
    return mol


def methane() -> Molecule:
    return _assemble("CH4", r"\mathrm{CH_4}", "methane", "C", "H", 1, (), gd.BOND_LENGTH_PM["C-H in CH4"])


def _pyramid(key: str, formula: str, name: str, central: str, ligand: str, length: float, angle: float) -> Molecule:
    mol = _assemble(key, formula, name, central, ligand, 1, (0,), length)
    bonds = np.array([s.direction for s in mol.sites[1:]])
    for site, direction in zip(mol.sites[1:], pm.set_cone_angle(bonds, -mol.sites[0].direction, angle)):
        site.direction = direction
    return mol


def ammonia() -> Molecule:
    return _pyramid("NH3", r"\mathrm{NH_3}", "ammonia", "N", "H", gd.BOND_LENGTH_PM["N-H in NH3"],
                    gd.BOND_ANGLE_DEG["NH3"])


def phosphorus_trifluoride() -> Molecule:
    return _pyramid("PF3", r"\mathrm{PF_3}", "phosphorus trifluoride", "P", "F", gd.BOND_LENGTH_PM["P-F in PF3"],
                    gd.BOND_ANGLE_DEG["PF3"])


def water() -> Molecule:
    mol = _assemble("H2O", r"\mathrm{H_2O}", "water", "O", "H", 1, (0, 1), gd.BOND_LENGTH_PM["O-H in H2O"])
    _set_bond_pair(mol, 2, 3, gd.BOND_ANGLE_DEG["H2O"])
    # Schematic: the lone-pair lobes open by as much as the bonds close.
    _set_bond_pair(mol, 0, 1, 2 * pm.TETRAHEDRAL_DEG - gd.BOND_ANGLE_DEG["H2O"])
    return mol


def phosphorus_pentachloride() -> Molecule:
    lengths = {i: gd.BOND_LENGTH_PM["P-Cl axial in PCl5" if i in pm.AXIAL else "P-Cl equatorial in PCl5"]
               for i in range(5)}
    return _assemble("PCl5", r"\mathrm{PCl_5}", "phosphorus pentachloride", "P", "Cl", 1, (), lengths)


def _axial_tilt(mol: Molecule, toward, degrees_: float) -> None:
    for i in pm.AXIAL:
        mol.sites[i].direction = pm.tilt(mol.sites[i].direction, toward, degrees_)


def sulfur_tetrafluoride() -> Molecule:
    lengths = {i: gd.BOND_LENGTH_PM["S-F axial in SF4" if i in pm.AXIAL else "S-F equatorial in SF4"] for i in range(5)}
    mol = _assemble("SF4", r"\mathrm{SF_4}", "sulfur tetrafluoride", "S", "F", 1, (3,), lengths)
    lone = mol.sites[3].direction
    _axial_tilt(mol, -lone, (180 - gd.SF4_AXIAL_DEG) / 2)
    _set_bond_pair(mol, 2, 4, gd.SF4_EQUATORIAL_DEG)
    return mol


def _t_shape(key: str, formula: str, name: str, central: str, ax_key: str, eq_key: str, ax_eq: float) -> Molecule:
    lengths = {i: gd.BOND_LENGTH_PM[ax_key if i in pm.AXIAL else eq_key] for i in range(5)}
    mol = _assemble(key, formula, name, central, "F", 1, (3, 4), lengths)
    _axial_tilt(mol, mol.sites[2].direction, 90 - ax_eq)
    return mol


def chlorine_trifluoride() -> Molecule:
    return _t_shape("ClF3", r"\mathrm{ClF_3}", "chlorine trifluoride", "Cl", "Cl-F axial in ClF3",
                    "Cl-F equatorial in ClF3", gd.CLF3_AX_EQ_DEG)


def bromine_trifluoride() -> Molecule:
    return _t_shape("BrF3", r"\mathrm{BrF_3}", "bromine trifluoride", "Br", "Br-F axial in BrF3",
                    "Br-F equatorial in BrF3", gd.BRF3_AX_EQ_DEG)


def xenon_difluoride() -> Molecule:
    return _assemble("XeF2", r"\mathrm{XeF_2}", "xenon difluoride", "Xe", "F", 1, (2, 3, 4),
                     gd.BOND_LENGTH_PM["Xe-F in XeF2"])


def sulfur_hexafluoride() -> Molecule:
    return _assemble("SF6", r"\mathrm{SF_6}", "sulfur hexafluoride", "S", "F", 1, (), gd.BOND_LENGTH_PM["S-F in SF6"])


def bromine_pentafluoride() -> Molecule:
    lengths = {i: gd.BOND_LENGTH_PM["Br-F apical in BrF5" if i == 0 else "Br-F basal in BrF5"] for i in range(6)}
    mol = _assemble("BrF5", r"\mathrm{BrF_5}", "bromine pentafluoride", "Br", "F", 1, (1,), lengths)
    apex = mol.sites[0].direction
    for site in mol.sites[2:]:
        site.direction = pm.tilt(site.direction, apex, 90 - gd.BRF5_APICAL_BASAL_DEG)
    return mol


def xenon_tetrafluoride() -> Molecule:
    return _assemble("XeF4", r"\mathrm{XeF_4}", "xenon tetrafluoride", "Xe", "F", 1, (0, 1),
                     gd.BOND_LENGTH_PM["Xe-F in XeF4"])


BUILDERS = {
    "CO2": carbon_dioxide, "BF3": boron_trifluoride, "SO2": sulfur_dioxide, "CH4": methane,
    "NH3": ammonia, "H2O": water, "PF3": phosphorus_trifluoride, "PCl5": phosphorus_pentachloride,
    "SF4": sulfur_tetrafluoride, "ClF3": chlorine_trifluoride, "BrF3": bromine_trifluoride,
    "XeF2": xenon_difluoride, "SF6": sulfur_hexafluoride, "BrF5": bromine_pentafluoride,
    "XeF4": xenon_tetrafluoride,
}


def molecule(key: str) -> Molecule:
    return BUILDERS[key]()


# ---------------------------------------------------------------------------
# Molecules that are not one-central-atom AXmEn cases
# ---------------------------------------------------------------------------


def ethene() -> dict[str, np.ndarray]:
    """Planar C2H4 in the xy plane, C=C along x, positions in pm."""
    half = gd.BOND_LENGTH_PM["C=C in C2H4"] / 2
    ch = gd.BOND_LENGTH_PM["C-H in C2H4"]
    hcc = np.radians((360 - gd.BOND_ANGLE_DEG["C2H4"]) / 2)
    left, right = np.array([-half, 0.0, 0.0]), np.array([half, 0.0, 0.0])
    hydrogens = []
    for carbon, outward in ((left, -1), (right, 1)):
        for up in (1, -1):
            direction = np.array([-outward * np.cos(hcc), up * np.sin(hcc), 0.0])
            hydrogens.append(carbon + ch * direction)
    return {"C": np.array([left, right]), "H": np.array(hydrogens), "p_axis": np.array([0.0, 0.0, 1.0])}


def diatomic(key: str) -> dict[str, object]:
    """HCl or O2 along the x axis, positions in pm (centre of the bond at the origin)."""
    if key == "HCl":
        length, symbols, order = gd.BOND_LENGTH_PM["H-Cl"], ("H", "Cl"), 1
    elif key == "O2":
        length, symbols, order = gd.BOND_LENGTH_PM["O=O"], ("O", "O"), 2
    else:
        raise KeyError(key)
    return {"symbols": symbols, "positions": np.array([[-length / 2, 0, 0], [length / 2, 0, 0]], dtype=float),
            "order": order}


def verify() -> list[str]:
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    expected = {
        "CO2": ("AX_2", "linear"), "BF3": ("AX_3", "trigonal planar"), "SO2": ("AX_2E", "bent"),
        "CH4": ("AX_4", "tetrahedral"), "NH3": ("AX_3E", "trigonal pyramidal"), "H2O": ("AX_2E_2", "bent"),
        "PF3": ("AX_3E", "trigonal pyramidal"), "PCl5": ("AX_5", "trigonal bipyramidal"),
        "SF4": ("AX_4E", "seesaw"), "ClF3": ("AX_3E_2", "T-shaped"), "BrF3": ("AX_3E_2", "T-shaped"),
        "XeF2": ("AX_2E_3", "linear"), "SF6": ("AX_6", "octahedral"), "BrF5": ("AX_5E", "square pyramidal"),
        "XeF4": ("AX_4E_2", "square planar"),
    }
    for key, (axe, shape) in expected.items():
        mol = molecule(key)
        check(mol.axe == axe, f"{key}: AXmEn {mol.axe} != {axe}")
        check(mol.shape == shape, f"{key}: shape {mol.shape} != {shape}")
        check(all(abs(np.linalg.norm(s.direction) - 1) < 1e-9 for s in mol.sites), f"{key}: unit directions")
    measured = {"SO2": gd.BOND_ANGLE_DEG["SO2"], "NH3": gd.BOND_ANGLE_DEG["NH3"], "H2O": gd.BOND_ANGLE_DEG["H2O"],
                "PF3": gd.BOND_ANGLE_DEG["PF3"], "CO2": 180, "BF3": 120, "XeF2": 180}
    for key, angle in measured.items():
        mol = molecule(key)
        for i, j in combinations(range(len(mol.bonds)), 2):
            check(abs(mol.bond_angle(i, j) - angle) < 0.05, f"{key} bond angle {mol.bond_angle(i, j):.2f} != {angle}")
    check(all(abs(molecule("CH4").bond_angle(i, j) - pm.TETRAHEDRAL_DEG) < 1e-9
              for i, j in combinations(range(4), 2)), "CH4 tetrahedral")
    sf4 = molecule("SF4")
    ax = [s.direction for i, s in enumerate(sf4.sites) if i in pm.AXIAL]
    eq = [sf4.sites[i].direction for i in (2, 4)]
    check(abs(mu.angle_deg(*ax) - gd.SF4_AXIAL_DEG) < 0.05, "SF4 axial angle")
    check(abs(mu.angle_deg(*eq) - gd.SF4_EQUATORIAL_DEG) < 0.05, "SF4 equatorial angle")
    for key, target in (("ClF3", gd.CLF3_AX_EQ_DEG), ("BrF3", gd.BRF3_AX_EQ_DEG)):
        mol = molecule(key)
        for i in pm.AXIAL:
            check(abs(mu.angle_deg(mol.sites[i].direction, mol.sites[2].direction) - target) < 0.05,
                  f"{key} axial-equatorial angle")
    brf5 = molecule("BrF5")
    check(all(abs(mu.angle_deg(brf5.sites[0].direction, brf5.sites[i].direction) - gd.BRF5_APICAL_BASAL_DEG) < 0.05
              for i in range(2, 6)), "BrF5 apical-basal angle")
    # The family morphs: one site at a time turns from atom to lone pair.
    family = [molecule(k).lone_pair_indices() for k in ("PCl5", "SF4", "ClF3", "XeF2")]
    check(all(a < b and len(b - a) == 1 for a, b in zip(family, family[1:])), "TBP family grows one lone pair at a time")
    family = [molecule(k).lone_pair_indices() for k in ("SF6", "BrF5", "XeF4")]
    check(all(a < b and len(b - a) == 1 for a, b in zip(family, family[1:])), "octahedral family grows one at a time")
    family = [molecule(k).lone_pair_indices() for k in ("CH4", "NH3", "H2O")]
    check(all(a < b and len(b - a) == 1 for a, b in zip(family, family[1:])), "tetrahedral family grows one at a time")
    ethene_ = ethene()
    h = ethene_["H"]
    check(abs(mu.angle_deg(h[0] - ethene_["C"][0], h[1] - ethene_["C"][0]) - gd.BOND_ANGLE_DEG["C2H4"]) < 0.05,
          "ethene H-C-H angle")
    check(np.allclose(np.r_[ethene_["C"][:, 2], h[:, 2]], 0), "ethene is planar")
    return failures


if __name__ == "__main__":
    problems = verify()
    if problems:
        print("Molecule library check FAILED:")
        for problem in problems:
            print("  -", problem)
        raise SystemExit(1)
    print(f"Molecule library check passed: {len(BUILDERS)} molecules built from valence counts, optimal")
    print("lone-pair sites and measured angles; every AXmEn code and shape name matches the textbook table.")
