# Kudu sprite ronde 12: B6a netter, minder rechte lijnen (maker)
Jordi: "doe maar b6b, maar netter, minder rechte lijnen", daarna "o dat is mijn fout, b6a bedoelde ik".
- **Uitgangspunt:** de png `r10/kudu_r10_B6a.png` zelf. Die wordt ingelezen, niet opnieuw gebouwd.
- **Wat blijft:** de vorm en manier van B6a, de schaduw van de manen en oog K4.
- **Scripts:**
  - `sprite/r12.py` zet de pixels, elk met een reden.
  - `sprite/r12_check.py` doet de controles.
  - `sprite/vel12.py` maakt de pngs, het vel en `telling.txt`.

## Telling rechte lijnstukken (> 3 px)
Gemeten op 0/d/K-pixels die aan manen- of franjevulling (l/m) grenzen, horizontaal en verticaal.

| | Aantal | Waar |
|---|---|---|
| **B6a vóór** | 5 | x9 y30–33 (franje links), x12 y30–34 en x13 y35–38 (franje langs de halsstrook), x15 y28–35 (nekmanen langs de halsstrook), x26 y32–36 (schouderrand) |
| **r12 na** | geen | |

Ter info, met de D-tint als lijn meegeteld:
- **x14 y25–29:** D D 0 d d. De twee D's boven de kaak zijn van B6a.
- **x27 y32–38:** de rand 0 met de slagschaduw D erboven en eronder, zoals in B6a (rand + 1 px D).
- **franjeonderkant y38 x10–14:** D 000 D.
- **Overige:** stukken buiten de wijziging die al in B6a zaten (x29 y27–30, y28 kaak, y30 kambodem, y40 punt).

## Controle (`telling.txt`)
- **41 px anders dan B6a.** Buiten manen + franje + halsstrook + 1 px rand: **0 px**. Oogvlak K4: **0 px**.
- **4 px vallen buiten de oude r8-zone** (`L.ZONE`): (28,34), (28,35), (28,36) en (27,38). Dat is de slagschaduw D, die 1 px naast de nieuwe schouderrand meeschuift.
- **Tintvlakjes < 3 px rond de wijzigingen:** geen. Er was er één, (17,35) m, en die is opgelost.
- **Palet:** ongewijzigd, 15 kleuren.

## Gewijzigde pixels (per groep; elke pixel met reden in `telling.txt`)
1. **Halsstrook als boog.** Hij blijft 2 px M en loopt nu:

   | Rij | x |
   |---|---|
   | 28 | 13, met de kaak-D op 12 ernaast |
   | 29 | 12–13 |
   | 30–32 | 13–14 |
   | 33–35 | 14–15 |
   | 36–38 | 15–16 |
   | 39 | 16–17 (B6a) |

   - **Afwijking t.o.v. B6a:** overal ≤ 1 px. Rij 28–29 schuift 1 px naar links, rij 33–38 1 px naar rechts.
   - **Waarom het niet anders kan:** in B6a liep de halsstrook 7 rijen recht (y28–34). Met hooguit 1 px verschuiving moest de boog daarom onder de kaak al beginnen.
2. **Nekmanen, linkerrand (lichtkant d).**
   - Nieuwe ligging: x14 (y28–29), x15 (30–32), x16 (33–35), x17 (36–37). De punt eindigt op (17,38) zoals in B6a.
   - Waar de rand wegging, komt vulling met de tint van de buren: (15,28) m, (15,29) m en (17,35) l.
3. **Keelfranje.**
   - **Linkerrand:** x9 (30–32), x8 (33–35), x9 (36), x10 (37). De bolling begint 1 rij eerder: (8,33) is d.
   - **Rechterrand (schaduwkant 0):** x12 (30–32), x13 (33–35), x14 (36–37). Die volgt de halsstrook.
   - **Vulling:** de nieuwe vulpixels hebben de tint van de buren (l), dus de schaduw blijft zoals in B6a.
4. **Schouderrand.**
   - Was x26 over y32–36, 5 recht. Nu een ronde boog: 25 (y31), 26 (32–33), 27 (34–36), 26 (37–38), 25 (39), 24 (40).
   - De slagschaduw D ligt zoals in B6a 1 px naast de rand en schuift mee.
   - De vrijgekomen randpixels krijgen de tint van de buur links (l/m).

## Zelf gekeken (8× en 1×)
- **Wat beter is:**
  - De halsstrook loopt nu als een gebogen hals van onder de kaak naar de borst.
  - De franje hangt als een lok die de hals volgt.
  - De schouder is rond in plaats van een rechte wand.
- **1×:** het silhouet is hetzelfde als B6a. Het verschil zie je vooral aan de rustiger randen.
- **Opgelost:** de losse m-pixel (17,35).
- **Aandachtspunt voor de keurder:**
  - Op rij 33 wordt de franje aan beide kanten tegelijk 1 px breder (van 2 naar 4 px vulling). Dat moet wel: links liep de rand anders 4 recht en rechts volgt hij de halsstrook. Op 8× leest het als een lok die onderaan dikker wordt, maar de franje is iets voller dan in B6a.
  - Links van de nekmanen staat op x14 y25–29 een verticaal van 5 donkere px (D D 0 d d). Alleen y27–29 is lijn; de twee D's zijn van B6a.
