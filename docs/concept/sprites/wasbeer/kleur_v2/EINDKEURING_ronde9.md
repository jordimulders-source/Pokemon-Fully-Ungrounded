# Eindkeuring kleur ronde 9 (verse keurder, 3 nov)

Te keuren: `ronde9.png` (zonder pupil) en `ronde9b.png` (met pupil), + `.txt`/`.pal`, `vel_ronde9.png`. Vergeleken op 1x/2x/4x/12x/16x, licht en donker, met 13 echte sprites (frame 1 + normal.pal: Zigzagoon, Linoone, Mightyena, Raticate, Teddiursa, Ursaring, Zangoose, Sneasel, Weavile, Furret, Sentret, Absol, Gumshoos) en met de lijn (`referenties/fase1_olinguito.png`, `fase2_coathief.png`). Eerst zelf geoordeeld, daarna pas `KEURING_ronde8.md` en `NOTITIES_ronde9.md` gelezen.

Coördinaten (x, y), 0-geteld; paletindex als hexteken (1 zwart, 2 masker, 3 lichtgrijs, 4–7 grijsbruin donker→licht, 8 oker, 9/a crème, b/c/d buidel, e/f oog).

**Uitslag: FAIL (3 van 10), maar dicht bij klaar.** Met 5 px (plus 2 optioneel) kan hij naar Jordi. Op 1x leest hij als wasbeer-Pokémon en past hij in de lijn. Wat nog faalt is klein pixelwerk op precies de plekken die Jordi noemde: het oog, de voet van het verre oor en de neusglans.

| # | Punt | Uitslag |
|---|---|---|
| 1 | Alpha-diff, open randen, ruis | **PASS** |
| 2 | Staartpunt (kleur) | **PASS** (de haak op 1x kan alleen met een silhouetwijziging: voor Jordi) |
| 3 | Ogen + omgeving, Pokémon-oog | **FAIL** |
| 4 | Oren | **FAIL** (verre oor) |
| 5 | Lijf links tussen arm en kop | **PASS** (de rechte rand zit in het silhouet: voor Jordi) |
| 6 | Neus | **FAIL** (1 px) |
| 7 | Shading overal | **PASS** |
| 8 | Leesbaarheid 1x | **PASS** |
| 9 | Past in de lijn | **PASS** |
| 10 | Geen afgekeurde dingen terug | **PASS** |

## 1. Alpha-diff, open randen, ruis: PASS
- Alpha-diff met `silhouet_v2/direct_s1a.txt`: **0** voor ronde9 en ronde9b (1682 px).
- Randpixels die geen 1/2/4/b zijn: 15, allemaal `c` (bruine selout aan de lichte kant van de verre klauw x 6–10, y 34–44, en de bovenkant van de buidel (40,19)). Dat is een gekleurde selout aan de lichtkant (SPRITING §8), geen open rand.
- Losse pixels (geen enkele 8-buur in dezelfde kleur, zwart niet meegeteld): **24 = 14 per 1000 px**. Ter vergelijking: Mightyena 19, Zigzagoon 28, Raticate 32, Teddiursa 61, Linoone 63, Sneasel 71. Bijna alle 24 zijn functioneel (glansjes, oogpixels, selout-anti-aliasing). Rustiger dan elke echte sprite.

## 2. Staartpunt: PASS
- Donkere dop (2) met een lichte boog 5/4 aan de linkerkant (licht linksboven). Binnenlijn (53,22)→(51,27) en een crème ring met glans (53,24) in de bocht. Op 2x en groter leest hij als een omkrullende punt, niet meer slordig.
- Op 1x is het een donkere punt met een lichtere linkerrand. De haak zelf vraagt lucht in het silhouet (zie Voor Jordi).

## 3. Ogen: FAIL
- Het nabije oog (20–22, 10–13) is nu: lid 1111 / e-a-e / f-f-f / 2-f-2. **De glans staat precies in het midden en de onderkant loopt uit in één punt (21,13).** Daardoor is het oog symmetrisch: op 12x/16x een schildje of kruisje, op 1x een rood plusje met een witte stip.
- Echte sprites met dit oogtype (Zigzagoon, Linoone, Mightyena) hebben de glans **linksboven**, een lichtere iris of reflectie **rechtsonder** en een ronde onderkant. Geen enkele heeft een gecentreerde glans boven een gecentreerde punt.
- **9b (pupil):** f-1-f in een oog van 3 px breed. SPRITING §11b zegt dat een pupil in het midden met iris aan beide kanten een oog van ≥ 4 px vraagt. Op 3 px leest het als sleutelgat. Sneasel, Weavile en Mightyena (Dark, rood oog) hebben geen zwarte pupil, en de lijn (olinguito, Coathief) ook niet. **Advies: 9 (zonder pupil), met de glans verplaatst** (reparatie 1–3). Na die reparatie kan 9b ook (glans dan diagonaal boven de pupil, zoals Zigzagoon), maar dat blijft Jordi's keuze.
- Omgeving: wenkbrauwboog (19–26, 7–9), twee maskerlobben met een brug 4 (16–17,10) en de maskerrand rechts van het oog (24→22, y 11–15) zijn netjes. Het verre oog (13,11–12) is bevroren en in orde.

## 4. Oren: FAIL (verre oor)
- **Verre oor:** de schedellijn onder het oor (23–25,5)→(26–28,6) stopt 1 px voor de buitenrand. (29,6) is 5, zodat de oorrand (29,5) 3 zonder lijn overloopt in de kopzijde (29,7). Op 12x is dat het "sluit niet" van Jordi. 1 px: (29,6) 5→4.
- **Nabij oor:** rand a/9, holte 4/5 die naar onder lichter wordt, selout 4 boven en 1 rechts. Netjes. De linkerkant loopt in één rechte lijn door in de kopzijde (x 12, y 3–7). Dat komt door het silhouet (voor Jordi).

