"""Export clean and performance-tagged prose, plus separate editorial cues."""
from __future__ import annotations

import argparse
import json
import re
import config as cfg
from narration import SCRIPT, TITLES
from narration_delivery import DELIVERY_CUES, OPENING_TAG
from utils.narration_audit import VOICE_RATE, words


def _stamp(seconds: float) -> str:
    minutes, rest = divmod(int(round(seconds)), 60)
    return f"{minutes:02d}:{rest:02d}"


def scene_text(key: str) -> str:
    """One continuous paragraph, without timestamps, directions or TTS pause tags."""
    return " ".join(line.strip() for _, line in SCRIPT[key])


def tagged_beat_text(key: str, line: str) -> str:
    """Preserve the scene delivery cues in separately recorded beat text."""
    for anchor, tags in DELIVERY_CUES[key]:
        if anchor in line:
            line = line.replace(anchor, f"{tags} {anchor}", 1)
    return f"{OPENING_TAG} {line}"


def tagged_scene_text(key: str) -> str:
    """Add sparse delivery cues without changing any spoken words."""
    text = scene_text(key)
    for anchor, tags in DELIVERY_CUES[key]:
        if text.count(anchor) != 1:
            raise ValueError(f"Scene {key}: delivery anchor must occur once: {anchor!r}")
        text = text.replace(anchor, f"{tags} {anchor}", 1)
    text = f"{OPENING_TAG} {text}"
    restored = " ".join(re.sub(r"\[[^\]]+\]", "", text).split())
    if restored != scene_text(key):
        raise ValueError(f"Scene {key}: delivery tags changed the spoken text")
    return text


def build_markdown(*, tagged: bool = False) -> str:
    label = "Narration with voice tags" if tagged else "Narration"
    lines = [f"# {label} — {cfg.PROJECT_TITLE}", "",
             f"{cfg.PROJECT_PART}. Continuous prose for recording one clip per scene.",
             "Generated from `narration.py` and `narration_delivery.py`; run `python -m utils.narration_export` after edits."]
    if tagged:
        lines += [
            "For ElevenLabs v3/v4: paste only the scene paragraph, or use `assets/narration/elevenlabs/scene_XX.txt`.",
            "Square brackets guide vocal delivery; they are not spoken words. Keep a warm, clear documentary tone.",
            "`[short pause]` marks an occasional thinking beat, not a timed silence. Other punctuation supplies the natural rhythm.",
            "Tag response varies with the selected model and cloned voice. For models without audio-tag support, use [the clean script](narration_script.md).",
            "Generate a scene clip with editorial pauses, or use `python -m utils.narration_export --beats` for cue-aligned beat recordings. Tags do not supply exact timing.",
            "Audio-tag syntax: [ElevenLabs documentation](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices).",
        ]
    else:
        lines += [
            "For expressive cloned-voice generation, use [the tagged script](narration_script_tagged.md) or `assets/narration/elevenlabs/scene_XX.txt` (ElevenLabs v3/v4).",
            "The plain-text files directly inside `assets/narration/` contain clean prose. Timing targets are in `narration_cues.md`.",
        ]
    lines.append("")
    offset = 0.0
    for key, duration in cfg.SCENE_DURATIONS.items():
        lines += [f"## Scene {key} — {TITLES[key]} — {_stamp(offset)}–{_stamp(offset + duration)}",
                  "", tagged_scene_text(key) if tagged else scene_text(key), ""]
        offset += duration
    return "\n".join(lines)


