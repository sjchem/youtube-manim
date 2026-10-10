"""Export continuous voice text and separate editorial cue sheets from narration.py."""
from __future__ import annotations

import json
import config as cfg
from narration import SCRIPT, TITLES


def _stamp(seconds: float) -> str:
    minutes, rest = divmod(int(round(seconds)), 60)
    return f"{minutes:02d}:{rest:02d}"


def scene_text(key: str) -> str:
    """One continuous paragraph, without timestamps, directions or TTS pause tags."""
    return " ".join(line.strip() for _, line in SCRIPT[key])


def build_markdown() -> str:
    lines = [f"# Narration — {cfg.PROJECT_TITLE}", "",
             f"{cfg.PROJECT_PART}. Continuous prose for recording one clip per scene.",
             "Generated from `narration.py`; edit that source and run `python -m utils.narration_export`.",
             "Paste the matching plain-text scene file into ElevenLabs. Timing targets are in `narration_cues.md`.", ""]
    offset = 0.0
    for key, duration in cfg.SCENE_DURATIONS.items():
        lines += [f"## Scene {key} — {TITLES[key]} — {_stamp(offset)}–{_stamp(offset + duration)}",
                  "", scene_text(key), ""]
        offset += duration
    return "\n".join(lines)


def build_cues() -> tuple[str, dict]:
    lines = ["# Narration timing targets", "",
             "Editorial targets for matching the recorded voice to the animation. These are not instructions to insert silence between sentences.",
             "Continuous TTS output does not guarantee these timings. Compare the actual audio before the final render.", ""]
    manifest = {"planned_duration_seconds": sum(cfg.SCENE_DURATIONS.values()), "scenes": []}
    offset = 0.0
    for key, duration in cfg.SCENE_DURATIONS.items():
        lines += [f"## Scene {key} — {TITLES[key]}", "",
                  "| Beat | Scene time | Film time | Spoken text |", "|---|---|---|---|"]
        cues = []
        for index, (start, line) in enumerate(SCRIPT[key]):
            end = SCRIPT[key][index + 1][0] if index + 1 < len(SCRIPT[key]) else duration - cfg.TIMING['transition']
            lines.append(f"| {index + 1} | {_stamp(start)} | {_stamp(offset + start)} | {line} |")
            cues.append({"beat": index + 1, "start_seconds": start, "end_seconds": end, "text": line})
        lines.append("")
        manifest['scenes'].append({"key": key, "title": TITLES[key], "film_start_seconds": offset,
                                  "duration_seconds": duration, "text_file": f"scene_{key}.txt", "cues": cues})
        offset += duration
    return "\n".join(lines), manifest


def main() -> int:
    (cfg.PROJECT_ROOT / 'narration_script.md').write_text(build_markdown(), encoding='utf-8')
    cues, manifest = build_cues()
    (cfg.PROJECT_ROOT / 'narration_cues.md').write_text(cues, encoding='utf-8')
    folder = cfg.PROJECT_ROOT / 'assets' / 'narration'
    folder.mkdir(parents=True, exist_ok=True)
    for key in cfg.SCENE_DURATIONS:
        (folder / f'scene_{key}.txt').write_text(scene_text(key) + '\n', encoding='utf-8')
    (folder / 'full_narration.txt').write_text('\n\n'.join(scene_text(k) for k in cfg.SCENE_DURATIONS) + '\n', encoding='utf-8')
    (folder / 'cue_sheet.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print('Exported continuous scene text, full narration, and separate Markdown/JSON cue sheets.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
