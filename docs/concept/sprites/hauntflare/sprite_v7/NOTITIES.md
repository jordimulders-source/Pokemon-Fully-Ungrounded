# Hauntflare v7: gezicht (maker, 15 nov)

Uitgangspunt `../sprite_v6/hauntflare_v6.png`; alleen linkeroog en mond vervangen. Niets getekend: elke gezichtspixel komt uit het v6-rechteroog of uit Haunters Gen 3-mond, alleen gespiegeld, geschrapt of verschoven.

Reproduceren: `python3 kandidaten.py` (pngs) · `python3 meet.py` (controles) · `python3 vel.py` (vel.png). Bronnen: `gezicht.py` (v6-gezicht, bol uit `sprite_v2/stap1_kleur.npy`), `haunter_mond.py` (Haunters mond in ons palet).

## Linkeroog (gespiegeld v6-rechteroog, 12 kolommen breed)
Na spiegelen: kolom j0 = buitenkant (links), j11 = binnenhoek. Binnenhoek op (23,28), dezelfde rij als de binnenhoek van het rechteroog (27-28,28): samen één V-blik, 3 px neusrug ertussen.
- **Oog A**: kolommen j3, j5, j8, j10 geschrapt (12 -> 8). Eén pixel per wenkbrauwtrede weg, dus de trap blijft dicht; het oog wordt smaller en daardoor steiler (zoals Haunters en Gengars verre oog: smal en steil).
- **Oog C**: als A, plus rij 2 van de punt geschrapt: minder steil, de hoek ligt dichter bij die van het rechteroog.
- Pupil: in het gespiegelde oog stond de pupil aan de binnenkant (kijkt naar rechts). De twee pupilpixels (wit- en onderlidrij) zijn binnen het oog verschoven naar 1 px van de linker witrand, zodat de kijkrichting gelijk is aan het rechteroog (rechteroog: 2 wit | pupil | 4 wit; linkeroog: 1 wit | pupil | 2 wit).
- Afgevallen: oog B (7 kolommen, ook de buitenste witkolom weg): de punt verliest zijn onderlijn (open rand).

## Mond (Haunters eigen mondpixels, x15-33, y38-45)
Kleuren: zwart -> 1, Haunters donkerste huidtint (zachte mondhoek/onderlip) -> 2, magenta -> 10, roze tong -> 5 (of 10 bij `C_donker`); huid -> hoofdkleur op die plek = de V-tanden (boven: kolom x21-23 en x27; onder: x22 en x26).
Aanpassing aan dit lijf (bij Haunter zit de mond onderaan de kop, tegen de wang):
- Weg als lijf-specifiek: Haunters wangomtrek (15,38), (15-16,39), linker kaaklijn (19,44), kinomtrek (20,45), kinschaduw op rij 45 (behalve de onderlip x27-28).
- Verkort (verre, linker deel draait weg): kolommen x18 (hoektand-kolom) en x20 geschrapt, 17 -> 15 breed.
- **M1**: zo geplaatst: rechterkant op x35, bovenlip y31 = 4 px links en 1 px lager dan v6.
- **M2**: ook openingsrij y42 geschrapt (onderste helft van de bol draait weg, mond iets platter), daardoor 2 px lager dan v6 (boven y32, onderkant y38; y39 blijft bol boven de ring).

## Bol die vrijkomt
Uit `sprite_v2/stap1_kleur.npy` (oude linkeroog en mond); daardoor komt ook de glans boven het linkeroog terug. Opgeruimd (1 px eigen tint op een vrijgekomen plek -> buurtint): (23,27) 9->8, (38,31) 6->7.

## Controle (`meet.py`)
- Alle kandidaten: **diff buiten de gezichtszone 0**, silhouet 0, 15 kleuren + transparant (v6-palet), P-modus, transparantie index 0.
- Losse pixels die blijven: (22,22) en (23,25) zijn bevroren v6-bolpixels naast de nieuwe glans (staan nu als 1-px vlekje; buiten de zone, dus niet aangeraakt); (31,25), (29,26), (28,29) zaten al in v6 rond het rechteroog; (24,34) is een tand (hoort zo).

## Kandidaten
- `kandidaat_A.png`: oog A + M1, tong.
- `kandidaat_C.png`: oog C + M2, tong.
- `kandidaat_C_donker.png`: oog C + M2, opening helemaal donkerrood (zoals v6).

## Favoriet (eerlijk)
**C**: de hoek van het verre oog sluit het best aan bij het rechteroog (één boze blik, niet scheel), en M2 zit lager en platter, wat op de onderste helft van een bol klopt. De tong in donkerroze is hoe Haunter zijn mond bouwt (donkere band onder de tanden, lichte tong); zonder tong (C_donker) wordt de opening één zware vlek. Zwak punt: de linker mondhoek (Haunters kleine hoektand) leest op 12x als een klein kluwen; op 1x/6x valt het weg.
