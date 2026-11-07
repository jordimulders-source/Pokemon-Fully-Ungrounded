# Hatun runa r4: eindkeuring Dragonfly Cave (7 nov)

Eindkeurder: alleen uitvoering, geen herontwerp. Jordi (7 nov): "ik vind hem netjes, ga maar los met eindkeuring, dragonflycave keuring en vergelijking met andere gen 3 sprites, dit is puur kleur gebruik en schaduwen". Vorm, silhouet, pose en ontwerp zijn dus bevroren; de nadruk ligt op **kleurgebruik en schaduw**.
Vel: `eindkeuring_vel.png` (r4 | verkleind model | Taillow | Swellow | Wingull | Spearow | Pidgey, alle op 8×, de `_gba`-sprites uit `graphics/pokemon/`; onderaan 1× en 2× op licht en donker).
Metingen: scripts op `raster.txt` + `normal.pal` (clusters per index met 4- en 8-buren, buitenrandscan per index, 2×2-dambordscan, HSV/helderheid per tint) en het model per spritepixel (blokken volgens `silhouet/sil.py`: schaal 16,875, bbox x108/y104, top 19, left 8; mediaan en dichtstbijzijnde paletindex). Helderheid L = 0,299R + 0,587G + 0,114B.

## Hoofdvraag (1×)
Leest als de vogel uit het model: zelfde pose en kleurvlakken (zwarte kruin met goudvlek, witte streep, masker, open bek, witte keel, gele buik, nabije vleugel met gouden onderkant, verre vleugel, roestbruine staart). Het oog leest nu: zwarte pupil met witte glans (18,48) en witte sikkel (20,47–48), ook op 1× op licht en donker. **PASS.**

## Eindoordeel: **NIET GOED, maar heel dichtbij** (11 px in 3 benoemde reparaties, alle kleur/schaduw; daarna GOED, alleen diff-controle nodig, geen nieuwe keuring)

## Kleurgebruik en schaduw, gemeten tegen Gen 3
| Tintgroep | r4 (L / tint H / verzadiging S) | Gen 3-vergelijking | Oordeel |
|---|---|---|---|
| Bruin 2–5 | 63 / 82 / 111 / 145; H 20→19→23→25; S 50/67/65/60 | Pidgey bruin 65/98/134/167, H 20→24; Spearow/Fearow 75/121/162 | PASS. Tintverschuiving als Pidgey (schaduw roder, licht geler). Stap 2→3 is maar 19 (Gen 3: 30–45), maar 2 is de donkerbruine rug als apart materiaal en meet in het model 63–66: trouw. 4 tinten = bekend grensgeval. |
| Goud/geel 6–8 | 148 / 175 / 208; H 37→42→47; S 71/73/66 | Fearow 121/162/189/211, H 38→35; Taillow geel 188/225 | PASS. Goede verschuiving naar oranje in de schaduw, stappen 27/33 (Taillow-orde). |
| Wit 9/A | 239 / 205 | Taillow/Swellow 255 + grijs 211 | PASS. Model meet in streep en keel 241–242 (vlak wit) en 214 alleen onderaan de keel; de sprite volgt dat (A op (19–20,53), (22,54)). |
| Masker F / omlijning 1 | 51 (koel blauwgrijs) / 25 (warm zwart) | Taillow omlijning 0, donkerblauw 51 | PASS. Twee zwarten uit elkaar te houden; pupil leest door de glans. |
| Grijs snavel B/C, rood D, E | 91/151; 132; 109 | | PASS. Kleine vlakken, op de modelplekken. |

