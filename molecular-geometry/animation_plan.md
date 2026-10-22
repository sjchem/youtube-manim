# Animation plan — Molecular Geometry, Explained Visually

22 chapters, 28:00 (27:50 of story plus a 10-second subscribe card). Every
chapter lands on its `config.SCENE_DURATIONS` second; narration beats in
`narration.py` drive the cues. "3D" means a projected `Stage`
(`manim_scenes/stage3d.py`): real rotating geometry, depth-sorted, with
perspective.

**Recurring visual rule:** show the electron geometry first (cyan bond lobes,
purple lone-pair lobes), then hide the lone pairs to reveal the molecular
geometry. One central model morphs between relatives instead of cutting to new
drawings.

| # | Time | Chapter | What moves |
|---|---|---|---|
| 01 | 00:00 | The shape mystery | Flat Lewis O=C=O and H–O–H write on; "3 atoms" counters. The 3D models take over at exactly the Lewis positions, the camera tips, CO₂ stays straight (live 180° arc), water bends while a live readout counts down from 180° to 104.5°. A gold "?" pulses; water's lone-pair lobes appear; title card. |
| 02 | 00:50 | Lewis structures are flat | Recap icons from Part 1 (energy valley, σ overlap, π overlap). Lewis vocabulary on water. Methane drawn as a flat cross with 90° squares; the 3D model turns edge-on (a line), then the bonds lift into a tetrahedron while a live arc goes 90° → 109.5°; faces flash; "connections" vs "shape"; electron-region lobes appear. |
| 03 | 02:15 | Electron regions push apart | A bare central atom. Two regions squeezed together relax to 180° — the actual gradient-flow path of the repulsion model. A third relaxes to 120°. The triangle tips flat, a fourth drops on top and the three fold down (umbrella) into a tetrahedron. A seeded random start relaxes again beside a live total-repulsion curve. "VSEPR" assembles from its initials; 2/3/4 line-up. |
| 04 | 03:35 | Counting regions | Four rule rows: single, double, triple bond, lone pair → one region each. AXₘEₙ colour-coded (A white, X cyan, E purple) with keys. Ammonia's Lewis structure is counted into AX₃E; 3 + 1 = 4 = steric number; ammonia's region layout turns. |
| 05 | 04:30 | Linear and trigonal planar | CO₂: Lewis, counts, regions push to 180°, spin. "4 electrons → 1 region". BF₃: Lewis, three 120° arcs, turned edge-on to a line (planar). 2/3/4 line-up with a red ✗ on "4: flat?". |
| 06 | 05:45 | The tetrahedron | Four regions in a square; red 90° crowding arcs and push arrows. Two tilt up, two down (live arc 90° → 109.5°). Faces; hydrogens arrive. The model turns 45° and sits on alternate corners of a cube; vectors (1,1,1) and (1,−1,−1); dot product −1, lengths √3, cos θ = −1/3, θ ≈ 109.47° boxed. |
| 07 | 07:15 | Ammonia: one lone pair | Methane's model: C → N with a valence-dot panel (3 for bonds, 2 stay). The top site becomes a purple lone pair. Tetrahedral faces (electron geometry) vs pyramid faces (molecular geometry), toggled on the same model. Live arc 109.5° → 106.7° as the bonds squeeze; red push arrows from the lone pair. |
| 08 | 09:00 | Water: two lone pairs | N → O, a second lone pair; tetrahedral electron geometry; lone pairs hidden; the model turns until H–O–H faces the camera; live arc 106.7° → 104.5°. CH₄ / NH₃ / H₂O line-up with measured angles. Honesty beat: qualitative trend, measured numbers, a struck-out fake formula. The opening pair returns with 2 and 4 regions; five regions tease. |
| 09 | 11:05 | Five electron regions | Tetrahedron + one below relaxes into a trigonal bipyramid. Equatorial triangle (gold) and axial tags; bipyramid faces. 120°, 90°, 180° arcs with a growing angle table. PCl₅ (gas phase) at measured lengths: axial 214 pm vs equatorial 202 pm. |
| 10 | 12:20 | One family, four shapes | PCl₅ with dashed guides for all five directions. A trial lone pair tries an axial site (3 red 90° arcs) then an equatorial one (2 red, 2 green 120°). Morphs PCl₅ → SF₄ (seesaw) → ClF₃ (T) → XeF₂ (linear), each with its formula, AXₘEₙ and measured distortions; a small CO₂ for comparison; four-model family line-up. |
| 11 | 14:00 | Six electron regions | Bipyramid + one relaxes into an octahedron; 90° and 180° arcs; eight faces. SF₆ rocked about two axes (all directions equivalent). Lewis count note; a faint lone pair asks the next question. |
| 12 | 15:00 | Flat from six | SF₆ → BrF₅ (square pyramid, measured upward tilt, live arc). Second lone pair tried cis (90°, red ✗) then trans (180°, green ✓). XeF₄: square face, edge-on line, "six regions… and flat?", lone pairs above and below. Octahedral family line-up. |
| 13 | 16:30 | Mixing orbitals | VSEPR directions; carbon's 2s sphere and three 2p orbitals (blue +, rose −); 90° arc vs gold tetrahedral directions ("no match"). ψ = cos α ψₛ + sin α ψₚ. A dial drives one orbital continuously from s to p with a live "% s" readout; sp marked. s ± p → two sp hybrids at 180°; the two unused p orbitals appear in purple. |
| 14 | 18:00 | sp² and sp³ | Three spheres mix into sp² hybrids (120°), unused p upright, fluorines on the tips (BF₃). Four mix into sp³ (tetrahedron, nothing left over), hydrogens on the tips. Orthogonality: hᵢ = (s + √n pᵢ)/√(1+n), ⟨hᵢ\|hⱼ⟩ = 0 → cos θ = −1/n; rows for n = 1, 2, 3; "the cube's −1/3 again"; two routes, same directions. |
| 15 | 19:40 | Methane and ethene | Methane's regions hand over to four sp³ hybrids; hydrogen 1s orbitals glide in head-on; gold σ glows. Ethene from measured geometry, plane laid flat: H–C–H arc, top view; sp² hybrids + upright p orbitals; σ framework; π overlap lobes above and below; one end twists 90° and the π overlap fades, then returns. |
| 16 | 21:00 | Two models, one molecule | NH₃ and H₂O with sp³ hybrids (lone-pair hybrids purple); measured angles vs struck "ideal sp³: 109.5°". A two-column VSEPR / Hybridization comparison. sp³d and sp³d² shown as historical textbook labels. |
| 17 | 22:00 | Bond dipoles | HCl with electronegativities, a leaning electron cloud, δ+ / δ−, and an orange bond-dipole arrow; a two-arrow vector-addition demo. CO₂'s two arrows chain tip to tail and cancel (μ = 0). Water's arrows chain on a separate right-hand stage to a green net arrow; a big net arrow on the molecule (μ ≠ 0, polar). |
| 18 | 23:20 | Symmetry decides polarity | BF₃, CH₄ and NH₃ in 3D; each bond-dipole set chained head to tail on a second stage that turns in step: the BF₃ triangle and CH₄ skew quadrilateral close (μ = 0); NH₃'s chain doesn't, and its net arrow points to the lone-pair side. Three symmetric nonpolar molecules, then two polar molecules, in spacious rotating comparisons; caveats. |
| 19 | 24:45 | Predict the shape | Recipe strip (Lewis → count → electron geometry → hide lone pairs) that lights up step by step. Three questions with countdown rings: SO₂ (bent, 119.3°), PF₃ (trigonal pyramidal, 97.8°), BrF₃ (T-shaped). BF₃ / PF₃ / BrF₃ line-up: three fluorines, three shapes, 0/1/2 lone pairs. |
| 20 | 26:30 | Molecules live in 3D | The opening pair returns and gains, layer by layer, regions (VSEPR), hybrids, and dipoles (μ = 0 vs μ ≠ 0). Flat Lewis structures return, then give way to the turning 3D models; "3D changes everything" card. |
| 21 | 27:25 | Why is oxygen magnetic? | O=O Lewis (all paired); a horseshoe magnet; seeded O₂ droplets drawn into the gap; "?"; a delocalised glow; "NEXT: Molecular Orbital Theory" card. |
| 22 | 27:50 | Stay curious | Subscribe card with turning CH₄ and H₂O models. |

