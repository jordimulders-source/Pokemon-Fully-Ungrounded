# Nachtaap fase 1, ronde 4: 3/4-pose (na KEURING_RONDE3.md)

Bestanden:
- `anim_front.png` (64×128, geïndexeerd, index 0 transparant)
- `normal.pal`
- `compare.png`: ronde 3 en 4 naast Aipom, Treecko, Torchic, Mudkip, Abra, Ralts, Natu, Spoink, Meditite en Wynaut (GBA-originelen) en Espurr, op 3× en 1×, met de silhouettest.
- `thumbnails.png`: de tussenstappen van deze ronde.
- `bron/build.py` maakt de sprite; `bron/compose.py` maakt het vel. `bron/base.py` en `base_f1.txt` zijn alleen de eerste ondertekening.

Afgerond op verzoek, omdat de gebruikslimiet bijna op was; er zijn geen extra iteraties gedaan.

## Verbeterpunten uit de keuring
1. **3/4-pose naar links:** het gezicht en de snuit staan naar links verschoven. Het verre oog is smaller (6 px tegen 8 px) en het verre oor steekt half achter de kop uit. Op de kop zit een schaduwband van 5 px aan de rechterkant.
2. **Zittend dierenlijf:** een peervormige romp (smal bij de nek), een ronde nabije dij met een voet naar voren, een kleinere verre dij en voet erachter, teenscheidingen en losse armen met een donkere scheiding tegen het lijf.
3. **Nachtaapmasker:** een donkere middenstreep van de kruin tot tussen de ogen, donkere zijstrepen langs de buitenkant van de ogen naar de kaken, en witte vlekken boven de ogen.
4. **Eén psychisch kenmerk:** de maanparel in de handen. Het voorhoofdjuweel en de roze oorstippen zijn weg. De oren zijn kleine schelpjes met een donkere binnenkant. Roze komt alleen nog voor op de neus en de staartpunt.
5. **Ogen:** halve oogleden in de schaduwtint met een rechte lidlijn. Daaronder zit een gloeiende maan-iris zonder pupil, met een donkere rand, 1 glanspixel en een lichtere kern. Er is geen volle zwarte ring meer. Een donkere iris met lid las in de tussenstappen als verveeld; de gloeiende versie leest als een psychische, rustige blik.
6. **Staart:** taps toelopend, met een S-bocht vanaf de heup die eindigt in een grotere Nazca-spiraal (straal 8). De punt licht roze op.
7. **Omlijning aan de lichtkant in de donkere tint (index 4).** Binnenlijnen zijn index 4, en onderaan zit één zwarte rand.
8. **Schaduw als halve maan** rechtsonder op kop, romp en dijen, met kleine hooglichten linksboven. Het contrast is groter dan in ronde 3: index 3 is donkerder en blauwer.
9. **Frame 2:** dezelfde ogen en hetzelfde karakter. De kop en de staart komen 1 px omhoog en de nabije arm zwaait met een ronde handpalm met 3 vingers in lijfkleur. De verre hand houdt de parel vast.

## Palet
```
'nachtaap': {'vacht': [1, 2, 3, 4], 'zilver': [5, 6, 7], 'roze': [8, 9, 10], 'maan': [11, 12, 13], 'wit': [14]}
```
| index | kleur | gebruik |
|---|---|---|
| 1–4 | #e6d5ff #ac94de #7362b4 #4d3d83 | vacht; 4 is ook de lijn aan de lichtkant en het masker |
| 5–7 | #f6f6ff #c5c5e6 #8b94bd | zilver: wenkbrauwvlekken, snuit |
| 8–10 | #ffa4d5 #e65aa4 #9c2962 | roze: neus, staartpunt; 10 is ongebruikt |
| 11–13 | #deffff #5abdde #202c5e | maan: ogen en parel |
| 14 | #ffffff | glans |
| 15 | #101010 | omlijning |

## check.py (`--stage 1`)
- Geen FOUT.
- LET OP: rand linksboven 0,21 (Hoenn p10 0,26). Dat komt door de donkere lijn aan de lichtkant waar de keuring om vroeg. Wil je het in de Hoenn-spreiding krijgen, dan kan index 4 nog een stap lichter.
- LET OP: geen back.png en geen icon.png (niet gevraagd).
- OK: hoogte 42, breedte 47, oppervlak 1230, 14 kleuren, zwart aan de rand 0,54, schaduw 0,50, dithering 0,04, zwarte binnenlijnen 0,04.
- Verschil tussen frame 1 en 2 is 0,285, net boven de Hoenn-p10 (0,282).

## Nog open
- De draai van de kop is nog bescheiden: de kopvorm zelf is rond en symmetrisch, alleen het gezicht is verschoven.
- De halve oogleden lezen nog een tikje verveeld.
- De spiraal raakt de kop.
- Geen back, icoon of proefvarianten.
