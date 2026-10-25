# Animation plan — Molecular Orbital Theory, Explained Visually

23 chapters, 34:10 (34:00 of story plus a 10-second subscribe card). The
central visual story: **atomic waves → wave combinations → molecular orbital
energies → electron filling → bonding and magnetism**, framed by one mystery:
why does liquid oxygen hang between the poles of a magnet?

Colour contract (see `config.py`): blue/rose = sign of ψ (phase); cyan =
density and bonding levels; orange = antibonding; gold = unpaired electrons
and key numbers; green = a confirmed result; purple = the model's limits and
abstractions; muted = scaffolding. 3D chapters use the projected `Stage` engine
(`manim_scenes/stage3d.py`) with computed orbital surfaces.

| # | Time | Chapter | What moves on screen |
|---|---|---|---|
| 01 | 00:00 | Why is oxygen magnetic? | A turning 3D O₂; the Lewis O=O with every pair ringed; liquid O₂ poured from a flask is pulled into the pole gap and bridges it (simulated pour); two gold spin arrows ask "unpaired?"; a red cross on the Lewis pairs; freeze frame → title card |
| 02 | 00:55 | Two pictures of a bond | Series path; two H 1s clouds slide together and their electrons settle between the nuclei (valence bond); a |ψ|² fog spreads over the whole molecule (MO); a six-atom Hückel phase map; VB vs MO panels, "magnetism" glows |
| 03 | 02:30 | Waves add or cancel | Sign-coloured sine waves with a live phase tracker and their sum; then two 1s profiles; a coefficient slides from +1 to −1 and a gold node appears halfway |
| 04 | 03:50 | Adding atomic waves (LCAO) | "LCAO" from initials; φA, φB phase maps; ψ± equations; the ∝ glows; density maps of ψ+ (piled up) and ψ− (node line); phase maps with a ± key; 2 tiles in → 2 tiles out; 1 and 3 crossed out; four Hückel orbitals stacked by energy with 0–3 nodes; N → N |
| 05 | 05:40 | Bonding and antibonding (3D) | Two 1s surfaces slide together in phase and fuse into σ1s; a full turn about the axis changes nothing; out of phase they cannot merge — nodal plane, ψ = 0; side by side; gold force arrows pull nuclei into the shared density; red arrows indicate the antibonding separation; the caption states that a node changes density and raises energy, rather than claiming a literal wall |
| 06 | 07:05 | Two energies | The MO diagram is built: the 1s level splits, rise > drop; the LCAO H₂⁺ energy curves are traced live as the nuclei approach, with a riding dot and a two-nucleus icon; the valley is a bond; the rule card |
| 07 | 08:20 | One electron, half a bond | H₂⁺ diagram; one electron flies into σ1s (gold); the bond-order formula; 1 − 0 over 2 = 0.5; LCAO curve with the deeper exact minimum |
| 08 | 09:40 | Hydrogen: a full bond | A second electron pairs (Pauli); BO = 1 = the Lewis line; measured length and strength bars (H₂ vs H₂⁺): not quite twice as strong; diamagnetic |
| 09 | 10:50 | Helium: electrons that cancel | Four electrons fill σ1s then σ\*1s; BO = 0; a balance tips toward antibonding; helium atoms drift apart; remove the top electron → He₂⁺, BO = ½; bond-order line-up; the real He₂ drawn to scale against H₂ |
| 10 | 13:00 | Sigma from p orbitals (3D) | A p orbital with its nodal plane; two p orbitals aimed at each other slide together → σ2p with small opposite back lobes; a full axial turn; the phase coefficient slides to −1 and the cloud tears into σ\*2p; big splitting; three p orbitals side by side |
| 11 | 14:30 | Pi orbitals come in pairs (3D) | Parallel p orbitals merge into π (nodal plane through the axis); flip → π\*; σ vs π split; the second π rotated 90° about the axis; degenerate levels; both turn into π\*; the π\* pair glows gold; 6 → 6 |
| 12 | 16:00 | Building the energy diagram | The valence diagram assembled piece by piece; the filled 1s core set aside; 8 → 8; Aufbau (a ladder), Pauli (a third arrow refused), Hund (two electrons take one π orbital each); σ2p and π briefly swap |
| 13 | 18:10 | Two orderings | B₂/C₂/N₂ vs O₂/F₂ diagrams; σ2s and σ2p framed as same-symmetry; push arrows; measured 2s–2p gaps on an axis; a gold marker slides from F to B while σ2p climbs past the π pair; the crossing band between N and O; "toy model" note |
| 14 | 20:10 | Filling nitrogen | Ten electrons start on the atoms and fly into the MOs in Aufbau order with a live tally; the configuration; all paired; 8 − 2 over 2 = 3; N≡N |
| 15 | 21:45 | Nitrogen's triple bond (3D) | σ2p followed by each π contribution; the other clouds fade to faint context; D₀ bars for B₂–F₂ (N₂ strongest); BO vs length; liquid N₂ poured through the magnet falls straight through; diamagnetic; 10 → 12 electrons |
| 16 | 23:00 | Oxygen: where are they? | **The climax.** The Lewis O=O's bond lines dissolve into dots; all twelve dots fly into oxygen's MO diagram in Aufbau order; the twelfth hovers, refuses to pair (red cross) and takes the second π\* with parallel spin; silence; everything dims except two glowing gold arrows; bar magnets; PARAMAGNETIC; the two π\* orbitals in 3D, one electron each |
| 17 | 25:30 | Mystery solved | 8 − 4 over 2 = 2; Lewis gets bond order right, misses the unpaired electrons; spins align in the field and the pour hangs in the gap; field off → spins scramble, liquid drops; O₂ and N₂ pours side by side; fair note on advanced VB theory |
| 18 | 27:30 | Take one electron away | Charge dial; the highest (π\*) electron leaves → O₂⁺; BO 2.5 on a live meter; measured bars: shorter, stronger; one unpaired |
| 19 | 28:50 | Add electrons instead | Electrons drop into π\*: superoxide (1.5), peroxide (1); four 3D O–O models stretched to measured lengths; unpaired 1, 2, 1, 0 |
| 20 | 30:10 | Boron and fluorine | B₂ filled live (Hund: paramagnetic); F₂ filled (diamagnetic); four compact diagrams B₂, N₂, O₂, F₂ with bond orders and spins |
| 21 | 31:25 | Read the diagram | An unlabelled filled diagram, a countdown ring; no lone arrows → diamagnetic; 6 − 2 over 2 = 2; reveal C₂ |
| 22 | 32:10 | From waves to chemistry | Recap montage: the hanging liquid; σ/σ\* forming; H₂, N₂, O₂ diagrams; shape · energy · occupancy; a gallery of four turning MOs; the series path; "Bonds aren't sticks. They're quantum states."; two gold spins |
| 23 | 34:00 | Subscribe | House subscribe card between a turning σ1s and π\*2p |

