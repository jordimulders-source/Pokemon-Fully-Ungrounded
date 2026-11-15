# Gemini-prompt: ijskomeet (fase 3 sneeuwbolslak-lijn, Ice/Cosmic), v1 (15 nov)

Regels: `docs/lessen/GEMINI.md`. Lijn: `docs/concept/IDEEEN.md` (Sneeuwbol-Pokémon), fase 1: `sprites/sneeuwbolslak/`.

## Jordi (letterlijk)
- 13 nov: "Ik zat voor fase 3 te denken aan iets wat een beetje lijkt qua vorm op de interloper uit outer wilds"; "vooral de langwerpige vorm, de donkere kern hoeft niet".
- 15 nov, over r1a/r1b (prompt uit het Gemini-gesprek van fase 2): "Vind ze echt lachwekkend slecht. Lijken net kirby en mario vijandjes. Het moet iets meer een bol met ijsuiteinden zijn, niet een bal met sterretjes. De kern is geëxplodeerd. Het mag wat meer grotesk zijn, met ijsstulpsels overal, beetje zoals de interloper in outer wilds, het moet ook geen lachgezichtje hebben, ogen wel."

## Afgekeurd
- `r1a_afgekeurd.png`, `r1b_afgekeurd.png`: gladde ronde bal met sterretjes, glimlach, blosjes; staartvinnen als een vis.

## Keuzes Claude (schrappen mag)
- "De kern is geëxplodeerd" gelezen als: de sneeuwbol-kern is opengebarsten en het ijs is naar buiten gegroeid. Navragen bij Jordi.
- Geen bijlage (GEMINI.md: een bijlage wordt gekopieerd; de afgekeurde plaatjes al helemaal niet). Het oude gesprek niet gebruiken: nieuw gesprek.
- Geen woorden als "cute", "stars", "sparkle", "galaxy" in de prompt; het Cosmic-deel zit in de vorm (komeet), niet in sterretjes.
- Ogen: klein en ernstig, geen mond (Jordi: "geen lachgezichtje, ogen wel").

## Prompt

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- The final stage of an Ice/Cosmic line that starts as a snail with a snow globe for a shell. Now it has become a living comet.
- Its core, the old snow globe, has exploded: the round core is burst open and cracked, and ice has erupted out of it in every direction. What is left is a lumpy, round mass of rough ice with jagged ice growths sticking out all over it.
- Shape: elongated like a real comet nucleus, a round lumpy head that stretches back into a long, rough tail of ice. Think of the comet "The Interloper" from the game Outer Wilds: an elongated icy body covered in irregular ice spikes and columns. Only the shape, no dark core.

DESIGN
- A bit grotesque and alien, not cute. Irregular, asymmetric ice protrusions of different sizes all over the body (thick columns, crooked spikes, broken shards), like ice that kept growing out of a cracked shell.
- Cracks in the core where the glass burst, with darker blue depth inside them.
- Face: two small, serious eyes set in the ice at the front of the head. NO mouth, NO smile, NO blush.
- Colors: pale icy blue-white ice, mid blue shadows, deep blue in the cracks. Light from top left.

POSE
- Three-quarter view facing left, the head at the front-left and the tail streaming back to the top right, as if it is flying through space.

STYLE AND FORMAT
- 64x64 pixel sprite, a final stage that fills most of the canvas, max 16 colors, 1 px dark outline, clean flat shading like official Game Freak Gen 3 sprites. No dithering.
- Compact composition: the tail stays inside the square, protrusions close to the body.
- Plain white background. NO stars, sparkles, glow, aura, particles, motion lines, floor or shadow. One single creature, no extra views.

AVOID
- Not a smooth ball, not a round mascot with a tail. Not a Kirby or Mario enemy, not a ghost, not a fish (no fins).
- No stars or star shapes anywhere, on or inside the body.
- No smile, no mouth, no cheeks. Not cute, not a plush toy, no glossy 3D render.
```

## Tips
- Weer te rond/glad: de AVOID-regel "Not a smooth ball" bovenaan zetten, nieuw gesprek.
- Toch sterretjes: "No stars" naar CONCEPT verplaatsen.
- Te druk (te veel kleine stekels): "fewer, bigger ice protrusions (about 6 to 8)".
