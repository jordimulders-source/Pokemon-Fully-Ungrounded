# Lama fase 2: kleur ronde 3 (maker-agent, 2 nov)

Jordi over 2c (letterlijk): "de vacht is idd te klonterig. Daarnaast lijkt die nu iets te volwassen denk ik?"
Deze ronde behandelt het eerste punt. Voor "te volwassen" zie `../../silhouet/variant_jonger/`.

## Opdracht
- De wol wordt één zachte massa:
  - rustige grote vlakken, licht linksboven;
  - een kernschaduw die de vorm volgt;
  - teruggekaatst licht.
- De wolligheid komt uit de omtrek. Binnenin hooguit 2–3 zachte plukken, zonder ronde klonten met een eigen schaduwrand.
- Silhouet ronde 2 en het palet blijven.

## Bestanden
- `lama.png`, `normal.pal` (= 2c), `raster_grid.txt`.
- `vel.png`:
  - rij 1: ronde 3 op 4× (licht en donker), met 2c ernaast;
  - daaronder op 3× en op 1×: ronde 3, 2c, de alpaca, Mareep, Flaaffy en Altaria.
- `bron/wol.txt`: **de enige overlay, met de hand getypt** (`rij x0 pixels`) op het raster van 2c.
- `bron/bouw.py`, `controle.py`, `zoom.py`, `vel.py`: alleen bouwen, controleren en kijken.

## Controles
```
mode P transparency 0 | pixels 1278 | alpha-diff 0 (silhouet/ronde2.txt)
kleuren 16 | palet = 2c | open randen 0
diff t.o.v. 2c: 115 px, allemaal vachtletters in y16-39 (hals, borst, rug, romp)
kleding, omlijning, kop, oog en poten: 0 px
```
Vacht over de hele sprite: s 30% | b 24% | l 23% | d 20% | h 2%.

## Wat er gebeurde
- **Hals:** één cilinder.
  - De kernschaduw onder de kin (s, links) blijft.
  - Het licht ligt links-midden (l), daarna komt b en rechts s tegen de rand.
  - De plukranden uit 2b (s-bogen) zijn weg.
  - Zachte plukken: bovenaan (22–23,16–17), al aanwezig, en op de hals (21,22), elk een h in l, zonder rand.
- **Borst, rug en schouder:**
  - De borst binnen de halsband is l/b.
  - De rug tussen halsband en aguayo is één l-vlak met een s-schaduw direct achter de band.
  - Schouderpluk (21–23,32–33): h in l.
- **Romp:**
  - Het licht vult de schouder en de voorkant van de borst. De grens tussen l en b loopt diagonaal (y32 tot x34, y33 tot x31, y34 tot x30, y35 tot x27, y36 tot x24).
  - Het midden is één rustig b-vlak.
  - De kernschaduw s wordt naar rechts dikker: y36 vanaf x44, y37 vanaf x36, y38 vanaf x24.
  - Teruggekaatst licht in b onder de buik: (35–39,38) en (36–38,39).
- **Achterwerk:** l bovenaan links, s aan de rechterrand (zoals in 2c), zonder klontrand.
- **Weg:** de klonten A–D, de schulpranden en de franjetongen uit 2c.

## Eigen keuring
Bekeken op 12×, 4×, 3× en 1×, op licht en donker, naast 2c, Mareep, Flaaffy en Altaria.
- Binnenin is de wol rustig, net als bij Mareep en Altaria: licht linksboven, schaduw onderaan, en de textuur in de omtrek.
- Op 1× leest het als één zacht wollig lijf. "Klonterig" is weg.

Wat eerlijk nog niet (helemaal) werkt:
- **Kernschaduw:** de bovengrens loopt in drie stappen (x44, x36, x24). Op 4× zie je een trap, op 1× een zachte buik. Met maar drie rijen buik kan het niet vloeiender zonder dithering.
- **Flank:** het midden (x28–46, y34–36) is een groot effen b-vlak. Dat is bewust en past bij de opdracht, maar het kan als "leeg" ogen naast Altaria. Een extra pluk daar zou weer naar klonten gaan.
- **"Te volwassen":** dat zit niet in de kleur maar in de verhoudingen; zie de silhouetvariant.

## Lessen
- Wol op een sprite van 64 px: de textuur hoort in de omtrek. Binnenin werken alleen grote vlakken met één of twee h-stippen. Elke schaduwrand binnenin leest als klont of schulp.
- Een kernschaduw op een smalle buik wordt een trap. Laat de stappen naar de schaduwkant (rechts) korter worden, dan volgt hij de ronding.
