# Pitahaya-draak fase 2 (teju), sprite r1 (maker)

Methode: model overnemen, niets tekenen (fase 1-recept: natief raster → exacte 3×3-reductie met regels → alleen technisch opschonen, elke wijziging met modelmeting).

## Stappen
1. `natief.py` (kopie fase 1, pitch 5,0–5,25): raster **5,076 px**, natief **201×201**, figuur **175×101**. Gecontroleerd op een uitvergrote uitsnede van de bek: pitjes zijn 1 natieve cel, tanden 3–5 cellen; geen veelvoud.
2. `groepen.py`: bg (bijna-wit verbonden met de rand + het witte gat in de staartkrul), zwart (lum < 42), roze, groen (G ≥ R), wit/lichtgrijs (vruchtvlees, tanden, oogwit), **pit** (grijs/zwart in de bek met ≥ 4 witte buren; componenten ≥ 8 px = tandomlijning → lijn). Lichtgrijze anti-aliasrand buiten de bek = achtergrond. Model: 30 pitcomponenten. Controle: `groepen.png`.
3. `half3.py`: 3×3-reductie (achtergrond ≥ 5/9; lijn bij ≥ 2 zwarte px; pit bij ≥ 2 pitpx; vlees bij ≥ 4 wit; anders gemiddelde → dichtstbijzijnde modeltoon van de meerderheidsgroep). 9 fases in `fases/`; gekozen **oy 0, ox 2** (oog: zwart ooglid + wit, tand 2 wit). Aanroep `python3 half3.py kaal.png 0 2 2 2`.
4. `maak_r1.py`: opschoning → `pitahaya2_r1.png`. Aanroep `python3 maak_r1.py 1 pitahaya2_r1.png --T groen --tand 42,5 --lz 2`. Elke wijziging in `pitahaya2_r1_afwijkingen.txt`. **Silhouet-diff met de kale reductie: 0.**

## Maat en palet
- **58×33 px, 1222 px**, x 3–60, onderste rij y 62 (1 px marge). Exacte 3× geeft 58 i.p.v. ±62 breed; 2,8× kan alleen met middeling (Hauntflare-les: dan worden lijnen en pitjes vlekken). Bewust 3× gehouden.
- **12 kleuren + transparant**, allemaal modelkleuren: zwart (19,19,15) · roze (113,43,55) (177,40,84) (231,78,123) (244,148,167) · groen (56,93,51) (83,125,66) (112,158,81) (155,181,96) · vruchtvlees (191,189,192) (237,234,237) · pit (44,42,46).
- Zwart binnen de figuur **8,6 %** (kaal 13,7 %); buitenrand 60 % zwart (Gen 3 45–68 %).

## Afwijkingen van de kale reductie (196 stappen; per zone)
| Stap | Reden | kop | oog | bek | rug/lijf roze | poten/groen | staart |
|---|---|---|---|---|---|---|---|
| A | dubbele binnenlijn: zwart naast een sterkere zwarte buur, breekt geen verbinding → vlaktint van het eigen blok | 1 | 0 | 0 | 2 | 5 | 3 |
| A2 | zwakke binnenlijn (≤ 2 van 9 modelpx zwart) → donkerste tint van het vlak (Gen 3: binnenlijn in vlaktint) | 2 | 0 | 0 | 6 | 11 | 6 |
| T | groene binnenvulling uit de gladde modelluminantie (σ 1,5) → dichtstbijzijnde groene modeltoon (fase 1 r6); roze niet (vlakte de lichtstrepen op de snuit weg) | 1 | 0 | 0 | 0 | 29 | 14 |
| M | bek: vruchtvlees per blok (≥ 3 wit/pit en niet minder dan roze) → grijs/licht naar het blokgemiddelde; pitjes opnieuw gekozen (zie onder) | 0 | 0 | 21 | 0 | 0 | 0 |
| D | tand voorin (zie onder) | 0 | 0 | 1 | 0 | 0 | 0 |
| B | buitenlijn 1 px: zwart aan de schaduwkant, selout aan de lichtkant (roze → (113,43,55), groen → (56,93,51)); randpixels die al zwart of een van de twee donkerste tinten zijn blijven | 16 | 0 | 10 | 7 | 12 | 10 |
| C | losse vulpixel (cluster van 1) → meest voorkomende buurtint uit dezelfde groep | 5 | 0 | 7 | 6 | 12 | 2 |
| E | 2×2-dambord van twee vultinten uit één groep → 1 px naar de andere tint (die met de modelhelderheid het dichtst bij) | 2 | 1 (roze naast het oog, oog zelf ongewijzigd) | 2 | 0 | 2 | 0 |

**Pixels die niet uit de kale reductie komen, apart benoemd:**
- **(5,42) zwart → wit (tand voorin).** Het model heeft daar een witte hoektand (natief x 16–18, y 89–92) die de lijnregel zwart maakte. Gekozen blok (42,5): 2 witte modelpx, rondom zwart (geen lichte kleur op de buitenrand). Alternatief (43,4) heeft 3 witte px maar ligt op de buitenrand. De tweede tand (8,43) staat al in de kale reductie (8 witte px van 9). Beide tanden 1 px (les fase 1).
- **Pitjes (7).** Kaal had 14 pitpixels, vaak tegen elkaar (raster). Regel: per vleespixel het aantal pitpx van het model; sterkste eerst, geen twee pitjes 8-naast elkaar, niet op de vleesrand. Resultaat 7: boven (palatum, grijs) (11,44) (13,46) (15,47); onder (licht vlees) (11,48) (14,49) (9,51) (11,51). Elk staat op een blok waar het model een pit heeft. Model heeft ±28 pitjes; op 64 px leest 1 pit per ±2 px vlees als vrucht, meer gaf dambord.
- Verder geen pixel met de hand: oog, nabije/verre poten, tenen, schubpunten, staartgat en snuitgat komen ongewijzigd uit de reductie (alleen B/C/E-tintwissels).

## Zelf vergeleken (vel.png: 8× naast het model op dezelfde maat, kop 12×, 1× licht/donker)
- Leest als laag vierpotig reptiel met wijd open bek, roze schubbenrug met groene punten, groene poten, staartkrul met gat; oog gemeen (zwart schuin ooglid + wit).
- Bek: grijs palatum boven, licht vlees onder, roze diagonale wang ertussen, zwarte pitjes; leest als doorgesneden pitahaya op 2×; op 1× als witte bek met stipjes.

## Zwakke punten (eerlijk)
- **Onderste vleesvlak kleiner dan in het model** (±5×6 px): het roze wangband en de lip nemen op 3× relatief meer ruimte; het model heeft een grote witte ovaal. Niet vergroot (zou hertekenen zijn).
- **Lip links** is selout (113,43,55) waar het model zwart lijntje + roze lip + lichtroze binnenrand heeft; lichtroze binnenrand valt onder ½ spritepx weg.
- **Pitjes 7 vs ±28 in het model**: bewuste keuze tegen dambord; de keurder moet beoordelen of het genoeg "dragonfruit" leest.
- **Breedte 58** i.p.v. ±62 (exacte 3×).
- Zwart binnen 8,6 %, net boven de Gen 3-band 1–8 %; de resterende binnenlijnen zijn sterke modellijnen (≥ 3/9 zwart: schubnaden en poot-over-lijf).
- 13 dambordjes resteren, allemaal tussen een lijn (zwart/selout) en een vultint (diagonale lijnen), niet tussen vultinten.
- Kop-roze is iets vlakker dan het model (lichtstreep op de snuit is 1 rij).
