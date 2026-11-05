# Lama fase 3: kleur ronde 2b (5 nov)

Gemaakt vanaf `ronde2/ronde2.txt`, alleen bombín en vlecht, met de hand in `bron/wijzigingen.txt` (`bron/bouw.py` plaatst en controleert). Kop, snuitlijn, kin en oog zijn bevroren en hebben 0 px diff.
- **Gewijzigd t.o.v. ronde 2: 38 px**, alle binnen de bombín (y4–9) en de vlecht (x24–29, y12–22). Buiten die zones 0 px, dat bewijst `bouw.py`.
- **Alpha-diff met `silhouet/ronde2.txt`: +5 / −0.** Alle 5 zijn bombín-pixels, max. 2 px buiten het silhouet:
  - x22–24 y4: bol, 1 rij boven het silhouet, tussen de oren;
  - x17–18 y9: rand, links.
  - Zie `alpha_diff.txt`.
- Open randen: 3, de bekende oorpixels van 2 px (x20 y2–3, x25 y3).

## Bombín
- **Bol 7×5** (x19–25, y4–8; was 5×4). Glans `S`/`d` linksboven, rode band `RRrrrm` op y8.
- **Rand 10 px** (x17–26, y9), die 2 px links uitsteekt, met glans `dd` op x19–20. De rechterkant zakt naar y10 (ongewijzigd uit ronde 2).
- **Oren:**
  - Het linkeroor blijft zichtbaar op y1–4 (4 rijen).
  - Van het rechteroor blijft de punt op y1–4 zichtbaar, plus de buitenkant x26–27 tot y8.
  - De bol dekt de onderkant van beide oren af.

## Vlecht
- **Plaats volgens `labels.txt` (`p`) plus de rand ernaast: x26–28**, behalve op y14–15. Daar is het silhouet maar 2 px breed (x26–27), omdat x25 de kop-crème tussen oog en vlecht moet blijven.
- **Terug van de rand naar de labels:** de verschuiving uit ronde 2 (x24–27 op y18–22) is teruggedraaid. x24–25 is daar weer kop/hals-crème `C`/`S`, zoals in 1b.
- **Knotten per 2 rijen, afwisselend:**
  - donker `kdk`/`kkk` op y12–13, y16–17 en y20–21;
  - licht `dd`/`dk` en `dSd`/`ddd` op y14–15 en y18–19.
- **Tullma `Rrm`** op y22 (x26–28), tegen de halsband.
- **Tussen oog en vlecht** blijft altijd 1 kolom kop-crème `S` (x25, y13–17).

## Eerlijke zwakke punten
1. **Op 1× leest de bombín als een zwarte hoed met rand,** groter dan in ronde 2. De koepel blijft wel smaller dan in de onderlaag: 7 px tussen de oren, en breder kan alleen door de punt van het rechteroor af te dekken.
2. **Op 1× leest de vlecht als een gestreepte donkere band** achter kop en hals, met de knotten als banden. Hij blijft op de silhouetrand liggen, dus de ronde krullen van de onderlaag (die buiten de omtrek bollen) kunnen niet.
3. **Op y14–15 is de vlecht maar 2 px breed:** het silhouet eindigt daar op x27 en x25 moet crème blijven.

## Bestanden
- `ronde2b.txt`, `lama3.png`, `normal.pal`, `alpha_diff.txt`.
- `vel_ronde2b.png`: zelfde opbouw als ronde 2, plus de kop op 8× (onderlaag | ronde 2 | ronde 2b).
- `bron/`: `wijzigingen.txt`, `bouw.py`, `vel.py`.

## Lessen
- Een vlecht op de silhouetrand leest op 1× alleen als hij donkere en lichte knotten afwisselt per 2 rijen. Zigzag per rij wordt ruis die als omlijning leest.
