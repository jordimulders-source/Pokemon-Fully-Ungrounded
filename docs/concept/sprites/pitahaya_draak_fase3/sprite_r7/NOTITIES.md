# Pitahaya-draak fase 3, sprite r7 (maker)

Jordi (18 nov), letterlijk: "de tong lijkt zo niet echt op een tong, dus haal die maar weg. Daarnaast vind ik rechts de beste, maar ik heb nog wel wat kritiek. Er is geen belijning tussen de achterpoot en de staart, lijkt net een blur. Plus het schaduw en kleur gebruik is in de hele sprite nog niet optimaal. Kan je daar nog aan werken? Hoofd en de vruchtvlees buik zijn nog het beste, maar verder mist die al het contrast dat sprites normaal wel hebben"

- **Basis:** `../sprite_r6/pitahaya3_r6_buik.png`, met de bekzone (x 0-12, y 26-38) uit `pitahaya3_r6_zonder_tong.png`. Het script controleert dat er geen tongpixels (geel, index 12-14) meer zijn.
- **Script:** `python3 maak_r7.py` schrijft `pitahaya3_r7.png` en `pitahaya3_r7_afwijkingen.txt`. Elke pixel heeft een assert op het oude teken. Het vel maak je met `python3 vel.py <tijdelijke map>`.
- **Studie:** Sceptile, Grovyle, Salamence, Tyranitar en Flygon (palet en gebruik per index).
  - Het groene basisvlak van Sceptile ligt rond L 115. De lichte tinten liggen op 167/205, de donkere op 55/98, plus zwart.
  - Ons basisgroen h lag op L 150. Daardoor las het hele lijf licht en vlak.
  - De stappen tussen de tinten waren wel in orde. Het probleem zat in de verdeling (bijna alles h) en in een te lichte basis.

## Controle
- Silhouet: alfa-diff 0 t.o.v. r6 zonder tong. T.o.v. r6 buik is de diff 17 px; dat is de tong buiten de bek, die weg is.
- Kop (x 0-20, y 12-30) pixelgelijk aan r6 zonder tong. Buikzone (RIJEN uit `../sprite_r6/buik.py`) pixelgelijk aan r6 buik.
- 14 kleuren incl. transparant. Index 13/14 zijn ongebruikt (zwart gezet), index 12 = nieuw diepgroen k.
- In totaal 182 px t.o.v. de basis. Zwart binnen de figuur (geen buitenlijn): 4,1% (r6: 3,6%).

## Palet oud → nieuw (alleen groen; roze, wit en zwart ongewijzigd)
| teken | oud | L | nieuw | L |
|---|---|---|---|---|
| k (12, nieuw) | (geel, tong) | – | (22,46,32) | 37 |
| g | (48,88,48) | 75 | (36,76,44) | 60 |
| G | (79,128,64) | 112 | (64,120,56) | 96 |
| h | (120,168,80) | 150 | (108,164,72) | 137 |
| H | (176,208,104) | 196 | (184,224,112) | 199 |

- Stappen nu 36 / 41 / 62, het basisgroen is donkerder en verzadigder.
- Kop en buik: daar zitten alleen groene blaadjes en de nek. Ze ogen even goed, maar zijn iets donkerder groen (zie vel).

## Per zone (px)
| zone | px | wat |
|---|---|---|
| 1 lijn voet-staart | 12 | Zwarte lijn op de modelplek: van (42,57) schuin omhoog via (45-48,56) en (49-50,55) naar de onderkant van het gat. Het gat (50,53), (51,54) en (52,53) is nu dicht omlijnd. |
| 1 staart onder de lijn | 8 | De bovenkant van de staart direct onder de lijn is H. Een donkere voet op een lichte staart geeft geen blur meer. |
| 1b dijboog + contour | 7 | Bovenrand van de dij (model y≈40) als g-lijn (41-44,40). De rechtercontour (46,41), (47,42) en (48,43) in k sluit aan op de bestaande ## (48-49,44). De dij liep eerst over in heup en staartwortel. |
| 2 dij + scheen | 25 | Hooglicht H linksboven onder de boog. Rechts van de rib G, de onderkant van de dij en de bovenkant van de scheen in G/g. |
| 2 slagschaduw heup | 9 | G op heup en staartwortel direct rechts van de dijcontour. |
| 2c romp / flank | 28 | Schaduwband onderaan de romp (rij 32-34) en de flank boven de dijboog (rij 38 vanaf x 43, rij 39 helemaal) in G, zodat de band de boog volgt. Daardoor leest de dij als vorm vóór de romp. |
| 3 staart | 60 | De rib (x 56-57) is de terminator: links h, rechts G. Onderaan ligt een sikkel g/k tegen de buitenlijn (rij 54-60). Het liggende deel heeft H boven, h, en G/g onder. |
| 4 vorm achter arm | 5 | Iets meer G rechts en onderaan. |
| 5 knots | 14 | Bovenrand r (selout in plaats van lichtroze op de rand), P-hooglicht linksboven, r rechtsonder. |
| 6 stekels | 14 | Klein P-hooglicht (3-5 px) linksboven op vijf platen. |

## Afwijkingen van het model
- De kleur wijkt af: donkerder basisgroen, meer schaduw en sikkels (Jordi: "Je mag met kleur altijd van het model afwijken").
- Vorm/silhouet: geen afwijking. De nieuwe lijnen liggen op modellijnen (voet/staart, dijboog, dijcontour).
- De bestaande afwijkingen van r6 blijven: de buikzone is door de maker vastgesteld en de pitjes zijn verplaatst.

## Eerlijk oordeel op 1×
- Naast Sceptile en Tyranitar heeft het lijf nu duidelijk licht en schaduw. De dij leest als ronde vorm en de staart als buis, met de schaduw aan de buitenkant.
- Nog zwak: de lichte H-wig op nek en schouder (x 20-33, y 21-27) is groot en fel. Die is niet aangeraakt, want hij hoort bij het deel dat Jordi goed vond.
- Gerepareerd: de schaduwband boven de dij liep eerst recht. Rij 38 is nu G vanaf x 43, zodat de band de boog volgt.
