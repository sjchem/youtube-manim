# Animation plan — Part 2

One question runs the whole film: **if the classical orbit is gone, what describes an electron in an atom?**
Every chapter hands the next one the diagram it was arguing with, so the joins are transformations rather than cuts:

```
ORBIT → WAVE → PROBABILITY → ORBITAL → ATOM → CHEMISTRY
```

`common.spine_strip()` draws those six stations and lights the current one. It appears twice — at the pivot in
chapter 10, and as the closing summary in chapter 18 — and is never parked permanently on the frame.

## The number bank

Chapter 3 is the film's hinge, and it is not a demolition. It puts Bohr's radius, energy and speed on screen, alongside the school shell-capacity rule. Their different origins matter when these numbers return later:

| Banked in chapter 3 | Spent in | What happens to it |
|---|---|---|
| `v₁ = 2.1877 × 10⁶ m/s` | 4 | becomes a de Broglie wavelength of 3.3249 Å — the size of the atom |
| that wavelength + `r₁` | 6 | `λ = 2πr₁` exactly, so `2πr = nλ` **is** `mvr = nh/2π`; Bohr's rule is recovered within the ring model |
| `r₁` and `v₁` together | 7 | the classical path also claims exact position and momentum vectors; their component spreads cannot both vanish |
| `r₁ = 0.529 Å` | 11 | returns as the peak of `P(r) = r²R²` — the likeliest distance, not a track |
| `2n² = 2, 8, 18` | 12 | re-derived from `1+3+5 = n²` orbitals × 2 spins |
| "cannot explain why atoms join" | 16–17 | answered by electron filling |

`utils/audit.py` asserts every one of these, including that `λ(v₁)/2πr₁ = 1` to nine significant figures.

## Chapters

