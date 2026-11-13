# Gemini-prompt: sneeuwbolslak fase 2 (Ice), startprompt v1 (13 nov)

Regels: `docs/lessen/GEMINI.md`. Lijn en besluiten: `docs/concept/IDEEEN.md` (Sneeuwbol-Pokémon). Fase 1: `sneeuwbolslak/SPEC.md`.
Bijlagen: 1. `bijlage_fase1_8x.png` (de afgewerkte fase 1, 8× vergroot op wit). 2. Zelf toevoegen (Jordi): dezelfde tuinslakfoto als bij fase 1, of een foto van een slak met een duidelijk spiraalhuis.

## Jordi (letterlijk)
- "2 of 3 ben ik niet uit, blijft ijs/cosmic." / "Ik dacht wel als puur ijs type beginnen die je vroeg kan encounteren, dus mogelijk is 3 fases game technisch logisch dan"
- "ik vind de slak wel een goed idee, fase 2 is echter nog niet echt een vooruitgang."
- Fase 3: "iets wat een beetje lijkt qua vorm op de interloper uit outer wilds" / "vooral de langwerpige vorm, de donkere kern hoeft niet".
- Op de voorstellen fase 2: "ja die vind ik tof, maar zorg er wel voor dat het in een sprite uit te beelden blijft."

## De goedgekeurde voorstellen fase 2 (IDEEEN.md)
1. Het huisje groeit door als echte slakkenspiraal en wordt langwerpig (bol → gedraaid ijshuis → komeetvorm).
2. Een ijskorst groeit over het glas; de bol is nog door barsten te zien.
3. De sneeuw binnenin wordt een sneeuwstorm.
4. Het slijmspoor bevriest tot een spoor van rijp (voorbode van de kometenstaart).

## Keuzes Claude in de prompt (Jordi heeft hier niets over gezegd; schrappen of aanpassen mag)
- **Rijpspoor (4):** GEMINI.md verbiedt ondergrond, en een los spoor op de grond leest in een sprite als vloer. Daarom gevraagd als bevroren, rijpige punt aan het staarteinde van het slakkenlijf, vast aan het lijf. Wil Jordi een echt spoor achter de slak: zeggen, dan gaat die regel eruit.
- **Het minuscule huisje in de bol:** niet besproken voor fase 2. In de prompt: verdwijnt half in de sneeuwstorm (alleen het dak te zien). Alternatieven: helemaal weg, of gewoon zichtbaar.
- **Roodbruin voetstuk:** niet besproken. In de prompt: blijft als de ring waar het huis aan het lijf vastzit (herkenbaar als dezelfde lijn).
- **Kop, ogen, lijfkleur:** zoals fase 1 (lichtblauw-wit, oogstelen). De Surskit-ogen tekent Gemini toch niet na; die doet de maker later weer.
- **Maat:** groter dan fase 1 (46 px), ± 56 px breed, nog niet het hele vak (fase 3 vult het).

## Prompt

```
Attachment 1 is the official-style Gen 3 front sprite of an original Pokémon: a small snail whose shell is a snow globe (pure Ice type, first stage of three). Attachment 2 is a real snail for anatomy.

Design its EVOLUTION (second stage, still pure Ice type) and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT: the snow globe is turning into a comet. This stage is the halfway point between a round snow globe and a long, sleek comet.
- The shell: the round glass globe has grown into a real snail spiral and has become elongated, a twisted shell of ice, longer than it is tall, pointing backwards (away from the head).
- A crust of ice has grown over the glass. Through cracks in the crust you can still see the glass globe inside.
- Inside the globe the gentle snowfall has become a snowstorm: dense swirling white snow, the tiny house half lost in it (only its roof visible).
- The reddish-brown snow-globe base is still there as the ring where the shell attaches to the body.
- The slime of the snail has frozen: the tail end of the foot turns into a frosty, rimy tip, attached to the body (a first hint of a comet tail).
- Same creature, clearly grown up: same pale icy blue-white body, same snail head with two long eye stalks and two short lower tentacles, a bit bigger and more confident.

KEEP IT READABLE AS A SPRITE
- One clear silhouette: low snail body, long twisted ice shell on top. Max 3 or 4 cracks, big and simple. The storm is white pixels and small swirls, not noise.
- The glass reads by one highlight on the visible part of the globe; the ice crust is a separate, slightly bluer and harder color with angular edges.

POSE
- Three-quarter view facing left, crawling forward, eye stalks up, like attachment 1.

STYLE AND FORMAT
- 64x64 pixel sprite, the creature larger than the first stage but not filling the whole canvas (there is a third stage), max 16 colors, 1 px dark outline, light from top left, flat Gen 3 shading with 3 to 4 tones per color, no dithering.
- Compact composition, everything close to the body.
- Plain white background. NO floor, slime trail on the ground, snow on the ground, shadow, base platform, glow, sparkles or effects outside the creature. One single creature, no extra views.

AVOID
- Not a snail carrying a separate globe or ice block: the shell is its own body part.
- No stars, galaxy, planets or space colors yet (those come in the third stage). No dark core.
- No big ice spikes or crystal clusters sticking out; the shell stays one smooth, elongated spiral shape.
- Not a plush toy, chibi or Neopets mascot. No glossy 3D render.
```

