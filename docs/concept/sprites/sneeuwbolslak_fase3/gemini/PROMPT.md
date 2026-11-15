# Gemini-prompt: sneeuwbolslak fase 3 (Ice/Cosmic), startprompt v1 (15 nov)

Regels: `docs/lessen/GEMINI.md`. Lijn en besluiten: `docs/concept/IDEEEN.md` (Sneeuwbol-Pokémon); fase 1 `sneeuwbolslak/`, fase 2 `sneeuwbolslak_fase2/` (SPEC + gemini/PROMPT.md).
Bijlage: `bijlage_fase2_8x.png` (afgewerkte fase 2), alleen voor ogen, kleuren en de plusvlokken.

## Jordi (letterlijk)
- "ik zat te denken aan een pokemon lijn die begint als snow globe en daarna cosmic wordt"
- "blijft ijs/cosmic. Is leuk als die van snow globe uitgroeit naar een soort cosmisch ijs sferisch ding"
- "Ik zat voor fase 3 te denken aan iets wat een beetje lijkt qua vorm op de interloper uit outer wilds" / "vooral de langwerpige vorm, de donkere kern hoeft niet"
- "in de derde fase barst deze bol compleet en ontstaat er zo de kern van de laatste vorm"
- "fase 3 is dus meteoriet (die we wel ogen geven natuurlijk)" → "sorry komeet bedoel ik"
- Bij de voorstellen voor fase 2 (waaronder "Fase 3: het slakkenlijf gaat op in de staart, het huisje is de komeetkern"): "ja die vind ik tof, maar zorg er wel voor dat het in een sprite uit te beelden blijft."

## Keuzes Claude (Jordi heeft hier niets over gezegd; schrappen of aanpassen mag)
- **Houding:** zwevend (een komeet vliegt); fase 2 moest kruipen, voor fase 3 is niets gezegd.
- **Kern:** waar de bol zat, nu een heldere ijskern zonder glas, met de plusvlokken van fase 1/2 als sterretjes erin (link met de lijn, Cosmic).
- **Staart:** het lijf (Clione-vorm van fase 2) is opgegaan in een lange ijsstaart naar achteren, met de kristallen van fase 2.
- **Mond:** de glimlachlijn van fase 2 blijft (niet besproken).
- **Maat:** vult het 64×64-vak bijna (eindvorm).
- De Interloper wordt in de prompt niet bij naam genoemd (geen herkenbare kopie); alleen de langwerpige vorm wordt beschreven.

## Prompt

```
Attachment 1 is the official-style Gen 3 front sprite of the SECOND stage of an original Pokémon line (pure Ice type): an icy sea-angel-shaped creature carrying a cracked, freezing snow globe with a snowstorm inside. Use it ONLY as a reference for the eye shape, the mouth, the ice colors and the plus-shaped snowflakes. Do NOT copy its body or globe.

Design the FINAL, third stage (Ice / Cosmic type) and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT: a living icy comet.
- The snow globe has burst completely. Where the globe was, the core of the comet has formed: a bright, icy core (no glass any more), with a few plus-shaped snowflakes shining in it like little stars.
- The body has dissolved into the comet: one long, sleek, elongated shape, like a spindle or a stretched teardrop of ice, wide and round at the core and tapering into a long icy tail behind it. A few ice crystals along the tail.
- Light, icy colors like attachment 1, with a hint of deep space blue. NO dark core.
- It has a face at the front of the core: two eyes like attachment 1 and a small smiling mouth line.

KEEP IT READABLE AS A SPRITE
- One clear, elongated silhouette, compact enough to fit a 64x64 sprite. Simple, big shapes; the tail is a few clean ice shapes, not a cloud of particles.

POSE
- Three-quarter view facing left, floating, the core in front and the tail streaming back and up.

STYLE AND FORMAT
- 64x64 pixel sprite, the creature filling most of the canvas (final stage), max 16 colors, 1 px dark outline, light from top left, flat Gen 3 shading with 3 to 4 tones per color, no dithering.
- Plain white background. NO floor, shadow, glow, sparkles, stars or effects outside the creature. No loose or floating pieces. One single creature, no extra views.

AVOID
- No snail body, no glass globe, no snow-globe base, no house.
- No dark or black core, no rock or meteorite look, no fire.
- Not a plush toy, chibi or Neopets mascot. No glossy 3D render.
```

## Tips
- Wordt het een rots/meteoriet: "made of ice, not rock" bovenaan zetten, nieuw gesprek.
- Te breed of te veel deeltjes in de staart: "compact, the tail is 3 or 4 clean ice shapes".
- Niet bijsturen in hetzelfde gesprek na 1–2 keer (GEMINI.md): beste resultaat als bijlage in een nieuw gesprek.
