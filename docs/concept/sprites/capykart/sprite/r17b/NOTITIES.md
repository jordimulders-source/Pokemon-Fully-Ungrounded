# Capykart r17b = r17 + tanden wit

Opdracht: tanden wit/lichtgrijs zoals in r15b in plaats van blokgeel; slot vrijmaken zonder zichtbaar verlies; verder niets veranderen.
Bestanden: `capykart.png` (+`_8x`), `vel.png` (r17b | r17 op 8×, kop-close-up 16× van beide, 1× op wit/crème/donker), `diff.txt`, `controle.txt`, `bouw.py` (bouwt op `../r17/capykart.png` en `../r17/_stap.npy`), `vel.py`, `controle.py`.

## Vrijgemaakt slot
Kleurafstand (CIE76) tussen alle paletparen van r17, kleinste eerst: bruin-midden↔bruin-schaduw dE 7,9 (158 px midden) · bruin-hoog↔bruin-licht 9,0 (164 px) · bruin-midden↔licht 10,6 · blauw licht↔donker 12,4 (maar dan verliest het blauwe blok zijn tweede vlak) · rood 13,6 · groen 14,0.
Gekozen: **bruin-midden (183,107,67) → bruin-schaduw (164,88,56)**: kleinste afstand; de 531 schaduwpixels blijven exact, 158 middenpixels worden schaduw (vooral snuit, nek en houtvlakken). Op 8× en 1× naast elkaar bekeken: snuit iets donkerder, maar nog duidelijk los van het lichte gezicht; vorm en nerf onveranderd. Bruin-hoog→licht oogde vergelijkbaar maar haalt het hooglicht van de kop weg.

## Tanden
De crème-pixels van de r15b-tanden (in r17 op geel gezet) → **wit (240,240,232)**, 10 px: (18–19,33) (21–22,33) (18–19,34) (21–22,34) (19,35) (21,35). De tandschaduw/het tussenstreepje blijft hoepel-donker (76,74,84), net als in r17 (r15b: blauwgrijs).

## Diff t.o.v. r17
168 px andere kleur = 158 (bruin-midden → schaduw) + 10 (tanden geel → wit); overig 0. Silhouet en alle indices verder identiek. Palet 16 incl. transparant: 0 transp · 1 zwart · bruin 2 lijn 3 schaduw 4 licht 5 hoog · 6–7 hoepel licht/donker · 8 geel · 9–10 rood · 11–12 blauw · 13–14 groen · 15 wit.
Controle: geen lichte kleur op de buitenrand, losse zwarte pixels alleen neusgat + mond (model); dezelfde kleine vlekjes als r17 (de midden-vlek (16,35) heet nu schaduw).
