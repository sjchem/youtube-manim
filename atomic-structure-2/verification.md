# Verification

Latest visual revision verified on 2026-09-14 with Python 3.12.9 and Manim Community Edition 0.21.0 (the repository's `youtube` pyenv).

## Revision to nineteen chapters — 2026-09-14

The film was restructured from 16 chapters / 23:50 to **19 chapters / 35:20**, adding three chapters and extending
ten. Every chapter was renumbered; `config.SCENES`, `main.CLASS_NAMES`, the scene module filenames, the class names,
each `prepare()` key and every narration heading were moved together.

### What was added

- **Chapter 03 (new, 100 s).** Bohr's model stated in numbers — `2n^2`, `r_1 = 0.53 Å`, `r_2 = 2.12 Å`,
  `E_1 = -13.6 eV`, `E_2 = -3.40 eV`, `v_1 = 2.188 × 10^6 m/s` — and the single failure the film's ending answers.
- **Chapter 05 (new, 90 s).** Two-slit interference built one electron at a time, and lost again under which-path
  detection.
- **Chapter 17 (new, 80 s).** Madelung's `(n + l)` rule, the `2p`/`3s` tie, and potassium's `4s^1`.
- **Chapter 04** gained the cricket ball's actual arithmetic and a logarithmic length ruler, and now spends Bohr's
  `v_1`. **Chapter 06** gained the `lambda = 2*pi*r_1` identity and the derivation of `m v r = n h / 2 pi`.
  **Chapter 07** now opens on Bohr's `(r_1, v_1, p_1)` and shows Heisenberg's microscope before withdrawing it.
  **Chapter 09** gained an everyday accumulation analogy. **Chapter 11** gained the radial distribution peaking on
  `a_0` and all five named d orientations. **Chapter 12** gained the house/floor/room address and the
  `1 + 3 + 5 = n^2`, `2n^2` derivation that recovers Bohr's 2, 8, 18. **Chapter 13** gained the third-shell
  penetration curves and the 4s/3d puzzle. **Chapter 14** derives the need for a fourth quantum number from
  helium's colliding addresses. **Chapter 15** gained oxygen's forced pairing. **Chapter 16** gained the
  `2, 8, 1` ↔ `1s^2 2s^2 2p^6 3s^1` bridge.

### New checks in `utils/audit.py`

- `lambda(v_1) / 2*pi*r_1 = 1` to within `1e-9`, and `3.324918 Å` to six figures.
- `r_1`, `r_2`, `v_1`, `p_1` and `r_3/r_1 = 9` against `scipy.constants`.
- The cricket ball at `1.035 × 10^-34 m`, and the nucleus/wavelength ratio inside the stated nineteen decades.
- `P(r) = r^2 R^2` normalized for 1s, 2s, 2p and 3d; zero at the nucleus while `|psi_1s|^2` is maximal there;
  peaking at `a_0` for 1s and at `n^2 a_0` for the largest `l` of each shell.
- Third-shell penetration: innermost lobes at `0.74`, `3.00` and `9.00 a_0`, and `3s > 3p > 3d` integrated to
  `1.5 a_0`.
- The Madelung sequence to ten subshells, the `4s = 4 < 3d = 5` comparison, and the `2p`/`3s` tie resolved by
  smaller `n`.
- `sum(2l+1) = n^2` and `2n^2 in (2, 8, 18, 32)`.

### Results

- **Science:** all three groups pass, including every assertion above.
- **Narration:** 19 exports match, windows contiguous, **4,877 words**, **35:20**, all chapter rates inside 80–150
  wpm (measured range 120.4–146.0).
- **Per-chapter render:** all 19 chapters land within one frame of their planned window, with **0 layout flags** —
  no text out of bounds, no caption collisions, nothing visible outside the anchor at any chapter end.

### Corrected during the revision

- **The penetration claim was wrong as first written.** The initial assertion `3s > 3p > 3d` integrated to `2 a_0`
  fails — 3p overtakes 3s there (`0.0169` against `0.0144`). The true statement is about the innermost lobe
  positions (`0.74`, `3.00`, `9.00 a_0`), and the integrated ordering holds only inside about `1.5 a_0`. The
  assertion, the on-screen core band and the narration were all rewritten to the region where the claim is true.
- **Chapter 12's depth-sorted z axis blocked the flat background.** `raise_ground()` refuses to restore the ground
  while anything depth-sorted is on stage, so the street beats rendered on bare background colour. The axis is now
  dropped before the camera closes and rebuilt when it reopens.

## Animated experimental recap

- Scene 02 now recreates scattering around a lit 3D nucleus, sends a light pulse through a hydrogen spectroscope, and links three discrete energy drops to their matching spectral lines. The nucleus, energy levels and spectrum remain visible while the circular route becomes a question.
- The final light clue comes from a surviving spectral line, which opens into the exact travelling-wave geometry expected by Scene 03. The nucleus is not shown emitting photons. Short cues replace persistent headings, and moving particles, packets and staged evidence reveals replace the former long still holds.
- The original narration and **50-second** window are unchanged. The final standalone audit passes at **50.07 s**, with zero text flags, no temporary-root leaks, a flat outgoing camera, cleared billboard registrations and the expected outgoing wave.
- Both joins pass using real chapters 01 → 02 → 03 at 30 FPS: **190.03 s** against **190 s** planned. The sphere helper moved into `manim_scenes/atomic_visuals.py`; an AST comparison confirms its lighting implementation is unchanged from the approved Scene 01.
- The schematic scattering curves stay outside the drawn nuclear surface. Explicit Bézier controls avoid spline overshoot. A crossfade to the dashed orbit avoids intermediate coils, and checkmarks have their own space beside the labels.
- Final motion preview: **50.66 s**, **854 × 480**, **15 FPS**, at normal speed without audio. Selected frames were reviewed across scattering, dispersion, energy changes, the questioned track and the final light cue.
- Artifacts: `output/scene02_revision/`, `output/scene02_continuity/audit.json`, `output/scene02_motion/review_frames.jpg`, and `output/scene02_motion/videos/scene_02_what_survives/480p15/Scene02WhatSurvives.mp4`.

## Richer opening

- Scene 01 now uses lit 3D spheres, a luminous partial trail on the single classical orbit, and a gentle camera move. Same-colour surface edges seal Cairo's antialias gaps; lighting freezes with the camera during static narration holds.
- The velocity arrow follows the actual tangent at the paused electron position. The track itself unwraps into the wave. The closing cloud uses brighter, static 1s detection samples with camera parallax and a brief title above it.
- The original narration and **40-second** chapter window remain unchanged. The final standalone check passes at **40.00 s**, with zero text flags, no temporary roots left behind, a restored flat camera at unit zoom, and no remaining fixed-orientation markers.
- Full-film continuity passes at **1430.33 s**, with no endpoint text flags. Later sphere seam and static-lighting refinements pass the focused opening check and do not change its choreography or timing.
- The final motion preview is **40.13 s**, **854 × 480**, **15 FPS**, at normal speed without audio. Sampled frames cover the moving electron, question markers, orbit-to-wave transition, cloud reveal and title fade.
- Review artifacts: `output/opening_revision/` (endpoint report and storyboard), `output/opening_full_continuity/audit.json`, and `output/opening_motion/videos/scene_01_where_is_it/480p15/Scene01WhereIsIt.mp4`. Final sampled frames are in `output/opening_motion/review_frames.jpg`.

## Current shortened cut

- Planned runtime **23:50**, **16 chapters**, **3,066 spoken words**. Script order, contiguous windows, speaking rates and all speech-only exports pass.
- Revised chapters **12–16** pass standalone at 15 FPS, with no endpoint text collisions or bounds violations. This check includes MathTex glyphs.
- The continuous `FullVideo` passes at 30 FPS: **1430.33 s** against the planned **1430 s**. The small difference is frame rounding across chapter joins.
- The lifecycle check passes across the full film: no chapter leaves a visible root outside its outgoing anchor.
- Science invariants pass: radial normalization, nodes and phase signs, the Gaussian uncertainty product, sampling statistics, enclosed surface probability and H–Ar occupancy constraints.
- Compilation passes over `config.py`, `main.py`, `manim_scenes` and `utils`.
- The continuous ending preview rendered successfully: **230.16 s**, **854 × 480**, **12 FPS**, no audio. Sampled frames around the chapter joins, teaser and subscribe card were visually reviewed.
- The revised ending's two storyboard sheets were visually reviewed. They cover the H/He/Li examples, carbon's choice, the Ne → Na bridge, recap and separate subscribe card.
- The former Cr/Cu source is preserved under `assets/references/next_video/`. The equation revision changes scene modules 03, 05 and 06; the other scene modules and the original orbital numerical models match their pre-revision sources.

## Linked equations and portraits

- The continuous chapters 03–06 motion review is **151.08 s**, **854 × 480**, **12 FPS**, at **3× production speed**, with no audio. The final uncertainty chapter was rendered from the preceding chapter’s outgoing wave and joined to the completed footage. Sampled frames verify readable live values before, during and after the squeeze, all three portraits, and the hydrogen equation layouts.
- Scenes 03, 05 and 06 pass their original narration windows at 15 FPS with zero endpoint text flags. The final Schrödinger layout also passes after moving the operator plate and energy labels away from the orbital.
- Live uncertainty readouts follow the packet-width tracker throughout the squeeze; the momentum unit stays fixed so doubling remains readable.
- The uncertainty brackets now measure from the mean to one standard deviation; their earlier ±sigma span incorrectly labelled a two-standard-deviation interval as one. The corrected scene passes its standalone audit.
- SI wavelength and uncertainty calculations pass, including reciprocal scaling. The hydrogen energy values agree with an independent finite-difference Hamiltonian applied to the actual 1s/2p wave functions.
- The full-film continuity check passes at 30 FPS, at **1430.33 s**. Later diagram refinements were individually rechecked and leave the chapter windows unchanged.
- Narration exports match at **3,066 words**; windows remain contiguous and the planned runtime stays **23:50**. The rate audit uses 80–150 words per minute, accommodating the user's existing 145.5-wpm opening without rewriting it.
- Portrait source pages, download URLs, credits and reuse statements are recorded in `assets/images/README.md` and `portrait_sources.json`.
- Equation-review storyboards live under `output/equation_revision/`; the final Schrödinger sheet is under `output/equation_schrodinger_final/`, and the corrected uncertainty sheet is under `output/equation_uncertainty_final/`. The continuous full-film report is `output/equation_full_continuity/audit.json`.

## Revision-specific fix

The shortened carbon/neon chapter exposed an extra root created by a `LaggedStart` over the three owned p-orbital boxes. The revised chapter indicates each owned slot directly, so the completed neon diagram remains a single anchor at the join.

## Earlier renderer fixes retained

- **The layout audit was silently skipping every equation.** `MathTex` holds no points of its own and reports a fill opacity of zero, so the visibility test excused all of them. The check now reads opacity from the glyphs. Fixing it immediately surfaced a real caption collision in chapter 9.
- **The flat background was hiding every 3D surface.** Manim's 3D camera sorts depth-sorted mobjects by distance and then draws everything else in front of them, so a background rectangle covers an orbital completely. Surfaces now carry a `_needs_depth_sort` flag and the scene lowers the ground before one arrives.
- **Laplacian smoothing tore the orbital meshes.** It contracts the narrow neck between the lobes of a d state until the surface opens, and the gap showed as background through the middle of the atom. Replaced with Taubin smoothing, which relaxes the facets without shrinking.
- **Manim's own 3D shading fought the per-face lighting**, producing dark wedges across otherwise smooth lobes. It is now switched off for the whole film in `cfg.apply_project_theme`.
- Chapters 10 and 15 (formerly 16) introduced a p orbital before opening the camera, so it appeared end-on as a disc. Both now move the camera first.
- The energy ladder in chapter 11 sat in the bottom half of the frame, because its level values are physical ordering rather than screen coordinates. It is now centred, and chapter 11 reads shelf positions from the diagram instead of repeating them as constants.

## Render cost

Measured on this machine at 2560 × 1440, 30 FPS, single process:

| Shot type | Wall time per second of video |
|---|---|
| Rotating calculated orbital | ≈ 22× realtime |
| Flat diagram chapter | ≈ 4.6× realtime |

Using the earlier measurements, the shortened film is roughly 420 s of 3D and 1010 s of 2D, so a full master is on the order of **four hours**. Use
`python main.py preview NN` while iterating; each orbital is a few thousand individually depth-sorted and
individually lit triangles, and that is where the time goes.

## What has not been done

A full-length 2K master and a recorded voiceover have **not** been produced. Endpoint checks do not replace
watching the video: they verify where each animation lands, not what it looks like in between. Follow
`voiceover_guide.md` after recording, and re-check the chapter `at()` marks against measured narration before
cutting a voiced master.

## Review artifacts

Generated files are ignored by Git:

- `output/equation_motion/videos/equation_preview/480p12/EquationPreview.mp4` — the revised continuous equation review, at 3× speed without audio.
- `output/equation_motion/review_frames.jpg` — selected final motion-review frames.
- `output/ending_revision/` — the revised chapters' endpoint audit and two storyboard sheets.
- `output/ending_full_continuity/audit.json` — the current full-film continuity audit at 30 FPS.
- `output/ending_motion/videos/ending_preview/480p12/EndingPreview.mp4` — continuous motion preview of chapters 12–16 at their actual narration pace, with no voiceover.
- `output/storyboard/` and the older general motion preview remain historical review artifacts; they predate the condensed ending and its chapter numbering.
