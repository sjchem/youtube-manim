# Set theory revision: examples linked to mathematics

The current film has 14 chapters and a planned production runtime of **21:56**.
The pizza opening, fruit basket, animal habitats, platypus, topping orders,
number counters, kitchen shelf, and toy gate remain. Each worked example now
leads to its mathematical rule on a clear screen. Scene 12 connects the rules
with one arbitrary membership test before the pizza finale.

The teaching rhythm follows the local `permu-combi` project: show a choice,
build its result, then give the formula a readable moment. The main formulas
use MathTex at roughly 60–74 points. Prose stays in the local Arial substitute,
Nimbus Sans, with larger bold headings, captions and object names. Scene 1
retains the gold Nimbus Roman title and white question requested earlier.
The Oceanic Next theme and bubbles are unchanged.

## Current review files

- `output/pizza_story_visual_review.mp4`: all 14 chapters, accelerated and silent, 854×480 at 15 FPS, about 3:17. The four rendered groups were joined without re-encoding.
- `output/math_recap_720p.mp4`: Scene 12 at its planned 84-second pace, 1280×720 at 15 FPS.
- `output/pizza_hook.mp4`: Scene 1 at its planned 48-second pace, 1280×720 at 15 FPS.
- `output/math_visual_storyboard.pdf`: four-page comparison of an example and its rule in every chapter.
- `output/math_visual_overview.png`: the same 14-chapter comparison on one sheet.
- `output/math_storyboard/`: individual rendered stills for the current revision.
- `output/elevenlabs_narration.zip`: 14 continuous per-scene voiceover passages and pacing estimates.
- `output/math_validation.txt`: checks of the displayed mathematical rules.

The existing 480p and 2K commands in `README.md` still render all 14 original
class names and modules. A 2K production video was not rendered in this pass.
The source and documents from before this mathematics revision are saved at
`output/before_math_rebalance.zip`.

## Checks and limits

Every chapter passed the 30 FPS timing audit for the 21:56 schedule. The text
audit passed all chapters at animation endpoints and at 25%, 50%, and 75% of
transitions. Extra timing and layout passes covered the revised Scene 2, Scene
6, Scene 7, Scene 10, Scene 11, and Scene 12 transitions. Rendered stills were
inspected at both 1280×720 and 854×480, and frames sampled from the combined
review were checked. The combined review and math recap passed full FFmpeg
decode checks.

The union, intersection, complement, subset, and both De Morgan membership
rules passed 4,096 checks across all pairs of subsets of a four-element
universe. The displayed fruit, animal, topping, and number results also passed.

The narration master now has 2,644 spoken words. Pacing estimates use 135
words per minute and leave room for natural pauses; they are not measured
ElevenLabs audio. The videos are silent. Generate the user's cloned voice
clips, listen, and align animation cues to the recordings for a final narrated
render. The accelerated review is for visuals, not voice timing.
