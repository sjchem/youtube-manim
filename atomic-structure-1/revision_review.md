# Revision review

Fifteen scenes replace the original seventeen teaching scenes and separate
closing card. Planned runtime is 22:05, with 2,772 spoken words. See
[the merge map](animation_plan.md) and [the narration](narration_script.md).

## Completed

- Rebuilt the opening as mystery, promise, bigger mystery, and story. The
  promise is spoken only: probe paths and detector flashes surround a concealed
  object and a drawn question mark. Scene 1 ends with the film title,
  “How We Discovered What an Atom Looks Like,” within its existing narration
  window; the spoken promise remains off screen.
- Merged the three pairs in source, narration, CLI order and chapter timestamps.
- Revised all narration for natural speech and corrected misleading scientific
  shortcuts. Exported fifteen clean TTS files plus a complete plain-text script.
- Replaced scene 07's dense deductions with three short cues beside animated
  scattering. Enlarged and brightened both radius equations and the core marker.
  A public-domain cricket-ball photograph now shrinks into a five-kilometre
  centre-to-edge comparison, with a quiet street motif and no repeated heading.
  The brief closing cue fades to leave electrons and field arrows. Radius/diameter
  and diagram-scale qualifications remain in the unchanged narration.
- Kept the same prism through the white-light/hydrogen comparison.
- Eased 3D camera sweeps, replaced moving reading holds with stable diagrams,
  and reduced sphere mesh detail only for low-resolution previews.
- Fixed the illustrative Thomson trajectory to retain its outgoing direction.
- Rebuilt Dalton's cutting sequence (scene 03) with shaded cubes, three cutting
  planes and eight genuine pieces per division. Its glowing solid-atom model
  rotates continuously during the explanation and placement changes.
  John Dalton's portrait and name now introduce the scene beside the cube,
  fading as the first cut begins within the same 75-second narration window.
- Rebuilt scene 04 as a 3D glass-tube experiment with metal electrodes, a wooden
  base, small component labels and fluorescent screen. Removed the explanatory
  sentence captions, vacuum label and visible beam; screen observations carry
  the experiment. Added Thomson's portrait to a separate measurement card,
  retained the modern mass comparison and preserved the final trial sequence
  verbatim. See [portrait credits](assets/images/README.md).
- Simplified scene 05's titles into brief introductions tied to their animations.
  Replaced the small charge subscripts with large orange positive and cyan
  negative terms. Removed lingering prediction text from the sheet view, reduced
  its lattice and path density, and preserved the final prediction card.
- Cleaned scene 06's experiment view: captions fade before being unpinned,
  the camera eases into the overhead view, and a reflective gold sheet replaces
  the atomic grid. Removed the running sentence captions, softened old tracks
  and flashes, and moved the textbook rarity figure to a separate clear card.

- Brightened scene 08's velocity and acceleration labels and matching arrows,
  enlarged the energy/radius terms, and set the radiation statement in bold type.
  The collapse now starts at the current orbit radius and electron position.
  Cleared the diagram before presenting the lifetime and centred failure card,
  keeping the closing question and narration unchanged.

- Rebuilt scene 09 around a powered hydrogen discharge, moving emitted-light
  packets and a travelling wave that smoothly shortens from red through green
  to violet. The crest-to-crest wavelength bracket contracts with the wave.
  Kept one prism and screen for the continuous-light and hydrogen trials, with
  rays visibly meeting the spectrum. Removed persistent headings and sentence
  captions; kept brief labels, a scanned element comparison, a stellar pattern
  shift and a visual staircase hand-off. Narration remains unchanged.

- Rebuilt scene 10's ramp and stairs as shaded solid forms with a plain gold
  ball. Removed the ramp instruction, claim card, crowding sentence and closing
  sentence. The physical steps fade into an energy diagram; the brief hydrogen
  label clears while the main level numbers and original GROUND STATE label
  remain. Preserved energy-proportional hydrogen spacing and added a stationary
  state hold, excitation and a red photon from the n=3 to n=2 transition.

- Rebuilt scene 11 with separate areas for energy levels, the enlarged
  ΔE = hν card, light waves and the spectrum. Removed the persistent heading,
  gloss and closing sentence. The visible-light comparison now uses 3→2 and
  6→2; its two packets move at the same displayed speed. Each barcode-writing
  transition clears its arrow and photon before the next. The 434 nm numerical
  example follows a full ladder clear, and the ending keeps the equation and
  spectrum without leftover arrows.

