# Pitahaya-draak fase 2, sprite r9 (maker): zwart in de mondhoek wordt roze

Jordi (letterlijk): "veel beter, maar het zwart van de mondhoek moet dan roze worden" · "zodat de kleur consistent is". Op de vraag of hij de V links of de mondhoek achterin bedoelde: "de mondhoek". Het is nog niet zeker welke van de twee hij bedoelt, daarom zijn er twee lezingen.

- Script: `maak_r9.py`.
- Vel: `vel9.py` → `vel.png`, met de bek op 12× (model | r8A | r9A | r9B | r9A_achter), r9A op 8×, en alle versies op 1× en 2× op licht en donker.
- Afwijkingen per pixel: `*_afwijkingen.txt`.

## Versies
- **`pitahaya2_r9A.png` en `pitahaya2_r9B.png` (op r8A en r8B), 3 px:** de zwarte bovenrand van de V, (9,44), (10,45) en (11,46), wordt r.
  - Dat is dezelfde selout als de onderrand van de V, (10,47) en (9,48). De lipband rond de insnijding heeft nu één kleur.
  - Tussen de wig (v of donkerst) en het roze zit een toonsprong van ±70 helderheid, en de wig grenst nergens aan lichtroze. Hij loopt dus niet zonder rand in het roze over.
- **`pitahaya2_r9A_achter.png` (op r8A), 2 px:** de V blijft zwart. De zwarte mondhoek achterin wordt roze:
  - (17,43) K→r, zoals de onderkant van de bovenlip (14–16,43) en de mondhoek (17,44);
  - (18,43) K→p, zoals de buren (18,42) en (19,43). Met r gaf hij een dambord met (19,42) r.
  - De kaaklijn (14–16,44) blijft een lijn.

## Bewijs (asserts)
- Alleen de genoemde pixels zijn gewijzigd, dus buiten de bekzone is de diff met r8 0.
- Het silhouet is gelijk.
- De bek is dicht: elke figuurpixel naast transparant is lijn, selout of tand.
- Geen dambord. De bekende lijn-tegen-vulling (16,43)/(17,44) uit keuring_r5 is uitgezonderd.
- De wig grenst niet aan p of P.

## Zelf getoetst
- **r9A/r9B:** de insnijding heeft rondom een roze lip en leest op 2× als een zachtere, schuine rand. De wig blijft als een donker vlak te zien. (10,44) is nog steeds één wigpixel, en hangt alleen diagonaal aan de wig; dat bleef zo uit r8.
- **r9A_achter:** de bovenlip loopt roze door naar de wang, de kaaklijn eindigt op (16,44). Op 2× is het verschil met r8A klein.
