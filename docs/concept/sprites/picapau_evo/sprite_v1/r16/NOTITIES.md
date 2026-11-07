# Picapau-evolutie: sprite r16 (twee kleine reparaties op r15)

Bron: `../r15/picapau_evo.png.keuring.md`. Alleen reparaties 1 en 2 zijn uitgevoerd. De optionele variant (bolle buitenrand van de voorrand) is niet gedaan. Het handwerk staat in `reparaties.txt`.

## Wat er veranderde (`diff_uitvoer.txt`: 5 px, 0 px buiten deze pixels)
1. **Kopstrook-restje:** (19,7), (18,8) en (19,8) waren lichtkastanje (1) en zijn nu kopbasis (2), zoals hun buren. De enige glans op de kop is nu die linksboven (x21-23, y3-5).
2. **Onderrand tussen de poten:** (20,39) en (21,39) waren zwart en zijn nu lijfkleur (2), dezelfde tint als de rij erboven.
   - Het lijf zakt in het midden 1 px tot op de tarsus en eindigt zo rond.
   - Het zwart blijft op (18-19,39) en (22,39); de rand is dicht.
   - Eerst geprobeerd met 3 (kastanjeschaduw). Dat gaf een tintvlakje van 2 px, dus het werd 2.

## Bevroren
- Slierten: 0 px.
- Snavel zelf (rij 9-13, 32 px): 0 px.
- (18,8) en (19,8) stonden in mijn P5-set uit `../r11/p5.txt` (rij 8, het voorhoofd boven de snavel). Ze zijn op verzoek van de keurder gewijzigd; daarom meldt de diff "snavel P5: 2 px".
- Omtrek: 0 px veranderd.

## Controle (`controle_uitvoer.txt`)
- Geen lichte kleur op de buitenrand.
- Geen losse pixels.
- Geen pixels die alleen diagonaal vastzitten.
- 15 kleuren + transparant.
- Eén tintcluster kleiner dan 3 px: G (19-20,11) in de bevroren snavel. Die was al bekend.

## Bestanden
- `picapau_evo.png`, `normal.pal`, `raster.txt`.
- `vel.png`: r16, r15, Pidgeot, Staraptor, Picapau en Raichu Gen 1 op 8×, met daaronder elk op 1× (licht en donker).
- Bouwen: `reparaties.txt`, `bouw_r16.py` en `platen.py`.
- Draaien: `python3.11 bouw_r16.py && python3.11 platen.py`.

## Zwak
- Niets nieuws. De punten die de keurder bij r15 acceptabel vond, gelden nog: kleine voeten op 1×, smal onderste stuk van de bliksem, dominante buik, rechte buitenrand van de voorrand.
- Nog niet opnieuw gekeurd.

Er is niets gecommit en niets verwijderd.
