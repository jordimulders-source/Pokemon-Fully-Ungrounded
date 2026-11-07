# Picapau-evolutie: sprite r3 (van model r5)

## Jordi letterlijk
- Over sprite r2: **"het ding is, het is nog niet echt een vogel he. De staart mag wat dunner en wat meer vogelachtig, desnoods zwart. De oren mogen ook naar achter bewegen, zwart en meer op de raichu lijken, verder mag die wat graden naar links draaien, want nu zien we een flink stuk hoofd met het oog helemaal aan de zijkant. De vleugel mag iets vogel achtiger"**
- **"ja het lijkt nu iets meer een alien dan een vogel, en ik heb liever eigenlijk een grote vogel met raichu motief"** (→ model r4)
- **"ja nu komen we ergens! de snavel mag open, dat geeft wat karakter. Vergeet mijn eerdere instructies over de oren, die mogen dunner en wat verder doorkrullen, iets meer zoals de onderkant van de oren van raichu"** (→ model r5)
- **"ja en in de pose mag de buik echt naar voren, die laten we een beetje op die gen 1 raichu pose lijken"**
- Over r5: **"de buik is teveel een bulge"**
- **"maar laten we een sprite gaan maken"** · **"dat is makkelijker te editen"** → deze sprite, met de r5-render als bron. De buik en de bliksem zijn in de sprite opgelost.

## Bestanden en werkwijze
- `bron/renders.py` rendert uit het r5-model, in dezelfde stand en hetzelfde kader als `R5_8x.png` (schaal 0,796):
  - `labels.png`: elk onderdeel een vlakke kleur;
  - `wit.png`: het witte model.
- `bron/bron.py` maakt per spritepixel `bron_labels.txt` (onderdeel), `bron_toon.txt` (toon 0–3) en `overtrekvel.png` (render met 4 px-raster).
- **`tekening.txt` is de sprite, met de hand getypt.** Per regel staan rij, kolom en de pixels als tekens, regio voor regio: verre vleugel, handpennen, dekveren met stippen, oren, kop, buik/flank, poten, steunstaart en schacht, bliksem.
  - De omtrek is cel voor cel overgetrokken van het overtrekvel en de labelkaart. De kleur en schaduw zijn met de toonkaart als gids pixel voor pixel ingetypt.
  - Er zitten geen kleurregels of formules in de code. `zet.py` zet de segmenten alleen op hun plek in `raster.txt` en meldt tikfouten (overlappende segmenten).
  - Reparaties gaan in `tekening.txt`, of direct in `raster.txt`.
- `palet.py`: het palet van r2, met 3/v/4 verder uit elkaar gezet voor de vleugel (zie onder).
- `bouw.py` maakt `picapau_evo.png` (geïndexeerd, 16 kleuren, index 0 transparant) en `normal.pal`.
- `controle.py` → `controle_uitvoer.txt`.
- `vel.py` → `vel.png`: 1× en 8× naast r2, Picapau, Taillow, Staraptor, Raichu Gen 1 en de r5-render.
- Draaien: `python3.11 zet.py && python3.11 bouw.py && python3.11 controle.py && python3.11 vel.py`

## Hoofdvraag: leest hij op 1× als een vogel (specht) met Raichu-motief?
- **Vogel: ja**, duidelijk meer dan r2 (dat las als vos).
  - Een ronde kop op een nek met een open beitelsnavel, en het oog vooraan bij de snavel zoals Picapau en Taillow.
  - Een grote opgezette vleugel met handpennen in een waaier en de ronde stippen.
  - Een spechtenstaart, en poten onder het lijf.
- **Raichu-motief: ja**: de zwarte oren met spiraal en haak, de dunne zwarte staartlus met de grote bliksem linksonder, de grote crème buik en de rode wang.

## Per punt
1. **"de buik is teveel een bulge"** (in de sprite opgelost, zoals gevraagd).
   - De voorrand is één doorlopende ronde curve van keel tot dijen: x 13 (keel, rij 25) → 12 → 11 → 10 → 9 (rij 34–39) → 10 → 11 → 12 → 13 → 15 (rij 48).
   - Er is geen knik bij de keel en geen insnoering naar de dijen, en de rand heeft nergens een recht stuk van meer dan 6 rijen.
   - De crème begint smal onder de snavel en wordt geleidelijk breder: hij hoort bij de hals en de borst, zoals bij Staraptor en Raichu Gen 1, en is geen losse bol.
   - De buik is het grootste lichte vlak.
   - Licht linksboven (a) raakt de belichte rand. De grens a/b loopt als boog. De schaduw (e) ligt als sikkel rechts en onder. Zo is er geen kussenschaduw.
