# Science review — The Periodic Table, Explained Visually

The table's block widths reflect the number of allowed electron states. A subshell with angular quantum number l contains 2l + 1 spatial orbitals, with two spin states per orbital. The s, p, d and f capacities are therefore 2, 6, 10 and 14. Atomic number supplies the element sequence; recurring valence configurations help explain the groups and their related chemistry.

The diagram also involves human layout choices. Placing helium with the noble gases and folding the long f regions below the main table makes the chart useful. The film distinguishes these choices from the physical state counts, rather than claiming that every part of the printed outline is uniquely dictated by quantum mechanics.

## Scientific distinctions carried into the narration and visuals

- **Ground states:** the atom's total energy is minimized, including electron interactions. “Put the next electron on a permanently fixed energy shelf” is too strong a model.
- **4s and 3d:** potassium and calcium have occupied 4s before the first d series begins. The diagrams show a schematic filling sequence, not a measured energy ladder for every atom. Occupancy and ionization change relative energies. The iron example shows loss of 4s electrons when Fe²⁺ forms.
- **Real d-series occupations:** scene 9 recomputes both 3d and 4s arrows for each atom from Sc through Zn. Chromium is [Ar]3d⁵4s¹ and copper is [Ar]3d¹⁰4s¹. Manganese and zinc restore 4s²; the animation no longer adds one d arrow mechanically at every step.
- **d block and transition metals:** the d region has ten columns. Under the usual strict definition, zinc is excluded from transition elements because its atom and common ion have full d subshells.
- **Main groups:** ns¹, ns² and ns²np¹–⁶ make the recurring patterns especially clear. Transition-metal chemistry also involves d electrons. Hydrogen is unusual: it has no closed inner core and is not an alkali metal.
- **Closed shell language:** He and Ne have completely filled principal shells. Ar and heavier noble gases have closed outer s and p sets; this does not mean every possible d or f state of the same principal shell is occupied. The narration uses the more precise wording.
- **Ionization:** removing an electron costs energy. In chemical reactions, other energy changes can make the overall process favourable. Noble gases are usually unreactive; heavier members can form compounds.
- **f-block convention:** this project uses Sc–Y–Lu–Lr in group 3 and fourteen-position La–Yb / Ac–No strips. Other printed layouts draw the boundary differently. La and Ac do not contain an f electron in their ground configurations, and early f-series atoms can mix f and d occupations. Fourteen is the subshell capacity, not a claim that every neighbouring atom adds precisely one f electron.
- **Periods:** the lengths 2, 8, 8, 18, 18, 32, 32 follow the usual sequence of subshell capacities. Period four combines 4s, 3d and 4p. Period six combines 6s, 4f, 5d and 6p. A period is not the complete filling of one principal shell. The previous square-number comparison has been replaced with these explicit recipes.
- **Orbital pictures:** surfaces plot angular density |Y|², omitting the radial factor and radial nodes. They are illustrations of angular shape, not full spatial isodensity surfaces. Blue/purple lobe colours encode wavefunction sign, never positive/negative charge. The sphere, dumbbell, clover and f example represent families; a family contains several independent functions, not simply copies of one rotated shape.
- **Sizes:** scenes 8 and 14 use Cordero covalent radii, carbon's sp³ value, on a consistent scale within each scene. Spheres illustrate relative covalent sizes, not hard physical boundaries of isolated atoms. The noble-gas illustrations are schematic. Li/F ≈ 2.2; Cs/Li ≈ 1.9.
- **Trends:** stronger effective attraction broadly contracts atoms across period two; additional shells broadly increase size down group one. Ionization energy and metallic character have general trends and exceptions.

## Model limits

`utils/physics_models.py` generates an idealized Madelung block grid and adds selected ground-configuration exceptions. This is a teaching model, not a full atomic structure calculation or a current authoritative database of every heavy atom's ground state. Position and block membership follow the chosen diagram convention; they are not reclassified from a literal “last electron” in every observed configuration. The self-check verifies capacities, electron conservation, positions, row counts, and the examples used in the film.

The continuity reference is the local Part 2 narration, especially scenes 16–18: neon to sodium, potassium, total-energy minimization, and the promised periodic-table explanation. [Part 2 repository](https://github.com/sjchem/youtube-manim/tree/main/atomic-structure-2).

## References

- [NIST neutral and ion configurations](https://math.nist.gov/DFTdata/atomdata/configuration.html): the configurations used for the first d series and the Fe/Fe²⁺ comparison. [Chromium ground state](https://physics.nist.gov/PhysRefData/Handbook/Tables/chromiumtable1_a.htm).
- [IUPAC periodic-table guidance](https://iupac.org/what-we-do/periodic-table-of-elements/): group numbering, alternative formats, the group-3 question, and the fact that IUPAC does not prescribe one 18- or 32-column drawing.
- [OpenStax Chemistry 2e, electron configurations](https://openstax.org/books/chemistry-2e/pages/6-4-electronic-structure-of-atoms-electron-configurations): state counting, Pauli, Hund, configurations, and the distinction between d-block membership and transition elements.
- [OpenStax Chemistry 2e, periodic properties](https://openstax.org/books/chemistry-2e/pages/6-5-periodic-variations-in-element-properties): shielding and the broad trends and exceptions.
- [Cordero et al., Covalent radii revisited (2008)](https://pubmed.ncbi.nlm.nih.gov/18478144/), DOI 10.1039/b801115j: the radius dataset used in the figures.
