# Nachtaap fase 3, kleur ronde 3: lijf (vacht als één geheel)

Basis: `../ronde1s/nachtaap_fase3.png` + `normal.pal` (ongewijzigd gekopieerd). Ronde 2 niet gebruikt.
Bestanden: `nachtaap_fase3.png` (resultaat), `normal.pal` (= 1s), `lijf.py` (de handmatige toontabel per rij, op 1s), `lijf.txt` (tekstraster van het resultaat), `basis_1s.txt`, `check.py` (diffbewijs), `vel.png`, `studie_rug.png` (+ `studie_rug.py`), `varianten/` + `vel_varianten.png`.

Jordi (letterlijk): "Het lichaam is overigens echt prutswerk. Ronde 2 maakt het slechter en alle onderdelen lijken nu los van elkaar te zitten. Kijk eens naar hoe het bij andere pokemon gaat" · "nu mag je eerst alle shading en kleur op het lichaam gaan fixen en er een geheel van maken" · "en de rug gaat vergeleken worden met allerlei pokemon sprites waar op de rug gekeken wordt en benen/vleugels/armen etc eraan verbonden zijn, gebruik ook back sprites hiervoor" · "ja en als het qua verhoudingen toch niet klopt, dan mogen suggesties uitgewerkt worden hoe dat te fixen, dat werkte met het been ook".

## 1. Studie (8×)
**Front: Vigoroth, Aipom, Primeape, Slaking, Medicham.**
- Ledematen lopen zonder naad over in het lijf. Een binnenlijn staat er alleen waar een ledemaat echt vóór het lijf ligt, en dan kort en vaak in de schaduwtint (Vigoroth: arm over de buik, Aipom: staartwortel).
- Shading in grote vlakken: een brede lichte massa aan de lichtkant (linksboven), één schaduwband langs de schaduwkant en een kernschaduw alleen aan de onderrand. 3 tinten plus omlijning, geen vlekken.
- Omlijning: gekleurd (donkere tint) aan de lichtkant boven/links, zwart onder/rechts. Een cilinder (Aipom-arm, Vigoroth-arm) heeft de lichtband direct tegen de gekleurde bovenrand, niet midden in de cilinder.

**Rug en aanzetpunten (`studie_rug.png`: 12 front- en 12 back-sprites op 3×, Aipom-back/Linoone/Salamence/Machamp-back op 8×).**
- Over de rug en schouders loopt één lichtband. De bovenkant van een aangezet ledemaat (Salamence-poten, Linoone-achterpoot, Aipom-back-staart) loopt in die lichtband door, zonder lijn.
- Onder het aanzetpunt zit altijd een schaduw (oksel, liesplooi, onder de vleugel- en staartwortel). Die schaduw hoort bij de schaduwband van de romp en is geen losse streep.
- Een overlap-lijn alleen waar het ledemaat echt over de romp valt (Machamp-back: armen over de rug; Aipom-back: hand over het lijf). Die lijn is kort en loopt uit in de schaduw eronder.
- Delen onder het lijf (Salamence-dijen, Linoone-buik) liggen in één schaduwvlak met de buik. De poot wordt licht waar hij onder het lijf vandaan komt.

**1s ernaast, per plek (wat het los maakte):**
- **Arm–schouder (healerarm):** een verticale lichtstreep (x22–23) en een dubbele schaduwstreep (x27–28) liepen over de hele lengte (rij 33–45). Het las als een buis die op de borst geplakt was.
- **Borst:** losse lichte vlekken (x28–31 r35–37, x32–34 r32–33, x23–28 r30–32) zonder logica.
- **Vuistarm:** de omlijning stond omgekeerd: zwart boven naast de lichtband, gekleurd (2) onder naast de schaduw. Verder stopte de lichtband bij rij 25, zodat de arm los van de schouder stond.
- **Dij–heup (opgeheven been):** de lichtband van 2 px stopte bij de dij. Daarna begon een tweede lichtvlek in het lijf.
- **Onderbeen–buik:** een schaduwband (r43–45) liep dwars over de wortel van het onderbeen, met daaronder weer een licht dij-vlak (r46–50 x33–40). Dat gaf een naad, en de dij leek een los stuk.
- **Onderbeen:** de lichtband lag 2 px onder de bovenrand (basis–licht–basis), zodat er een ribbel ontstond in plaats van een cilinder. De onderrand had een dubbele donkere rand (r51–52) met een binnenlijn `222` bij de knie.
- **Staartwortel:** al grotendeels één geheel met de bil (r36–38). Alleen het hoekje `22` (r35) blijft; dat ligt tegen een transparante inham, dus het is een echte rand.

