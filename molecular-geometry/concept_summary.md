# Concept summary — Molecular Geometry, Explained Visually

*Chemical Bonding · Part 2.* Follows *Chemical Bonding, Explained Visually*
(why atoms bond) and leads into *Molecular Orbital Theory, Explained Visually*.

## The question

Carbon dioxide and water both have three atoms. CO₂ is straight (180°); H₂O is
bent (about 104.5°). Why — and can we predict a molecule's shape just from its
electrons?

## The idea in one paragraph

A molecule's shape is set by where its nuclei and electrons settle together.
Two complementary models make that predictable. **VSEPR** counts the
*electron regions* around a central atom (each bond — single, double or triple
— counts once; each lone pair counts once) and arranges them as far apart as
possible: 2 → linear, 3 → trigonal planar, 4 → tetrahedral, 5 → trigonal
bipyramidal, 6 → octahedral. That is the **electron geometry**. Hide the lone
pairs and what remains — the atoms — is the **molecular geometry**: bent,
pyramidal, seesaw, T-shaped, square planar and so on. **Hybridization**
(valence bond theory) then *describes* the same directions with orbitals:
mixing one s with n p orbitals gives equivalent hybrids with equal s character, whose orthogonality
forces cos θ = −1/n (180°, 120°, 109.47°), with any unused p orbitals left for
π bonds. Shape then decides **polarity**: bond dipoles are vectors, and a
symmetric arrangement of identical bonds cancels (CO₂, BF₃, CH₄) while a
lopsided one does not (NH₃, H₂O).

## Intuition → formal idea, in the film's order

| Step | Intuition (picture) | Formal idea |
|---|---|---|
| Lewis structures | letters, lines, dots on flat paper | connectivity and electron-pair bookkeeping, not 3D shape |
| Regions repel | lobes pushed apart on a sphere | minimum of Σ 1/dᵢⱼ for n unit vectors (a model of the VSEPR idea) |
| Counting | one lobe per bond or lone pair | AXₘEₙ; steric number m + n |
| Tetrahedral angle | H on alternate corners of a cube | (1,1,1)·(1,−1,−1) = −1, \|a\|\|b\| = 3 → θ = cos⁻¹(−1/3) ≈ 109.47° |
| Lone pairs | purple lobe present but hidden in the shape | electron geometry vs molecular geometry |
| Five regions | axial vs equatorial | fewest 90° lone-pair contacts → lone pairs go equatorial |
| Six regions | two lone pairs as far apart as possible | trans placement → square planar XeF₄ |
| Hybrids | a dial from s to p | ψ = cos α ψₛ + sin α ψₚ; sp, sp², sp³ at tan²α = 1, 2, 3 |
| Hybrid angles | not put in by hand | ⟨hᵢ\|hⱼ⟩ = (1 + n cos θ)/(1 + n) = 0 → cos θ = −1/n |
| Polarity | arrows chained tip to tail | vector sum of bond dipoles; zero for symmetric identical bonds |

## Models and where they stop being literal

These caveats are stated in the narration or on screen where they matter.

* **Electron regions as lobes.** The cyan (bond) and purple (lone pair) lobes
  are schematic: they show *directions* and *space*, not computed electron
  densities. Lone-pair lobes are drawn fatter and shorter, following the
  VSEPR heuristic that a lone pair, held by one nucleus, spreads out closer to
  the central atom.
* **The repulsion relaxation** (chapters 03, 09, 11) is a literal computation
  — n points on a sphere under a 1/d repulsion, following the gradient flow —
  but it is a *model of the VSEPR idea*, not a quantum calculation. The
  narration says so ("a simple computer model does the pushing").
* **Measured angles are measured.** VSEPR predicts the arrangement and the
  decreasing-angle trend within the CH₄ / NH₃ / H₂O comparison, never the exact numbers. Every
  angle on screen (NH₃ 106.7°, H₂O 104.5°, SO₂ 119.3°, PF₃ 97.8°, SF₄ 173.1° /
  101.6°, ClF₃ 87.5°, BrF₃ 86.2°, BrF₅ 84.8°, C₂H₄ H–C–H 117.4°) comes from
  experimental gas-phase structures. The film explicitly rejects any
  "109.5° − k × lone pairs" formula.
