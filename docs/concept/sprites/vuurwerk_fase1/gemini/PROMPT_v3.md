# Gemini-prompt: vuurwerklijn fase 1, v3 (19 nov)

Nieuw gesprek per variant, geen bijlage. Gebaseerd op v2 (`PROMPT_v2.md`); alleen de twee punten van Jordi veranderd.

## Jordi over r2 (`../r2/gemini_A_salamander.png`, `../r2/gemini_B_gekko.png`)
"Beter, kleuren prima, alleen de armen krullen niet en hij komt niet uit de vuurpijl".

## Analyse en wijzigingen Claude
- In v2 stond (eigen toevoeging van Claude, niet van Jordi) dat **het lijf** om de pijl krult. Gemini maakte daarvan een staart die om de pijl draait, met korte armpjes die de pijl knuffelen. Jordi zei: "dat de armen eerst om de vuurpijl krullen". v3: het lijf gaat recht omhoog langs de pijl; **de armen zijn de krullen**, verder draait niets om de pijl.
- Gemini tekende een losse uitlaatvlam naast een staartpunt. v3: precies één vlam uit het mondstuk en dat is het wezen; geen staartpunt, het laagste punt van het wezen zit in het mondstuk.
- Werkt dit niet: voorstel om een simpele vormschets als bijlage te geven (bij de spooktrein haalde tekst alleen het ook niet).

## Prompt (A; voor B zie onder)

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style).

CONCEPT
- Fire/Fairy type, small first stage of an evolution line. Endearing because it is tiny and clings to its rocket.
- A FIREWORK ROCKET STANDS PERFECTLY UPRIGHT in the middle: pointed tip at the top, casing with HORIZONTAL rings in pink, magenta and yellow, and a clear round NOZZLE at the bottom.
- Exactly ONE flame comes out of the nozzle, and that flame IS the Pokémon: it leaves the nozzle, bends upward and becomes the creature's body in one unbroken stream. There is NO separate exhaust flame and NO tail tip anywhere: the lowest point of the creature is inside the nozzle.
- The creature is ONLY AN UPPER BODY made of fire: head, neck, chest and two arms. Below the chest the body gets narrower and narrower until it is just the flame jet entering the nozzle. NO belly, NO sitting body, NO hind legs, NO tail.
- The body rises STRAIGHT UP along the side of the rocket, so the head peeks out above the rocket, next to the tip. The body itself does NOT wrap around the rocket.
- THE ARMS ARE THE COILS: the two arms are very long, as long as the rocket, thin like ribbons of fire. Starting at the shoulders, each arm SPIRALS DOWN AROUND THE ROCKET CASING, passing in front of the rocket, behind it and in front again (one full turn). Only BELOW those coils, near the bottom of the casing, do the two small hands appear, gripping the rocket. Nothing else wraps around the rocket.
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
- No round cartoon head with big shiny eyes and a big smile. No orange lizard. No belly, no legs, no tail, no sitting pose. No creature hugging the rocket from the side. No tail or body coiling around the rocket. No separate rocket flame. No diagonal stripes on the rocket. No smooth skin, no flat single color. No horns. No green, blue or orange. No text. No glossy 3D render.
```

### Variant B (wimpergekko)
- HEAD-regel vervangen door: `- HEAD: the head of a CRESTED GECKO (Correlophus ciliatus): triangular head, large lidless eyes with vertical slit pupils, a row of small spiky crests above each eye like eyelashes that continue back along the sides of the head; here those crests are little flame points. Calm, curious expression with a closed mouth line. It is a gecko head made of fire, not a cartoon dinosaur.`
