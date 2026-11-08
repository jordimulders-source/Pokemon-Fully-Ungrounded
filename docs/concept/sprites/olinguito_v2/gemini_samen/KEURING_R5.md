# Keuring olinguito r5 (onafhankelijke keurder, 8 nov)

Sprite: `olinguito_r5.png`. Getoetst tegen Jordi's opdracht (SPEC r2/r4): **kopvorm = Gemini** (`gemini/ronde2_v4_pose.png`, mag gladder), **kopinkleuring = oude sprite** (`af/olinguito.png`: masker, klein rood oog met glans, patroon rond oog en neus, oor- en hoofdpatroon, géén mond), pose lijf/poten/klauwen (2 per poot)/staart = Gemini, lijf = gewone Gen 3/Dragonfly Cave-keuring.

Vellen (allemaal in `keuring_r5/`):
- `vgl_8x_oud_r5_gemini.png`: oud | r5 | Gemini, 8×
- `kop_8x_r5_gemini_overlay.png`: kop r5 | Gemini | r5-omtrek (rood) over Gemini
- `r5_omtrek_over_gemini_8x.png`: hele omtrek over Gemini (zelfde schaal als `stappen/sil.py`)
- `kop_oud_vs_r5_12x.png`: kop oud | r5
- `vgl_1x.png` / `vgl_1x_als_3x.png`: oud | r5 | Gemini op 1×
- `naast_gen3_4x.png`: r5 naast Linoone, Zigzagoon, Sentret, Aipom
- `lijf_12x_raster.png`: lijf met raster (rode lijn = elke 5e kolom/rij)
- `illustratie_reparatie_8x.png` / `_1x_als_3x.png`: r5 | r5 + álle reparaties hieronder (alleen ter illustratie van de keurder, geen opleverbestand; de maker voert ze zelf uit)

## Metingen
- Omtrek r5 vs Gemini-silhouet (`stappen/sil.npy`): 1134 vs 1101 px; 40 px alleen in r5, 7 px alleen in Gemini. In de kop is het enige verschil (32,26)–(32,28): r5 vult de inkeping tussen nabij oor en achterhoofd op.
- Achterkant kop: buitenlijn staat 15 rijen recht op x=32 (rij 22–36); daarbinnen een schaduwkolom van 4 px breed met evenwijdige randen (x=28–31, rij 32–40, index 8) en de naad kop/lijf (`1 3` op x=32–33) loopt 17 rijen recht naar beneden. In Gemini buigt de grens kop/hals van x≈32 (rij 29) via ≈31 (33), ≈30 (35–36), ≈29 (39) naar ≈28 (41).
- Kopinkleuring tegen oud: bruine kruin (index 4) oud ±45 px van het verre oor schuin naar achter; r5 ±15 px, alleen een strook x=28–31. Masker oud: 4 rijen volle breedte + uitloper ónder-vóór het oog (richting neus, 2–7 px links van het oog); r5: 3 rijen volle breedte + uitloper ónder-áchter het oog (x=19–27 rij 37, x=21–25 rij 38): gespiegeld. Wangvlek (index 6) staat in r5 onder het oog i.p.v. onder de uitloper.
- Oog: `c a a / a b a` identiek aan oud, zelfde plek in het masker (2 rijen masker erboven). Neus `fe/ff/f1` als oud. Geen mondlijn. OK.
- Grijze tinten (114/89/72/56) liggen 16–25 uit elkaar (Taillow ±30–40), maar dat is de oude inkleuring die Jordi goedkeurde; geen afkeur.
- Clusterscan: geen tintvlakjes < 3 px in de vlakken behalve glans, selout en de belly-snipper (zie L2).

## 1. KOP

**1a. Omtrek = Gemini: PASS.** De omtrek valt binnen 1 px op het verkleinde Gemini-silhouet (voorhoofd 16→13 in treden 1,2,3,6; neus de meest linkse punt; ver oor klein linksboven, nabij oor rond rechtsboven). Op 1× naast Gemini dezelfde massa.

