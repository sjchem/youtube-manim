"""Export the spoken text, with no headings, for the whole film and each chapter.

`narration_script.md` is the single editable source. Everything under
`assets/narration/` is derived from it, and `--check` fails if the two have
drifted, which is what stops a recording session from being made against a
stale script.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NARRATION_DIR = PROJECT_ROOT / "assets/narration"

HEADING = re.compile(r"^## Scene (\d{2}) — (.*?) — (\d+):(\d{2})–(\d+):(\d{2})$", re.M)
WORD = re.compile(r"\b[\w']+\b")


def sections() -> list[dict]:
    """Every chapter's key, title, window in seconds, and spoken text."""
    script = (PROJECT_ROOT / "narration_script.md").read_text()
    headings = list(HEADING.finditer(script))
    chapters = []
    for index, heading in enumerate(headings):
        stop = headings[index + 1].start() if index + 1 < len(headings) else len(script)
        chapters.append(
            dict(
                key=heading[1],
                title=heading[2],
                start=int(heading[3]) * 60 + int(heading[4]),
                end=int(heading[5]) * 60 + int(heading[6]),
                text=script[heading.end():stop].strip(),
            )
        )
    return chapters


def export(check: bool = False) -> None:
    chapters = sections()
    expected = {f"scene_{chapter['key']}.txt": chapter["text"] + "\n" for chapter in chapters}
    expected["full_narration.txt"] = "\n\n".join(chapter["text"] for chapter in chapters) + "\n"

    NARRATION_DIR.mkdir(parents=True, exist_ok=True)
    if not check:
        for name, content in expected.items():
            (NARRATION_DIR / name).write_text(content)

    stale = [
        name for name, content in expected.items()
        if not (NARRATION_DIR / name).exists() or (NARRATION_DIR / name).read_text() != content
    ]
    if stale:
        raise AssertionError(f"Stale narration exports: {stale}")
    print(f"{len(chapters)} scene exports and full narration match")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail instead of rewriting")
    export(parser.parse_args().check)