| Eis | Oordeel | Reden |
|---|---|---|
| ≤ 3 tinten per groep + omlijning | PASS (grensgeval bruin) | Zie boven. |
| Licht linksboven, schaduw als sikkel | PASS met 2 uitzonderingen | Buik licht links → 7 → sikkel 6 rechtsonder; staart en verre vleugel lichter boven, donker onder; nabije vleugel lichte voorrand links, omlijning rechts. Uitzonderingen: lichtste geel 8 tegen de **onderrand** van de buik (23–25,55) en lichtbruin 5 tegen de **rechter (schaduw)rand** van de nabije vleugel. Beide wijken ook af van het model (reparatie 2 en 3). |
| Buiksikkel 6 (y53–56) | PASS | Model meet daar 7 (L 161–169); de sprite zet de donkerste geeltint als sikkel langs de rechteronderrand. Dat is standaard Gen 3-vormschaduw (Taillow-buik) en volgt de rand; zie ter info. |
| Geen banding / pillow shading | PASS | Grenzen 8/7 en 7/6 in de buik zijn bollende curven die het model volgen (8|7-grens per rij gelijk aan het model, y50–53). Geen rand van licht rondom. |
| Geen dambord / tintvlakjes < 3 px | PASS | 25 clusters < 3 px (8-buren); Taillow 47, Spearow 55, Wingull 66, Pidgey 87, Swellow 107. De overgebleven zijn veerpunten, schuine veerlijntjes, goudvlek, oog en snavel op gemeten modelplekken. Het r3-dambord (x34–35, y35–38) is weg. 2×2-patronen in de slagpennen (x35–41, y26–33) zijn kruisende schuine veerlijntjes, model toont dezelfde textuur; niet storend op 1×–2×. |
| Belijning 1 px, selout | **FAIL (3 px)** | Gekleurde selout (3, rug 2) aan de lichtkant, zwart aan de schaduwkant: goed. Maar drie gaten in de onder-/schaduwrand waar een bruine pixel de omlijning onderbreekt (de zwarte buren raken elkaar niet, ook niet diagonaal): (18,41) = 3, (50,40) = 2, (45,44) = 2. Snavelselout B op (12,48)/(11,49) is lichtkant en bewust: PASS. |
| Contrast tegen Taillow | PASS | Stappen 27–34 per tint (Taillow 30–40); alleen bruin 2→3 kleiner (trouw aan het model). |

## Reparaties (top op prioriteit; alleen indexwijzigingen binnen het silhouet)
1. **Open onderrand dicht** (Gen 3: zwart aan de schaduwkant, geen open randen). (18,41): 3 → **1** (model mediaan 33,20,22 = omlijning). (50,40): 2 → **1** (gat tussen (51,40) en (49,41), onderkant staart). (45,44): 2 → **1** (gat tussen (46,44) en (44,45), onderkant rug). 3 px.
2. **Lichtste geel weg van de onderrand van de buik.** (23,55), (24,55), (25,55): 8 → **7** (model 214–218,166–174,56–62 = 7). Het lichtste geel hoort linksboven in de buik, niet tegen de onderste omlijning. 3 px.
3. **Geen lichtbruin aan de schaduwkant van de nabije vleugel.** (42,26), (41,28), (42,30), (41,34): 5 → **4** (model 171–179,98–105,57–60 = 4). Nu staan er lichte veerpuntjes tegen de rechteromlijning, tegen de lichtrichting in; het model heeft daar middenbruin. 4 px. (Ook (41,25) staat zo, maar meet in het model op de rand; mag mee, hoeft niet.)

Verder geen punten die op 1×–2× winst geven. Buiten deze 10–11 px: diff 0.

## Ter info voor Jordi (geen fout)
- De buik heeft in de sprite een donkere sikkel (6) rechtsonder waar het model alleen middengeel heeft; dat is de Gen 3-manier om de buik rond te maken. Wil je hem vlakker zoals het model: 6 → 7 op y53–56 rechts.
- De gouden onderkant van de nabije vleugel is één vlakke tint (6), net als in het model (meet overal 152–154). Op 1× leest dat als één vlak; Gen 3 zou er vaak een schaduw in zetten, maar het model heeft er geen.
- Donkerbruin (rug) en de donkerste veertint liggen dicht bij elkaar (L 63 tegen 82); daardoor is de onderste helft van de verre vleugel vrij donker en rustig. Trouw aan het model.
- Kleine kop en opgezette staart zijn het model, geen fout.
