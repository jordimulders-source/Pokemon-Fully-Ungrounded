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

## Ronde 4 (15 nov), prompt v4
- `r4_gemini.png`. Jordi: "Al iets beter, alleen ik vind de buitenste laag net iets te neutraal, daar mag wat meer ijsschots vorm in".

# Prompt v5 (15 nov): nieuw gesprek, bijlage = `r4_gemini.png`, één wijziging
Let op (GEMINI.md): "keep X, change Y" kan X slopen. Gaan ogen of vorm achteruit: v5b draaien.

```
Attachment 1 is a front sprite of an original Pokémon in official Gen 3 style (Ruby/Sapphire/Emerald pixel art): a living comet of ice, Ice/Cosmic type.

Redraw it with ONE change: the outer layer of ice (the pale white dome and the pale spikes) is too smooth. Give it the shape of ice floes: the surface is made of a few large, flat, angular plates of ice with straight edges and sharp corners, like broken pack ice, slightly overlapping, with thin darker blue lines where the plates meet. Keep it to a few big plates, not many small cracks.

KEEP EXACTLY
- The silhouette and pose: rounded front at the left, spikes and vapor tail sweeping back to the top right.
- The face: the two round, icy cyan eyes, nothing else. No mouth, no eyebrows.
- The dark indigo/violet spikes and the nebula patches, the pale vapor tail, all colors.

FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, flat Gen 3 shading, no dithering.
- Plain white background, no stars, sparkles or effects. One single creature.
```

## Prompt v5b: nieuw gesprek, bijlage = `interloper_referentie.png`
v4 ongewijzigd, met in SHAPE na de eerste regel:
`- The outer layer of ice is not smooth: it is made of a few large, flat, angular plates of ice like ice floes / broken pack ice, with straight edges and sharp corners, slightly overlapping. A few big plates, not many small cracks.`

## Ronde 5 (15 nov), prompt v5
- `r5_gemini.png`. Jordi: "halve bak doet die maar". Gemini tekende alleen naden op de gladde koepel; het silhouet bleef rond.

# Prompt v6 (15 nov): nieuw gesprek, bijlagen = 1. `interloper_referentie.png`, 2. `r4_gemini.png`
Keuze Claude: de ijsschotsen moeten het silhouet zelf veranderen (hoekige omtrek, platen die over elkaar schuiven), niet alleen lijnen op het oppervlak. r4 alleen als bijlage voor gezicht en kleuren.

```
Attachment 1 is the comet "The Interloper" from the game Outer Wilds: reference for the overall shape.
Attachment 2 is an earlier draft of my Pokémon: reference ONLY for the face (two round icy cyan eyes, no mouth) and the colors (pale icy white, indigo and violet spikes, nebula patches, pale vapor tail). Do not copy its smooth rounded head.

Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art): the final stage of an Ice/Cosmic line, a living comet of ice that burst out of a snow globe.

THE OUTER LAYER IS MADE OF ICE FLOES
- The whole front and the outer layer are built from large, thick slabs of pack ice, like broken ice floes pushed on top of each other.
- This must change the SILHOUETTE: the outline is angular, made of straight edges and sharp corners where the slabs stick out. NO smooth round curve anywhere on the head.
- The slabs have thickness: each slab shows a lit top face and a darker blue side edge, and some slabs overlap and tilt up at their edges.
- About 6 to 8 big slabs, not many small cracks, not lines drawn on a smooth surface.
- Behind the slabs, the dark indigo/violet spikes sweep backwards like the Interloper, with a pale vapor tail.

FACE
- Completely neutral: only two round, icy cyan spheres as eyes, set into the front slab, like Lunatone, Solrock and Minior's core. NO mouth, NO eyebrows, NO ridges above the eyes.

POSE
- Three-quarter view facing left, the front at the left, spikes and tail streaming back to the top right.

FORMAT
- 64x64 pixel sprite, a final stage that fills most of the canvas, max 16 colors, 1 px dark outline, light from top left, flat Gen 3 shading, no dithering.
- Plain white background. NO stars, sparkles, aura, particles, floor or shadow. One single creature, no extra views.

AVOID
- No smooth dome, no round head with lines on it. Not a monster, no angry face. Not cute. Not a robot or spaceship (no panels or rivets). No glossy 3D render.
```

## Aanvulling Jordi op v6 (15 nov, vóór het draaien)
- "en dat vuur of wat dan ook wat ervan af komt is ook maar erg halve bak, dat zou wat meer omringend mogen zijn aan het uiteinde. De ogen wil ik wat hoger en nog wat meer laten gloeien, sinister"

# Prompt v7 (15 nov): vervangt v6, zelfde bijlagen (1. `interloper_referentie.png`, 2. `r4_gemini.png`)

