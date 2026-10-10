# Animation plan — Periodic Trends, Explained Visually

20 chapters, 23:40. Four chapters use real 3D (`ThreeDScene` with a tilted
camera): 06, 10, 15, 18. Every other chapter is flat, but its atoms are
seeded 3D point clouds that turn slowly, so nothing on screen is static.

**One visual grammar** (defined once in `manim_scenes/common.py`):

| Idea | Picture | Colour |
|---|---|---|
| Outer electrons | a turning, projected probability sample; contour is a size guide | cyan |
| Inner (core) electrons | a smaller, denser cloud | gray-blue |
| Nucleus | a glowing ball with its charge (+Z) written on it (not to scale) | red |
| The nucleus's pull | gold arrows pointing inward, thickness ∝ Slater Z_eff | gold |
| Felt charge Z_eff | a purple bar or label | purple |
| Energy released / required | green arrows down / orange arrows up | green / orange |
| A property | one cool→warm heat scale; in 3D, a tower height | heat scale |
| Element / block | Part 3's rounded tile and block colours (s blue, p green, d gold, f purple) | block colours |

## Chapter by chapter

| # | Time | Chapter | What moves |
|---|---|---|---|
| 01 | 00:00 | **A strange contradiction** (hook) | A lithium cloud shrinks step by step to fluorine (NCERT radii, one scale), a dashed ring keeping lithium's size; then grows from lithium to caesium. Fluorine and caesium side by side with a "?"; one electron escapes caesium, one is pulled into fluorine. Title card. |
| 02 | 01:02 | **From shape to prediction** | Part 3's four blocks fly in and assemble the table; s/p/d/f pills. Symbols fade to outlines. A tile releases an atom; "size / grip / pull on one more". A heat wave of real ionization data sweeps the main groups. The memorised arrow is crossed out; three questions appear. |
| 03 | 02:17 | **The pull of the nucleus** | A + nucleus and − electron; gold tug arrow. Charge ×2 → pull bar ×2; distance ×2 → pull bar ×¼ (Coulomb, computed). "pull ∝ Z / r²". A planetary orbit is drawn and crossed out; the cloud replaces it; "dense: likely / faint: rare"; a display contour, "No hard boundary". |
| 04 | 03:22 | **Shielding and Z effective** | Sodium: 11 protons, a gray core of 10 inner electrons, one outer electron. Gray push arrows: shielding. "+11" bar vs a short purple "felt" bar; Z_eff. Split screen: left Li→F (same shell; Z_eff bar rises, cloud contracts), right Li→Na→K (new shells; cloud expands). The contest: gold arrows in, cyan arrows out. |
| 05 | 04:47 | **Across a period, atoms shrink** | The cloud and a live graph move together, Li→F (152→64 pm), pull arrows thickening. Brackets mark metallic vs covalent radii; the covalent-only data set (Cordero) is overlaid dashed — same trend. Period 3 (186→99 pm) in gold. "and down?" |
| 06 | 06:18 | **Down a group, atoms grow** (3D) | Translucent lit spheres Li→Cs to scale, one ring per shell; the camera tilts so the shells read as rings in depth. Values and "caesium ≈ 1.7 × lithium". Halogens F→I (drawn 1.7× larger, labelled). The spheres go away: a cloud thins out; two bonded clouds with d and r = d/2. Verdict: pull wins across; shells win down. |
| 07 | 07:38 | **Losing and gaining electrons** | Na loses its outer electron; the outer cloud fades leaving the core, the dashed ring showing the old size (186→95 pm); 11 protons hold 10 electrons. F gains one; the cloud swells with repulsion arrows (64→136 pm). Note: atomic and ionic radii are measured differently. |
| 08 | 08:52 | **Same electrons, different size** | O²⁻, F⁻, Na⁺, Mg²⁺ start identical, 10 electrons each (1s² 2s² 2p⁶); their charges are revealed, pull arrows thicken, and the clouds contract to 140/136/95/65 pm. Mg²⁺ inside the O²⁻ ghost ring. |
| 09 | 09:43 | **How hard is it to remove an electron?** | Definition and X(g) → X⁺(g) + e⁻. Lithium and neon side by side with energy meters filling at the same rate: lithium's electron escapes at 520, neon's only at 2081 — about 4×. Pull arrows explain: far + weak Z_eff vs close + strong. |
| 10 | 10:57 | **The ionization mountain range** (3D) | The line graph for Z = 1–86 draws itself; peaks (noble gases) and cliffs (alkali metals) are labelled; it becomes bars, the bars swing up into a 3D mountain range as the camera tilts; a gold ridge joins the falling peaks. Back to 2D: period 2 enlarged, two red wrong-way steps. |
| 11 | 12:05 | **When the trend seems to break** | Bars Be 900 vs B 801 and an "expected" ghost. Orbital-box energy diagrams: Be's electron lifted from 2s, B's from the higher, more shielded 2p (shorter gold lift). N vs O: three unpaired vs one pair with a red repulsion spark. Period 3 repeats both dips. |
| 12 | 13:30 | **Adding an electron instead** | An electron flies in; X(g) + e⁻ → X⁻(g). Energy diagram: released = level drops (green, ΔH < 0). Chlorine's 3p fills (−349). Neon would require a higher shell: the level rises (orange), and the extra electron fades; no stable Ne⁻ is left. Bars across period 3 and down group 17; fluorine's bar turns red with a "?". |
| 13 | 14:32 | **Fluorine versus chlorine** | The guess "fluorine (smaller)" is crossed out by the bars −328 vs −349. Close-up: five 2p electrons crowd fluorine's compact p region and push a newcomer back; chlorine's 3p region has room. Schematic balance bars: pull, crowding, net welcome (green ratio = measured). |
| 14 | 15:38 | **A tug of war inside a bond** | H–Cl with a shared cloud drawn evenly, crossed out, then sliding toward chlorine; δ⁺ / δ⁻. Three cards keep ionization, electron gain and electronegativity apart, each with its own mini animation. The Pauling scale: H 2.2, Cl 3.2, Δ ≈ 1.0. |
| 15 | 16:40 | **Electronegativity across the table** (3D) | A lit 3D electron-density landscape: a symmetric ridge (Cl–Cl) leans more and more as ΔEN grows (H–Cl, 2, Na–Cl; increasing ionic character, no universal cutoff), camera slowly orbiting. Back to the table, coloured by Pauling values: up and to the right; F ≈ 4.0, Cs 0.79. |
| 16 | 17:44 | **Sodium gives, chlorine takes** | Na (ionization 496, low) and Cl (−349). The electron transfers (simplified model); Na⁺ shrinks, Cl⁻ swells; the ions attract. The honest ledger: +496, −349, net +147 uphill. A turning rock-salt crystal; one Na⁺ and its six Cl⁻ neighbours light up; the lattice pays the bill. KCl, NaBr, KBr; groups 1 and 17 on a mini table. |
| 17 | 19:08 | **A map of chemical behaviour** | The table recoloured by tendency: + badges for groups 1–2, metallic character down-left, − badges for N, O, F, noble gases ringed, then metals → metalloids → non-metals across. Period-3 oxides: Na₂O basic, Al₂O₃ amphoteric, SO₃ acidic, on a blue→orange bar. |
| 18 | 20:22 | **A map of invisible forces** (3D) | Tabs: Radius → Ionization → Electronegativity → Electron gain. The main-group tiles rise into a heat-map skyline that morphs between tabs while the camera orbits; electron-gain exceptions sit flat and orange. Four 2D mini maps with their arrows. The opening paradox replayed with live atoms (Li→F, Li→Cs), the three questions, and a final orbiting skyline: "INVISIBLE FORCES". |
| 19 | 22:47 | **From trends to bonds** | The table fades to Na and Cl; their tiles become atoms; size, ionization, electronegativity and reactivity link them; the atoms drift together until their clouds meet. "Why do atoms bond at all?" Next: Chemical Bonding, Explained Visually. |
| 20 | 23:30 | **Subscribe** | House-style card with two small turning atoms. |

## Render cost notes

- A cloud is drawn as six depth layers (one VMobject each), not hundreds of
  Dots: Cairo pays per mobject, so this is several times faster and looks the
  same.
- The 3D chapters keep solids cheap: prisms (6 faces each), one 476-face
  surface rebuilt only while it morphs, translucent spheres at 10×20.
- The rock-salt crystal is hand-projected (shaded discs sorted by depth), so it
  turns at 2D cost.
