# Eindkeuring r5 (Dragonfly Cave): muriqui, nachtaap fase 3

**Oordeel: GOED.** Er zijn geen harde uitvoeringsfouten. Hieronder staan zachte punten (optioneel) en ontwerpvragen ter info.

Getoetst is alleen de uitvoering als Gen 3-sprite, volgens SPRITE_KERN, SPRITING (DFC-gids), FAKEMON_CHECKLIST E en GEMINI. Trouw aan het model telde niet mee: de gelijkeniskeurder gaf daar al PASS op (r4/KEURING.md). De vlakke bovenrand van de ogen en de 3 witte sikkelbogen op de rug zijn bewust anders dan het model en tellen dus niet als fout.

Vergelijkingsvel: sprite 6× en 1× naast Ambipom, Aipom, Mr. Mime, Medicham en Infernape, één keer op een lichte en één keer op een donkere achtergrond.

## Afvinken
| Punt | Oordeel |
|---|---|
| Kleuren | OK. 15 kleuren + transparant (index 0) |
| Buitenlijn | OK. Overal 1 px dik, zonder klonten. Aan de buitenrand staan alleen donkere tinten: `1`, de selout `4`/`5` en gloedrand `f`. Er staan geen lichte pixels aan de buitenkant, dus geen anti-aliasing naar buiten |
| Selout | OK. De lichtkant heeft gekleurde selout: de kop linksboven en de maanhoorn met `4`, de linkerrand van de opgeheven arm met `5`, de vingertoppen linksboven met `4`. Nergens wisselen `1` en lila om en om op één rand |
| Binnenlijnen | OK. De kaaklijn (x19–20, y34–45) staat in `5`, een donkere tint van het vlak. De vingers zijn gescheiden met `d`/`1` |
| Contrast | OK. De lijftinten c/3/4/5/1 hebben helderheid 163/127/89/58/21, dus stappen van 31–38, binnen de Taillow-norm. Het aandeel zeer donkere pixels is ±0,19, binnen de band van 0,10–0,25 |
| Licht linksboven | OK. De romp is boven `3` en onder `4`. De arm heeft rechts een smalle schaduwsikkel in `4`. Het hooglicht `2` zit in de kopkom linksboven. Het snuitje heeft schaduw `8` rechts en onder. Het verre been staat helemaal in `4` (E1) |
| Pillow shading | Geen. De kop is licht aan de linkerkant en heeft schaduw onder de snuit, geen ring langs de omtrek |
| Banding | Geen. De sikkel op de arm volgt de vorm en de rompschaduw is een vlak, geen band langs de rand |
| Losse pixels en ruis | Geen ruis. De kleine clusters van 1–2 px zijn allemaal bewuste details: vingertoppen, oogglans en -reflectie, neusgaten, mondlijn, de 1 px dunne lijnen van de spiraalstaart en de sikkelbogen |
| Tinten per vlak | OK. Lijf ≤ 3 tinten + lijn (c/3/4 + 5). Gloed e/a/f. Snuit 7/8 + mondlijn 5. Maan 9/b + 5 |
| Ogen | OK. Witte glans linksboven `9`, iris `a`, lichte reflectie onder `e`, rand `f`. Het verre oog (x5–6) is smaller en ligt dichter bij de kopomtrek (B3) |
| Leesbaarheid 1× | OK op licht en op donker. Je ziet meteen een aap met de maansikkel, het roze snuitje, de gloedhand en de spiraalstaart. Op donker valt de zwarte lijn weg, net als bij de echte sprites, en blijft de vorm leesbaar door de c/3/4-tinten |
| Vergelijking met echte sprites | Het niveau van afwerking en het waardebereik passen tussen Ambipom en Aipom. Zelfde schaal, zelfde lijndikte |

## Zachte punten (optioneel, géén afkeur)
1. **Onderrand van het been**, de trap van de onderlijn: 3-2-2-**1**-2-3. De enkele stap op (37,49) is een lichte besluiteloosheid. Je ziet het pas op 8×; op 1× niet.
2. **Onderrand van het been, y52 x43–52**: een recht stuk van 10 px. Het model is daar ook vrijwel recht, dus dit blijft zo.
3. **Bovenrand van de romp, y30 x25–30**: zwart aan de lichtkant. Ambipom heeft daar ook een donkere lijn, dus het mag. Wie wil, kan het afzwakken naar `5`, zoals de linkerrand van de arm.

## Ter info voor Jordi (ontwerp, geen keurpunt)
- Het lijf heeft geen eigen hooglichttint: `c` zit alleen op de handen en de staart, en het been staat helemaal in schaduw. De R/S-stijl gebruikt meer hooglicht. Een Gen 3-lichtronde mag volgens GEMINI.md ("Gen 3 boven het model voor licht en contrast") alleen als Jordi erom vraagt.
