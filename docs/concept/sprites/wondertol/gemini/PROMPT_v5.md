# Gemini-prompt: wondertol, v5 (16 nov)

Nieuw gesprek, geen eerdere versies als bijlage. Bijlagen: (1) foto vuursalamander (alleen kop en poten), (2) `referenties/jordi_ref1_vonken_grond.webp` en/of (3) `referenties/jordi_ref4_ground_bloom_groen.png` (Jordi's referenties voor de wondertol).

## Jordi (16 nov)
Over v4 (`r4/gemini_v4.png`): "dit lijkt meer een soort supernova". Daarna 4 referenties: "hier referenties" (`referenties/jordi_ref1..4`).
(Wat Claude in de referenties ziet: een klein, verblindend fel heet punt laag op de grond; daaruit spuiten lange, dunne, gebogen vonksporen omhoog en opzij als een lage koepel/fontein; geen vuurrad naar de kijker, geen bol.)

Jordi: "die groene stuur ik ook naar gemini bij de volgende prompt" → regel toegevoegd dat Gemini de kleuren van de bijlagen negeert (kleur B, geen groen).

## Wijzigingen t.o.v. v4 (keuzes Claude, schrappen mag)
- Lijf = het felle hete punt laag bij de grond (wit-goud, naar roze/magenta aan de rand); uit rug en flanken spuiten gebogen vonksporen omhoog en opzij als een lage fontein. Geen pinwheel/spiraal meer.
- Salamander laag bij de grond (zoals in v3/v4 de kop laag), kop en poten van vuur.
- Vonksporen als dikke, effen gebogen pixelstrepen (anders verdwijnen ze op 64×64).
- Kleur B blijft (Jordi): goud-wit, roze, magenta, karmijn, turkoois accent.

## Prompt

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style).

CONCEPT
- Fire/Fairy type, the middle stage of a firework evolution line: a SALAMANDER WHOSE BODY IS A BURNING GROUND-SPINNER FIREWORK.
- Attachment 1 (fire salamander) is only for the head and legs. The other attachments show what the ground-spinner firework looks like when lit: a small, blinding hot point low on the ground, with long curved spark trails shooting up and out of it like a low fountain. Use the attachments ONLY for the shape of the firework; ignore their colors (one of them is green) and use the colors described below.
- THE BODY IS THAT BLAZING HOT POINT: a compact, low, glowing body of white-gold fire close to the ground, shading to hot pink and magenta at its edges. The creature is low and flat to the ground, not standing up.
- FROM ITS BACK AND SIDES, CURVED SPARK TRAILS SHOOT UP AND OUTWARD like a low dome-shaped fountain, slightly curling as if it spins. Draw them as thick, solid, curved pixel streaks so they stay readable at 64x64.
- THE HEAD sticks out of the front of the glowing body: a FLAT, WIDE salamander head, held low, with small eyes on top of the head and a wide mouth line. The head is made of fire; only the eyes and the mouth are drawn into the flame.
- FOUR SHORT SALAMANDER LEGS made of fire, splayed sideways, with small splayed toes. The tail is a short flame trailing behind, low to the ground.
- FIREWORK COLORS, NOT CAMPFIRE COLORS: white-gold at the hot body, hot pink and magenta at its edges, deep crimson outline accents, spark trails in gold and pink with ONE ACCENT of turquoise blue in a few spark trails. Gold-yellow spots like a fire salamander on the head. No green.
- FAIRY: playful and mischievous expression.

STYLE AND FORMAT
- Official Gen 3 front sprite, 64x64, max 16 colors, 1 px dark outline on the body, light from top left, flat Gen 3 shading with 3 to 4 tones per color, no dithering.
- Clear silhouette at 64x64: a low glowing salamander body with a fountain of curved sparks rising from it.
- Three-quarter view facing left. Compact composition that fits a square.
- Plain white background. NO floor, shadow, smoke or motion lines. One single creature.

AVOID
- NOT A PINWHEEL, NOT A SPIRAL GALAXY, NOT A SUPERNOVA, no disc facing the viewer. Not a shell, not a turtle, not a solid ball.
- NOT CHARMANDER: no big round head, no big cute eyes, no upright body, no belly, no arms, no flame on the tail tip. No dragon look, no horns or spikes.
- No separate firework object, nothing it lies or sits on. No smooth skin. No coiled body, no snake shape. No glitter specks, no twinkling stars. No orange. No round explosion in the sky. No rocket, no stick. Not Wooper. No hearts. No text. No glossy 3D render.
```
