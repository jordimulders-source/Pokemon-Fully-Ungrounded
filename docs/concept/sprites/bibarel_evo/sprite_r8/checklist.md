# r8 checklist (zelftoets maker), vanaf r7
Bouw: `python3 sprite_r8/bouw.py` (vanuit `bibarel_evo/`). Gewijzigd t.o.v. r7: 130 px, **buiten de zones 0** (script-bewijs), silhouet gelijk, 15 kleuren + transparant.
Zones: palet (14 px van de oude 140/120/100), 1/2 x24–39 r35–51, 3 x33–42 r45–54, 4 x26–32 r34–35, 5 x26–38 r26–33, 6 x10–21 r26–34.

## Reparaties
| # | Opdracht | Gehaald | Meting |
|---|---|---|---|
| 1a | paletplek vrij: 140/120/100 samenvoegen | ja | 14 px → crème-donker 176/138/96 (dichtstbij, RGB-afstand 40; lum 124→145). Plekken: oogringen (21,16–18), (24,16–17), (29,16–18), (33,16–17), (21,21–22), potloodpunt (3,23), (4,23). Oog leest nog (grijze ring wordt tan; zie vel). |
| 1b | crème-middentint als sikkel | ja | nieuw idx 10 = 228/204/166, lum 207 (k 233 → 207 → h 181 → m 145: stappen 26/26/36). 77 px: rechterhelft borststuk x34–39 r35–44 (breedte 2,2,2,3,4,6,5,4,3,3: lens, niet evenwijdig) en buik r45–51 (x29–35 → x24–26, breedte 7,8,7,7,6,5,3). Lichte kern linksboven blijft k. Geen vlakjes < 3 px in het crème. |
| 2 | zakje lichter, gat onderzoom | ja | zakje blijft k, borststuk rechts ervan en eronder nu middentint → zakje leest als lichter vlak. Gat zat op **(24,44)** (k); (25,44) was al tan → (24,44) k→h. |
| 3 | rechterrand crème buigt naar het kruis, sikkel dikker naar onder | ja | rand per rij r45–54: r7 42,40,39,38,38,36,36,35,34,34 (rechte 45°) → r8 42,40,38,37,37,36,36,36,35,34 (snel naar binnen, dan verticaal langs de dij, dan naar het kruis). Donker crème per rij 3,1,2,2,3,3,3,4,3,2. Dij krijgt 3 px bruin-midden (39,47), (38,48), (38,49). |
| 4 | bovenrand borststuk als boog | ja | rand tussen de bandjes r34,35,35,36,35,35,34 (x26–32) i.p.v. recht r35; (29,35) bruin-donker in de inham. |
| 5 | borst: stamkleur weg, één plooi | ja | (29,26), (35,29), (36,29) → bruin-lijn (model daar donker); (31,31) → bruin-donker. Plooi uit `model/r10_k8_64.png`: linksverticaal x30 r26–29 + band r30 x29–34; schouderplooi (35,27), r28 x34–38, r29 bruin-lijn x35–37, (35,30). Losse stippen (31,27), (29,28), (31,29), (34,27), (36,27) → bruin-midden. Stamkleur in de zone: 0 px. |
| 6 | linkerbovenarm: binnenlijn één tint | ja | (16,28), (16,29), (20,28) → bruin-lijn 96/56/32 (= keurders "a"; "donkerbruin" zo gelezen, de lijntint naast deze pixels). Ook (10,27), (19,34) stam → bruin-lijn en (11,27) → bruin-lijn (model 66), (11,34) stam → bruin-donker, (21,27) losse donkere stip → bruin-midden (model 144). Stamkleur in de arm nu alleen hand (x13–17). |

## Jordi's checklist
| Regel | Gehaald | Meting |
|---|---|---|
| "geen rechte lijnen" | ja | bovenrand borststuk is boog; rechterrand crème gebogen (zie 3); zakje recht = mag. Linkerbuikrand x19 zit in het model (niet aangeraakt). |
| "Het moeten geen effen vlakken zijn" | ja, verbeterd | crème nu 4 tinten; grootste k-vlak 186 px (was 231 incl. potlood/zak), h-vlak 76 (was 117), m-vlak 77. |
| "A maar moet netter" / vorm r5 tot het kruis, benen bruin | ja | ongewijzigd t.o.v. r7 behalve rand (3) en boog (4), beide naar r5. |
| kraag r1 | ja | niet aangeraakt (diff 0). |
| broek tinten r1 / bovenlichaam-patroon r1 | ja | bruin-palet ongewijzigd; alleen de genoemde stippen. |
| "tuinbroekvorm, niet volledig rechte lijnen, bovenlichaam geen pixelblur, gewoon nette vormen, genoeg kleurtinten en schaduw" | ja | geen middeling; borst/arm alleen losse stippen → modelvormen; crème heeft sikkel. |
| tuinbroek 1-op-1 vorm (borststuk, zakje, bandjes) | ja | bandjes/zakje ongewijzigd; borststukrand naar r5. |
| "en let op kleurtinten en schaduw" | ja | crème 233/207/181/145, bruin ongewijzigd (stappen 37/37/38). |
| tanden wit, ogen Bibarel, neus rood | ja | tanden/neus diff 0; oogring 140/120/100 → 176/138/96 (alleen tint, vorm gelijk). |

## Zelf gezien (eerlijk)
- Buik: k → middentint → h → m loopt nog diagonaal schuin naar rechtsonder; breedtes variëren (7–3 / 3–7), maar keurder moet beoordelen of het als banding leest.
- Oogring tan i.p.v. grijs: iets minder koel; als dat stoort is idx 9 (96/78/64) het alternatief (donkerder).
