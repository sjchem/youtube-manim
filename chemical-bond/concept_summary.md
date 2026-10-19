# Concept summary — Chemical Bonding, Explained Visually

*Chemical Bonding · Part 1. Follows "Periodic Trends, Explained Visually" (Atomic Structure · Part 4).*

## The question

Why do atoms form chemical bonds at all — and what decides whether they
**share**, **transfer**, or **delocalise** electrons?

## The core idea

A chemical bond forms when the interactions among nuclei and electrons give an
arrangement with **lower total energy than the separated atoms**:

$$E_{\text{together}} < E_{\text{apart}}$$

The ingredients are attraction (each electron to every nucleus), repulsion
(nucleus–nucleus, electron–electron) and quantum mechanics (confining an
electron raises its kinetic energy; two electrons occupying the same spatial orbital
must have opposite spins). The film never treats the octet rule as the cause of
bonding; it appears as a useful bookkeeping pattern and is shown failing in
chapter 15.

## The story, in order

| Idea | What the film shows | Key numbers (sources below) |
|---|---|---|
| Why two H atoms stop at one distance | Six pairwise forces, then one total energy E(r) with a valley | H–H bond length 74 pm |
| The energy landscape | A tracker drives atoms, cloud and a dot on E(r); swept round, the curve becomes a circular moat (3D) | — |
| Stable bond | A schematic well illustrates gas-phase bond enthalpy; breaking costs, forming releases energy | H–H 436 kJ/mol |
| Reaction energy | H₂ + Cl₂ → 2 HCl as broken vs formed | 436 + 243 − 2 × 432 = −185 kJ/mol (measured −184.6) |
| Valence electrons, Lewis dots | Counts H 1, C 4, O 6, Cl 7; octet as a pattern | — |
| Covalent bonding | Shared cloud for H₂; Lewis Cl₂ (lone pairs), O₂ (double), N₂ (triple); bond order | — |
| Valence bond theory (3D) | 1s + 1s and head-on p + p overlap → σ (axially symmetric); side-by-side p + p → π with a nodal plane; O₂ = σ + π, N₂ = σ + 2π | head-on overlap > sideways overlap at a realistic bond distance (computed) |
| Ionic bonding | Gas-phase transfer is **uphill**; the crystal pays | Na IE 496, Cl EA 349 → +147; lattice 787; from gas atoms −640 kJ/mol |
| The lattice | Rock salt: 6 opposite, 12 like, 8 opposite neighbours …; Madelung sum ≈ 1.75 × one pair | Madelung 1.7476 (computed); MgO lattice ≈ 4.8 × NaCl |
| Polarity | One shared cloud leans as ΔEN grows; δ+/δ−; a continuum, not two boxes | EN: H 2.20, Cl 3.16, Na 0.93 |
| Metallic bonding | Positive cores in an electron sea; current; layers slide (metal bends, salt shatters) | Cu (fcc) has 12 nearest neighbours (computed) |
| Length and strength | Valley position = length; schematic depth = enthalpy scale; vibration; C–C/C=C/C≡C; F₂ vs Cl₂ | C–C 154 pm/348, C=C 134/614, C≡C 120/839; F–F 141 pm/159, Cl–Cl 199 pm/243 |
| Octet limits | H duet; BF₃ six around boron; SF₆ twelve in the Lewis count; O₂'s magnetism | — |
| Synthesis | Three panels → three valleys → one principle; bond-type map from electronegativities | — |
| Teaser | CO₂ straight (180°), H₂O bent (104.5°) | — |

## Models, and where they stop being literal

- **The energy curve** is an empirical Morse illustration. Its horizontal
  scale uses H₂'s approximately 74 pm equilibrium separation; its depth is
  deliberately calibrated to the roughly 436 kJ/mol gas-phase dissociation
  enthalpy near 298 K. This is **not** an exact electronic potential: the
  spectroscopic well depth Dₑ is about 458 kJ/mol, while dissociation from
  the lowest vibrational state D₀ is about 432 kJ/mol. Zero-point motion and
  thermal terms distinguish these quantities. The narration and graph caption
  identify the schematic scale. The two Morse terms illustrate competing
  trends, rather than measuring separate classical forces. Stable capture also
  requires the excess energy to leave through radiation or other particles.
- **Electron clouds** are seeded random samples of a hydrogen-like radial
  density. The forming bond cloud (`PairCloud`) and the leaning polar cloud
  (`BondCloud`) are illustrations of sharing, **not computed molecular orbitals**.
- **3D orbital surfaces** (chapters 08–09) are isosurfaces of simple LCAO
  densities built from hydrogen-like s and p functions with overlap
  normalisation. At large separation they approximate separated atomic densities. They are
  visual aids for overlap and symmetry, not a calculated valence-bond wavefunction
  or an exact solution for H₂, Cl₂, O₂, or N₂. Spin arrows are quantum labels.
