# Steel/Cosmic-lijn (satelliet) – ontwerp
Citaten en besluiten (Jordi, 23 nov); het overzicht staat ook in `docs/concept/IDEEEN.md`.
- 17 nov: "een Steel/Cosmic lijn met o.a. een satelliet erin" · 20 nov: "Steel/Cosmic-lijn waarin één Pokémon een satelliet is".
- "satelliet is fase 2 of 3, ruimtestation misschien 3 en dan nog iets ervoor".
- "de zuid amerika link is niet nodig hier".
- "ja eens met groter en complexer maken" (voorstel Claude: Spoetnik-bolletje → satelliet → ruimtestation, zoals Magnemite → Magneton).
- "ik wil er machines van maken ja" → keuze **B: pure machine met eigen persoonlijkheid** (Klink, Magnemite, Porygon), geen machine in dierenvorm.
- Voorstel Claude, Jordi "dat klinkt goed": fase 1 klein Spoetnik-bolletje met antennes en één oog → fase 2 satelliet met zonnepanelen en een telescoopoog → fase 3 ruimtestation uit gekoppelde modules waarin de satellieten herkenbaar blijven (groter en complexer, zoals Magneton).
- **1 oog** (Jordi).
- "we doen nu alleen de designs": evolutiemethode, lore, namen later.
- Open: kleuren (niet besproken; in r1 laat Claude Gemini kiezen).

## Fase 1 rondes
- r1 (`fase1/gemini/r1.png`): "conceptueel prima idee, maar dit is teveel detail". Claude: paneelnaden, koperen vlekken, schoteltjes op de antennepunten, 4e korte antenne, drie ringen rond het oog → r2 nieuwe startprompt zonder die details. Jordi erbij: "en het mag nog net iets meer pokemon qua kleur gebruik" → kleurregel in r2, vaste kleuren (zilvergrijs, geel oog, koper) eruit zodat Gemini Pokémon-kleuren kiest.
- r2 (`fase1/gemini/r2.png`, blauwe bol, rood/geel oog): Jordi: "ik zou graag voor wit paars willen gaan, bijna een beetje de mewtwo kleuren, maar wel wat smoother en meer cyber qua look. Daarnaast vind ik deze pose iets te recht, mag wat meer driekwart, ik vond het ontwerp net wat beter, qua detail mogen we een beetje ertussenin zitten, deze heeft weer net te weinig detail en de inspiratie is niet meer herkenbaar. Belangrijk is ook vooral dat de pootjes iets groter worden zodat het geen 1 pixel lijnen worden". Claude: r2 kijkt naar rechts (oog rechts); "ontwerp net wat beter" gelezen als r1. → r3 nieuwe startprompt: wit/paars à la Mewtwo, smooth/cyber, meer driekwart naar links, detail tussen r1 en r2 met herkenbare Spoetnik-kenmerken (evenaarnaad, antennevoetjes), dikkere antennes (≥2–3 px).
- r3 (`fase1/gemini/r3.png`): wit/paars, driekwart links, Spoetnik herkenbaar, antennes dik genoeg. Claude: antennes ongelijk en alle kanten op, oog zonder blik (ringen), weinig contrast; voorstel A (r3 = model) of B (r4: antennes gelijk naar achteren, oog met pupil). Wacht op Jordi.
- Jordi over r3: "oog oneens, dat hoeft niet per se, mag best robotisch zijn, alleen de glans op het oog vertaalt niet naar een sprite, je mag wel prompten voor de andere 2 punten" → r4 nieuwe startprompt: r3 + antennes gelijk en naar achteren, meer contrast (diepere paarse schaduw), oog robotische lens zoals r3 maar zonder glans.
- r4 (`fase1/gemini/r4.png`): antennes gelijk, paars en naar achteren, oog zonder glans. Claude: bol nog licht en linksboven geen donkere buitenlijn (oplosbaar in de spritefase); voorstel r4 = model. Wacht op Jordi.
- Jordi over r4: "lijkt een beetje op een pokebal bijna haha maar dat vind ik niet erg".
- Jordi over r4: "is deze pose alleen genoeg driekwart? met de rechte lijn ook?" → Claude: nee, rechte naad + oog op de rand = bijna profiel → r5 (prompt in chat, alleen kijkhoek).
- r5 (`fase1/gemini/r5.png`): Jordi "ik weet niet of ik deze sterker vind, wat vind jij?". Claude: kijkhoek beter (gebogen naad, volume, verkorte antennes), maar antennes dunner (op 64 px ±1–2 px), voetjes wit, naad op 64 px bijna weg. Wacht op Jordi.
- r6 (`fase1/gemini/r6.png`, r6-prompt = r5-kijkhoek + r4-antennes/voetjes/naad): Jordi "de mooiste tot nu denk ik, maar de poten zijn wat kort" · "en het is niet echt een oog meer". Claude: ook 5 antennes i.p.v. 4; oog klein naast de grote bol. → r7 = r6 + antennes lang (± bol-diameter), precies 4, oog groter (±1/3 van de bol) zodat het als oog leest, nog steeds robotisch zonder glans.
- r7 (`fase1/gemini/r7.png`): Claude: oog leest weer als oog (pupil + iris), antennes lang, naad gebogen; weer 5 antennes (korte 4e tussen middelste en onderste), antennes op 64 px ±2 px. Voorstel: r7 = model, korte 5e antenne weg in het model (afwijking, Jordi beslist). Wacht op Jordi.
- Jordi: "dan haal je die kleine 5e weg, zitten de andere wel op een logische plek? Ik heb het gevoel dat de lengte van de onderste te kort is, maar ik weet niet of jij dat logisch kan verlengen" → `fase1/model/model_r7b.png` (natief raster r7 via `model/natief.py`, pitch 10,24; `bewerk_r7.py`: 5e antenne weg, onderste +15 px verlengd door het eigen pixelpatroon (stap 3,1) te herhalen, punt verplaatst). Wacht op Jordi.
- Jordi (met foto van de echte Spoetnik): "op zich klopt het wel zo te zien he". Claude: ja, ook bij Spoetnik lopen twee antennes ongeveer parallel en waaieren de andere uit.
- **Model bevroren (Jordi, 23 nov: "begin maar met bouwen om 19:01")**: `fase1/model/model_gekozen.png` (= r7b; natief 99 px: `model_gekozen_natief.png`). Spritefase start 19:01.
- Jordi (spritefase, 23 nov): "let erop dat de bol mooi rond blijft".
