# Pitahaya-draak fase 3, sprite r9 (maker): keurderpunten op r8

- **Basis:** `../sprite_r8/pitahaya3_r8.png`. Het palet is ongewijzigd.
- **Script:** `python3 maak_r9.py` schrijft `pitahaya3_r9.png` en `pitahaya3_r9_afwijkingen.txt`. Elke pixel heeft een assert op de oude kleur.
- **Vel:** `python3 vel.py <tijdelijke map>` maakt het vel: r9 | r8 | model op 8×, close-ups op 12× (knots + schutblad, staart, scheen + verre been), en 1× en 2× naast Salamence, Tyranitar en Sceptile.

## Controle
- 128 px t.o.v. r8.
- Silhouet: alfa-diff 0 t.o.v. r8.
- Kop (x 0-20, y 12-30) pixelgelijk aan r8. De bek is pixelgelijk aan r6 zonder tong, de buikzone aan r6 buik.
- 14 kleuren incl. transparant.

## Per punt (px)
| punt | px | wat |
|---|---|---|
| 1 schutblad beenzijde | 6 | Taps blad: voet (26-28,51) h h G, dan (27,52) h + (28,52) G, dan (27,53) G en de punt (27,54) g. Links zit een donkere scheiding tegen het roze: (26,52) g en (26,53) d. (28,53) is weer roze r. |
| 2 liggende staart | 17 | De bovenrand (33-37,57) is G in plaats van g. Het hooglicht H loopt alleen nog op x 34-40 (rij 58). h op rij 59 loopt door tot x 46. De g-sikkel begint op rij 59 bij x 52 en op rij 60 bij x 42, dus rechts in de bocht dikker. Geen vier parallelle banden meer. |
| 3 scheen | 33 | Doorlopende lichte voorkant (h, 2 px) langs de linkercontour van de knie (41,49) tot de voet (43-44,55). Eén rib in g op x 46, rechts ervan G. |
| 3 verre achterbeen | 39 | Een stap donkerder (h→G, G→g). De meest linkse h per rij blijft h als eigen lichte kant, net als bij de verre arm. Zonder die kant las het been als donker gat. |
| 4 rechterflank staart | 30 | Eén rib in g op x 56 (rij 44-53), links ervan G, rechts G en een dichte sikkel van 2 px g tegen de buitenlijn (x 59-60, op rij 44 x 58). Geen om-en-om G/g meer. |
| 5 nabije hand | 3 | (30,47), (32,47) en (34,46) h→G; de vingerlijnen zijn alleen nog g. |

**Welk been staat vóór (punt 3, gemeten in het model).** Het gestreepte been in het midden (dij x 38-49 met scheen naar de voet op de staart) is het nabije achterbeen. De vorm x 19-28, y 41-50 onder de nabije arm hoort bij het verre been. Die eindigt achter de knots en is in het model donkerder groen. De keurder heeft dus gelijk.

## Eerlijk oordeel
- Op 1× wijkt het verre been nu terug en springt de nabije scheen naar voren.
- De liggende staart leest als buis met een kort hooglicht.
- Het schutblad leest als blad met een punt, niet meer als randlicht.
- Twijfelpunt: het verre been is nu overwegend g en daarmee het donkerste vlak van het lijf. Is dat te zwaar, dan kunnen we vanuit G één stap terug.
