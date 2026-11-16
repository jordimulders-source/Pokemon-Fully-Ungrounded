# Gemini-prompt: blobfish fase 1 (Water), startprompt v1 (16 nov)

Regels: `docs/lessen/GEMINI.md`. Lijn en besluiten: `docs/concept/IDEEEN.md` (Blobfish-lijn).
Bijlage: zelf toevoegen (Jordi): een foto van een blobfish **zoals hij onder water in de diepte is** (niet de ingezakte versie aan boord).

## Jordi (letterlijk)
- Typing: Water → Water (16 nov).
- "ja de boetseerklei is wel een goede voor fase 1, die is dan licht derpy blij, lijkt voor de rest echt op de blobfish als die onderwater is, goede lippen dus, blij om je te zien lijkt wel, ligt op de bodem. Wel duidelijk van klei"
- (Concept Claude dat hij koos: "Fase 1 is een netjes geboetseerd vissenfiguurtje. Fase 2 is natte klei die zijn vorm verliest en uitzakt, met vingerafdrukken nog zichtbaar." Voor fase 2 koos Jordi daarna iets anders, zie `blobfish_fase2/gemini/PROMPT.md`.)

## Keuzes Claude (Jordi heeft hier niets over gezegd; schrappen of aanpassen mag)
- **Kleur:** roze-grijze klei (de kleur van een blobfish), mat, geen glans.
- **Klei zichtbaar maken:** een paar vingerafdruk-/boetseersporen en een grove, handgemaakte vorm; geen speelgoed-glans.
- **Maat:** basisvorm van een 2-fasenlijn, vult het 64×64-vak niet helemaal.
- **Geen bodem getekend** (GEMINI.md: nooit ondergrond); "ligt op de bodem" alleen als houding: plat op de buik, vinnen opzij.

## Prompt

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- A blobfish made of modelling clay. Pure Water type, the first stage of a two-stage line.
- The attached photo is a real blobfish as it looks deep under water (NOT the collapsed blob above water): use it for the anatomy. Big round head, body tapering into a short tail like a tadpole, small fins, small eyes, and big, well-defined lips.
- It looks exactly like that living blobfish, but it is clearly sculpted from clay: matte surface, a few fingerprint and sculpting marks, slightly lumpy hand-made shapes. Clay is the material, it is still one living creature.

PERSONALITY
- Slightly derpy and happy, as if it is glad to see you. A goofy, friendly smile with those big lips.

DESIGN
- Color: pinkish-grey clay, matte, no shine. Simple, few colors.
- Readable silhouette: big head, tapering body, fins visible.

POSE
- Three-quarter view facing left, lying flat on its belly as if resting on the sea floor, fins spread to the sides, looking up at the viewer.

STYLE AND FORMAT
- 64x64 pixel sprite, the creature not filling the whole canvas (first stage), max 16 colors, 1 px dark outline, light from top left, flat Gen 3 shading with 3 to 4 tones per color, no dithering.
- Plain white background. NO floor, sea bed, rocks, shadow, bubbles, water or effects. One single creature, no extra views.

AVOID
- Not the collapsed, saggy blobfish face; no slime, no drool, no jelly or gloss.
- Not a plush toy, chibi or Neopets mascot. No glossy 3D render, no claymation photo.
```

## Tips
- Wordt het de ingezakte blob: "the deep-sea form, a normal fish shape, NOT the collapsed blob" bovenaan zetten, nieuw gesprek.
- Leest het niet als klei: "visible fingerprints, matte, hand-sculpted" sterker maken.
- Niet bijsturen na 1–2 keer (GEMINI.md): beste versie als bijlage in een nieuw gesprek.