* **Bond lengths in the family chapters are uniform** so only the angles
  change during a morph (PCl₅ → SF₄ → ClF₃ → XeF₂, SF₆ → BrF₅ → XeF₄).
  PCl₅ in chapter 09 is drawn with its measured axial (214 pm) and equatorial
  (202 pm) lengths, because that difference is the point being made. PCl₅ is
  described in the gas phase (the solid is ionic, [PCl₄]⁺[PCl₆]⁻).
* **Water's lone-pair lobes** open by as much as the bonds close; lone-pair
  directions are not measurable, so this is a drawing convention.
* **Hybrid orbital shapes** are the textbook polar plot of the angular
  density, r(θ) = A(θ)², with A = cos α + √3 sin α cos θ, every mixture
  normalised the same way (A² averages to 1). |ψ| isosurfaces with a shared
  Slater radial factor were computed too (`utils/orbital_models.py`); they are
  much fatter (an sp³ lobe is wider than long) and hard to read, so they serve
  as a cross-check: both agree on direction, phase and the growth of the back
  lobe from sp to sp³. Colours show the sign of ψ (blue +, rose −); unused p
  orbitals are purple.
* **Hybridization is a description, not a cause.** The film says it is a
  mathematical re-description of the same electrons, not orbitals "melting",
  that it does not by itself prove a shape, that perfect sp³ hybrids would
  give 109.5° rather than the measured NH₃/H₂O angles, and that water's real
  orbitals are more nuanced than four identical hybrids.
* **sp³d and sp³d²** are presented only as historical textbook labels; modern
  calculations give d orbitals a minor role in main-group "hypervalent"
  bonding.
* **Bond-dipole arrows** point toward the more electronegative atom (the common
  chemistry convention; the physics dipole-moment vector points the other
  way, from − to +). Arrow lengths are proportional to the Pauling
  electronegativity difference — an illustration of direction and symmetry,
  not a dipole-moment calculation. Methane's weak C–H arrows are drawn larger
  than to scale so the closing 3D chain can be seen. The film notes that shape
  is not the only factor in polarity.
* **The "umbrella"** is a metaphor for the regions folding into a
  tetrahedron, and the oxygen-magnet teaser is a qualitative picture of
  paramagnetism (explained by unpaired electrons in molecular orbitals in the
  next film).

## Sources

* Gas-phase bond angles and lengths: NIST Computational Chemistry Comparison
  and Benchmark Database (CCCBDB), experimental geometries; CRC Handbook of
  Chemistry and Physics, "Structure of Free Molecules in the Gas Phase".
* Pauling electronegativities and gas-phase dipole moments: CRC Handbook of
  Chemistry and Physics (dipole moments after Nelson, Lide & Maryott,
  NSRDS-NBS 10).
* VSEPR: R. J. Gillespie & R. S. Nyholm, *Q. Rev. Chem. Soc.* 11, 339 (1957);
  R. J. Gillespie & I. Hargittai, *The VSEPR Model of Molecular Geometry*
  (1991).
* Hybrid orthogonality and cos θ = −1/n: standard valence-bond treatment, e.g.
  P. Atkins & J. de Paula, *Physical Chemistry*, valence-bond theory chapter.
* d orbitals in hypervalent molecules: E. Magnusson, *J. Am. Chem. Soc.* 112,
  7940 (1990); A. E. Reed & P. v. R. Schleyer, *J. Am. Chem. Soc.* 112, 1434
  (1990).
* Thomson problem (points on a sphere under 1/d repulsion; trigonal bipyramid
  for 5, octahedron for 6): J. J. Thomson, *Phil. Mag.* 7, 237 (1904), and the
  standard numerical tables since.

Every number in `narration.py` is cross-checked against these data by
`python -m utils.geometry_data` (25 spoken claims), and every molecule's
lone-pair count, AXmEn code and shape name is derived and checked by
`python -m utils.molecule_library`.

Review references:
[OpenStax: molecular structure and polarity](https://openstax.org/books/chemistry-2e/pages/7-6-molecular-structure-and-polarity)
supports the distinction between electron geometry and molecular shape and the
need to consider both bonding and structure when assessing polarity.
[ElevenLabs delivery guidance](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
explains model-dependent tags and pacing; cue-aligned audio placement supplies
timing independently of those delivery suggestions.
