# Nachtaap fase 3: kleurronde 1h (5 nov), kleine afronding op 1g

Basis: `../ronde1g/` (blijft staan). Bron: `bron/ronde1h.txt` (bovenop 1g) → `bron/bouw.py`; `bron/check.py` (bevroren delen t.o.v. v7, diff per punt t.o.v. 1g); `bron/vel.py` (1h naast 1g); `bron/zoom.py`.
Opdracht: klein (Jordi: "niet extreem ingrijpend"), ≤ ±60 px. **Totaal 44 px diff met 1g; 1 px buitenomtrek.**

## Bevroren (check.py, t.o.v. v7)
Kop/gezicht/maan 0, hand/gloed-kleuren 0, staart (incl. staartwortel) 0, buitenomtrek dij 0.
Opgeheven been (x28–44, rij 0–30): alleen de toegestane pixels plus één randpixel:
- (29,29) van leeg → D;
- (30,30) van D → L;
- (29,30) van D → L. Dit is het laatste stuk van de oude rugrand op rij 30 (in v7 x28–30 D), dat binnen de beenrechthoek valt. Zonder deze pixel blijft er een dubbele rand in de hoek staan. Ik meld hem apart.

Vak hand/gloed: 1 px, (21,47). Dat is de armpixel uit 1g (V→L), geen gloed.

## Per punt (diff met 1g)
1. **Rug–dij-hoek (3 px, 1 omtrek):** de rugrand loopt nu in segmenten 2–3–3–2 (rij 32, 31, 30 x26–28, rij 29 x29–30) en gaat dan over in de voorrand van het been. De holle hoek is een afgeronde overgang geworden. Onder de nieuwe rand ligt lichtband L ((29,30) en (30,30)).
2. **Romp bol (5 px):** de terminator ligt 1–2 px verder naar linksboven (rij 42–44). Daardoor is de buikonderkant een bredere S-band (rij 43–45) die als één vlak onder het lichte middenvlak ligt. Er zijn geen D-lijnen en geen vlekken.
3. **Knie/bovenbeen (27 px):**
   - Het bovenbeen (de lob onder het lijf) heeft een lichtkant bovenop: V op rij 46–50, x36–40. De S-kern zit rechts (x41–44), de D/K-onderrand blijft.
   - De wortel van het onderbeen is V (x45–48, rij 46–50).
   - Tussen boven- en onderbeen loopt nu een zachte boog: de S-kern van het bovenbeen naast de lichte wortel van het onderbeen. Er is geen donkere streep.
4. **Bovenkant heup (9 px):** onder de staartwortel is de heup licht (V) tot aan de rand: rij 38 x42–43, rij 39 x41–44, rij 40 x41–43, rij 41 x40. Daardoor is de donkere band van staartwortel naar onderbeen gebroken. De staartwortel zelf is 0 px veranderd. Onder de lichte heupkap volgt de S-schaduwkant (rij 41–45).

## Controle
- Open randen: 0.
- Losse pixels: geen nieuwe.
- korrel.py: 0 uitsteeksels, 27 inkepingen, 1 tand. Dat is gelijk aan v7 en 1g.
- Pixels: 1821 (1g: 1820).

## Eerlijk: zwak
- **Romp:** boller dan 1g, maar de grens licht/schaduw over de buik is een vrij regelmatige diagonale trap (rij 39–44). Op 3× leest die eerder als een schuine vlakgrens dan als een ronde terminator. Het model is ronder en heeft een duidelijkere kernschaduw. Met nog ±10 px kan die grens een boog worden (oplopende segmenten 1-1-2-3).
- **Staartwortel:** de lichte heupkap ligt direct onder de bevroren S-staartwortel. Daardoor leest de staartwortel iets meer als een los stuk dat óp de heup ligt, dan als iets dat eruit groeit.
- De onderlaag in het vel toont het been nog op de oude plek (het model is niet aangepast).

## Lessen
- Een rechthoekig masker rond een bevroren deel vangt ook naburige randpixels, zoals (29,30). Meld zo'n pixel apart in plaats van hem stil mee te nemen of een rare hoek te laten staan.
