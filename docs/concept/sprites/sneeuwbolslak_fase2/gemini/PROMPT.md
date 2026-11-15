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
- Voorstel Claude: fase 2 als cocon (Shelgon/Kakuna/Silcoon): ijs over het hele lijf, één ronde ei-/druppelvorm, kopje piept vooraan uit, rond venster met de chaos, barsten over de cocon. Open: a. inhoud draaikolk, b. huisje, c. voetstuk, d. staart.
- Jordi: "ik wil liever geen oogstelen maar in vorm 2" En: "fase 1 is echt een slak en vanaf fase 2 stappen we daar al van af".
- Voorstel Claude: cocon met gezicht (1a ogen in het ijs, 1b venster is oog, 1c geen gezicht) + open a–d. Jordi: "fase 3 is dus meteoriet (die we wel ogen geven natuurlijk)"
- Jordi: "sorry komeet bedoel ik, fase 2 krijgt ook ogen, want er zijn weinig pokemon zonder ogen"
- Jordi: "1a, dat blijft qua vorm vergelijkbaar met fase 1, a2, b2 indien mogelijk, c1, d1"
- Dus: ogen in het ijs vooraan, door een spleet (vorm vergelijkbaar met fase 1); in de draaikolk één helder lichtpunt; huisje nog net zichtbaar (indien mogelijk); voetstuk als ring rond de cocon; korte ronde staart naar achteren.

# Prompt v3 (15 nov): cocon, nieuw gesprek

Bijlage: alleen `bijlage_fase1_8x.png`, uitdrukkelijk alleen voor ogen en kleuren (les r2: een bijlage trekt Gemini terug naar de oude vorm; gaat dat mis, dan zonder bijlage opnieuw).
Keuzes Claude (schrappen mag): ei-/druppelvorm iets langer naar achteren (Jordi: "langzaam 1 geheel", "minder puntig"; Interloper-richting); ± 56 px; geen mond (niet besproken).

```
Attachment 1 is the official-style Gen 3 front sprite of the FIRST stage of an original Pokémon line: a snail with a snow globe as its shell (Ice type). Use it ONLY as a reference for the eye shape and the color palette. Do NOT copy its snail body, eye stalks or globe.

Design the SECOND STAGE (pure Ice type) and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art). The final third stage will be an icy comet.

CONCEPT: a cocoon stage, like Shelgon, Kakuna or Silcoon. The snail is gone: it has frozen into one smooth, solid shell of ice. The comet is growing inside and will break out.
- Shape: one single rounded egg/teardrop shape of frosted ice, slightly longer towards the back, smooth and rounded, NO points or spikes.
- Eyes: two eyes peeking out through a narrow slit in the ice at the front, the same eye shape as in attachment 1. No eye stalks, no head sticking out, no mouth.
- Window: on the side of the cocoon there is a round window of clear glass (what is left of the snow globe). Behind it, a wild swirling vortex of snow, with one bright point of light in the center, the core of the comet. If it fits, a tiny house is just barely visible in the storm.
- A few large, simple cracks run from the window over the ice, as if it is about to burst.
- The reddish-brown snow-globe base is now a ring around the cocoon.
- A short, rounded frozen tail at the back, the first hint of a comet tail. Attached to the body.

KEEP IT READABLE AS A SPRITE
- One clear, simple silhouette: a smooth ice egg with a short tail. Max 3 or 4 cracks. The vortex is white swirls and pixels around one bright point, not noise.
- Ice reads by flat Gen 3 shading and one highlight in the top left.

POSE
- Three-quarter view, the front (with the eyes) facing left, resting on the ground.

STYLE AND FORMAT
- 64x64 pixel sprite, the creature about 56 pixels wide (larger than the first stage, not filling the whole canvas), max 16 colors, 1 px dark outline, light from top left, flat Gen 3 shading with 3 to 4 tones per color, no dithering.
- Plain white background. NO floor, snow on the ground, shadow, glow, sparkles or effects outside the creature. No loose or floating pieces. One single creature, no extra views.

AVOID
- No snail body, no foot, no eye stalks, no tentacles, no shell spiral or cone.
- No ice blocks or brick pattern, no ice spikes or crystal clusters.
- No stars, galaxy or planets outside the bright core.
- Not a plush toy, chibi or Neopets mascot. No glossy 3D render.
```

