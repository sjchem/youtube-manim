"""Narration source: continuous spoken prose, cut into visual beats.

Each beat is ``(spoken text, visual hold in seconds)``. A beat's window is the
time its words take at ``PACE`` words per second (a little slower than the
narrator's natural ~2.86 words per second, so the voice never races the
picture), plus the hold: extra seconds for a 3D move, a derivation step or a
prediction countdown. Beat start times and scene lengths are *derived* from
these windows, so ``config.SCENE_DURATIONS`` always matches the script.

Scenes hold on a beat with ``common.beat(scene, t, i)``. Export joins the prose
for a voice recording and writes cue sheets separately
(``python -m utils.narration_export``).

Every number spoken here is checked against the model by
``python -m utils.gas_data`` — change a value in ``utils/physics_models.py``
and the check names the line that no longer agrees.

Spelling for the cloned voice: numbers are written out in words, symbols as
they are read aloud ("P V equals n R T", "k B T", "v x squared").
"""

from __future__ import annotations

import re

PACE = 2.6            # words per second used to size each beat's window
TRANSITION = 0.55     # closing fade of every scene, seconds
_WORD = re.compile(r"[A-Za-z0-9']+")


def words(line: str) -> int:
    return len(_WORD.findall(line))


TITLES: dict[str, str] = {}
SCRIPT: dict[str, list[tuple[float, str]]] = {}
HOLDS: dict[str, list[float]] = {}
DURATIONS: dict[str, float] = {}


def _scene(key: str, title: str, beats: list[tuple[str, float]]) -> None:
    TITLES[key] = title
    t = 0.0
    out: list[tuple[float, str]] = []
    for text, hold in beats:
        out.append((round(t, 1), text))
        t = round(t, 1) + words(text) / PACE + hold
    SCRIPT[key] = out
    HOLDS[key] = [hold for _, hold in beats]
    DURATIONS[key] = round(t + TRANSITION, 1)


# ---------------------------------------------------------------------------
# Chapter 1 — The invisible world of gases
# ---------------------------------------------------------------------------

_scene("01", "The invisible crowd", [
    ("Blow into a balloon, and it swells. Pump up a bicycle tyre, and it turns hard enough to carry your weight.", 1.8),
    ("Yet the air inside looks like nothing at all. No colour. Almost no weight. Just empty space.", 1.2),
    ("But that empty space is pushing. Near sea level, the pressure force on one square metre equals the weight of about ten tonnes. Opposite sides usually balance; a pressure difference gives the net push.", 2.0),
    ("So what is doing the pushing? Imagine shrinking yourself millions of times, and stepping inside.", 2.2),
    ("You would not find a smooth, continuous substance. You would find a crowd: countless molecules, each one moving in a straight line until it strikes something, and then flying off in a new direction.", 2.0),
    ("Many of them strike the walls. And every strike is a tiny push.", 2.0),
    ("One push is far too small to feel. But there are so many molecules, striking so often, that together they can hold up a car.", 1.8),
    ("None of these molecules knows Boyle's law, or the ideal gas equation. Yet together, they obey those laws with remarkable precision.", 1.6),
    ("How can random motion produce such predictable behaviour?", 1.8),
    ("This is The Molecular Dance.", 5.0),
])

_scene("02", "Random parts, a precise whole", [
    ("Here is the puzzle at the heart of this lesson.", 0.8),
    ("Up close, everything looks random. Follow one molecule: repeated collisions change its direction. Tracking every molecule in a real gas is impractical.", 2.5),
    ("Step back, and the randomness disappears. The pressure gauge holds steady. So does the thermometer. Pressure, volume and temperature can be measured, and predicted.", 2.0),
    ("The same thing happens with a crowd of people. You can't predict where one person in a busy station will walk next. But you can predict how many will pass through the gates each minute.", 1.6),
    ("The gas laws describe the crowd, not the individual.", 1.4),
    ("To understand them, we will follow one chain of reasoning, in four questions. What holds molecules together, and what lets them separate? Why does a gas push on its container? Why do pressure, volume and temperature follow simple rules? And can one equation explain them all?", 3.0),
    ("Let's begin with the forces between molecules.", 1.5),
])

