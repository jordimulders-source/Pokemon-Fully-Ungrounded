# Eindkeuring olinguito r6 (onafhankelijke eindkeurder, 8 nov)

Sprite: `olinguito_r6.png` (64×64, 4-bit geïndexeerd). Alleen uitvoering getoetst (Gen 3 + Dragonfly Cave); ontwerp, vorm, pose, kopinkleuring en kleurkeuze zijn goedgekeurd en niet beoordeeld. De K1–K4- en L1–L3-reparaties uit `KEURING_R5.md` zijn in r6 aanwezig (diff r5→r6: 91 px; grens kop/hals is nu 32,32,32,32,32,31,31,31,30,29,29,28 over rij 29–40).

Vellen (in `eindkeuring_r6/`):
- `naast_gen3_1x_licht.png` / `_donker.png` (+ `_als3x`): r6 naast Linoone, Zigzagoon, Sentret, Aipom op 1×
- `naast_gen3_4x_licht.png` / `_donker.png`: idem op 4×
- `raster_10x.png`: hele sprite met raster (rode lijn = elke 5e kolom/rij)
- `detail_kop_20x.png`, `detail_buik_achterpoten_24x.png`, `detail_voorpoten_klauwen_24x.png`, `detail_staart_20x.png`: met coördinaten
- `voor_na_reparatie_20x.png`: r6 vóór | na mijn 7 pixels (rood omkaderd)
- `olinguito_r6_voor_eindkeuring.png`: kopie van r6 zoals ik hem kreeg

## Per punt

| Punt | Oordeel | Toelichting |
|---|---|---|
| Palet ≤ 16 incl. transparant | PASS | 16 kleuren, index 0 = (152,208,160) transparant, alle 16 in gebruik. |
| Licht linksboven consistent | PASS | Hooglicht op voorhoofd, rug, dij, staart en nabije voorpoot links/boven; schaduw rechts/onder. |
| Vormschaduw en sikkel | PASS | Kop: 8-sikkel achter (4→3→2 px, na K2). Lijf: 3-schaduw rechts varieert 2–4 px, volgt de dij. Staart: `3 5 5 4 1`-buis. |
| Selout | PASS | 9 aan de lichtkant van de kop, 3 aan de lichtkant van rug/staart, 1 aan de schaduwkant. Waar het zwarte masker de linkerrand raakt wisselt 9/1 (zo ook in de oude, goedgekeurde inkleuring). |
| Buitenlijn schoon | PASS na reparatie | Vóór: 4 vulpixels raakten transparant (open rand): (37,47) (38,47) roze voetzool verre achterpoot, (45,50) roze zool nabije achterpoot, (41,46) hiel nabije achterpoot. Gerepareerd binnen het silhouet (zie onder). Kin-trap 3-3-3-5 regelmatig, geen dubbele lijnen behalve de natuurlijke knoop (27,41)/(28,41) waar kin, verre en nabije voorpoot samenkomen. Geen ingesloten weeslijnpixels (script). |
| Clusters / ruis | PASS | Tintvlakjes < 3 px alleen in staart (1–2 px brede buis, hoort zo), oor-/kopselout, oog (glans), klauwen en neus (kleine delen) en (13,38)–(14,38) = snuithooglicht onder het masker (bewust uit K4). Geen ruis in de vlakken. |
| Geen pillow shading | PASS na reparatie | Onderste deel nabije voorpoot (rij 47–49) was nog `4 5 4 3`: donkere rand aan de lichtkant met hooglicht in het midden. Hooglicht doorgetrokken naar de lichtkant; loopt nu 2 px (rij 43–49) en taps naar 1 px (rij 50). |
| Geen banding | PASS | Rug-hooglicht volgt de bovenrand maar wordt onderbroken door het dijhooglicht; schaduwrand rechts varieert in breedte. |
| Leesbaar op 1× licht/donker | PASS | Leest naast Linoone/Zigzagoon als echte Gen 3-sprite: masker, rood oog, krul-staart, klauwen. Op donker vallen de zwarte buitenlijnen weg zoals bij alle Gen 3-sprites; silhouet blijft herkenbaar. |
| Twee voorpoten los | PASS | Verre (3, 2 px breed, hoger, links) en nabije (licht, eigen poot lager) gescheiden door één gedeelde lijn op x=28. |
| Verre achterpoot schoon | PASS na reparatie | Getaperde binnenlijn (37,41)→(35,44) scheidt buik en verre dij, 2-schaduw eronder; zool was open aan de onderkant, nu gesloten. |
| Klauwen (2 per poot) | PASS | Verre voorpoot: 2 klauwen `c d` op x=21–22 en 24–25, rij 52–54; nabije: 2 klauwen, rij 56–60, schuin naar links (2-2-1). Licht links, donker rechts, punten gesloten. |
| Oog in zwart masker | PASS | `c a a / a b a` op (22–24, 35–36), glans linksboven, leest op 1× als rood oog in het masker. |

## Gewijzigde pixels (7, alle binnen het silhouet, geen vorm-/ontwerpwijziging)

| Pixel | Was | Wordt | Waarom |
|---|---|---|---|
| (37,47) | 15 (donkerroze) | 1 (lijn) | zool verre achterpoot sluiten |
| (38,47) | 15 | 1 | idem |
| (45,50) | 15 | 1 | zool nabije achterpoot sluiten |
| (41,46) | 4 | 1 | hiel nabije achterpoot sluiten |
| (29,47) | 4 | 5 | hooglicht nabije voorpoot aan de lichtkant (geen pillow) |
| (29,48) | 4 | 5 | idem |
| (29,49) | 4 | 5 | idem |

Bestand opnieuw opgeslagen als 4-bit geïndexeerde PNG, zelfde 16-kleurenpalet, transparantie index 0. Diff met `eindkeuring_r6/olinguito_r6_voor_eindkeuring.png` = precies deze 7 pixels (script).

## Oordeel
**PASS** (na 7 px uitvoeringsreparatie). Geen open punten voor de maker.

## Ter info voor Jordi (ontwerpniveau, geen afkeur)
- De staart heeft op rij 13–16 een inham van 1 px aan de binnenkant (linkerrand x=49 i.p.v. 48). Dat komt exact uit het Gemini-silhouet (`stappen/sil.npy`), dus niet aangeraakt; op 1× is het nauwelijks zichtbaar. Wil je een strakke staart: (48,13)–(48,16) → 3 en (49,13)–(49,16) → 5.
- Naast Linoone/Zigzagoon is de olinguito als geheel donkerder en contrastarmer (grijze kop-tinten 16–25 uit elkaar, Gen 3 ±30–40). Dat is de goedgekeurde kleurkeuze; bij de shiny/paletfase eventueel nog eens naar kijken.
