"""Sparse ElevenLabs v3/v4 delivery cues, separate from the spoken science.

Each anchor must occur exactly once in its scene. Cues sit at sentence starts
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
        ("Yet the air inside", "[short pause]"),
        ("But that empty space", "[short pause] [emphasized]"),
        ("So what is doing", "[pause] [curious]"),
        ("How can random motion", "[short pause] [curious]"),
        ("This is The Molecular", "[pause] [warmly]"),
    ],
    "02": [
        ("Step back, and the", "[short pause]"),
        ("The gas laws describe", "[short pause] [emphasized]"),
        ("Let's begin with the", "[pause] [warmly]"),
    ],
    "03": [
        ("For water, these intermolecular", "[short pause] [emphasized]"),
        ("So where does an", "[pause] [curious]"),
    ],
    "04": [
        ("But the electrons are", "[short pause]"),
        ("Now bring a second", "[short pause] [curious]"),
        ("Look at the noble", "[pause]"),
    ],
    "05": [
        ("When two such molecules", "[short pause] [curious]"),
        ("But head to head,", "[short pause] [emphasized]"),
        ("They are not equally", "[short pause] [emphasized]"),
    ],
    "06": [
        ("Now a particularly important,", "[pause] [curious]"),
        ("The effect is dramatic.", "[short pause] [emphasized]"),
    ],
    "07": [
        ("But when their electron", "[short pause] [emphasized]"),
        ("The depth of the", "[pause] [curious]"),
    ],
    "08": [
        ("Average K equals three", "[short pause] [emphasized]"),
        ("Notice the word average.", "[short pause]"),
    ],
    "09": [
        ("Warm them, and the", "[short pause]"),
        ("Now give them far", "[short pause]"),
        ("But even then, something", "[pause] [curious]"),
    ],
    "10": [
        ("This is the turning", "[emphasized]"),
        ("Utterly tiny.", "[short pause] [curious]"),
    ],
    "11": [
        ("Now spread each spike", "[short pause]"),
        ("Faster molecules push harder,", "[short pause] [warmly]"),
    ],
    "12": [
        ("In real air, about", "[short pause] [emphasized]"),
        ("Pressure is not something", "[pause] [emphasized]"),
    ],
    "13": [
        ("Gather every velocity arrow", "[short pause]"),
        ("That one third is", "[short pause] [warmly]"),
    ],
    "14": [
        ("Substitute, and the two", "[short pause]"),
        ("P V equals n R T. The", "[pause] [emphasized]"),
        ("You won't be asked", "[pause] [warmly]"),
    ],
    "15": [
        ("Let's look inside.", "[short pause]"),
        ("Pressure rose, and no", "[short pause] [emphasized]"),
        ("And here's the hidden", "[pause] [curious]"),
    ],
    "16": [
        ("Pause and predict the", "[short pause]"),
        ("Half the volume, twice", "[short pause] [emphasized]"),
    ],
    "17": [
        ("You can feel this", "[short pause]"),
        ("One more warning.", "[pause]"),
        ("So before using any", "[short pause] [emphasized]"),
    ],
    "18": [
        ("Now heat the gas.", "[short pause]"),
        ("A hot air balloon", "[pause] [warmly]"),
    ],
    "19": [
        ("They all meet at", "[short pause] [emphasized]"),
        ("One caution.", "[pause]"),
    ],
    "20": [
        ("What is the new", "[short pause] [curious]"),
        ("Now a trap.", "[pause]"),
        ("But the volume grows", "[short pause] [emphasized]"),
    ],
    "21": [
        ("Now heat it.", "[short pause]"),
        ("More momentum per hit,", "[short pause] [emphasized]"),
        ("A sealed, rigid gas", "[pause]"),
    ],
    "22": [
        ("One microscopic change.", "[short pause] [emphasized]"),
        ("Car tyres show this,", "[pause]"),
    ],
    "23": [
        ("Double the molecules, double", "[short pause] [emphasized]"),
        ("You see a related", "[pause] [warmly]"),
    ],
    "24": [
        ("Equal volumes of ideal", "[short pause] [emphasized]"),
        ("You may have seen", "[pause]"),
    ],
    "25": [
        ("P V equals n R T. The", "[short pause] [emphasized]"),
        ("Now picture every state", "[pause] [curious]"),
        ("The four laws were", "[pause] [warmly]"),
    ],
    "26": [
        ("A weather balloon holds", "[pause] [curious]"),
    ],
    "27": [
        ("Turn it around,", "[short pause] [curious]"),
        ("But remember what this", "[pause] [emphasized]"),
    ],
    "28": [
        ("How does each gas", "[short pause] [curious]"),
        ("Try it.", "[pause]"),
        ("Back to the mountain.", "[pause] [warmly]"),
    ],
    "29": [
        ("The gas in the", "[short pause]"),
    ],
    "30": [
        ("But our model hides", "[pause] [emphasized]"),
        ("So what happens when", "[pause] [curious]"),
    ],
    "31": [
        ("Thanks for watching.", "[warmly]"),
    ],
}
