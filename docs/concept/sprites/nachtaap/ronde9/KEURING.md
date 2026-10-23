# Keuring nachtaap ronde 9 (laatste check, 23 okt)

Onafhankelijke keuring van `anim_front.png` (2 frames, 64×64), naast de *Spriting Guide* (volledig gelezen: Recolors, Revamps, Splices, Outlining, Shading, Shine, Textures, Outline Shading), de fakemon-gids (Simple / Not hybrids / Not humans), `SPRITING.md`, `FAKEMON_DESIGN.md`, `POKEMON.md` en alle nachtaap-punten in `FEEDBACK.md`.

Vellen (in `keuring/`):
- `vel1_vergelijking.png`: 1× op licht en donker (frame 1 en 2) en 3× naast 13 echte sprites: Jigglypuff, Wigglytuff, Aipom, Abra, Smoochum, Natu, Espeon, Mew, Teddiursa, Spinda, Elekid, Mankey (Gen 3) en Chimchar (Gen 4).
- `vel2_koppen_ogen.png`: koppen en ogen op 8× (nachtaap, Jigglypuff, Wigglytuff, Aipom, Smoochum, Teddiursa, Espeon, Mew, Natu, Chimchar) en frame 1/2 op 1×.

Coördinaten: (x, y) binnen het frame, y = 0 bovenaan het frame.

## Eindoordeel: **bijna af**
Op 1× leest hij als een Gen 3-Pokémon: compact silhouet, 13 kleuren, licht van linksboven, omlijning per kleurgroep (zwart-aandeel van de rand 0,51; Abra 0,49, Mankey 0,50, Elekid 0,53) en geen anti-aliasing aan de buitenkant. Kop, oogmaat (27% van de kopbreedte, Jigglypuff 25%) en oogkleur zijn goed. Wat hem nog verraadt, zit in een paar plekken. Het belangrijkste is de **knoop waar oor en staartkrul samenkomen**, want daar zit het Nazca-kenmerk. Verder **ogen die nog een zwarte stip in een ring zijn**, een **verre arm die even licht is als de nabije** en wat **open randen**. Met punt 1 t/m 5 erbij is hij af. Punt 6 t/m 8 zijn polijstwerk.

## Regel voor regel

