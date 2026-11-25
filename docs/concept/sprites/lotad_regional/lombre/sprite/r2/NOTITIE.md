# Gaucho-Lombre r2: hoofd (maker, 25 nov)

Basis: `../r1/lombre_gaucho_A5.png` (Jordi: "A5 akkkord maar zorg dat het hoofd verder consistent is, daarnaast valt het linkeroog nu teveel weg en is het rechteroog nog net niet genoeg lombre maar dan bozer"). De mondvorm A5 is niet aangeraakt.

## Bestanden
- `lombre_gaucho_r2_A.png`, `_B.png`, `_C.png`: 64×64, P, index 0 transparant, 14 kleuren incl. transparant, figuur 42×57 zoals A5.
- `vel.png`: kop 12× (A5 | A | B | C | model | Gen 3-Lombre gespiegeld, op lichtgrijs zodat wit leest); A/B/C geheel 8×; 1× (en 2×) op wit en donker naast A5 en Lombre.
- `bouw.py` (alle wijzigingen als lijst pixels met reden), `pixels.txt` (uitvoer: elke pixel oud → nieuw), `vel.py`.
- Verschil met A5: A en B 30 px, C 35 px, **allemaal binnen het hoofdvak x18–36, y22–35; daarbuiten 0** (gecontroleerd). A↔B verschillen alleen op (30,26) en (31,26); A↔C op die twee plus de wenkbrauw (29–32,24).

## 1. Hoofd consistent (gelijk in A/B/C)
- (20,28) rood lijn → zwart: de voorkant van de lip loopt nu in één zwarte lijn door naar de kaak (dit was een rest van de oude kopcontour).
- (21,27) gezicht → zwart: de bovenlijn van de lip (Lombre-stempel, x22–24) sluit nu aan op de kopomtrek in plaats van los in het gezicht te staan.
- (21,26) rood lijn → gezicht: een dubbele rode lijn naast de omtrek (x20) weg.
- Rij 33 x23–30 gezicht midden → rood donker: een schaduwsikkel onder de kaak, zoals de rest van de kop (de Lombre-kaak was één vlak).
- Rij 34 x27–29 rood lijn → zwart: de kinlijn is nu één doorlopende zwarte lijn (zwart en rood lijn wisselden elkaar af).

## 2. Ver oog (gelijk in A/B/C)
Wit 2 hoog met een zwarte stip rechtsboven (naar de kijker), zoals bij de gaucho-Lotad (wit + stip):
- (21,25) wit en (22,25) zwart: zo stond het al in het model.
- (21,26) rood lijn → wit: **nieuw**, de tweede witte pixel.
- (21,24) zwart → gezicht: het oog zit niet meer vast aan de zwarte omtrek erboven en verdwijnt daardoor niet meer.

## 3. Nabij oog = Gen 3-Lombre-oog, bozer
Eerst is het modeloog (x29–34, y25–28) leeg gemaakt naar gezicht midden. Daarna is het Lombre-oog geplakt: `anim_front_gba.png` frame 1, x28–33, y22–25 (wit + zwarte ooglidlijn), 1-op-1, met verschuiving +1 x en +3 y. Het oog staat **ongespiegeld**. Lombre kijkt naar rechts; gespiegeld zou de lidlijn naar achteren zakken, zoals Lombre's eigen vriendelijke blik. Ongespiegeld zakt hij naar de snuit, en dat is de boze blik. De brauw (rij 24, rood donker) en de zwarte rand achter het oog (x35) zijn nog van het model.
- **A:** het Lombre-oog zonder meer.
- **B:** het wit boven het ooglid vooraan is weg: (30,26) → zwart en (31,26) → gezicht. Het lid is vooraan dicht, wat een bozere frons geeft.
- **C:** als B, maar (30,26) en (31,26) worden gezicht (geen zwart). Daarbij is de modelbrauw (29–32,24) een tint donkerder gemaakt (rood donker → rood lijn).

Pixels die niet uit het model of uit Lombre komen: alles hierboven behalve de 16 Lombre-oogpixels en de 2 modelpixels van het verre oog.

## Zwakke punten (eerlijk)
1. Achter het nabije oog liggen 4 zwarte pixels bij elkaar: het hoekje van het Lombre-lid (34,25) en (34,26) plus de modelrand (35,25) en (35,26). Dat leest als een zware brauw. Ik heb het laten staan, omdat het uit het model en uit Lombre komt.
2. De zwarte puntjes van de lippunt (de mondvorm A5) blijven op 1× wat druk. Die zijn bewust niet aangeraakt.
3. Er is nog geen keurder en geen DC-eindkeuring gedaan.
