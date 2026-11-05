# Lama fase 2: kleur ronde 1b (maker-agent, 2 nov)

Drie punten terug van Claude: (1) de halsband las als sjerp (mijn eigen woord), (2) de aguayo las als een rechthoekig blok of koffer, (3) romp, dij en hals waren plat. De rest is bevroren: kop, oog, oren met kwast, handschoenen, poten, hoeven en palet. Het silhouet heeft alpha-diff 0.

## Werkwijze en bestanden
- `bron/raster.txt` (ronde 1, ongewijzigd) + **`bron/reparaties.txt`**: met de hand getypte rijen die alleen de drie zones overschrijven. `bouw.py` weigert pixels buiten het silhouet.
- Bouwen en controleren:
  ```
  python3 bron/bouw.py && python3 bron/controle.py && python3 bron/diff_r1.py && python3 bron/vel.py
  ```
- `lama.png` (P, 16 kleuren, transparency=0), `normal.pal` (ongewijzigd palet), `raster_grid.txt`, `vel.png` (ronde 1b op 4× licht en donker, ronde 1 op 4× ernaast, 1×, en op 3× en 1× naast de alpaca en 5 Gen 3-sprites), `bron/zoom_*.png` (8×).

## Bewijs
```
mode P transparency 0 | pixels 1188 | alpha-diff 0
kleuren gebruikt: 16
open randen: 0 []
gewijzigd per zone: {'romp/dij/hals': 167, 'halsband': 58, 'aguayo': 78} | buiten de zones: 0
```
Zones (`diff_r1.py`):
- de rijen 23–44, zonder de kin (r23 x≤15), de staart (r21–24 x≥50) en de voorpoten (r41–44 x≤34);
- daarbinnen: aguayo x36–47 r25–33, halsband x19–31 r26–31, de rest is romp/dij/hals.

Kop, oog, oren, handschoenen, poten, hoeven, staart en palet: **0 px gewijzigd**.

## 1. Halsband: een ring om de hals
- **Ring:**
  - De band zit nu hoger op de hals, waar de hals nog een eigen cilinder is (r26–29). Daar volgt hij als een **U** de ronding.
  - De voorkant hangt het laagst (x22–26, r28–29). Links (keel) loopt hij omhoog naar de rand en rechts stijgt hij naar r25–26, waar hij achter de hals verdwijnt (x31: rand k).
- **Smaller:** 2 rijen in plaats van 3:
  - bovenste rij in aguayo-blokjes van 2 px, teal, geel, rood (zoals het bandje van de alpaca);
  - onderste rij rood, met q vooraan in het licht en m achteraan in de schaduw;
  - randpixels m.
- **Pompons:** 5 (p, y, t, p, y) aan de onderkant van de U (x22, 24, 26 op r30, x28 op r29, x30 op r28), met slagschaduw (s) op de vacht ertussen.
- **Op 1×:** een gekleurde ring met belletjes aan de halsbasis, geen streep van schouder naar keel.

## 2. Aguayo: een doek over de ronde rug
- **Kleiner:** 11×8 in plaats van 13×10. De karamel vacht van rug en achterwerk blijft eromheen zichtbaar.
- **Bovenrand = ruglijn:** de zoom (m) loopt in de omtrek mee met de bruine rugrand (d), zonder zwart kader.
- **Strepen in de lengte van de rug:** roze, geel, blauw (2), rood.
- **Onderrand als boog:** de onderrand hangt in een boog over de flank (r29 → r32 in het midden → r29), zodat de strepen onderaan worden afgesneden zoals een doek die over een ton valt.
- **Licht en schaduw:**
  - lichte tinten bovenop; rood met q aan de lichtkant links;
  - naar rechts, waar de doek wegbuigt, n/m/d;
  - zwart (k) alleen aan de schaduwkant: de rechterhoek en de zoomhoeken rechts;
  - links is de rand gekleurd (m).
- **Slagschaduw:** s op de vacht direct onder de zoom.

## 3. Volume
- **Hals als cilinder:** de lichtkant links (l, één h), het midden b, de schaduwkant rechts (s), de rand d/k. Onder de kaak een slagschaduw.
- **Romp:**
  - een lichte rugzone rechts van de doek (l op het achterwerk);
  - een schouderbol met een licht vlak linksboven (l, x28–31 r31–33);
  - een rustige flank in b;
  - daaronder een **kernschaduw** die de ronde buik volgt: s vanaf r36–37, een donkere band d op r39 (gekarteld met s), en onderaan s als teruggekaatst licht met de k-rand;
  - het achterwerk met de schaduwkant rechts (s/d).
- **Dij als bol:** het hooglicht linksboven (l/h, x46–48 r40–42), b eronder, de schaduw naar achteren en onder (s, k-rand); de verre dij in s/d.
- Grote vlakken. De wolplukken in de omtrek blijven (silhouet bevroren). Losse pixels alleen bij bewuste details: pompons, oogglans, nagels, enkele hooglichtjes.

## Eigen keuring (4×, 3× en 1× naast ronde 1, Stantler en Ponyta)
- Halsband: leest als ring met pompons. Hij zit hoger dan in de onderlaag; dat is een bewuste keuze, omdat de halsbasis in de onderlaag samenvalt met borst en schouder, zodat elke band daar schuin oogt.
- Aguayo: leest als een kleine gestreepte doek met een hangende onderrand, niet meer als koffer.
- Romp, dij en hals: duidelijk ronder dan in ronde 1 (buik, schouder, dij, hals).
- Ik zie geen zelfgenoemd zwak punt dat nog gerepareerd moet worden.

## Lessen
- Een halsband op een schuine hals leest als sjerp zolang hij op de halsbasis zit, waar hals en borst samenvallen. Zet hem waar de hals nog een eigen cilinder is en teken een korte U met beide uiteinden omhoog.
- Een doek met omlijning rondom en hangende hoeken leest als een koffer. Laat de bovenrand opgaan in de ruglijn, maak de onderrand een boog en schaduw alleen aan de kant waar de doek wegbuigt.
- Kernschaduw met de beperkte vachtramp: s → d-band (gekarteld) → s als teruggekaatst licht → k-rand. Zo wordt de buik rond zonder een extra kleur.
- Een reparatielaag (`reparaties.txt`) over het oude raster plus een diff per zone maakt "de rest pixel voor pixel gelijk" vanzelf bewijsbaar.
