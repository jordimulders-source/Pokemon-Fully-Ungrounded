# Herkeuring Pinsir-evolutie v2 r3 (23 nov, onafhankelijke keurder)

Getoetst: `pinsir_evo_v2_r3_A.png` en `_B.png` tegen `referenties/model_v2_r4.webp`, op dezelfde maatstaf als `sprite_v2_r2/KEURING.md`: de twee eisen, met lijnen, schaduw en tinten op Gen 3-niveau.
Hulpbeelden in `keuring/`: `kop_16x.png`, `kop_1_2_4x.png`, `gezicht_28x.png`, `rug_14x.png` (A | B | model), `linksonder_16x.png`, `rechtsonder_14x.png` en `raster_AB.txt` (index per pixel, E = 14).

## Eindoordeel: BIJNA, met rug B (na de reparaties hieronder)
Rug A voldoet niet: zie Rug.

## Controle van de r2-reparaties
| r2-punt | Status | Opmerking |
|---|---|---|
| Te licht | ✔ | Eigen meting klopt met `helderheid.md`: alle vlakken binnen ±6. Index 6 hoort nu alleen bij room. |
| Kopschild effen en verticale knip | ✔ | Schuine lichte band 14, vlak 5, onderrand 4 over de hele breedte, lichte streep rechtsonder. Geen knip op x 20–21. Drie tinten. |
| Selout lichtkant schild | ½ | De zes pixels zijn 2, maar **(12,14) is nog 1** tussen 2-pixels (12,13) en (11,15). |
| Ogen | ✔ | Recept goed uitgevoerd. Op 1×, 2× en 4× (`kop_1_2_4x.png`): twee gele spleten onder de rand met een zwarte balk eronder. Eén boze blik, niet scheel. Het rechteroog is groter, net als in het model. |
| Verre been en voet | ✔ | Knobbel, lijn (19–23,54), rand (18,51–53), sikkel en twee gescheiden klauwen staan op de modelplekken. |
| Nabije hand | ✔ | Drie klauwen met zwart eromheen, geen dambord meer. Klein, maar leesbaar zoals in het model. |
| Knie, dubbele lijn, banding-stroken | ✔ | Binnenkant 5 met hooglicht 14, één lijn, geen lichte stroken meer op y 46–47. |
| Koepel en onderarm | ✔ | Koepel 5 met hooglicht, onderarm 4 met een lichte rand. |
| Buik | ✔ | Vlak 7 (modeltint), hooglicht 8 linksboven, sikkel 6. |
| Kaakrood | ✔ | 12 = (172,98,82). Kaken gemeten 90, model 90. |
| Rugstekels | ✔ | Zes driehoekjes van 3 px op de gemeten modeltoppen, met lichte flank links en donkere rechts. Silhouet: +47 px en 0 px weg (geteld tegen r2: klopt). Ze zijn kleiner dan in het model, maar lezen als de gekartelde rij uit het model. |

## Nieuwe fouten en restpunten (geldt voor A en B, tenzij anders vermeld)
1. **Open buitenlijn door de nieuwe rugrand** (geen lichte kleur op de buitenrand, geen open randen): vulpixels grenzen direct aan transparant.
   - (48,24) index 3 wordt 1. Dat is de inkeping vóór de stekel op x 50.
   - (54,29) index 5, (55,29) index 3 en (56,29) index 3 worden 1. Dat is de onderkant van de stekelvoet boven de steile rand op x 53.
2. **Verre-beenknobbel overschrijft de buitenlijn**: (15,49) is 14 op de silhouetrand, tussen (15,48)=1 en (15,50)=1. Wordt 1. Het hooglicht blijft op (16,49).
3. **Nabije scheen is een effen vlak**: x 36–44, y 55–60 bestaat uit 48 px die allemaal index 4 zijn. Het model is hier links lichter en rechts donkerder. Reparatie:
   - linkerrand binnen de lijn (36,56)–(36,59) en (37,55)–(37,58) wordt 5;
   - rechterrand (44,55)–(44,59) en (43,59)–(43,60) wordt 3 als sikkel;
   - het midden blijft 4.
4. **Licht pixel tussen de ogen**: (16,21) is 14. Dat is het lichtste bruin, midden op de neusbrug tussen de ogen. Het model is daar donker. Wordt 4.
5. **Selout schild**: (12,14) 1 wordt 2 (zie de tabel).

## Rug A tegen B
- **A**: de tinten zijn goed verdeeld (3/4/5 = 69/137/66 px in x 36–53, y 22–45). Maar de rug blijft een kriskras-net van 110 naadpixels die niet in de richting van de modelbanden lopen. Op 1× en 2× leest dat als ruis, en dat is geen Gen 3. **Voldoet niet.**
- **B**: de naden lopen nu diagonaal langs de rugrand, zoals de modelbanden. Dat is trouw en rustig. Maar de platen zijn bijna effen: 278 px index 4 tegen 29 px 5 en 27 px 3 in hetzelfde vak. Het beschreven hooglicht en de schaduw per plaat zijn nauwelijks terug te vinden. Dat is de Coathief-les ("erg effen 2 kleuren"). **Voldoet na deze reparatie:**
  - per plaat de 1–2 rijen direct onder elke naad 4→5. Dat zijn de lichte bovenranden, bijvoorbeeld (41,29),(41,30),(42,30),(43,30),(43,31),(46,33),(47,33),(49,35),(49,36),(47,41),(49,42),(49,43),(51,42),(51,43),(41,35). Doe dit langs **de hele lengte** van elke naad, niet alleen waar B van A verschilt;
  - de rij direct boven elke naad 4→3 (schaduw), bijvoorbeeld (38,25),(41,27),(42,27),(45,29),(46,30),(47,31),(49,33),(41,32),(47,38),(49,40),(52,41), ook weer langs de hele naad;
  - per plaat de 1–2 kolommen langs de rechter-/onderrand 4→3, zodat de plaat bol oogt;
  - doel: binnen elke plaat zichtbaar licht boven en donker onder. Het gemiddelde moet ±105 blijven (model 102), dus evenveel 5 als 3.

## Kort
BIJNA, rug B. Over: vijf buitenlijnpixels dicht (punten 1–2), de nabije scheen bol maken (punt 3), (16,21) en (12,14), en volume per rugplaat in B. Daarna is de sprite wat mij betreft klaar voor Jordi. Rug A valt af door de naadruis.
