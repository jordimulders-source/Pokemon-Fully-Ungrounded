# Keuring satelliet fase 1 – sprite r1 (verse keurder, 23 nov)

Gekeurd: `../sprite_r1/sprite.png` tegen `../model/model_gekozen_natief.png` (×0,787). Eerst blind geoordeeld (vel `vel.png`, raster `sprite_12x_raster.png`), daarna pas `RAPPORT.md` van de maker gelezen.
Scripts: `meet.py` (silhouet tegen het model, tintclusters), `rond.py` (cirkelfit + trappen bol), `voorstel.py` (de reparaties hieronder op een kopie → `voorstel.png`, `vel_voor_na.png`; de sprite zelf is niet aangeraakt).

## Eindoordeel
| eis | oordeel |
|---|---|
| 1. Accuraat op het model | **PASS** |
| 2. Gen 3-sprite volgens SPRITE_KERN | **BIJNA** (23 pixels + 2 paletkleuren, geen vormwerk) |

## Eis 1 – trouw aan het model: PASS
- Silhouet gemeten (eigen afbeelding van het model, dekking per spritecel): **0 px model-only**, 69 px sprite-only, en daarvan zijn er 68 precies 50/50-cellen (gelijkspel) en 1 is de gemelde nieuwe pixel (32,54) aan de bovenrand van de middelste antenne. Het silhouet is gelijk aan de kale reductie van de maker.
- Onderdelen afgevinkt op 8×: bol (59×52 bbox, zelfde plek), gebogen naad (verticaal stuk rechts → diagonaal → linksonder, zoals het model), oog (paarse buitenring, donkere binnenring, teal iris met lichte tint linksboven, zwarte pupil; geen glans), **3 zichtbare paarse bolvoetjes** (linksboven plat zoals het model, rechtsboven, onder), **precies 4 antennes**, richting en lengte als het model (ook de verlengde onderste).
- Kleurafwijkingen (naadlip → w, reflectierand → l, diepere schaduw) zijn kleur en dus toegestaan.

## Eis 2 – Gen 3: BIJNA
**Volume (eerst getoetst): ja.** Hooglicht op de bolling linksboven, basis, schaduw, diepe-schaduwsikkel rechtsonder, reflectierand onderaan; de tintverdeling zit binnenin, niet alleen langs de rand. Leest op 1× en 2× als een glanzende bol met een oog.

**Gemeten tegen echte Gen 3-sprites** (`graphics/pokemon/*/anim_front_gba.png`, frame 1):
| sprite / groep | tinten (helderheid) | stappen |
|---|---|---|
| Electrode wit | 255 / 238 / 205 + selout 158 + lijn 84 | 17 / 33 / 47 |
| Electrode rood | 200 / 157 / 107 / 83 + 50 + 16 | 43 / 50 / 24 |
| Voltorb wit | 255 / 216 / 174 + lijn 84 | 39 / 42 |
| Voltorb rood | 195 / 128 / 107 / 92 + 50 | 67 / 21 / 15 |
| Togepi geel | 249 / 240 / 195 / 147 + 65 | 9 / 45 / 48 |
| **sprite lijf** | 255 / 225 / 172 / 127 + selout 64 / lijn 23 | **30 / 53 / 45** |

**Open punten van de maker**
1. **4 lijftinten: akkoord.** Gen 3 doet dit zelf bij grote bollen (Voltorb- en Electrode-rood en Togepi-geel hebben 4 tinten + lijn). Het volume hangt eraan; niet samenvoegen.
2. **Stap 53: te groot.** De grootste gemeten Gen 3-stap tussen twee lijftinten is 50 (Electrode rood), wit gaat niet verder dan 47. Reparatie P1 hieronder brengt het naar 42 / 45, alleen palet, geen pixels.
3. **Banding:** de lichte band **onderaan** (l binnen m, rijen 49–51) is Gen 3: Electrode heeft dezelfde reflectierand langs de onderkant van het rode deel. Mag blijven. De 1 px w-strook **rechts naast de naad** (kol 30, rij 26–36) loopt evenwijdig aan naad en rand; op 1×/2× leest hij als lip van de naad, niet als dubbele lijn. Geen FAIL; laat staan.

