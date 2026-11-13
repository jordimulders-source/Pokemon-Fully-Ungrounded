# Poesrups: kleur r4 (alleen kleur en schaduw; vorm van r2 bevroren)

Jordi (13 nov): "ik vind links mooier, ga hem nu nog beter inkleuren, dragonflycave en gen 3 sprite eindkeuring en dan afronden, bug/fairy type".
Start: `../kleur_r2/raster.txt`. Handraster met alleen de gewijzigde stukken: `stappen/r4.txt` (eindstand r4c), gelegd over r2 met `stappen/leg.py` (weigert alpha- en oogwijzigingen). Eerste poging: `stappen/r4a_eerste_poging.txt`.

## Studie (Gen 3-sprites uit de repo, `studie.py` → `studie_vel.png`; luma = 0,3R+0,59G+0,11B)
| Sprite | Tinten voor wit (luma, px) | Stappen | Schaduw / selout / textuur |
|---|---|---|---|
| Silcoon | 255 (29) · 237 (285) · 218 (143) · 191 (81) + lijn 173/107 | 18, 19, 27 | Hooglicht is een klein vlak linksboven; de basis is het grootste vlak; de schaduw beslaat de onderste ±40 % en de grens loopt schuin op naar rechts (een sikkel, geen rechte lijn); diepste tint alleen rechtsonder. Draden: 1-px-lijnen twee stappen donkerder dan het vlak waar ze doorheen lopen (173 op 237, 191 op 218). Bovenrand in lichtgrijs (173), zwart alleen onder en rechts. |
| Dewgong | 255 (97) · 232 (694) · 206 (666) · 164 (171) + lijn 82 | 23, 26, 42 | Schaduw is één grote sikkel onderlangs die naar de staart (rechts) hoger komt; de diepste tint alleen in de onderrand rechts. Omlijning blauwgrijs (82), zwart alleen onderaan. |
| Seel | 255 · 232 (563) · 206 (356) · 164 (77) | 23, 26, 42 | Zelfde recept in klein. |
| Altaria (wolk) | 245 (506) · 224 (397) · 199 (258) · 179 (69) | 21, 25, 20 | Verdeling ±40/32/21/6 %: veel hooglicht (R/S-stijl), elke bol van de wolk een eigen sikkel rechtsonder; pluis = gekartelde grens, geen dithering. |
| Swablu (vleugel) | 255 (95) · 239 (195) · 215 (214) · 161 (83) | 16, 24, 54 | Bolletjes met elk een schaduw rechtsonder; rand in de schaduwtint aan de lichtkant. |
| Castform | 255 · 224 (92) · 194 (148) | 31, 30 | Twee tinten + hooglicht; schaduw rechts en onder, warm grijs. |
| Mareep (wol) | 231 (256) · 196 (177) · 151 (62) · 97 | 35, 45, 54 | Warm; krullen als korte boogjes in de schaduwtint, geen losse pixels. |
| Swinub | 195 · 165 (179) · 133 (95) · 97 | 30, 32, 36 | Vacht: korte streepjes in de haarrichting en een gekartelde onderrand; schaduw rechtsonder als één vlak. |
| Wurmple / Cascoon | segmenten: licht 250/235 → 210–222 → lijn | 28–40 | Elk segment licht links, schaduw rechts tegen de naad. |
| Poedellarve (familie) | 244 (252) · 217 (87) · 196 (73) · 167 (41) | 27, 21, 29 | Elk segment licht linksboven, 7/6 rechtsonder tegen de naad. |
| Poedelmot (familie) | 247 (521) · 215 (269) · 195/174 | 32, 20/41 | Warm crème; R−B 8 → 48 → 64. |

Conclusie: wit bij Gen 3 = 3 vlaktinten onder het hooglicht met stappen van 20–40; de schaduw is een sikkel die naar de van het licht afgekeerde kant (rechts, staart) hoger komt en per bol/segment opnieuw begint; lijnen in het wit zijn ±2 stappen donkerder dan het vlak waar ze doorheen lopen. r2 had dat niet: 478 px wit, 43 px tint 7, en een rechte grens op rij 50/51.

