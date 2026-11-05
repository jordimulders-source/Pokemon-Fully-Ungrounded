# Nachtaap fase 3: ronde 1f, opgeheven been naar rechts (varianten, 5 nov)

Jordi: "dit been komt midden uit het lichaam, maar zou een stukkie meer naar rechts moeten, 10 pixels misschien, misschien meer? zodat we het middenstuk van het lichaam zien en dit echt een been is" · "eigenlijk is het bovenste been het belangrijkste, dus laten we dat maar eerst goed krijgen" · "maak meerdere versies die geleidelijker naar rechts schuiven".

Basis: `../ronde1e/` (vijf reparaties + palm). Varianten `v3`, `v5`, `v7`, `v9`, `v11` (elk `nachtaap_fase3.png`, `normal.pal`, `raster.txt`), overzicht `vel_varianten.png` (1e = +0 en de vijf varianten op 3× en 1×, model ernaast). Bron: `bron/been.py` (`python3 been.py 3 5 7 9 11`), `bron/vel.py`.

## Wat er per variant gebeurt (zelfde regels, alleen s verschilt)
- **Been (rij 4–30):** het hele opgeheven been (want-voet, onderbeen, dij) is s px naar rechts verschoven, ongewijzigd van vorm, hoek, lengte en kleur. De oude plek is leeg.
- **Dijwortel/heup (rij 31–35):** de dijwortel schuift mee over de romp. Rechts is hij afgekapt op x43 met een K-rand, zodat er minstens 1 px lucht (x44) tot de spiraal (x45) blijft. Op rij 35 loopt de heup via een D-pixel over in de staartwortel.
- **Rug zichtbaar:** waar het been stond, loopt de romp door met een D-rugrand op rij 31 van de schouder naar de dij. De laatste s/3 kolommen vóór de dij liggen een rij hoger (ronde oksel). Onder de rugrand komt een lichtband (L, rij 32), want het licht valt van linksboven.
- Oude binnenomlijning van de vorige dijwortel is vacht geworden.
- **Staart:** 0 px diff (gecontroleerd op alle pixels van spiraal en staartwortel). Kop, maan, gezicht, hand, gloed, vuistarm en onderste been: niet aangeraakt.

## Telling (diff met 1e; afwijking silhouet ronde 1 is groot omdat het been verschuift)
| variant | px gewijzigd | open randen | korrel.py |
|---|---|---|---|
| v3 | 330 | 0 | 0 uitsteeksels, 0 tanden |
| v5 | 386 | 0 | 0 uitsteeksels, 0 tanden |
| v7 | 443 | 0 | 0 uitsteeksels, 1 tand (x44,y34: de lucht tussen heup en spiraal) |
| v9 | 462 | 0 | idem |
| v11 | 465 | 0 | idem |

De 26–33 "inkepingen" zijn de bewuste spiraalspleet van 1 px, en bij v7–v11 ook de lucht van 1 px tussen been/heup en spiraal.

## Eerlijk: wat nog niet af is (bewust minimaal; Jordi kiest eerst de verschuiving)
- **Rugrand:** de D-lijn op rij 31 is bij v9/v11 een rechte lijn van 6–8 px. Na de keuze maak ik er een boog van.
- **Heuprand bij v9/v11:** de rechterrand op x43 (rij 28–34) is recht en verticaal, omdat hij tegen de spiraal is afgekapt. Bij v11 is de dij daar smaller dan in het model.
- **Bil:** de bolling rechtsonder (staartwortel/onderste been) is nog die van 1d/1e. Die herzie ik pas als het been gekozen is, zodat heup, dij en bil één vorm worden (Jordi).
- **Licht:** de lichte vlekken van de oude dijwortel blijven op de romp staan en schuiven ook mee met de heup. Daardoor zijn de romp en de heup nog wat vlekkerig; dat komt in het volumewerk.
- **Vuistarm:** nog de oude (te dikke) arm, op Jordi's volgorde.
- Indruk op 1× (zelf gekeken): **v7–v9** laten het middenstuk van de rug het duidelijkst zien, zonder dat het been tegen de spiraal plakt. Bij v11 komt de voet dicht bij de spiraal en wordt de heup krap.
