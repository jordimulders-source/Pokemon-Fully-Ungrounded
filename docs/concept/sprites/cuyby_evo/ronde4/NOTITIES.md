# Cuyby-evolutie ronde 4: kleinere snuit, meer haar over het gezicht

Jordi over ronde 3: "Ziet er goed uit." Kleuren, schaduw, kruin, pose en vacht blijven zoals ze zijn. Verder was hij er tevreden mee: "is ook duidelijk een Cuyby-evolutie". Deze ronde is daarom bewust klein:
1. **De witte snuit iets kleiner.**
2. **Het haar valt iets verder over het gezicht en de snuit.** Het nabije oog blijft vrij, het verre oog blijft bedekt.
3. De nodig-punten uit de keuring (`../ronde3/KEURING.md`): de open randen in frame 1 en 2 (N1, N2). N3 valt samen met punt 1.

Er is niets veranderd aan het ontwerp, het palet, de kruinvorm, de pose of de vacht van de romp.

## Bouwen (vanuit de repo-root)
```
python3 docs/concept/sprites/cuyby_evo/ronde4/bron/rle4.py        # delen_rle.txt -> delen.txt
python3 docs/concept/sprites/cuyby_evo/ronde4/bron/bouw9.py docs/concept/sprites/cuyby_evo/ronde4
python3 docs/concept/sprites/cuyby_evo/ronde4/bron/vel.py         # compare.png + metingen
```
- **Bron in eindcoördinaten.** In ronde 3 stonden de coördinaten van vóór het knippen. Dat maakte elke reparatie omrekenwerk.
  - `omzet.py` heeft `ronde3/bron/delen.txt`, dat al geknipt is, eenmalig teruggeschreven naar run-length-rijen. Die rijen staan nu in `delen_rle.txt`.
  - Zonder wijzigingen gaf dat exact hetzelfde raster als ronde 3. Dat is gecontroleerd met `cmp`.
  - `rle4.py` is `rle3.py` zonder knip.
- De coördinaten hieronder zijn dus gelijk aan die in `bron/raster_f1.txt` en in de keuring.

## Wat er veranderde
| deel | ronde 3 | ronde 4 |
|---|---|---|
| **pony** | Drie lokken die diagonaal eindigen bij x21→x13 (y28–36), met zwarte scheidingen midden in het licht. | Vier lokken. Ze lopen 1–2 rijen verder door en buigen onderaan omlaag over het gezicht, zoals haar dat eerst van de kruin schuin valt en dan hangt. Lok 4 (x21–24, y27–35) bedekt de bles en 1–2 px van de linkerrand van de vlek. De punten liggen op verschillende hoogte: x22y35, x18y36, x15y37. Scheidingen in r, K alleen onder de punten (keuring P1). |
| **snuit** | Witte wig van bles plus snuit, x12–23 en y28–43, 74 px wit (zonder de glans in het oog). | Alleen de snuit is zichtbaar: een ronde vorm van x13–20 en y36–42 met het neusje op x12–13, 38 px wit (bijna de helft). De rechterrand ligt op x20 in plaats van x22. De kin ligt op y42 in plaats van y43, met een slagschaduw d eronder. De bovenrand ligt onder de lokpunten. |
| **wang** | Het wit raakte de vlek over de hele hoogte. | Tussen de snuit en de vlek zit een wangetje haar (d/s, x21–23, y38–41). Het wit raakt de vlek alleen nog bovenaan (y36–37), zodat de Cuyby-overgang van zwart naar wit blijft. Door het wangetje zit de snuit in de vacht. |
| **kruin** | Bovenkanten van sprieten open. | r op x20y12, x13y15, x15y16, x17y17 en x19y18. De achterste spriet is dicht (x32–36, y17–18). De vorm en de beweging zijn gelijk gebleven. |
| **kruinvoet** | Lag in frame 2 open op (15,20) en (31,20). | Een r op y19 (x15, x31). In frame 1 lag daar al een r van de spriet. |
| **randen** | d/q/s op de schaduwkant tegen de lucht. | K op x47y24, x50y28, x54y42, x52–53y43, x48y47, x44y48, x50y48 en x38y50 (nieuw deel `randen`). |

