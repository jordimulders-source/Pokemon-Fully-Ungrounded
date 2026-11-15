# Eindkeuring af (r10A) – sneeuwbolslak fase 2

Getoetst: `af/sneeuwbolslak_fase2.png` / `sprite/maker/raster_af.txt` (palet `pal6.py`) tegen het model `sprite/r8_bol_r7.png` (`meet/model_1x.png`, `model_raster_8x.png`). Gemeten met `meet/px.py`, `meet/recht.py`, `bewaak.py`, een clusterscan (4-verbonden vlakjes < 3 px) en een scan op `#` zonder transparante buur. Naast Glalie, Regice, Snorunt, Walrein, Sealeo en fase 1 gelegd. Eerdere keuringen pas na de blinde indruk gelezen.

**Oordeel: PASS na 1 MOET-pixel** (buiten de opdrachtzone van r8–r10; de bol en de mond zelf zijn in orde).

## Blinde indruk (8× en 1×)
- Op 1× leest alles: kop met oog en blauwe wang, mondlijn, ronde bol op de rug, rode ring, flap en scherfstaart. Naast Glalie/Regice valt hij qua palet en belijning niet uit de toon.
- De bol leest nu duidelijk als **sneeuwbol met storm**: vier schone plusvlokken ((29,27), (33,33), (38,29), (26,36)), daartussen witte krullende banen, glanslicht linksboven, lichte bodem, barst in `d`. Op 1× zie je een witte wervel achter glas, geen bevroren bal meer. Jordi's "vlokken met sneeuwstorm" en "meer sneeuwstorm" zijn ingevuld.
- Mond A: één taps lopende lijn in `d` van de snuitpunt (5,48 `a`) naar onder de wang; leest als mond, niet meer als losse diagonaal. Wijkt bij x 17–18 een rij af van het model (model y 51, sprite y 50), maar dit is Jordi's keuze (A), dus geen punt.
- Silhouet-diff 0 (`bewaak.py` OK). 21 rechte stukken, langste 5 px, geen in de bolrand. 11 kleuren + transparant.
- Buiten bol en mond is alles gelijk aan r7b (diff alleen in de mondzone).

## MOET (letter uit `raster_af.txt` gecontroleerd)
| Pixel | Nu | Wordt | Waarom |
|---|---|---|---|
| (22,39) | c | a | Losse lichte pixel (1 px tintvlakje) precies in de aansluiting kop–bol–nek. Het model is daar donker (L gem 118 ≈ `a` 126, p15 41). Met `a` loopt de kopbovenlijn (21,38 `d` → 22,38 `a`) dicht door naar de neklijn (22,40 `d`); er ontstaat één `a`-hoekje van 3 px met (22,38) en (23,39). Proefrender gemaakt: aansluiting sluit, geen nieuwe tint, silhouet onveranderd. |

(KEURING_r5 wilde (22,39) alleen licht houden als (23,39) `#` werd; dat is `a` geworden, dus die voorwaarde geldt niet meer.)

## MAG
- Ringtinten `r`/`s` liggen dicht bij elkaar (L 87 tegen 101, stap 14 i.p.v. ±30). Zichtbaar door de tintverschuiving, en het is de modelmediaan (r5 MOET 2); laten.
- IJsgroep gebruikt `a b c e w` (+`d`), dus meer dan 3 tinten; `w` alleen als glans/vlok/storm, `e`→`w` stap 19. Zelfde palet als de eerdere PASS; Regice doet hetzelfde.
- Plusvlok (26,36): de linkerarm (25,36) loopt over in de lichte glasrand `e` (24,36)/(25,37); iets minder scherp dan de andere drie. Eventueel (25,37) `e`→`b`.
- Rechterkant bol y 32–34: stormbaan `w` op x 39 direct naast de rand `c`/`e` (x 40–41) maakt een 3 px brede lichte band langs de schaduwkant. Model is daar ook licht (L 179–205); laten.
- Bovenin (y 24 `b`-band, y 25 `wwww`) liggen storm en rand vrij horizontaal gestapeld; leest als stormbaan, geen fout.
- (23,40)/(24,41) `c`: diagonaal lichtpaar naast het open ringeinde; klopt met het model (L 204–208).

## Ter info voor Jordi
- Geen technische of trouwfouten meer in bol en mond; alleen één pixel in de nekaansluiting (die er sinds r6 al zat).
- De storm blijft een stilering: witte banen en plusvlokken op een blauwe doorkijk (in het model donkere banen op licht). Plek, barst, ronding en ijspunten zijn die van het model.