**1b. Leest de kop als een gladde ronde schedel, niet hoekig: FAIL.** Niet door de omtrek maar door de binnenkant: de achterkant van de kop is een rechte muur (rechte buitenlijn, rechte naad, rechte 4 px-schaduwkolom), en het nabije oor loopt zonder inkeping over in die muur. Samen met de horizontale tintgrenzen leest dat als helm. Reparaties:
- **K1 (inkeping onder het oor, zoals Gemini):** (32,26), (32,27), (32,28) → transparant; (31,26), (31,27), (31,28) → index 1.
- **K2 (achterhoofd rond, naad volgt Gemini):** buitenlijn kop schuift 1 px naar links waar hij recht was. Rij 34, 35, 36: (31,y) → 1, (32,y) → 3. Rij 37: (30,37) → 1, (31,37) → 3. Rij 38 en 39: (29,y) → 1, (30,y) → 3. Rij 40: (28,40) → 1, (29,40) → 3. Plus (28,32) 8 → 6 (schaduwkolom boven afronden). Grens wordt dan x = 32,32,32,32,32,31,31,31,30,29,29,28 (rij 29–40), een boog i.p.v. een muur; de 8-schaduw wordt vanzelf een sikkel (4→3→2 px).

**1c. Oude inkleuring correct toegepast: FAIL (oog, neus, geen mond: wel goed).**
- **K3 (bruine kruin achter op de kop, als oud; SPEC: "warmbruine kruin alleen achter op de kop"):** index 6 → 4 op (22,22) (23,22) (24,22) (22,23) (23,23) (24,23) (23,24) (24,24) (24,25) (25,25) (24,26) (25,26) (26,26) (25,27) (26,27) (27,27) (26,28) (27,28) (27,29) (27,30) (27,31). Een schuine bruine band van het verre oor langs de voorrand van het nabije oor naar de bestaande strook achter; volgt de bol van de schedel (helpt ook 1b).
- **K4 (masker en wangvlek als oud):** rij 37 wordt volle maskerrij: (12,37) 9 → 1; (13..18,37) 6 → 2. Rij 38 = uitloper vóór het oog: (13,38) (14,38) 8 → 6; (15..20,38) 8 → 2; (21..24,38) 2 → 6; (25,38) 2 → 8. Wangvlek onder de uitloper: (17,39) (18,39) (19,39) 8 → 6; (23,39) (24,39) (25,39) 6 → 8; (18,40) 8 → 6; (22,40) (23,40) (24,40) 6 → 8; (18,41) 8 → 6; (22,41) (23,41) 6 → 8.
- Klein, mag: (27,34)–(27,37) 2 → 8, dan stopt het masker net als oud 2 px achter het oog.

## 2. LIJF / GEHEEL (Gen 3 + Dragonfly Cave)

**PASS op:** licht linksboven (rug-hooglicht 5 boven-links, schaduw 3 en 1 rechts/onder), selout (3 aan de lichtkant van rug en staart, 1 aan de schaduwkant), staart (`3 5 5 4 1` = Gen 3-buis met selout, geen banding), dij-hooglicht volgt Gemini, achterpoten met eigen voet, klauwen 2+2, haakjes netjes, geen losse pixels, leest op 1× naast Linoone/Zigzagoon als echte sprite. Twee voorpoten zijn nu twee (verre donker, hoger, links; nabije lichter, eigen klauwen lager).

**FAIL op drie kleine punten:**
- **L1 (nabije voorpoot = kussenbuis):** x=29–33 rij 42–50 heeft 9 rijen dezelfde strepen `4 5 4 3 3` (hooglicht 1 px in het midden, donkerder aan beide kanten = pillow/banding). Licht komt van links: (29,43) (29,44) (29,45) (29,46) 4 → 5. Hooglicht is dan boven 2 px aan de lichtkant en loopt taps naar 1 px.
- **L2 (snipper tussen nabije voorpoot en verre achterpoot):** (35,41) (36,41) (35,42) 4 → 3. Nu een lichte driehoek van 5 px tussen twee zwarte lijnen (ruis op 1×); als buikschaduw rust het.
- **L3 (verre voorpoot 1 px dun, rij 43–45):** (25,43) (25,44) (25,45) transparant → 1; (26,43) (26,44) (26,45) 1 → 3. Poot wordt 2 px, zoals rij 46–48 al is, en valt binnen het Gemini-silhouet (dat heeft (24,43)). Helpt de "twee voorpoten"-lezing op 1×.

Opgemerkt, geen afkeur: nabije voorpoot heeft 9 rijen evenwijdige randen (A6-richtlijn), maar zo staat hij ook in Gemini; links van het gezicht wisselen 9 en 1 op de rand, maar dat is waar het zwarte masker de rand raakt (oud ook zo).

## Oordeel
1a PASS · 1b FAIL (K1, K2) · 1c FAIL (K3, K4) · 2 FAIL licht (L1–L3).
Totaal ±75 px, allemaal binnen de opdrachtzones; omtrek wijzigt alleen bij K1, K2 en L3, steeds richting Gemini. Na deze reparaties verwacht ik PASS; daarna opnieuw keuren (diff 0 buiten deze pixels bewijzen).