# ---------------------------------------------------------------------------
# Chapter 2 — Intermolecular forces
# ---------------------------------------------------------------------------

_scene("03", "Inside versus between", [
    ("Start with a single water molecule.", 1.2),
    ("Its oxygen and two hydrogens are held together by covalent bonds. These are forces inside the molecule: intramolecular forces.", 1.6),
    ("But a glass of water holds trillions of trillions of molecules, and they cling to one another. Forces between molecules are called intermolecular forces.", 2.2),
    ("For water, these intermolecular links are much weaker. Breaking an O H bond inside water takes about four hundred and sixty kilojoules per mole. A typical attraction between neighbouring water molecules is only about twenty.", 2.4),
    ("Boiling water doesn't break water molecules apart. It only pulls whole molecules away from their neighbours.", 2.2),
    ("So where does an attraction between neutral molecules come from? There are several mechanisms. And the simplest one works even for atoms with no polarity at all.", 1.2),
])

_scene("04", "London dispersion forces", [
    ("Take a helium atom. On average, its electron cloud is perfectly symmetrical around the nucleus.", 1.2),
    ("But the electrons are always moving. At any instant, the cloud may be a little lopsided, with slightly more charge on one side.", 2.0),
    ("That makes a temporary dipole: one end slightly negative, the other slightly positive.", 1.4),
    ("Now bring a second atom nearby. The temporary dipole pushes the neighbour's electrons away from its negative end. The neighbour becomes a dipole too, an induced dipole, lined up to attract.", 2.2),
    ("The flicker keeps changing direction, but the neighbour follows it, so the attraction never averages away. This is the London dispersion force.", 2.0),
    ("It is short ranged. The interaction energy falls roughly as one over r to the sixth. Double the distance, and the magnitude of that energy drops about sixty-four times.", 2.6),
    ("And it grows with the size of the electron cloud. Bigger clouds are easier to distort: they are more polarizable.", 1.4),
    ("Look at the noble gases. Helium boils at about four kelvin. Xenon, with its far larger cloud, boils at about one hundred and sixty-five.", 2.6),
    ("Dispersion acts between every pair of atoms and molecules, polar or not.", 1.5),
])

_scene("05", "Permanent dipoles", [
    ("Some molecules carry a dipole all the time. In hydrogen chloride, chlorine pulls the shared electrons toward itself.", 1.4),
    ("The chlorine end is slightly negative, and the hydrogen end slightly positive. A permanent dipole.", 1.4),
    ("When two such molecules meet, orientation matters.", 0.8),
    ("Head to tail, opposite charges are closest, and they attract.", 1.6),
    ("Side by side and pointing opposite ways, they attract too, more weakly.", 1.6),
    ("But head to head, like charges face each other, and they repel.", 1.8),
    ("For fixed orientations, this interaction energy falls off as one over r cubed, and its sign depends on the angles. Notice that this is an energy, not a force.", 2.0),
    ("In a gas, though, molecules tumble constantly. If every orientation were equally likely, attraction and repulsion would cancel exactly.", 2.2),
    ("They are not equally likely. Attractive orientations have lower energy, so thermal motion visits them a little more often. The average comes out attractive.", 2.6),
    ("And this averaged attraction falls off as one over r to the sixth, the same distance law as dispersion.", 2.0),
])

_scene("06", "Induced dipoles and hydrogen bonds", [
    ("A permanent dipole can also act on a molecule that has none.", 0.8),
    ("Bring hydrogen chloride near an argon atom. The dipole's charges distort argon's electron cloud, and create an induced dipole, aligned to attract.", 2.2),
    ("This dipole induced dipole attraction also falls off as one over r to the sixth.", 1.4),
    ("Now a particularly important, directional attraction: the hydrogen bond.", 1.0),
    ("When hydrogen is bonded to a very electronegative atom, such as oxygen, nitrogen or fluorine, electron density shifts away from hydrogen. It carries a partial positive charge, not a full positive charge.", 1.8),
    ("That spot is drawn to a lone pair on a neighbouring molecule. In water, each molecule can join up to four of these links, building a shifting three dimensional network.", 3.0),
    ("Ammonia forms them too, through the lone pair on its nitrogen.", 1.8),
    ("The effect is dramatic. Hydrogen sulfide, a heavier molecule with a similar shape, boils at about minus sixty degrees Celsius. Water, with its hydrogen bonds, boils at one hundred.", 2.6),
    ("Hydrogen bonds hold liquid water together, and explain many of its unusual properties.", 1.6),
])

