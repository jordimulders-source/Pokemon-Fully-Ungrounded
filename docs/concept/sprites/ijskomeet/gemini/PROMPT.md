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

## Ronde 2 (15 nov), prompt v1
- `r2_afgekeurd.png`. Jordi: "dit klopt niet, ik vind het nog teveel kiddy qua ogen en mond, plus de barst zit niet meer in deze pokemon, deze pokemon is de kern die uit de barst gekomen is en daardoor evolved is".
- Mijn lezing van "kern is geëxplodeerd" (barsten in de kern) was dus fout.

# Prompt v2 (15 nov): nieuw gesprek, geen bijlage

Keuzes Claude (schrappen mag): ogen als smalle spleten zonder pupilglans (studie GEMINI.md: mysterieus in Gen 3 = klein, donker lid, geen ronde glimmende iris). Geen schaal of glasresten in beeld: Jordi noemde ze niet.

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- The final stage of an Ice/Cosmic line. The earlier stages were a snail whose shell was a snow globe. Inside that globe a core of ice grew, until it burst out through the cracks of the globe. This Pokémon IS that core: it broke free, and by doing so it evolved into a living comet.
- The body itself is whole and unbroken: no cracks, no holes, no broken glass on it. It is a solid, lumpy sphere of rough ice with jagged ice growths sticking out all over it.
- Shape: elongated like a real comet nucleus, the round lumpy core at the front stretching back into a long, rough tail of ice. Think of the comet "The Interloper" from the game Outer Wilds: an elongated icy body covered in irregular ice spikes and columns. Only the shape, no dark core.

DESIGN
- Grotesque and alien, not cute. Irregular, asymmetric ice protrusions of different sizes all over the body (thick columns, crooked spikes, shards), as if the ice keeps growing out of it.
- Face: only two eyes, small, narrow and cold, like slits in the ice, set deep at the front of the core. NO mouth, NO eyebrows, NO cheeks. The face must not look friendly, angry or cartoonish: it should feel like something ancient and unknown watching you.
- Colors: pale icy blue-white ice, mid blue shadows, deep blue in the darkest places. Light from top left.

POSE
- Three-quarter view facing left, the core at the front-left and the tail streaming back to the top right, as if it is flying through space.

STYLE AND FORMAT
- 64x64 pixel sprite, a final stage that fills most of the canvas, max 16 colors, 1 px dark outline, clean flat shading like official Game Freak Gen 3 sprites. No dithering.
- Compact composition: the tail stays inside the square, protrusions close to the body.
- Plain white background. NO stars, sparkles, glow, aura, particles, motion lines, floor or shadow. One single creature, no extra views.

AVOID
- No cracks or fractures on the body, no broken shell, no glass.
- No mouth, no frown, no smile, no big round eyes, no eye shine. Not a children's cartoon, not a Kirby or Mario enemy, not a mascot.
- Not a smooth ball, not a ghost, not a fish (no fins). No stars or star shapes anywhere.
- No glossy 3D render.
```

## Na v2 (15 nov), vóór Jordi hem draaide
- Jordi: "en het is nog niet cosmic genoeg". Voorstellen Claude: ruimtekleuren (indigo/violet in de diepe delen), echte komeetstaart van ijsdamp/gas, ruimte met nevel in doorzichtige plekken van het ijs, ogen die koud oplichten. Jordi: "allemaal wel goede suggesties, qua ogen kan je kijken naar oa minior, lunatone en solrock, dat zijn ook niet blije lachende stenen".
- Ogenstudie (repo-sprites): Lunatone: één oog diep in een donkere kas, rode iris met donkere ring; Solrock: ogen verzonken in de steen, gekleurde ring met rode pupil; Minior-kern: grote bleke oplichtende ogen zonder pupil. Alle drie: geen mond, geen wenkbrauwen of oogleden, het oog zit ín het gesteente. `ogen_studie.png`.

# Prompt v3 (15 nov): nieuw gesprek, geen bijlage (vervangt v2)

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- The final stage of an Ice/Cosmic line. The earlier stages were a snail whose shell was a snow globe. Inside that globe a core of ice grew, until it burst out through the cracks of the globe. This Pokémon IS that core: it broke free, and by doing so it evolved into a living comet from deep space.
- The body itself is whole and unbroken: no cracks, no holes, no broken glass on it. It is a solid, lumpy sphere of rough ice with jagged ice growths sticking out all over it.
- Shape: elongated like a real comet nucleus, the round lumpy core at the front stretching back into a long, rough tail of ice. Think of the comet "The Interloper" from the game Outer Wilds: an elongated icy body covered in irregular ice spikes and columns. Only the shape, no dark core.

COSMIC
- Space-frozen colors: pale icy blue-white on the lit surfaces, turning into deep indigo and violet in the shadows, the hollows and towards the tail, as if the ice froze in the darkness of space.
- A few translucent patches in the ice show deep space inside: dark indigo with a soft violet nebula. Only nebula clouds, no star shapes.
- Behind the ice tail, a real comet tail: a thin, pale trail of icy vapor and gas streaming back, attached to the body. This is the only soft, glowing part.

DESIGN
- Grotesque and alien, not cute. Irregular, asymmetric ice protrusions of different sizes all over the body (thick columns, crooked spikes, shards), as if the ice keeps growing out of it.
- Face: only two eyes, set deep into the ice like the eyes of Lunatone, Solrock and Minior's core: each eye sits in a dark socket in the ice and glows with a cold light (pale cyan or violet), unblinking, no eyelids, no eyebrows. NO mouth. The face must not look friendly, angry or cartoonish: like an ancient object from space that is watching you.
- Light from top left.

POSE
- Three-quarter view facing left, the core at the front-left and the tail streaming back to the top right, as if it is flying through space.

STYLE AND FORMAT
- 64x64 pixel sprite, a final stage that fills most of the canvas, max 16 colors, 1 px dark outline, clean flat shading like official Game Freak Gen 3 sprites. No dithering.
- Compact composition: the tails stay inside the square, protrusions close to the body.
- Plain white background. NO separate stars, sparkles, aura, particles, motion lines, floor or shadow. One single creature, no extra views.

AVOID
- No cracks or fractures on the body, no broken shell, no glass.
- No mouth, no frown, no smile, no cheeks, no cute round cartoon eyes with a white shine dot. Not a children's cartoon, not a Kirby or Mario enemy, not a mascot.
- Not a smooth ball, not a ghost, not a fish (no fins). No star shapes anywhere, on or inside the body.
- No glossy 3D render.
```

