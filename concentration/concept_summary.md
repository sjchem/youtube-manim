# Concept summary — Concentration, Explained Visually

## The one idea

A concentration is always a fraction: **an amount of the thing we care about,
divided by a reference**. Change the reference and the number changes, even
though nothing in the glass has changed. Every measure in the film is one of
four quantities over another:

| Measure | Numerator | Denominator (the reference) | Unit |
|---|---|---|---|
| Molarity (amount concentration) *c* | moles of solute | volume of **solution** | mol/L = M |
| Molality *m* (or *b*) | moles of solute | mass of **solvent** | mol/kg = m |
| Normality *N* (historical) | reaction **equivalents** | volume of solution | eq/L = N |
| Mole fraction *x* | moles of one component | moles of **everything** | none |
| Mass percent % (w/w) | mass of solute | mass of solution | % |
| % (w/v) | grams of solute | 100 mL of solution | % |
| % (v/v) | volume of solute | volume of final solution | % |
| Mass concentration γ | mass of solute | volume of solution | g/L |
| ppm, ppb | a part | 10⁶ or 10⁹ parts, **on a stated basis** | — |

## The reference solution

18.0 g glucose + 180.0 g water; measured final volume 191.0 mL (the brief's
illustrative measurement, used as an input rather than predicted from adding
volumes). Rounded molar masses 180 and 18 g/mol.

| Quantity | Value |
|---|---|
| *n*(glucose), *n*(water) | 0.100 mol, 10.0 mol |
| mass of solution | 198.0 g |
| molarity | 0.100 / 0.1910 L = **0.524 M** |
| molality | 0.100 / 0.1800 kg = **0.556 mol/kg** |
| mole fraction of glucose | 0.100 / 10.1 = **0.00990** (water 0.99010) |
| mass percent | 18.0 / 198.0 × 100 = **9.09 %** |
| % (w/v) | 18.0 g / 191.0 mL × 100 = **9.42 %** |
| mass concentration | 18.0 g / 0.1910 L = **94.2 g/L** |
| density | 198.0 / 191.0 = **1.037 g/mL** |

Rounded molar masses are the teaching convention here. Exact molar masses
can change the final reported digit, so keep one consistent convention
throughout the worked example.

## The three reveals

1. **One solution, many correct values** — they differ because their
   denominators are different physical things (scenes 01, 04, 06, 12, 14).
2. **Temperature changes molarity, not molality** — a closed sample with expansion headspace keeps its
   liquid composition while its volume grows. If it expands like water (ρ 0.99821 → 0.97778
   g/mL from 20 to 70 °C), 191.0 mL becomes 195 mL and the molarity falls to
   0.513 M; the molality stays 0.556 mol/kg (scene 08).
3. **Normality depends on the reaction** — 0.500 M H₂SO₄ is 0.500 N when one
   proton-equivalent per acid formula unit is consumed (→ NaHSO₄) and 1.00 N when both equivalents are consumed
   (→ Na₂SO₄). N = M × z, and z belongs to the stated reaction. IUPAC
   discourages "normality" and "equivalent"; the film says so and recommends
   molarity plus a balanced equation (scenes 10–11).

## Connections

* **Density bridges volume and mass**: one litre weighs 1000 ρ grams; the
  solute in it weighs c M_s; the rest is solvent, so m = c / (ρ − c M_s)
  (ρ in kg/L, M_s in kg/mol). For the reference: 1036.6 g, 94.2 g, 942.4 g, and
  about 0.524 / 0.9424 = 0.556 mol/kg (unrounded values retained internally) (scene 17).
* **Dilution conserves moles**: M₁V₁ = M₂V₂ while nothing reacts or escapes;
  100 mL of 2.00 M made up to 500 mL is 0.400 M (scene 18).
* **Mole fractions sum to one**, and for an ideal solution Raoult's law
  P_water = x_water P°_water: here about 1 % lower (scene 13).
* **Colligative properties use molality**: ΔT_f = K_f m with K_f = 1.86 K kg/mol
  gives about 1.03 °C for the reference solution; ΔT_b = K_b m ≈ 0.28 °C
  (dilute, ideal, non-electrolyte) (scene 07).
* **ppm/ppb need a basis**: by mass 1 ppm = 1 mg/kg; 1 mg/L ≈ 1 ppm only for
  dilute water-like solutions (in ethanol, 1 mg/L ≈ 1.27 ppm by mass); gases
  usually by amount (CO₂ above 400 ppm) (scenes 16, 19).

## Honest limits and metaphors

* The 191.0 mL volume is the brief's illustrative measurement; the heating
  step assumes water-like expansion; the molarity-vs-molality plot uses a
  constant apparent molar volume calibrated on the reference solution. Each is
  labelled as a model.
* Ethanol–water contraction (50 + 50 mL → about 96.5 mL) is computed from
  tabulated mixture densities at 20 °C.
* Packing spheres, freezing lattices, vapour escaping a surface and one bead
  per 0.0100 mol in the dilution are pictures, labelled "a picture, not to
  scale" on screen. Swarms that claim a ratio keep the true 1 : 100 glucose to
  water molecule ratio; particle sizes are not to scale.
* Thermal motion is a smooth deterministic jiggle, not a molecular dynamics
  simulation.

## Sources

* IUPAC *Compendium of Chemical Terminology* (Gold Book): amount
  concentration, molality, mole fraction, mass concentration.
* IUPAC *Compendium of Analytical Nomenclature* (Orange Book): concentration
  terms; "normality" and "equivalent" not recommended.
* D. Harvey, *Analytical Chemistry 2.1* (LibreTexts), ch. 2: concentration
  units, normality for a stated reaction, ppm/ppb, % w/w, w/v, v/v.
* CRC *Handbook of Chemistry and Physics*: water density vs temperature;
  ethanol and ethanol–water densities; K_f and K_b of water.
* OpenStax *Chemistry 2e*, ch. 11: colligative properties and Raoult's law.
* NOAA Global Monitoring Laboratory: atmospheric CO₂ above 400 ppm.

The reaction multiplier z means equivalents per mole. It is not the IUPAC
equivalence factor f_eq, which uses the reciprocal convention. Acid structures
are proton-equivalent bookkeeping; aqueous sulfuric acid contains ions. The
0.500 M label always describes the original stock, before adding base.

Temperature independence assumes unchanged liquid composition. Once ice
forms or solvent boils away, recalculate the remaining liquid’s composition.

Mole-fraction sampling is independent and with replacement: the expected
waiting time for glucose is 1/x = 101 picks, not a guarantee for one trial.

Direct references used in the review:

- [IUPAC: amount concentration](https://goldbook.iupac.org/terms/view/A00295/plain)
- [IUPAC: molality](https://goldbook.iupac.org/terms/view/M03970)
- [IUPAC: amount fraction](https://goldbook.iupac.org/terms/view/A00296)
- [IUPAC: equivalence concept and normality](https://publications.iupac.org/analytical_compendium/Cha06sec3.pdf)
- [OpenStax: colligative properties](https://openstax.org/books/chemistry-2e/pages/11-4-colligative-properties)
- [NOAA: global atmospheric carbon dioxide](https://gml.noaa.gov/ccgg/trends/gl_trend.html?simple=True)