| Regel (gids) | Echte sprites | Nachtaap r9 | Oordeel |
|---|---|---|---|
| Palet: 3 tinten per kleur + omlijning, gelijke tint | Aipom 12, Jigglypuff 13 kleuren | Violet 5 tinten (K, D, v, b, L), crème 3 + bruine omlijning, oog 4: 13 in totaal | ✔ |
| Verzadiging | Espeon-basis (180,115,230), Aipom (180,98,230): verzadiging ±0,5–0,57 | Basis (160,128,200): 0,36; op 1× bleek lila naast Aipom en Espeon | ontwerpnotitie (onderaan) |
| Lichtbron linksboven, schaduwgrens op de 'evenaar' | Jigglypuff, Teddiursa: schaduw rechts en onder | Kop en buik goed; **verre arm en rechterflank niet** (zie punt 3) | ✗ deels |
| Slagschaduw altijd in schaduwtint | Teddiursa: kin werpt schaduw op de borst | Frame 1: rij 41 crème-schaduw onder de kin ✔; **frame 2: weg** (punt 5) | ✗ frame 2 |
| Hooglicht klein, precies waar het licht loodrecht valt | Chimchar-arm: hooglicht alleen op de schouder | Nabije arm: L-streep over de hele lengte (y 41–48) | polijsten (punt 6) |
| Omlijning 1 px, geen klonten zwart | alle | **2 px zwart** op (42–43, 27–29) en de oorrand loopt in de staart over (punt 1) | ✗ |
| Omlijning per kant: zwart in de schaduw, basis in het licht, hooglichtrand linksboven | Jigglypuff 18% lichte rand, Aipom 30% | Kopbovenrand in schaduwtint v (11 px) ✔; elders vrijwel geen lichte rand (2%) | ✔ (donker, maar binnen Gen 3) |
| Anti-aliasing alleen binnen | alle | Geen buitenpuntjes; op donker schoon | ✔ |
| Gesloten omtrek | alle | Vulpixels tegen transparant op (44,28), (49,32), (37,48), (20,54), (33,41); frame 2 ook (37,46) | ✗ (punt 4) |
| Curven: geen hoek of punt, geen besluiteloosheid, geen lange rechte stukken | Mew- en Espeon-staart, Aipom-arm | Staart-J (2-2-1-1-1-1-2-2-3) ✔; kopzijkanten 8 px recht (Jordi tevreden); kin 10 px recht (y 40, x 21–30); armen als rechte buizen | ✔ / polijsten |
| Symmetrie, gekopieerde delen | Splices-regel 1; Teddiursa en Smoochum: ongelijke kanten | Ver oog = nabij oog min één kolom; oren gelijk (5×7); armen gelijk getekend; middenstreep exact recht in het midden | ✗ deels (punt 3, 7) |
| Ogen: glans + gekleurde reflectie | Jigglypuff: wit 2×2 linksboven, iris donker boven en licht onder; Espeon: ring donkerrood, geen zwart | Glans WW linksboven ✔, roze reflectie rechtsonder ✔, ring donkermagenta ✔; **pupil bijna-zwart en groot, bovenlid even zwaar als de zijkanten** | ✗ (punt 2) |
| Ogen niet opgeplakt | Jigglypuff: oogrand in de huidtint, bovenlid met een flick naar de buitenhoek | Crèmeschaduw rond de oogkas ✔; vorm 5-7-7-7-7-7-5 = afgeronde vierkant | punt 2 |
| Verre ledematen zichtbaar, kleiner en donkerder | Chimchar, Teddiursa | Aanwezig ✔, maar even breed en even licht als de nabije | ✗ (punt 3) |
| Verbindingen | alle | Verre voet (36–39, 53–55) ✔; nabije voet (10–12, 52–55) losse kiezel op 1× | polijsten (punt 8) |
| Silhouet op 1× | | Leesbaar: zittende aap met grote ogen; de krul leest als '9' of haak, niet als spiraal | punt 1 |
| Psychic | Espeon, Smoochum, Natu | Magenta ogen op violet: ✔ | ✔ |
| Nachtaap-herkenbaarheid | | Grote ogen, lichte vlekken boven de ogen, middenstreep: ✔ | ✔ |
| Simple / not hybrid / not human | | Simpel, één geheel, geen neus ✔ | ✔, zie ontwerpnotitie (Aipom) |
| Frame 2 | Gen 3: zelfde schaduwlogica in beide frames | Kop 1 omlaag, staart 1 omhoog; lijf vast | ✗ (punt 5) |
| Oppervlak | Aipom 856, Mankey 872, Treecko 967 | 1041 | grensgeval, niet blokkerend |

## Puntenlijst (geprioriteerd)

**1. Knoop van oor en staartkrul: NODIG**
- *Wat:* het rechteroor (x 37–41, y 25–31) en het binnenstuk van de spiraal (x 41–50, y 25–34) raken elkaar. Op (42–43, 27–29) ligt 2 px zwart naast elkaar. De onderrand van het oor (y 31, x 38–41) loopt recht over in de staartvulling (x 42–46). Het staartpuntje heeft een gaatje van één transparante pixel op (44,27), en dat leest als een oogje. De krul smelt op (50, 32–34) vast aan de buitenring. Daardoor leest de Nazca-spiraal op 1× als een gesloten lus met een klont erin ('9'), niet als een spiraal.
- *Regel:* omlijning altijd 1 px, klonten zwart weghalen (Revamps, Scyther); delen zorgvuldig plaatsen (Splices); "een ronde punt leest als een oog" (SPRITING §11b).
- *Goed bij:* Mew en Espeon (staartkrul met overal minstens 1–2 px lucht ertussen), Spinda (spiraal als lijn met open tussenruimtes, leesbaar op 1×).
- *Oplossing:* teken de binnenkrul opnieuw met een band van 3 px (D-b-K) in plaats van 4. Laat het puntje vrij eindigen met een rond kopje van 2–3 px rond (46,29), los van de buitenring, met overal ≥ 2 px gat. Zorg voor ≥ 1 px lucht tussen de oorrand (x 41) en de krul: schuif de spiraal 1 px naar rechts of maak het oor 1 px smaller. Liever niet: de oorrand als enige lijn vóór de krul laten lopen. Als het in 14×16 px niet past, is een alternatief een rond staarteind met een Spinda-achtige spiraallijn erop.