## 5. Lijf links tussen arm en kop: PASS
- De kleur sluit aan. Onder de kin ligt een slagschaduw 5 (15–17,20)/(16–17,21), daarna een bolle borst 7 met een kern 3 (17–18,23)/(17,24), en via 6 de verre schouder. De horizontale 4-lijn van ronde 7 is weg.
- Klein punt (optioneel): (13–15,19) is nog 7, een lichte rij tussen de crème kin en de schaduw. Daardoor staat er licht-donker-licht onder de kaak. Zie reparatie 6.
- De rechte rand x 15, y 21–27 (7 px) zit in het bevroren silhouet.

## 6. Neus: FAIL (1 px)
- De neus is nu een donkere massa van 3x2 (11–13,16–17) aan de snuitpunt. Dat is goed, geen streep meer.
- De glans (12,16) 7 grenst direct aan de crème snuit (12,15) 9. Op 12x en 2x leest hij daardoor als een **inkeping** (twee donkere puntjes met een gat ertussen), niet als glans op een bolle neus. 1 px: (12,16) 7→4. De neus blijft dan één donkere bol met een zachte glans bovenop.

## 7. Shading: PASS
- Licht linksboven op kop (kruin 3), borst, dij (diagonale sikkel 7, y 36–41), buidel (d linksboven, b rechts) en staartringen (lichte linkerkant). Schaduw rechts en onder volgt de vorm. Geen pillow, geen banding langs de omtrek, geen losse vlekken meer: het 6-vlak achter de kop en de 4 in de onderarm zijn weg.
- Wel gezien, niet als FAIL gerekend: de bovenarmstreep 4-3-6-5-4 (x 30–35, y 21–25), die per 2 rijen 1 px verspringt. Dat leest als cilinder.

## 8. Leesbaarheid 1x: PASS
Op 1x leest hij, op licht en donker, als sluipende wasbeer-Pokémon met masker, witte snuit, wenkbrauw, ringstaart, buidel en klauwen. Doffer dan de echte sprites door het warme grijs, maar dat is bevroren.

## 9. Lijn: PASS
Rood oog in een donker masker, crème klauwen, ringstaart. Hij oogt als een logische eindvorm na olinguito en Coathief (1,28x Coathief).

## 10. Afgekeurde dingen: PASS
Geen helmmasker, geen traan (de onderste oogpixel zit in het oog en verdwijnt bij reparatie 3 als punt), geen trapjes, geen grijs blok, geen klauwen uit de buik, geen jetpack, pose niet horizontaal.

## Reparaties (5 px + 2 optioneel; alleen kleur, buiten bevroren zones)
1. (20,11) e→a: glans naar linksboven.
2. (21,11) a→e: donkere iris boven.
3. (22,13) 2→f: ronde onderkant, lichte iris rechtsonder. Het oog wordt 1111 / a-e-e / f-f-f / 2-f-f: een rond oog met glans linksboven en reflectie rechtsonder. In 9b blijft de pupil (21,12) 1.
4. (29,6) 5→4: de lijn onder het verre oor sluit op de rand (30,6).
5. (12,16) 7→4: neusglans zacht, de neus leest als één bol.
6. *(optioneel)* (14,19) 7→5 en (15,19) 7→5: de slagschaduw begint direct onder de kin.

Daarna opnieuw controleren: alpha-diff 0, verre oog (13,11–12), klauwen, buidel en buikcrème 0 px diff.

## Voor Jordi (silhouet of ontwerpkeuze)
- **Pupil:** 9 of 9b. Mijn advies is 9 (de lijn en Sneasel/Weavile/Mightyena hebben geen pupil; 3 px is te smal voor een pupil in het midden).
- **Staarthaak op 1x:** de bocht is in het silhouet dicht. Een echte haak vraagt 1–2 px lucht tussen punt en schacht (rond x 51–52, y 24–27).
- **Rechte randen in het silhouet:** borst x 15, y 21–27 (7 px) en kopzijde/nabij oor x 12, y 3–7 (5 px).
- **Nabije hand + onderarm** (bevroren handen, vorm uit de render): op 1x leest de hand als een crème blokje met twee zwarte streepjes op de borst. Rechts ervan leest de donkere onderarm (x 28–34, y 26–33) als een klodder met een rechte bovenkant.
- **Mond:** er is geen mondlijn; zo laten of een mondje van 1–2 px.

## Wat ik anders zie dan de vorige keuringen
- **Oog:** `KEURING_ronde8` vroeg om e-a-e / f-1-f / 2-f-2. Dat is uitgevoerd, maar die vorm zelf is het probleem: een gecentreerde glans boven een gecentreerde punt is symmetrisch, en een pupil in het midden past niet in 3 px (SPRITING §11b).
- **Verre oor:** R3 zette (29,6) op 5, niet op 4. Daardoor is de oorvoet nog steeds open.
- **Neus:** ronde 8 raadde een lichtere glans (7) aan. Die raakt nu de crème en leest als inkeping. Ik raad het tegenovergestelde aan: een zachtere glans (4).
- **Ruis:** de maker telde 96 "losse binnenpixels" met een andere maat. Met de 8-buurmaat zijn het er 24, minder dan bij alle 7 echte sprites die ik heb gemeten. De vlekken waar Jordi over klaagde zijn weg.
