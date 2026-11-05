# Lama fase 3: kleur ronde 5B (5 nov)

**Jordi over 4b (letterlijk):**
- "nu is er geen nek meer"
- "ik ben nog niet tevreden met het oog, het is nu gewoon bijna een zwarte vlek, niet typisch lui oid, kijk nogmaals naar slakoth, slaking etc"
- "probeer beide manieren maar"

**Aanvulling (letterlijk):** "ja een zichtbaar ooglid lijkt me goed, deze moet vooral nonchalant en unimpressed kijken".

## Wat
- **Lijf = 2b, exact.** Alles buiten de kopzone is 0 px diff, en ook de labels `x` in de kopzone zijn 2b.
- **Kop overgetrokken van `kopbron/*_B`** (kop 1,1× om de oorpunten, ±3 rijen hals), met de hand in `bron/kop.txt`. Werkwijze als ronde 4: onderdeel uit `kop_labels_B`, lijnen uit `kop_lijnen_B`, licht en schaduw in het palet van 2b.
- Controles (`diff_bron.txt`):
  - onderdeel wijkt af in 2 cellen, beide het oogwit (x24–25 y15: `E` → `H`, bewust);
  - 0 open randen, 15 kleuren;
  - buiten `silhouet/ronde2.txt` +18, leeg −11 (de kopvorm van de bron).

## Oog (Slakoth/Slaking, unimpressed)
| rij | pixels | wat |
|---|---|---|
| y13 | x22 `d`, x23–25 `SSS` | bovenlid als eigen vlak in kop-schaduw |
| y14 | x22–25 `kkkk` | zwarte lidlijn, vlak, 1 px langer dan het oog naar voren |
| y15 | `d k H H` (x22–25) | oogwit met een kleine pupil laag vooraan |
| y16 | x23 `d`, x24–25 `kk` | onderrand |
| y17 | x23–25 `SSS` | zachte kring onder het oog |

- Het bovenlid hangt over de bovenste helft van het oog: verveelde, "al gezien"-blik.
- **Scheiding met de vlecht:** x26 op y13–15 is kopkleur `S` (in de bron: vlecht/lijn).

## Afwijkingen van de bron (met reden)
- **Oog:** x22–25 y13–16 en x26 y13–15, zoals hierboven. Het lid steekt 1 px voorbij de oogcellen, het lidvlak 2 px.
- **Open randen in het oor van 2 px:** x26 y4–6 `d`, x27 y6 `k`.
- **Voorhoofdrand:** x16 y15 `d` (open rand).
- **Hoedband `RRrrm`** op y9 x20–24 (bron: band x20, hoed x21–24 met lijn). Zo leest de band.

## Eerlijk
- Het oog is klein (oogwit 2 px). Op 1× leest het als een halfgesloten, verveeld oog met lid, niet als zwarte vlek.
- Hals ±3 rijen (y20–23), zoals de bron.

## Bestanden
- `ronde5B.txt`, `lama3.png`, `normal.pal`, `diff_bron.txt`.
- `bron/kop.txt`, `bron/bouw.py`.
- Vel: `../vel_ronde5.png` (samen met A).
