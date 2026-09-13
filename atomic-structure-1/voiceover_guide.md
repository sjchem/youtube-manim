# Voiceover production guide

Use `assets/narration/scene_01.txt` through `scene_15.txt` for separate generations,
or `assets/narration/full_narration.txt` for the complete text. These contain only
spoken narration. Regenerate them with `python utils/narration_export.py` whenever
the Markdown script changes.

The script uses complete sentences, contractions, paragraph breaks and only a
few ellipses. Numbers and the meaning of formulas are written as spoken words.
Keep the on-screen equations in the animation; do not paste LaTeX into TTS.

## Delivery

Aim for a calm, curious explanation. The planning windows average about 126
words per minute, including pauses. They are an editing target, not a voice
setting guaranteed to produce an exact duration.

- Scene 01: conversational opening; leave a short silence after “crash” and
  “Why doesn't this happen?” Deliver the promise warmly and directly. The promise
  is narration only; the viewer watches probes and detector flashes around an
  unresolved visual question, with no sentence cards to read.
- Scene 06: slow slightly at “Watch this one.” Let the backward turn register
  before explaining it. Do not add an excited delivery to every sentence.
- Scene 07: give “about five kilometres” room to land, then distinguish radius
  from diameter. Keep the size caveat conversational.
- Scenes 09–11: pause between observation, question and explanation. Give
  “four hundred and thirty-four nanometres” a clear, unhurried reading.
- Scene 14: leave a short pause after “That is our next mystery.” Finish with
  the next video promise; keep all the next video details in this scene.
- Scene 15: give the separate thank-you and subscription message the same warm
  voice as the story. Leave space for the closing card to settle.

## ElevenLabs handling

First generate a short sample using your chosen cloned voice and model. Listen
for pronunciation, natural sentence endings and whether the pauses fit your
animation. Use the same voice, model and settings for every scene.

Standard punctuation and text structure are a portable starting point. Eleven
v3 supports expressive audio tags and does not support SSML break tags; other
models have different pause handling. The supplied files deliberately contain
neither SSML nor model-specific stage directions. Check the current
[ElevenLabs guidance](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
before adding model-specific controls.

Pronunciation checks: Thomson (“TOM-sun”), Rutherford (“RUTH-er-furd”), Bohr
(“bore”), Geiger (“GUY-ger”), Marsden (“MARZ-dun”), cathode (“KATH-ohd”), anode
(“AN-ohd”), and nanometres (“NAN-oh-mee-ters”). These are listening notes, not
extra text to paste into the narration. Adjust for your own accent.

## Synchronization after generation

1. Export each scene with the matching number, for example
   `assets/audio/scene_07.wav`.
2. Measure the duration rather than assuming the TTS followed the word-rate
   estimate. For example:

   ```bash
   ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 assets/audio/scene_07.wav
   ```
3. Align paragraphs to visual beats in the editor. Adjust reading holds or
   animation timing where the voice needs more room. Do not stretch the whole
   spoken track just to fit an estimated window.
4. If scene windows change, update `config.py`, narration headings and YouTube
   chapters together, then run the narration export and timing checks again.
5. Listen to the final combined track across scene joins. Check that no word is
   clipped and that the surprise and cliffhanger pauses survive the edit.

The source does not automatically attach audio. No ElevenLabs request or paid
voice generation was made during this revision.
