# Keuring sprite r4 ruimtestation (onafhankelijke keurder, 25 nov)

Getoetst: `sprite/r4/sprite.png` tegen `model/model_gekozen.png` (r13b), `kaal.png`, `diff.png`, `log.txt`.
Alleen de twee eisen: (1) accuraat op het model, (2) Gen 3-frontsprite.
Coördinaten zijn (x, y) in `sprite.png` (64×64). Indexen: 1 = zwart (24,19,36), 2 = navy (41,38,69), 5 = paneellijn-lila, 6/7/8 = paars.

## Oordeel: BIJNA

Op 1× naast het verkleinde model (`vergelijk_1x_4x.png`) leest de sprite als het model: kruisvorm, grote oogbol linksvoor, twee kleine oogbollen, bol rechtsboven, mast boven en onder, vier lange panelen met 4 vakken en een mastpaneel met 3 vakken. Er is niets toegevoegd of weggelaten. De resterende punten zijn kleine fouten in de omlijning, op ongeveer 25 pixels.

## Eis 1: accuraat op het model, PASS met één kanttekening
- 240 pixels wijken af van de kale reductie. Ik heb ze per groep nagelopen in `log.txt` en `diff.png`, en ze vallen allemaal in de besproken categorieën: panelen 4/4/4/4 en mast 3 (dwarslijnen), oogring met iris en pupil, omlijning (navy aan de lichtkant, zwart aan de schaduwkant) en een staafje dat door een gat in de reductie liep. Ik heb geen hertekende vormen gevonden. Het silhouet is gelijk aan kaal, op de omlijningspixels na.
- Kanttekening (zie MOET 3): bij het rechter zij-oog heeft de maker twee **outlinepixels van kaal** overschreven met ringpaars, (49,39) en (50,40). Daardoor ligt de oogring op de buitenrand. In het model ligt onder de ring nog de omtreklijn van de bol, dus dit is geen trouwe "zij-ogen leesbaar"-reparatie.

## Eis 2: Gen 3-techniek
- Kleuren: 16 inclusief transparant (index 0). OK.
- Licht: linksboven. Buizen en bollen lopen van F/E boven naar C onder. OK.
- Bollen rond (`bollen2.py`, cirkelfit op de vrije rand): grote oogbol 0,41 · bol rechtsboven 0,34 · kleine oogbol R 0,38 · kleine oogbol L 0,72. Alle bollen ≤ 0,8. OK.
- Ogen op 1×: het voorste oog is goed leesbaar. De zij-ogen zijn klein maar lezen als teal met een pupil. OK.
- Omlijning: werkt met navy aan de lichtkant en zwart aan de schaduwkant, net als de goedgekeurde fase 2 (gemeten: lichtkant (44,34,84), schaduwkant (24,18,34)). Op een aantal plekken staan zwart en navy om en om op één rand, of zit er een gat in de rand (zie MOET).
- Zwart binnen het silhouet (`binnenzwart.py`, 35 px): alles komt uit kaal, op plekken waar het model een donkere spleet of een donker vlak achter heeft (ring rond de mastvoet, kraag tussen oogbol en buis, mast achter de buis). Geen MOET.

## MOET-reparaties (alleen recolors en twee outlinepixels; niets hertekenen)
1. **Zwart aan de lichtkant tussen navy → navy (2):** (46,21), (38,26), (39,26), (40,26), (33,28), (27,35), (24,37), (50,35), (17,41).
2. **Navy aan de schaduwkant tussen zwart → zwart (1):** (22,50), (36,42), (37,43), (37,47). De rechterrand van de onderste mast (x 37) is dan helemaal zwart.
3. **Open rand bij de zij-ogen:**
   - Rechter zij-oog: zet (49,39) en (50,40) terug naar 1, zoals in kaal (het model heeft daar de omtreklijn van de bol). De ring blijft (49,38) 8, (51,40) en (52,40) 6. Controleer daarna of iris en pupil nog leesbaar zijn.
   - Linker zij-oog: (17,29) transparant → 2. Zo sluit de navy rand die al op x 16 (rijen 30–31) en (18,28) staat, en liggen (18,29) 8 en (17,30) 7 niet meer op de buitenrand. Het silhouet wijzigt met 1 px; de cirkelfit blijft ≤ 0,8 (afstand tot het middelpunt 2,06 bij r 2,12).
4. **Paneellijnen die op de buitenrand eindigen** (lila 5 op de rand; in het model eindigen de lijnen binnen de donkere paneelrand): (34,17) → 2, (26,20) → 2, (30,21) → 2, (52,29) → 2, (56,30) → 2, (37,23) → 1 (punt rechts, schaduwkant). De dwarslijn wordt 1 px korter; het aantal vakken blijft 4/3.

Na de reparatie opnieuw meten: `lijnzijde.py` (verwacht: 0 en 0, op (1,38) na), `bollen2.py` (≤ 0,8) en de lichte randpixels uit `bollen2.py`.

## Ter info (geen MOET)
- (1,38): een zwart puntje aan de linkertip van paneel PD, aan de lichtkant. Op een tip van 1 px valt dat niet op.
- (38,28): een zwart pixel tussen paars 8 in de ring rond de mastvoet. Het komt uit kaal (in het model is het daar overwegend donker). Het leest licht als ruis in de ring; laat het staan tenzij de maker in het model ziet dat het ringpaars moet zijn.
- Voorste oog: de 2×2-pupil (13–14, 49–50) raakt links direct de ring, zonder iris ertussen. In het model zit de pupil links in de iris; het verschil is minder dan 1 px op 64 px, dus het telt niet.
- De lila rand binnen de paneelomlijning en de lengtelijn van de panelen in het model kunnen op 64 px niet getoond worden; telt niet.
- Jordi's open punt uit de SPEC (de stang van het tweelingpaneel weer zichtbaar maken) is een ontwerpvraag en geen keurpunt.

## Bestanden van deze keuring
`vel_keur.py` + `vergelijk_8x.png` (sprite / kaal / model / diff), `zoom.py` + `zoom_*.png` + `vergelijk_1x*.png`, `bollen.py`, `bollen2.py`, `lijnzijde.py`, `binnenzwart.py`, `ruis.py`.
