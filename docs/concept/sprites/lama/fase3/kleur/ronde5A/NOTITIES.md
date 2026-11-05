# Lama fase 3: kleur ronde 5A (5 nov)

Jordi's woorden en de oog-aanvulling staan in `../ronde5B/NOTITIES.md`.

## Wat
- **Hele figuur op `kopbron/silhouet_A.txt`** (1402 px). Kop 1,25× om de halsaansluiting, hals zoals het model, lijf ±7% kleiner.
- **Alpha-diff met silhouet_A: +0 / −0** (`controle.txt`). 0 open randen, 15 kleuren, palet van 2b.

### Lijf
- `bron/overzet.py` zet de met de hand gekleurde pixels van 2b op silhouet A met een vaste, met de hand gekozen rij- en kolomtoewijzing. Er wordt geen tint of shading berekend.
  - 3 rijen van 2b vallen weg in egale vlakken: y34 (pak), y44 (groene ruche), y48 (poten boven de windsels).
  - 2 kolommen vallen weg: x20 (verre voorpoot) en x44 (achterpoot/rug).
  - De rest schuift 3 rijen omlaag en 1 kolom naar rechts.
  - Halsband, pompons, riem, ruches en beide windsels houden al hun banden.
- Daarna **58 pixels met de hand** in `bron/lijf_reparaties.txt`, per groep met reden:
  - de omtrek op silhouet A (±1 px), met nieuwe randpixels in de omlijningskleur;
  - de staartpluim (y24–25);
  - de nabije achterpoot 1 px naar binnen;
  - de hoef van de nabije voorpoot 1 px naar rechts;
  - de hoeven van de verre achterpoot.
- Geen korrels: de omtrek is die van silhouet A.

### Kop
- Overgetrokken van `kopbron/*_A` in `bron/kop.txt`. Onderdeel-diff tegen `kop_labels_A`: **0 cellen**.
- **Lijnafwijkingen: 21**, alle in `controle.txt`:
  - het oog (zie hieronder);
  - de scheiding oog/vlecht (x26 y14–17 `S`);
  - open randen in de oren van 2 px (x20–21 y3–4, x28 y6, x28 y9) en de pony (x20 y12);
  - de mondlijn x19–20 y22, 1 px verschoven naar de bemonsterde kleur.

## Oog (zelfde recept als B)
| rij | pixels | wat |
|---|---|---|
| y14 | x22 `d`, x23–25 `SSS` | bovenlidvlak |
| y15 | x22–25 `kkkk` | vlakke zwarte lidlijn |
| y16 | `d k H H` (x22–25) | oogwit, pupil klein, laag vooraan |
| y17 | x23 `d`, x24–25 `kk` | onderrand |
| y18 | x23–25 `SSS` | kring onder het oog |

- Scheiding met de vlecht: x26 is kopkleur.

## Eerlijk
1. Het lijf is een overzetting van 2b met weggelaten rijen en kolommen. De verre voorpoot is 1 px smaller (3 px) en de rok 1 rij lager; op 4× zag ik geen breuken in de banden. Een keurder moet het lijf naast 2b nalopen.
2. Het oog is klein (oogwit 2 px), net als bij B.

## Bestanden
- `ronde5A.txt`, `lama3.png`, `normal.pal`, `controle.txt`.
- `bron/overzet.py`, `bron/lijf_overgezet.txt`, `bron/lijf_reparaties.txt`, `bron/kop.txt`, `bron/bouw.py`.
- `bron/vel.py` maakt `../vel_ronde5.png`.
