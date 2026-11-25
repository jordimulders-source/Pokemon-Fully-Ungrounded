# Regionale Poliwhirl (Ice/Poison) – sprite r1 (maker)

Model: `../referenties/gemini_gekozen_v1.png` (bevroren, Jordi 25 nov). Uitvoer: `poliwhirl_regional_r1_{a1,a2,b1,b2}.png` (64×64, geïndexeerd, index 0 transparant, beestje 50×47 op x 7–56, y 12–58), `vel.png`.
Varianten: **a** = spiraalvorm van de Gen 3-Poliwhirl in modelrood, **b** = Poliwhirl-spiraal letterlijk; **1** = ogen Gen 3-Poliwhirl, **2** = ogen regionale Poliwag (af).

## Aanpak (overnemen, niet hertekenen; scripts van de regionale Poliwag r1)
1. `meet.py`: periode **15,36 px** (x en y), zelfde raster als bij Poliwag v2.
2. `reduceer.py` → `kaal.npy`/`reductie.npz`: vast raster, fase 6,0/5,0 (materiaalzuiverheid 0,833), meerderheidsmateriaal per cel (lucht/geel/rood/ijs/donker).
3. `basis.py` (gedeeld door alle vier):
   - A tinten uit de modelhelderheid: lijf zwart σ 1,0 (≥ 68 → 4, ≥ 38 → 3, anders 2), geel σ 1,0 (≥ 203 → 5, ≥ 172 → 6, anders 7), handschoenen en kristallen vrijwel per cel (σ 0,45), rood per cel.
   - B omlijning: lijf zwart; geel licht kant 7 / schaduwkant 1; handschoenen 11 linksboven / 1 rechtsonder (zoals het model: blauwgrijs boven, zwart onder); kristallen 11 / 15. Lichtkant per pixel uit de 3×3-luchtburen.
   - C reparaties naar het model (zie onder) + opvullen van het modeloog.
4. `varianten.py`: spiraal en ogen als bovenlaag. `uitvoer.py`: png's, diffbewijs, afwijkingen. `vel.py`. Hulp: `celinhoud.py`, `naast.py`, `toon.py`, `prev.py`, `controle.py`.

## Palet: 15 kleuren + transparant, identiek aan de regionale Poliwag (`palet.py`)
1 omlijning · 2/3/4 lijf · 5/6/7 geel · 8/9/10/11/15 ijs · 12/13/14 rood. Alle vier de varianten gebruiken alle 16.
Omzetting van de bronsprites: Poliwhirl wit → 8, lichtgrijs 222 → 9, 189/164 → 10, grijs 123 → 4, 82 → 3, zwart → 1 (ogen en spiraal b); spiraal a: band 123 → 12, 82 → 13, zwart → 14.

## Bewijs: varianten verschillen alleen in oog- en spiraalzone (`uitvoer.py`)
a1–a2 93 px (alle in de oogzone), a1–b1 81 px (alle in de spiraalzone), a1–b2 174 (93 + 81); **0 px erbuiten** voor alle zes de paren.

## Afwijkingen t.o.v. de kale reductie (andere index / ander materiaal)
| zone | px | a1 | a2 | b1 | b2 |
|---|---|---|---|---|---|
| ogen | 184/176 | 134 / 75 | 111 / 44 | 134 / 75 | 111 / 44 |
| spiraal | 146 | 65 / 48 | 65 / 48 | 91 / 88 | 91 / 88 |
| mond | 56 | 14 / 2 | idem | idem | idem |
| kristallen | 202 | 92 / 0 | idem | idem | idem |
| handschoenen | 141 | 45 / 8 | idem | idem | idem |
| voeten | 93 | 32 / 5 | idem | idem | idem |
| rest (kop, lijf, armen, benen) | 418 | 107 / 1 | idem | idem | idem |
"Andere index" is vooral tint (lichtveld) en omlijning; "ander materiaal" zijn de pixels die niet letterlijk uit de reductie komen.

