# Eindkeuring r18 → r19 (16 nov, verse eindkeurder)

r19 is r18 met 20 px opgeschoond door `sprite_r18/eind_fix.py`. Er zijn alleen bestaande paletindexen gebruikt. De asserts bewijzen: groen-diff 0, gezichtslijnen-diff 0, rij 0–19 diff 0, geen nieuwe index en buiten de lijst diff 0.
Vel: `eindkeuring_vel.png`. Bovenaan op 8×: r19 | r18 | r17 | model_64. Daaronder op 2×/1×: dezelfde vier naast Gengar, Magcargo, Claydol en Forretress. Onderaan: de koeienvanger op 12× (r19 | r18 | r17 | model natief) en de kop op 8× (r19 | r18).

**Oordeel: PASS.** Ik zie r19 als eindversie voor Jordi. De twee open punten van r17 zijn opgelost. Een paar kleine dingen zijn nog te verbeteren: zie MAG.

## 1. Hoofdvraag
- **r18 vs r17 (1×/2× eerst): beter.**
  - Koeienvanger: in r17 las hij op 1× als een donkere vlek met grijze blokken. Nu leest hij als één puntige, getande kaak:
    - een doorlopende zwarte V-bovenrand met drie dalen (x8 y47, x14 y49 en x20 y48), zoals in Jordi's W-schets;
    - een lichte plaatrand die de V volgt;
    - naden die naar linksonder leunen (x9→8, x13→12, x18→17), de rechter als een ondiepe "<", zoals in Jordi's schets;
    - een middentand met een punt van 1 px op (15,56–57), met groen ernaast zoals in het model.
  - Kop: warmer en ronder dan r17. De bleekgrijze linkerhelft is weg en het licht valt linksboven (lichte platen, lichtbruin voorhoofd, donkerbruin rechts).
- **r19 vs r18: iets rustiger, niet slechter.** De lichtbruine vlek op de linkerwang was deels een vlek. De smalle lichtrand langs de buitenlijn (x3, y33–36) en de strook boven de grijns (y37) waren banding. De harde donkergrijze balk onder het linkeroog (11, model-toon midden) gaf een "wal" onder het oog. In r19 is dat weg. De diagonale wanglichtvlek onder het oog blijft: die geeft de bol.
- **Naast Gen 3:** drukker dan Gengar en Claydol, maar vergelijkbaar met Magcargo/Forretress. Dat volgt uit het model, dat zelf vol is. Op 1× lezen de kop met grijns, de kaak, de wielen en de geest.

## 2. Metingen (r17 → r18 → r19)
| | r17 | r18 | r19 |
|---|---|---|---|
| Kleuren | 13 | 14 | 14 (+ lichtbruin 14) |
| Eilandjes < 3 px ijzer/bruin (8-verbonden, y≥20) | 16 | 7 | 5 |
| Losse zwarte (< 3 px, y≥20) | 5 | 4 | 4 |
| Buitenlijn ijzer zwart | 56 % | 47 % | 47 % (Gen 3: 45–68 %) |
| Bijna-zwart totaal | 10,5 % | 9,7 % | 9,7 % |
| Licht linksboven | zwak | ja | ja |

- Bruin 14/8/9 heeft lum-stappen van 28 en 37 (goed).
- Pillow shading: nee. Banding: na de r19-fix alleen nog de voorhoofdwig x14–18 langs de plaatrand (MAG).

## MAG (geen blokkade)
- Plaattinten 7 en 10 verschillen maar 14 in lum (159/145). Daardoor lezen de lichte platen als bijna één tint. Dat zat er al zo in sinds r17.
- Er zijn nog een paar kleine eilandjes:
  - (6,52–53) roest 9 in de linker kaakplaat;
  - (10,50–51) 12;
  - (7–8,31) 11 bij de wenkbrauw;
  - (4,28) selout.
- De losse zwarte pixel (25,31) is bevroren (gezichtslijn). Die vraag aan Jordi staat nog open.
- Of het lichtbruin (14) Jordi's smaak is, beslist Jordi. Het is geen modelkleur maar een tint voor het volume.
