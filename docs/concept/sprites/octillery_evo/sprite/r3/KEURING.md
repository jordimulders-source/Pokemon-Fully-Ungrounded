# Keuring r3 – Octillery-evolutie frontsprite (`octi.png`)

Onafhankelijke keurder, 11 nov. Blind geoordeeld (eigen 1×/2×/8×/14×-vergrotingen, model `referenties/ontwerp_gekozen.png` geschaald naar de sprite-bbox (1,24)–(62,63) op hetzelfde raster, naast Gen 3 Octillery, Gyarados, Seviper en Scizor). Er waren geen makerrapporten bij r3. Getoetst zijn alleen de twee eisen: (1) trouw aan het model, (2) een goede Gen 3-sprite. Coördinaten zijn spritepixels (x,y).

## Eindoordeel: NIET klaar voor Jordi

Alle onderdelen zijn er en staan grotendeels op hun plek. Plaatsing en massa zijn een goede basis. Als sprite is hij nog niet goed genoeg. De lijnen zijn te zwaar en te recht, waardoor hij als een blokkerige machine leest en niet als een inktvis. **36% van de opake pixels is bijna-zwart** (index 1 en F, L < 45). Bij Gen 3 ligt dat op 12–19%, zelfs Seviper (een zwarte Pokémon) zit op 17%. De gemiddelde helderheid is 76, tegen 115–129 bij Octillery, Scizor en Gyarados. Op 1× is het een donker blok met buizen, het gezicht valt weg en de tentakels rechts lezen als ringen.

## Per onderdeel

| Onderdeel | Oordeel |
|---|---|
| Mantel + segmenten | REPAREREN (zie 2, 6) |
| Vinnen (rugvin, staartvin) | REPAREREN, klein (zie 6) |
| Kop | REPAREREN (zie 2, 5) |
| 2 ogen | REPAREREN (zie 4) |
| Geribbeld mondkanon met opening | GOED, klein punt bij 8 |
| Bovenste kanon met monding | GOED, klein punt bij 9 |
| Onderste kanon met monding | GOED, klein punt bij 9 |
| Krul achter de kop + wratten | REPAREREN (zie 7) |
| 2 rupsband-tentakels | REPAREREN (zie 3) |
| 3 tentakels rechts (incl. donkere boog met zuignappen) | REPAREREN (zie 1); donkere boog met 3 zuignappen = GOED |
| Zuignappen buitenkant / omcirkelde wratten weg | GOED (de wratten onder de kin zijn weg, zoals toegestaan) |
| Toegevoegd, niet in model | REPAREREN (zie 3: roze schijven rechtsonder) |

## Reparaties, op belang

1. **Tentakels rechts zijn geometrische ringen en geen tentakels (eis 1 + 2).**
   - De bovenste tentakel (x=51–62, y=40–50) is een gesloten rechthoekige lus. Bij x=58–61, y=42–49 loopt een kaarsrechte verticale buis van 8 rijen met het identieke patroon `1431` (banding).
   - In het model stijgt die tentakel schuin op van (47,48) naar (54,41), boogt over de top naar (58,41) en krult omlaag naar een **spitse vrije punt rond (59,47)**. Hij sluit niet aan op de middelste tentakel en komt niet verder dan x≈59.
   - De middelste tentakel (x=41–62, y=50–52) is een rechte balk van 3 px dik met rechte lijnen boven (y=49/50) en onder (y=53, 19 px lang). In het model loopt hij licht stijgend van (46,51) naar (61,49) en **loopt hij taps toe tot een 1 px punt die omhoog krult**.
   - Wat moet gebeuren: beide tentakels als gebogen, taps toelopende armen met spitse punten tekenen, het gat tussen boven- en middententakel open laten (wit bij x=52–58, y=45–48) en de wratten aan de onderkant houden.
2. **Te veel en te zware zwarte binnenlijnen; te weinig selout (eis 2).** De binnenlijnen zijn nu bijna-zwart (F = 68,12,20). Teken ze in de donkerste roodtint (2) of donkerder rood, taps en alleen waar vorm over vorm valt. Zet aan de lichtkant (bovenranden mantel y=24–33, bovenrand bovenste arm x=6–14, y=39–44) een gekleurde selout in donkerrood in plaats van F. Concreet gaat het om:
   - de mantelsegmentlijnen (x≈40, 45–49, 53–56, y=27–37);
   - de rechte horizontale lijn onder de rugvin (y=27, x=42–57);
   - de lijnen in de rupsband (y=55, x=33–40; y=57, x=38–46; y=53, x=41–59);
   - de verticale lijnen bij x=30, 33 en 36 (y=57–62).

   Doel: het aandeel bijna-zwart terug naar ±20%. Op de linkerrand van de krul (x=19–20, y=37–43) wisselen 1 en F elkaar af (1-1-F-F-1-1). Kies daar één lijnkleur.
3. **Rupsband leest niet als opgerold (eis 1 + 2).**
   - Het gebied x=30–55, y=53–62 bestaat uit horizontale strepen (banding) met lange rechte lijnen. In het model is de verre rupsband een **langgerekte gesloten lus**: een ovaal van (30,57) tot (55,55) met één gebogen binnenlijn die de lus volgt. De onderrand loopt schuin van (55,55) naar (30,63).
   - Teken het als een ovale lus met een gebogen binnencontour en schaduw die de bocht volgt.
   - **Weghalen:** de roze zuignapschijven bij (40–42, y=58–61) en (45–47, y=58–59). Die staan niet in het model. Het model heeft alleen roze schijven op de nabije rupsband linksonder, bij x=22–32, y=58–63, en die zijn in de sprite goed.
