# Silicobra (Uyuni) – ronde 6 (vanaf 5A)

Jordi (letterlijk): "dat bedoelde ik niet met kuiflijn, ik bedoelde het hoofd zoals bij de originele silicobra, maar dan met een iets zachtere lijn. 5a is momenteel het beste maar de halsband mag nog wat groter aan de bovenkant, aan de onderkant prima"

Bestanden:
- `silicobra_uyuni.png`: 64×64, geïndexeerd, palet van ronde 2/4/5, 15 kleuren, transparency=0.
- `silicobra_uyuni_raster.txt`: de bron.
- `scripts/handwerk.py`: de met de hand gezette pixels op 5A.
- `scripts/bouw.py`, `scripts/controle.py` (met overlay tegen het origineel), `scripts/vel.py`.
- `vel.png`: origineel, 5A en ronde 6 op 4× en 1×, licht en donker; onderaan het gezicht op 8×, origineel naast ronde 6.

## 1. Gezichtslijn zoals in het origineel, zachter
- **Loop:** precies die van de lijn in het origineel (index 3/2 tussen gezicht en achterkop):
  - bovenkant rij 17 x=21–25;
  - rij 18 x=26–27;
  - via de bovenkant van de oogrand (rij 19, die er al lag);
  - (30,20) en (31,21);
  - langs de wang x=32 op rij 22–26;
  - (31,27), (31,28) en (30,29) naar de kaak.
- **Dikte:** 1 px, zonder hoekige trapjes. Het is dezelfde boog als in het origineel.
- **Kleur:** zachter dan de buitenomlijning:
  - bovenkant in middentint grijs-oker `e` (146,128,104), lichter dan de rand `h` daarnaast;
  - zijkant en kaak in `h` (124,108,90), nog steeds duidelijk lichter dan de donkere buitenrand `O` aan die kant.
  - Op (31,27), (31,28) en (30,29) lag in 5A een donkere lijn (`K`/`O`), net als in het origineel (index 2/A); ook die is nu zachter.
- **Wang:** zoals in het origineel (index 6) zit tussen oogring en lijn weer een smalle strook gezichtskleur (`f`): (31,22), (31,25) en (31,26). Daardoor leest het gezicht als een eigen ronde vorm onder de kuif.
- **Ongemoeid:** oog en oogrand, snuit, silhouet en het barstpatroon verder weg.

Overlay-bewijs (`controle.py`): elke gewijzigde kop-pixel valt in het origineel op index 3, 2 of A (lijn) of 6 (wang).

## 2. Halsband aan de bovenkant groter
- **Bovenrand:** loopt nog 1–2 px hoger dan in 5A: x=18–27 op rij 33, het midden x=28–31 op rij 34, x=32–33 op rij 33 en rechts x=34–39 op rij 32.
- **Kin en kop:** links ligt de band nu direct onder de kinlijn; verder naar rechts onder de kaak en de achterkop.
- **Glans:** de glans volgt de nieuwe bovenrand.
- **Ongewijzigd:** de belletjes, de onderkant (rij 36 en lager is identiek aan 5A) en het silhouet (0 alpha).

## Diff t.o.v. 5A
| Zone | Alpha | Kleur |
|---|---|---|
| Gezichtslijn en wang (kop) | 0 | 19 |
| Bovenkant band (rij 31–35) | 0 | 19 |
| Rest (incl. onderkant band, oog, snuit, voet, krul) | 0 | 0 |

Open randen 0, losse pixels 0.

## Eerlijk oordeel
- Het gezicht leest weer als een eigen vorm, zoals bij de originele Silicobra, met een zachte lijn die niet hard of zwart oogt. Dat is het best te zien op 4× en 8×; op 1× is het subtiel, net als in het origineel.
- De band zit voller onder kin en kop, en de onderkant is zoals Jordi hem goedkeurde.
- Zelf zie ik geen open zwak punt.

## Lessen
- "Een lijn zoals het origineel" betekent: dezelfde loop als de grens in de basis (hier index 3/2 tussen gezicht en achterkop), niet een nieuwe lijn langs de kuif. Bij twijfel de basis als overlay nemen en per pixel de index noemen.
- Een grenslijn tussen twee lichte vlakken leest pas als de ene kant ook zijn eigen kleur terugkrijgt (hier de beige wangstrook).
