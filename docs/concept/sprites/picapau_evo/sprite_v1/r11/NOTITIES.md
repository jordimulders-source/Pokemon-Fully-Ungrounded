# Picapau-evolutie: sprite r11 (op probeersel P5)

## Jordi letterlijk
- Over de probeersels: **"p5 is de enige die er oke uit ziet, ga daar maar mee verder. Ik ben nog steeds niet tevreden met de slierten op het hoofd overigens, die moeten beiden ongeveer uit dezelfde plek komen en netjes langs elkaar hangen zoals de raichu oren op de gen 1 sprite"**
- Aanvulling: **"en ja ze mogen overlappen"**. De regel "1–2 px tussenruimte, niet kruisen" vervalt dus. Waar ze overlappen ligt de nabije spriet vóór de verre, en de verre blijft zichtbaar waar hij uitsteekt.
- Eerder: zie `../r7/NOTITIES.md` t/m `../probeersels/NOTITIES.md`.

## Bevroren
- De snavel van P5 is goedgekeurd en bevroren.
- `diff_uitvoer.txt`: **0 px verschil met P5 buiten de zones** krullen (x14-46, y0-16) en verre vleugel (x8-18, y7-17).
- De snavelpixels staan niet in de diff.

## Raichu Gen 1, de oren (close-up van `referenties/jordi_inspiratie_raichu_gen1.png`)
- Beide oren komen van ongeveer hetzelfde punt bovenop/achter op de kop. De zwarte massa's raken elkaar daar en vormen samen één voet.
- Ze lopen naast elkaar, vrijwel evenwijdig, schuin naar achteren-rechts.
  - Het verre oor ligt hoger en loopt langs de bovenkant naar rechts.
  - Het nabije oor ligt er direct onder en zakt iets meer.
  - Ze worden alleen gescheiden door een dunne lichte rand; op sommige plekken overlappen ze.
- Elk oor heeft een lichte binnenkant. De punt krult om in een zwarte krul. De krul van het nabije oor ligt lager dan die van het verre oor.
- De voeten zijn breed, de punten smal.

## Wat r11 doet
1. **Slierten:**
   - **Voet**: één gemeenschappelijke voet op de achterkruin. Verre (26-27,2) en nabije (28,3) raken elkaar schuin.
   - **Verre spriet**: een boog over de kruin (rij 1-4) die met 1 rij per 3 px naar achteren zakt en eindigt in een spiraal met gat (x40-45, rij 4-10).
   - **Nabije spriet**:
     - begint 2 rijen lager, evenwijdig vanaf dezelfde voet;
     - zakt sneller en krult eerder, in een spiraal met gat (x33-38, rij 8-14), onder de verre door;
     - de twee raken elkaar alleen bij de voet en kruisen niet.
   - Geen recht stuk langs de bovenrand van het beeld; de oude oren van r9/P5 zijn weg.
2. **Verre vleugel:**
   - **Boven de snavel**: de waaier eindigt in twee veerpunten (pen 1 tot rij 9, pen 2 tot rij 10 tegen de snavel), met de kleuren van de rest van de waaier (k/3/v/4). De rechte zwarte afsluitlijn van P5 op rij 9 is weg.
   - **De vleugelwortel onder de keel** heeft weer een bovenrand (k op rij 13-14).

## Werkwijze
- `bouw_r11.py`:
  - leest `../probeersels/P5.png`;
  - wist de oude oren (`oude_oren.txt`, uit `r9/kop.txt`);
  - zet `wijzigingen.txt` erop (met de hand);
  - maakt `raster.txt`, `picapau_evo.png` en `normal.pal`;
  - draait `controle.py` en de diff.
- `platen.py` maakt `vel.png`: boven de kop op 8× van r11, P5 en Raichu Gen 1; onder de hele sprite op 1× en 8×.
- Draaien: `python3.11 bouw_r11.py && python3.11 platen.py`

## Controle (`controle_uitvoer.txt`)
- Geen lichte kleur op de buitenrand.
- Geen losse pixels.
- 15 kleuren + transparant.
- Eén tintcluster kleiner dan 3 px: G (19-20,11). Die zit in de bevroren P5-snavel en is niet aangeraakt.

## Eerlijke zwakke punten
1. **Geen binnenkant.** De sprieten zijn zwarte lijnen van 1 px, zonder lichte binnenkant zoals de Raichu-oren. Ze lezen als twee gekrulde sprieten (slierten), niet als brede oren. Een lichte binnenkant kan ik toevoegen als Jordi dat wil.
2. **Verre spriet.** Hij loopt in trapjes van 3 px (rij 1 → 4). Het laatste stuk op rij 4 (x37-43) is samen met de bovenkant van de spiraal 7 px recht.
3. **Ze overlappen niet.** De sprieten raken elkaar alleen bij de voet. Overlappen mag nu ("en ja ze mogen overlappen"), maar dat heb ik nog niet gebruikt. Gaan ze dichter op elkaar, dan leest het meer als Raichu.
4. **Nabije spiraal.** Die hangt vrij laag (tot rij 14), naast de achterkop en vlak boven de top van de nabije vleugel.
5. **Vleugelwortel.** De nieuwe bovenrand onder de keel is klein en recht (4 px). Op 8× zie je een klein zwart hoekje tussen keel en snavel.
6. **Niet gekeurd.** Er is nog geen onafhankelijke keuring gedaan.

Er is niets gecommit en niets verwijderd.