_scene("07", "Too close: repulsion", [
    ("If molecules attract, why don't they simply collapse into one another?", 1.0),
    ("Push two atoms closer and closer. At first, the attraction grows.", 1.8),
    ("But when their electron clouds begin to overlap, a fierce repulsion takes over. The electrons resist being squeezed into the same space, and the nuclei repel each other too.", 1.8),
    ("Put attraction and repulsion together, and you get the full interaction energy: a steep wall, a well, and a long, shallow tail.", 2.4),
    ("A common model is the Lennard-Jones curve. Its repulsive term rises as one over r to the twelfth. Its attractive term falls as one over r to the sixth.", 2.0),
    ("At the bottom of the well is the distance where the two are balanced. That is where neighbours in a liquid or a solid tend to settle.", 2.0),
    ("The depth of the well tells us how strongly molecules hold on to each other. So if they attract, why doesn't every gas collapse into a liquid?", 2.2),
])

# ---------------------------------------------------------------------------
# Chapter 3 — Thermal energy versus intermolecular attraction
# ---------------------------------------------------------------------------

_scene("08", "Thermal motion", [
    ("Because molecules never sit still.", 1.0),
    ("Gas particles move continuously. Molecules can also rotate and vibrate. Here, we focus on their translational motion through the container.", 1.4),
    ("Temperature is related to average energy per particle, rather than the total energy of the sample. For a classical ideal gas, average translational kinetic energy is proportional to absolute temperature.", 1.4),
    ("Average K equals three halves k B T.", 2.4),
    ("Here k B is the Boltzmann constant, about one point three eight times ten to the minus twenty-three joules per kelvin, and T is measured in kelvin.", 1.8),
    ("Notice the word average. At any instant, some molecules are slow and some are fast. Temperature describes the whole distribution, not any one molecule.", 2.2),
    ("Heat the gas, and the whole distribution shifts to higher speeds.", 2.6),
    ("At room temperature, the average is tiny: about six times ten to the minus twenty-one joules per molecule. But per mole, the thermal energy scale, R T, is about two and a half kilojoules.", 2.2),
])

_scene("09", "The tug of war", [
    ("So two effects compete. Attractions pull molecules together. Thermal motion shakes them apart.", 1.6),
    ("Watch sixty-one atoms that attract each other, in a real, two dimensional simulation.", 1.4),
    ("When the thermal energy is small compared with the depth of the well, they lock into a crystal. Each atom only vibrates about its place. A solid.", 3.0),
    ("Warm them, and the atoms begin to slip past one another, while still holding together. A liquid.", 3.4),
    ("Now give them far more energy than the well can hold. The atoms fly apart and fill the whole container. A gas.", 3.6),
    ("The state of matter depends on this balance between intermolecular attraction and thermal energy, together with the pressure.", 1.6),
    ("Argon's well is only about one kilojoule per mole deep, less than half of R T at room temperature. That's why argon is a gas in this room, and turns liquid only near eighty-seven kelvin.", 2.2),
    ("In a dilute gas, molecules are far apart and spend almost all their time flying freely. So as a first approximation, we ignore their attractions entirely and treat them as tiny points. That's the ideal gas model.", 1.8),
    ("But even then, something remains. What happens when those moving molecules strike a wall?", 2.2),
])

# ---------------------------------------------------------------------------
# Chapter 4 — Where gas pressure comes from
# ---------------------------------------------------------------------------

_scene("10", "One molecule, one wall", [
    ("This is the turning point of our story. Where does gas pressure come from?", 1.4),
    ("Start with just one molecule, of mass m, bouncing around inside a cube of side L.", 2.6),
    ("Focus on one wall, and on one part of the velocity: the part perpendicular to that wall, v x.", 2.0),
    ("The molecule strikes the wall and bounces back elastically. Its speed is unchanged. Its motion along the wall is unchanged. Only v x flips sign.", 2.6),
    ("Its momentum along x goes from plus m v x to minus m v x. A change of two m v x.", 2.0),
    ("That momentum doesn't vanish. The wall receives it: a push of two m v x, outward, every time.", 2.0),
    ("Take a nitrogen molecule whose speed perpendicular to the wall is about five hundred metres per second. Its momentum transfer is around five times ten to the minus twenty-three kilogram metres per second.", 2.2),
    ("Utterly tiny. So how can tiny pushes add up to the pressure of the air?", 2.0),
])

