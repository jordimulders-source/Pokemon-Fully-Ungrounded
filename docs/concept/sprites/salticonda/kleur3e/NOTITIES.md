# Salticonda – kleurronde 3e (kleur3, alleen de kuiftextuur)

Jordi (letterlijk): "maak maar een versie van 3 waar je de vorm niet aanpast, maar alleen de textuur van de kuif".

## Bestanden
- `salticonda.png` en `salticonda_raster.txt`.
- `vel.png`: kleur3 en kleur3e, koppen op 9× en het geheel op 4× en 1×, op licht en donker.
- Scripts in `../scripts/`:
  - `kop3e.py`: per rij de met de hand gezette textuurpixels.
  - `check_kleur3e.py`: het diff-bewijs.
  - `vel_kleur3e.py`: maakt het vel.

## Wat er veranderde
Alleen pixels **binnen** de kuif (niet de omlijning) zijn veranderd: 66 in totaal. Daar zit nu de zouttextuur van 3b:
- **Naden:** de bestaande naden van kleur3 zijn okernaden (`g`) geworden, op dezelfde plek:
  - de naad uit de kuifdip naar de wenkbrauw;
  - de achternaad;
  - de lange naad achter de wang.
- **Nieuwe naden:**
  - een naad aan de rechterkant, van de bovenrand naar de wenkbrauwhoek, met een zijtak naar de achterrand: Y op (35,6);
  - een tak van de achternaad naar de rand: Y op (38,15).
- **Opstaande randen:** lichte randen (`a`/`b`) aan de lichtkant van elke naad en schaduw (`c`/`d`) aan de andere kant.
- **Korrels:** een paar lichte korrels (`a` tussen `b`) op de bovenranden.
- **Achterkant:** het afwisselende c/d-patroon is een rustige overloop c → d → e geworden.

## Diff-bewijs (`python3 scripts/check_kleur3e.py`)
- **Alpha-diff met kleur3:** 0, dus de vorm is exact dezelfde.
- **Gewijzigd:** 66 pixels, allemaal in het kuifinterieur.
- **Buiten het kuifinterieur:** 0. Neus, snuit, oog, wenkbrauw, wang, halsband en lijf zijn dus pixel voor pixel kleur3.
- **Omlijning:** 0 pixels gewijzigd.
- **Palet:** gelijk; transparency 0. Open randen: 0.

## Oordeel
- Het is dezelfde kop als kleur3, maar de kuif leest nu als zoutkorst met platen.
- De textuur blijft op 1× rustig.
- Ik zie geen open zwak punt.
