# Keuring r5 – pitahaya-draak fase 2, `sprite_r5/pitahaya2_r5.png` (alleen de bek)

Eerst blind gekeken, daarna `sprite_r5/NOTITIES.md` en `studie_open_bek.png` gelezen.
Hulpmiddelen in deze map:
- `zij.py` → `bek_r5.png` (bek op 18× naast het model, met raster);
- `1x2x_licht.png` en `1x2x_donker.png` (r4 | r5, op 1× en 2×);
- `gen3_open_bek.png` (Feraligatr, Croconaw, Gyarados, Sharpedo, Exploud en Salamence op 4×);
- `meet.py` (clusters, dambord).

Diff met r4: 23 px, allemaal binnen x 9–17, y 42–48. Het silhouet is gelijk.
Letters: v = (155,154,159) nieuw donkergrijs, w = (191,189,192) grijs, W = (237,234,237) wit, s = pit, K = zwart, r/p/P = roze van donker naar licht.
**Vervallen (melding coördinator):** het roze binnen de bek (verre lip en binnenrand) wordt in r6 een donkere tint van het wit/grijs. Opmerkingen over die roze pixels zijn daarom alleen beschrijving, geen reparatie.

## Oordeel: FAIL. Alleen punt 2 (bovenlip) faalt; punt 1 en 3 zijn in orde.

### 1. Leesbaarheid van de delen (2× en 1×)
- **Bovenlip met tanden:** leest als zwarte kaaklijn met 2 witte tandjes (4,43) en (8,43). Dat zijn tanden van 1 px tegen het lichte of transparante vlak, zoals bij Sharpedo en Salamence.
- **Bovenkaak/wig:** de donkergrijze wig (10–13, 43–45) leest op 2× als schaduw onder de bovenkaak. Croconaw en Gyarados doen het net zo: de donkerste tint zit bovenin en achterin de bek. Dit is een duidelijke winst ten opzichte van r4, waar dit het grijze vak was dat Jordi omcirkelde.
- **Verre lip:** op 12× is het een roze diagonaal (10,46) → (13,45). Op 2× is hij dun maar zichtbaar, op 1× valt hij weg in de toonsprong. Dit vervalt, want r6 maakt hem grijs.
- **Witte onderkaak/tong:** leest op 1× en 2× als licht vlak met pitjes binnen de lipband, het lichtst vooraan links. Dat is de Gen 3-opbouw van Croconaw en Exploud. Gehemelte (v) en tong (W) verschillen 2 tintstappen, zoals in de studie.
- Achterin, op x14–16 en y45–48, loopt de tong grijs (w) door tot onder de kaaklijn. Dat volgt het model en leest als schaduw achterin.

### 2. Bovenlip nog een rechte lijn?
**Ja, deels.**
- Achterin zakt hij nu in stappen: (12–13,43) en (14–16,44).
- Het voorste stuk is nog 9 px recht op rij 42, van x3 tot x11. Op 1× en 2× leest de bovenlip daardoor nog steeds als liniaal.
- Het model is hier ook recht (de maker heeft dat gemeten), maar Jordi gaf vrij om naar Gen 3 te kijken.
- Croconaw en Gyarados laten de kaaklijn in steeds kortere stukken naar de mondhoek zakken, en hebben geen lange rechte run.

### 3. Netheid in de bekzone
- Het grijs heeft 3 tinten (v/w/W) plus de pit; dat mag. Zwart binnen de figuur is 5,6 %.
- Het dambord (16,43)/(17,44) is een lijn tegen vulling bij de mondhoek: normaal.
- Losse pixels:
  - p (10,45) en p (17,45) vervallen, want het roze binnen de bek gaat in r6 weg.
  - W (15,49) mag blijven; het modelblok is 6/9 licht (zie keuring_r3).
  - v (11,45) hangt diagonaal aan de wig; geen probleem.
- Pit (10,48) staat in de hoek tegen de lipband. Het is de grootste pit uit het model, op zijn modelplek. Hij mag blijven.

## Reparatie (herleid tot Croconaw/Gyarados, Gen 3)
1. **Bovenlip als trapcurve 7–4–3 in plaats van 9–2–3:** laat de kaaklijn al na de tweede tand zakken, zoals de kaaklijn van Croconaw en Gyarados in kortere stappen naar de mondhoek loopt.
   - (10,43) en (11,43): v → K. De lijn ligt nu op rij 43 voor x10–13.
   - (10,42) en (11,42): K → r. Dat is het roze van de bovenkaak, dezelfde tint die de maker al op (14–16,43) boven de zakkende lijn gebruikt.
   - Tanden (4,43) en (8,43), en rij 42 van x3 tot x9, blijven gelijk. De tanden hangen dan nog onder de lijn.
   - De wig blijft zichtbaar, als (10,44), (12,44), (13,44) en (11,45) met pit (11,44).
   - Ziet dat te leeg uit, maak dan als variant ook (9,42) → r, met (9,43) als lijn. Daarvoor moet (9,43) K blijven, wat al zo is.
   - Meet daarna op 2× of rij 42 niet meer als rechte lijn leest.
2. Niets anders. Het roze binnen de bek gaat in r6 naar grijs (Jordi). Houd daar dezelfde toonvolgorde aan: wig donkerst, tong vooraan het lichtst.

Diff buiten (9–11, 42–43): 0.