_scene("11", "From hits to force", [
    ("Two things matter: how big each push is, and how often it comes.", 1.4),
    ("After hitting the wall, our molecule must cross the box and come back before it can strike again: a distance of two L, at speed v x.", 2.2),
    ("So the time between hits is two L over v x.", 2.0),
    ("On a graph of force against time, each hit is a sharp spike. Its area is the momentum delivered: two m v x.", 2.6),
    ("Now spread each spike evenly over the time until the next one. The area stays the same, but the force becomes steady.", 3.2),
    ("Average force equals the push, divided by the time between pushes: two m v x, over two L over v x.", 2.2),
    ("The twos cancel, and one v x moves up. The average force is m v x squared over L.", 2.8),
    ("Faster molecules push harder, and they come back sooner. That's why the speed appears squared.", 2.4),
])

_scene("12", "A crowd of molecules", [
    ("One molecule gives a sputtering force: long gaps, and sudden spikes.", 1.8),
    ("Five molecules give a busier pattern, but it's still ragged.", 2.0),
    ("Fifty, and the relative fluctuations shrink. Five thousand, and the force is nearly smooth. Each trace is divided by its own mean so we can compare fluctuations, not absolute forces.", 3.0),
    ("In real air, about three times ten to the twenty-three molecules strike every square centimetre of a wall, every second. An ordinary pressure gauge averages these tiny impacts into a steady reading.", 2.4),
    ("So add up all N molecules. The total force on the wall is N m times the average of v x squared, over L.", 2.2),
    ("Pressure is force per unit area. Divide by the wall's area, L squared, and L cubed is the volume, V.", 2.2),
    ("P equals N m times the average of v x squared, over V.", 2.4),
    ("Pressure is not something stored inside a gas. It is the steady flow of momentum, from molecules to the walls.", 2.4),
])

_scene("13", "Why one third?", [
    ("But molecules don't only move along x. They fly in every direction.", 1.4),
    ("Gather every velocity arrow at one point. Their tips form a fuzzy ball. No direction is special.", 3.2),
    ("Each velocity has three parts: v x, v y and v z. By Pythagoras in three dimensions, v squared equals v x squared plus v y squared plus v z squared.", 2.6),
    ("Average over the molecules. Small samples fluctuate, but at equilibrium, with no preferred direction, the three mean squares are equal.", 2.8),
    ("So the average of v x squared is exactly one third of the average of v squared.", 2.0),
    ("That one third is three dimensional space, showing up in the equation.", 1.6),
    ("Put it into our pressure. P V equals one third N m times the average of v squared.", 2.8),
    ("This is the pressure equation of the kinetic theory of gases.", 2.4),
])

_scene("14", "From motion to temperature", [
    ("Now connect pressure to temperature.", 1.0),
    ("The average kinetic energy is one half m times the average of v squared. So one third N m times that average is two thirds N times the average kinetic energy.", 2.2),
    ("P V equals two thirds N times average K.", 2.0),
    ("And we already know the average kinetic energy: three halves k B T.", 1.8),
    ("Substitute, and the two thirds and the three halves cancel. P V equals N k B T.", 2.8),
    ("Finally, count molecules in moles. N is n times Avogadro's number, and Avogadro's number times k B is the gas constant, R.", 2.0),
    ("P V equals n R T. The ideal gas law, built from nothing but moving molecules and bouncing walls.", 2.6),
    ("Notice the difference. Temperature tracks the average energy of each molecule. Pressure also depends on how many molecules there are, and how much room they have.", 2.2),
    ("You won't be asked to derive this in Class eleven. But it shows why the gas laws work. Now let's watch each of them happen.", 2.2),
])

# ---------------------------------------------------------------------------
# Chapter 5 — Boyle's law
# ---------------------------------------------------------------------------