**2. Ogen: zwarte stip in een ring → gloeiend oog: NODIG (Jordi's hoofdpunt)**
- *Wat:* de donkerste massa in het oog is de bijna-zwarte pupil (K, 40/24/56; ±11 px op x 17–20, y 30–34). De ring (M) is boven even zwaar als opzij. De vorm (rijen 5-7-7-7-7-7-5) is een afgerond vierkant. Daardoor blijft het een sticker of brillenglas, en eerder schattig dan mysterieus. Het verre oog (x 27–32) is het nabije oog min één kolom.
- *Regel:* Shine (kraalogen: glans + gekleurde reflectie, diepte); SPRITING §12 (niet opgeplakt, typekleur); Splices-regel 1 (geen gekopieerde delen).
- *Goed bij:* **Jigglypuff**. Daar is de pupil donkerblauw (65,49,156), niet zwart, de iris verloopt van donker boven naar licht onder, het bovenlid is de donkerste lijn met een flick naar de buitenhoek, en de onderrand is licht. **Espeon**: ring donkerrood (131,57,65), helemaal geen zwart. **Chimchar**: bovenlid zwaar, onderkant open.
- *Oplossing:* pupilvorm houden (Jordi: "vorm prima"), maar in een diep pruim/magenta op een vrije paletplek (index 14/15, bijv. ±(80,16,72)). Bovenlid y 29: de middelste 3 px in K (nabij x 17–19, ver x 29–30) plus 1 px flick naar de buitenhoek. Hoeken van y 29 en y 35 nog 1 px extra afronden (rijen 3-5-7-7-7-5-3 of 5-7-7-7-7-5-3), zodat het oog rond leest. Het verre oog niet als kopie maken: 1 px lager of 1 px smaller bovenaan, glans 1 px.

**3. Verre arm en rechterflank in het licht: NODIG**
- *Wat:* de rechterarm (x 31–36, y 41–53) heeft dezelfde opbouw als de linker (D-b-v-K, basis tegen het lijf aan). Op de rechterflank staat een kolom basistint (x 31, y 44–48) tussen de buikschaduw (x 29–30) en de arm, als een lichtrand aan de schaduwkant. Op 1× staat de buik tussen twee gelijke paarse pilaren: symmetrisch en vlak.
- *Regel:* schaduwgrens op de evenaar, en de kant van het licht af blijft in de schaduw (Shading; officiële sprites negeren teruggekaatst licht). Verre ledematen kleiner en in de schaduwkleur (SPRITING §12). Geen identieke delen (Splices 1).
- *Goed bij:* Chimchar en Teddiursa: de verre arm is donker, smaller en deels achter het lijf.
- *Oplossing:* x 30–31 (y 42–48) in v. Op x 32 een K-scheiding in plaats van D. De arm 3 px breed (v-v-K, hooguit 1 b bovenaan de schouder). Het verre handje vooral in crème-schaduw (s), met 1–2 px C.

**4. Open randen: NODIG (snel)**
- *Wat:* vulpixels die direct aan transparant grenzen: (44,28) L bij het staartpuntje, (49,32) v onder in het spiraalgat, (37,48) v onder de staartvoet, (20,54) v links onder de knie, (33,41) v boven op de verre schouder. In frame 2 ook (37,46) v, met (36,46) transparant: daar zit een gaatje tussen arm en staartvoet.
- *Regel:* gesloten omtrek, 1 px omlijning; aan de schaduwkant zwart, in het licht de omlijningsbasis (Outline Shading).
- *Goed bij:* alle referenties (geen enkele Gen 3-sprite heeft vulkleur tegen transparant, behalve de omlijnings-hooglichtrand linksboven).
- *Oplossing:* (37,48), (49,32), (20,54) → K. (33,41) → D. (44,28) verdwijnt met punt 1. Frame 2: (36,46) → K.

**5. Frame 2 verliest de slagschaduw onder de kin: NODIG**
- *Wat:* in frame 1 ligt onder de kin een rij crème-schaduw (y 41, x 22–30). In frame 2 zakt de kop 1 px en begint de buik direct met basistint (y 42: CCCCCCC). Zo lijkt de kop op de borst geplakt, en die frame-wissel valt het eerst op.
- *Regel:* slagschaduw van een ander lichaamsdeel altijd volledig in de schaduwtint (Shading).
- *Goed bij:* Teddiursa en Jigglypuff houden in beide frames dezelfde schaduw.
- *Oplossing:* frame 2 y 42, x 22–30 → s. Daarbij (36,46) uit punt 4. Kijk ook of de kin (y 40, x 21–30: 10 px recht K) aan de uiteinden 1 px kan oplopen (2-6-2), dan rondt hij af.

**6. Nabije arm en staart als buizen: polijsten**
- *Wat:* de linkerarm (x 15–21, y 40–48) is 9 rijen lang even breed, met evenwijdige strepen D-L-b-v-K en een L-hooglicht over de hele lengte. De staart (y 37–46) is 4 px breed met overal dezelfde streepvolgorde. Allebei lezen ze als slang of pijp.
- *Regel:* hooglicht klein en precies (Shading). Organische vormen buigen, geen lange rechte stukken (SPRITING §12).
- *Goed bij:* Chimchar (arm dunner bij de pols, lichte knik), Mew (staart 3 px, verjongt naar het eind).
- *Oplossing:* L alleen op de schouder (y 41–43), verder b. Arm naar de pols toe 3 px (y 46–48: D-b-K). Stappen 3-2-2-1 in plaats van 3-3-2, dan zit er een lichte elleboog in. Staartmidden 3 px (D-v-K).

**7. Middenstreep op het gezicht: polijsten**
- *Wat:* de streep op x 24–25, y 23–35 is 13 rijen kaarsrecht, 2 px breed en volledig in de schaduwtint. Hij leest als een naad of groef midden over het gezicht en versterkt de symmetrie.
- *Regel:* markeringen volgen de vorm en krijgen zelf licht en schaduw (Shading, Textures); geen lange rechte stukken.
- *Goed bij:* Teddiursa (halve maan op het voorhoofd, mee gearceerd met de kop), Spinda (vlekken volgen de bolling).
- *Oplossing:* een wig van 3 px op het voorhoofd (y 22–25), 2 px in het midden en 1 px tussen de ogen (y 32–35). Het bovenste deel in b met 1 px L linksboven, onderaan in v.

**8. Nabije voet en knie: polijsten**
- *Wat:* de nabije voet (x 10–12, y 52–55) is een paars kiezeltje van 3×3 links van de hand. Op 1× leest hij los. De knie (x 19–27, y 49–55) is een grote lila bult midden onderaan (Jordi in ronde 1: "knieën wat groot").
- *Regel:* alles verbinden en afmaken (SPRITING §12); simpel en leesbaar op sprite-formaat (fakemon-gids, *Simple*).
- *Goed bij:* Teddiursa (zittend; de voet met zool steekt naar voren, aan het been vast), Aipom.
- *Oplossing:* de voet 5×3 met 2 teenpixels, die zichtbaar aansluit op de knie (scheen 1–2 px zichtbaar onder de hand). Of de voet direct vóór de knie zetten. De knie 1 px smaller en lager.

## Ontwerpnotities (geen pixelpunten, voor Jordi)
- **Aipom-gelijkenis:** violet lijf, crème gezicht, ronde oortjes met crème binnenkant en een bijzondere staart. Naast elkaar op `vel1` lijkt hij familie van Aipom. In concept B stond een **bleke lila gezichtsschijf met indigo rand**. Dat zou hem losmaken van Aipom en meer nachtaap maken (die heeft lichte vlekken boven de ogen en een donkere omlijsting).
- **Kleurdiepte:** het violet is grijziger dan Gen 3-violet (verzadiging 0,36 tegen 0,5–0,57 bij Espeon en Aipom). Concept B zei "dieper violet". Een iets verzadigder basis en schaduw maakt hem op 1× meer Gen 3 en meer Psychic.
- **Toon:** het concept is "ziet er eng uit, maar geneest". Glimlach, grote zwarte pupillen en een frontale zithouding maken hem nu vooral lief. Punt 2 brengt het mysterieuze terug. Een kleiner, neutraal mondje (2–3 px) zou ook helpen.