**Pixels die niet uit de reductie komen (buiten ogen/spiraal):**
- Linkerkristal (10,8), (10,9), (10,10): wit facet dat via een kier met de achtergrond verbonden was en daardoor als lucht werd gelezen → ijs (8, uit de modelcel W9). Dit zijn ook 3 van de silhouetverschillen.
- Neusgaten (19,8) en (22,8) → 7: de twee donkere stipjes van het model (minderheid in de cel).
- Mond (17,11) en (25,11) → 13: cellen met 40 % rood die de modellijn verbinden (anders twee losse stukken).
- Teenlijnen (12,42), (13,42), (36,43), (37,44), (40,44) → 7: de donkergele lijnen van het model (30–40 % van de cel).
- Ruis: 6 losse tintpixels in lijf/geel naar de buurtint: (38,13), (26,14), (8,19), (18,32), (33,35), (13,40).
- Handschoenen 8 / voeten 5 / mond 2 materiaalwissels = omlijning (zwart aan de schaduwkant).

**Ogen (toegestaan: "negeer de ogen want die kan je fixen"):** het hele modeloog (wit, pupil, zwarte ring; cirkel r 2,7 rond (16; 4,5) en (29; 4,5)) eerst opgevuld met de kop eromheen (buurtint), silhouetrand blijft; wit op de rand → 1. Daarna:
- **1:** linker- en rechteroog van `graphics/pokemon/poliwhirl/anim_front_gba.png` 1-op-1 (samenhangend oog, 7×7), plus 1 px ring in 1 (het blauwe ooglid van Poliwhirl omgezet). Het Poliwhirl-oog is groter dan het modeloog (7 tegen ±5 cellen): het bedekt het gele kopje boven het oog en de ring steekt 9 px buiten het silhouet ((15,0), (13,2), (12–13,3–5), (13,6)).
- **2:** de oogregels van de regionale Poliwag letterlijk (`OOG_VER` links, `OOG_NABIJ` rechts, inclusief hun ooglid 6/7 en lijf 2); 1 px buiten het silhouet: (13,7).

**Spiraal (toegestaan: "die kan je ook gewoon van poliwhirl copypasten"):** modelrood in de buik terug naar geel (tint uit het buikgeel), dan de Poliwhirl-spiraal 1-op-1 met het midden (31,32) op het midden van de modelspiraal (22,5; 23,5).
- **Let op: niet 1–2 px bijgeknipt maar veel meer.** De hele Poliwhirl-spiraal is 21×19 px; de modelspiraal is 11×10 en de hele gele buik ±13×12. Gebruikt is een cirkel met straal 5 rond het midden (= middelpunt + één volle winding; straal 5 valt volgens de bandmeting in een witte tussenruimte, dus de knip loopt niet door een band). De buitenste winding (±5 px rondom) is weggelaten.
- a: band 12/13/14 (Poliwhirls eigen schaduw in rood), tussenruimtes = buikgeel. b: Poliwhirls zwart/wit/grijs, omgezet naar palet (wit wordt licht ijsblauw: het palet is vol, geen neutraal lichtgrijs).

## Eigen zwakke punten
1. **Spiraal a leest op 1× als een rode schijf met gele krul**, niet als de dunne ringen van het model: Poliwhirls kern is een dikke band met 1 px tussenruimte. Groter kan niet zonder de buik te verlaten. Spiraal b leest als een donkere schijf met lichte krul.
2. **Ogen 1 zijn groot (brilachtig)** en bedekken de gele bovenkop; ogen 2 zijn kleiner en asymmetrisch (vér- en nabij-oog van de 3/4-Poliwag), het rechteroog leest als een witte halve maan. Beide letterlijk overgenomen, niet aangepast.
3. **Kleine tintclusters (<3 px): ±175**, vooral in kristallen (113 ijs, 30 rood) = de facetten van het model op 4–8 px per kristal; niet gladgestreken (regel "nooit rustiger maken"). Lijf 15 / geel 23 zijn vooral overgangen bij omlijning, neusgaten, teenlijnen.
4. Voorhoofdstreep tussen de ogen is lijf 4 (modelgrijs ±70) en leest lichter dan de zwarte streep van het model.
5. Lijfzwart (40/58/88) leest blauwgrijzer dan het bijna zwarte model (zoals bij de regionale Poliwag gekozen).
Geen lichte pixels op de buitenrand (controle.py), 16 kleuren incl. transparant in alle vier.