**Regels**
- Buitenlijn: 155 zwart + 125 donkerpaars, geen lichte randpixel behalve **(12,23)** (P tegen transparant = open rand). Selout links/boven paars, vanaf rij 37 zwart: één wissel, geen om-en-om. Antennes: paarse bovenrand, zwarte onderrand, consequent.
- Antennes: per kolom 2–3 px kleur over de hele lengte (A1 2–3, A2 2–3, A3 2, A4 2–3); alleen de uiterste punt van A1 (kol 41) 1 px. Voldoet aan "geen 1 pixel lijnen".
- Oog: leest op 1× als oog, geen glans. In orde.
- Tintvlakjes < 3 px (8-buren): lijf (26,7)/(26,8)/(26,12)/(27,14) rond de bovenkant van de oogring, (25–26,36) en (36,37) aan de rechterrand, lichtpaars (41,6) aan het einde van de naad. Antennepunten tellen niet.
- Hooglicht: rechterkant is een rechte verticale rand (kol 21, rij 19–24) met een knobbel op (22,22); geen vloeiende curve.

**Bol mooi rond (Jordi: "let erop dat de bol mooi rond blijft")** – `rond.py`: cirkelfit op de zichtbare buitenlijn (zonder antennes/voetjes): centrum (20,5 ; 33,6), r = 18,3.
| kwadrant | max afwijking | rms |
|---|---|---|
| linksboven | −0,76 px (3,29) | 0,33 |
| linksonder | +0,74 px (18,52) | 0,35 |
| rechtsboven | −0,82 px (37,29) | 0,40 |
| rechtsonder | +0,86 px (23,52) | 0,45 |

Nergens > 1 px: de bol is rond. Wel onregelmatige trappen (de kale reductie van het model heeft exact dezelfde, dus dit komt uit het verkleinen, niet van de maker):
- **Linksboven** (rijen per x, van de evenaar omhoog): 8, **5, 1, 2, (6 overgeslagen)**, 2, 1 — tegenover linksonder 8, 3, 2, 1, 1, 2, 1. Kolom 3 te lang, x = 6 overgeslagen: een platte schouder met een knik op rij 21→22.
- **Linksonder** (kolommen per y): 1, 1, 1, 1, 1, 1, **2, 1, 2**, 2, 3, 6 — zigzag bij kol 8–10.
- **Rechts**: x = 37 over 5 rijen boven x = 38 over 4 rijen (evenaar korter dan het stuk erboven).
- Boven: 16 px vlak op rij 16 (kol 13–28), maar kol 15–22 ligt achter het voetje en het model is daar ook vlak; binnen 1 px niet op te lossen zonder het voetje te verplaatsen → laten.
- Onder: 6 px op rij 52, 0,8 px buiten de fit, uit het model, symmetrisch genoeg → laten.
Na de reparaties R1–R3 (getest in `voorstel.png`): linksboven 8, 3, 2, 2, 1, 2, 1 (spiegel van linksonder), linksonder 1-1-2-2-2-3-6, rechts 4/5; max afwijking per kwadrant 0,64 / 0,68 / 0,64 / 0,78 px. Alle verschoven randpixels liggen binnen 1 px van het model.

## Reparaties (op prioriteit; (rij, kol), tintnamen als in het makerpalet)
1. **R1 rand linksboven naar de cirkel** (lijn 1 px naar binnen, binnen 1 px van het model): (22,5) D → transparant; (24,4) D → transparant en (24,5) w → D; (25,3) D → transparant en (25,4) w → D; (26,3) D → transparant en (26,4) w → D.
2. **P1 palet** (stap 53 → 42/45): tint 7 l (174,162,218) → (184,174,226); tint 8 m (130,114,184) → (140,126,194). Geen pixels.
3. **T1 hooglicht afronden** (rechte rand + knobbel): (22,22) W → w; (18,20) W → w; (19,21) W → w; (24,21) W → w.
4. **R2 rand linksonder**: (48,9) transparant → zwart; (47,9) zwart → m.
5. **R3 rand rechts**: (29,38) transparant → zwart; (29,37) zwart → m.
6. **T3 open rand**: (12,23) P → D.
7. **T2 losse tintpixels**: (26,12) w → W; (27,14) w → W; (26,7) W → w; (36,37) l → m; (25,36) l → m; (26,36) l → m; (41,6) p → P.

Totaal 23 pixels + 2 paletkleuren; geen vorm uit het model verandert. Na deze reparaties verwacht ik PASS op beide eisen.