## Tips
- Gemini maakt de schelp weer rond of zet een losse bol erop: de AVOID-zin "own body part" naar boven, nieuw gesprek.
- Te druk (veel barsten, ruis in de bol): "max 3 cracks", "storm: about 15 white pixels and 2 swirls".
- Gaat het mis, niet bijsturen in hetzelfde gesprek (GEMINI.md): beste resultaat als bijlage in een nieuw gesprek.

## Reactie Jordi op r1 (13 nov)
- "het huis is iets teveel nu een bol met ijs erop. Dat die scheurt en gaat open breken en chaotischer wordt zie ik zitten, ik vind eigenlijk de slak zelf nog teveel van hetzelfde, die moet al meer hints geven richting eindfase, dat we de kosmische kant op gaan, zonder echt het weg te geven"
- Voorstellen Claude: A1 korst breekt open (scherven kantelen naar buiten), A2 losse zwevende scherven, A3 storm lekt door de barsten, A4 bol en korst één klomp; B1 vuile sneeuwbal, B2 lijf naar indigo, B3 gestroomlijnd lijf (oogstelen naar achteren), B4 langere staart, B5 sterglans in de ogen.
- Jordi: "ik vind het wel tof dat de bol bevriest en al wat meer de komeet weggeeft, barsten prima, scherven die naar buiten kantelen kunnen we niet uitbeelden, losse scherven ook niet. Langere staart prima, de slak moet minder slak worden en al meer richting kosmisch ontwerp gaan, kan je daarmee vooruit? Gestroomlijnd lijf ook goed"
- Dus: wel bol bevriest + barsten, B3, B4, minder slak/meer kosmisch. Niet: A1-scherven, A2. Niet genoemd en dus niet in de prompt: A3, B1, B2, B5.

# Prompt v2 (13 nov): nieuw gesprek

Bijlagen: 1. `bijlage_fase1_8x.png` (fase 1), 2. `r1_gemini.png` (eerste poging fase 2).
Keuzes Claude (schrappen mag): voetstuk en lijfkleur blijven (niet besproken, stonden in r1 zonder bezwaar); de inhoud van de bol niet genoemd behalve dat hij bevriest; nog steeds geen sterren/galaxy (Jordi: "zonder echt het weg te geven").

```
Attachment 1 is the official-style Gen 3 front sprite of an original Pokémon: a small snail whose shell is a snow globe (pure Ice type, first stage of three). Its final stage will be a long, sleek icy comet (Ice/Cosmic). Attachment 2 is a first attempt at the second stage: the direction is right, but it is still too much a snail with an ice-covered ball on its back.

Design the SECOND STAGE (still pure Ice type) and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT: halfway between the snow-globe snail and the comet. Less of a snail, more towards a cosmic design: it should hint at the comet it will become, without giving it away.
- The globe is freezing solid: frozen, frosted ice that already looks more like the icy core of a comet than a glass ball. Big, simple cracks run through it. It stays one solid shape.
- Streamlined body: longer and lower, built for speed, the eye stalks swept back.
- A longer tail: the frozen tail end streams out backwards in a long frosty trail, attached to the body, a clear start of a comet tail.
- Keep the link with attachment 1: pale icy blue-white body, the reddish-brown snow-globe base as the ring where the frozen globe attaches to the body.

KEEP IT READABLE AS A SPRITE
- One clear, elongated silhouette, low and long, everything pointing backwards. Max 3 or 4 cracks, big and simple.

POSE
- Three-quarter view facing left, moving forward.

STYLE AND FORMAT
- 64x64 pixel sprite, the creature larger than the first stage but not filling the whole canvas (there is a third stage), max 16 colors, 1 px dark outline, light from top left, flat Gen 3 shading with 3 to 4 tones per color, no dithering.
- Compact composition, everything attached to the body.
- Plain white background. NO floor, trail on the ground, snow on the ground, shadow, base platform, glow, sparkles or effects outside the creature. No loose or floating pieces. One single creature, no extra views.

AVOID
- Not a snail carrying a ball: the frozen globe is its own body part.
- No ice blocks or brick pattern, no cone or drill shape.
- No stars, galaxy or planets.
- Not a plush toy, chibi or Neopets mascot. No glossy 3D render.
```

## Reactie Jordi op r2 (13 nov)
- `r2_gemini.png`. Jordi: "compleet mislukt".
- Analyse Claude: "less snail, more cosmic" vertaalde Gemini als kop weglaten (haakvormige stomp zonder gezicht); "freezing solid" genegeerd (glazen bol met huisje, alleen barsten); de bijlagen trokken hem terug naar de bol van fase 1. Abstracte woorden werken niet; Gemini heeft concrete vormen nodig.
- Jordi verder over r2: "dit is toch verschrikkelijk", "alles hieraan is slecht"; "die eerste was beter".

## Ronde 3 (13 nov)
- `r3_gemini.png` (door Jordi zelf geprompt). Jordi: "Dit is nog teveel de eerste vorm. Het is een beetje waar ik vooraf bang voor was, fase 2 lijkt teveel op fase 1. Hoe gaan we een tussenfase creëren die tussen die slak in zit en een komeet. De slak moet al langzaam dus meer opgaan. De bol moet bevriezen, maar minder puntig en het moet allemaal langzaam 1 geheel vormen. De chaos in de bol die begint te ontstaan ben ik wel fan van, alsof de laatste vorm nu in de bol zit en zodra die barst de hele pokemon overneemt. Laten we eerst overleggne voordat we prompten"
