"""Check narration density against each authored chapter window."""

from __future__ import annotations

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
for _path in (str(PROJECT_ROOT), str(PROJECT_ROOT.parent)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import config as cfg  # noqa: E402

SCRIPT = PROJECT_ROOT / "narration_script.md"
HEADING = re.compile(
    r"^## Scene (?P<scene>\d{2}).*?—\s*(?P<start_m>\d+):(?P<start_s>\d{2})"
    r"–(?P<end_m>\d+):(?P<end_s>\d{2})",
    re.MULTILINE,
)
WORD = re.compile(r"\b[\w'+-]+\b")
# The closing card is scored, music, and a visual hold rather than teaching.
END_CARD = max(cfg.SCENE_DURATIONS)
MIN_RATE = 85.0
MAX_RATE = 112.0


def main() -> int:
    text = SCRIPT.read_text(encoding="utf-8")
    matches = list(HEADING.finditer(text))
    if not matches:
        print(f"No chapter headings found in {SCRIPT.name}")
        return 1

    print("Narration density audit")
    print("scene   words   window   delivery     status")
    failed = False
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end() : end]
        words = len(WORD.findall(body))
        start_seconds = int(match["start_m"]) * 60 + int(match["start_s"])
        end_seconds = int(match["end_m"]) * 60 + int(match["end_s"])
        duration = end_seconds - start_seconds

        authored = cfg.SCENE_DURATIONS.get(match["scene"])
        if authored is not None and abs(authored - duration) > 0.5:
            print(f"{match['scene']:>5}   window {duration}s disagrees with SCENE_DURATIONS ({authored:.0f}s)")
            failed = True

        rate = words * 60 / duration
        if match["scene"] == END_CARD:
            status = "END CARD"
        elif rate < MIN_RATE:
            status = "TOO SPARSE"
            failed = True
        elif rate > MAX_RATE:
            status = "TOO DENSE"
            failed = True
        else:
            status = "OK"
        print(f"{match['scene']:>5}   {words:>5}   {duration:>5}s   {rate:>6.1f} wpm   {status}")

    total = sum(cfg.SCENE_DURATIONS.values())
    minutes, seconds = divmod(int(total), 60)
    print(f"\nProgram total: {total:.0f}s ({minutes}:{seconds:02d})")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
