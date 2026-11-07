# Nachtaap fase 2: kleursprite ronde 2

Deze ronde is een reparatie in twee zones. Al het andere is ronde 1, bevroren:

| Zone | Gebied | Wat er veranderde |
|---|---|---|
| A, kop | x 2–27, y 34–57 | maan, ogen en snoet |
| B, verre hand | x 2–16, y 54–61 | vingers en tint |

**Bestanden:**
- `nachtaap.png` en `normal.pal`.
- `vel.png`, met daarop:
  - ronde 1 en ronde 2 op 4×, en ronde 2 ook op donker;
  - de onderlaag;
  - de kop op 8× naast de onderlaag en fase 1;
  - de ogen op 8× naast die van fase 1;
  - 1× en 3× naast Lairon, Sableye, Aipom, Grumpig en Mismagius.
- In `bron/`:
  - `raster.txt`;
  - `bouw.py` met de uitvoer in `bouw_uitvoer.txt`;
  - `alpha_bewijs.py`;
  - `diff_bewijs.py` met de uitvoer in `diff_uitvoer.txt`;
  - `vel.py`.

## Bewijs
- **Alpha-diff:** 0 (1459 px), zowel tegen de `.txt` als tegen de `.npy`.
- **Open randen:** 0.
- **Pixeldiff met ronde 1 buiten zone A en B:** 0. Binnen de zones zijn 121 pixels gewijzigd.
- **Palet:** index 0–14 is gelijk aan ronde 1, dus het lijf en de nabije hand houden exact hun kleur. Index 15 was een ongebruikte reserve en is nu `f` (e2c8a0), de crème van de verre hand.
- **Maan, gemeten tegen de onderlaag** (onderlaag 4:1 verkleind, wit = minstens 8 van de 16 subpixels wit, kopgebied y 34–49):

| | wit | wit + zilverlila |
|---|---|---|
| onderlaag | 67 | – |
| ronde 1 | 58 | 77 (te veel lila, te smal) |
| ronde 2 | 83 | 94 |

  De overlap met de onderlaag is 52 px. Dat ronde 2 iets groter uitvalt, komt doordat het silhouet ±1 px ruimer is dan de onderlaag.

## Zone A: wat er concreet anders is
**Maan**
- Het is een groot wit vlak over de bovenste helft van de kop:
  - de bovenkant begint direct onder de kruinlijn (y 37) en is rond (6 → 10 → 12 → 13 → 15 → 17 px breed);
  - het violet erboven en eromheen is alleen nog een rand van 1 px.
- De punten lopen aan beide kanten langs de ogen omlaag tot y 47, onder ooghoogte.
- Het violette middenstuk bolt rond in, tot y 41.
- Zilverlila (`n`) zit alleen nog als randje van 1 px aan de schaduwkant (rechts) en aan de onderste punten.
- Het lichtlila vlak aan de rechterkant uit ronde 1 is weg. Dat las samen met de band als een voorhoofd en wenkbrauwen.

**Ogen, anders dan fase 1 (Jordi: "incl ogen")**

| | fase 1 | ronde 2 |
|---|---|---|
| Omvang | groot, 7 × 8 px op een kleinere kop | 6 × 6 px, kleiner ten opzichte van de kop |
| Iris | zachtroze/magenta, vult het oog | karmijn, alleen een ring van 1 px: donker boven, licht onder |
| Pupil | – | zwart, 2 × 2, precies in het midden |
| Bovenlid | zwaar, rondom crème | geen zwaar lid |
| Ring | – | donker rondom: zwart in de maan, `d` aan de onderkant in de vacht |
| Glans | – | 1 px linksboven |

- De twee ogen zijn hetzelfde opgebouwd, met de glans aan dezelfde kant en de pupil gecentreerd. Het verre oog kijkt niet meer anders.
- Het resultaat is een strakke, ronde, starende nachtaapblik (zoals op foto 1 en 4): niet bezorgd, niet slaperig, geen babyoog.

**Snoet**
- Fase 1 en ronde 1 hadden een breed, kort babysnoetje.
- Nu begint er een neusbrug tussen de ogen (`l`/`m`, y 47–49). Die loopt door in een smaller, langer snoetje (5 px breed, y 48–53).
- Daarop zitten een neus van 2 px, één rij lucht en een korte, rechte mond (3 px). Onder de mond zit nog een rij snoet, zodat de mond niet met de kinlijn samensmelt.

**Toets naast fase 1** (8× en 1× op het vel):
- Fase 1 heeft een crème gezichtsschijf met grote roze ogen en een donkere wig.
- Ronde 2 heeft een witte maan, kleinere rode ringogen met pupil en een violet gezicht met een smal snoetje.
- Dezelfde lijn blijft herkenbaar aan de vacht, de oortjes en de rode/roze oogkleur. Het leest niet meer als "fase 1 met ander lijf".

## Zone B: verre hand
- De vulling is nu een warme crème in de schaduw (`f`). Daardoor is het grijsbruin weg; de omlijning blijft de crème-omlijning `t`.
- Twee inkepingen van 1 px in de omlijning bij de vingertoppen (x 6 en x 8, y 58–59) geven 3 vingers.
- Aan de rechterkant is de hand gescheiden van de nabije hand met `t`, niet met zwart.
- De knokkellijn uit ronde 1 is weg.

## Eerlijk
- De verre hand blijft door het bevroren silhouet een lange, platte vorm (zoals in de onderlaag). Op 1× leest hij nu als een lichte hand met vingertoppen, niet als een plankje.
- Zelf zie ik geen open zwak punt.

## Lessen
- **Een maan die je maar half in wit zet, met lila aan de schaduwkant en een lichte vachtrand erboven, leest op 1× als een band met een lila voorhoofd.** Houd een kleurvlak dat "wit" moet lezen voor minstens ±85% wit, met de schaduwtint alleen als randje van 1 px.
- **Meet een kenmerk uit de onderlaag na door 4:1 te verkleinen** (aantal witte pixels plus overlap) in plaats van op het oog over te nemen.
- **"Volgende fase" zit in het gezicht.** Kleinere ogen met een irisring en een grote centrale pupil, een neusbrug en een smaller, langer snoet maken een kop volwassener zonder de omtrek te veranderen.
- **Bij een kleurfix in één zone:** gebruik een vrije paletindex voor de nieuwe tint, zodat de bevroren delen ook in RGB exact gelijk blijven (pixeldiff in indexen én hetzelfde palet).
