# Uku Pacha r2: notitie van de maker

**Bestand:** `uku_pacha_r2.png` (64×64, geïndexeerd, index 0 = transparant, **16 kleuren incl. transparant**). Vel: `vel.png` (r2 | r1 | model op 8×, koppen en kronkels op 12× naast het model, r2 op 1× en 2× op licht en donker).

**Bijsturing Jordi (via coördinator), letterlijk:** "ik wil eerst een eindproduct zien", "misschien werken de lijnen gewoon". Daarom zijn in deze ronde **geen lijnen weggehaald**: alle blokjeslijnen van het model staan erin. De Arbok-afstand is gemeten maar niet toegepast.

## Werkwijze (scripts, in volgorde; `python3` vanuit deze map, uitkomst reproduceerbaar, diff 0)
1. `kwant.py`: natief raster (100×100) → 16 modelklassen (`kwant_8x.png`).
2. `stap1_lijnen.py`: zelfde transformatie als r1 (`geom.py`, factor 0,6957). Elke lijncel van het model (klassen 0–4) wordt naar spriteruimte geprojecteerd en met zijn 8-buren verbonden, zodat lijnen **doorlopen** in plaats van in streepjes te breken. Vlakken = oppervlak-gewogen meerderheid van de modeltinten.
3. `stap2_schoon.py`: lijnen 1 px dun (Zhang-Suen), buitenrand dicht, losse vlakpixels weg. `stap2b_vlak.py` levert alleen het geestmasker.
4. `stap3_raster.py`: tekstraster; de geest krijgt zijn lichte eigen omlijning (modeltoon) en geen zwarte lijnen (het model heeft daar geen lijnen).
5. `koppen.py`: **beide koppen en beide vleugels per pixel naar het model** (puntmonster `punt.py` en `zoom.py` naast het model; die vervangen px.py/box1x.py van de poedelmot met dezelfde functie voor dit model).
6. `blokken.py 10`: blokjes tussen de lijnen (≤ 10 px) krijgen één toon: de meerderheidstoon van het model over dat hele blok (zelfde plek, geen nieuwe vorm).
7. `afwerk.py`: buitenlijn volgens Dragonfly Cave (zwart alleen aan de schaduwkant onder/rechts; lichtkant = outline base in de donkerste eigen tint: lijf navy `n`, koppen/vleugels donkerblauw `D`, geest lichtblauwgroen `l`), 1-px tintvlekjes en losse lijnpunten weg → `uku_pacha_r2.png`.
8. Controle: `check.py` (alpha, kleuren, vlekjes, klonten), `lijnfreq.py` (Arbok-meting), `vel.py`.

**Silhouet:** alpha-diff met r1 = **0** (bevroren, geen enkele omlijningspixel heeft een alphawijziging nodig gehad).

## Palet (16)
transparant · zwart K (16,20,28) · navy n (36,50,76) binnenlijn + lichtkant-omlijning lijf · donker d (66,78,102) · leisteen s (82,102,132) · midden m (108,130,158) · basis b (112,150,172) · lichtblauw h (130,164,200) koppen · geest/licht l (119,175,186) · bleek p (156,212,212) · lichtst w (194,235,230) · blauw B (75,108,148) · donkerblauw D (44,73,111) · geel oog Y · tong P · tand W.
Kleur wijkt bewust af van het model waar het contrast te klein was ("geen grijze brei"): helderheidsstappen d→s→m→b ±25 per stap, lijn n ±27 onder d; de grijze modeltoon (77,87,98) is opgegaan in s (was een grijze tussentint zonder eigen contrast); de koppen kregen een lichtblauw h in plaats van het teal van de buik (model: (118,152,182)).

