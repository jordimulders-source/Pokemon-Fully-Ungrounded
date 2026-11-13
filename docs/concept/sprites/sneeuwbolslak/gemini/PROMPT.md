# Gemini-prompt: sneeuwbolslak (fase 1, Ice), startprompt v1 (13 nov)

Regels: `docs/lessen/GEMINI.md`. Lijn en besluiten: `docs/concept/IDEEEN.md` (Sneeuwbol-Pokémon).
Bijlage: zelf toevoegen (Jordi): een foto van een gewone tuinslak (zijaanzicht, voelsprieten uit).

## Jordi (letterlijk)
- "ik zat te denken aan een pokemon lijn die begint als snow globe en daarna cosmic wordt"
- "de sneeuwglobe moet wel een soort hybride zijn, kan niet alleen een bol zijn."
- "Ik dacht wel als puur ijs type beginnen die je vroeg kan encounteren"
- "ik vind de slak wel een goed idee"
- "ja die vind ik tof, maar zorg er wel voor dat het in een sprite uit te beelden blijft."

## Gekozen (Jordi, 13 nov: "1c en 2a")
- Wat er in de bol staat: C, een minuscuul huisje.
- Kleur van het slakkenlijf: A, lichtblauw-wit.

## Keuzes Claude voor leesbaarheid in een sprite (schrappen mag)
- Bol rond en relatief groot (± de helft van de sprite), met één lichtvlek linksboven en 3–5 sneeuwpixels: glas lees je in Gen 3 aan de lichtvlek, niet aan transparantie.
- Het voetstuk van de sneeuwbol is waar het huisje aan het lijf vastzit (de slak draagt de bol op zijn rug als huisje).
- Klein, vroeg vangbaar: het beestje vult de 64×64 niet helemaal.

## Prompt

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- A small snail whose shell is a snow globe. Pure Ice type, the first stage of a three-stage line, an early-game Pokémon.
- It is ONE creature, a true hybrid: the glass globe IS its shell and grows from its back. The round base of the snow globe (like the wooden/plastic base of a souvenir snow globe) is where the shell attaches to the snail's body.
- Inside the globe: a tiny house, with a few snowflakes floating around it. Keep the contents very simple so they read at sprite size.
- The attached photo is a real garden snail: use it for the anatomy of the body (soft foot, two long eye stalks with the eyes on top, two short lower tentacles).

DESIGN
- Body color: pale icy blue-white. Simple, cute but not a plush toy.
- The globe is large and round, about half of the sprite. Show the glass with one clear highlight in the top left and a darker edge, NOT with see-through effects. 3 to 5 white snow pixels inside.
- Readable silhouette: snail body low and long, round globe on top, eye stalks clearly visible.

POSE
- Three-quarter view facing left, crawling forward, eye stalks up and curious.

STYLE AND FORMAT
- 64x64 pixel sprite, the creature smaller than the canvas (it is a first stage), max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Compact composition, everything close to the body.
- Plain white background. NO floor, slime trail, snow on the ground, shadow, base platform, glow, sparkles or effects outside the globe. One single creature, no extra views.

AVOID
- Not a snail carrying or sitting next to a separate snow globe: the globe must be its own shell.
- No spiral shell drawn on or around the globe. No crystals or ice spikes yet (those come in later stages).
- No face on the globe, no stars or galaxy inside the globe.
- Not a plush toy, chibi or Neopets mascot. No glossy 3D render.
```

## Tips
- Gemini zet een losse bol naast de slak: de AVOID-zin over "own shell" naar boven halen, nieuw gesprek.
- Bol te druk (veel vlokken, landschap): "contents: only 3 snowflakes" en het beste resultaat als bijlage in een nieuw gesprek.

---

# Prompt v2 (13 nov): nieuw gesprek, r1 als bijlage

Jordi: "ja schrijf die prompt, voetstuk mag blijven". Bijlagen: 1. `r1_gemini.png`, 2. de tuinslakfoto.
Keuzes Claude (schrappen mag): kleine mond op de kop; schaduw op het lijf iets blauwer zodat het glas lichter afsteekt (lijf blijft lichtblauw-wit). Rafelige onderkant: Jordi heeft niets gezegd; de prompt vraagt een strakke omlijning, zoals v1.
Let op (GEMINI.md): "keep X, change Y" kan ook X slopen. Gaat het silhouet of de bol achteruit: v1 opnieuw in een nieuw gesprek draaien.

```
Attachment 1 is a draft of an original Pokémon: a small snail whose shell is a snow globe (pure Ice type, first stage, early game). Attachment 2 is a real garden snail for anatomy.

Redraw it as a clean official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

KEEP EXACTLY
- The silhouette and pose: low snail body facing left, large round glass globe on its back, two eye stalks up.
- The globe: the tiny house inside, a few snowflakes, one highlight in the top left.
- The reddish-brown snow-globe base that attaches the globe to the body.
- Body color pale icy blue-white.

FIX ONLY THESE
1. The head: make it a clear, rounded snail head (use the real snail in attachment 2) with a simple cute face: the eyes are clearly visible dark eyes at the tips of the two long eye stalks, and a small mouth. Two short lower tentacles, smooth, not lumpy stubs. No extra bumps or growths.
2. Contrast: the globe needs a dark 1 px outline all around, including the left side. Shade the body with slightly bluer, darker tones so the glass reads lighter than the body and they do not blend together.
3. Shading: flat Gen 3 shading in 3 to 4 tones per color. NO dithering or checkerboard patterns.
4. Outline: one clean, closed 1 px dark outline around the whole creature, also along the bottom of the foot (no ragged or melting edge).

FORMAT
- 64x64 pixel sprite, the creature smaller than the canvas, max 16 colors, light from top left.
- Plain white background. NO floor, slime trail, shadow, glow, sparkles or effects outside the globe. One single creature, no extra views.

AVOID
- Do not change the shape or size of the globe, do not add a spiral shell, crystals, ice spikes, stars or a face on the globe.
- Not a plush toy, chibi or Neopets mascot. No glossy 3D render.
```
