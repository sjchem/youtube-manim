# Concept summary — Periodic Trends, Explained Visually

*Atomic Structure · Part 4. Sequel to "Why Does the Periodic Table Have This Shape?"*

## The question

Why do atoms get **smaller** across the periodic table but **larger** down it, even
though both directions add protons and electrons? And how does that one contest
also decide which atoms give electrons away, which pull them in, and how they
bond?

## The core idea

Every main-group trend in the film comes from three questions about the
**outermost electrons**:

1. **How far are they from the nucleus?** (Which shell they occupy.)
2. **How strongly does the nucleus pull on them?** The charge they actually feel
   is the *effective nuclear charge*, Z_eff: the nuclear charge minus the part
   cancelled (shielded) by the other electrons, mostly the inner ones.
3. **How are the electrons arranged?** (Which orbital the electron is in, and
   whether it is paired.)

Coulomb's law sets the scale of the contest: attraction ∝ (charge) / (distance)².

- **Across a period**, each step adds a proton and puts the new electron in the
  *same* shell. Electrons in one shell shield each other poorly, so Z_eff rises
  and the cloud is pulled in. **Charge wins → atoms shrink.**
- **Down a group**, each step opens a *new, farther* shell. The extra protons are
  largely cancelled by the extra inner electrons, so distance takes over.
  **Shells and shielding win → atoms grow.**

## The trends, in the order the film builds them

| Property | What it measures | Broad trend (main group) | Exceptions shown |
|---|---|---|---|
| Atomic radius | size of a bonded atom (a measure, not a wall) | grows **down** and **left** | — |
| Ionic radius | size of an ion in a crystal | cations shrink, anions swell; isoelectronic ions shrink as Z rises | — |
| First ionization enthalpy | energy to remove the outermost electron from a gas-phase atom | rises **across**, falls **down** | Be > B (2p starts higher, more shielded); N > O (paired-electron repulsion); repeated as Mg > Al, P > S |
| Electron gain enthalpy | energy change when a gas-phase atom accepts an electron (negative = released) | more negative **across** (to the halogens), less negative **down** | F less negative than Cl (crowded 2p); N, Be, Mg, noble gases need energy |
| Electronegativity | pull on *shared* electrons in a bond (relative Pauling scale) | rises **across** and **up**; F highest | noble gases not compared |

These are tendencies with physical reasons, clearest for the main-group
elements, not exception-free laws.

## What the visuals mean (and do not mean)

- **Electron clouds** are seeded random samples of a hydrogen-like radial density
  (P(r) ∝ r² e^(−2r/a)), projected into 2D and scaled for illustration. They
  do not calculate each element's orbitals. Dots are probability samples, not
  separate electrons; the dashed contour is a display guide, not a measured
  atomic boundary. An atom has no hard surface.
- **Cloud sizes** are measured radii on one shared scale per shot. In the lithium
  vs neon experiment (chapter 09) and the ion/shell close-ups the sizes are
  schematic and labelled as such.
- **Nuclei are not to scale.** They would be ~100,000 times smaller than the cloud.
- **Pull arrows** are scaled by Slater's rules for Z_eff — a rough, classic
  estimate used only for arrow thickness; no Slater number is shown on screen.
- **The electron-transfer picture of NaCl is a simplified model.** The film shows
  that isolated-atom transfer is uphill (+496 − 349 = +147 kJ/mol) and that the
  lattice formation releases energy. The narration also includes the need to
  account for atomization from the elements in a complete energy balance.
- **The 3D bond landscape** (chapter 15) illustrates unequal sharing; it is a
  schematic density, not a computed molecular orbital. A large electronegativity
  difference suggests ionic character; there is no universal numerical cutoff.
- **The F vs Cl balance bars** are schematic except for the green "net" bars,
  whose ratio is the measured 328 : 349.

## Data and sources

All values live in `utils/element_data.py`; scenes never type a number.

- **NCERT Chemistry Part I, Class XI, Unit 3** ("Classification of Elements and
  Periodicity in Properties"): atomic radii (metallic radius for metals, covalent
  for non-metals), ionic radii, electron gain enthalpies.
- **NIST Atomic Spectra Database**: first ionization energies (eV), converted
  with 1 eV = 96.485 kJ/mol and rounded (beryllium therefore reads 900, the
  textbook's 899 being the same 899.5 rounded down).
- **Cordero et al., Dalton Trans. 2008, 2832–2838**: single-bond covalent radii,
  used for the radius heat map and the "covalent only" overlay so that one map
  uses one definition.
- **Pauling electronegativities** (Allred's 1961 revision); lead uses the Pb(II)
  value.
- **Pauling crystal radii** for O²⁻, Mg²⁺ and Cl⁻ (same scale as NCERT's Na⁺, F⁻).
- Electron affinities for main-group elements NCERT does not list (e.g. B, C,
  Al, Si, P, Ga–Bi, At) enter only the electron-gain heat map, without numbers
  on screen.

`python -m utils.element_data` checks that the data really show every trend,
ratio and exception the narration states, and that each of the 27 numbers
spoken in `narration.py` matches the data.

## Accuracy notes

- Atomic and ionic radii come from different measurements; the film says so and
  compares them as a pattern only.
- Noble-gas radii (van der Waals) are never mixed into the covalent radius map.
- Clementi–Raimondi Z_eff values *rise* slowly down a group while Slater's stay
  flat; the narration avoids claiming either and says the extra protons are
  "largely cancelled", which is true for both.
- Electron gain enthalpy is reported with NCERT's sign convention
  (ΔegH ≈ −electron affinity).

## References for this review

- [NCERT Class XI Chemistry, Unit 3](https://ncert.nic.in/textbook/pdf/kech103.pdf): teaching radii, ionization exceptions and electron-gain sign convention.
- [NIST Atomic Spectra Database: ionization energies](https://physics.nist.gov/PhysRefData/ASD/ionEnergy.html): first ionization data.
- [Cordero et al., “Covalent radii revisited” (2008)](https://doi.org/10.1039/B801115J): the consistent covalent-radius map; a compiled radius scale, including estimates.
- [IUPAC Gold Book: electronegativity](https://old.goldbook.iupac.org/html/E/E01990.html) and [electron affinity](https://goldbook.iupac.org/terms/view/E01977): distinguish a relative bonding scale from gas-phase electron attachment.
- [OpenStax Chemistry 2e: ionic and covalent bond strengths](https://openstax.org/books/chemistry-2e/pages/7-5-strengths-of-ionic-and-covalent-bonds): the complete Born–Haber energy cycle includes atomization and lattice formation.
- [Leimbach et al., “The electron affinity of astatine” (2020)](https://www.nature.com/articles/s41467-020-17599-2): the measured 2.41578 eV value used only in the heat map (approximately −233 kJ/mol).

The fluorine/chlorine close-up counts five **p-subshell electrons** in each
atom (2p⁵ and 3p⁵). Each atom has seven valence electrons in total, including
the two s electrons. The beads show occupancy, not circular electron paths.
Neon's attachment illustration does not leave a bound Ne⁻ ion on screen.
Disputed boundary classifications and superheavy elements stay muted in the
chemical-tendency map rather than receiving definite measured behaviour.