| # | Window | Anchor it receives | What it does with it | Anchor it hands on |
|---|--------|--------------------|----------------------|--------------------|
| 01 | 0:00–0:40 | — | Three rotating classical shells with small glowing electrons and a red/gold nucleon cluster; isolate one electron with a short luminous trail; crosshair and tangent velocity flicker; the actual track unwraps into a wave, then a bright static detection cloud gains depth through camera parallax | detection cloud |
| 02 | 0:40–1:30 | cloud | Scattering around the same red/gold nucleon cluster as scene 1; the cluster persists through the evidence panels and the questioned orbit; hydrogen light disperses into four bright lines; energy drops match their colours; the evidence remains while the route becomes a question, then a surviving spectral line opens into travelling light | matter wave |
| 03 | 1:30–3:10 | wave | Nested Bohr shells with a small bright electron continuously circling during camera moves, narration holds and diagram transforms; larger near-white cyan n labels and pale-gold numerical values; 2n² counted to 32; radius arrows to 0.53 Å and 2.12 Å; a spacious −13.61/−3.40 eV ladder and enlarged energy formula; a short trail highlights the same moving electron beside 2.188 × 10⁶ m/s; three gold quantity chips; two moving atoms approach with a question mark in the clear gap; the outgoing single orbit keeps moving until the next chapter | orbit |
| 04 | 3:10–5:40 | orbit | Illuminated light source, travelling field pulses and separate phosphor detections; de Broglie portrait; λ = h/p with a spacious p ≈ mₑv label beside it; continuously moving amplitude with speed 1 → 2 million m/s and a shrinking wavelength bracket; bright cricket-ball arithmetic and logarithmic comparison; Bohr's v₁ gives 3.32 Å; periodic crystal with advancing incident wavefronts, animated scattered crests, detector arrivals and an intensity curve all driven by the same coherent finite-array amplitude; I ∝ \|ΣAⱼ\|² is explained in narration; the outgoing amplitude keeps moving under the one-electron question | travelling wave |
| 05 | 5:40–7:10 | wave | Compact apparatus leaves dedicated caption bands; confined source electrons stay active; moving gold classical pellets build two strips; six individual electrons show a cyan/violet amplitude pulse followed by one bright mint detection, with no drawn quantum trajectory; hundreds of white-centred points build fringes; a live glowing amplitude map and colour-matched P = \|A₁+A₂\|² explain the bands; a fresh coral detection run with a path detector uses P = \|A₁\|²+\|A₂\|² and a smooth envelope; outgoing standing-wave ring oscillates with fixed nodes | ring standing wave |
| 06 | 7:10–8:25 | ring wave | Bright live ring wave with cyan/violet phase trails and a glowing H centre; a coral seam shows the non-closing trial; closed 4-, 5- and 6-wavelength patterns crossfade while phase motion continues; ring shifts left beside larger bright equations; a moving gold circumference highlight supports λ = 2πr₁ = 3.3249 Å; spaced algebra recovers mvr = nh/2π with an explicit h/(mv) fraction; a brief ring-analogy caption hands off a travelling wave | travelling wave |
| 07 | 8:25–11:45 | wave | **Opens on Bohr's r₁, v₁ and p₁ = m v** with a continuously rotating bright electron and following radial/tangent vectors; colour-coded numerical values; **then Heisenberg's microscope**, short λ against long λ with their recoil arrows, withdrawn under "but this blames the apparatus"; five coloured travelling components stack into a live Gaussian amplitude; position and momentum panels share one `ValueTracker`; bright Δx/Δp one-sigma markers occupy separate clear lanes; the relation on a plate; Heisenberg portrait; 100 → 50 pm doubles the minimum spread; the orbit's markers go red | packet |
| 08 | 11:45–14:05 | wave | Clamped string, three modes with their nodes counted; then the 3D camera continuously circles smaller, lowered 1s/2p surfaces; left-side energy and momentum/operator equations stay clear of the shapes; Schrödinger portrait; Ĥψ = Eψ expands to kinetic plus Coulomb potential; 1s/−13.6 eV and 2p/−3.40 eV arrive as paired outputs; flatten to a phase slice | phase slice |
| 09 | 14:05–17:00 | phase slice | Sign legend and charge warning in separate clear bands; gentle framing push-ins on unchanged density slices; square it; a moving selected region and P(V) = ∫\|ψ\|²dV; **then the street plan** — one cat photographed at random, 150 pins densest at a gently glowing warm doorway, and the two-line mapping to detections and density; then eight detections one at a time, then nine hundred, kept within the caption-safe area; the records fade into the map | density slice |
| 10 | 17:00–18:10 | density slice | Smaller ORBIT/ORBITAL headings; continuously orbiting classical marker alongside a gently framed fixed density; the path fades, and ORBIT visibly transforms into ORBITAL; the state moves to centre and continues a slow push-in; six-station spine | density slice |
| 11 | 18:10–21:55 | density slice | All 3D orbital displays reduced by 22%, including the 2s node radius and reference axis; 1s boundary choice and linked radial probability; translucent/cutaway 2s; 2p nodal sheet tessellated at z=0 and shown near side-on; p orientations and all five d shapes; separate side column for the d-state count; nodal-plane view repeated clearly at the end | 2p surface |
| 12 | 21:55–26:15 | 2p surface | n watched as scale, ℓ as shape with s/p/d/f badges; **then the camera closes and a street of three houses is built** — house number = n, floor = ℓ, room = orbital, and house n has exactly n floors; **the rooms are counted** 1, 1+3, 1+3+5 = n², ×2 spins = 2n², landing on 2, 8, 18 with "shell capacity follows from state counting"; L² follows each angular family; camera reopens for Lz = m_ℓℏ, the worked 2pz address, and Sz = ±ℏ/2; a bounded, slow camera sway continues through the 3D narration holds; soft room-by-room highlights keep the housing analogy and capacity explanation active; ends on the shorthand card with a gentle row-by-row reading highlight | shorthand card |
| 13 | 26:15–28:45 | card | Fixed hydrogen shelves with a passing light highlight; an animated schematic force balance at one outer-electron position shows unchanged nuclear attraction plus increasing inner-electron repulsion; **three aligned radial panels** share the same radius and probability scales, with separate 0.74, 3.00 and 9.00 a₀ peak cards and an illustrative core strip in each row; a moving common-radius guide compares the fixed curves; split levels remain active with light sweeps and highlighted same-shell comparisons for n=2 and n=3; a marker walks 1s → 4s → 3d; the 4s/3d puzzle leads to orbital boxes | orbital-box diagram |
| 14 | 28:45–30:05 | boxes | Each new electron appears as a drawn spin arrow in the existing diagram; a moving border follows the active 1s or 2s orbital; H and He density portraits receive a gentle close-up; the portrait yields to He’s matching spatial addresses, which are highlighted in turn before focus moves to the differing spin label; the correct opposite-spin pair is drawn before Pauli is named; Li opens 2s; all motion clears before handoff | boxes |
| 15 | 30:05–31:55 | boxes | Carbon’s allowed candidate arrows are drawn in turn, with moving borders comparing the active orbitals; a gentle density close-up yields to the later equation; Hund follows the lower-energy choice; oxygen adds the third parallel arrow, then the opposite-spin partner; moving focus compares the equivalent p orbitals during the explanation; neon’s last two arrows arrive in sequence, and the three completed boxes are highlighted while deriving 3 × 2 = 6 | neon boxes |
| 16 | 31:55–33:10 | neon boxes | Na’s 3s arrow is drawn into the existing diagram; all 2,8,1 shell markers keep rotating while brighter equations map shells to subshells, with a gold outer electron and moving reading highlights; schematic density views turn rigidly about their nuclei, with a bright cyan closed Ne outer shell and bright gold Na 3s density over muted blue cores; the gold ionization marker remains visible as the valence density fades and Na⁺ remains | Ne/Na comparison |
| 17 | 33:10–34:30 | comparison | Eighteen glowing occupancy markers build with the argon counter; light sweeps keep the fixed energy levels readable. Gold 4s and violet 3d carry the candidate comparison through bright arithmetic columns, moving row guides and flowing diagonal arrows. A bright nineteenth marker lands on 4s; the final configuration and occupied level receive a moving reading highlight. Original narration and 80-second timing remain. | shelves |
| 18 | 34:30–35:05 | answer | A continuously moving classical electron unwraps into a travelling wave. Bright fixed detections build in batches; the camera opens the 2p cloud and its matching lit orbital emerges at the same display scale, with the answer and probability equation held clear of the figure. A continuous camera drift reveals the orbital; occupied arrows draw into their boxes. The existing periodic-table reveal, spine and next-video teaser stay intact. | periodic table |
| 19 | 35:05–35:20 | table | Separate thank-you card; staged SUBSCRIBE and cyan rule; white science tagline; gentle emphasis and fade | — |

