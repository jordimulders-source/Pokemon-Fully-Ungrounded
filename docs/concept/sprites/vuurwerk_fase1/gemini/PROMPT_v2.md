# Gemini-prompt: vuurwerklijn fase 1, v2 (19 nov)

Nieuw gesprek per variant, geen bijlage (Jordi, 19 nov: "nee bijlagen zijn niet nodig, gemini heeft een groot referentiekader").

## Jordi over r1 (`../r1/gemini_A_salamander.png`, `../r1/gemini_B_gekko.png`; namen in volgorde zoals gestuurd)
"Hij wil heel graag Charmander maken. Ze zijn allebei sowieso nog niet goed, het lichaam komt niet zichtbaar uit de pijl. De armen krullen niet een extra ronde om de pijl en het hoofd is gewoon charmander bij beiden, of ik nu salamander of gecko doe".

## Wat Claude verandert (keuzes, niet besproken; schrappen mag)
1. **Charmander:** "Not Charmander" eruit (een Pokémon noemen = Gemini kopieert hem, GEMINI.md) en ook "baby", "cute smile" en "big head, large shining eyes" (samen = Charmander). In plaats daarvan een soort met een eigen kop:
   - A: **vuursalamander** (*Salamandra salamandra*): platte brede kop, kleine zwarte bolle ogen bovenop de kop, dikke klieren (parotoïden) achter de ogen, geen wangen.
   - B: **wimpergekko** (*Correlophus ciliatus*): stekelige kammetjes boven de ogen die als wimpers doorlopen naar achter op de kop, grote ogen zonder oogleden met verticale pupil. De kammetjes kunnen als vlammetjes.
   - Cute via houding en verhouding (klein, klampt zich vast), niet via een cartoonkop.
2. **Lijf zichtbaar uit de pijl:** de pijl krijgt een duidelijk mondstuk onderaan; de vlam uit dat mondstuk loopt zonder onderbreking door in het lijf; het lijf heeft geen onderkant, het wordt naar beneden smaller tot het de vlam uit het mondstuk ís. Expliciet: geen zittend lijf, geen buik, geen achterpoten.
3. **Extra ronde van de armen:** elke arm is lang en slap als een lint, draait een volle ronde om de huls (je ziet de arm vóór en achter de pijl langs gaan) en pas daaronder komt de hand. De huls krijgt **horizontale** ringen in plaats van een schroefstreep, zodat de krullende armen niet in de strepen opgaan.

## Prompt (A; voor B zie onder)

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style).

CONCEPT
- Fire/Fairy type, small first stage of an evolution line. Endearing because it is tiny and clings to its rocket.
- A FIREWORK ROCKET STANDS PERFECTLY UPRIGHT in the middle: pointed tip at the top, casing with HORIZONTAL rings in pink, magenta and yellow, and a clear round NOZZLE at the bottom.
- A jet of fire shoots out of the nozzle and BENDS UPWARD. That jet of fire IS the Pokémon's body: one unbroken stream from the nozzle into the creature. You can clearly follow the flame from the nozzle into the body. No gap, no seam.
- The creature is ONLY AN UPPER BODY made of fire: head, neck, chest and two arms. Below the chest the body gets narrower and narrower until it is just the flame jet entering the nozzle. NO belly, NO sitting body, NO hind legs, NO tail.
- The body curls up around the rocket so the head peeks out above the rocket, next to the tip.
- THE ARMS: each arm is long and ribbon-like and WRAPS ONE FULL TURN AROUND THE ROCKET CASING (you see the arm pass in front of the rocket, disappear behind it and come back). Only BELOW that coil do the small hands appear, gripping the casing.
- HEAD: the head of a FIRE SALAMANDER (Salamandra salamandra): flat, broad, rounded snout, small black bulging eyes on top of the head, thick swollen glands behind the eyes, no cheeks. Calm, curious expression with a closed mouth line. It is a salamander head made of fire, not a cartoon dinosaur.
- Made of fire: flame edges and flame streaks, not smooth skin. Only the eyes and mouth are drawn into the flame.
- FIREWORK COLORS, NOT CAMPFIRE COLORS: vivid, saturated, glittering. Gold-white at the head, hot pink in the middle, magenta at the nozzle. Glitter specks and a few small four-pointed twinkling stars. No orange.
- No firecrackers. NO firework explosions or burst shapes anywhere.

STYLE AND FORMAT
- Official Gen 3 front sprite, 64x64, max 16 colors, 1 px dark outline, light from top left, flat Gen 3 shading with 3 to 4 tones per color, no dithering.
- Solid shapes with clean outlines that read as a clear silhouette at 64x64; no thin strands.
- Three-quarter view facing left. Compact composition that fits a square.
- Plain white background. NO floor, shadow or smoke. One single creature.

AVOID
- No round cartoon head with big shiny eyes and a big smile. No orange lizard. No belly, no legs, no tail, no sitting pose. No creature hugging the rocket from the side. No diagonal stripes on the rocket. No smooth skin, no flat single color. No horns. No green, blue or orange. No text. No glossy 3D render.
```

### Variant B (wimpergekko)
- HEAD-regel vervangen door: `- HEAD: the head of a CRESTED GECKO (Correlophus ciliatus): triangular head, large lidless eyes with vertical slit pupils, a row of small spiky crests above each eye like eyelashes that continue back along the sides of the head; here those crests are little flame points. Calm, curious expression with a closed mouth line. It is a gecko head made of fire, not a cartoon dinosaur.`
