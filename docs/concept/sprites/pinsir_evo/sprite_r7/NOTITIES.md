# Pinsir-evolutie frontsprite, ronde 7 (basis r6)

Jordi bij r6: "stuk beter dan 5 al wel", en naast het model (letterlijk): "de rechterkaak is aan de bovenkant een beetje afgekapt tov het model, desnoods overlapt het de mond maar een klein beetje. links loopt weer net te ver door tov het model, daar zou je iets meer de aansluiting moeten kunnen zien. De ogen mogen iets meer zoals het model ook, niet intimiderend genoeg. Het hoofd is kaal, maar dat is veelal kleurgebruik en afwezigheid van stekels, de vraag is alleen of de stekels kunnen. Het vleugelpatroon is niet goed qua tinten. De rechterschouder is niet rond genoeg en het rechterbeen is ook een beetje een blurry mess, de staart is een stopmpje. Verder is het kleurgebruik en de tinten zijn gewoon niet goed, bijna overal slechts 2 kleurtinten maar"
Over het dekschild: "vleugelpatroon van model is misschien wat te complex, dus kijk vooral naar hoe andere sprites dat doen, incl mega pinsir", "misschien zit daar iets vergelijkbaars tussen".

Bestanden: `pinsir_evo_r7.png` (met kopstekels), `pinsir_evo_r7_zonder_stekels.png` (64×64, geïndexeerd, index 0 transparant, 16 kleuren incl. transparant), `bouw.py`, `vel.png` (r7 met | r7 zonder | r6 op 8×; r7 naast het model op dezelfde maat; dekschild 8× naast Mega Pinsir, Shuckle, Crustle; 1× en 2× naast Gen 3 Pinsir/Heracross/Tyranitar/Aggron), `r7_naast_model.png` (zoals `sprite_r6/r6_naast_model.png`). Bouwen: `cd pinsir_evo && python3 sprite_r7/bouw.py [raster|detail]`.

## Per punt
1. **Rechterkaak** (tabel `KOP`, gemeten op het model, rooster 16× en 40×): de bovenkant staat nu op rij 29 (was 30), afgerond met kaaklijn-hoekjes (x25 rij 28, x26 rij 29–30); x22 rij 30–33 is kaak geworden (1 px over de rechterrand van de mond), x21 is de zwarte scheiding tegen de tanden.
2. **Linkerkaak**: eindigt bij x14 in de donkere kaaktint, x15 rij 29–31 is de kaaklijn en rij 28 zwart. Daarna begint de gezichtsplaat, dus de aansluiting is zichtbaar (model: kaak eindigt bij x≈14,5).
3. **Ogen**: zoals het model een zwarte wenkbrauwband op rij 27 (tussen de ogen donkere lijntint), met lage witte spleten eronder. Ver oog: verticaal x16, rij 27–28. Nabij oog: x21–23, rij 28. Oog A (pupil binnen-onder) vervalt.
4. **Kopschild**: volle tintreeks (5 tinten, lichte voorfacet linksboven, donkere achterkant) via de nieuwe vulling (punt 9).
   - Stekels (variant): de randstekels van het model op (15,19), (18,18), (23,17), (26,15) en (44,18) zijn nu 3 px breed aan de basis (zwart | licht | zwart). Dat zijn 4 nieuwe silhouetpixels: (14,20), (17,19), (25,16), (45,19).
   - Drie kegeltjes op het schild zelf (model: (27,20), (32,19), (36,19)) als lijntint-punt met een licht/donker paar eronder.
   - `_zonder_stekels.png` heeft silhouet-diff 0 met r6.
5. **Dekschild**: voorbeeld Mega Pinsir (vleugel: een paar grote vlakke vlakken in een contrasttint direct tegen de basiskleur, zonder eigen lijn), daarnaast Crustle (banden die de vorm volgen); Shuckle ter vergelijking (vlekken met lijn, niet gebruikt).
   - Op het model gemeten dwars op de lengteas: lichte randbanen aan beide lange kanten, twee donkere langsbanen (u −2,2 en +2,5) en een gemengd midden. De streepjes zelf zijn op 64 px ruis.
   - r7: oker in 3 tinten (licht randbaan / midden / schaduw aan de punt en de onderrand) plus twee donkere langsstrepen. Die zijn onderbroken waar het model daar licht is en om de ±5 px, zoals de streepjes van het model. In het midden staan de sterkste modelvlekken.
   - Tinten dichter bij het model: tekening 53, schaduw 84, midden 117, licht 156 (model: 77,46,22 / 139,100,69 / 184,143,105).
