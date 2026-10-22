# Molecular Geometry — visual and narration review

Reviewed against the supplied brief on 20 October 2026. The title remains
**Molecular Geometry, Explained Visually**, following *Chemical Bonding,
Explained Visually*. All **22 scenes** remain independently renderable, with a
planned total of **28:00**.

## Changes

- Smoother shaded atoms, finer translucent electron-region and orbital
  gradients, softer reflections, and smoother small oxygen molecules.
- Lewis bonds and electron dots now clear the actual element glyph bounds,
  including large oxygen symbols and two-letter bromine symbols.
- Angle labels stay in the readable picture area. Cube direction labels clear
  before the final rotating tetrahedron shot.
- The five-region family uses smaller, bounded turns and a wrapped shape name.
  The polarity recap compares three nonpolar molecules, then two polar ones,
  giving each structure room to move.
- Water's tip-to-tail dipole construction sits beside its molecule, so the
  vector chain no longer crosses a hydrogen atom.
- Closing molecules move into the upper band before the title appears and
  remain visible while turning.
- BF₃'s hybrid-orbital view now has a boron centre. Ethene's orbital view shows
  one C–C sigma cylinder and separate pi lobes; unused teaching layers fade
  back so the overlap is easier to see.
- The VSEPR/hybridization comparison uses shorter captions. Opening chapter
  headings clear within the first few seconds.
- A half-turn alignment now recovers the actual rotation axis, preserving rigid
  geometry even for a 180-degree turn.

## Narration and voice timing

The revised script has **3,648 words**. At **100 words per 35 seconds**, that
is approximately **21:17 of speech**, leaving **6:43 distributed through the
28-minute visual edit** for looking, morphs, predictions, breathing and the
closing card. Each of the **242 narration beats** fits its own window; the
fastest requires about **2.77 words/second**, below your stated 2.86.

Clean and tagged narration, Markdown timing cues and the JSON cue sheet have
been regenerated. Cue sheets now show estimated speech and visual-pause time.
The script avoids suggesting that every four-region molecule is bent, limits
the decreasing-angle comparison to CH₄/NH₃/H₂O, and identifies equal-character
orthogonal hybrids as an ideal model. Molecular polarity considers both bond
polarity and structure, consistent with
[OpenStax's molecular structure treatment](https://openstax.org/books/chemistry-2e/pages/7-6-molecular-structure-and-polarity).

For automatic cue placement, run `python -m utils.narration_export --beats`,
record the numbered texts at your usual pace, and save each recording under
`assets/audio/scene_XX/beat_001.wav` and the following beat numbers. The scene
places them at their cues without altering your voice speed. Alternatively,
use one edited `assets/audio/scene_XX.wav` with pauses matched to the cue sheet.
The audio checker rejects incomplete beat sets, duplicate formats, mixed modes
and recordings that cross the next cue or closing fade.

Delivery tags guide expression; they do not supply exact silence durations.
Their response depends on the voice and model, as described in
[ElevenLabs' guidance](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices).

## Validation

- Mathematical projection, repulsion paths, lone-pair site selection, hybrid
  orthogonality, all 15 library molecules and 25 spoken numerical claims pass.
- Every narration beat passes the pace audit; tagged exports preserve the
  spoken words. All 242 separate clean/tagged text exports were checked.
- All 22 scenes pass individual timing checks at 30 fps, within one frame of
  their planned duration. The sum remains 1,680 seconds.
- All 22 scenes pass sampled text layout checks, including intermediate
  animation states and live model updates. This is a sampled check, not a
  proof about every rendered pixel.
- Synthetic audio checks verify cue offsets and rejection of missing, long,
  duplicate, unexpected and mixed recordings. Rigid half-turns and translucent
  sphere fades were also checked.
- Short 854×480, 15 fps motion samples were rendered and inspected for the
  water vector construction and closing composition. Dense structural scenes
  also have updated storyboard frames.

The full 1080p film and final cloned-voice recordings have not been rendered or
listened to in this review. Actual recordings still need `python main.py
audio-check` and an editorial listen against the picture.

## Review files

- [Water vectors — motion sample](output/review/scene_17_review.mp4)
- [Closing composition — motion sample](output/review/scene_20_review.mp4)
- [Water vectors — frame sheet](output/review/scene_17_motion_sheet.png)
- [Updated structural storyboards](output/review/final_storyboard/)
- [Tagged narration](narration_script_tagged.md)
- [Narration timing cues](narration_cues.md)
- [YouTube package](youtube_package.md) — 10 upload chapters, retaining all
  22 animation scenes.