## Ronde 3 (15 nov), prompt v3
- `r3_afgekeurd.png`. Jordi: "het is nu weer teveel een monster, boze ogen, boze mond. Dat wil ik niet. Hij moet heel neutraal zijn, gewoon 2 ogen en geen mond, die ogen zijn ijzige spheren die passen bij het idee. Beetje zoals bij lunatone, minior en solrock. Het design zelf is iets beter, maar qua vorm heb ik nog liever wat meer iets als de interloper."
- Jordi stuurde een beeld van de Interloper mee: `interloper_referentie.png` (ronde voorkant, lange ijspunten die allemaal naar achteren wijzen, langs de vliegrichting, gasstaart eromheen).

# Prompt v4 (15 nov): nieuw gesprek, bijlage = `interloper_referentie.png` (vervangt v3)

Keuzes Claude (schrappen mag): de Interloper als bijlage alleen voor de vorm (geen Pokémon-ontwerp, dus overnemen is hier juist de bedoeling); de donkere rotsplekken op de voorkant expliciet weg (Jordi 13 nov: "de donkere kern hoeft niet"). Kleuren en nevel uit v3 blijven ("design iets beter").

```
Attachment 1 is the comet "The Interloper" from the game Outer Wilds. Use it ONLY as the reference for the shape.

Design an original Pokémon based on this shape and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- The final stage of an Ice/Cosmic line. The earlier stages were a snail whose shell was a snow globe. Inside that globe a core of ice grew, until it burst out of the globe. This Pokémon IS that core: it broke free and evolved into a living comet from deep space.

SHAPE (follow attachment 1)
- A smooth, rounded dome of ice at the front, where the face is.
- From the dome, long ice spikes all sweep BACKWARDS, side by side, in the direction of the tail, like the Interloper. They are long, pointed, slightly different in length, and all point back. No spikes sticking out sideways or forwards.
- The body is whole: no cracks, no holes, no broken glass. No dark rocks on the front, only ice.

COSMIC
- Pale icy blue-white on the lit surfaces, turning into deep indigo and violet in the shadows between the spikes and towards the back.
- One or two translucent patches in the ice show deep space inside: dark indigo with a soft violet nebula. No star shapes.
- Around and behind the spikes, a thin, pale comet tail of icy vapor and gas streaming back, attached to the body. This is the only soft, glowing part.

FACE
- Completely neutral, no emotion: just two eyes and nothing else.
- The eyes are two round, icy spheres set into the dome, glowing with a cold pale cyan light, like the eyes of Lunatone, Solrock and Minior's core: calm, unblinking, no pupils or a tiny one, no eyelids.
- NO mouth, NO teeth, NO eyebrows, NO frown, NO ridges or brow shapes above the eyes. The face is smooth ice around the two eyes.

POSE
- Three-quarter view facing left, the dome at the front-left and the spikes and tail streaming back to the top right, as if it is flying through space.

STYLE AND FORMAT
- 64x64 pixel sprite, a final stage that fills most of the canvas, max 16 colors, 1 px dark outline, clean flat shading like official Game Freak Gen 3 sprites. No dithering.
- Compact composition: the spikes and tail stay inside the square.
- Plain white background. NO black space background, NO separate stars, sparkles, aura, particles, motion lines, floor or shadow. One single creature, no extra views.

AVOID
- Not a monster: no angry eyes, no mouth, no teeth, no skull-like face.
- Not cute: no smile, no cheeks, no cartoon eyes with a white shine dot.
- Not a smooth ball, not a spiky ball with spikes in every direction, not a ghost, not a fish. No glossy 3D render.
```
