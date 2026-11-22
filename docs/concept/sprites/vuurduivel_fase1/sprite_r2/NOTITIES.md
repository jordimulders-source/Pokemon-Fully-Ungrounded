# Vuurduivel fase 1, sprite r2

**Sprite:** `vuurduivel_r2.png` (64×64, 4-bit palet, 15 kleuren incl. transparant). 50 px hoog, ongewijzigd t.o.v. r1.
**Vel:** `vel.png` = r2 8× | r1 8× | model op dezelfde schaal; daaronder het gezicht van r2 op 12× naast het model; 1× op licht en donker.
**Script:** `wijzig_r2.py` (r1-raster + benoemde reparaties); elke pixel met reden in `wijzigingen_r2.txt`.

**Pixeldiff t.o.v. r1:** 28 pixels, allemaal binnen x16–28, y21–38 (ogen, hoorns, mond). Daarbuiten 0 (gemeten).

## Voorbeeldsprite voor de blik
Bestudeerd op 8×–16× (GBA-versies `anim_front_gba.png`): Gengar, Haunter, Sneasel, Nuzleaf, Banette, Sableye.
**Gekozen voorbeeld: Haunter.** Die heeft precies de blik van het model: wit oogwit als wig onder een dik, schuin zwart lid dat naar het midden van het gezicht zakt (de V), een kleine pupil in de binnenste onderhoek van het wit, en geen zwarte onderrand onder het oog. Het verre oog is smaller en blijft toch een wig met pupil.

## Wat er veranderd is (r1 → r2)
- **Linker (verre) oog, x15–19 y30–34, Haunter-techniek op de modelplek** (model: wit kol 33–36 en rij 65–68 = sx16–18 en sy32–34, pupil rechts):
  - lid schuin omlaag naar rechts: (15–17,31), (17,32), (18,32), (19,33); wenkbrauwpixel (17,30) uit het model blijft
  - oogwit 6 px: (16,32), (16–18,33), (16–17,34)
  - pupil (18,34) in de binnenste onderhoek, met wit erboven en links ervan, zodat hij niet in het lid opgaat
- **Rechter (nabije) oog, x23–29 y28–34** (model: wit sx25,5–28,5 en sy31,5–33, pupil linksonder, wenkbrauw (26,28)–(24,30)):
  - wenkbrauw (26,28), (25,29), (24,30) uit het model blijft
  - lid schuin omlaag naar links: (27–28,30), (25–26,31)
  - oogwit (27–28,31–33), plus een wit reepje (25,32) links van de pupil, zoals het model
  - pupil (26,32), (25–26,33) linksonder; linkerrand (24,32); onderrand y34 in donkere vlaktint
- **Mond:**
  - hoektand 2 px wit (24,36) en (24,37); de modeltand is ±2 natieve px, dus 1 sprite-px, maar 2 px zodat hij leest
  - donkere mondrand rechts gesloten: (25,36) en (26,38) zwart
  - de linkertand (20,37) blijft
- **Hoorns los van het haar:**
  - rechterhoorn: zwarte rand rondom tegen het haar (punt (26,21), links (25,22), (24,23), (24,24), rechts (27,22–24)), lichtstreep (26,22), (25,23), (25,24), voet in rood met donkerrode hoekjes (25,25), (27,25)
  - linkerhoorn: zwarte rand aan de haarkant (16,23), (17,24), (17,25), donkerrood aan de lichtkant (14,23), (14,24), (15,22), (15,25), lichtstreep (15,23), (15,24)

## Niet uit het model
- Het lid en de vorm van de oogwig volgen de Haunter-techniek (plek, maat en blik uit het model). De aparte wenkbrauw van het verre oog smelt daardoor samen met het lid (vel x15–18, y30–32).
- Hoektand 2 px in plaats van 1.
- Zwarte hoornrand aan de haarkant van beide hoorns: in het model staat daar zwart (rechterhoorn) of donkerrood (linkerhoorn). Hier overal zwart, zodat ze loskomen van het rode haar.

## Zelf gezien
- Op 1× lezen beide ogen nu als oogwit met pupil; het linkeroog valt niet weg.
- Het rechteroog is 2 px breed wit + het reepje; wit en pupil samen zijn 4 px breed, zoals het model.