## Ronde 4 (15 nov)
- `r4_gemini.png` (prompt v3). Jordi: "dit is veel minder mooi dan wat we al hadden".
- Analyse Claude: grijze klomp (steen/zeehond, geen ijs of glas), het voetstuk werd een rode raamlijst, de draaikolk een sterrenstelsel (verraadt de eindvorm), geen huisje; alles wat fase 1 charmant maakte (glas, sneeuw, huisje, lichtblauw) is weg.
- Jordi verder over r4: "het is juist nog minder de vorm die ik wilde hebben, verder klopt het niet samen, het is ook geen duidelijke snowglobe meer"
- Claude bood aan: Jordi beschrijft de vorm, of een ontwerpvel met vier varianten. Jordi: "doe maar een totaal nieuwe prompt".

# Prompt v4 (15 nov): totaal nieuw, nieuw gesprek

Bijlage: `bijlage_fase1_8x.png`, alleen voor ogen en kleuren.
Alles uit Jordi's woorden (zie hierboven): slak gaat op, geen oogstelen, wel ogen (vorm als fase 1); bol bevriest, minder puntig, alles langzaam één geheel; duidelijke sneeuwbol; chaos in de bol alsof de eindvorm erin zit; barsten; gestroomlijnd; langere staart; lichtpunt; huisje indien mogelijk; voetstuk als ring; geen scherven.
Keuzes Claude (schrappen mag): ogen vooraan op het lijf onder/vóór de bol (zonder kop moeten ze ergens zitten); de bol vooraan en het lijf dat erachter uitloopt in de staart (zo wijst alles naar de komeetvorm); ± 56 px.

```
Attachment 1 is the official-style Gen 3 front sprite of the FIRST stage of an original Pokémon line: a snail whose shell is a snow globe (pure Ice type). Use it ONLY as a reference for the eye shape, the colors and the snow-globe details. The line ends in a long, sleek icy comet.

Design the SECOND STAGE (pure Ice type) and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT: the in-between stage. It is no longer a snail: the snail has slowly dissolved into its snow globe, and body and globe are growing together into one streamlined whole, halfway towards a comet.
- It is still clearly a SNOW GLOBE: a big round glass globe with snow inside and the reddish-brown snow-globe base, which is now a ring where the globe meets the body.
- The globe is freezing: frost creeps over the glass from the edges, and a few big, simple cracks run through it. Rounded and smooth, no points or spikes.
- Inside the globe chaos is starting: a swirling snowstorm, with one bright point of light in the center, as if the final form is growing inside and will take over the whole Pokémon once the globe bursts. If it fits, the tiny house from attachment 1 is just barely visible in the storm.
- The body: no snail foot, no head, no eye stalks. A smooth, frozen, streamlined body that flows out of the globe towards the back and ends in a longer frozen tail, the start of a comet tail.
- Eyes: two eyes at the front of the body, below the globe, with the same eye shape as in attachment 1.

KEEP IT READABLE AS A SPRITE
- One clear silhouette that reads as one creature: round globe in front, body and tail streaming back. Max 3 or 4 cracks. The storm is white swirls and pixels around one bright point, not noise.
- The glass reads by one clear highlight in the top left.

POSE
- Three-quarter view facing left.

STYLE AND FORMAT
- 64x64 pixel sprite, the creature about 56 pixels wide (larger than the first stage, not filling the whole canvas), max 16 colors, pale icy blue-white like attachment 1 (no grey), 1 px dark outline, light from top left, flat Gen 3 shading with 3 to 4 tones per color, no dithering.
- Plain white background. NO floor, snow on the ground, shadow, glow, sparkles or effects outside the creature. No loose or floating pieces or shards. One single creature, no extra views.

AVOID
- No snail body, foot, head, eye stalks or tentacles. No spiral shell or cone.
- No ice blocks or brick pattern, no ice spikes or crystal clusters.
- No galaxy, stars or planets.
- Not a plush toy, chibi or Neopets mascot. No glossy 3D render.
```