## Lijnfrequentie (gemeten, niet toegepast)
- **Arbok** (Gen 3 `anim_front_gba.png`, bovenste 64×64; lijnen = zwart + donkerpaars): schubbanden langs de staart op rij 15 → 21 → 28 = **6–7 px**; over de buik (rij 49) x 25 → 30 → 38 = **5–8 px**. Automatisch (`lijnfreq.py`, vlakstuk tussen twee binnenlijnen langs rijen en kolommen): mediaan 3,0, gemiddeld 4,0 px; binnenlijnen 23 % van de pixels (incl. kapmotief en ogen).
- **Uku Pacha r2:** buikbanden langs de dalende nek kolom 24: 42 → 47 → 52 → 58 = **5–6 px**, kolom 19: 44 → 48 → 54 = 4–6 px; automatisch mediaan 3,0, gemiddeld 3,8 px; binnenlijnen 19 %.
- Op de buik zit r2 dus al dicht bij Arbok; het verschil zit in de **kronkels** (vooral de rechter), waar de schubblokken van het model 2–3 spritepixels groot worden. Als Jordi lijnen weg wil: daar eerst (navy segmentlijnen `n` in de kronkels, de zwarte spiraallijnen `K` laten staan).
- **Weggehaalde lijnen: geen** (op Jordi's bijsturing). Alleen technisch: lijnen van 2 px dik naar 1 px gedund en 1 losse lijnpunt in een vlak weggehaald (ruis van de verkleining, geen modellijn).

## Pixels die niet 1-op-1 uit het model komen (en waarom)
- **Buitenlijn: 76 px** omgekleurd (DC-regel: K aan de schaduwkant, eigen donkere tint aan de lichtkant, geest in eigen lichte tint). Vorm ongewijzigd.
- **Koppen (handwerk naar puntmonster): links 127, rechts 89 px t.o.v. de automatische projectie.** Afwijkingen van het puntmonster zelf: linkeroog als 2×2 (wit + bleek) met zwarte rand en wenkbrauw (model: lichte spleet in zwart, valt bij 0,70 uiteen); tongvork op 1 px (twee punten (3,26) en (5,26–27), model ±1 px lager); bovenrand van de kop D i.p.v. zwart (DC). Rechteroog: geel 3 px breed met zwarte pupilpunt onderaan (model: 2×2 geel met donkere hoek); bekslijn als doorlopende trap (model: ±0,5 px hoger, valt op de rijgrens).
- **Vleugels: 64 px** handwerk naar het puntmonster (arm licht boven, vlies D, vingers n); lichtblauw h op de armrand (model (91,127,170)).
- **Blokken egaal: 26 px** (blokje = meerderheid van het model over het blok).
- **Ruis: ±25 px** 1-px tintvlekjes en losse lijnpunten naar de omringende vlaktoon (excl. oog, tanden, neusgat).
- **Grijs → leisteen:** alle (77,87,98)-pixels van het model (vooral rug linkernek) staan als s.

## Zelfgenoemde zwakke punten
1. **Rechterkronkel leest minder als spiraal dan in het model**: de modellijnen zijn daar dun en dicht; op 64 px worden het veel korte navy segmenten tussen de zwarte spiraallijnen. Niet opgelost door lijnen weg te halen (verboden in deze ronde); het contrast zwart (spiraal) vs navy (segment) is wel vergroot zodat de spiraal ervoor ligt. Dit is het punt waar Jordi's lijnvraag beslist.
2. **Zes 1-px blokjes ingesloten door lijnen** in de kronkels ((9,45), (7,47), (12,50), (43,51), (15,53), (18,59)): in het model is dat een klein schubblok; laten staan omdat weghalen een lijn zou samenvoegen.
3. **Kleine 2×2 lijnklonten** waar modellijnen samenkomen: (25,19) nekknik, (26,42), (12,48), vleugelklauw (41,39–40), onderrand (26–27,62).
4. **Op donkere achtergrond** valt de gekleurde lichtkant-omlijning (n/D) linksboven weg; dat is de DC-keuze en zo doen onze goedgekeurde sprites het ook.
5. Linkeroog is nu een klein licht oog met zwarte wenkbrauw; leesbaar op 1×, maar het boze spleetoog van het model komt minder over. Als Jordi dat wil: oog 1-op-1 van een Gen 3-slang (Seviper/Arbok) overnemen.
