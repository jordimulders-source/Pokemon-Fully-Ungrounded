# Lama fase 3: kleur ronde 4b (5 nov)

Alleen het oog (x23–27, y14–18), vanaf `ronde4/ronde4.txt`; de rest is 0 px diff met ronde 4. Reden (Claude): de modelring van 3×4 px was op 1× en zelfs op 8× vrijwel onzichtbaar.

## Wat ik deed
**Oog in de stijl van fase 2**, op de plek en ter grootte van de oogcellen van de bron, droog en half gesloten:

| rij | pixels | wat |
|---|---|---|
| y14 | x24–25 `SS` | lidmassa |
| y15 | x23–25 `kkk` | zwaar vlak bovenlid, zwarte lijn |
| y16 | x23–25 `dkk` | iris boven donker |
| y17 | x23–25 `Hkd` | lichtje laag vóór, onderkant van de iris bruin |
| y18 | x25 `S` | zacht onderlid |

- **Scheiding met de vlecht:** x26 op y15–17 is kopkleur `S`. Daar zit 1 px tussen oog en vlecht (x27, bruin).

## Gewijzigde pixels: 10 (`ronde4.txt` → `ronde4b.txt`)
- Allemaal binnen x23–27, y14–18.
- Per pixel: x24y14 C→S, x25y14 C→S, x23y15 C→k, x25y15 S→k, x23y16 S→d, x25y16 S→k, x26y16 k→S, x23y17 C→H, x25y17 k→d, x25y18 k→S.
- **Buiten de oogcellen (E/D) van de bron, alle ±1 px:**
  - x24 y14, x25 y14 (lidmassa erboven);
  - x23 y15–17 (voorkant van lid, iris en lichtje).

## Eerlijk
- Het oog is een blok van 3×3 met een lidmassa erboven. Een langer lid dan de iris (zoals in fase 2) kan pas met x22, en dat ligt 2 px buiten de oogcellen. Daarom niet gedaan.
- Op 1× leest het nu als oog, met een droge, halfgesloten blik.

## Bestanden
- `ronde4b.txt`, `lama3.png`, `normal.pal`.
- `vel_ronde4b.png`: zelfde opbouw; kop 8× met render | ronde 4 | ronde 4b.
- `bron/vel.py`.