- Reduced scene 12's four comparison-row labels from 34 to 30 points.
  Successful points use warm cream and the unmet Rutherford points use a
  soft blue-grey; green checks, red crosses and panel headings retain their
  existing colours and sizes.

- Cleaned scene 13's opening: the question fades before the zoom and “no.”
  sits below the small atom. The atom fade preserves transparent orbit rings.
  Reduced the four limitation points to 34-point warm cream text and removed
  “and there was a deeper problem,” keeping the wave-behaviour statement and
  the existing narration window.

- Enlarged scene 14's orbit, nucleus and electron by about one third. Removed
  the probability sentence and limited the question to a three-second hold.
  The cloud uses 420 brighter, camera-facing dots with depth sorting; its brief
  “One electron” cue clears before the longer visual hold. Text fades while
  still fixed to the screen, and the 3D scene fades before the camera resets.
  The closing card and narration now say “Next video.”

Scene 14 keeps the next-video introduction, while `Scene_15_Subscribe` provides a
separate 15-second closing card and its own narration.

## Verification

Narration sequence, windows, word rates and exported-text consistency pass.
The original fourteen scenes were exercised by the timing and text-layout audits; flagged
captions and tight timing windows were corrected and checked again. Key physics
checks cover the scale ratio, 434 nm example and outgoing toy-scattering slope.
Python compilation passes. Representative frames from every scene were reviewed.
After separating the closing card, scenes 14 and 15 both pass timing and layout
checks; all fifteen narration exports match the revised script.

Rendered and inspected previews:

- [Opening](media/videos/scene_01_impossible_atom/480p15/Scene01ImpossibleAtom.mp4)
- [3D cutting and rotating Dalton atom](media/videos/scene_03_dalton_sphere/480p15/Scene03DaltonSphere.mp4)
- [3D cathode-ray experiment](media/videos/scene_04_cathode_rays/480p15/Scene04CathodeRays.mp4)
- [Thomson model and prediction](media/videos/scene_05_thomson_prediction/480p15/Scene05ThomsonPrediction.mp4)
- [Gold-foil experiment](media/videos/scene_06_gold_foil/480p15/Scene06GoldFoil.mp4)
- [Cricket-ball scale](media/videos/scene_07_empty_space/480p15/Scene07EmptySpace.mp4)
- [Classical collapse](media/videos/scene_08_unstable_atom/480p15/Scene08UnstableAtom.mp4)
- [Hydrogen barcode](media/videos/scene_09_light_barcode/480p15/Scene09LightBarcode.mp4)
- [Energy floors](media/videos/scene_10_energy_floors/480p15/Scene10EnergyFloors.mp4)
- [Photon energy and spectral lines](media/videos/scene_11_photon_ladder/480p15/Scene11PhotonLadder.mp4)
- [Rutherford and Bohr comparison](media/videos/scene_12_what_bohr_got_right/480p15/Scene12WhatBohrGotRight.mp4)
- [Limits of the orbit picture](media/videos/scene_13_not_an_orbit/480p15/Scene13NotAnOrbit.mp4)
- [Beyond the orbit: next video](media/videos/scene_14_part_two/480p15/Scene14PartTwo.mp4)
- [Separate subscribe card](media/videos/scene_15_subscribe/480p15/Scene_15_Subscribe.mp4)