6. **Rechterschouder**: cirkel gemeten op de modellijn (Hough: midden (35.6, 35.0), straal 3.5 spritepx). Binnen de bol staan geen binnenlijnen, alleen bolschaduw in 4 tinten met hooglicht linksboven en een sikkel rechtsonder. De rand wordt lijntint waar het model een lijn heeft.
7. **Rechterbeen**: de knie is ook zo'n bol (midden (44.6, 52.8), straal 2.9). Dij en voet zijn eigen vlakken met 4–5 tinten. De verre knie (24.2, 50.0, r 2.4) is een stap donkerder.
8. **Staart**: de segmenten 209/206/213 en de punt 166 zijn één vlak met 193, dus geen verticale strepen meer. Een lichte band loopt langs de bovenkant tot in de punt, zoals het model (bovenkant khaki, onderkant donker). Silhouet is ongewijzigd: de staartlengte gelijk aan het model (punt x63, y44–46).
9. **Tinten per vlak**: elk vlak krijgt via rangorde van een lichtscore een reeks opeenvolgende tinten.
   - De lichtscore is de modeltoon binnen het vlak (gladgestreken) plus het vormlicht: linksboven licht, rechtsonder schaduw.
   - Vlakken van ≥ 30 px krijgen 4 tinten (glans alleen waar het model glans heeft), vlakken van 10–29 px 3 en kleine vlakken 2.
   - Donkere vlakken (romp, verre ledematen; model bijna zwart) gebruiken de lijntint als diepste schaduw. Zo gaan de lijnen daar in het donker op.
   - Het lijfpalet is donkerder dan in r6, zoals het model: 33 / 55 / 88 / 126 / 172.

## Tinten per vlak (vulling, zonder buitenrand en binnenlijnen; r7 tegen r6)
| onderdeel (vlak) | px | r7 | r6 |
|---|---|---|---|
| kopschild (12) | 138 | 5 | 3 |
| dekschild (35) | 235 | 5 | 3 |
| schouder/bovenarm (69) | 46 | 5 | 3 |
| onderarm (135) | 46 | 3 | 3 |
| dij/knie (159) | 52 | 5 | 3 |
| voet nabij (237) | 34 | 4 | 2 |
| staart (193) | 66 | 4 | 2 |
| romp: borst 50 / kraag 55 / buik 99 / onderbuik 179 | 29 / 15 / 34 / 18 | 3 / 3 / 3 / 3 | 2 / 2 / 2 / 2 |
| rug (1) | 37 | 4 | 3 |
| kop (46) | 18 | 3 | 1 |
| verre knie (185) / verre voet (243) | 30 / 30 | 3 / 3 | 2 / 1 |
| verre onderarm (107) | 25 | **2** | 1 |
Vlakken ≥ 20 px met minder dan 3 tinten: **r7 1 (verre onderarm), r6 7** (van 13). Kleine vlakken (klauwen, stekels < 10 px) hebben 1–2 tinten.

## Controle
- Silhouet-diff met r6: zonder stekels 0, met stekels 4 (zie punt 4). Mond ongewijzigd behalve de kolom x21 (rij 30–33 zwart, punt 1).
- Zwart 19,4 %. Zwarte binnenpixels 44 (r6 39): de 5 extra zijn de wenkbrauwband en de mondrand x21, alle in het gezicht. Daarbuiten staat geen zwart.
- Tintvlekjes < 3 px (8-samenhang): r7 15 (r6 6). Daarvan zijn 4 gezicht (bevroren), 5 de bedoelde lichte stekel/kegelpixels (alleen in de variant met stekels) en 6 echte (o.a. (31,33), (42–43,42), (27,50–51), (37,54)).
- Kaaklijntint vervalt: de kaak gebruikt de schildlijntint (66,36,18; bijna gelijk aan 72,28,22). Die paletplek is nu de lichte okertint van het schild.

## Zelf geziene zwakke punten
- Het onderlijf (verre arm, ver been, voeten met klauwen) blijft druk; het model is daar ook complex. Klauwen lezen op 1× matig.
- Verre onderarm heeft maar 2 tinten.
- De dekschildstrepen zijn een vertaling van de langsbanen van het model, geen 1-op-1 tekening (zoals Jordi vroeg). Ze lezen iets regelmatiger dan het model.
- Ogen zonder pupil (model heeft er ook geen); als Jordi oog A's pupil terug wil, is dat één pixel per oog.
- Kopstekels zijn op 64 px klein (3 px). Leesbaar op 2×, op 1× vooral als rafel op de rand.
Verse keurder nodig vóór Jordi.
