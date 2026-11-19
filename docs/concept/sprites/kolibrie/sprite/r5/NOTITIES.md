# Soulibri r5: Jordi's vleugellijn in frame 2 netjes afgewerkt (19 nov)

**Jordi (letterlijk):** "voor zover ik het kan zien zijn de pixels waar ik zwart in heb getekend de buitenlijn van de vleugel" · "ja de lijn is correct, alleen je moet het wat netter afwerken, dat kan niet allemaal door 1 kleur vervangen worden, volg dragonflycave regels etc" · "A is een goede basis, maar moeten meer tinten" · "het moet heel subtiel kleurgebruik zijn, zodat die in een gif niet gek eruit ziet".

**Basis:** `r1/frame2.png`. De staartpixels uit r2 vervallen. Frame 1 is ongewijzigd (`frame1.png` = r1). Palet is `r1/normal.pal`. De plek van de lijn (21 px uit `r4/jordi_lijn.py`) staat vast.

**Tintkeuze:**
- De rand van dezelfde vleugel in frame 1 is 41× c (12) en 5× vleugellijn 4. De lijn blijft binnen die tinten, dus niet harder dan frame 1.
- Licht komt van linksboven. De bovenkant en de einden zijn c (12), dus taps en aansluitend op de bestaande vleugelrand.
- De hoek rechtsboven en de rechterkant (schaduwkant) zijn 4.
- Alleen waar de vleugel direct tegen de donkere staart ligt (2 px) is het 11, de A-tint.
- Geen 3 en geen zwart. Nergens wisselen twee tinten om en om; elke tint ligt als aaneengesloten stuk.
- De twee e-pixels 1 px binnen de 11-pixels zijn d geworden: een zachte schaduw. Frame 1 heeft d-banden in deze vleugel.
- De pixels van de lijn die al de juiste tint hadden (bovenkant c), zijn niet gewijzigd.

**Twee versies (open vraag):**
- **(a)** De pixels rechts van de lijn blijven ongewijzigd.
- **(b)** De vleugelpixels rechts van de lijn op y 17–21 (indices 4/11/12/13/14) zijn transparant, zoals de witte kier in het model. De staartrand aan de kier is dicht gemaakt (5 → 2). Let op: daarbij verdwijnt ook het donkere grijze plekje (4/11) bij y 20–21.

**Bestanden:**
- `frame2_a.png` en `frame2_b.png` (64×64, P, transparency=0)
- `anim_front_a.png` en `anim_front_b.png`
- `anim_a.gif` en `anim_b.gif` (frame 1 ↔ 2, 4×, 0,5 s per frame)
- `vel.png` (r1 | a | b: zone op 12×, geheel op 8× met de zone rood omkaderd, en 1× op licht en donker)
- Scripts: `lijn.py` en `vel.py`

**Diff:** het script bewijst met een assert dat er buiten de zone x 41–52, y 8–23 niets verandert (0 px), en dat het silhouet alleen verandert door de kierpixels in b.

## Per pixel: (x,y) oud → nieuw, reden

### a
variant a: 15 px gewijzigd t.o.v. r1/frame2.png, buiten zone x41-52 y8-23: 0
(47,10) 12 -> 4  hoek rechtsboven, overgang naar schaduwkant: 4
(48,10) 12 -> 4  hoek: 4
(48,11) 12 -> 4  rechterkant: 4
(49,11) 12 -> 4  buitenste hoekpixel: 4
(47,12) 14 -> 13  1 px binnen de lijn naast 11: e -> d, zachte schaduw (frame 1 heeft d-banden in deze vleugel)
(48,12) 4 -> 11  tegen de donkere staart: een tint donkerder, 11 (basis A)
(47,13) 14 -> 13  idem
(48,13) 13 -> 11  tegen de staart: 11
(47,14) 12 -> 4  staart wijkt: 4
(46,15) 12 -> 4  rechterkant (schaduwkant): 4
(46,16) 12 -> 4  rechterkant: 4
(46,17) 13 -> 4  rechterkant: 4
(45,18) 14 -> 12  binnenste van het dubbele stuk: c (lijn dunner)
(46,18) 14 -> 4  buitenste van het dubbele stuk: 4
(45,19) 14 -> 4  onderloop: 4

### b
variant b: 39 px gewijzigd t.o.v. r1/frame2.png, buiten zone x41-52 y8-23: 0
(47,10) 12 -> 4  hoek rechtsboven, overgang naar schaduwkant: 4
(48,10) 12 -> 4  hoek: 4
(48,11) 12 -> 4  rechterkant: 4
(49,11) 12 -> 4  buitenste hoekpixel: 4
(47,12) 14 -> 13  1 px binnen de lijn naast 11: e -> d, zachte schaduw (frame 1 heeft d-banden in deze vleugel)
(48,12) 4 -> 11  tegen de donkere staart: een tint donkerder, 11 (basis A)
(47,13) 14 -> 13  idem
(48,13) 13 -> 11  tegen de staart: 11
(47,14) 12 -> 4  staart wijkt: 4
(46,15) 12 -> 4  rechterkant (schaduwkant): 4
(46,16) 12 -> 4  rechterkant: 4
(46,17) 13 -> 4  rechterkant: 4
(47,17) 12 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(45,18) 14 -> 12  binnenste van het dubbele stuk: c (lijn dunner)
(46,18) 14 -> 4  buitenste van het dubbele stuk: 4
(47,18) 13 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(48,18) 12 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(50,18) 11 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(51,18) 5 -> 2  b: staartrand aan de kier dicht: 5 -> 2 (donkere rand)
(45,19) 14 -> 4  onderloop: 4
(46,19) 14 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(47,19) 13 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(48,19) 13 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(49,19) 12 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(50,19) 12 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(51,19) 5 -> 2  b: staartrand aan de kier dicht: 5 -> 2 (donkere rand)
(46,20) 4 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(47,20) 4 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(48,20) 11 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(49,20) 13 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(50,20) 13 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(51,20) 5 -> 2  b: staartrand aan de kier dicht: 5 -> 2 (donkere rand)
(44,21) 12 -> 4  b: buitenrand naar de kier: 4, taps naar c op (43,22)
(46,21) 4 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(47,21) 11 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(48,21) 11 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(49,21) 13 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(50,21) 13 -> 0  b: lichte vleugelpixel rechts van de lijn -> transparant (witte kier uit het model)
(51,21) 5 -> 2  b: staartrand aan de kier dicht: 5 -> 2 (donkere rand)