2. **Bliksem groter (±1,13×) en vrijer onder het lijf uit.**
   - Hij is 23 rijen hoog (rij 36–58), met een duidelijke knik (de "plank" op rij 46–47).
   - Het bovenste blad staat helemaal links van de buik. Het onderste blad komt onder de buik en de voet uit en sluit aan op de staartschacht.
   - Kleuren: y licht, 1 schaduw rechts en onder, 2 als selout aan de lichtkant, zwart aan de schaduwkant.
3. **Snavel open.**
   - Grijs zoals Picapau. De bovensnavel is 3 rijen (G-rand, licht a/g, donkere onderkant G), de ondersnavel 2 rijen plus de zwarte onderrand.
   - Daartussen zit een donkere mond (C) van 2 rijen. Beide delen zijn op 1× ≥ 2 px.
4. **Oren** (zwart, achter op de schedel).
   - Nabij oor: een korte zwarte voet met G-glans die overgaat in een **spiraal van 1 px zoals Raichu Gen 1** (8 × 8 px), ±1¼ slag naar binnen. Het gat en de spleet zijn op 1× zichtbaar.
   - Verre oor: een dun blad met een **haakje aan de punt zoals Gen 3**.
   - Beide staan tegen de lucht. Daarvoor heb ik de punten van de verre vleugel 2 kolommen naar rechts gezet ten opzichte van de render (bewuste afwijking).
5. **Vleugel.**
   - Voorrand met selout. Daarachter een band kleine dekveren (3, licht), dan grote dekveren (v) met ronde lichte stippen (a, 2×2), en dan zeven handpennen en armpennen in een waaier, gescheiden door donkere lijnen (4) die vanuit de hand uitwaaieren, met ronde uiteinden.
   - Bovenop de punten van de verre vleugel (alleen v/4, schaduwtint).
   - Palet: 3/v/4 = (168,78,36) / (120,48,22) / (70,28,14). De helderheidsstappen zijn daarmee ±30 (r2 ±20), zodat de lagen en veerlijnen lezen. 3 is ook de schaduwtint van het lijf.
6. **Kop, oog en wang.**
   - Het oog is pixel voor pixel dat van Picapau (via r2).
   - De wang heeft twee tinten (c/C), met de schaduw rechtsonder.
   - Licht 1 linksboven en een sikkel 3 rechts en onder.
7. **Staart.**
   - Drie spitse spechtenveren (v/4, zwart aan de onderkant).
   - Daarna een dunne zwarte schacht van 2 px met G-glans, die rechts omlaag loopt en onderlangs naar de bliksem.
8. **Poten.**
   - Nabije poot: loopbeen g/G, een grote voet met 2 tenen voor en 2 achter, en zwarte klauwen.
   - Verre poot: hoger en verder naar achteren, alleen schaduwtint G.

## Controle (`controle_uitvoer.txt`)
- Geen lichte kleur op de buitenrand.
- Geen losse pixels.
- Geen tintclusters kleiner dan 3 px (omlijning en oog uitgezonderd).
- 15 kleuren + transparant, 1948 px.
- Alleen-diagonaal verbonden zijn 6 px: de 1px-lijnen van de oorspiraal en het haakje (bewust, zoals Gen 1) en de achterste klauw.
- Afwijking van de r5-massa: +274 / −132 px. Dat is bewust: de buikrand, de grotere bliksem, de oren en de verschoven punten van de verre vleugel.

## Eerlijke zwakke punten
1. **Poten.**
   - De voeten zijn groter dan in r2, maar naast Staraptor en Taillow blijven ze klein en grijs: de nabije voet is een balkje van 2 rijen en de verre voet 1 rij.
   - "Grote voeten met klauwen" komt op 1× nog maar half over.
   - Grijs is de kleur van Picapau. Eventueel 1 rij hoger en de tenen apart tekenen.
2. **Vleugel donker en vol.**
   - De waaier is een groot donker vlak. De lagen lezen op 8×; op 1× vooral de stippen en de lichte voorrand.
   - De punten van de verre vleugel bovenop zijn smal en spits en kunnen als "vingers" lezen.
   - Mogelijke reparatie: ronde, bredere toppen, en per handpen een 3-streep aan de bovenkant.
3. **Flank.**
   - Rechtsonder (rij 39–46, x 30–42) ligt een groot vlak 3 zonder vorm: dij en onderbuik hebben geen eigen binnenvorm.
   - Een kleine boog 2 boven de dij zou het lijf boller maken.
4. **Kop.** Het vlak 1 linksboven is vrij groot en vlak. De overgang kop–hals heeft geen binnenlijn; dat is wel zoals Picapau.
5. **Verre vleugel.** Tussen kop en nabije vleugel staat een strook dicht donker (v/4) zonder veren, met één lichte stip (b).

Er is niets gecommit.
