# Hoatzin fase 2, r5 (19 nov), maker

Alleen benoemde pixels op r4 (`r4.png`), script `r5.py`, log `r5.log`. **Pixeldiff t.o.v. r4: 25 px, silhouet 0.** Buikvarianten opnieuw in `buik/`. `vel.png` = r5 | r4 | model | Pidgeot.

| Punt | px | wat |
|---|---|---|
| 1 donkere streep x22–23 y28–36 | 5 | (23,29), (22,31), (22,33), (23,34), (22,35) → toon 2; criterium: mediaan van het model < 30 (zoals px.py). (23,33) meet 59 → blijft. |
| 2 oog | 5 | pupil (12,21)+(12,22) zwart; iris rood waar het model roze is (R−B per cel): (11,22), (13,21), (13,22) (stonden al rood); (11,21) glans → blauw 9, (12,23) → blauw 9. x14 meet sterk blauw (R−B −92), dus geen iris op x14. |
| 3 selout linkerrand buik | 4 | (16,42–44), (17,46) → 3; rand x16–17 y38–46 nu één toon. |
| 4 bovenrand buik | 2 | (18,37), (22,37) → toon 4 (model 100/108 lager dan midden 111–112). |
| 5 tenen | 4 | (22,55), (18,56), (20,57) → 14 (model 50–73), (17,58) → 1 (model 41). |
| 5 staartlijn | 6 | dubbele pixels in de binnenlijn → rechter houden: (42,49), (43,50), (44,51), (45,53), (46,54), (47,55) → 2. |
| 5 gezicht achterrand | 1 | (15,20) → 8 (model 63); de rest van x15–16 y19–22 was al zwarte rand. |

Variant `hoatzin_oogring.png` (3 px anders): iris als gesloten ring (6 rood rond de pupil) — leest als ruit/plus; de gemeten versie is de hoofdversie.
