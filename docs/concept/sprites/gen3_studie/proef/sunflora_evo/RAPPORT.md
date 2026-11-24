# Proef tintzones: Sunflora-evolutie (24 nov)

Bron: `docs/concept/sprites/sunflora_evo/af/sunflora_evo.png` (niet aangeraakt). Resultaat: `na.png`, vergelijking: `voor_na.png` (voor | na | Gen 3 Sunflora op 6×; daaronder op 1× ook Sunkern, Solrock en Bellossom). De wijzigingen staan als pixellijsten in `maak.py` (geen kwantiseren, middelen of blur).

## Probleem
De gezichtsschijf had ringen van tinten langs de rand: van buiten naar binnen oranje (5) / donker goud (4) → geel (3) → crème (2) → soms weer geel, en aan de rechterkant twee gele ringen met een crème streep ertussen. Het las als airbrush/kussen. Gen 3 Sunflora: één crème grondtint, één schaduwzone (rechts en onder) met een harde grens, buitenlijn donker.

## Wat er per zone veranderde (76 px, allemaal binnen de schijf, x 17–40, y 17–39)
| Zone | Wat | px |
|---|---|---|
| Lichtkant buitenlijn (linksboven) | de buitenste ring (oranje/geel) wordt één lijn in donker goud 4 (selout), ook bovenop de schijf waar crème direct tegen de stralen lag | 14 |
| Grondtint | gele ringpixels binnen de lichtkant (links, linksboven) en losse gele stipjes rechts → crème 2 | 18 |
| Schaduwzone | één sikkel in geel 3 rechts (2 px boven, 3–4 px midden), die onderaan overgaat in de bestaande gele kinzone; ook linksonder een smalle strook; oranje/goud in de rand van die zone → 3 | 35 |
| Schaduwkant buitenlijn (rechts) | oranje/goud aan de rechterrand → bruin 6; onderaan blijft de bestaande zwarte lijn | 9 |
| Stralen, lijf, blad, voeten | niets | 0 |

Palet ongewijzigd (14 kleuren + transparant), PNG mode P, 64×64.

## Bewijzen (uit `maak.py`)
- Silhouet (transparantiemasker): **diff 0**.
- Gezicht: **diff 0** op 81 bevroren pixels: ogen (1/8/9), mond (6, tong a, de 4 onderin), de wenkbrauwlijn (\_/\_/ in geel, 15 px) en de losse AA-pixels aan de gezichtslijnen (20,27) (19,28) (24,28) (29,28) (34,28) (23,25) (30,25) (31,30) (30,34).
- Geen enkele wijziging buiten het vak x 17–40, y 17–39.

## Wat ik zelf nog zwak vind
- De bevroren AA-stipjes onder de ooguiteinden (19,28) (24,28) (29,28) en naast de mondhoek (31,30) zijn zelf kleine vlekjes zonder richting; ze horen bij het gezicht, dus blijven staan. (34,28) valt nu wel in de schaduwzone.
- De wenkbrauwlijn is in dezelfde geel als de schaduw; rechtsboven ligt de wenkbrauw dicht bij de sikkel, maar ze raken elkaar niet.
- Linksonder (rond x 19–21, y 33–36) is de schaduwstrook smal en hoekig, omdat de zwarte lijn daar al grillig loopt (silhouet en bestaande lijn niet aangeraakt).
- Stralen niet aangepakt: de oranje vlekken in de gele stralen en de gemengde oranje/goud randjes lezen naast Solrock nog onrustig. Dat was buiten deze opdracht (alleen de schijf).
- Geel 3 als schaduw is verzadigder/oranjer dan het khaki van Sunflora; een eigen schaduwkleur kan in slot 15 (nu ongebruikt), maar dat heb ik niet gedaan om het palet gelijk te houden.

