"""Sparse ElevenLabs v3/v4 delivery cues, separate from the spoken science.

Each anchor must occur exactly once in its scene. Put cues at sentence starts
so regenerated scripts keep continuous prose and never split a technical term.
Bracketed directions are performance suggestions, not exact timing controls.
See https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices
"""

from __future__ import annotations

# Shared opening delivery keeps the cloned narrator consistent across clips.
OPENING_TAG = "[warm, conversational delivery]"

# Unique text anchors make a script edit fail visibly if a cue needs updating.
DELIVERY_CUES: dict[str, list[tuple[str, str]]] = {
    "01": [
        ("It doesn't fall through.", "[short pause] [curious]"),
        ("But the Lewis structure says", "[thoughtful]"),
        ("So where are they hiding?", "[pause] [curious]"),
        ("One where electrons belong", "[warmly]"),
    ],
    "02": [
        ("But there is another way", "[short pause] [curious]"),
        ("Neither picture is simply wrong.", "[thoughtful]"),
    ],
    "03": [
        ("Now shift one", "[curious]"),
        ("Same two waves.", "[short pause] [warmly]"),
        ("Remember those two pictures:", "[short pause] [thoughtful]"),
    ],
    "04": [
        ("But be careful.", "[thoughtful]"),
        ("Not one. Not three. Two.", "[short pause] [warmly]"),
        ("This is an approximation.", "[thoughtful]"),
    ],
    "05": [
        ("Now bring them together out of phase.", "[curious]"),
        ("Density between the positive nuclei", "[short pause] [thoughtful]"),
        ("Shape is only half the story.", "[warmly]"),
    ],
    "06": [
        ("Here, the rise is a little larger", "[thoughtful]"),
        ("The valley means a bound hydrogen ion", "[warmly]"),
        ("Electrons in bonding orbitals", "[short pause] [thoughtful]"),
    ],
    "07": [
        ("Half a bond!", "[excited]"),
        ("And this isn't just bookkeeping.", "[thoughtful]"),
        ("So it doesn't always take", "[short pause] [warmly]"),
    ],
    "08": [
        ("And the data agree.", "[warmly]"),
        ("So far, more electrons", "[short pause] [curious]"),
    ],
    "09": [
        ("Bond order zero.", "[short pause] [surprised]"),
        ("Here's a test.", "[curious]"),
        ("One honest footnote.", "[short pause] [thoughtful]"),
    ],
    "10": [
        ("Now flip one phase", "[curious]"),
        ("What happens to the other two", "[short pause] [curious]"),
    ],
    "11": [
        ("Now the crucial part.", "[short pause] [thoughtful]"),
        ("Keep your eye on", "[softly]"),
    ],
    "12": [
        ("Count them.", "[warmly]"),
        ("Watch it in action.", "[curious]"),
        ("There is one more twist.", "[short pause] [thoughtful]"),
    ],
    "13": [
        ("Why would the order change?", "[curious]"),
        ("Let's drive the gap", "[warmly]"),
        ("This is a simplified picture.", "[short pause] [thoughtful]"),
    ],
    "14": [
        ("Ten electrons, every one", "[warmly]"),
        ("A triple bond, exactly", "[short pause] [warmly]"),
    ],
    "15": [
        ("Now the magnetic question.", "[curious]"),
        ("Nitrogen makes sense.", "[short pause] [thoughtful]"),
        ("Let's find those", "[softly]"),
    ],
    "16": [
        ("The magnet says otherwise.", "[thoughtful]"),
        ("Now let them in.", "[softly]"),
        ("Remember Hund's rule.", "[short pause] [softly]"),
        ("And the other doesn't pair", "[short pause] [softly]"),
        ("There they are.", "[long pause] [softly]"),
        ("Oxygen is paramagnetic,", "[warmly]"),
        ("The Lewis structure had no way", "[short pause] [warmly]"),
    ],
    "17": [
        ("And now the experiment makes sense.", "[short pause] [warmly]"),
        ("One fair note.", "[thoughtful]"),
        ("And it has one more surprise", "[short pause] [curious]"),
    ],
    "18": [
        ("The bond order went up.", "[surprised]"),
        ("It sounds backwards.", "[thoughtful]"),
        ("So what if we go the other way", "[short pause] [curious]"),
    ],
    "19": [
        ("Magnetism changes too.", "[thoughtful]"),
        ("Add an electron, and the bond", "[short pause] [warmly]"),
    ],
    "20": [
        ("Fluorine.", "[short pause]"),
        ("Line them up.", "[warmly]"),
    ],
    "21": [
        ("Take a few seconds.", "[softly]"),
        ("Look for lone arrows.", "[long pause] [warmly]"),
    ],
    "22": [
        ("What looked like a mystery", "[short pause] [warmly]"),
        ("Bonds aren't sticks.", "[pause] [thoughtful]"),
        ("And sometimes, they're", "[short pause] [playful]"),
    ],
    "23": [],
}
