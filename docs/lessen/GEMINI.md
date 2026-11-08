# Sprites vanaf een Gemini-ontwerp (Jordi, 7 nov: "pas de regels maar aan voor gemini modellen die sprites gemaakt worden")

**Eerst:** `SPRITE_WERKWIJZE.md` → "Gemini-model namaken" (poedelmot/poedellarve: meetgereedschap px.py/box1x/lijnkaart vanaf ronde 1, één keurder met alleen de twee eisen, 8× naar Jordi, verse maker > ±400k tokens). Dit bestand vult aan.

Wanneer Jordi een ontwerp in Gemini laat maken en kiest, gelden deze regels **in plaats van** stap 1–3 van `SPRITE_KERN.md` (ontwerp, bron, silhouet). De rest van SPRITE_KERN (netheid, belijning, ogen, keurslot) blijft gelden.

## Ontwerp in Gemini
- Claude schrijft de prompt (Engels); Jordi plakt hem in Gemini en stuurt het resultaat. Voorbeeld en rondes: `docs/concept/sprites/viscacha/gemini/README.md`.
- Vast in elke prompt: echte diersoort als anatomie (foto meesturen), "official Gen 3 front sprite (Ruby/Sapphire/Emerald style)" (Jordi, 7 nov: Gen 3, niet Gen 5; Gen 5 is 96×96 en botst met 64×64/≤16 kleuren), 3/4 naar links, geen elektriciteit/gloed/effecten, **geen rots/ondergrond/schaduw**, witte achtergrond, ≤16 kleuren, 64×64, een AVOID-regel (Neopets/knuffel, konijn, enz.).
- **Gemini is slecht in verbeteren:** korte bijstuurfeedback werkt hooguit 1–2 keer; daarna drijft hij af (viscacha werd Raichu). Beter: de beste versie als bijlage in een **nieuw gesprek** met een nieuwe startprompt.
- "Meer Pokémon"/"cuter" laat Gemini naar bekende soorten glijden (Pikachu/Raichu); noem expliciet wat níet mag lijken.
- Jordi's keuze = **bevroren ontwerp**: pose, verhoudingen (kopgrootte, oren), kenmerken en kleuren. Opslaan als `referenties/gemini_gekozen_*.png`, feedback per ronde in `gemini/README.md`, Jordi letterlijk in SPEC.

## Van Gemini-plaatje naar sprite
- De sprite is een **vertaling** van het Gemini-plaatje naar 64×64, geen nieuw ontwerp. Silhouet = masker van het plaatje verkleind (massa heilig), kleuren = de Gemini-kleuren.
- Kwantiseren naar het palet mag als **onderlaag** (Gemini-plaatjes zijn al pixelachtig); daarna met de hand opschonen volgens SPRITE_KERN (tinten, sikkelschaduw, selout, ogen van een echte sprite). Geen kale scriptuitvoer opleveren.
- **Niet afwijken van Gemini** behalve wat Jordi expliciet toestaat (viscacha: alleen het oog). Ook niet uit eigen zorg ("leest als kraag"): Jordi 7 nov "je mag alleen met ogen afwijken". Twijfel = Jordi vragen, niet zelf of via de keurder besluiten.

## Keuren
- De keurder toetst **trouw aan het Gemini-plaatje + spritetechniek**, niet het ontwerp. Ontwerppunten (kop klein, minder cute) zijn géén FAIL; **elke afwijking van Gemini wel** (vorm, maat of plek van een onderdeel, iets weggelaten).
- Vergelijk op 8× naast het Gemini-plaatje (verkleind) én 2–3 echte sprites.
- De regel "na 2 mislukte rondes stoppen" telt hier alleen bij ontwerp- of vertaalproblemen; rondes met alleen benoemde pixelreparaties (contour, toonvlakken) gaan door, doel ≤ 5.

