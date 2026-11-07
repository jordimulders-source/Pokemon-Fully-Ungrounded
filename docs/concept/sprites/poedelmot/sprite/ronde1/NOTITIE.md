# Poedelmot sprite ronde 1 (6 nov): draft

Jordi: "Ga maar gewoon een sprite bouwen. Dan gaan we daar stukje bij beetje dingen in aanpassen". Later kwam erbij: "dat je er een gewoon een draft versie van maakt, wel in sprite en dat we dan geleidelijk aan alles beter maken", met de poten naar Giratina. Dit is die draft.

## Bestanden
- `raster.txt`: het met de hand getypte raster (een teken per pixel, hex-index, '.' = transparant). **Bron voor elke volgende ronde.**
- `teken.py`: maakt van raster.txt `anim_front.png` (64×64, geïndexeerd, 14 kleuren incl. transparant), `normal.pal` en `sprite_8x.png`.
- `controle.py` → `controle.txt`: alpha tegen silhouet ronde 3, clusters < 3 px, buitenrand, kleuren.
- `studie.py` → `studie.png`: Butterfree, Venomoth, Dustox, Beautifly, Swablu, Altaria, Whimsicott op 6×.
- `keurvel.png` + `keurvel.png.keuring.md`: naast de tak-foto, het vilt, Butterfree, Venomoth en Giratina.

## Wat er gedaan is
- **Basis:** silhouet ronde 3. **Verre voorvleugel** terug als kleine vleugel links naast het verre oor (x1–14, y16–27), niet tussen oor en kop.
- **Studie:** Butterfree: witte vleugel met aders van 1 px en donkere omlijning. Altaria en Swablu: wit met een warme grijze selout en schaduwbogen per wolpluk.
- **Palet:** wol 6/5/4/3 met selout 2 en zwart 1 aan de schaduwkant; vleugel crème 7/8 met adertjes 9; oren c/d/a met omlijning en strepen b. Geen roze of blauw.
- **Wol:** licht van linksboven, sikkelschaduw rechtsonder, plukbogen in de buik (lobben) en een plukje op het voorhoofd.
- **Ogen:** het oog van Emolga (x25–28, y22–26) pixel voor pixel overgenomen. Het nabije oog is volledig (4×5), het verre oog heeft drie kolommen. Er zit 2 px wol tussen. Geen neus.
- **Oren:** vilt-bladvorm, strepen loodrecht op de as.
- **Poten (Giratina):** opnieuw getekend en buiten de omtrek van ronde 3. De zes poten zijn dik, met dij, knievouw en pompon. Het voorpaar staat groot vooraan, het rechtse tweetal (midden en achter) staat dicht bij elkaar, naar buiten en hoger. Het linkse tweetal piept achter de verre voorpoot uit.

## Zwakke punten
Zie de keuring: de wol is glad in plaats van pluizig, de kop en het lijf lezen als een sneeuwpop, de aders zijn trapjes, de oorstrepen zijn grof, het linkse tweetal leest als een klont en de verre voorvleugel is klein. Er is nog geen onafhankelijke keurder geweest.
