# Sauna-yeti (sneeuwmonster fase 3): eindkeuring (27 nov)

Bron: `../sprite_r6/sauna_yeti_r6.png`. Model (bevroren): `../model.png`, gemeten via `../natief.png` (pitch 5,867) en `gemeen.model_op_schaal()` (vlakgemiddelde per spritepixel). Vergeleken op 8× en 1× naast fase 2 (`../../sneeuwmonster_fase2/af/`), de maatstaf (Skinguin, Dundragoon, Zapacha, Princadee) en Gen 3 `anim_front_gba.png` (Ursaring, Slaking, Absol, Glalie).
Jordi: "let vooral op de ton bovenop die is nog niet goed qua kleurtinten, schaduw etc, zelfde voor het gezicht". Opdracht: schaduw, belijning, kleurtinten (Dragonfly Cave).
Bevroren (assert index-diff 0 in `bouw.py`): silhouet, ogen/pupillen/neus/mond-haak, alle steenpixels. Niets hertekend: alleen de index van bestaande pixels en twee paletwaarden, elk op een gemeten modelwaarde.

## Oordeel vooraf (r6)
**Emmer: FAIL op tinten/schaduw.** Gemeten modelhout (natieve cellen, gekwantiseerd): licht (200,152,112) L161 (de meest voorkomende houttint), midden-licht (184,128,88) L140, midden (140,84,48) L95, donker (96,56,32) L65, diepst (64,32,24) L40. In r6 is 49 van de 70 houtpixels `#` (132,78,42) L91: die ene tint was tegelijk outline base, naad tussen de duigen en de vulling van de hele schaduwkant. Gevolg: de schaduwkant (model L56–86) was te licht, de lichte kant te donker (naden op x30 en x33 donker terwijl het model daar 4 van 4 lichte cellen heeft), en de outline base links had amper contrast met het hout ernaast. De band was één grijs (88,92,104) L92 over de hele breedte; het model heeft licht linksboven (L132–151), midden (L98–117) en donker rechts/onder (L56–77).
**Gezicht: BIJNA.** De vlakverdeling per pixel klopt met het model (huidaandeel per pixel gemeten: de h-pixels liggen op de modelhuid). Twee tintfouten: (1) h (208,226,244) hue 210 is lavendelblauw, de modelhuid is cyaan (201,227,236) hue 199, dezelfde familie als handen en voeten (kale huid); daardoor las het gezicht als witte vacht in plaats van huid. (2) De lichtere gezichtslijnen (wenkbrauwen, wang-, kin- en kaaklijn) waren s (120,156,190) L149; het model heeft daar een teal lijn (100,136,154) L~128 (mediaan van de modelcellen L110–150 in het gezicht), donkerder en groener. 4 huidpixels stonden op w/m (model huid ≥ 50 %, L204–225).
**Belijning: BIJNA.** Buitenlijn 1 px, l aan de lichtkant, K aan de schaduwkant, geen lichte kleur op de buitenrand. Restpunten: zwarte binnenlijnen (rechterarm over het lijf, linkerarm, hand- en voetcontour; 38 px), de schaduwband onder de rechterarm in lijntint l (2–3 px dik met de zwarte lijn ernaast = een lijn van 3 px), een 2×2-knoop bij de arm, dubbele onderrand van de rechterhand, geen outline highlights.
**Schaduw rest: PASS.** Licht linksboven, sikkel rechts en onder, onderlijf m; gebogen grenzen; losse s/m-pixels in de vacht zijn modelstrengen (bewust laten staan, geen "rustiger maken").

