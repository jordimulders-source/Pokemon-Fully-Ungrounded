# Kudu r15: rechte lijnen nalopen
Jordi (27 nov), op r14 met rode streepjes (`jordi_rechte_lijnen.png`): "check alleen nog of al deze rechte lijnen nodig zijn".
Uitgangspunt: `r14/kudu_r14.png`. Script: `sprite/r15.py` (elke pixel met assert op de oude waarde; lijst in `pixels.txt`), vel: `sprite/vel15.py` (`vel.png`).
Lever: `kudu_r15.png` (P-modus, zelfde palet `normal.pal`), `kudu_r15_8x.png`, `grid.npy`.

## Werkwijze
- De rode streepjes zijn als componenten uit Jordi's plaatje gehaald en omgerekend naar spritepixels (schaal 10,22 × 10,0; gecontroleerd op de buikschaduw (rij 44) en de oortop (rij 16)).
- **Meting in het model** (`r3/model_A3.png`, cel 16 px, x0 = 91, sprite-x = (mx − 91)/16 + 6): per spriterij/-kolom de randpositie in het model (voorgrondrand, toongrens of streepmidden), gemiddeld over de 16 modelrijen.
- **Regel (impala r7):** een knik alleen waar het model ≥ 0,2 px van de spritelijn afwijkt, 1 px naar de kant van het model; niets hertekend, geen nieuwe kleuren, geen blur. Waar het model zelf recht is: laten staan.
- **Gen 3-maat voor poten** (langste rechte silhouetrand bij hoefdieren, `anim_front_gba`, y ≥ 40): Stantler 7, Girafarig 5, Tauros 6, Ponyta 6, Rapidash 10 (één dunne poot). Kudu r14: 11, 10, 9 → r15: max 8 (twee niet-gemarkeerde linkerranden van poten), de gemarkeerde nu 7.

