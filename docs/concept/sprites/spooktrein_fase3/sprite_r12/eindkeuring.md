# Eindkeuring spooktrein fase 3, r12 (16 nov, verse keurder)

**Oordeel: FAIL (klein).** Hoofdbeeld is goed; de trein heeft nog 21 px ruis (zwart in vlakken, dubbele lijn, dambord, buil in de rand) die het groen niet heeft. Alle MOET-punten zijn niet-groen en staan in `eind_moet.py` → `eind_voorstel.png` (+ `_8x`); groen-diff 0 met assert. Na toepassen: korte herkeuring (regel "na wijziging opnieuw keuren"), geen makerronde nodig.

Vel: `eindkeuring_vel.png` (8×: r12 | r12 + MOET met rode kaders | model; onder: voorstel en model op 1×/2× naast Gengar, Haunter, Magcargo, Claydol, Forretress).

## 1. Hoofdvraag
- **Lijkt op het model: ja.** Pompoenkop-loc met grijns, schoorsteen met geest, lijfplaten met groene kieren, koeienvanger met drie platen, twee geestwielen, wolkensliert. Verhoudingen en compositie kloppen; op 2× herken je het model direct.
- **Mooie Gen 3-sprite: ja, op de ruis na.** Op 1× leest de kop met grijns duidelijk; het geheel is drukker dan Gengar/Claydol, maar dat komt uit het model (wolken, kieren). Vult het 64×64-vak helemaal: groter dan de vijf referenties, ter info voor Jordi.
- **Trein net zo netjes als het groen? Nog niet helemaal.** Kop (platen, lichte plaat linksboven, roest) en koeienvanger zijn rustig en lezen als grote vormen; de lijfplaten en de naad kop/lijf rechtsonder hebben nog losse zwarte pixels en een dubbele zwarte onderlijn. Met de MOET-lijst is dat weg.

## 2. Dragonfly Cave / SPRITE_KERN (gemeten)
| Punt | Meting | Oordeel |
|---|---|---|
| Kleuren | 13 + transparant (≤16) | ok |
| Tinten per groep | roest 7/8/9, grijs 10/11/12, zwart 1; groen 6 tinten (bevroren) | ok |
| Contrast | 7→8 45, 8→9 37, 10→11 46, 11→12 30, 12→1 44 (Taillow ±30–40) | ok |
| Vlekjes < 3 px (niet-groen) | 53 clusters; schoorsteen (bevroren natief) en lijnovergangen buiten beschouwing, echte ruis: (31,31), (35,31), (22,43), (8,47), (33,24) | MOET/MAG |
| Losse zwart in vlak | (31,31) in 11, (35,31) in 12, (22,43) in roest, rij 42 x32–37 dubbele lijn | MOET |
| Buitenlijn ijzer | 56 randpixels: 41 % zwart (r11 55 %); lichtkant 18× roest-selout 9, 6× grijs 12, 4× zwart | ok (Gen 3 45–68 %, lichte soort ±40) |
| Groen op buitenrand | geen lichte groentint (2/3/4/5/13) op de rand | ok |
| Bijna-zwart totaal | 9,2 % (Gengar 7, Haunter 12, Magcargo 14) | ok |
| Licht linksboven | kop: lichte platen linksboven, roest/zwart rechtsonder; koeienvanger lichte schuine bovenranden | ok |
| Banding / pillow | geen; kop heeft sikkelschaduw rechts | ok |
| Dambord | echte: (24,45)/(24,46), (7,47) (rest = diagonale lijnen of bevroren schoorsteen) | MOET |
| Recht waar model rond is | kop linksboven 3-1-1-1-2-2-4: vloeiend genoeg; koeienvanger linkerrand x1 y48–55 met buil (0,52–53) = spijkertje | MOET (buil) |

## 3. MOET (21 px, belangrijkste eerst; x,y oud→nieuw)
**A. Naad kop/lijf rechtsonder (zwart in vlak, dambord)**
1. (22,43) 1→9
2. (24,45) 1→12
3. (24,47) 1→12
4. (25,47) 12→1 (buitenrand tegen het groen wordt zwart; diagonale lijn (26,44)–(23,48) loopt nu door)

**B. Onderrand onderste lijfplaat: dubbele zwarte lijn y42/y43 → schaduwrij**
5. (32,42) 1→12 · 6. (33,42) 1→12 · 7. (34,42) 11→12 · 8. (35,42) 1→12 · 9. (36,42) 12→9 · 10. (37,42) 1→9

**C. Losse zwarte pixels in de grijze lijfplaat** (model heeft daar een donker puntje: donkerste grijs, geen gat)
11. (31,31) 1→12 · 12. (35,31) 1→12

**D. Koeienvanger**
13–16. Buil linkerrand weg: (0,52) 9→0, (0,53) 9→0, (1,52) 8→9, (1,53) 8→9
17–19. Roest blijft als streep in de lichte wig: (2,51) 7→8, (2,52) 7→8, (2,53) 7→8
20. (8,47) 11→9 (lichte schuine bovenrand loopt 2-2-1 zonder grijs stipje)
21. (15,53) 12→1 (naad van de middentand doorlopend)

## 4. MAG
- Bovenste lijfplaat (x27–41, y24–33): model heeft een lichte (beige) rand linksboven op de plaat; r12 is daar roest 9/donkergrijs. Een rij 7/10 langs de bovenrand zou dichter bij het model en meer volume geven.
- (33,24) grijze 1-px uitstulping in de wolk; (41,28) 9→1 (hoek van de plaat tegen het groen).
- (2,30),(2,31) roestzakje van 2 px tussen rand en zwarte plaatlijn → 9.
- (20,44) 8→9 (los roestpixel in de kin).
- Lichte wig x2–3, y44–58: 15 rijen even breed (zuil); model loopt taps toe naar de punt.

## Ter info (groen, bevroren, geen punten)
Geen harde technische fouten in het groen gevonden (geen lichte tint op de buitenrand, palet binnen 16).
