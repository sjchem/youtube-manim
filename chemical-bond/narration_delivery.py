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
        ("And yet the atoms", "[thoughtful]"),
        ("Why don't they drift", "[curious]"),
        ("Yet all of them", "[short pause] [warmly]"),
    ],
    "02": [
        ("So what happens", "[curious]"),
        ("Instead, we will", "[warmly]"),
        ("And one idea", "[short pause] [thoughtful]"),
    ],
    "03": [
        ("Closer in, something", "[curious]"),
        ("Quantum mechanics adds", "[thoughtful]"),
        ("Tracking every force", "[warmly]"),
    ],
    "04": [
        ("Between the slope", "[thoughtful]"),
        ("Now let's give", "[curious]"),
        ("A bond is not a hook.", "[short pause] [thoughtful]"),
    ],
    "05": [
        ("Breaking the hydrogen bond", "[thoughtful]"),
        ("That surprises a lot", "[warmly]"),
        ("But what are the electrons", "[short pause] [curious]"),
    ],
    "06": [
        ("Gilbert Lewis had", "[warmly]"),
        ("Now look at a pattern.", "[curious]"),
        ("But careful.", "[short pause] [thoughtful]"),
    ],
    "07": [
        ("But remember what the dots", "[thoughtful]"),
        ("But atoms can share", "[warmly]"),
        ("But here is a puzzle.", "[short pause] [curious]"),
    ],
    "08": [
        ("Now turn the molecule", "[curious]"),
        ("A bond like this", "[thoughtful]"),
        ("But what if two p orbitals", "[curious]"),
    ],
    "09": [
        ("The result is a pi bond", "[thoughtful]"),
        ("Now we can read", "[warmly]"),
        ("What happens when one atom", "[short pause] [curious]"),
    ],
    "10": [
        ("But let's check the energy.", "[curious]"),
        ("It is uphill.", "[thoughtful]"),
        ("Here is the something else.", "[warmly]"),
    ],
    "11": [
        ("Pick one sodium ion.", "[curious]"),
        ("Sum the electrostatic attractions", "[thoughtful]"),
        ("Ionic bonding is not", "[short pause] [warmly]"),
    ],
    "12": [
        ("What lies in between?", "[curious]"),
        ("This is a polar covalent bond.", "[thoughtful]"),
        ("So there are not two separate boxes", "[short pause] [warmly]"),
    ],
    "13": [
        ("Delocalised means", "[thoughtful]"),
        ("Now hit the metal.", "[curious]"),
        ("Shared, transferred, or delocalised", "[warmly]"),
    ],
    "14": [
        ("Now compare carbon with carbon.", "[warmly]"),
        ("So is shorter always stronger?", "[short pause] [curious]"),
        ("For related bonds", "[thoughtful]"),
    ],
    "15": [
        ("But it is a pattern, not a law.", "[thoughtful]"),
        ("Yet liquid oxygen", "[curious]"),
        ("The octet rule is a useful shortcut.", "[warmly]"),
    ],
    "16": [
        ("They look completely different.", "[curious]"),
        ("Underneath every one", "[short pause] [thoughtful]"),
        ("That is the chemical bond.", "[warmly]"),
    ],
    "17": [
        ("So why is one straight", "[curious]"),
        ("To answer that", "[warmly]"),
        ("Next time:", "[short pause] [curious]"),
    ],
    "18": [],
}
