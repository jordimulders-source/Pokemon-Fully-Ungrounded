# Picapau-evolutie: sprite r12 (alleen de slierten, op r11)

## Jordi letterlijk
- **"p5 is de enige die er oke uit ziet, ga daar maar mee verder. Ik ben nog steeds niet tevreden met de slierten op het hoofd overigens, die moeten beiden ongeveer uit dezelfde plek komen en netjes langs elkaar hangen zoals de raichu oren op de gen 1 sprite"**
- **"en ja ze mogen overlappen"**

## Coördinator over r11
De slierten waren trapjeslijnen die als rommelige draad lazen. Daarom:
- 2 px dik;
- dicht op elkaar en deels overlappend (de nabije vóór de verre);
- hangend in één gladde boog met een spiraal onderaan;
- de verre spiraal hoger en verder naar rechts;
- trapjes in een vaste reeks en geen rechte stukken langer dan 3 px.

## Wat r12 doet (`slierten.txt`, met de hand)
- **Dikte en kleur**: beide sprieten zijn 2 px dik, met donkerste bruin (4) aan de lichte kant (boven/links) en zwart (k) aan de schaduwkant (onder/rechts).
- **Voet**: één gemeenschappelijke voet op de achterkruin (x26-29, rij 1-3).
  - De nabije ligt direct onder en vóór de verre.
  - Daar liggen ze tegen elkaar (4-k-4-k) en lezen ze samen als één pluk.
  - Daarna wijken ze uiteen.
- **Verre spriet**:
  - na een korte top op rij 0 hangt hij in trapjes 3-3-3-3-2 naar achteren-omlaag;
  - hij rolt rechtsom in een spiraal met gat, rechtsboven (x41-46, rij 5-10).
- **Nabije spriet**:
  - zakt sneller, in trapjes 3-3-2-1-1-1;
  - komt rechts omlaag en rolt naar links en omhoog naar binnen, in een spiraal met gat linksonder (x34-39, rij 8-13).
- De spiralen liggen schuin boven elkaar en raken elkaar niet. Er loopt niets meer langs de bovenrand behalve de top van 3 px.

## Bevroren: bewijs
- `diff_uitvoer.txt`: **0 px verschil met r11 buiten de zone slierten** (x24-46, y0-14).
- De snavel (P5) en de verre vleugel van r11 zijn ongewijzigd.

## Controle (`controle_uitvoer.txt`)
- Geen lichte kleur op de buitenrand.
- Geen losse pixels.
- Geen alleen-diagonale verbindingen.
- 15 kleuren + transparant.
- Eén tintcluster kleiner dan 3 px: G (19-20,11) in de bevroren P5-snavel.

## Bestanden
- `picapau_evo.png`, `normal.pal` en `raster.txt`.
- `slierten.txt`.
- `bouw_r12.py` (r11 zonder slierten + `slierten.txt`, controle en diff).
- `platen.py` → `vel.png`: kop op 8× van r12, r11 en Raichu Gen 1, met daaronder de hele sprite op 1×.
- Draaien: `python3.11 bouw_r12.py && python3.11 platen.py`

## Eerlijke zwakke punten
1. **Spiralen.** Op 6×6 met een lijn van 2 px is het gat klein (2×2 tot 3×2) en open naar één kant. Op 1× lezen ze meer als een haak of "6" dan als een volle spiraal.
2. **Rechte stukken.**
   - De bovenkant van de verre spiraal is 4 px recht (rij 5), en de rechtse zijde van de nabije spiraal 4 px (x38-39, rij 8-11).
   - Dat is 1 px langer dan de regel van maximaal 3.
   - De trapjes van de verre spriet zijn 3-3-3-3-2: een gelijkmatige helling, nog geen echt versnellende boog.
3. **Kleur.** Ze zijn bruin en zwart, zonder lichte binnenkant zoals de Raichu-oren. Ze lezen als donkere sprieten.
4. **Overlap.** Die zit alleen bij de voet; verder lopen ze naast elkaar met 1 px ertussen.
5. **Rand van het beeld.** De verre spiraal reikt tot x46. Dat is ruim binnen het beeld, maar dicht bij de vleugelpunt rechtsboven.
6. **Niet gekeurd.** Er is nog geen onafhankelijke keuring gedaan.

Er is niets gecommit en niets verwijderd.
