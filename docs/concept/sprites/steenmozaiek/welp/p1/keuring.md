# Keuring welp p1 (patroonvarianten A/B/C), 15 nov

Onafhankelijke keurder, eerst blind beoordeeld: 8× naast r11 en het model (verkleind), 1× naast Seviper, Growlithe, Vulpix en de volwassen steenjaguar.
Palet (alle drie gelijk aan r11): 1 zwart, 2 (59,34,36) donkerste bruin, 3/4/5 bruin donker/mid/licht, 6/7/8 lila donker/mid/licht, 9 (188,178,164) crème-schaduw, 11 (217,204,174) crème, 14 (204,166,148) perzik-crème.

## Keuze: C — **FAIL** (richting goed, nog niet trots te tonen)

### Wat goed is (C)
- Silhouet identiek aan r11 (alpha-diff 0); wijzigingen zitten op het lijf (x 20–48, y 27–55).
- Schouder: geen lijntjes meer maar een ingekleurd vlak (crème ring, lila vulling, ingekerfde spiraal in bruin 3), op de modelplek en groter dan r11, zoals het model met de "staart" naar beneden.
- Heup: leest als spiraal, níet als schietschijf (A's heup is wél een doelwit: lila ring, crème ring, donkere stip in het midden; daarom niet A).
- B bedekt het meest, maar de schouder wordt een grote platte schijf en de heup weer concentrisch; het lijf gaat erdoor 'stickerachtig'. C is de beste balans.
- Bedekking: 228 patroonpixels (r11: 151); lila rugstreep blijft op de modelplek.

### MOET
1. **Oog is per ongeluk gewijzigd (in A, B én C; fout in `basis.py`, die zette patroonkleuren buiten de zone terug naar bruin):** (20,27) moet weer index **6** (nu 4), (21,28) moet weer index **11** (nu 4). Daarna diff tegen r11 voor y < 30 = 0 bewijzen.
2. **Staart onder de schoudering valt uiteen in losse korrels:** (29,50)=11, (30,50)=9, (28,51)=11, (31,51)=9, (33,52)=14 zijn losse stippen met bruin ertussen. Maak er één doorlopende haak van, 1–2 px breed, van de ring (≈x 28–31, y 47–48) omlaag naar ≈(29–31, 53), crème 11 aan de lichtkant links, 9 rechts; zoals het steeltje in het model. Geen geblokte 9/4/9-afwisseling.
3. **Heupspiraal opschonen (x 38–48, y 46–54):** losse crème pixels (45,48)=9, (46,49)=9, (44,51)=9, (46,52)=9, (41,52)=14 en de donkerste-bruin-blokjes (index 2) binnen de spiraal (≈x 42–45, y 50–51) maken er een rommelig 'e'-tje van. Eén doorlopende crème spiraalband (2 px op de bovenste/linker winding, 1 px naar binnen toe) met de groef in bruin **3**, niet in 2 (2 leest als omlijning/gat). Het lichte facet bovenop de heup (index 5, y 47–48) laten staan.
4. **Schouderschijf heeft geen volume:** de lila vulling is vrijwel overal index 8 (één tint), waardoor de schouder een platte sticker wordt en het facet eronder verdwijnt. Zet de onder/rechter sikkel van de schijf (≈x 32–35, y 43–46, binnen de ring) in **7**, en laat de bovenlinker winding 8; de crème ring rechtsonder mag 9 blijven i.p.v. 14 (perzik 14 wijkt in tint af en leest als vlek: (36,45), (25,45), (34,49)). Zo loopt het licht linksboven door het patroon heen, zoals het facet in r11.

### MAG
- Geïsoleerde lila pixels in de rugstreep ((35,33), (34,34), (36,34), (35,35), (37,35) = 7) samenvoegen tot een strakkere 7/8-band langs de rug; nu licht gespikkeld.
- Meer bedekking (Jordi: "het lichaam wat meer bedekt") kan nog met een kleine tweede winding of krul op de achterdij of borst, als het model daar iets toont; niet verzinnen waar het model niets heeft.
- Na de reparaties A's schoudervorm niet terugzetten: A en C zijn daar gelijk; alleen de heup van C gebruiken.

### Oordeel eigenaar-vraag
Zou Jordi dit mooi vinden? Nog niet: de schouder is eindelijk 'ingekleurd' en dat is de goede kant op, maar de losse korrels in de staart en heup lezen als "blurry mess" op 8× en de vlakke lila schijf neemt een stuk 3D weg. Met de vier MOET-punten (vooral 2–4) verwacht ik wel een versie die je trots kunt laten zien.
