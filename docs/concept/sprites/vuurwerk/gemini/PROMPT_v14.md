# Gemini-prompt: vuurwerklijn fase 3 (Fire/Fairy), v14 (16 nov): zonder barsten, minder glad, meer vuurwerkkleur

Nieuw gesprek, GEEN bijlage (zoals v13).

## Alle besluiten van Jordi tot nu (letterlijk, 16 nov)
- Slang; "de staart 1 vuurpijl"; "het hoofd moet van vuur zijn"; "en het lichaam ook, alsof alles uit de vuurpijl komt"; "sterker"; "furieuzer qua vorm"; "dat het er niet zo dynamisch uitziet" (moet dynamischer); "schuin omlaag is niet zo erg".
- "wat twinkel en iets zachtroze erin is ok"; "teveel een vlam en net te weinig vuurwerk"; "meer vuurwerk kleur en minder normaal vuur"; "fairy hoeft niet bepaald cute te zijn, zie grimmsnarl".
- "geen spieren/gedrongen"; "wat meer ringen"; "wat losse vlammen om de vorm wat dynamiek te geven"; "er komen geen rotjes, het vuurwerk ontstaat echt vanuit het vuur zelf".
- Over v9: "ik vind de vorm tof, de vuurpijl ook, het hoofd vind ik nog iets te dragon/boos"; v10: "het gezicht is beter"; daarna "het hoofd is wel wat te kaal".
- Zonder barsten: "de vorm klopt niet".
- Over v13 (`r10/gemini_v13.webp`): "hij is te glad, de kleur mag ook wat meer vuurwerk nog, laten we niet meer vragen ook aan gemini om vuurwerk explosies te maken, want dat kan die niet" → **barsten komen niet meer in de prompt; die zetten we in de spritefase zelf** (naar `../referentie_vuurwerk_pixelart.png`).

## Keuzes Claude (niet besproken; schrappen mag)
- Tegen de veer van v9–v12: lussen van verschillende grootte, lijf taps (vol bij de kop, dun bij de pijl), kop sluit vloeiend aan.
- Pijl vast: het vuur stroomt uit de achterkant van de pijl.
- Kop niet kaal: vlampunten achter op de kop (optie (a); Jordi koos nog niet).
- "Te glad": het lijf krijgt over de hele lengte vlamtongen langs beide randen en vlamstrepen erin (zoals v9, waarvan Jordi de vorm tof vond).
- "Meer vuurwerkkleur": v13 is één zalmrode kleur. Vuurwerk = fel, verzadigd, meerdere kleuren en glitter: kleurverloop langs het lijf (goud-wit bij de kop → felroze → magenta/karmijn bij de pijl) met glitterspikkels en witgloeiende hooglichten.
- Plekken waar de barsten later komen: niet gevraagd; kiezen we in de spritefase.

## Prompt

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style).

CONCEPT
- Fire/Fairy type, a fully evolved Pokémon that chases away evil spirits. Strong, dynamic, slender (no muscles, not stocky).
- It is a SERPENT MADE OF FIRE THAT POURS OUT OF A FIREWORK ROCKET. The rocket is its tail end: the fire streams directly out of the back of the rocket and becomes the serpent's body and head. Body and rocket are firmly connected, no gap.
- THE BODY TAPERS: fullest near the head, getting thinner toward the rocket.
- THE BODY MAKES SEVERAL LOOPS OF DIFFERENT SIZES, flowing like a ribbon of fire through the air. Not a stacked spring or coil of equal rings.
- NOT SMOOTH: the body is clearly made of flames. Along its whole length both edges are ragged with flickering flame tongues, and flame streaks run through it. No smooth skin or tube.
- A few loose flames break away from the body and lick outward for motion.
- THE HEAD IS MADE OF FIRE and flows smoothly out of the body: a smooth, rounded SERPENT head, not a dragon head, with a few flame points at the back of the head. Determined, not angry. Only the eyes and the mouth are drawn into the flame.
- THE ROCKET: pointed tip, striped casing in pink, magenta and yellow; it may point diagonally down.
- FIREWORK COLORS, NOT CAMPFIRE COLORS: vivid, saturated and glittering, not one flat red. The color shifts along the body like a firework changing color: glittering gold-white at the head, hot pink in the middle, magenta and crimson toward the rocket. Glitter specks and small white-hot highlights sparkle inside the flames. No orange.
- FAIRY, BUT NOT CUTE: a wild, fierce fae spirit. A few small four-pointed twinkling stars.
- No arms, no legs, no firecrackers. NO firework explosions or burst shapes anywhere.

STYLE AND FORMAT
- Official Gen 3 front sprite, 64x64, max 16 colors, 1 px dark outline, light from top left, flat Gen 3 shading with 3 to 4 tones per color, no dithering.
- Solid shapes with clean outlines that read as a clear silhouette at 64x64; no thin strands.
- Three-quarter view facing left. Compact composition that fits a square.
- Plain white background. NO floor, shadow or smoke. One single creature.

AVOID
- No smooth skin, no flat single color. No pompoms or round bursts. No spring or slinky shape. No floating, separate rocket. No dragon snout, horns, whiskers or brow ridges. No collar or halo behind the head. Not Rayquaza, not Gyarados. No green, blue or orange. Nothing cute, no hearts. No text. No glossy 3D render.
```

## v14b (16 nov): hoofd = explosie (experiment)
Jordi: "of we maken het hoofd ene explosie en we kijken wat die gaat doen". Zelfde prompt, twee regels anders:
- HEAD-regel vervangen door:
  `- THE HEAD IS A FIREWORK EXPLOSION: where the fiery body ends, it bursts open into a firework explosion, and that explosion IS the head. The eyes and the mouth are inside the explosion itself. There is no snake head sticking out of it, no collar, no halo.`
- In de no-regel: `NO firework explosions or burst shapes anywhere.` → `No firework explosions anywhere except the head.`
Les uit v4–v6: een gezicht "in het midden van de barst" gaf steeds een kop in een kraag; daarom staat er expliciet dat er geen slangenkop uitsteekt.
