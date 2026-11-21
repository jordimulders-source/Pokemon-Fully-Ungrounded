# Kelp-/anemoon-Vileplume frontsprite, ronde 2

Bestanden: `vileplume_r2.png`, `kaal.png` (= r1), `bouw.py` (`python3 r2/bouw.py r2`), `vel.png` (r2 8× | r1 8× | model 8× / close-ups 12× / 1×).

## Wijzigingen t.o.v. r1 (eigen zwakke punten)
- **Lijftint weer volgens de modelschaduw:** het lijf tussen de klonten is R2 met R1 alleen waar het model R1 heeft (onderrand), gemeten binnen 2 spritepx. r1 zette alles op R1 en was daardoor roder/donkerder dan het model (tintverdeling model R2:R1 = 1,3; r2 1,6; r1 0,3). Geen kleurafwijking meer.
- **Klontpunt** gemeten op de lichte modeltentakels zelf (r1 nam ook de R0-lijnen mee). Klein effect.
- **Kraaglijn** bovenop het lijf: in het model een ondiepe U (natief x86–95, y102–105, W0); de reductie gaf twee losse streepjes. Doorlopend op de modelplek: y33 x25 en x29, y34 x26–28 (3 px anders dan na de reductie).
- **Kratergrijs:** in de kraterzone wint grijs vanaf 30 % dekking als het minstens zoveel dekt als zwart en niet aan de anemonen grenst (1 px).
- Rechterarm (r1-twijfel): nagemeten, de vorm met oksel-inham staat zo in het model (arm natief 4–5 px = 2 spritepx); niet aangepast.

## Telling
805 px anders dan de kale reductie: anemonen 713 (mondjes 35) · lijf+armen 34 · poten 54 · krater 4.

## Zwak punt voor r3
- Tintvlakjes < 3 px: R1 7, R2 17, R3 3, W 4 (SPRITE_KERN: geen tintvlakjes < 3 px).