## Production priorities (from the brief) and where they live

1. CO₂ vs H₂O from 2D to 3D — chapter 01 (and the callback in 20).
2. Regions reorganising from 2 to 6 — chapters 03, 09, 11 (computed relaxation paths).
3. CH₄ → NH₃ → H₂O with lone pairs appearing and hiding — chapters 07–08, one model.
4. s and p combining into sp, sp², sp³ — chapters 13–14 (computed mixing).
5. Bond-dipole vectors CO₂ vs H₂O — chapter 17, extended to 3D in 18.

## Visual review refinements

Atoms use 36 shading contours and a soft reflection; translucent regions and
orbitals use finer gradients. Angle labels remain within the readable picture
area. Lewis bonds and lone-pair dots clear the actual element glyph bounds,
including large O and two-letter Br. Opening headings clear after a few seconds.
The four-member five-region comparison uses smaller bounded turns and a wrapped
shape label. The polarity recap shows three nonpolar molecules, then two polar
ones. In the finale, both molecules turn in the upper band above the title.
The ethene orbital view shows one C–C sigma cylinder plus separate pi lobes.

Narration estimates use 100 words / 35 seconds. JSON cue sheets include expected
speech and visual-pause durations; optional per-beat recordings are placed at
those cues without changing voice speed. All 22 scenes and the 28:00 plan remain.
