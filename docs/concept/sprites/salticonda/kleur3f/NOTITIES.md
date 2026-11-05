# Salticonda – kleurronde 3f (laatste afwerking vanaf 3e)

Jordi (letterlijk): "3e is het beste, maar zorg nog dat de kop ook past bij het lichaam, qua shading en overgang, dan vind ik hem verder goed".

## Bestanden
- `salticonda.png` en `salticonda_raster.txt`.
- `vel.png` bevat:
  - kleur3e en kleur3f op 4× en 1×, op licht en donker;
  - een 8×-uitsnede van de overgang kop → halsband → bovenste winding.
- Scripts in `../scripts/`:
  - `kop3f.py`: de regels per zone.
  - `check_kleur3f.py`: het diff-bewijs.
  - `vel_kleur3f.py`: maakt het vel.

## Analyse: lijf tegen kop (3e)
- **Windingen:** licht van linksboven. Elke rij loopt van `b` via `c` en `d` naar een brede `e`-band. Die band beslaat het rechter ±40% van de winding.
- **Kop (3e):** de kuif was tot vlak bij de rechterrand `b`/`c`, met maar 1–2 px `d`/`e`. Daardoor oogde de kop lichter en vlakker dan het lijf, alsof er een ander licht op viel.
- **Bovenste winding:** die liep direct onder de halsband in hooglicht (`b`) door. Daardoor leek de kop erop geplakt.

## Wat er veranderde: 75 pixels, alleen tinten
| Zone | Pixels | Wat |
|---|---|---|
| Kop: schaduwkant van de kuif (rij 5–19) | 59 | Per rij vanaf 66% van de kopbreedte 1 tint donkerder, vanaf 86% nog een tint. Dezelfde tintenfamilie en stappen als op de windingen. |
| Overgang: slagschaduw op de bovenste winding | 16 | Rij 26, x 15–30, direct onder kaak en halsband, 1 tint donkerder. |
| Elders | 0 | |

- **Schaduwkant kop:** de schaduw gaat nu net zo diep als rechts op de windingen: `d` en dan `e` tot aan de omlijning. Zo loopt de kernschaduw met de ronding van de koepel mee.
- **Lichte bovenkant:** de koepel (rij 0–4) is bewust niet aangeraakt; die blijft licht, net als de bovenkant van elke winding.
- **Naden en omlijning:** de okernaden (`g`) en de omlijning zijn niet veranderd. De opstaande randen aan de schaduwkant schuiven één tint mee (`a`→`b`, `b`→`c`), zodat de textuur in de schaduw blijft lezen.
- **Slagschaduw:** links op de winding (x 13–14) blijft het hooglicht staan, want het licht komt van linksboven. Naar rechts loopt de schaduw over in de bestaande schaduwkant van de winding. De kop zit daardoor ín de kegel.

**Halsband en rechterkant:** daar heb ik bewust niets veranderd.
- De band volgt de ronding van de nek al: licht `q` met glans links, `s`/`t` rechts, en een onderrand die in het midden zakt.
- Rechts loopt het donkere band-eind (`t`/`d`) al zacht over in de rug van de winding (`e`). Daar zit geen harde naad tussen.
- Een pixel van de band veranderen zou een vormwijziging in de band zijn.

## Diff-bewijs (`python3 scripts/check_kleur3f.py`)
- **Alpha-diff met 3e:** 0, dus het silhouet is gelijk.
- **Gewijzigd:** 75 pixels, binnen het budget van ±80: 59 in de kop, 16 in de overgang, 0 elders.
- **Naden en omlijning:** 0 gewijzigd, dus de vorm en textuur van de kuif staan.
- **Bevroren delen:** neus, neusgaten, gezicht, oog, wenkbrauw, wang en halsband: 0 gewijzigd.
- **Palet:** gelijk; transparency 0.

## Eerlijk oordeel
- Op 4× naast elkaar valt het licht op kop en lijf nu hetzelfde: van linksboven, met dezelfde diepe schaduwkant rechts.
- De kop zit dankzij de slagschaduw in de kegel in plaats van erop.
- Het gezicht is ongewijzigd en oogt dus niet vreemder dan 3e.
- Ik zie geen open zwak punt.

## Lessen
- Een kop die bij het lijf moet passen, vergelijk je per rij op de verdeling van de tinten (welk deel van de breedte `d`/`e` is). Kijken naar losse kleuren zegt weinig.
- Een kleine slagschaduw (1 tint, 1 rij) direct onder halsband en kaak is genoeg om een kop in een lijf te laten zakken.
