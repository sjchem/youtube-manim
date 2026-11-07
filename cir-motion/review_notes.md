# Circular Motion — scene review

Reviewed against both supplied attachments. All 26 scenes were inspected in
source and fresh storyboard frames. The Oceanic theme and native Manim 3D
visuals are retained. The planned runtime remains 37:40.

Opening headings expire after a short hold. Chapter transitions now show the
title alone, without a chapter number or badge. Narration carries the longer
explanations; labels and answers stay compact.

## Scene-by-scene result

| Scene | Review and correction |
|---|---|
| 01 — Hook | Checked straight-road and circular-track framing, speedometer, turning arrows and final title. Shared car bounds now enter the motion audit. |
| 02 — Acceleration | Checked the three changing-velocity demonstrations, comparison panels and equation transitions. |
| 03 — Speed and velocity | Moved the horizontal vector label above the arrow; constrained result widths; reduced snapshot arrows and cleared them during the live lap. |
| 04 — Tangent | Shortened the tangent guide; moved its label; shortened the summary. Comparison arrows fade before the next demonstration. |
| 05 — Components | Cleared derivative and component readouts before the magnitude proof; narrowed the square-root expression; checked the space-time helix. |
| 06 — One lap | Shortened captions, corrected rounded arithmetic to an approximation, and explicitly removed the old result outline before the velocity demonstration. |
| 07 — Delta v | Cleared the detached subtraction workbench and second velocity before the limiting diagram; split the centripetal label into two short lines. |
| 08 — Velocity triangle | Separated the approximation and table in successive fades; raised and spaced table rows; removed the obsolete reference ring before the final proof. |
| 09 — Derivation | Raised the paired-circle legends and checked the shrinking-angle proof, velocity-circle construction and numerical result. |
| 10 — Speed and radius | Checked both comparison tracks, the shared physical clock, true arrow scaling, radius change and snapshot cleanup. |
| 11 — Coast and nudge | Corrected narration: the polygon's corners stay on the circle, while its chords pass inside. Checked refinement and live acceleration. |
| 12 — Radians | Title-only chapter opener; checked arc-length construction, conversion labels, signs and full-turn readout. |
| 13 — Angular velocity | Checked angular readout, graph and 3D turntable; equations remain above the moving illustration. |
| 14 — Period | Shortened definitions, cleared them in a separate fade before reciprocal formulas, and simplified the numerical period line. |
| 15 — Angular acceleration | Used compact horizontal comparison cards with more bottom clearance. |
| 16 — Centripetal force | Shortened the force definition and examples; checked force arrows, result and three physical force sources. |
| 17 — String release | Cleared rejected paths and their labels on release; moved Newton's first law away from the outgoing ball and removed obsolete equations from the final fade; shortened the gravity inset caption and kept its arrow within the inset. |
| 18 — Car and friction | Separated the two demand bars; condensed their numerical captions; checked the wider skid path and replay. |
| 19 — Satellite | Corrected equal-time straight-line reference distance; removed misleading whole-fraction cancellation strikes; added a moving satellite to the real 400 km orbit. |
| 20 — Rotating frames | Reduced car/track sizes, kept captions inside taller panels, bounded rotating landmarks, moved formula above the road and cleared its caption before the final comparison. Added the Coriolis qualification in narration. |
| 21 — Uniform motion | Raised the closing question and checked the radial-only diagram and readouts. |
| 22 — Nonuniform motion | Cleared earlier arrows before introducing the polar basis; checked radial, tangential and resultant arrows and worked values. |
| 23 — Comparison table | Tightened row spacing to clear the final principle; reduced icon arrows so they do not intrude into neighbouring text or rows. |
| 24 — Challenges | Replaced full-sentence bottom answers with compact results at the right; moved the second comparison circle left; cleared rejected release paths before the answer. |
| 25 — Synthesis | Qualified the inward-force statement as uniform circular motion in both narration and caption; checked the six-value grid and closing 3D track. |
| 26 — Closing card | Checked text spacing and final fade. |

## Shared visual correction

A 3D arrow with `glow=False` previously regained a halo each time the stage
projected it. Projection now preserves that setting. Remaining live-arrow
halos are narrower and softer. A regression check exercises both settings
through visible, partially faded and hidden states.

The layout audit now includes essential 2D geometry and 3D car bodies, with
4–8 motion samples per animation, in addition to text overlap, frame bounds
and title expiry. These are sampled checks; they do not prove every possible
frame is collision-free.

## Narration

The corrected source is `narration.py`. Clean and ElevenLabs-tagged scripts,
per-scene files, per-beat files and cue sheets have been regenerated. Existing
delivery tags and beat start times are preserved. Scientific corrections are
recorded with sources in `assets/references/brief_review.md`.

## Validation

Passed: Python compilation; numerical models and spoken numbers; narration
pacing and delivery; visual contracts; all-scene timing at 15 and 30 fps;
full-film construction (2260.00 seconds, zero leftover objects); and sampled
moving-layout checks for all 26 scenes (zero remaining detected issues).

The first motion sweep caught transition overlaps in scenes 14 and 17. Both
were corrected and rechecked, including timing and full-film continuity.
Scene 23 was rechecked after making its closing equation more compact to
leave additional subtitle space. Full evidence: `output/review/validation.txt`.

Fresh contact sheets are in `output/review/storyboard/scene_XX_sheet.png`.
Silent 480p motion excerpts are supplied in
`output/review/rotating_frames_preview.mp4` and
`output/review/skid_preview.mp4`. A compact all-scene overview is in
`output/review/overview.png`. The full 37:40 film and narration
audio have not been rendered as part of this review.