## 2. Wat ik deed (220 px, alleen indexen 1–5)
- **Eén lichte massa (5)** linksboven: van de dij van het opgeheven been (die uitwaaiert: 2→4→6→7 px) via rug en schouder (r31 x23–36) over de borst. Hij loopt als een gebogen evenaar naar linksonder en wordt smaller tot de lichte kant van de healer-bovenarm (x22–23, rij 40–45 en verder in de onderarm). De losse vlekken zijn weg.
- **Eén schaduwband (3)** langs de schaduwkant: van de schaduwkant van het opgeheven been (x37–39) door de bil rechts (x40–43, de staartwortel ligt erin) en daarna langs de onderkant van de buik. Daar wordt hij breder naar rechtsonder.
- **Healerarm:** geen streep over de hele lengte meer. Bovenaan gaat de arm op in de borst (zoals in het model). Een korte binnenlijn in schaduwtint (x27, rij 40–45) staat alleen waar de arm vóór de buik hangt, met de okselschaduw ernaast die in de schaduwband van de buik overgaat. De dubbele `33` is weg. x20 r33–34: 3→4 (geen tweede donkere rand naast de kopomlijning).
- **Vuistarm:** de bovenrand is gekleurd (2) van vuist tot schouder (lichtkant) en de onderrand zwart (1) (schaduwkant). De lichtband ligt tegen de bovenrand en loopt door tot in de lichte massa van de schouder (r26–31). Op r20 is de band 3 px naar de vuist verlengd. De vorm en de vuist zijn ongewijzigd.
- **Opgeheven been:** de lichtband is doorlopend gemaakt (r16–17, r23: de 4 tussen rand en licht werd 5). De dij waaiert uit in de lichte massa.
- **Dij onder het lijf:** één schaduwvlak (3) met de buik, zoals Salamence en het model. Kernschaduw (2) alleen tegen de onderrand. De binnenlijn `222` bij de knie is weg.
- **Onderbeen:** de lichtband ligt nu direct tegen de gekleurde bovenrand (2 px), met basis eronder, schaduw en een zwarte onderrand. Hij begint licht bij de heup, waar het been onder de bil vandaan komt. De dubbele bovenrand-trapjes zijn tot één pixel teruggebracht (de binnenste pixel van elk trapje is licht geworden).
- Niet aangeraakt: enkel/voet onder (r53+ x52+), voet boven (r4–11), staart, kop, maan, hand en gloed.

## 3. Bewijs (`python3 check.py`)
- alpha-diff **0**; palet gelijk aan 1s; niet-vacht-indexen (6–F) gewijzigd: **0**.
- Healerhand + gloed (x4–23, r44–62): **0 px**. Staart (x44–63, r22–40, met spleten): **0 px**. Beide voeten: **0 px**.
- Kopvak x0–19 r27–45: 5 px gewijzigd (plus 2 px op x20, net buiten het vak). Alle 7 zijn vuistarm/healerarm, geen kop: (16,27) (17,28) (18,29) (19,30) (19,31) is de onderrand van de vuistarm 2→1 (de kop-run eindigt op x15–17 in die rijen), en (20,33) (20,34) is de healerarm 3→4 (de kopomlijning staat op x19). Kop-binnenkant, ogen, snuit en maan: 0.
- Open randen (3/4/5 naast transparant): geen.

## 4. Verhoudingsvarianten (`vel_varianten.png`, 3× en 1× licht/donker; kies ik niet)
Bij het vergelijken met Salamence, Linoone en de Aipom-back hangt de dij onder het lijf als een zak omlaag (onderrand r54, het onderbeen r52). Dat is de "rare kont" van eerder. Varianten tillen de onderrand van de dij geleidelijk op (de omtrek verandert alleen daar, x36–46):
- `varianten/dij_min1.png`: −1 px (x37–45). Kniekuil blijft.
- `varianten/dij_min2.png`: −2 px (x36–46). De dij loopt vloeiend over in het onderbeen, met een kleine kuil.
- `varianten/dij_min3.png`: −3 px. De onderkant is bijna recht, zonder kniekuil.
- `varianten/dij_min4.png`: −4 px. Dunste dij. Er ontstaat een trapje van 2 px bij x45→46 dat bij een keuze nog met de hand glad moet.
Andere verhoudingen (de dikte van de armen, de lengte van de romp) lijken me naast de referenties in orde. Daar heb ik geen varianten van gemaakt.

## 5. Eigen check (1× en 3× naast 1s, Vigoroth, Aipom, Primeape)
- Op 3× en 1× is het nu één lijf. Been, schouder en borst delen één lichtvlak, en buik, dij en bil één schaduwvlak. De healerarm leest pas onder de borst als losse arm. Er staan geen strepen of vlekken meer.
- **Niet goed / open (eerlijk):**
  1. De lichte massa op schouder en borst is groot en vlak (±60 px één tint). Op 3× oogt hij iets plat naast Aipom, die tussen licht en basis nog een zachte overgang heeft. Er is geen extra tint in het palet; dit kan een kwestie van smaak zijn, maar het is een open punt.
  2. Boven rij 40 is de healer-bovenarm opgegaan in de borst (zoals het model). Jordi kan de arm daar als "weg" lezen.
  3. Het schaduwvlak onder het lijf (buik + dij) is groot en donker. Dat volgt het model en Salamence, maar zonder variant `dij_min` oogt de onderkant zwaar.
  4. De vuistarm heeft nu een gekleurde bovenrand. Op een lichte achtergrond is hij daar zachter begrensd dan in 1s (Gen 3-regel, maar het is een wijziging aan een arm waar Jordi lang over deed).
  → Omdat ik zelf deze punten noem, is dit **geen PASS**. Het is een basis voor de keuze van Claude en Jordi en voor een keurder.

## Lessen
- Een lijf wordt één geheel door eerst per rij de grens van de lichte massa en het begin van de schaduwband vast te leggen (twee doorlopende curven over romp en ledematen), en pas daarna per onderdeel te kijken. Shading per onderdeel geeft per onderdeel een eigen streep.
- Controleer bij elke cilinder of de lichtband tegen de gekleurde rand ligt. Basis–licht–basis is een ribbel, geen ronding.
- Diagonale omlijningen van 3 px breed (trapjes met overlap) maken een dubbele rand. Maak de binnenste pixel van elk trapje vulling.
- Een verplicht "bevroren vak" als rechthoek (kopvak) raakt soms pixels van een ander onderdeel. Meld per pixel wat het is in plaats van alleen het getal.
