# Regionale Abra, kleur_r7 (eindkeurder + maker, 13 nov)

Jordi: "schaduw, kleuren en belijning" (vorm, pose en ogen goedgekeurd: "ja"). Uitgangspunt `basis_F.png`. Keuring: `KEURING.md`.
Reproduceren: `python3 maak_r7.py -v` (edits als data, met reden; controleert silhouet en ogen) → `abra_r7_A.png`, `abra_r7_B.png`; `python3 maak_vel.py` → `abra_r7_A_8x.png`, `abra_r7_B_8x.png`, `vel.png`.

## Palet (index: A | B, rol)
| idx | letter | A | B | rol |
|---|---|---|---|---|
| 0 | . | (255,0,255) | idem | transparant |
| 1 | K | (14,13,22) | idem | zwart: omlijning schaduwkant, plaatnaden |
| 2 | L | (60,54,80) | (66,64,86) | lijnkleur huid: selout lichtkant, binnenlijnen |
| 3 | 1 | (49,48,61) | idem | plaat donker |
| 4 | 2 | (71,68,87) | idem | plaat/vlekjes (6 px) |
| 5 | 3 | (89,88,103) | idem | plaat licht; ook vlekjes en plooien op de huid (was I) |
| 6 | T | (104,98,126) | (96,88,124) | lichte selout / donkerste huid |
| 7 | s | (130,126,150) | (146,140,170) | huid schaduw |
| 9 | b | (180,179,191) | (184,184,196) | huid licht |
| 10 | h | (209,206,219) | (220,220,230) | huid hooglicht |
| 8, 11 | m, I | ongebruikt | | blijven in het palet zodat de indexen gelijk blijven aan r2–r6 |
A = modeltonen (gemeten onder elke index, mediaan klopt binnen ±5). B = huidreeks van `../../kadabra_regional/af/kadabra_charlatan.png`; platen en zwart gelijk aan A.

## Gewijzigde pixels (37, identiek in A en B)
| pixel | oud → nieuw | reden |
|---|---|---|
| (24,51) | I → K | vulkleur op buitenrand; model sK/sK |
| (27,27) (27,28) | m → s | plooi naast rechteroog; model 175/123, 114/175 |
| (26,29) (27,29) (26,30) (26,31) | m → s | schaduwgrens snuit; model half b, half s (128–133) |
| (26,32) (26,33) (26,34) | m → b | snuitbanding h|b|m|s → h|b|b|s; modelmediaan 162–163 |
| (26,45) (27,45) (28,45) | m → b | bovenkant dij; mediaan 152–156 |
| (40,47) | m → b | rechterhand; mediaan 152 |
| (41,47) (40,48) | m → s | rechterhand; mediaan 141 / onderhelft zwart |
| (34,27) | I → 3 | wangvlekje (vibe), bijna-dubbele tint samengevoegd |
| (31,40) | I → 3 | buikvlekje |
| (11,49) (12,49) (13,49) | I → 3 | teenplooi |
| (22,51) (22,52) | I → 3 | vingerplooi links |
| (30,60) | I → 3 | staartvlekje |
| (29,51) | T → L | vingertop: T tussen twee K's |
| (29,52) | K → L | vingertop linkerrand is lichtkant; model licht 253/100 |
| (29,39) | L → K | gatrand arm/lijf: L tussen drie K's; model 96/95/7/49 |
| (30,42) (30,43) | T → L | gatrand: één lijnkleur |
| (30,58) | I → K | onderrand vingertop; model KK/.. (r3 MAG a) |
| (52,52) | s → 3 | ringstreepje staart, model 83 (r3 MAG c) |
| (53,52) (52,53) | b → s | staartring, donkere modelhelft (r3 MAG f) |
| (22,50) | b → 3 | top vingerplooi, model 57 (r3 MAG d) |
| (39,40) | s → b | lichte streep bovenarm, model 183 (r3 MAG g) |
| (15,54) (15,55) | K → L | linkerrand scheen = lichtkant (selout) |

## Controle
- Silhouet-diff 0 met basis_F; ogen (8 pixels) ongewijzigd (assert in `maak_r7.py`).
- 9 kleuren + transparant (was 11).
- Geen vulkleur op de buitenrand; geen geïsoleerde lijnkleur op de buitenrand; geen 2×2 zwartblokken. Losse vulclusters < 3 px zijn modelvlekjes/knokkels (bewust).
- Zwart K 21,6 % (onveranderd), L 12,3 %, K+L 33,9 %, T 3,7 %. Gen 3 ter vergelijking: abra 18,0 %, kadabra 18,7 %, mightyena 17,7 %, umbreon 12,8 % zwart.

## Open voor Jordi
1. **A of B** (huid naar de regionale Kadabra).
2. Zwart 21,6 %, iets boven Gen 3; komt uit de zwarte plaatnaden en kaak van het model. Lichter maken kan alleen door van het model af te wijken.