## Where the animation effort went

1. **Lewis dots → MO slots (ch16).** Each Lewis electron is carried along an
   arc to the slot `mo_models` assigns; Hund's rule is shown as a refused
   pairing; the payoff is a dimmed diagram with two gold spins.
2. **Computed 3D orbitals (ch05, 10, 11, 15, 16, 22).** Every surface is
   |ψ| = level of a normalised LCAO combination, split into signed lobes by
   marching cubes, recomputed per frame while nuclei slide or the phase flips.
3. **Energy-level splitting and filling (ch06–09, 12–21).** One reusable
   `MODiagram` whose arrows always come from Aufbau/Pauli/Hund.
4. **The magnet pour (ch01, 15, 17, 22).** A seeded droplet simulation with a
   ∇(B²) pull for a paramagnetic liquid.
5. **O₂ → O₂⁺ → O₂⁻ → O₂²⁻ (ch18–19).** A charge dial, a bond-order meter,
   and 3D bonds stretched to measured lengths.

## Review refinements (24 October 2026)

Density samples stay in a bounded picture window, clear of titles. The wave
sum has more room above the caption, and wide p-orbital views use a smaller
zoom. Phase remains blue/rose in every orientation. The electromagnets have
shaded side and top faces, winding reflections and a consistent pole gap.
Nitrogen's orbital contributions are inspected one at a time. Oxygen-series
distance models use single connectors, with their fractional bond orders
stated separately. The final rotating pair shows oxygen's two π* states with
one spin marker each, rather than attaching unpaired spins to a 1s cloud.
