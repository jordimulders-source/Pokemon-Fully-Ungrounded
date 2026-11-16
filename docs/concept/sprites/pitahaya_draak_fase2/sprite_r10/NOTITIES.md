# r10 (16 nov): eindkeuringslijst uitgevoerd op `sprite_r9/pitahaya2_r9A.png`

Model = overnemen, nooit hertekenen. Elke pixel staat met de reden in `pitahaya2_r10_afwijkingen.txt` (punt, x, y, oud, nieuw, reden). Script: `maak_r10.py`. Het script controleert met asserts de oude waarde van elke pixel en of de diff buiten de lijst 0 is. Ook bewaakt: het silhouet wijzigt alleen op de 10 B-pixels, en de V-rand en het gehemelte zijn bevroren. Meetgereedschap: `modeltoonkaart.py` (gladde modelhelderheid binnen het roze, modeltoon per spritepixel). Vel: `vel.py` → `vel.png`.

**Totaal: 93 px in `pitahaya2_r10.png`, plus 8 px in de variant `pitahaya2_r10_plaatlicht.png` (alleen D2).** Kleuren 13, dambord 7 (geen nieuwe).

| Punt | px | Wat |
|---|---|---|
| A1 | 16 | Mondhoek (9 px) en verre lip (6 px) van P naar p; (17,45) van p naar r (modeltoon r). |
| A2 | 3 | Onderkant van de onderkaak (9–11,54) wordt r (schaduw, zoals Exploud en Gyarados). |
| A3 | 2 | (9,53) en (10,53) van p naar P: modeltoon P, voorste lipbocht. P staat nu nergens meer naast w. |
| A4 | 2 | (8,48) en (8,49) van d naar r: de lipcontour is één tint. |
| E | 0 | d #681838, P #f8a0c0, g #305830, G #4f8040, h #78a850, H #b0d068. Stappen roze d→r→p→P: 21/43/50 werd 34/43/61. Groen: 29/30/28 werd 35/38/43. Het roze blijft roze (op 1× en 2× bekeken). |
| B1 | 8 | Staart rechts: (61,48–51) K (modeldekking 2,3,3,2/9), (60,48–51) g. Langste rechte stuk: 7 → 4 px. |
| B2 | 4 | Linkerpoot: teenlijn (12,58) K, inkepingen (12,59) en (15,59), bolling (12,56) (dekking 2/9). Onderrand: 9 → 3 px recht. |
| B3 | 6 | Kop: (18–20,34) weg (dekking 6/9), (18–20,35) d. Bovenrand: 10 → 4 px recht. |
| C1 | 17 | Vlaktint op de buitenrand → selout (15 G→g, 2 p→d). Vlaktint op de rand: 17 → 0. |
| C2 | 4 | Kopselout één tint d. |
| D1 | 19 | Grenzen gelegd op de gladde modelhelderheid (σ 1,5 spritepx, alleen roze). p→r (10 px) waar de waarde < 103 is: de terminator stijgt naar de romp (rij 42/43) en bij de keel, en ligt laag (44/45) waar het lijf naar voren bolt. r→d (9 px) waar de waarde ≤ 78 is: een sikkel boven de nabije voorpoot (24–27,48–49) en langs de middelste dij ((37,50), (38,51), (39,51)). |
| D3 | 11 | Groen hooglicht h→H op het randlicht van het model (≥ 4 van 9 natieve px in H-kleur): middelste dij 3, achterste dij 1, staartkrul 7 (de spiraalband). H gaat van 7 naar 18 px. |
| D2 | 8 (variant) | P waar de gladde modelhelderheid ≥ 140 is: de top van de twee grote rugplaten. Dit staat niet in het model en zit alleen in de variant. |
| F | 1 | (40,52) G→g (modeltoon g). |

## Afwijkingen van de keuring (gemeten; meting gevolgd)
1. **D1:** de keurder noemt de evenaar "een liniaal die niet in het model zit". Het model heeft de p/r-grens zelf ook recht op rij 44/45 (modeltoon). De gladde kaart stelde ook 10× r→p voor. Die zijn niet gedaan: op elk van die plekken heeft het model een naad of plaatschaduw (modeltoon r), en die wegpoetsen is hertekenen. De onderhelft blijft daardoor grotendeels één vlak r, zoals in het model.
2. **D1-sikkel:** de keurder noemde "rij 52–53, x 23–27 en x 38–41". Daar zitten groene poten. De donkerste modelplekken in het roze liggen op rij 48–51. De keel krijgt daarom op (24–27,48–49) wel d, omdat het model daar het donkerst is (L 75–78).
3. **D3:** de keurder vroeg om H "linksboven op elke dij". Het model heeft het lichtste groen als **randlicht rechts** op de dijen en langs de staartkrul. Ik heb het model gevolgd, niet linksboven. (46,47) (4/9) is weggelaten, omdat hij een dambord gaf met (47,48).
4. **F:** (27,50), (28,51), (21,52), (48,52) en (47,53) blijven G. Volgens de modeltoon zijn ze G: de donkere linkerrand van de middelste dij, een stukje verre poot, en de overgang h→G→g onder de achterste dij. Alleen (40,52) is aangepast.
5. **B2:** (12,59) en (15,59) hebben een modeldekking van 9/9. De inkeping volgt dus de teenlijnen in het model en niet de dekking. Dat is de reparatie van de keurder, en die heb ik zo overgenomen.

## Zelftoets (1×, 2×, 8×, naast het model, Salamence en Lairon)
- A–G: A, B, C, E en F zijn opgelost. D1 is gedeeltelijk opgelost (zie afwijking 1). D2 zit in de variant. D3 is gedaan volgens het model. G-A6 (rechte stukken) is opgelost door B.
- Nieuwe losse pixels of dambordjes: geen (dambord 7 → 7, geen nieuwe posities). De nieuwe H- en d-pixels liggen als diagonale ketens langs de vorm.
- Rechte stukken: staart 4, kop 4 en poot 3 px (was 7, 10 en 9).
- Zwak punt dat blijft: de onderkant van het lijf is een groot vlak r. Dat komt uit het model. Meer volume daar betekent tinten tekenen die het model niet heeft. Dat is een keuze voor Jordi en niet voor de maker.
