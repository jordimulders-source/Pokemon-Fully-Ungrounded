# Regionale Starmie r9: eindkeuring Dragonfly Cave op r8_A (27 nov)

**Eindoordeel: PASS.**
- Basis: r8_A, dus r7 (eindkeuring PASS) met de bovenste voorpunt 1 rij langer.
- 2 pixels gewijzigd. Palet ongewijzigd (16 kleuren incl. transparant).
- Silhouet: alpha-diff 0 tegen r8_A (assert in `bouw.py`). Niets getekend en niets gladgestreken.

Bouwen (vanuit `starmie/`): `python3 sprite_r9/bouw.py && python3 sprite_r9/vel.py`.

Inhoud van `vel.png`:
- bovenaan r9 | r8_A | r7 op 8×, met de wijziging blauw omkaderd;
- rechts een close-up van de bovenpunt op 12×: r9 | r8_A | model;
- onderaan 2× en 1× op wit en donker: r9, r8_A, r7, model, Gen 3 Starmie en de regionale Staryu.

Meetmaat: D = de modelhelderheid van alleen de koekcellen onder een spritepixel, uit het natieve r4-raster, zoals in r7. Mediaan van D per tint: 4 → 129, 5 → 166, 6 → 188.

## (a) Schaduw en volume

### Nieuwe bovenpunt (rij 4–8, x 27–33)
De handkleuring van de coördinator klopt met het model:
- **Rij 5:** 2 5 5 4 1, met D 137/157/168/133/113.
- **Rij 6:** 2 5 5 4 1, met D 160/169/178/145.

Het licht ligt links (5) en het donker rechts (4) tot aan de afgestompte tip. Het donkere vlak loopt als één diagonaal door: (31,5) (31,6) (32,7) (32,8) (33,9) (34,10) en verder. Het sluit aan op rij 6–9 zoals bij de Gen 3-tip (licht links, donker rechts, zie `anim_front_gba` rij 7–14).

### Wijziging: 2 px, 5 → 6 (glans)
De pixels zijn (28,8) met D 188 en (28,7) met D 181.
- Langs de binnenkant van de linkerlijn van de bovenarm loopt een glansstreep: (27,9) (26,11) (25,13) … (19–21,20). Die stopte op rij 9, terwijl de lichtste koekpixels van de tip hoger liggen. Nu loopt het licht door tot in de punt.
- Dit volgt de gids, r. 452–455: "lighter pixels on the inside of the outline".
- Rij 5–6 blijven 5/4, want D is daar ≤ 178 (dus geen 6).
- Geen band en geen pillow shading.

### Rest van de sprite
Geen nieuwe punten. De volume-oordelen van r7 gelden nog.

## (b) Belijning: 0 px
- **Bovenpunt:**
  - De toprij is 2 2 1. De linkerkant is outline base (28,5–6) en (27,7–8); de rechterkant is zwart (32,5–6) en (33,7).
  - Er is één wissel, op de hoek rechtsboven. Dat is hetzelfde patroon als de andere afgestompte punten in r7: rechterpunt rij 21 eindigt op 1, linkerpunt kolom 4 heeft eerst 2 en dan 1.
  - Ter info: de Gen 3 Starmie zet ook de hoekpixel rechtsboven van de toprij in de outline base. (31,4) in zwart is niet fout en volgt r7, dus ik heb hem laten staan.
- **Hele sprite, gemeten:**
  - De buitenrand bestaat alleen uit index 1 (117) en 2 (68). Er staat geen lichte kleur op de rand.
  - Er zijn geen losse wisselpixels: geen 1 tussen 2's of andersom.
  - Er is geen outline base aan de schaduwkant waar alleen onder of rechts transparant is.
  - Zwart waar alleen boven of links transparant is: (19,11), (4,23), (6,26), (11,32), (11,33), (26,51). Dat zijn alle schuine randen die naar beneden of rechts aflopen (schaduwkant van de punten). Het is hetzelfde als in r7 en niet fout.

## (c) Kleurtinten: 0 wijzigingen
Het palet van r7 blijft, met de koek gelijk aan de regionale Staryu, de hue shift in het paars en de stappen 33–35.
- De nieuwe tip gebruikt alleen bestaande tinten: 2, 4, 5, 6 en 1.
- Op 1× en 2×, op wit en op donker, leest de punt nu als een spitse top in plaats van een platte rand.
