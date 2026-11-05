# Kolibrie pre-evo – silhouet ronde 1 (maker, 2 nov)

Opdracht (Jordi, letterlijk): "ik wil deze eigenlijk zittend met de vleugels ingeklapt, misschien snavel open omdat die gevoed wil worden. Moet echt cute zijn". Puur Flying, dus geen Ghost-kenmerken. Alleen stap 2: silhouet, één kleur.

## Bestanden
- `silhouet.txt`: 64×64, `#` = vol. Met de hand rij voor rij overgetrokken op het overtrekvel (geen ellipsen, geen geknipte sprites, geen automatisch verkleinde foto).
- `silhouet_1x.png` (render van de txt: `python3 render.py`).
- `overtrekvel.png` (`overtrekvel.py`, zones in `zones.txt`): foto 1 als onderlaag (10 foto-px = 1 spritepixel, kop van de foto = kop van het silhouet) met het 64-raster, het silhouet erover (rode omtrek), de afwijkzones A–G in oranje, en ernaast foto 5 en foto 3 (gespiegeld, kop naar links).
- `vel.png` (`vel.py`): silhouet 4× en 1× naast Natu, Togepi, Pichu, Fletchling, Taillow en de eindvorm.

## Game Freak-studie (kleine vogels, zittend/staand, silhouet)
| sprite | px | wat het silhouet laat lezen |
|---|---|---|
| Natu | 431 | Kop en lijf één bol; bek als korte wig in de as van de kop; voetjes als twee platte balkjes van 2 rijen onder de buik. |
| Taillow | 838 | Ronde kop ±50% van de hoogte, nekknik waar de kop overgaat in de rug; staart en vleugel steken diagonaal naar rechtsachter en breken de bolvorm. |
| Fletchling | 606 | Kop als eigen bol, borst bolt naar voren onder de kin; vleugel omhoog; dunne pootjes. |
| Pichu / Togepi | 565 / 489 | Baby-maat: grote kop, kort lijf, kleine stompjes onderaan; geen lange ledematen. |
Les: een zittend vogeltje leest niet als ei als (1) de kop een eigen onderdeel is (nekknik of kin-inham), (2) de bek een wig in de kijkrichting is, (3) iets diagonaal naar rechtsachter steekt (staart/vleugelpunten) en (4) er onder de buik alleen korte voetjes staan, geen slierten.

## Wat ik per zone deed (zie overtrekvel)
- **Kop (y9–26):** omtrek van foto 1 overgetrokken (voorhoofd x14, wang x15, kin y25–26), kruin 3 px hoger en ronder (B) en achterhoofd ±2 px voller (C) om de kop groter en ronder te maken. Nekknik op y20–21 (achterhoofd x33 → x32 → rug vanaf x34) zodat de kop los van het lijf leest.
- **Bek (A, x8–14, y10–21):** open bedelbek van foto 3: bovensnavel schuin omhoog (±45°), ondersnavel bijna horizontaal; brede basis die vloeiend in voorhoofd en kin overgaat (geen los stokje). Bovensnavel 2–3 px dik, punt 2 px; ondersnavel 2 px dik; gaap 1 px bij de mondhoek (x13, y17) tot 4–6 px bij de punten. Lengte ±6 px: kort, zoals bij jonge kolibries.
- **Borst (G):** onder de kin een inham (x19 op y26–27), dan bolt de borst naar voren tot x16 (y31–33): donsbolletje, en de kop blijft een eigen vorm.
- **Rug:** bolle lijn vanaf de nek naar rechtsonder, segmentlengtes geleidelijk oplopend (1-1-1-2-2-3-3-4), geen rechte diagonaal; loopt niet boven de kop uit.
- **Buik (D):** 8 px hoger afgerond dan in foto 1 (lijf korter, foto 5).
- **Staart (E):** kort stompje naar rechtsonder (x38–45, y41–46), met een inham (x35–37, y41) tussen buik en staart.
- **Pootjes (F):** nabije poot links (x24–28, tenen naar links), verre poot rechts kleiner (x31–34), 2 kolommen lucht ertussen; direct onder de buik, geen tak.

## Getallen
- **743 px** (doel 550–750; Pichu 565, Fletchling 606, Taillow 838; eindvorm 1000 → pre-evo 0,74×).
- Box x8–45, y9–46: 38 × 38.
- **Kop-hoogte:** kruin y9 tot kin y26 = 18 van 38 rijen = **47%** (zonder staartpunt, tot de voetjes y43: 18/35 = 51%). Doel 45–50%: ok.
- **Kop-oppervlak:** 296 px = 40% (met bek 44%); norm ±41%: ok.
- Eén samenhangend geheel (1 component), geen losse pixels.

## §0-checklist en harde eisen
1. 3/4 links-voor: kop naar links, kop iets omhoog zoals foto 1; het lijf staat diagonaal (kop linksboven, staart rechtsonder). Op silhouetniveau is de 3/4-draai van de borst pas in kleur te zien (witte borst links-voor zoals foto 1). ok voor deze stap.
2. Ledematen geteld: twee pootjes, staartstompje, bek (2 helften); vleugels zijn ingeklapt en liggen binnen de omtrek (zoals foto 1); ze komen in de kleurronde. ok.
3. Geen rechte lijnen ≥ 4 px waar het dier rond is: nagelopen met een script; alleen het achterhoofd (x33, y16–19) en de rug op de breedste plek (x43, y36–39) hebben 4 rijen, beide op het breedste punt van een bolle vorm met oplopende segmenten ervoor en erna. ok.
4. Ogen: n.v.t. (silhouet).
5. Leest op 1× als een jong vogeltje met open snavel (zie `vel.png`, onderste rij). ok.
6. Formaat vergeleken met Natu/Togepi/Pichu/Fletchling/Taillow: ok.
7. Pose niet stijf: diagonale houding, pootjes verschillend van grootte, staart schuin. ok.
- Bekende fouten uit de opdracht: geen ei/pinguïn (nekknik, kin-inham, staartstompje schuin, bek als wig), rug loopt niet boven de kop, bek steekt niet als stokje uit (brede basis), geen kuifveertjes, geen slierten onder het lijf. Geen Ghost-kenmerken.

## Wat nog niet klopt / voor Jordi
- Geen open zwakke punten die ik zelf zie. Smaakkeuze voor Jordi (geen fout): het lijf kan nog 3 rijen korter (getest: 664 px, kop 53% van de hoogte), dan wordt hij bolliger maar komt het kop-oppervlak op 45%, boven de norm van ±41%; daarom niet gekozen.
- Hoe "kolibrie" het jong leest hangt in kleur vooral af van de bek (donker met gele mondhoeken) en het fluweelviolet; het silhouet zelf leest als jong vogeltje, wat bij een jonge kolibrie met korte snavel klopt.

## Lessen
- Overtrekvel met de foto op hetzelfde raster als het silhouet maakt zichtbaar hoeveel je afwijkt; mijn eerste zones waren te optimistisch gelabeld ("1–2 px") terwijl de overlay 3 px liet zien. Zones altijd naast de overlay labelen, niet uit het hoofd.
- Een nekknik van 1 px (achterhoofd even naar binnen vóór de rug uitbolt) is genoeg om kop en lijf op 1× als twee delen te laten lezen.
- Bij een open bek de bovensnavel aan de basis laten overlopen in het voorhoofd: dan leest hij als bek, niet als los stokje of hoorn.
