# Keuring Gnometrotter Ice r5 (verse keurder, 23 nov)

Te keuren: `../sprite_r5/gnometrotter_ice.png` (64×64). Model: `../r3/gemini_r3_lijf.png`. Maatstaf: `gnometrotter_rock/af/`, Jordi's blok "Ice en Grass" in `gnometrotter_rock/PLAN.md`.
Beeld: `vel.png` (model op schaal | sprite, 8×). Let op: het model staat op de Rock-geometrie en valt daardoor niet pixelexact op de sprite; trouw is per onderdeel beoordeeld.

## Oordeel: **BIJNA**

Eerst blind op het oog (1× en 8×), daarna `RAPPORT.md` gelezen.

### Jordi's punten voor deze ronde
| punt | stand | meting |
|---|---|---|
| gesp weg | **ok** | riem x 18–49, y 37–42 is alleen c/d/e met 2-lijnen; geen gespvorm |
| rechterschouder rond zoals Rock | **ok** | roze ovaal x 50–54, y 26–32: breedte per rij gelijk aan Rock af (rij 29–31: x 50/51–53/54 in beide); hooglicht F op (51,28),(52,28),(51,29), 6 links, 7 onder, zwart rechts |
| linkerhand zoals Rock | **ok** | x 0–17, y 27–37 kleurgelijk aan Rock af, behalve de ijspegelkop van de stok (y 36–37) en de aansluiting (16–17, 27–28): bedoeld |
| lijf meer ijsvormen, alleen roze/blauw | **half** | romp: ja (facetnaden in 6 met lichte rand F/8; alleen paletindexen 6/7/8/F + de bestaande ijsrand). **Benen: niet gedaan** (maker zegt het zelf). Jordi's "roze/blauwe lichaam" omvat de benen. |
| rest behouden | ok | volgens `r5_log.txt` 0 px buiten romp/schouder |

### Per kleurzone (gemeten: grootste samenhangende vlak van één index)
- **Romp roze (6/7/8/F): geen effen vlak meer**, leest op 4× en 1× als gefacetteerd roze ijs; duidelijk beter dan r4. Twee restpunten:
  - Het 7-vlak rechtsonder is één effen blok van **43 px** (x 37–48, y 28–35) dat zonder schaduwsikkel direct tegen de 2-lijn/ijsrand loopt. Gen 3 zou hier een sikkel in de donkerste tint leggen.
  - Het F-vlak (33 px, x 34–41, y 25–32) is groot maar is het lichte facet uit het model en ligt links-midden: acceptabel.
- **Benen blauw (9/A/B): effen + banding.** B 98 px, A 82 px, 9 54 px (9 bijna alleen als lijn). Linkerdij: rij 43–46 B, rij 47–49 A, over de hele breedte: horizontale banden parallel aan de riem, geen links-rechts-volume. Rechterdij: rij 42–46 vrijwel effen B (x 39–44), alleen de rechterkolommen A. Linkerscheen x 16–27, y 50–53: zelfde horizontale B→A-band. Facetten uit het model (lichte barsten + donkere onderkant) ontbreken; de enkele 9-naden lezen als donkere krassen, niet als ijs.
- **Muts (2/3/4/5): effen**, buiten de opdracht ("rest behouden"): 5 is één vlak van 120 px (links), 4 één vlak van 163 px (rechts), 3 maar 22 px als naadlijnen; geen schaduwkant rechts/onder (4 grenst direct aan zwart). Ter info aan Claude/Jordi, niet repareren zonder Jordi.
- **Baard (c/d/e): effen**, buiten de opdracht: d-blok links, c-blok rechts (38 px samenhangend), rechte verticale strepen; was al door de vorige keuring benoemd ("radiator"). Ter info.
- **Rechterhand (6/7/8/F)**, buiten de opdracht: vrijwel effen 8 (x 53–60, y 34–39), 7 alleen in de onderste rij. Ter info.

### Techniek
- Licht linksboven: romp ok (bovenrand donker door schaduw onder baard/muts, zoals het model).
- Kleine vlakjes: in de romp alleen lijnpixels (6-naden) en hooglichten; geen losse ruisvlekjes in de gewijzigde zone.
- **Open rand / losse zwarte klont bij de neus (bestond al, maar is fout):** zwart (14,20),(15,20),(14,21),(15,21),(15,22) hangt los onder de ijspluk links van de neus, met een doorzichtig gaatje op x 16, y 20–22. Rock af heeft daar niets. Zwart staat hier aan de linkerkant (lichtkant).
- Binnenzwart (48,28) in de naad tussen romp en schouder: past bij Rock (daar ook donker), mag blijven.

## Reparaties (alleen deze; diff 0 erbuiten)
1. **Sikkel 7-vlak rechtsonder romp** → index 6: (48,29),(47,30),(46,31),(45,32),(44,33),(43,33),(42,34),(41,34). Niet de onderste rij langs de riem (y 35–37), anders ontstaat een donkere band.
2. **Neusklont** → index 0: (14,20),(14,21),(15,21),(15,22). (15,20) blijft 1 als onderrand van de ijspluk. Optioneel (17,20),(17,21) 1 → 6 (eigen donkerste tint aan de lichtkant van de neus, zoals Rock daar donkerroze heeft).
3. **Benen ijsvormen** (open opdracht van Jordi), zone: dijen x 18–49, y 42–49 en schenen/voetbollen x 16–28 en x 40–50, y 50–55. Facetvlakken overnemen uit het model (niet tekenen), en per facet volume i.p.v. horizontale banden: B linksboven op de bolling, A midden, 9 als sikkel rechts/onder langs de vorm; de modelbarsten als lichte naad (B), niet als 9-kras. Silhouet en zolen ongewijzigd.

Na 1–3: opnieuw keuren. Muts, baard en rechterhand zijn effen maar vallen onder "rest behouden"; voorleggen aan Jordi, niet zelf aanpakken.
