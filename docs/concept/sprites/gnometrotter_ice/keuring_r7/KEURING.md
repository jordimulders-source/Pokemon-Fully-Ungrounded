# Keuring Gnometrotter Ice r7 (verse keurder, 23 nov)

Te keuren: `../sprite_r7/gnometrotter_ice.png`. Model: `../r3/gemini_r3_lijf.png`. Maatstaf: `gnometrotter_rock/af/`, blok "Ice en Grass" in `gnometrotter_rock/PLAN.md`.
Beeld: `vel.png` (1× | r7 8× | Rock af 8× | model | r7 10× met de reparatiezones). Eerst blind beoordeeld, daarna pas `keuring_r5` en de makerrapporten gelezen.
Coördinaten: (x,y) in de 64×64-sprite. Indexen: 1 zwart, 6/7/8/15 roze (donker→licht), 9/10/11 blauw (donker→licht).

## Oordeel: **BIJNA**

### Jordi's punten
| punt | stand | meting |
|---|---|---|
| gesp weg | **ok** | riem y 38–42 alleen ijstinten 12/13/14 + 2-lijn, geen gespvorm |
| linkerhand gelijk aan Rock af | **ok** | x 2–17, y 29–35: 0 px verschil met Rock af (verschil alleen in de stok, buiten scope) |
| rechterschouder rond zoals Rock af | **bijna** | rand rechts per rij 27–32: r7 x 53,54,54,**54**,55,55; Rock af 53,54,54,**55**,55,55. Op rij 30 is r7 1 px ingedeukt (zwart op 54, Rock heeft daar 7 en zwart op 55). Binnenin ok: hooglicht 15 linksboven (51–52,28),(51,29), 7 als schaduw rechtsonder. |
| lijf meer ijsvormen, alleen roze/blauw | **romp ja, benen half** | zie hieronder |
| rest behouden | **ok** | diff t.o.v. r3: alleen romp, schouder, linkerhand, gesp en benen; rechterhand, muts, baard, zolen 0 px |

### Volume en ijs
- **Romp (6/7/8/15): leest als gefacetteerd roze ijs/kristal**, op 1× en 8×. Groot licht facet 15 links-midden (x 34–41, y 27–31) zoals het model, sikkel 6/7 rechtsonder die meebuigt met de buik ((48,29)→(41,34)), licht linksboven, ≥3 tinten, geen effen vlak. Weinig naden en vrij netjes. Kleine kanttekening: rij 26 (x 35–38 en 45–48, 7) is een vrijwel horizontale band; niet blokkerend.
- **Benen (9/10/11): volume nu goed** (11 linksboven, 10 midden, 9 als sikkel rechts/onder; de horizontale banden van r5 zijn weg, geen vlakjes < 3 px in de vlakken). **Maar de twee barsten zijn kaarsrechte kolommen**: linkerdij 11 op x 23, y 43–49 (met 9-kolom x 24), rechterdij 11 op x 45, y 41–48 (8 rijen recht, met 9 op x 46). Op een bolle dij in driekwart lezen die als broeknaad/vouw, niet als ijsbarst; in het model buigen beide barsten mee met de bol. Dat is precies Jordi's "onthoud het perspectief". Op 1× lezen de benen nog als blauwe broek, op 8× half als ijs.
- **Breuk in de linkerbarst**: (23,44) is 9 midden in de 11-lijn, waardoor (23,43) een losse 11-pixel is.

### Techniek
- Belijning: zwart doorlopend rechts/onder, geen open randen in de scope. Zwart (48,28) in de naad romp/schouder zit ook in Rock af: mag blijven.
- Losse pixels (8-buren) in de scope: alleen lijnstukjes in 6 langs baard/muts ((32,25),(36,36)) en 9 langs randen; geen ruis die opvalt, behalve (23,43) hierboven.

## Reparaties (alleen deze; diff 0 erbuiten)
1. **Schouder rij 30**: (54,30) 1 → 7, (55,30) 0 → 1. Dan is de rand gelijk aan Rock af.
2. **Linkerbarst heel maken**: (23,44) 9 → 11.
3. **Barsten in perspectief** (zone, niet tekenen maar de kromming van de modelbarst overnemen): linkerdij x 22–25, y 43–50 en rechterdij x 43–48, y 41–50. De 11-lijn met zijn 9-schaduwkant per 2–3 rijen 1 px laten verspringen langs de modelbarst, zodat er geen rechte kolom van > 3 px meer staat. Eén lijn per dij blijft (Jordi akkoord met weinig lijnen). Silhouet, zolen en de rest van de benen ongewijzigd.

Na 1–3 is de sprite in mijn ogen PASS binnen de scope.

## Ter info, buiten scope ("de rest behouden")
- Muts en baard zijn grote effen vlakken (baard als rechte verticale strepen), rechterhand vrijwel effen 8. Niet aanpakken zonder Jordi.
- Ijsstrook links van de linkerdij (x 18–21, y 42–47) leest als los stuk baard/ijs naast het been; komt uit r3.