These are 854 × 480, 15 FPS previews, approximately 65, 75, 120, 120, 125, 115, 80, 125, 95, 95, 85, 80, 60 and 15 seconds, respectively.
The revised Dalton scene also passes the timing and text-layout audits. Its
[review frames](output/review/scene_03.jpg) show the split cubes and changing
surface orientation throughout the atom explanation.
The [new opening frame](output/review/scene_03_dalton_portrait.png) shows Dalton's
portrait beside the cube; its addition also passes timing and layout checks.
Scene 04 passes timing at 15 and 30 FPS and the text-layout audit. Its
[rendered review frames](output/review/scene_04.jpg) confirm the shadow, both
screen-spot deflections, Thomson's portrait, modern value and preserved ending.
The screen fluorescence is drawn over the screen surface so Cairo's depth sort
cannot hide the downward-deflected spot.
Scene 05 passes timing at 15 and 30 FPS and the text-layout audit. Its
[rendered review frames](output/review/scene_05.jpg) confirm the charge colors,
title fades, clear sheet view and unchanged final prediction card. The preview
is 120.06 seconds; the original narration remains unchanged.
Scene 06 passes timing at 15 and 30 FPS and the text-layout audit. Its
[rendered review frames](output/review/scene_06.jpg) confirm the horizontal title
fade, metallic foil, smooth overhead transition, quieter trails and isolated
rarity card. The foil covers all selected incoming lanes. The assembled preview
is 125.13 seconds; narration exports still match the original script.
Scene 07 passes timing at 15 and 30 FPS and the text-layout audit. Its
[rendered review frames](output/review/scene_07.jpg) confirm the sequential cues,
large radius equations, transparent ball photograph, continuous pullback,
uncluttered distance diagram and visual ending. The new preview is 115.07 seconds
at 854 × 480 and 15 FPS. The existing narration and all exports remain unchanged.
Scene 07 now uses a flat camera; the other six 3D chapters retain their camera moves.
Scene 08 passes timing at 15 and 30 FPS and the revised text-layout audit. Its
[rendered review frames](output/review/scene_08.jpg) confirm the brighter symbols,
bold radiation statement, cleared vector labels during collapse and separate
conclusion card. The preview is 80.07 seconds at 854 × 480 and 15 FPS; narration
exports remain unchanged and match the script.
Scene 09 passes timing at 15 and 30 FPS and the final text-layout audit. Its
[rendered review frames](output/review/scene_09.jpg) confirm the brief opening
labels, powered discharge, smooth red–green–violet wave and contracting bracket,
connected prism rays, continuous rainbow without slice seams, four-line screen,
barcode comparison and stellar example. The longer/shorter cues fade without
morphing their letters. The completed preview is 125.07 seconds at 854 × 480 and
15 FPS. Narration exports remain unchanged and match the script.
Scene 10 passes timing at 15 and 30 FPS and the text-layout audit. Its
[rendered review frames](output/review/scene_10.jpg) confirm the shaded ramp and
steps, clear ball landings, transition to energy rails, short-lived hydrogen
label, preserved GROUND STATE label and red emitted-light packet. The preview
is 95.07 seconds at 854 × 480 and 15 FPS. Narration remains unchanged.
Scene 11 passes timing at 15 and 30 FPS and the text-layout audit. Its
[rendered review frames](output/review/scene_11.jpg) confirm the prominent ΔE
equation, separated wave rows, one transition at a time, 434 nm example and
final spectrum with no leftover arrows or sentence captions. The preview is
95.06 seconds at 854 × 480 and 15 FPS. Narration exports are unchanged and match
the script.
Scene 12 passes the text-layout audit. Its [comparison frame](output/review/scene_12_comparison.png)
confirms smaller, warm-toned row labels with clear margins inside both panels.
The new preview is 85.07 seconds at 854 × 480 and 15 FPS.
Scene 13 passes timing at 15 and 30 FPS and the text-layout audit. Its
[rendered review frames](output/review/scene_13.jpg) confirm that the question
clears before the zoom, “no.” sits below the atom, the smaller limitation
points use warm cream, and the deleted lead-in is absent. The preview is
80.07 seconds at 854 × 480 and 15 FPS; narration exports remain unchanged.
Scene 14 passes timing at 15 and 30 FPS and the text-layout audit. Its
[rendered review frames](output/review/scene_14.jpg) confirm the brief horizontal
question fade, larger atom, brighter round cloud dots, clear cloud-only hold,
and smooth fade before the NEXT VIDEO card. The preview is 60.07 seconds at
854 × 480 and 15 FPS. Narration and exports now say “In the next video”; the
complete script contains 2,772 spoken words and passes the narration audit.
The final render setting remains 30 FPS. See [render instructions](README.md).
The complete high-resolution film has not been rendered in this revision.

ManimGL 1.7.2 was already installed in the active `youtube` pyenv. Its separate
[4-second smoke render](media/manimgl/ManimGLSmoke.mp4) passed using EGL and Mesa
software OpenGL. No reinstall was needed. The main film remains Manim CE as
requested.

Final audio synchronization requires the actual ElevenLabs voice track. No
cloned speech was generated or added. Use the [recording guide](voiceover_guide.md)
for the remaining recording and editing step.
