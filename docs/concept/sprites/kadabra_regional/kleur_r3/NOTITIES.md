# Regionale Kadabra: kleur r3 (schoppen, pupillen, kaart)

Basis: `basis_r2.txt` (= `../kleur_r2/raster.txt`). Jordi over r2, letterlijk: "de schoppen ipv de klaver is mogelijk een beter idee, verder zie ik zijn pupillen niet en is de kaart net niet goed genoeg, verder erg prima". Alles buiten de drie zones is bevroren.

Bouwen: `python3 r3.py schoppen_3 oog_3 kaart_B` (schrijft alle `var_*.txt/.png`, en met de genoemde varianten `raster.txt`, `kadabra_charlatan.png`, `kadabra_charlatan_8x.png`; drukt per variant de pixeldiff buiten de zone en de silhouetwijziging af), `python3 vel.py`. Meten: `controle.py`, `lichtkant.py`, `stat.py`, `r.py`.

Zones (x0,y0–x1,y1, eindes exclusief): schoppen 23,16–29,23 · oog 21,19–33,25 · kaart 0,14–12,33.

## 1. Voorhoofd: rode schoppen (t licht linksboven, r basis, s rechts, steel en voet)
De klaver van r2 is gewist (a-strook x24–25, daarnaast b). Alle drie hebben een punt, lobben, een steel van 1 px en een voet van 3 px; zonder voet leest hij als pijl of ruit.
| variant | maat | plek | opbouw |
|---|---|---|---|
| schoppen_1 | 3×5 | x24–26, y17–21 | punt, 2 rijen lijf, steel, voet. Dichtst bij de maat van het model (klaver 4×4). |
| schoppen_2 | 5×5 | x24–28, y17–21 | punt, 3, 5 (lobben 1 rij), steel, voet. |
| schoppen_3 | 5×6 | x24–28, y16–21 | als 2 met lobben van 2 rijen. Leest op 1× het duidelijkst als schoppen. |
De schoppen op de kaarten van de charlatan-Alakazam zijn 3×4 zonder voet (punt, 2 rijen van 3, steel).

## 2. Ogen
Studie: de echte Gen 3-Kadabra heeft oogwit met een zwarte rand en **geen pupil**; de echte Alakazam heeft per oog 1 zwarte pupilpixel met wit aan weerszijden (dichtbij) of wit aan de buitenkant (ver oog, pupil aan de neuskant); de charlatan-Alakazam: lid, daaronder wit–pupil–wit–wit, wit eronder.
Ver oog, in alle varianten gelijk: lid d (22,21), wit (22,22), pupil o (23,22), wit (23,23).
| variant | dichtbij-oog | |
|---|---|---|
| oog_1 | (28–30,22) = w o w onder de bestaande wenkbrauw | 1 rij, pupil 1 px, oogwit 2 px |
| oog_2 | rij 20 (30–32) d, rij 21 (28–29) d + (30–31) w, rij 22 (27) d, w o w, (31) d | het oog van de echte Alakazam pixel voor pixel: 2 rijen, schuin, wenkbrauw 1 rij hoger |
| oog_3 | rij 22 w o w, rij 23 (28) d, (29–30) w, (31) c | 2 rijen, oogwit 4 px, pupil 1 px met wit links, rechts en eronder |
Een pupil van 2 px hoog (geprobeerd) gaf een rond, open oog en past niet bij de sluwe blik; niet opgenomen.

## 3. Kaart
| variant | kaart | schoppen | silhouet |
|---|---|---|---|
| kaart_A | 6×8 (x1–6, y19–26), maat van het model; rechte rand, gelijke hoeken | 3×4, tegen de vingertop met nagel (6,22) zoals in het model | +8 px: (2,19), (5,19), (1,20), (6,20), (6,21), (7,22), (7,23), (8,24) |
| kaart_B | 7×10 (x0–6, y17–26), rechtop | 3×5 met voet, 1 px wit rondom | +30 px (kaart 2 rijen hoger, 1 kolom naar links en 1 naar rechts; lijst uit `r3.py`) |
| kaart_C | 9×12 (x0–8, y15–26), rechtop | 5×6 met ronde lobben | +63 px |
Geen pixels eraf. De figuur begint bij B en C op x0 (box 63×54). Hand: 3 vingers, ongewijzigd vanaf rij 25 (alleen de kaarthoek erboven). Nagel: A (6,22); B en C wit pixel (6,24), aan drie kanten zwart omsloten, vinger eronder. De a-rij onder in de kaart (rij 25) is de lichtgrijze strook uit het model.

## Beste combinatie: schoppen_3 + oog_3 + kaart_B (`raster.txt`)
- schoppen_3: de enige die op 1× lobben toont; oog_3: pupil op 1× op licht en donker te zien; kaart_B: leest als speelkaart met symbool en blijft in verhouding tot het model en tot de kaarten van de Alakazam (7 px breed, symbool 3 px).
- Pixeldiff tegen r2: 73 px, **buiten de zones 0** (`r3.py`), silhouet +30 px (alleen kaart), niets eraf.
- `controle.py`: 11 kleuren + transparant, open randen 0, losse o 0. Clusters < 3 px: (25,16)+(24,17) a (rest van de lichte strook boven de schoppen), (20,25) n en (5–6,28) b (beide al in r2). Lichtkant 17 % zwart (r2 12 %; komt door de kaartrand).

## Zwakke punten
- **Kaart B is groter dan het model** (7×10 tegen ±5×7) en rechtop in plaats van licht gekanteld; de schoppen 3×5 leest op 1× als donker symbool, de vorm pas op 2–3×. Alleen C toont op 1× een schoppen, maar die kaart is bijna zo hoog als de kop.
- **Kaart A** leest op 1× nog steeds als wit rondje met zwarte vlek: op modelmaat is er geen ruimte voor wit rond het symbool.
- **Nagel** leest in geen variant op 1× als nagel (wit puntje naast de kaart).
- De hand raakt de kaart bij B en C alleen aan de hoek rechtsonder; de kaart steekt er los boven uit.
- **Voet van schoppen_3** (25–27,21) ligt 1 px van het ooglid (29,21); op 1× vormen ze bijna één donkere streep.
- **Oog_3** is groter dan het oog van het model (2 rijen in plaats van 1) en minder dichtgeknepen; oog_2 is sluwer maar tilt de wenkbrauw 1 px op.
- De schoppen is 5×6 tegen 4×4 voor de klaver in het model.
- Nog niet gekeurd door een onafhankelijke keurder.