- **O₂ in valence bond theory** is drawn as σ + π. Chapter 15 says plainly that
  this picture (and its Lewis structure) cannot explain why liquid oxygen is
  attracted to a magnet; that needs molecular orbital theory.
- **The electron sea** is a simplified picture of delocalised electronic states.
  Copper is not explained by a literal sequential donation of one free electron
  per atom. Electron drift and conventional current point in opposite directions.
- **Ion and atom sizes** are shrunk or schematic so arrangements stay visible.
  The mini valleys in chapter 16 are labelled "schematic shapes".
- **Average bond enthalpies** for related carbon bonds support a broad
  length/strength trend. Their differences are not independently measured σ or
  π energies: molecular environments and the entire electronic structure change.
- **Ionic bookkeeping** begins with separated Na(g) and Cl(g). The −640 kJ/mol
  result is not NaCl’s standard formation enthalpy from Na(s) and ½Cl₂(g). The
  Madelung factor describes the electrostatic contribution; a real equilibrium
  lattice also includes short-range repulsion and other contributions.
- **SF₆** is shown as a connectivity/electron-count diagram, not as a planar
  molecule. Its actual geometry is octahedral; the Lewis count does not mean
  twelve localized electrons occupying sulfur’s outer shell.
- **The bond-type map** in chapter 16 is a van Arkel–Ketelaar triangle using
  Pauling electronegativities (x: mean, y: difference); its region boundaries
  are conventions, as chapter 12 says.

## Sources

- Bond lengths of diatomic molecules (rₑ): NIST Computational Chemistry
  Comparison and Benchmark Database (from Huber & Herzberg).
- Bond dissociation enthalpies at 298 K: CRC Handbook of Chemistry and Physics,
  "Bond Dissociation Energies" (Luo).
- Average C–C, C=C, C≡C bond lengths and enthalpies: Brown, LeMay et al.,
  *Chemistry: The Central Science*, Tables 8.4–8.5.
- Ionization energy of Na: NIST Atomic Spectra Database; chlorine electron
  affinity: NIST Chemistry WebBook (1 eV = 96.485 kJ/mol).
- Lattice energies (NaCl, MgO), MgO melting point: CRC Handbook. Tables differ
  by a few kJ/mol by convention, so the narration says "about".
- ΔfH°(HCl, g) = −92.31 kJ/mol: CODATA, for the bond-energy cross-check.
- Pauling electronegativities; H₂O and CO₂ geometries: standard reference values.
- Morse width for H₂ from ωₑ = 4401 cm⁻¹, Dₑ = 4.75 eV.

`python -m utils.bond_data` verifies every pattern the narration states (C–C
series ordering, F₂ shorter yet weaker than Cl₂, the uphill transfer, the
reaction ledger against the measured heat) and checks that each of the 31
spoken numbers and claims matches the data.

## Boundaries with Part 2 (Molecular Geometry)

This film covers why bonds form, bond energy, Lewis structures, σ/π overlap,
ionic/covalent/metallic bonding, bond polarity and bond length/strength. It
deliberately leaves molecular shape, VSEPR, bond angles, hybridisation and
overall molecular polarity to Part 2 — only teasing them (CO₂ vs H₂O, two
polar bonds cancelling, water's lone pairs).

## Direct reference links used in this review

- [NIST: experimental H₂ bond length](https://cccbdb.nist.gov/expgeom2x.asp?casno=1333740).
- [NIST: atomic hydrogen thermochemistry](https://webbook.nist.gov/cgi/cbook.cgi?ID=C12385136&Mask=1): twice the atomic formation enthalpy gives approximately 436 kJ/mol for dissociation of H₂ at 298 K.
- [NIST JANAF: hydrogen reference data](https://janaf.nist.gov/pdf/JANAF-FourthEd-1998-Hydrogen.pdf): distinguishes ground-vibrational-state dissociation from room-temperature enthalpy.
- [IUPAC: chemical bond](https://goldbook.iupac.org/terms/view/CT07009) and [bond energy](https://goldbook.iupac.org/terms/view/B00701).
- [IUPAC: sigma and pi symmetry](https://old.goldbook.iupac.org/pdf/S05434.pdf).
- [OpenStax: valence bond theory](https://openstax.org/books/chemistry-atoms-first-2e/pages/5-1-valence-bond-theory).
- [OpenStax: ionic and covalent bond strengths](https://openstax.org/books/chemistry-atoms-first-2e/pages/9-4-strengths-of-ionic-and-covalent-bonds).
- [OpenStax: metallic and other crystalline solids](https://openstax.org/books/chemistry-2e/pages/10-5-the-solid-state-of-matter).
