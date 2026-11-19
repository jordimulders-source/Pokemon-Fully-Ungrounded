# Gemini-prompt: vuurwerklijn fase 2, v6 (19 nov): lijnschets in plaats van vormschets

Nieuw gesprek, **alleen bijlage `../schets/lijnschets_v6.png`** (`schets/maak_lijnschets.py`): alleen de looplijn van het lijf, de pijl, een cirkel voor de plek van de kop en twee rondjes voor de handen.

## Jordi over r5 (`../r5/gemini_v5.png`)
"dit werkt ook niet"; "hij volgt je schets te letterlijk".
Jordi over de eerste lijnschets: "maar je schets mist wel het krullen nu he" → lijnschets krult nu anderhalve slag om de pijl.
(Claude: kop werd een crème schedel met lange snuit, armen klompjes, extra losse vlamsliert rechts; de opbouw uit de achterkant van de pijl kwam wel goed.)

## Gemini weigerde (19 nov)
Jordi: "hij zegt nu 2 keer dat die geen unsafe images kan genereren". Vermoeden Claude: de lijnschets (lijn + cirkel = poppetje) samen met "bazooka" leest als een persoon met een wapen. "bazooka" vervangen door "party cannon" (feestkanon); humor van het vuurwapen blijft in de houding.

## Prompt

```
Design an original Pokémon as an official Gen 3 pixel-art front sprite (Ruby/Sapphire/Emerald style).

The attached image is only a GESTURE LINE: the grey line shows the path of the body (light grey = behind the rocket), the circle shows where the head goes, the two small rings show where the hands hold the rocket. Design the creature yourself along that line; do not copy the lines.

WHAT IT IS
A confident young fire salamander made entirely of fire, that comes out of a firework rocket and proudly holds that rocket under its arms, aimed forward like a party cannon. The creature is clearly BIGGER than the rocket.

HOW IT IS BUILT
- Fire comes out of the open back end of the rocket. That fire IS the creature's body: it makes a short bend, then WINDS AROUND THE ROCKET one and a half times, like a snake coiled around a branch (you see it pass in front of the rocket twice), and then rises up into an upright body, like a rearing cobra.
- Two short arms hold the rocket, its tip pointing diagonally forward and up.
- No legs, no feet, no second tail, no extra loose flames: the one flame from the rocket is the whole body.

HEAD
A living, cute-but-cocky salamander face, not a skull: cream-white, a bit longer and flatter than a baby's, rounded snout. Half-lidded black eyes, a confident grin, a small bulge behind each eye. No gills. One crest of flame sweeping backward over the head. Not Charmander, no dragon.

COLORS
Firework colors shifting along the body: cream-white head, hot pink chest, red where the fire leaves the rocket. Rocket: pink, magenta and yellow stripes, pink tip.

FORMAT
64x64, max 16 colors, 1 px dark outline, flat Gen 3 shading, no dithering, three-quarter view facing left, compact, plain white background, no shadow. No smoke, no speed lines, no sparkles, no explosions. No text.
```