_scene("15", "Squeeze the gas", [
    ("Boyle's question: what happens when you squeeze a gas?", 1.0),
    ("In sixteen sixty-two, Robert Boyle trapped some air in the sealed end of a J shaped glass tube, and poured mercury into the open end. The more mercury he added, the harder it pressed, and the smaller the trapped air became.", 1.8),
    ("Let's look inside. Trap a fixed amount of gas under a piston, and keep its temperature constant. The gauge reads one bar.", 2.0),
    ("Push the piston down slowly, letting heat escape, so the temperature never changes.", 2.6),
    ("The molecules move exactly as fast as before. Their average kinetic energy hasn't changed.", 1.8),
    ("But now they have less room. Each one crosses the box sooner, and returns to the walls more often.", 2.0),
    ("Watch the piston. The hits come thicker and faster. Halve the volume, and the hits on each square centimetre double. So does the pressure.", 2.8),
    ("Pressure rose, and no molecule got faster.", 1.8),
    ("Plot pressure against volume, and you trace a curve: a hyperbola. P is proportional to one over V.", 3.0),
    ("And here's the hidden simplicity. At every point on the curve, the rectangle P times V has the same area. P V is constant.", 3.0),
    ("P one V one equals P two V two.", 2.2),
])

_scene("16", "Boyle in numbers", [
    ("Let's try it. A sample occupies four litres at one bar. It is compressed, at constant temperature, to two litres.", 1.6),
    ("Pause and predict the new pressure.", 3.6),
    ("P two equals P one V one, over V two: one bar times four litres, over two litres. Two bar.", 2.2),
    ("Half the volume, twice the pressure.", 1.6),
    ("Another way to see it: plot P against one over V, and the curve becomes a straight line through the origin.", 2.4),
    ("Each hyperbola belongs to one temperature. It's called an isotherm. Warm the gas, and the molecules hit harder at every volume, so the whole curve moves outward.", 2.8),
    ("Higher temperature, a larger constant: P V grows in step with T. We'll see exactly why in a moment.", 2.0),
])

_scene("17", "Thinner air", [
    ("Boyle's law hides a second idea. Squeeze a gas into half the space, and the same molecules are packed twice as densely.", 1.6),
    ("At constant temperature, density is proportional to pressure.", 1.8),
    ("You can feel this on a mountain. Air at sea level is squeezed by the weight of all the air above it. Climb, and there is less air above you, so the pressure falls, and the air thins out.", 2.6),
    ("On the summit of Everest, the pressure is only about a third of its value at sea level. Every breath holds far fewer oxygen molecules. That's why climbers struggle, and why many carry oxygen.", 2.4),
    ("One more warning. Boyle's law needs constant temperature. Pump a bicycle tyre quickly, and the pump gets warm.", 2.0),
    ("Rapid compression does work on the gas faster than heat can escape. The molecules speed up, and the pressure rises more than Boyle's law predicts.", 2.8),
    ("So before using any gas law, ask first: what is being held constant?", 2.2),
])

# ---------------------------------------------------------------------------
# Chapter 6 — Charles' law
# ---------------------------------------------------------------------------

_scene("18", "Heat it, let it grow", [
    ("Charles' question: what happens when you heat a gas, but keep its pressure constant?", 1.0),
    ("Put a freely sliding piston on top, loaded with a weight. The load and atmosphere set the external pressure. At equilibrium, the gas pressure balances that load.", 2.0),
    ("Now heat the gas.", 1.4),
    ("The molecules speed up. They strike harder and more often. For a moment, the pressure inside beats the weight, and the piston rises.", 3.0),
    ("As the volume grows, the molecules have farther to travel. Hits on each square centimetre become less frequent, until the push balances the weight again.", 2.6),
    ("Higher temperature, same pressure, larger volume.", 1.8),
    ("Measure carefully, and the volume grows in step with absolute temperature. Double the kelvin temperature, and the volume doubles.", 2.6),
    ("V is proportional to T. V one over T one equals V two over T two.", 2.2),
    ("A hot air balloon shows a related effect, rather than a fixed-amount Charles experiment. Air escapes through its open bottom. The warmer air inside is less dense, and the buoyant force can lift the balloon.", 2.4),
])

