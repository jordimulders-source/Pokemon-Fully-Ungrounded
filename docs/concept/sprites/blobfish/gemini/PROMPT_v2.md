# Gemini-prompt: blobfish fase 1 (Water), startprompt v2 (16 nov)

Bijlage: `../referenties/blobfish_onderwater.png` (Jordi's plaatje van de blobfish onder water). **Nieuw gesprek, v1 niet meesturen** (GEMINI.md: Gemini kopieert een vorige versie).
Afgekeurde v1: `r1/gemini_v1_afgekeurd.png`.

## Jordi over v1 (letterlijk, 16 nov)
- "dit is niet goed. Je ziet er geen klei in, behalve de kleur (maar is juist leuk als die zo'n play dough kleur krijgt), plus het is niet genoeg deze vis" (bij het plaatje `blobfish_onderwater.png`)
- "en ook weer teveel, op de neus na" / "dat die gewoon de afbeelding verder heeft nagemaakt"
- "de neus mag niet zo hangen, dat moet het grote verschil zijn"
- "en hij moet minder een visvorm hebben, omdat die dus gekleid is"

## Wat er verandert t.o.v. v1
- Klei duidelijk zichtbaar (Claude: hoe Play-Doh eruitziet: gerolde worstjes, platgedrukte lapjes met vorkstreepjes, naden waar stukken tegen elkaar gedrukt zijn, vingerafdrukken).
- Kleur: "zo'n play dough kleur" (welke kleur: niet gezegd, Gemini kiest).
- Anatomie volgens Jordi's plaatje (grote kop, grote ronde borstvinnen, waaierstaart, rugvin), maar het plaatje niet natekenen.
- Minder een visvorm, omdat hij gekleid is.
- Neus hangt niet (het grote verschil met fase 2).
- Rest van v1 (derpy blij, goede lippen, ligt op de bodem) blijft.

## Prompt

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- A blobfish sculpted out of Play-Doh. Pure Water type, the first stage of a two-stage line.
- The attached picture shows the blobfish as it looks deep under water. Use it ONLY for the anatomy, do NOT copy or trace the picture: design a Pokémon. Anatomy: a big, bulbous head, a tapering body, big rounded pectoral fins with fin rays, a small dorsal fin, a fan-shaped tail fin with rays, small eyes and big, thick lips.
- THE NOSE DOES NOT HANG: no drooping, sagging nose over the mouth. The face is firm. This is the big difference with its evolution.

IT MUST CLEARLY READ AS PLAY-DOH
- Because it is modelled out of Play-Doh, it has LESS of a fish shape: hand-modelled dough shapes, not a realistic fish body.
- Bright Play-Doh color (one cheerful toy-dough color), matte.
- Built from dough pieces pressed together, with visible seams where pieces meet.
- The lips are a thick rolled dough sausage pressed onto the face.
- The fins are flattened dough pieces with fork-pressed lines as fin rays.
- A few fingerprint marks on the head.

PERSONALITY
- Slightly derpy and happy, as if it is glad to see you. A goofy smile with those big lips.

POSE
- Three-quarter view facing left, lying flat on its belly as if resting on the sea floor, pectoral fins spread to the sides, looking up at the viewer.

STYLE AND FORMAT
- 64x64 pixel sprite, the creature not filling the whole canvas (first stage), max 16 colors, 1 px dark outline, light from top left, flat Gen 3 shading with 3 to 4 tones per color, no dithering.
- Plain white background. NO floor, sea bed, rocks, shadow, bubbles, water or effects. One single creature, no extra views.

AVOID
- Not a copy of the attached picture. No hanging or drooping nose. Not the collapsed, saggy blobfish; no slime, drool, jelly or gloss.
- Not a plush toy, chibi or Neopets mascot. No glossy 3D render, no claymation photo.
```

## Tips
- Weer te veel een kopie van het plaatje: probeer zonder bijlage (de anatomie staat al in de prompt).
- Te weinig Play-Doh: "made entirely of Play-Doh, like a child's sculpture" bovenaan.