def build_cues() -> tuple[str, dict]:
    lines = ["# Narration timing targets", "",
             "Editorial targets for matching the recorded voice to the animation. At ~100 words per 35 seconds, allow the remaining beat window for looking, movement and breathing.",
             "Target 140–150 spoken words per finished minute; dense orbital views and prediction time use less. At the measured voice pace, the remaining time is deliberately distributed after the corresponding narration beats.",
             "Continuous TTS output and pause tags do not guarantee these timings. Hold the current visual after each beat for the suggested pause; measure the real audio before the final render.", ""]
    manifest = {"voice_words_per_second": VOICE_RATE, "planned_duration_seconds": sum(cfg.SCENE_DURATIONS.values()), "scenes": []}
    offset = 0.0
    for key, duration in cfg.SCENE_DURATIONS.items():
        count = sum(words(line) for _, line in SCRIPT[key])
        speech = count / VOICE_RATE
        lines += [f"## Scene {key} — {TITLES[key]} — {_stamp(offset)}–{_stamp(offset + duration)}", "",
                  f"**{count} words · est. speech {speech:.0f}s · visual pauses and closing fade "
                  f"{duration - speech:.0f}s · scene {duration:.0f}s** ({60 * count / duration:.0f} words per minute)", "",
                  "| Beat | Scene time | Film time | Est. speech | Visual pause | Spoken text |", "|---|---|---|---|---|---|"]
        cues = []
        for index, (start, line) in enumerate(SCRIPT[key]):
            end = SCRIPT[key][index + 1][0] if index + 1 < len(SCRIPT[key]) else duration - cfg.TIMING['transition']
            spoken = words(line) / VOICE_RATE
            pause = end - start - spoken
            lines.append(f"| {index + 1} | {_stamp(start)} | {_stamp(offset + start)} | {spoken:.1f}s | {pause:.1f}s | {line} |")
            cues.append({"beat": index + 1, "start_seconds": start, "end_seconds": end,
                         "estimated_speech_seconds": round(spoken, 3), "estimated_visual_pause_seconds": round(pause, 3),
                         "suggested_pause_start_seconds": round(start + spoken, 3),
                         "pause_instruction": "Hold the current visual after this beat; adjust to the actual recording.",
                         "audio_stem": f"scene_{key}/beat_{index + 1:03d}",
                         "text": line, "tagged_text": tagged_beat_text(key, line)})
        lines.append("")
        manifest['scenes'].append({"key": key, "title": TITLES[key], "film_start_seconds": offset,
                                  "duration_seconds": duration, "text_file": f"scene_{key}.txt", "word_count": count,
                                  "words_per_finished_minute": round(60 * count / duration, 1),
                                  "estimated_speech_seconds": round(speech, 3),
                                  "estimated_visual_pause_seconds": round(duration - speech, 3), "cues": cues})
        offset += duration
    return "\n".join(lines), manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--beats', action='store_true', help='Also export separate clean/tagged text for each cue')
    args = parser.parse_args()
    if set(DELIVERY_CUES) != set(cfg.SCENE_DURATIONS):
        raise ValueError("Delivery cues must cover exactly the configured scenes")
    # Validate every anchor before writing any export.
    tagged_text = {key: tagged_scene_text(key) for key in cfg.SCENE_DURATIONS}
    (cfg.PROJECT_ROOT / 'narration_script.md').write_text(build_markdown(), encoding='utf-8')
    (cfg.PROJECT_ROOT / 'narration_script_tagged.md').write_text(build_markdown(tagged=True), encoding='utf-8')
    cues, manifest = build_cues()
    (cfg.PROJECT_ROOT / 'narration_cues.md').write_text(cues, encoding='utf-8')
    folder = cfg.PROJECT_ROOT / 'assets' / 'narration'
    folder.mkdir(parents=True, exist_ok=True)
    tagged_folder = folder / 'elevenlabs'
    tagged_folder.mkdir(parents=True, exist_ok=True)
    for key in cfg.SCENE_DURATIONS:
        (folder / f'scene_{key}.txt').write_text(scene_text(key) + '\n', encoding='utf-8')
        (tagged_folder / f'scene_{key}.txt').write_text(tagged_text[key] + '\n', encoding='utf-8')
    (folder / 'full_narration.txt').write_text('\n\n'.join(scene_text(k) for k in cfg.SCENE_DURATIONS) + '\n', encoding='utf-8')
    (tagged_folder / 'full_narration.txt').write_text('\n\n'.join(tagged_text.values()) + '\n', encoding='utf-8')
    if args.beats:
        for key, beats in SCRIPT.items():
            clean_dir = folder / 'beats' / f'scene_{key}'
            tagged_dir = tagged_folder / 'beats' / f'scene_{key}'
            clean_dir.mkdir(parents=True, exist_ok=True)
            tagged_dir.mkdir(parents=True, exist_ok=True)
            for index, (_, line) in enumerate(beats, 1):
                (clean_dir / f'beat_{index:03d}.txt').write_text(line + '\n', encoding='utf-8')
                (tagged_dir / f'beat_{index:03d}.txt').write_text(tagged_beat_text(key, line) + '\n', encoding='utf-8')
    (folder / 'cue_sheet.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print('Exported clean and ElevenLabs-tagged narration for all scenes, plus Markdown/JSON cue sheets.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
