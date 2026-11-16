# Strenge keuring r26 (paletronde, variant C) → r27 (16 nov, zelfde keurder)

r26 heeft dezelfde indexen als r25 (diff 0); alleen paletwaarden zijn veranderd.
Vel: `sprite_r27/vel_r27_r26_r25.png`. Daarop staan r27, r26 en r25 op 8×, 2× en 1× naast het model. Voor Forretress, Magcargo en Steelix: zie de vergelijking hieronder.

## Oordeel
- **r26: FAIL op één punt.** Contrast en groen zijn duidelijk beter, maar het donkergrijs is weg. Zie 2.
- **r27: PASS.** De reparatie bestaat alleen uit paletwaarden (0 px): `sprite_r26/streng_fix27.py`.

## Hoofdvraag (1× en 2×)
- **r26 tegenover r25: beter in contrast.** De kop heeft meer volume, met een lichte plaat linksboven en een donkere sikkel rechts. De grijns en de wielen springen eruit, en de wiel-wolkgrens leest.
- **r26 is wel slechter in materiaal.** De grijzen 10, 11 en 12 zijn beige en bruin geworden (verzadiging 0,14–0,25, hue 19–33°). Roestdonker 9 is paarsrood geworden (hue 355°). Op 2× lezen de koeienvanger en de lijfplaten daardoor als zandkleur en pruim, niet als roestbruin met donkergrijs (SPEC, en het model heeft neutraal donkergrijze platen).
- **r27 vs r26/r25:** het contrast van r26 blijft, de platen lezen weer grijs en de schaduw is weer roestbruin. Naast het model is r27 het trouwst. Naast Forretress, Magcargo en Steelix is hij nog steeds drukker (dat komt uit het model), maar de waardestructuur is nu Gen 3-achtig.

## Metingen (r25 → r26 → r27)
| | r25 | r26 | r27 |
|---|---|---|---|
| Zwakke tintgrenzen (< 20 lum), alles | 10 % | 2 % | 2 % |
| Zwakke tintgrenzen, metaal | 20 % | 0 % | 0 % (Gen 3: 0–9 %) |
| Roest 14/8/9 (lum) | 142/114/77 | 146/120/56 | 146/120/58 |
| Metaal 7/10/11/12 | 182/145/99/69 | 197/170/120/78 | 197/170/121/79 |
| Groen verzadigd 2/3/6 | 194/148/102 | 200/158/98 | idem |
| Groen bleek 4/5/6 | 178/147/102 | 178/136/98 | idem |

- **Contraststappen:**
  - Metaal: 27, 50 en 42.
  - Roest: 26 en 62. De laatste stap is groot, maar 9 is ook de selout of schaduw en zit vlak bij zwart, zoals bij Magcargo. Dat is in orde.
  - Groen: 3 tegen 5 is nu 22, 2 tegen 4 ook 22.
- **Hue-shift:**
  - Roest: 23° naar 17° naar 3° (r27). De schaduw schuift naar rood, wat Gen 3-achtig is, zonder het paars van r26.
  - Grijs: licht warm (hue 30–36°, verzadiging ≤0,09 voor 10–12).
  - Groen: van licht naar donker 111° naar 150°, dus de schaduw schuift naar blauwgroen. Goed.
- **Lijnen en silhouet:** zelfde indexen als r25, dus dezelfde uitkomst als in `sprite_r25/strenge_keuring.md`. Zwart 2×2 komt 7 keer voor (allemaal in model- of Jordi-zones). Zwart is 7 % aan de lichtkant van de kop.
- **Schaduw:** het licht valt overal linksboven. Er is geen pillow shading en geen banding bijgekomen. Een paletwijziging verschuift geen grenzen.
- **Groen geestgevoel:** blijft, en is zelfs sterker, omdat de wolken meer diepte hebben en de wielen loskomen van de wolk.

## Reparatie r27 (alleen palet, helderheid per index gelijk aan r26)
| Index | r26 | r27 | Reden |
|---|---|---|---|
| 9 | (82,44,47) | (90,46,38) | paarsrood → donker roestbruin |
| 10 | (179,168,154) | (176,169,160) | beige → licht warm grijs |
| 11 | (130,118,106) | (124,120,114) | bruin → donkergrijs |
| 12 | (89,74,67) | (82,78,75) | bruin → donkerst grijs |


## MAG
- Index 6 naast 12 is 98 tegen 79 = 19 lum, op 15 grenzen. Het verschil in tint (groen tegen grijs) scheidt ze wel. Als 12 donkerder wordt, botst hij met 9.
- Index 3 naast 4 (11 grenzen) en 5 naast 11 (9 grenzen) zijn klein en verschillen in tint.
