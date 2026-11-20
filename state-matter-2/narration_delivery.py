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
        ("But there is a problem.", "[pause] [emphasized]"),
        ("Keep squeezing, and", "[short pause]"),
        ("Droplets appear.", "[short pause] [curious]"),
        ("So the equation is", "[pause]"),
        ("This is Beyond Ideal", "[pause] [warmly]"),
    ],
    "02": [
        ("First, a surprise", "[short pause]"),
        ("Every step uses the", "[pause] [warmly]"),
    ],
    "03": [
        ("They collide.", "[short pause]"),
        ("But look at the", "[short pause] [curious]"),
        ("No molecule keeps one", "[pause]"),
    ],
    "04": [
        ("Now let them collide.", "[short pause]"),
        ("Then something remarkable happens.", "[pause] [curious]"),
        ("This is the central", "[short pause] [emphasized]"),
        ("One caution.", "[pause]"),
    ],
    "05": [
        ("Near the centre, the", "[short pause]"),
        ("Make the shell bigger.", "[short pause]"),
        ("A growing shell times", "[pause] [emphasized]"),
        ("You don't need to", "[short pause] [warmly]"),
    ],
    "06": [
        ("The peak is the", "[short pause]"),
        ("Why this order?", "[pause] [curious]"),
        ("One detail.", "[pause]"),
    ],
    "07": [
        ("The whole curve shifts", "[short pause]"),
        ("Speed grows as the", "[short pause] [emphasized]"),
        ("Mass matters too.", "[pause]"),
    ],
    "08": [
        ("One. A gas", "[short pause]"),
        ("Together, these rules lead", "[pause] [emphasized]"),
    ],
    "09": [
        ("But squeeze the gas", "[short pause]"),
        ("But bring them closer,", "[short pause]"),
        ("So the ideal gas", "[pause] [emphasized]"),
    ],
    "10": [
        ("Now follow one molecule", "[short pause]"),
        ("This is called a", "[short pause] [emphasized]"),
        ("The picture of a", "[pause]"),
    ],
    "11": [
        ("Now squeeze both boxes.", "[short pause]"),
        ("With less free room,", "[short pause]"),
        ("When size and repulsion", "[pause] [emphasized]"),
    ],
    "12": [
        ("At low pressure, the", "[short pause]"),
        ("Temperature matters too.", "[pause]"),
        ("Quick check.", "[pause] [curious]"),
        ("Attraction.", "[long pause] [emphasized]"),
    ],
    "13": [
        ("First, attraction.", "[short pause]"),
        ("Now double the density.", "[short pause] [curious]"),
        ("This correction is an", "[pause]"),
    ],
    "14": [
        ("Picture two molecules as", "[short pause]"),
        ("Around each molecule there", "[short pause] [emphasized]"),
        ("Notice what this means.", "[pause]"),
    ],
    "15": [
        ("The result is the", "[short pause] [emphasized]"),
        ("Let's test it.", "[pause]"),
        ("Now give the same", "[pause]"),
        ("The ideal gas equation is", "[pause] [warmly]"),
    ],
    "16": [
        ("For an ideal gas,", "[short pause]"),
        ("Here is Z against", "[pause]"),
        ("Z also has a", "[pause]"),
    ],
    "17": [
        ("At one special temperature,", "[pause] [curious]"),
        ("Every gas has its", "[short pause]"),
        ("One warning.", "[pause]"),
    ],
    "18": [
        ("Then, at a certain", "[short pause] [curious]"),
        ("Keep squeezing.", "[short pause]"),
        ("Why doesn't the pressure", "[pause]"),
        ("One substance, one temperature,", "[pause] [emphasized]"),
    ],
    "19": [
        ("At about thirty-one degrees", "[short pause] [emphasized]"),
        ("Watch a sealed tube", "[pause]"),
        ("At the critical point,", "[short pause]"),
    ],
    "20": [
        ("But below a certain", "[short pause] [curious]"),
        ("Replace the wiggle with", "[pause]"),
        ("So an equation built", "[pause] [emphasized]"),
    ],
    "21": [
        ("The two edges of that", "[short pause]"),
        ("But there is another", "[pause] [curious]"),
        ("We end up with", "[short pause]"),
        ("Gas and liquid are", "[pause] [emphasized]"),
        ("So keep three ideas", "[pause]"),
    ],
    "22": [
        ("Every gas has a", "[short pause]"),
        ("Nitrogen's is about", "[pause]"),
        ("For otherwise comparable molecules,", "[pause] [emphasized]"),
    ],
    "23": [
        ("Remember the speed distribution.", "[short pause]"),
        ("Eventually, the two rates", "[pause]"),
        ("Warm the liquid.", "[pause]"),
    ],
    "24": [
        ("Evaporation happens at the", "[short pause]"),
        ("Lower the outside pressure,", "[pause]"),
        ("Raise the pressure,", "[short pause]"),
        ("And in a rigid sealed", "[pause] [curious]"),
    ],
    "25": [
        ("A molecule at the", "[short pause]"),
        ("Surface tension can also", "[pause]"),
        ("You may have heard", "[pause] [warmly]"),
    ],
    "26": [
        ("Reshape a cube of", "[short pause]"),
        ("Mercury does the opposite.", "[short pause]"),
        ("Follow water all the", "[pause] [curious]"),
        ("Of course:", "[short pause] [emphasized]"),
    ],
    "27": [
        ("Trap a liquid between", "[short pause]"),
        ("Neighbouring layers exchange momentum.", "[pause]"),
        ("Eta is the viscosity.", "[short pause]"),
    ],
    "28": [
        ("In water, it plunges.", "[short pause]"),
        ("Warm a liquid, and", "[pause]"),
        ("One famous myth deserves", "[pause] [curious]"),
        ("It isn't.", "[short pause] [emphasized]"),
    ],
    "29": [
        ("But real molecules are", "[short pause]"),
        ("They explain why real", "[pause]"),
        ("The molecules never turned", "[pause] [warmly]"),
        ("That is the chemistry", "[long pause] [warmly]"),
    ],
    "30": [
        ("Thanks for watching.", "[warmly]"),
    ],
}