## Ronde 5 (15 nov)
- `r5_gemini.png` (prompt v4). Jordi: "dit is het ook niet, laat me even een beschrijving bedenken". Volgende prompt komt uit Jordi's eigen beschrijving.

## Beschrijving Jordi (15 nov), bij r1
- "Wat dit goed deed is de bol zelf, deze begint te barsten, plus in de bol begint een chaotische sneeuwstorm te ontstaan, in de derde fase barst deze bol compleet en ontstaat er zo de kern van de laatste vorm. De positie van de bol is goed, ik ben niet zo overtuigd van dat hele puntige schild erbovenop, maar ik ben er ook niet op tegen. Dat het lichaam langer wordt en steeds ijziger met kristallen zie ik ook zitten. Sowieso kan het hele lichaam van ijs worden ook, wat ik in deze vorm nog niet goed vind is dat het nog steeds dezelfde vorm slak is, daar moeten we dus iets anders van maken, vooral de ogen, misschien een ander soort dier met dezelfde vorm, die al meer een ijs vorm heeft, kan je iets met deze beschijving, prompt nog niet, maar spar even mee"
- Voorstellen Claude: Andes-gordeldier, zee-engel (Clione), Liolaemus-hagedis, heremietkreeft. Jordi: "de clione zie ik zitten, maar we behouden dus nog wel de bol op de rug"
- Claude vroeg naar houding, vleugels, rood hart, ogen, hoorntjes, schild. Jordi: "we gebruiken de clione echt alleen voor de vorm, dus dit zijn vragen die niet belangrijk zijn, ik heb mijn voorkeur al aangegeven."

# Prompt v5 (15 nov): Clione-vorm, bol van r1, nieuw gesprek

Bijlagen: 1. `r1_gemini.png`, alleen voor de bol (barsten, storm, positie op de rug). 2. Zelf toevoegen (Jordi): een foto van een zee-engel (*Clione limacina*), voor de vorm.
Uit Jordi's beschrijving: bol als in r1 (positie, barsten, chaotische storm); lijf langer en ijziger met kristallen, mag helemaal ijs; niet meer de slakkenvorm, vooral andere ogen; Clione alleen voor de vorm; bol op de rug.
Keuzes Claude (schrappen mag): puntig schild weggelaten (Jordi: niet overtuigd, niet tegen); geen lichtpunt in de bol (Jordi: de kern ontstaat in fase 3); voetstuk als ring (stond in r1, eerder c1); ogen: twee simpele ogen in de kop, niet nader ingevuld; ± 56 px.

```
Attachment 1 shows an earlier draft of an original Pokémon: use it ONLY for the snow globe on its back (its position, the cracks, the chaotic snowstorm inside, the reddish-brown base ring). Do NOT copy the snail body, eye stalks, face or the pointed shell on top. Attachment 2 is a sea angel (Clione limacina): use it ONLY for the body shape.

Design this Pokémon (pure Ice type, the second of three stages; the final stage is an icy comet) and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- Body: the shape of a sea angel (attachment 2), made of ice. Longer than a snail, becoming icier, with a few ice crystals on the body. The whole body is ice.
- Eyes: two simple eyes in the head. No eye stalks.
- On its back: a snow globe, in the same position as in attachment 1. The glass is starting to crack, and inside a chaotic snowstorm is forming.

KEEP IT READABLE AS A SPRITE
- One clear silhouette. Max 3 or 4 cracks, big and simple. The storm is white swirls and pixels, not noise. The glass reads by one clear highlight in the top left.

POSE
- Three-quarter view facing left.

STYLE AND FORMAT
- 64x64 pixel sprite, the creature about 56 pixels wide, max 16 colors, pale icy blue-white, 1 px dark outline, light from top left, flat Gen 3 shading with 3 to 4 tones per color, no dithering.
- Plain white background. NO floor, water, bubbles, shadow, glow, sparkles or effects outside the creature. No loose or floating pieces. One single creature, no extra views.

AVOID
- No snail shape, no snail foot, no eye stalks, no pointed shell or cone.
- No galaxy, stars or planets.
- Not a plush toy, chibi or Neopets mascot. No glossy 3D render.
```
