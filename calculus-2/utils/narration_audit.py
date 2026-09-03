"""Check narration density against each authored chapter window."""

from __future__ import annotations

import re
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "narration_script.md"
HEADING = re.compile(
    r"^## Scene (?P<scene>\d{2}).*?—\s*(?P<start_m>\d+):(?P<start_s>\d{2})"
    r"–(?P<end_m>\d+):(?P<end_s>\d{2})",
    re.MULTILINE,
)
WORD = re.compile(r"\b[\w'+-]+\b")


def main() -> int:
    text = SCRIPT.read_text(encoding="utf-8")
    matches = list(HEADING.finditer(text))
    print("Narration density audit")
    print("scene   words   window   delivery   status")
    failed = False
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end() : end]
        words = len(WORD.findall(body))
        start_seconds = int(match["start_m"]) * 60 + int(match["start_s"])
        end_seconds = int(match["end_m"]) * 60 + int(match["end_s"])
        duration = end_seconds - start_seconds
        rate = words * 60 / duration
        # The subscribe card intentionally leaves room for music and the final
        # visual hold.  Spoken teaching chapters should stay accessible.
        if match["scene"] == "14":
            status = "END CARD"
        elif rate < 85:
            status = "TOO SPARSE"
            failed = True
        elif rate > 112:
            status = "TOO DENSE"
            failed = True
        else:
            status = "OK"
        print(f"{match['scene']:>5}   {words:>5}   {duration:>5}s   {rate:>6.1f} wpm   {status}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
