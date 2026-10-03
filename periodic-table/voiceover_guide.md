# Recording with your ElevenLabs voice

Use `assets/narration/scene_01.txt` through `scene_16.txt`. Each contains one continuous paragraph of spoken prose: no timestamps, speaker labels, animation instructions, or pause tags. `narration_script.md` is the readable master; `assets/narration/full_narration.txt` combines the scenes with blank lines between them.

Record one clip per scene using your own saved ElevenLabs voice. Aim for a curious, conversational delivery, roughly 130–145 words per minute, letting the questions and visual reveals breathe. The planned film lasts **22:43**, including transitions. Timing is a production target until the actual voice is recorded.

The spellings “one s”, “three d”, “n s two” and “n plus l” are intentional spoken forms. Read Z as “zee” or “zed” consistently; read l as “ell”. Superscripts are spoken electron counts, rather than mathematical powers. No API key or ElevenLabs account is required to export or preview the animation.

## From recording to render

1. Generate or record each continuous scene clip. Listen for element-name pronunciation and natural transitions between sentences.
2. Compare it with the same scene in `narration_cues.md`. Those times describe the intended visual reveals; they do not require a pause after every sentence. `assets/narration/cue_sheet.json` carries the same data for editing tools.
3. Save one file per scene in `assets/audio/`, named `scene_01.wav`, `scene_02.wav`, etc. MP3 and M4A are also accepted; keep only one format per scene.
4. Run `python main.py audio-check`. This checks missing files, duplicate formats, and clip lengths. It cannot verify word-level alignment.
5. Preview with `python main.py preview 06`. Available voice clips are automatically added at the start of their scenes, including in `FullVideo`.
6. Before the final render, align the important reveals to the voice. Adjust beat times in `narration.py` and scene durations in `config.py` when needed; then run `python -m utils.narration_export` and `python main.py check`.
7. Render with `python main.py render` after reviewing the voice and picture together.

Missing audio produces silent scenes so animation work can continue. A clip longer than its scene stops rendering with a clear error, preventing narration from spilling into the next chapter. Short clips leave time for visual pauses; a short clip still needs a listening check. Continuous TTS prose by itself does not guarantee synchronization with the authored cue times.

## Files to edit

Edit `narration.py`, then regenerate the prose and cues. The scene files use the same beat indices, so preserve each scene's beat count or update its choreography too. Keep explanatory detail in the narration; the screen should carry a diagram, a short label, or the equation currently being discussed.