```
Attachment 1 is the comet "The Interloper" from the game Outer Wilds: reference for the overall shape, and for how the pale comet tail surrounds the back of the comet.
Attachment 2 is an earlier draft of my Pokémon: reference ONLY for the colors (pale icy white, indigo and violet spikes, nebula patches) and the two round eyes with no mouth. Do not copy its smooth rounded head, its eye position or its thin wisp of vapor.

Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art): the final stage of an Ice/Cosmic line, a living comet of ice that burst out of a snow globe.

THE OUTER LAYER IS MADE OF ICE FLOES
- The whole front and the outer layer are built from large, thick slabs of pack ice, like broken ice floes pushed on top of each other.
- This must change the SILHOUETTE: the outline is angular, made of straight edges and sharp corners where the slabs stick out. NO smooth round curve anywhere on the head.
- The slabs have thickness: each slab shows a lit top face and a darker blue side edge, and some slabs overlap and tilt up at their edges.
- About 6 to 8 big slabs, not many small cracks, not lines drawn on a smooth surface.
- Behind the slabs, the dark indigo/violet spikes sweep backwards like the Interloper.

COMET TAIL
- At the back end, a pale icy-blue comet tail of vapor and gas wraps AROUND the rear of the body, like in attachment 1: it surrounds the spikes above and below and streams back as one broad, soft shape. Not a thin wisp or a single trail of smoke.
- It stays inside the 64x64 square and is attached to the body.

FACE
- Only two round, icy spheres as eyes, like Lunatone, Solrock and Minior's core. Place them HIGH on the front slab, in the upper part of the front.
- The eyes glow strongly with a cold, bright cyan light, with a small halo of glow on the ice around them. Sinister, like something watching you from the dark.
- NO mouth, NO eyebrows, NO ridges above the eyes, NO pupils.

POSE
- Three-quarter view facing left, the front at the left, spikes and tail streaming back to the top right.

FORMAT
- 64x64 pixel sprite, a final stage that fills most of the canvas, max 16 colors, 1 px dark outline, light from top left, flat Gen 3 shading, no dithering.
- Plain white background. NO stars, sparkles, particles, floor or shadow. One single creature, no extra views.

AVOID
- No smooth dome, no round head with lines on it. No mouth, no teeth, no angry brows. Not cute. Not a robot or spaceship (no panels or rivets). No glossy 3D render.
```

## Ronde 6 (15 nov), prompt v7
- `r6_afgekeurd.png`. Jordi: "wat een mislukking".
- Analyse Claude: r4 als bijlage werd weer overgetrokken (zelfde punten en dezelfde dunne sliert rechtsboven), met een ring van gas eraan geplakt en hoekige platen eroverheen. Plus te veel eisen tegelijk (GEMINI.md).

# Prompt v8 (15 nov): nieuw gesprek, ALLEEN bijlage `interloper_referentie.png`
Geen eerdere Gemini-versie meesturen; kleuren en ogen in woorden. Minder eisen.

```
Attachment 1 is the comet "The Interloper" from the game Outer Wilds. Design an original Pokémon with this shape and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

It is the final stage of an Ice/Cosmic line: a living comet of ice that burst out of a snow globe.

SHAPE (follow attachment 1)
- The front is a mass of thick, broken ice floes pushed together: an angular outline with straight edges and sharp corners, slabs that tilt up and overlap.
- From the front, long ice spikes sweep backwards, side by side, like the Interloper.
- A broad, soft comet tail of pale vapor surrounds the back half of the body, above and below the spikes, and streams back to the top right, like the glow around the Interloper.

COLORS
- Pale icy white and light blue on the front, deep indigo and violet on the spikes, with a soft violet nebula visible inside the ice between them. No star shapes.

FACE
- Two round eyes high on the front, glowing bright cold cyan, sinister. Nothing else: no mouth, no eyebrows, no pupils.

POSE AND FORMAT
- Three-quarter view facing left, flying to the left, tail to the top right.
- 64x64 pixel sprite filling most of the canvas, max 16 colors, 1 px dark outline, light from top left, flat Gen 3 shading, no dithering.
- Plain white background, no stars, no space background, no floor. One single creature.
```

## Ronde 7 (15 nov), prompt v8
- `r7_gemini.png`. Jordi: "Dit is de beste tot nu toe, maar ik twijfel over de ogen en de positie".
- Daarna Jordi: "wacht ik weet het, ik ben bijna tevreden, maar ik wil dat die ijsschotsen nog net iets meer op een dier lijken, alsof dat het lichaam is".

# Prompt v9 (15 nov): nieuw gesprek, bijlage = `r7_gemini.png`, één wijziging
Welk dier zei Jordi niet; de prompt noemt er geen (navragen of het de slak van fase 1 moet worden).

```
Attachment 1 is a draft of an original Pokémon in official Gen 3 style (Ruby/Sapphire/Emerald pixel art): a living comet of ice, Ice/Cosmic type, the final stage of a line that started as a snail.

Redraw it with ONE change: the ice floes at the front must look a bit more like an animal, as if the slabs ARE its body. Arrange the same kind of slabs so they read as a creature: the slab with the eyes is clearly its head, and the slabs behind and below it form its body. It stays made of ice floes, only the arrangement changes.

KEEP
- The angular broken-ice-floe look, the colors, the two glowing cyan eyes and no mouth.
- The dark indigo/violet spikes sweeping back, the violet nebula between them, the broad pale vapor tail around the back.
- The direction: flying to the left, tail to the top right.

FORMAT
- 64x64 pixel sprite filling most of the canvas, max 16 colors, 1 px dark outline, light from top left, flat Gen 3 shading, no dithering.
- Plain white background, no stars, no floor. One single creature.
```