## Uitgevoerd (`bouw.py`, 113 px index-diff + 2 paletkleuren)
| stap | px | wat (gemeten) |
|---|---|---|
| P1 palet | – | hout donker 7: (132,78,42) L91 → (100,58,38) L68 = model donker hout (96,56,32) L65 / schaduwkant L56–86. Ramp nu 9 L155 / 8 L115 / 7 L68 / K, stappen 40/47/36, hue 28 → 27 → 19 (naar rood in het donker). 7 = outline base van de emmer (eigen donkerste tint) |
| P2 palet | – | h: (208,226,244) hue 210 → (200,226,236) L219 hue 196 = modelhuid (201,227,236). 59 van de 65 h-pixels lagen in het gezicht; de 6 overige zijn lichte vachtplekken (model daar ook cyaan, hue 199–201) |
| E1 | 11 | houtvulling per pixel = meerderheid van de natieve houtcellen (licht ≥ 140 / midden 95–140 / donker < 95; zelfde regel als de kale reductie van r1). Gelijkspel → midden; een r6-naad blijft midden als donker+midden ≥ de helft van licht; donker naast de buitenlijn → midden. (34,12) d→b 5/4/0 · (33,13) #→b 4/0/0 · (37,13) #→d 0/2/2 · (30,14) #→d 2/1/1 · (33,14) #→b 4/0/0 · (36,14) #→d 0/4/2 · (37,14) #→d 0/2/2 · (29,15) b→d 3/2/4 (naast de rand) · (30,15) #→b 4/1/0 · (32,15) b→d 3/3/0 · (33,15) #→d 2/4/0. Hout nu licht 13 / midden 16 / donker 39 (r6 11/10/49): licht linksboven, midden in het midden, donker rechts, naden op hun gemeten plek (x30 r13–14, x37) |
| E2 | 12 | band (r6 alles g): licht s op (28,16) (30–32,16) (model L132–151); donker c (steen, (52,50,58)) op de onderrand rechts (38,17) (36,18) (37,18) (40,18) (41,18) (40,19) (model L56–74); linkereind (27,16) (26,17) # → c = outline base in de eigen donkerste tint van de band. Band nu s 4 / g 17 / c 8: licht linksboven, donker rechtsonder, zoals het model |
| G1 | 18 | gezichtslijnen s → a (96,140,156) L128 = gemeten modellijn in de huid (100,136,154): wenkbrauwen (26,22) (29,22) (31,22), voorhoofd-/brauwboog (32,21) (33,21) (35,21) (36,22) (30,23) (37,23), wang/kaak (25,27) (35,27) (35,28) (26,29) (27,30), kin (27–30,32). Alleen s-pixels die aan ≥ 67 % huid grenzen; plek en vorm gelijk, alleen de tint. De lijnhiërarchie blijft: leden/contour l L90 → plooien a L128 → huid h L219 |
| G2 | 4 | huid w/m → h (modelhuid ≥ 50 %, L204–225): (27,22) (37,22) (27,25) (33,25). Het ooghoekje (32,24) m bleef staan (oogzone bevroren) |
| B1 | 21 | schaduw onder de rechterarm: de l-band x42–44 r33–41 is in het model de teal schaduw van het lijf (L124–136), niet de lijn → a (16 px); waar het model lichter is (L144–157) → s (5 px): (42,37) (40,39) (41,39) (43,40) (44,41). De lijn zelf blijft 1 px op x45 |
| B2 | 38 | binnenlijnen niet zwart (DC: "black for the outline and the very deepest shadows"; binnenlijnen in de donkerste eigen tint): K → l op dezelfde plek. Rechterarm 26 px (x43–48, r32–49), linkerarm 4 px (17,38) (16,39) (15,40) (15,41), contour rechterhand (45,50) (45,51), linkervoet (41,53–55) (40,56) (40,57), (33,57) (zwart tussen twee l, om en om) |
| B3 | 1 | (46,36) l → m: 2×2-lijnblok op het knooppunt van de twee armlijnen (model L192) |
| B4 | 4 | dubbele onderrand rechterhand: l boven de zwarte buitenlijn (52,55) (54–56,55) → a (hand midden), lijn weer 1 px ("always one pixel wide") |
| B5 | 4 | outline highlights in s op de lichtste lijnpixels van schouder/arm linksboven (model L211–226): (15,30) (14,31) (7,37) (6,38). Zelfde aanpak als fase 2 (B9) |

Diff per zone: silhouet 0, ogen/pupillen/neus 0, stenen 0 (assert). Emmer 23 px, gezicht 22 px, armen/handen/voeten 68 px.

## Palet na (16 incl. transparant)
0 transp · 1 K (24,32,56) · 2 l (62,96,140) L90 · 3 s (120,156,190) L149 · 4 m (162,191,222) L185 · **5 h (200,226,236) L219 (huid)** · 6 w (244,250,255) L248 · **7 (100,58,38) L68** / 8 (160,104,56) L115 / 9 (204,144,88) L155 hout · 10 g (88,92,104) · 11 a (96,140,156) · 12 A (136,170,180) · 13 c (52,50,58) · 14 o (232,124,44) · 15 y (244,192,80).
Niets samengevoegd: het palet bleef vol; de band leent s (licht) en c (donker), zodat er geen extra grijs nodig was.

## Controles na
Geen lichte kleur op de buitenrand. Zwart binnen de figuur alleen nog: pupillen, neus, mondhaak, stenen, de vingerplooien van beide handen ((5,50) (6,51) (4–6,52); (46–48,51–53) (51,55)) en hoek (40,58). Geen 2×2-lijnblokken buiten ogen, stenen en vingers. Emmer licht/midden/donker 13/16/39, band 4/17/8.
Gen 3-vergelijking: Ursaring/Slaking `_gba` hebben 24/61 zwarte pixels binnen de figuur (vingerplooien, diepste hoeken); de resterende zwarte vingerplooien vallen daaronder ("the very deepest shadows").

## Ter info voor Jordi
- **Band:** het lichte deel van de band is s (120,156,190), een koel blauwgrijs, omdat het palet geen plek heeft voor een neutraal lichtgrijs (model (152,144,136)). Op 1× leest hij als stalen band met licht links; Gen 3-staal is ook koel blauwgrijs. Wil je hem neutraler grijs, dan moet er een paletkleur weg (bijv. geel 15, 7 px in de stenen).
- **Zwarte armlijnen:** r6 had de lijn van de rechterarm over het lijf zwart (model ook zwart). Volgens de DC-regel zijn het binnenlijnen en zijn ze nu lijntint l; de schaduw eronder is teal zoals in het model. Wil je de zwarte versie terug: dat is alleen B2 (38 px), los terug te zetten.
- **Vingers:** de zwarte vingerplooien (linkerhand 3×2 boven de onderrand, rechterhand) zijn niet aangeraakt: in het model zwart, en het is detail.
- **Steenfacetten:** de facetten zijn koel grijs g (88,92,104) L92, het model is warmer en donkerder (77,61,61) L66. Niet veranderd (stenen bevroren, zelfde tint als fase 2).

Bestanden: `sauna_yeti_ek.png`, `sauna_yeti_8x.png`, `vel.png` (r6 | ek | model op 8×; emmer en gezicht op 16× als r6 | ek | model; 1× op licht en donker naast fase 2, Skinguin, Dundragoon), `bouw.py`.