## Per lijn
| # | lijn (Jordi) | recht nodig? (meting) | wat veranderd |
|---|---|---|---|
| 1 | rechterhoorn, rechterrand (x30, rij 6–12) | **nee.** Model: 30,6 · 30,1 · 30,1 · 30,5 · 30,8 · 31,3 · 31,4 (S-draai: smal bij rij 7–9, breder onderaan); sprite overal 31. | Rij 7–9 rand 1 px naar binnen: (30,7–9) 0→transparant, (29,7–9) 3→0; (30,6) 3→0 (rand dicht). Hoorn daar 3 px (model 3,06). 7 px. |
| 2 | horizontaal over de hoornvoeten (y≈14,5–15,3, x9–26) | **ja.** Links (x9–17) ligt geen horizontale pixelrand: de lijn kruist de verticale linkerhoorn. Rechts is het de liggende boog van de rechterhoorn (rij 12–15); model: bovenrand 12,1–12,65, onderrand witte slijprand 15,1–15,2, dus binnen 0,2 px gelijk aan de sprite. De boog is in het model zelf horizontaal. | niets |
| 3 | oortop rechts onder de hoorn (rij 16, x24–29) | **nee.** Model (oorvlak-boven): 18,1 · 17,2 · 16,9 · 16,3 · 16,4 · 17,0 (x24–29): rond, het hoogst bij x27–28. | Oortop bij x27–28 1 px omhoog: (28,15) transparant→K (+1 silhouetpx), (27,15) 0→K (anders K/zwart om en om), (27,16) en (28,16) K→R. 4 px. |
| 4 | horizontaal op ooghoogte (rij 22: onderkant linkeroor tot oog en rechteroor) | **nee** (links). Model, onderrand linkeroor: 22,1 · 23,0 · 23,3 · 24,7 (x7–10): loopt schuin af naar de wang; sprite rij 22 x8–11 vlak. Rechteroor: model 23,7 · 23,3 · 22,6 (x26–28) = de sprite-trap al. Oog K4 + wenkbrauw: niet aangeraakt (de lijn is daar de oogbovenkant zelf, geen losse vachtgrens). | (10,22) 0→r, (10,23) transparant→0 (+1 silhouetpx). 2 px. |
| 5 | onderkant snuit/mondlijn (rij 28, x11–18) | **nee.** Model: mondlijn stijgt bij x14 naar 27,6–27,9 (mondhoek), kaaklijn x15–17 op 28,8–29,0. Sprite: 8 px op één rij. | (14,27) M→D, (14,28) D→M: mondhoek 1 px omhoog. 2 px. Neus/mond-zone x8–12 niet aangeraakt. |
| 6 | keelfranje/halsstrook, rechterrand (x21, rij 28–34) | **ja.** Model: manenlijn op 21,1–21,4 over rij 27–35 (golf ≤ 0,15 px), daarna 21,8–22,2 op rij 36–37; dat is precies de sprite (x21 t/m rij 35, x22 vanaf 36). | niets |
| 7 | keelfranje, linkerrand van de halsstrook (x18, rij 29–34) | **nee.** Model: 18,2 · 18,4 · 18,6 · 18,7 · 18,7 · 19,0 (rij 28–34) schuift naar rechts; de sprite stapte pas op rij 35. | Stap 1 rij eerder: (19,34) M→K, (18,34) K→l. 2 px. |
| 8 | bovenrand rug bij de strepen (rij 31, x39–46) | **nee.** Model: 30,9 · 31,0 · 31,0 · 31,3 · 31,3 · 31,3 · 31,3 · 31,5 · 31,8 · 32,2 (x39–48): de rug loopt geleidelijk af; sprite 8 px op rij 31, dan pas een stap. | Stap bij x44: (44–46,31) D→transparant, (44,32) L→D, (45,32) L→D, (46,32) W→D (streeptop 47 begint nu op rij 33). Runs nu 5 + 5. 6 px. |
| 9 | witte flankstreep x37 (rij 34–43) | **nee.** Model (streepmidden): 36,7 · 36,8 · 37,1 · 37,3 · 37,4 · 37,4 · 37,2 · 37,0 · 36,8 · 36,6: buigt naar rechts. | Streep 1 px naar links op rij 34, 42 en 43 (W en buurtint gewisseld; (37,43) wordt M, niet D, zoals het model). Blijft 1 px. 6 px. |
| 10 | witte flankstreep x44 (rij 34–42) | **nee.** Model: 43,7 · 43,9 · 44,1 · 44,1 · 44,1 · 44,1 · 44,1 · 43,8 · 43,8: buigt naar rechts. | Streep 1 px naar links op rij 34, 41 en 42. Blijft 1 px. 6 px. |
| 11 | achterrand achterwerk (x52, rij 43–47) | **nee.** Model: 53,4 · 53,1 · 53,1 · 53,3 · 53,6 (rij 44–48): hol bij rij 45–46. | Rij 44 en 47 1 px naar buiten: (53,44) en (53,47) transparant→0, (52,44) en (52,47) 0→M. 4 px. |
| 12 | bovengrens buikschaduw (rij 44, x35–44) | **nee** (rechts). Model-helderheid: schaduw begint op x34–36 rij 41–43, x37–41 rij 44, x43 rij 43 (149), x44 rij 42: een U. Sprite x37–43 op rij 44. | (43,43) M→D. Run x37–42 (6). 1 px. |
| 13 | achterpoot rechts, rechterrand (x54, rij 50–60) | **nee.** Model: 55,06 op rij 51–56, 55,2–55,4 op rij 57–59 (koot), 54,8 op rij 60. Gen 3 (Stantler `5888f`) heeft dezelfde koot-verbreding. | Rij 57–59 1 px naar buiten: (55,y) transparant→0, (54,y) 0→M. Run 11 → 7. 6 px. |
| 14 | verre voorpoot, linkerrand (x23, rij 50–58) | **nee.** Model: 22,6 · 22,7 · 22,7 · 23,0 · 23,3 · 23,3 · 23,3 (rij 50–56): bovenaan breder. | Rij 50–51 1 px naar buiten: (22,y) transparant→K, (23,y) K→D (zoals rij 48–49). Run 9 → 7. 4 px. |
| 15 | nabije voorpoot, rechterrand (x32, rij 51–60) | **nee.** Model: 33,4 · 33,3 · 33,25 · 32,9 · 32,6 … (rij 51–55): versmalt geleidelijk, niet in één stap op rij 51. | Rij 51–53 1 px naar buiten: (33,y) transparant→0, (32,y) 0→M. Runs 6 + 7. 6 px. |

## Controle
- 56 pixels veranderd, waarvan 18 silhouetpixels; per lijn hooguit 1 px verschoven.
- Oog K4 (x15–19, y21–24): 0 px. Neus/mond-zone x8–12: 0 px. Geen nieuwe kleuren (palet = r14).
- Geen lichte vulling op de buitenrand (controle: 0 open randen, zoals r14).
- Strepen blijven 1 px breed; ze buigen nu zoals in het model.

## Niet gedaan / ter info
- Lijn 2 en 6 zijn recht gelaten: in het model zijn ze ook recht (afwijking < 0,2 px). Bij 16 modelpx per spritepixel is meten daar klaar (GEMINI.md, impala r7–r10).
- Ongemarkeerd en nog 8 px recht: de linkerrand van de achterpoot rechts (x52, rij 53–60) en van de nabije voorpoot (x30, rij 53–60). Niet aangeraakt, want Jordi markeerde ze niet.