_scene("19", "Absolute zero", [
    ("Here's where Charles' law reveals something deep.", 0.8),
    ("Measure a gas's volume at several temperatures in Celsius, and plot the points. They fall on a straight line.", 2.4),
    ("Repeat with a different amount of gas, or at a different pressure. Another straight line, with a different slope.", 2.2),
    ("Now extend every line backward, toward colder temperatures.", 2.6),
    ("They all meet at the same point: zero volume, at minus two hundred and seventy-three point one five degrees Celsius.", 2.8),
    ("That temperature is absolute zero. Measuring from there gives the Kelvin scale: T in kelvin equals the Celsius temperature plus two hundred and seventy-three point one five.", 2.4),
    ("On the Kelvin scale, every line passes through the origin. That's why gas laws need absolute temperature.", 2.4),
    ("One caution. No real gas reaches zero volume. Real gases leave the ideal-gas regime, and many condense on cooling. The meeting point is an extrapolation of ideal gas behaviour, not a measurement.", 2.2),
])

_scene("20", "Kelvin, not Celsius", [
    ("Try this one. A gas occupies two litres at three hundred kelvin. It is heated at constant pressure to four hundred and fifty kelvin.", 1.4),
    ("What is the new volume?", 3.6),
    ("Temperature rose by half, from three hundred to four hundred and fifty kelvin. So the volume rises by half: three litres.", 2.4),
    ("Now a trap. Warm a gas from twenty to thirty degrees Celsius. The Celsius number rises by fifty percent, but absolute temperature does not.", 1.8),
    ("But the volume grows by only about three percent.", 2.2),
    ("In kelvin, twenty degrees Celsius is two hundred and ninety-three point one five kelvin, and thirty degrees is three hundred and three point one five. A rise of only a few percent.", 2.2),
    ("Gas laws need absolute temperature. In SI we use kelvin: the scale on which classical ideal-gas translational energy extrapolates to zero at zero kelvin.", 2.4),
])

# ---------------------------------------------------------------------------
# Chapter 7 — Gay-Lussac's law
# ---------------------------------------------------------------------------

_scene("21", "Heat it, hold it", [
    ("In Charles' law, the gas was free to expand. What if we stop it?", 1.0),
    ("Seal the gas in a rigid container. The volume cannot change. The amount cannot change.", 1.8),
    ("Now heat it.", 1.6),
    ("The molecules speed up. Each one strikes the wall harder, delivering more momentum per hit.", 2.0),
    ("And faster molecules cross the box sooner, so they strike more often too.", 2.0),
    ("More momentum per hit, and more hits per second. The pressure climbs.", 2.4),
    ("Pressure is proportional to absolute temperature. P one over T one equals P two over T two.", 2.4),
    ("Heat a sealed container from three hundred to three hundred and sixty kelvin, and a pressure of one bar becomes one point two bar.", 2.2),
    ("Both effects grow with speed, so the pressure grows with speed squared, which is proportional to temperature.", 2.2),
    ("A sealed, rigid gas cylinder shows this directly. With a fixed amount of gas, warming raises its pressure because molecules transfer momentum to the walls faster.", 2.2),
])

_scene("22", "Same cause, different outcome", [
    ("Put the two experiments side by side.", 1.2),
    ("In both, heating does the same thing to the molecules: it raises their average kinetic energy.", 2.6),
    ("With a free piston, the gas expands, and the pressure stays the same. With rigid walls, the volume stays the same, and the pressure rises.", 3.0),
    ("One microscopic change. Two macroscopic outcomes. The difference is only what we hold constant.", 2.2),
    ("Car tyres show this, roughly. After a long drive, the air inside is warmer, and the pressure reads higher. A tyre can stretch a little, so it isn't perfectly rigid, but Gay-Lussac's law gives a good estimate.", 2.0),
    ("Constant pressure: V is proportional to T. Constant volume: P is proportional to T.", 2.4),
])

# ---------------------------------------------------------------------------
# Chapter 8 — Avogadro's law
# ---------------------------------------------------------------------------

