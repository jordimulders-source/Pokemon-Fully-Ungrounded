# Salticonda – kleurronde 3d (vanaf kleur3: kuif groter, niet breder)

Jordi (letterlijk): "nee de kuif is breder, niet groter. Tot nu toe heeft de linkse veruit de beste kuif en de beste neus, die neus bij de andere twee is heel raar". Over de textuur van 3b: "textuur prima". 3b en 3c zijn afgekeurd voor de vorm van de kuif en de neus.

## Bestanden
- `salticonda.png` en `salticonda_raster.txt`.
- `vel.png`: kleur3 en kleur3d, koppen op 9× (op dezelfde hoogte uitgelijnd) en het geheel op 4× en 1×, op licht en donker.
- Scripts in `../scripts/`:
  - `kop_kleur3d.py`: verschuiving, kuifsilhouet en de kuif met de hand per rij.
  - `check_kleur3d.py`: het diff-bewijs.
  - `kuifmaat.py`: de kuifmaten.
  - `vel_kleur3d.py`: maakt het vel.

## Werkwijze
1. **Verschuiving:** de hele sprite van kleur3 gaat 3 px omlaag. Kleur3 liep van rij 0 tot 60, nu loopt hij van rij 3 tot 63.
2. **Silhouet:** het kuifsilhouet van kleur3 is geschaald met 1,2× om het ankerpunt (16,10): de voorkant van de kuif, op ooghoogte.
   - Boven het oog schaalt het in beide richtingen, dus de koepel groeit vooral omhoog.
   - Onder het oog schaalt alleen de breedte, aflopend naar 1,08×, zodat de achterkant niet uitdijt.
   - Daarna is de achterkant met de hand 2–3 px ingekort. Met de volle 1,2× uitbouw werd hij 1,48× (te veel en te breed).
   - De vorm blijft die van kleur3: twee toppen met een dip ertussen, de voorrand boven het voorhoofd en de ronde achterkant.
3. **Textuur:** de kuif is met de hand ingekleurd met de zouttextuur van 3b:
   - okernaden op de plekken van de kleur3-naden;
   - een zijtak met een Y op de voorste plaat;
   - een Y achterboven en een Y onderaan de achterkant;
   - lichte opstaande randen en korrels.
4. **Bevroren:** de neus en het snuitfront (met de neusgaten van kleur3), gezicht, oog, wenkbrauw, wang, halsband en lijf zijn kleur3, alleen verschoven. De neus van 3b en 3c is niet gebruikt.

## Kuifmaat (`python3 scripts/kuifmaat.py`)
Dit is hetzelfde masker als eerder, met de voorrand vanaf x 12. Bij 3d schuift het masker 3 rijen mee.

| Versie | Oppervlak | Breedte | Hoogte | Koepel boven de wenkbrauwboog |
|---|---|---|---|---|
| kleur3 | 309 px | 31 (x 13–43) | 20 (vanaf rij 0) | 5 rijen |
| **kleur3d** | **407 px (1,32×)** | **34 (1,10×)** | **22 (1,10×), vanaf rij 1** | **7 rijen (1,4×)** |

- De groei zit vooral in de hoogte: de koepel boven het oog is 1,4× hoger.
- De breedte groeit maar 1,10×. Ter vergelijking: 3c groeide 1,23× in de breedte en 0,95× in de hoogte.
- **Totaal oppervlak:** 1,32×, net boven de gevraagde 1,2–1,3×. Ik heb het zo gelaten omdat bij verder inkorten de koepel weer smaller zou worden dan hij hoog is.

## Diff-bewijs (`python3 scripts/check_kleur3d.py`)
- **Niet-kuifpixels van kleur3** (neus, snuit, gezicht, oog, wenkbrauw, wang, halsband, lijf): 2269.
  - Anders na 3 px verschuiving: **0**.
  - Waarvan halsband en lijf (1868 px): 0 anders.
- Er komen geen pixels onder de kuif bij die niet uit kleur3 komen.
- Rij 0 is leeg (1 px lucht) en de onderste rij is 63.
- Palet gelijk aan kleur3, transparency 0, 0 open randen.

## Checklist
| Punt | Oordeel |
|---|---|
| Kuif groter, niet breder | ok. Hoogte en koepel groeien meer dan de breedte. |
| Zelfde vorm als kleur3 | ok. Twee toppen met dip, voorrand boven het voorhoofd, ronde achterkant. |
| Neus en snuitfront = kleur3 | ok (0 verschil na verschuiving). |
| Textuur van 3b | ok. Okernaden, opstaande randen, korrels; geen zwart, geen kubussen. |
| Lijf alleen verschoven | ok (0). |
| 1 px lucht boven | ok. |

## Eerlijk oordeel
- Naast kleur3 leest de kuif als dezelfde kuif, alleen groter. Vooral de koepel boven het oog is hoger, hij is niet uitgebouwd naar achteren.
- De neus en het gezicht zijn die van kleur3.
- Ik zie geen open zwak punt.

## Lessen
- **Groter, niet breder:** "groter" betekent schalen om een anker in alle richtingen, met dezelfde vorm. Een kraag aan de achterkant leest als breder (3c).
- **Ruimte maken:** bij een kop die tegen de bovenrand zit, maak je ruimte door het hele sprite omlaag te schuiven als er onderaan lege rijen zijn. Bewijs met een diff dat het lijf alleen verschoven is.
- **Maat bijhouden:** meet na elke stap met hetzelfde masker. De eerste uitbouw kwam uit op 1,48×, ver boven de opdracht.