4. **Ogen te klein; het gezicht valt op 1× weg (eis 1).**
   - Het verre oog is nu 1×2 geel op (26,40–41). In het model is het ±3×2 geel met een donker lid erboven (x=26–28, y=39–41). Maak het 2–3 px breed met een pupilpixel.
   - Het nabije oog is nu 5×4 (x=35–39, y=40–43). In het model is het ±7 breed (x=33–40), amandelvormig, met een **zwaar schuin boos lid** van (32,42) oplopend naar (40,39). Het lid is nu alleen 3 px op y=39, x=38–40. Verleng het lid over de hele bovenkant en maak het oog 1–2 px breder naar links.
   - Neem de vorm over van een echt Gen 3-oog met spleetpupil (bijv. Gyarados of Seviper), niet zelf verzinnen.
5. **Rechte lijnen waar de kop rond is (eis 2).**
   - De rechterwangrand is één verticale F-lijn van ±19 px (x=41, y=38–49, dan x=40, y=50–56). In het model is het een bolle curve van (42,40) naar (40,53).
   - De kin is een rechthoekig kader: x=32 en x=40 verticaal, y=55 horizontaal (x=33–40). In het model is het een ronde, lichtere bult bij (33–39, 50–57).
   - Bij het verre oog vormen de verticale lijn x=24 (y=36–42) en de horizontale lijn y=42 (x=24–31) een doos. In het model is dat de gebogen overgang van de krul naar de kop en de bovenrand van het mondkanon.
   - Wat moet gebeuren: alles als curven.
6. **Mantel en vinnen (eis 1 + 2).**
   - De mantelsegmentlijnen zijn rechte diagonalen. In het model zijn het bollen bogen die naar rechtsonder buigen. Laat ze buigen en maak ze lichter (zie 2).
   - De onderrand van de mantel is 13 px recht op y=37 (x=48–60). In het model daalt die licht van (58,37) naar (42,40), met de punt van de staartvin bij (57–58,37).
   - De rugvin (x=42–57, y=24–26) mag recht (in het model is hij ook hoekig), maar de lijn eronder moet donkerrood zijn in plaats van F.
7. **Krul achter de kop leest als een rechte kolom (eis 1 + 2).** Nu x=19–23, y=36–43, met een kaarsrechte linkerrand. In het model is het een ronde haak: de buitenboog loopt van (20,44) omhoog naar (21,36) en buigt naar rechts de kop in bij (25,35), met 3 gele wratten op de buitenboog. Rond de linkerrand en de top af en voeg eventueel een derde wrat toe bij (20,40).
8. **Opening van het mondkanon is een rechthoek.** Het donkere vlak (x=19–23, y=44–50) heeft vierkante hoeken. In het model is de opening een ronde mond met een roze rand eromheen (x=17–24, y=43–51). Rond de hoeken af en laat de roze rand links als boog doorlopen. De ribbels (x=24–31) zijn GOED.
9. **Kanonmondingen (klein).**
   - Bovenste kanon: de opening is 2×2 plus 1 grijs (x=3–4, y=40–41). In het model is ze ±2×3 (x=2–3, y=40–42). Maak haar 1 px hoger.
   - Onderste kanon: de opening (x=8–13, y=54–60) begint ±2 px te laag. In het model loopt de ellips van y≈52 tot 60. Maak haar 1–2 px hoger.
   - De losse lichtgrijze pixel D op (11,58) in de zwarte opening is ruis. Weghalen of vervangen door E.
10. **Losse tintpixels (eis 2, klein).** Het clusterscript vindt ±30 rode eilandjes van 1–2 px buiten de wratten, bijvoorbeeld 3 op (5,44), 5 op (12,43), 6 op (9,41), 4 op (52,46), 7 op (29,49) en 8 op (25,43), (26,44) en (29,44) in de ribbels. Voeg ze samen met de tint ernaast, behalve bewuste glans. De diagonale reeks losse 9-pixels in de staartvin (57–58, 29–31) mag als kraslijn uit het model, mits doorlopend.

## Wat goed is (niet aanraken)
- Compositie en bbox volgen het model (verhouding 62×40 ≈ 1,54, zoals het model).
- De plaatsing van mondkanon, bovenste kanon (arm en monding naar links), onderste kanon (loop, roze rand, gele wratten van de rupsband links ervan), donkere boog met 3 zuignappen en het gat erin.
- De omcirkelde wratten onder de kin zijn weg en er is geen zichtbare plaknaad boven de loop van het onderste kanon.
- Palet: 15 kleuren. De roodstappen 2→6 liggen tussen ±25 en 40 L. Licht valt linksboven.

## Advies
Punt 1 t/m 5 samen in één makerronde: die bepalen of hij als Gen 3-sprite leest. De vorm en plaatsing van de kanonnen en het mondkanon (punt 8 en 9 alleen klein) bevriezen met een alpha-diff. Daarna opnieuw keuren.
