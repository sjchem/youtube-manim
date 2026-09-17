"""Export clean per-scene narration and report pacing or local audio duration."""

from __future__ import annotations

import argparse
import re
import subprocess

import config as cfg


def read_narration(source: str) -> list[tuple[str, str]]:
    """Validate chapter ranges and return only continuous, speakable text."""
    sections = re.findall(
        r"^## Scene (\d{2})([^\n]*)\n(.*?)(?=^## Scene |\Z)", source, re.M | re.S,
    )
    if [key for key, _, _ in sections] != list(cfg.SCENE_DURATIONS):
        raise ValueError("Narration chapters must match SCENE_DURATIONS in order")
    elapsed = 0
    result = []
    for key, heading, body in sections:
        times = re.search(r"\((\d+):(\d{2})\s*[–-]\s*(\d+):(\d{2})\)", heading)
        if not times:
            raise ValueError(f"Scene {key} needs a (MM:SS – MM:SS) recording range")
        start_m, start_s, end_m, end_s = map(int, times.groups())
        duration = cfg.SCENE_DURATIONS[key]
        if (start_s >= 60 or end_s >= 60 or start_m * 60 + start_s != elapsed
                or end_m * 60 + end_s != elapsed + duration):
            raise ValueError(f"Scene {key} timestamps do not match its animation budget")
        body = body.strip()
        if not body or re.search(r"\d+:\d{2}|^\s*(?:#|>|---)|\*\*|`", body, re.M):
            raise ValueError(f"Scene {key} must contain spoken prose without timestamps or markup")
        # Line wrapping in Markdown must never become pauses or TTS instructions.
        result.append((key, " ".join(body.split()) + "\n"))
        elapsed += duration
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check existing exports without rewriting")
    args = parser.parse_args()
    root = cfg.PROJECT_ROOT
    source = (root / "narration_script.md").read_text()
    sections = read_narration(source)
    directory = root / "assets/audio/scripts"
    if not args.check:
        directory.mkdir(parents=True, exist_ok=True)
    failed = False
    elapsed = 0
    print("Scene      Start  Target  Words  Words/min  Local audio")
    for key, body in sections:
        path = directory / f"scene_{key}.txt"
        if args.check:
            if not path.exists() or path.read_text() != body:
                print(f"STALE: {path}")
                failed = True
        else:
            path.write_text(body)
        words = len(re.sub(r"[*_`\[\]()#>]|\d+:\d+", " ", body).split())
        duration = cfg.SCENE_DURATIONS[key]
        audio = next(
            (
                root / "assets/audio" / f"scene_{key}{suffix}"
                for suffix in (".wav", ".mp3", ".m4a")
                if (root / "assets/audio" / f"scene_{key}{suffix}").exists()
            ),
            None,
        )
        audio_note = "not supplied"
        if audio:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(audio)],
                capture_output=True, text=True, check=True,
            )
            actual = float(result.stdout)
            audio_note = f"{actual:.1f}s ({duration - actual:+.1f}s room)"
            if actual > duration:
                failed = True
                audio_note += " TOO LONG"
        rate = words * 60 / duration
        flag = "" if 110 <= rate <= 165 else "  <- check pace"
        print(
            f"scene_{key}  {elapsed // 60:02d}:{elapsed % 60:02d}  {duration:5.0f}s  "
            f"{words:5d}  {rate:9.0f}{flag}  {audio_note}"
        )
        elapsed += int(duration)
    total = sum(cfg.SCENE_DURATIONS.values())
    print(f"\nProgramme: {total:.0f}s ({int(total) // 60}:{int(total) % 60:02d})")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
