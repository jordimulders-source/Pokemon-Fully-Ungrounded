# Eindkeuring onweerswolk-Altaria r5 (Dragonfly Cave-stijl, 21 nov)

Getoetst: `altaria_r5.png` tegen het model (`model_kop/natief_kop15_dy10.png`, 3×3 natief per spritepixel, blok (X,Y) = natief x 3X+4, y 3Y−13), de goedgekeurde Swablu (`../af/swablu.png`) en Gen 3 Altaria/Swablu/Castform/Salamence/Flygon. Proefkopie met alle MOETEN: `proef_eindkeuring.png` (94 px anders dan r5, alpha +1/−1).

## Oordeel per punt
- **Kop, ogen, snavel:** goed. Linkeroog (22,22–23) en rechteroog met glans (27–28,22–23) lezen beide op 1×; zwart alleen in de pupillen; snavel + wang volgen het model. Bevriezen.
- **Belijning:** gekleurde selout (navy 2 op de wolk, donkerviolet 7 op kop/kuif), geen zwart buiten de ogen: voldoet aan "zachter en niet zwart". Op donkere achtergrond valt de wolkrand weg, net als bij de goedgekeurde Swablu: aanvaard.
- **Korrel:** 61 tintvlakjes < 3 px in de wolk (4-buur), waarvan 27 los middentint 4/5 zonder functie (geen kaprand, geen naad). Moet weg.
- **Kuif:** twee strengen lezen, schokkerig zoals bedoeld. Fout: losse donkere pixels in lichte twijgjes (korrel) en een gat van 1 px in de donkere onderrand van de bovenste streng (33,11).
- **Static:** leest als static, maar de lange lijn in de rechtervleugel is op 6 plekken 2 px dik (klonten/L-hoeken); daardoor trekt hij meer aandacht dan het model toelaat. Losse navy pixel naast de vonk links (3,26) leest als vuil.
- **Volume onderkant:** de onderste bol (Y57–61) is lichter (4) dan het lijf erboven; het model is daar donker (2/3). Leest als licht van onderen (pillow). Moet donker.
- **Rechtervleugel:** kappen van bol A en B zijn 2 px hooglicht en mengen met de static; na de lijst hieronder lezen A, B, Rb en C als losse kappen, maar nog zwakker dan links.
- **Bollen in het lijf:** het lijf leest op 1× nog als gelaagde platen (rechte naden Y49, Y52–53, Y55–56 en de rechte naad (7–11,25) links), niet als de ronde bollen van het model en de Swablu. Dat is geen pixellijst meer maar een zone-opdracht (zie MOET 6).

## MOETEN (getest op `proef_eindkeuring.png`; paletindex van `altaria_r5.png`)
1. **Ontkorrelen (27 px; regel: los vlakje < 3 px van tint 3/4/5, niet aan de buitenrand, niet aan een kaphooglicht 6, niet in kop/snavel X19–33 Y22–28 → meerderheid van de 4-buren):**
   - 4→3: (6,19) (7,19) (10,20) (14,21) (13,23) (12,24) (13,31) (12,32) (47,23) (50,22) (55,19) (45,34) (44,35) (45,46)
   - 4→5: (8,18) (13,20) (43,25) (22,33) (22,34) (48,34) (49,35) (14,38) (31,51)
   - 5→3: (18,23) · 5→4: (37,30) (38,30) · 3→4: (43,26) (44,26)
2. **Kuif (6 px):** twijgjes één tint: (31,7) (35,7) (36,6) (35,9) 7→9; donkere stip in licht (33,10) 7→10; gat in de onderrand dicht: (33,11) transparant→7 (model: onderrand doorlopend).
3. **Static 1 px dik (7 px):** (54,19) (54,26) (53,28) (52,29) (51,30) 11→3; (55,24) 11→4; (50,31) 11→2 (naad loopt door).
4. **Vonk:** (3,26) 2→transparant.
5. **Kappen rechtervleugel (8 px, plek uit het model):** bol A (56,18) (57,18) 5→6; bol B (49,21) 5→6, (47,22) 5→6, (46,22) 6→5; bol Rb (45,23) 5→6, (46,23) 6→5 (B en Rb niet meer aan elkaar); bol C (41,26) 5→6.
6. **Onderste bol donker (44 px):** in Y57–61 elke 4 → 3 (model daar 2/3; licht linksboven, schaduw onder).

Na 1–6: 0 nieuwe losse tintvlakjes in de static/kuif, wolkvlakjes < 3 px van 61 naar 41 (de rest zijn kaprand-/naadpixels), silhouet ±1 px.

## MOET 6b (zone-opdracht voor de maker, niet als pixellijst te geven)
Lijf X10–53 Y44–57 en rechtervleugel X38–60 Y19–31: **neem de bolgrenzen over uit het model** (meerderheidsband per blok, niet het gemiddelde: zie GEMINI.md "Blur door gemiddelde tint"). Elke modelbol krijgt een gebogen onderboog in 3 (niet 2) die de bol volgt in plaats van een rechte naad over 5+ px; per bol een hooglichtkern 6 van ≥ 3×2 linksboven waar het model 'licht' is (lijf: grote voorste bol X23–33 Y39–46, kleine bol X31–35 Y48–51; rechtervleugel A X56–59 Y16–18, B X47–51 Y20–22, C X40–44 Y24–26). Kop, kuif, static en silhouet diff 0.

## ZOU KUNNEN
- Linkervleugel: kappen L1–L3 1 px groter naar het model (model-kap ±4×3); rechte naad (7–11,25) gebogen.
- Static-tint 11 iets koeler/lichter (bv. (168,222,244)) zodat hij niet met hooglicht 6 (L180) verward wordt; nu L195.
- Kuif: vork rechtsboven (42–47,6–10) is een 1 px trap; mag zo blijven (schokkerig).

## PASS/FAIL
**FAIL.** Met MOETEN 1–6 is hij netter (korrel, kuif, static, onderkant), maar het lijf en de rechtervleugel lezen nog niet als ronde bollen zoals het model en de Swablu ("echt een goede nette versie" is het dan nog niet). PASS verwacht na MOET 6b, mits geen nieuwe korrel en diff 0 op kop/kuif/static.