# Ronde 2: stralen (24 nov)
Opdracht (coördinator): per straal één licht en één schaduw. Bij geel/oranje is de lichtkant links/boven geel en ligt de schaduw als één oranje zone rechts/onder. Bij navy is de grondtint blauw, met hooguit een smalle lichtere rand aan de lichtkant en de donkerste tint aan de schaduwkant. Waar een straal over een andere valt, komt er één binnenlijn. Schijf, gezicht, silhouet, blad, steel en voeten bleven bevroren. Resultaat: `na_r2.png`, vel `voor_na_r2.png` (voor | r1 | r2 | Solrock | Sunflora, op 6× en 1×), pixellijsten in `maak_r2.py`.

## Per straal (141 px)
| Straal | Wat | px |
|---|---|---|
| A boven, navy facet | schaduwrand 8 langs de rechterkant doorgetrokken (was onderbroken door 7) | 8 |
| B oranje vlam linksboven | bruine lichtrand → 4, linkerhelft geel, rechterhelft oranje | 14 |
| C/C2 gele stralen linksboven | 1 px oranje schaduwstrook langs de rechterrand | 5 |
| D navy linksboven | punt was donkerst (9) → lichtrand 7 links, grond 8, onderrand 9 | 16 |
| F0 boven de linkerstraal | oranje vlek in het geel weg; bruine puntjes → lichtrand 4 | 3 |
| E grote linkerstraal | punt 4; losse oranje vlekken → één oranje strook onderlangs het geel | 10 |
| F1/F2 oranje stralen linksonder | lichtkant (boven/links) geel met 4-rand, rest oranje | 18 |
| G vlammetje in navy linksonder | zalmkleurige pixels weg; licht links, oranje rechts | 8 |
| H straal onder + vlam | lichtpixel links bovenaan, vlam ernaast een gele lichtrand | 3 |
| N oranje straal boven | bruine punt → 4, linkerhelft geel, rechterhelft oranje | 17 |
| M gele straal rechtsboven | bruine pixels in de lichtrand → 4; oranje vlek in geel en oranje tong in navy weg; zalm weg | 6 |
| L oranje straal rechts | was bruin boven/oranje onder (omgekeerd) → 4-rand + geel boven, oranje onder | 10 |
| K navy straal rechts | bovenfacet 7 en onderfacet 8 met één grens in de lengte; losse 7 in het onderfacet weg; 4 in de vlam → 5 | 14 |
| J oranje straal rechtsonder | bovenste rij geel | 4 |
| vlammen onderaan | lichtrand linksboven geel | 5 |

## Bewijzen (uit `maak_r2.py`)
- Silhouet t.o.v. het origineel in `af/`: **diff 0**.
- Schijf + gezicht t.o.v. r1: **diff 0** (alles binnen een cirkel van r 11,6 rond het schijfmidden is uitgesloten; het script weigert daar elke wijziging).
- Blad, steel, voeten en alle zwarte lijnen (index 1): **diff 0** (het script weigert die kleuren als bron of doel).
- Palet ongewijzigd, 14 kleuren + transparant, mode P 64×64.

## Wat ik zelf nog zwak vind (r2)
- Het gebied linksonder (F0/F1, x 9–19, y 18–38) blijft druk: drie stralen en navy lopen daar door elkaar, en de oranje zone van F0 (x 12–14) is nog een losse vlek, geen strook in de lengte.
- De oranje vlammen ín de navy stralen (K rechts, onderaan) heb ik als tekening uit het model laten staan, alleen schoongemaakt. Naast Solrock blijven ze het drukste deel.
- Lijnen tussen overlappende stralen zijn niet overal één binnenlijn: soms 4, soms 9 en soms zwart, omdat ik zwart (1) niet heb aangeraakt.
- De grote navy massa onderaan heeft nog geen lichtrand; ik heb die vlak 8 gelaten ("hooguit").
- Twee pixels van de vlam rechtsonder (36,36) en (35,37) vallen binnen de beschermde schijfcirkel en zijn dus niet bijgewerkt.