The Be/B/N/F walkthrough and the Cr/Cu comparison remain deferred. Archived Cr/Cu material lives in
`assets/references/next_video/`; it is the natural first exception to chapter 17's closing caveat.

## Equations

Three get the plated treatment and nothing else does:

- `\lambda = h/p` (chapter 4)
- `\Delta x\,\Delta p \geq \hbar/2` (chapter 7)
- `\hat H\psi = E\psi` (chapter 8)

Everything else is pinned plain text at the top or bottom of the frame, and leaves as soon as the beat it
explains is over. The derivation in chapter 6 (`2πr = nλ → mvr = nh/2π`) is built line by line in the right-hand
lane rather than plated: it is an argument, not a headline.

## Analogies, and how they are retired

The film uses four, and each one is captioned as an analogy on screen before it is handed on:

| Analogy | Chapter | Caption that retires it |
|---|---|---|
| A wave closing on a ring | 6 | "ring analogy · real states are three-dimensional" |
| A string clamped at both ends | 8 | "an analogy · an atom has no string and no wall" |
| A cat photographed at random | 9 | "an analogy · a cat is somewhere between photographs" |
| A street of houses with floors and rooms | 12 | "an analogy · a shell is not a container" |

## Pacing

- Cues hold 1.5–3 seconds. No caption repeats a whole narration sentence.
- `at(t)` marks the beats. `QuantumScene.at` raises rather than drifts if the choreography overruns, so a chapter
  cannot quietly eat its neighbour's window.
- `finish()` pads to the planned duration and refuses to end with anything visible outside the anchor.
- Narration runs 120–146 wpm per chapter; `utils/audit.py` rejects anything outside 80–150.


Revision: chapter 5 illustrates amplitudes at both slits without drawing an electron trajectory. Path detection begins a fresh run and removes only interference. Chapter 11 replaces the surface/plot overlap with a linked density slice and spherical probability integral. Chapter 12 adds L², Lz and Sz at the relevant label introductions. Narration preserves the 19 windows while distinguishing these calculations from the house and cat analogies.