_scene("23", "Add more molecules", [
    ("One variable left: the amount of gas.", 1.0),
    ("Keep the temperature constant, with a weighted piston setting the external pressure. Compare states after the piston has balanced. Then add more molecules.", 2.0),
    ("More molecules means more hits on the walls each second. The pressure inside rises above the weight, and the piston rises.", 3.2),
    ("It stops when the molecules are spread just as thinly as before: the same number in each litre, the same hits on each square centimetre.", 2.6),
    ("Double the molecules, double the volume. V is proportional to n.", 2.4),
    ("V one over n one equals V two over n two.", 2.0),
    ("So a container with twice as many molecules doesn't have to be at twice the pressure. If its volume doubles, the pressure doesn't change at all.", 2.2),
    ("You see a related effect when breathing in. Your chest expands first, lowering lung pressure slightly so air flows in. Near the same pressure and temperature, more air occupies more volume.", 2.0),
])

_scene("24", "Equal volumes, equal numbers", [
    ("In eighteen eleven, Amedeo Avogadro took the idea further.", 1.0),
    ("Take three boxes of the same volume, at the same temperature and pressure: one of helium, one of nitrogen, one of carbon dioxide.", 2.2),
    ("Helium atoms are light and fast. Carbon dioxide molecules are heavy and slow. But at the same temperature, they all carry the same average kinetic energy.", 2.6),
    ("Light particles hit more often but transfer less momentum per hit. At the same temperature, their time-averaged pressure contribution per particle is the same. Equal pressures and volumes therefore mean equal particle numbers.", 2.4),
    ("Equal volumes of ideal gases, at the same temperature and pressure, contain equal numbers of molecules. Whatever the gas.", 2.2),
    ("How many? At room temperature and one bar, every litre holds about two point four times ten to the twenty-two molecules.", 2.2),
    ("This gives a universal molar volume. At two hundred and seventy-three point one five kelvin and one bar, one mole of any ideal gas occupies twenty-two point seven one litres.", 2.4),
    ("You may have seen twenty-two point four litres. That value belongs to one atmosphere, a slightly higher pressure than one bar.", 2.4),
])

# ---------------------------------------------------------------------------
# Chapter 9 — The ideal gas equation
# ---------------------------------------------------------------------------

_scene("25", "Four laws, one surface", [
    ("We now have four laws. Each one holds two quantities constant, and relates the other two.", 1.4),
    ("Boyle: constant temperature and amount. V is proportional to one over P.", 1.4),
    ("Charles: constant pressure and amount. V is proportional to T.", 1.4),
    ("Gay-Lussac: constant volume and amount. P is proportional to T.", 1.4),
    ("Avogadro: constant pressure and temperature. V is proportional to n.", 1.6),
    ("Combine the volume relations, and V is proportional to n T over P. Replace the proportionality with a constant, R, and rearrange.", 2.6),
    ("P V equals n R T. The ideal gas equation.", 2.4),
    ("Now picture every state of one mole of ideal gas, all at once. Pressure, volume and temperature form a single curved surface.", 4.0),
    ("Slice it at constant temperature, and you get Boyle's hyperbola.", 3.0),
    ("Slice it at constant volume, and you get Gay-Lussac's straight line.", 3.0),
    ("Slice it at constant pressure, and you get Charles' line.", 3.0),
    ("The four laws were never separate. They are views of one surface, one equation.", 3.4),
])

_scene("26", "Using P V equals n R T", [
    ("All pressures in the gas equations are absolute pressures. R is the universal gas constant. In SI units, it is eight point three one four joules per mole per kelvin.", 1.6),
    ("And it's the same constant we met inside the kinetic theory: Avogadro's number times the Boltzmann constant.", 2.0),
    ("Chemists often prefer litres and bar. Then R is zero point zero eight three one four litre bar per mole per kelvin.", 1.8),
    ("So one mole at three hundred kelvin and one bar fills about twenty-five litres: a box about twenty-nine centimetres on each side.", 2.6),
    ("For a fixed amount of gas moving between two states, n R stays constant, so P one V one over T one equals P two V two over T two.", 2.4),
    ("A weather balloon holds two litres at one bar and three hundred kelvin. High up, the pressure is half a bar, and the temperature two hundred and fifty kelvin. What's its volume?", 3.0),
    ("Halving the pressure doubles the volume, to four litres. Cooling from three hundred to two hundred and fifty kelvin shrinks it by a sixth. Three point three three litres.", 2.6),
])