## Lessen
- **Elk onderdeel afvinken tegen Gemini op dezelfde schaal** (kop, oren, oog, neus, mond, snorharen, aanhangsels, poten, lijf, staart): de viscacha-wangpluk werd stilletjes verkleind en het gezicht vereenvoudigd; Jordi: "je hebt het niet goed gecontroleerd".
- **Gezicht apart vergelijken** (viscacha r4, 7 nov: Jordi "kijk eens goed naar het gezicht ... neus, whiskers, mond"; twee keurders en Claude misten het): maak altijd een close-up van de kop van sprite en Gemini op dezelfde schaal naast elkaar en vink per onderdeel af: neus, mond, snuitvorm, kin, snorharen, oog, oren. Snorharen uit Gemini niet weglaten: 1 px lijntjes zoals Raticate/Sandshrew.
- **Onderlaag eerst, niet hertekenen** (viscacha r1–r6): elke handmatige hertekening verschuift onderdelen een paar pixels van Gemini (oorvorm, neus-Y, snorhaarpad, teenlijntjes) en levert FAIL op FAIL. Begin met het gekwantiseerde Gemini-plaatje op de juiste schaal (alles incl. snorharen in 64×64), houd elke featurepixel op zijn plek, schoon alleen technisch op (buitenlijn, ruis, ≤3 tinten), vervang alleen wat Jordi toestaat. Meld de afwijking van de onderlaag per zone.
- **Viscacha af in 8 rondes** (7 nov): r1–r6 tekenden op het oog en hielden vast; r7–r8 met de poedelmot-methode (verse maker, meetgereedschap, Claude stuurt benoemde reparaties na het vel, één keurder met de twee eisen, daarna DFC-eindkeuring) gaven in 2 rondes PASS en "erg goed". Begin dus meteen zo.
- **Gen 3 boven het model voor licht en contrast** (viscacha r9, Jordi "perfect, doe maar"): een Gemini-model is vaak vlak (weinig contrast, geen hooglicht, lichtrichting wisselend). Na de vormkeuring mag een kleurronde naar Gen 3 (stappen ±30–40, hooglicht linksboven, verre ledematen donkerder) zonder het ontwerp te veranderen; vraag het Jordi.
- **Een rug/romp die in het model vlak is mag bol** als Jordi het vraagt; trapjes in een regelmatig curvepatroon (2‑3‑5 / 5‑3‑2‑1‑1), geen herhaalde gelijke trappen. Jordi's krabbel (rode lijn/stip) schalen en op het raster leggen om pixels te vinden.

- **Consistent ontwerp = goede prompt** (Jordi, 7 nov, hatun runa): echte soort + kenmerken + gedrag (de kiskadie die "bem-te-vi" roept en afzet naar een insect) gaf over gesprekken heen steeds hetzelfde dier. Gedrag als pose-bron werkt beter dan "dynamic pose".
- **Geen details onder sprite-schaal vragen:** een rij symbolen/tocapu in een streep van 3 px werd losse icoontjes en is niet naar 64×64 te vertalen (Jordi). Patronen pas als groot vlak, of zelf in de pixels.
- Woorden als "headband/braided" + wit/rood geven een Japanse hachimaki; beschrijf een cultuurverwijzing als verenvlak, niet als voorwerp.
- **Basisontwerp als bijlage in een nieuw gesprek wordt gekopieerd** (Hitmontop-evolutie, 7 nov, Jordi: "hij past het basisontwerp niet aan"): voor een andere pose geen eerder Gemini-plaatje meesturen, maar het ontwerp in woorden + een posebron die de pose echt toont (3D-model); een stickman leest Gemini niet als pose.
- **Hitmongroove (8 nov), 5 sprite-rondes:** eerst de kop pixel voor pixel naar Gemini volgen gaf een onherkenbare kop (±20 px); de ogen 1-op-1 uit de echte stamsprite (Hitmontop) halen maakte hem meteen familie. Strenge eindkeuring met 3 vragen (familie/evolutie, past in Gen 3, DFC) en Jordi's eigen vermoeden ("arm te recht") als apart punt werkte; een ronde met alle keurdersreparaties (r4) vond Jordi slechter dan de basis: reparaties per stuk tonen en de basis laten kiezen.
- **Gemini-prompts (Hitmongroove):** pose via een 3D-model als bijlage werkte (Gemini weigerde niet); Hitmon-verhoudingen als eigen blok met maten (kop ≥ torso, hand ½ kop) hield hem niet-menselijk.