## §0-checklist (SPRITING.md)
| # | punt | stand |
|---|---|---|
| 1 | Lichaam én blik diagonaal | **Ok.** De pose is ongewijzigd uit ronde 3 (3/4 naar links-voor, rug daalt, zoom stijgt, verre pootjes links en hoger). De snuit wijst nog steeds naar links-voor. |
| 2 | Ledematen, oren, ogen geteld en verbonden | **Ok.** Er zijn 4 pootjes en 1 zichtbaar oor. Het nabije oog is vrij (x25–28, y33–36, de ring g is onaangeroerd), het verre oog zit onder de pony. Neus en mond (e c e, y41) zijn er. `bouw9`: **geen open randen** in frame 1 en 2 (ronde 3: 19 en 21). |
| 3 | Geen rechte lijnen in de omtrek | **Ok.** `bouw9` vindt geen randstuk van meer dan 4 px. De nieuwe onderrand van de lok rechts stijgt naar de punt (x51–55, y43→42). |
| 4 | Ogen geïntegreerd | **Ok.** Het oog is ongewijzigd: bovenlid en ring g, glans a linksboven, weerkaatsing n rechtsonder. Lok 4 eindigt links van de ring. Boven het oog staan geen donkere pixels, dus er ontstaat geen boze wenkbrauw (les §17). |
| 5 | Silhouet op 1× | **Ok.** Het silhouet is gelijk aan ronde 3. Op 1× is de snuit nu een klein licht vlekje onder de pony in plaats van de grootste vlek. Wat je eerst ziet is de vlek met het oog, en het dier zit meer in zijn vacht (zie `compare.png`, licht en donker). |
| 6 | Formaat | **Ok.** 1416 px (frame 2: 1418), 49×44. Dat is +17 px door de dichtgemaakte randen. Het ligt tussen Linoone (1357) en Piloswine (1515). |
| 7 | Pose niet stijf | **Ok.** De pose is ongewijzigd. |

Verder: het palet heeft 16 kleuren en is ongewijzigd. De lijst van 15 gebruikte kleuren is gelijk gebleven.

## Metingen (frame 1)
| sprite | oppervlak | b×h | zwart rand | zwart lichtkant | zwart schaduwkant |
|---|---|---|---|---|---|
| ronde 3 | 1399 | 49×44 | 0,49 | 0,14 | 0,77 |
| **ronde 4** | 1416 | 49×44 | 0,55 | 0,18 | 0,88 |
| Piloswine | 1515 | 42×48 | 0,43 | 0,00 | 0,79 |
| Mareep | 893 | 38×33 | 0,49 | 0,12 | 0,84 |
| Linoone | 1357 | 51×60 | 0,56 | 0,41 | 0,62 |

Het zwart-aandeel steeg doordat de schaduwkant nu overal dicht is. Ronde 4 zit daarmee nog binnen Gen 3: Vulpix en Whismur 0,85, Eevee 0,78.

## Eigen oordeel
- **Beter:**
  - Op 1× is de snuit niet meer het eerste wat je ziet.
  - Het gezicht zit dieper in de vacht. Pony en wang omsluiten de snuit en de vlek.
  - Tegen een donkere achtergrond lekken geen lichte randpixels meer weg.
- **Twijfel:**
  - De vier lokken over het gezicht hangen onderaan vrij recht naast elkaar (scheidingen op x12, x16 en x20). Op 3× is dat net een gordijn. Als dat te regelmatig leest, kan de middelste scheiding onderaan 1 px naar rechts buigen.
  - Lok 4 legt haar over de linkerrand van de vlek. Is dat te veel, dan kan hij 1 px smaller (x24 terug naar G).