_scene("27", "Weighing a gas", [
    ("The ideal gas equation can even weigh molecules.", 1.0),
    ("Write the amount as mass over molar mass. Then P V equals m over M, times R T, and the density, m over V, equals P M over R T.", 2.6),
    ("At the same pressure and temperature, density is proportional to molar mass.", 1.8),
    ("At one bar and three hundred kelvin, nitrogen has a density of about one point one two grams per litre. Helium, about zero point one six. Seven times lighter. That's why a helium balloon rises.", 2.6),
    ("Turn it around, and a density measurement gives the molar mass: M equals density times R T over P. One point one two grams per litre gives twenty-eight grams per mole: nitrogen.", 2.6),
    ("But remember what this equation assumes: molecules with no size, and no attractions. Hold on to that thought.", 2.2),
])

# ---------------------------------------------------------------------------
# Chapter 10 — Dalton's law of partial pressures
# ---------------------------------------------------------------------------

_scene("28", "Mixtures of gases", [
    ("Air is not one gas. It is mostly nitrogen and oxygen, sharing the same space.", 1.6),
    ("How does each gas contribute to the pressure?", 1.2),
    ("In an ideal mixture, molecules ignore each other. Each gas strikes the walls as if the others weren't there.", 2.4),
    ("So the total push on the walls is the sum of the pushes from each gas.", 2.0),
    ("P total equals P A plus P B. For any number of gases, the total is the sum of the partial pressures.", 2.2),
    ("Each partial pressure is what that gas alone would exert in the whole container: P i equals n i R T over V.", 2.0),
    ("So each gas's share of the pressure is its share of the molecules, its mole fraction, x i. P i equals x i times P total.", 2.4),
    ("Try it. Two moles of nitrogen and one mole of oxygen, at a total pressure of three bar.", 1.8),
    ("Nitrogen's mole fraction is two thirds, oxygen's one third. So nitrogen supplies two bar, and oxygen one.", 2.4),
    ("Back to the mountain. Oxygen is about twenty-one percent of air, so at sea level it supplies about zero point two one bar. On the summit of Everest, only about zero point zero seven.", 2.4),
    ("The same collisions that explained Boyle's law explain Dalton's.", 2.0),
])

_scene("29", "Gas over water", [
    ("Dalton's law turns up in every chemistry lab.", 1.0),
    ("Collect a gas, say hydrogen, by bubbling it into an upturned jar of water.", 2.6),
    ("The gas in the jar also contains water vapour. Once it is saturated at the measured temperature, water contributes its equilibrium vapour pressure. Equal water levels inside and outside make the total gas pressure equal atmospheric pressure.", 2.4),
    ("So the measured pressure is the dry gas plus water vapour. P dry gas equals P total minus the pressure of water vapour.", 2.4),
    ("At twenty-five degrees Celsius, water vapour supplies about zero point zero three one seven bar. If the total is one bar, the dry gas exerts zero point nine six eight bar.", 2.4),
    ("This vapour pressure of water is called aqueous tension, and it rises with temperature.", 2.2),
])

# ---------------------------------------------------------------------------
# Chapter 11 — Conclusion: the limits of the perfect gas
# ---------------------------------------------------------------------------

_scene("30", "Where the ideal gas ends", [
    ("We began with an enormous crowd of molecules, moving randomly inside a container.", 1.4),
    ("From their collisions, we explained pressure. From pressure, temperature, volume and amount, we found the gas laws, and one equation that unites them.", 2.6),
    ("But our model hides a simplification. We treated molecules as points that never attract one another.", 1.6),
    ("Real molecules attract. A molecule about to strike the wall is tugged back by its neighbours, so it hits a little softer.", 2.6),
    ("Real molecules take up space. Squeeze a gas hard enough, and that space is no longer negligible.", 2.6),
    ("Even an ideal gas already has a spread of molecular speeds: the Maxwell-Boltzmann distribution. Understanding that spread is our next step.", 2.8),
    ("So what happens when these assumptions fail? That is where the ideal gas ends, and real gases begin. See you in Part two.", 3.4),
])

_scene("31", "Stay curious", [
    ("Thanks for watching. Stay curious.", 4.4),
])
