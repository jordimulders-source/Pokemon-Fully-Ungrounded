# Poedelmot: kleur r11 (nieuwe maker)

Start: `kleur_r10/raster.txt` + `normal.pal` (palet ongewijzigd). Silhouet bevroren: alpha-diff 0. Ogen, kop, kinboog, sprietnerf (C) en linkerspriet niet aangeraakt (diff in de oog/kop-zone alleen de vacht links van het linkeroog: (16–18,31), (16,32–33)).
Handgetekende rijen per onderdeel in `stappen/*_rows.py` (segmenten per rij), toegepast op r10 met `stappen/apply.py` (meldt elke silhouetfout). `stappen/tl.py` = vergelijkingsraster (model en sprite met coördinaten).

## Gedaan
1. **Rechtervleugels**: het bakstenen raster is weg. Voorvleugel: crème vlak (7), een brede witte geschulpte buitenrand met één golvende tan lijn (1 px), een grote C-krul (46–49, 27–31) met een staart naar rechts, een kleine boogkrul (51–54, 26–28) en één tan vlek (51–53, 23–24). Een witte voorrandlijn loopt langs de onderkant van de spriet van (48,26) naar (38,33), met een donkere lijn eronder (de plek waar de vleugel achter kop en kraag vandaan komt). De tan vleugelvoet ligt bij 40–46, 30–34. De naad tussen voor- en achtervleugel is 1 px en loopt van y35 tot y37 naar de inkeping. Achtervleugel: witte bovenrand onder de naad, tan voet, een C-krul (45–47, 38–40), een golflijn onderaan (y42–43) en een witte rand rechts. De donkere grenslijn met de kraag loopt van (40,36) naar (45,45). Onderrand: een lijn met twee inkepingen op de pluim erachter.
2. **Linkervleugel**: wit met een crème waas en twee tan streken (10–14, 30–31) en (16–18, 30–31), een tan vlek (13–15, 33–34), een crème onderband (y35) en een donkere onderlijn (y36).
3. **Pootjes en aansluiting**: een kraagplukje (wit, V-vormig) hangt tussen A en B tot y52. De bovenlijn van A loopt schuin af (16,48) → (20,50). B heeft een ronde bovenlijn op y48. C is groter: de bovenboog ligt nu op y53 en C is helder wit. D en E (de verre pluimen) zijn wit met een crème schaduwsikkel en minder wit dan de nabije pluimen. B2 is crème (schaduw onder B). De klauwtjes zijn die van r10.
4. **Kraag**: de witte vacht valt over het middenstuk tot y47, met een plukkerige onderrand op y48 (een witte punt bij x33). De rechterkraag naast de vleugellijn is wit met een crème schaduwband. De dubbele parallelle lijn van r10 is weg.
5. **Rechterspriet**: onder de nerf staan nu steile, evenwijdige ribben (1 px breed, 2 px hoog, stap van 1 per 2 rijen, periode 3), loodrecht op de nerf zoals in het model. Boven de nerf staan korte tikjes. Het schaakbord is weg.

## Controle (`controle_uitvoer.txt`)
- Alpha-diff 0 (1782 px), open randen 0, selout-reeksen < 3: 0.
- Losse pixels 0, tintclusters < 3 px 0.
- Bewust lijnwerk van 1 px (krullen, schulplijn, witte voorrandlijn) staat in `krul_lijnen.txt`.
- Indexen: 1234567ABC (8 en 9 niet meer gebruikt).

## Eerlijke zwakke punten
- **Pootjes**: op 1×/8× lezen ze nog als een rij ronde pluimen. De buitenomtrek (het bevroren silhouet) bepaalt dat voor een groot deel. Het verschil in maat en hoogte is nu vooral te zien aan C (laag en groot) en E (hoog en groot), en minder goed aan A tegenover B. De klauwtjes zijn niet herzien en blijven 2–3 px stipjes.
- **Middenstuk**: de platen en naden zijn die van r10. In het model zijn ze grijzer met zwarte lijnen. Hier is het nog een vrij groot tan vlak.
- **Vleugelkrullen**: in tan 6 op crème 7 zijn ze subtiel (contrast ±40). Ze kunnen op 1× wegvallen. De voorvleugel is iets warmer/tanner dan het model.
- **Kraag**: de plukjes in de vacht zelf zijn nauwelijks te zien. Het silhouet ligt vast, dus de pluizigheid van het model zit alleen in de onderrand.
- **Rechterspriet**: met periode 3 zijn de ribben grover dan in het model. De nerf is een stappenlijn.
- Niet onafhankelijk gekeurd.