## Wat is gewijzigd (118 van 1058 px van index gewisseld; alpha 0, ogen 0, geen enkele lijnpixel in index 1–4 gewisseld)
1. **Koepel, vlak 1 (kop):** sikkel in 7 tegen naad 1, van (28,44) taps uitlopend naar (25–29,48/49), met 6 in de nok (rij 48–49) die aansluit op de bestaande 6/5-holte van r2. De kop leest daardoor als bol vóór het lijf.
2. **Vlakken 2, 3 en 4:** elk een witte wig links (lichtkant) die naar onder smaller wordt en een 7-wig rechts tegen de naad die naar onder breder wordt; daaronder 6. De grens wit→schaduw is daardoor per segment een schuine lijn en komt naar de staart toe hoger (vlak 1 begint op rij 44, vlak 4 op rij 47 maar is daar al helemaal 7 op rij 49); de rechte grens op rij 50/51 is weg.
3. **Naden:** op dezelfde pixels; tint 6 waar ze door wit lopen (boven), 5 waar links ervan schaduw ligt ((29,44), (30,45–48), (35,43–44), (36,45–48), (40,43–45), (41,46–48), (45,47–50)). Taps: boven licht, onder donker.
4. **Onderrand:** de 777-rij onder het wit (rij 51–52) is 6 geworden (anders lag er licht onder schaduw). Achter is de onderkant donkerder: (41–42,56), (39–44,57), (47–48,56), (47,57) in 5.
5. **Staart:** witte bovenrand blijft (licht van boven); (47–49,53) in 7 als overgang; punt (54–56,54) in 5.
6. **Pootjes:** pootje 3 (29–30,60) van A7 naar 76, pootje 5 (41,59) naar 4. Volgorde nu: 2 licht, 3 middentint, 4 schaduw, 5 het donkerst.
7. **Niet aangeraakt:** kam, pony, gezicht, ogen, loklijnen, buitenlijn (die volgde de regel al: 4 boven, 3 links/rechts van de krullen, 2 onder en rechts; geen afwisseling binnen één rand).

## Palet (oud → nieuw; rest gelijk)
| Index | r2 | r4 | Luma | Stap |
|---|---|---|---|---|
| A wit | 246,244,234 | gelijk | 243,5 | |
| 7 | 226,216,200 | 224,212,190 | 213,2 | 30,3 (was 26,3) |
| 6 | 204,194,174 | 200,186,162 | 187,6 | 25,6 (was 22,4) |
| 5 | 178,162,140 | 172,154,130 | 156,8 | 30,8 |
| 4 | 146,130,112 | 142,124,106 | 127,4 | 29,3 |
| 3 | 104,88,82 | gelijk | 92,1 | 35,3 |
| 2 | 52,40,36 | gelijk | 43,2 | 49,0 |
Geen extra kleur (8 + transparant). Schaduw iets warmer (R−B 34/38/42; model 32–40, mot 48). Geen aparte hooglichttint: A is hooglicht én basis (Altaria/R-S-stijl: veel hooglicht); een tint boven 244 leest niet.
Verdeling r4: A 406 · 7 95 · 6 191 · 5 129 (r2: 478 · 43 · 206 · 95).

## Controle (`controle_uitvoer.txt`)
onbenoemde alpha-diff met het silhouet 0; alpha-diff met r2 0; ogen-diff 0; open randen 0; losse pixels 0; tintclusters < 3 px 0; selout in 10 reeksen van 3–20 px; 8 kleuren + transparant.

## Rondes
- r4a: te vroeg en te breed 7/6 in vlak 2–4 → de witte wiggen waren 1–2 px en lazen als strepen; de achterhelft was grijs.
- r4b: wit breder en langer, 6 pas vanaf rij 48–50. Controle: één 7-cluster van 2 px.
- r4c (eindstand): (34,45) in 7, cluster weg.

## Resterende zwakke punten (eerlijk)
1. **Begin van de 7-wiggen is 1 px breed** langs de naad ((28,44), (34,43–44), (39,43–45)): op 8× een dun streepje naast de naadlijn; op 1×/2× leest het als verdikking van de naad. Keuze: taps begin in plaats van een stompe trap.
2. **Kop is nog een groot wit vlak** (±300 px) zonder eigen hooglichtzone; het volume komt van de sikkel rechts en de schaduw onder de pony. Een extra hooglichttint heb ik bewust niet toegevoegd.
3. **De kam is ongewijzigd** (alleen palet): de krullen hebben geen extra eigen schaduwkant gekregen; dat had lijnwerk van Jordi's goedgekeurde vorm geraakt of 1–2-px-vlekjes gegeven.
4. **Onderrand midden (x23–37)** is nog het r2-patroon van 6 met 5/4-loklijnen; alleen achter (x39+) is hij donkerder gemaakt. De vijf loklijnen blijven dicht op elkaar (r2-punt 3).
5. **De 7-kolom (6,46–49)** langs de linkerrand staat er nog (binnen-AA van r2); strikt genomen loopt die parallel aan de rand.
6. Stap 7→6 is 25,6 (onder de 30); groter maken zou 6 uit de familie van de larve (196) trekken.
