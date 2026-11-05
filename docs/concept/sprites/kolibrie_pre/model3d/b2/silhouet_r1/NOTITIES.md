# Kolibrie pre-evo – silhouet r1 (hoek B2)

Bron: `../silhouet_direct.txt` (render B2 direct verkleind, 704 px). Reparaties met de hand in vier zones, letterlijk als pixels in `maak.py`; `controle.py` zoekt losse pixels, uitsteeksels en spleten; `vel.py` maakt het vel.

**Resultaat: 687 px** (direct 704). Eén deel, geen gaten.

## Diff per zone (t.o.v. silhouet_direct.txt)
| zone | rechthoek (x0,y0)–(x1,y1) | erbij | eraf |
|---|---|---|---|
| snavel | (13,12)–(21,23) | 0 | 12 |
| kin/keel | (16,24)–(22,30) | 0 | 5 |
| pootjes | (22,41)–(37,46) | 4 | 5 |
| staartpunt | (38,41)–(46,46) | 1 | 0 |
| **buiten de zones** | | **0** | **0** |

Kop, rug, borst en vleugelrand zijn dus pixel voor pixel de render (ook geen ±1 px gladmaken nodig gehad).

## Wat ik deed
1. **Snavel:** de klont (linkerrand 14-14-15-16-17-17-17-16-15-15) opnieuw als het r7b-bekje: dunne bovensnavel schuin omhoog met de punt op (14,14) waar de render hem zet, inkeping (17,14) tussen snavel en voorhoofd zoals in r10, open V met het diepste punt op (19-20,18) = de mondhoek van het model, ondersnavel-wig met een holle bovenrand (19-18-16-15, zoals r10: 14-13-11-10) en de punt 2 px hoog op (15,22-23). Verkort: 6 px van punt tot mondhoek (r10: 7–8 px). V-opening 6 px diep.
2. **Kin/keel:** inham van 2–3 px op y26–29 (linkerrand 20-21-21-20), 2 rijen hoog zodat het geen kras van 1 px is; kop en borst zijn nu twee bollen.
3. **Pootjes:** nabije poot = profiel r2-vorm (stam 3 px, teenrij 5 px naar links) op x24–28, y42–44 (plek uit de render); verre poot als klein klompje (x31–34, y42–44, onderkant rond) zoals in de render, tenen van ons af. Twee kolommen lucht tussen de poten (x29–30), buik erboven leeg. Spleet van 1 px tussen buik en staart (41,36) verbreed tot een inkeping van 2 px (x35–36). Spleet van 1 px tussen de poten (29,42) is weg.
4. **Staartpunt:** losse pixel (43,45) weg; taps 7-6-5-2 px (y42–45), punt x42–43.

## Checklist §0 / norm
1. 3/4 links-voor: ok (lijf 32°, kop 44° uit het model).
2. Ledematen geteld en verbonden: twee pootjes, staart, snavel; één deel: ok.
3. Geen rechte lijnen waar rond: omtrek van de render; rechterrand rug/vleugel loopt in treden van 4–6 px (steile helling), zo in de render.
4. Ogen: n.v.t. (silhouet).
5. Leest op 1×: vogeltje met open bekje, kop en borst gescheiden.
6. Formaat: 687 px; Taillow 838, Starly 767, profiel r2 732. Lijf niet dikker dan de render (alleen pixels eraf).
7. Pose: zit, gewicht naar voren, poten verschillend.

## Zelf nog zwak / eerlijk
- **687 px, 3 onder de bandbreedte 690–740**: alle verlies komt uit de snavel (−12) en de kin (−5); bewust niet ergens anders bijgeplakt omdat het lijf niet dikker mag. Mag het aantal omhoog, dan het liefst met een iets vollere ondersnavel-wig (+2), niet in het lijf.
- **Ondersnavel en kin** lopen in het silhouet in elkaar over met alleen een trede van 3 px (y23→y24); dat de wig een eigen onderdeel is, moet straks de kleur (oranje/geel tegen lila) doen. In het silhouet leest de snavel als één open "<".
- **Bovensnavelpunt** is 1 px hoog op de uiterste kolom (14,14) en de inkeping (17,14) is 1 px; beide zo in de render én in de goedgekeurde r10, dus bewust gehouden.
- **Verre poot** heeft geen teentjes (klompje); dat is de render, maar naast de nabije poot met tenen kan het als "stomp" lezen.
- Op 1× is het bekje klein (een "<" van ±6×9 px); het leest, maar minder uitgesproken dan in het profiel r2, door de verkorting.

## Lessen
- De directe verkleining van een open snavel klontert altijd dicht (de V is 1–3 px); plan de snavel vanaf het begin als handzone, met de mondhoek van het model als ankerpunt.
- `controle.py`: numpy-bools optellen geeft `True` in plaats van een getal; eerst naar int casten.
