# Gemini-prompt: vuurwerklijn fase 1, v5 (19 nov): opnieuw opgebouwd

Nieuw gesprek, geen bijlage.

## Jordi over r4 (`../r4/`)
"het hoofd zit nu te hoog, plus de armen doet die nog steeds niet goed"; "en hij komt nog steeds niet uit de vuurpijl"; "ligt het niet aan prompting?"

## Analyse Claude: ja, het ligt aan de prompt
- v1–v4 beginnen met "een salamander van vuur" en zetten "komt uit de pijl" als één regel tussen twintig andere. Gemini ziet dan twee dingen (een hagedis + een pijl) en zet ze naast elkaar; een salamander heeft volgens hem een lijf en een staart, dus die tekent hij erbij (als krul om de pijl).
- "Arms" roept normale armpjes op; dat ze om de pijl krullen staat er pas later bij en verliest het van het beeld "beestje knuffelt pijl".
- "Head, neck, chest" + "head peeks out above" = lange hals, kop te hoog. "Round nozzle" werd een glazen bol.
- Les die er al stond (GEMINI.md, Banette-evolutie): begin met wát het wezen is en hoe het eruitziet, details daarna. En: een bekend beeld werkt beter dan een beschrijving.

## Wat v5 anders doet
- Begint met het beeld: **een geest die uit een wonderlamp komt** (onderlijf = rookspoor uit de tuit), maar de lamp is een vuurpijl en het spoor is vuur uit de onderkant. Dat is precies "alleen het bovenlijf, komt uit de pijl"; Gemini kent dat beeld.
- Armen: **lang en slap als linten** die als de streep van een kapperspaal om de pijl draaien; geen "upper body/neck/chest".
- Kop: vlak boven de punt, de kin raakt de punt bijna.
- Onderkant: "open bottom end of the cardboard tube", geen "nozzle".
- Veel korter; kleur en stijl ongewijzigd (r2: "kleuren prima").

## Prompt (A; voor B "fire salamander" → "crested gecko" en de kopregel uit `PROMPT_v2.md`)

```
Design an original Pokémon as an official Gen 3 pixel-art front sprite (Ruby/Sapphire/Emerald style).

WHAT IT IS
Think of a genie coming out of a magic lamp: the genie has no legs, its body is a trail that streams out of the lamp. This Pokémon works the same way, but the lamp is an upright FIREWORK ROCKET and the genie is a small FIRE SALAMANDER made entirely of fire. The fire trail comes out of the open BOTTOM end of the rocket, curves up along the rocket and becomes the salamander's chest and head. There is nothing else: no legs, no tail, no second body.

POSE
- The rocket stands perfectly upright. The head rests just above the pointed tip of the rocket, chin almost touching the tip. Short body, no long neck.
- Its two arms are very long and floppy, like ribbons of fire. They wind around the rocket like the stripe on a barber pole, going round the rocket from top to bottom. At the end of each arm, near the bottom of the rocket, a small hand grips the rocket.
- Only the fire trail and the two arms touch the rocket. Nothing else winds around it.

DETAILS
- Head of a fire salamander: flat, broad, rounded snout, small black bulging eyes on top of the head, swollen glands behind the eyes. Calm, curious. Cute because it is small and clings to its rocket.
- Made of fire: flame edges, flame streaks, glitter specks, a few four-pointed twinkles. Gold-white at the head, hot pink in the middle, magenta where the fire leaves the rocket. No orange.
- Rocket: cardboard tube with horizontal pink, magenta and yellow rings, pointed pink tip. The bottom end is simply open, the fire comes straight out of it.

FORMAT
64x64, max 16 colors, 1 px dark outline, flat Gen 3 shading, no dithering, three-quarter view facing left, plain white background, no shadow. No firework explosions. No text, no 3D render.
```
