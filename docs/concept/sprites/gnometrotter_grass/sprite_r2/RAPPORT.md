# Gnometrotter (Grass) – frontsprite r2 (23 nov)

Basis: r1 (`../sprite/`), zelfde gedeelde reductie, palet en pijplijn (scripts hier gekopieerd en aangepast). Lever: `gnometrotter_grass.png`, `gnometrotter_grass_8x.png`, `vel.png` (r2 | r1 | model op schaal 8×; 1× licht/donker; naast Gnomad en Rock r2). Silhouet t.o.v. r1: 0 px anders; 158 px anders t.o.v. r1.

## Reparaties (alles uit het model, niets getekend)
1. **Neus als losse bal** (10 px): neusvulling als bal (8, sikkel 7 rechtsonder, 15 linksboven), rand rondom 6 met zwarte boog linksonder (zoals r1), en waar de neus tegen het even roze lijf ligt is de rand zwart (= de zwarte modellijn rondom); lijfpixels die de neus raken krijgen slagschaduw 7.
2. **Rock-keurpunten voor deze pose**:
   - **Voetballen** (`zones.py`): de blauwe modelvlakken onder Y 440 (model) zijn eigen onderdelen voetbal L/R met de dij ervoor; grenslijn dij|voet = onderdeelgrens/modellijn in 9; voet licht 11, schaduw 10 alleen rechtsonder (45 px).
   - **Geen ruis in de broek**: in broek en voeten tellen alleen lange modellijnen (skeletstukken ≥ 45 modelpx, `skel_lang.npy`); losse lijnstukjes < 4 px weg (37 px).
   - **Schouderovaal R**: vulling 8 over de hele breedte, 15 linksboven, lijn 6 rondom inclusief onderrand (10 px).
   - **Linkerarm**: had in Grass geen dambord (arm = twee schijfjes met lijn ertussen, zoals het model); ongewijzigd.
3. **Bladmuts** (56 px): alleen de lange bladgrenzen uit het model (groene lijnkleur 5); elk blad in zijn meerderheidstoon van het model, plus de Gen 3-schaduwsikkel aan de rechterkant van de muts. Geen losse donkere pixels meer.

## Afwijking t.o.v. de kale reductie (`tel.py`)
Totaal 1176 / 2056 (lijn 640, DC 3, vlaktint/volume 533); silhouet 9 px erbij (dunne delen op drempel 0,35, zelfde als r1), 0 eraf. Pixels buiten de regels: zoals r1 (hooglichtjes, 5 px onderdeelkaart, 4 outline highlights, 2 px om-en-om).

## Controle
64×64 P, transparant 0, 16 kleuren, zwart 9,6 %, geen losse zwarte pixels; lichte kleur op de buitenrand alleen de outline highlights.

## Zwakke punten
- Schouderovaal leest nu als licht ovaal, maar blijft klein naast de lijfplaten.
- Rechtermuts is één donker vlak met één bladgrens; het model heeft daar twee bladeren (de tweede grens is een kort skeletstuk en valt onder de 45 px-regel).
