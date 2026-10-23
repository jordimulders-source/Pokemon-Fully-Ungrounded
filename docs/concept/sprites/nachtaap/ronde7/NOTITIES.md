# Nachtaap fase 1, ronde 7: pixel-over van concept B volgens de spritingregels

Modeltekening: **concept B** (`docs/concept/ontwerp/nachtaap/concept_B.png`), ongewijzigd: dieper violet, indigo rand rond een bleke lila gezichtsschijf, cyaan ogen, tarsierhurk, hand bij de wang, Nazca-spiraalstaart, geen borststeen.

## Wat anders is dan ronde 6
| Klacht (Jordi / blinde test) | Ronde 7 |
|---|---|
| "heel cartoony" | De omlijning is per kleurgroep opgebouwd. Op de belichte randen is de schaduwkleur de omlijning, met een lichtere tint aan de binnenkant. Aan de schaduwkant is hij zwart. Gemeten: 27% van de buitenrand is lichte omlijning (ronde 6: ±7%), 50% is zwart en 23% indigo. |
| "staart niet aan het lijf verbonden" | De staart komt dik (3 px vulling) laag achter de rechterdij vandaan. Hij loopt over de grond, buigt geleidelijk omhoog en draait in de spiraal naar binnen. Het puntje wordt 1 px dun en krult in het midden. |
| "ogen minder mysterieus", "reusachtige brillenglazen" | De ogen zijn halfgesloten amandelogen (6×3 iris onder een zwaar, recht ooglid), zonder ring eromheen. Ze hebben een witte glans linksboven, een lichtcyaan weerkaatsing rechtsonder, een donkere spleetpupil en een donkere onderrand in de iriskleur in plaats van zwart. Het verre oog is smaller (3 breed). In frame 2 zakt het ooglid een rij. |
| frontaal en symmetrisch | 3/4 naar links: de gezichtsschijf en de ogen zitten links, achter de kop zit een violette massa. Elk lichaamsdeel is anders: één hand bij de wang, één op de knie, een hoge knie rechts, een schuine dij links, en twee verschillende oren (het verre oor half achter de kop). |
| zachte shading met weinig contrast | Hooglicht staat in een grote vlek linksboven op de kop, de knieën en de spiraal. De evenaar loopt schuin van rechtsboven naar linksonder. De achterkop, de achterkant van de staart en de slagschaduw onder de kop (op de romp) zijn volledig schaduwkleur. |

## Werkwijze
1. Concept B verkleind tot ±48 px als onderlegger (alleen om af te lezen, niet in de sprite). Daarna per lichaamsdeel een eigen tekstraster in `bron/nachtaap.py`: staart, oren, romp, onderarm, benen, kop, hand en hand-op-knie. Getekend van achter naar voren. Elk raster is met de hand geschreven, inclusief schaduw en omlijning.
2. Per deel eerst de grove vorm, dan gerenderd (12–14× ingezoomd) en pixel voor pixel bijgewerkt. Gedaan in vijf rondes:
   1. eerste opzet;
   2. spiraal herschreven tot er echt een krul in zit (eerst was het een schietschijf);
   3. hand en arm vereenvoudigd: drie tanden werden een want met korte vingers, de onderarm loopt nu achter de kin langs;
   4. kop een kolom smaller en een rij lager, omdat het oppervlak te groot was;
   5. omlijning en vachtgrenzen.
3. Frame 2: het ooglid zakt een rij en de spiraal veert 1 px op (de stuit blijft liggen).

## Checklist SPRITING.md
| Regel | Toegepast |
|---|---|
| 1. Geen vormgereedschap | Geen PIL-ellipsen, -polygonen of automatische schaduw/omlijning. `lib.py` legt alleen tekstrasters neer. |
| 2. Grof, dan per deel gladstrijken; pixel-over | Pixel-over van concept B op ±48 px, per lichaamsdeel een raster, telkens gerenderd en bijgewerkt (zie Werkwijze). |
| 2. Gen 3-formaat | 64×64 per frame. Figuur 44×39, oppervlak **1047 px** (zie Eigen oordeel). |
| 3. Lijnen/curven | Kopcontour linksboven: segmenten 8-3-2-1-1, dan verticaal 2 en 9 (de stap van 1 naar 10 is rechtgezet). Spiraal: buitenrand 4-2-1-1, dan verticaal. Overgang stuit/staart: 5-2-1-1 boven, 9-1-1-1 onder. Geen hoeken of punten in rondingen; de enige punten zijn vingertoppen en tenen. |
| 3. Geen gespiegelde of gekopieerde delen | Oren, handen, benen en ogen zijn elk apart getekend en verschillen in vorm en grootte. |
| 4. Palet: 3 tinten + omlijning per kleur | Violet: Aipom-ramp een stap dieper en iets blauwer (hooglicht/basis/schaduw + indigo omlijningsbasis). Lila: Espeon-crème naar lila (3 tinten, omlijning via indigo). Cyaan: weerkaatsing/iris/donker. Roze: 2 tinten. Plus wit (glans), pupil en zwart. 15 kleuren + transparant. Geen verlooptinten. |
| 5. Licht linksboven, evenaar, slagschaduw | Zie de tabel hierboven. Slagschaduw van de kop op de romp en van de dij op de staartwortel staat volledig in de schaduwkleur. |
| 5. Veel hooglicht (R/S-stijl) | Ruime hooglichtvlekken (kop, knieën, spiraal en hand). Geen witte glimlichtjes op de vacht. |
| 6. Glans alleen waar het glanst | Wit staat alleen in de ogen. |
| 6. Ogen: glans + gekleurde weerkaatsing tegenover | Wit linksboven, lichtcyaan rechtsonder, op pixelniveau vergeleken met Espeon (3×3, zwart ooglid boven, glans linksboven) en Umbreon (smalle iris met pupil). |
| 7. Vacht gekarteld | De grens tussen basis en schaduw op de achterkop is gekarteld (rijen 3–6). Geen ruis elders. |
| 8. Omlijning per kleurgroep, 1 px, geen klonten | Belichte randen hebben de schaduwkleur (s) met een lichtere tint aan de binnenkant. De overgangen hebben indigo (o) en de schaduwkant zwart (K). Overal 1 px breed. Het enige zwarte binnenvlak is het ooglid. |
| 8. Lichtere pixels alleen binnen | Ja: de buitenste pixel is nooit lichter dan de pixel ernaast naar binnen. |
| 8. Pseudo-omlijning | De dunne staartpunt en de vingers zijn alleen met kleur gescheiden waar ze 1–2 px breed zijn. |
| 9. Frames / indexen | `anim_front.png` 64×128, 2 frames, 16 kleuren, index 0 transparant. Elk onderdeel heeft eigen indexen (violet, lila, cyaan, roze, pupil, glans). |

## Meting omlijning (frame 1, `keuring_ronde5/scripts/metrics.py` + aandeel bijna-zwart)
| | oppervlak | b×h | donkere buitenrand (lum<60) | waarvan zwart | detail | verzadiging |
|---|---|---|---|---|---|---|
| **ronde 7** | 1047 | 44×39 | **0,73** | **0,50** | 1,87 | 0,52 |
| ronde 6 | 999 | 43×37 | 0,93 | 0,00 | 2,02 | 0,56 |
| Aipom | 856 | 32×56 | 0,60 | 0,40 | 2,00 | 0,48 |
| Abra | 906 | 42×40 | 0,56 | 0,49 | 1,93 | 0,72 |
| Treecko | 967 | 47×48 | 0,65 | 0,61 | 1,76 | 0,51 |
| Umbreon | 1069 | 43×49 | 0,91 | 0,42 | 1,59 | 0,16 |
| Espeon | 1101 | 42×48 | 0,26 | 0,26 | 1,63 | 0,38 |

Let op: de meting "donkere buitenrand" telt ook de gekleurde omlijningsbasis mee (indigo is lum ±49). De 0,93 van ronde 6 was dus geen zwart. Het was een rand die overal even donker was, zonder lichtere omlijning op de belichte kant. Het zwart-aandeel (0,50) zit nu midden in het Gen 3-bereik (0,26–0,61). De donkere rand (0,73) zit nog boven Aipom en Abra, tussen Treecko en Umbreon in. Meer lichte omlijning kan alleen op de kop rechtsboven, en die zit achter het oor.

## Extra lessen uit de gids zelf (niet in SPRITING.md)
- **Revamp-volgorde (Scyther):** eerst de hele omlijning zwart, dan elke kleur zijn omlijningsbasis behalve rond de schaduwen, klonten weghalen, en daarna pas het omlijnings-hooglicht. Die volgorde heb ik per deel gevolgd.
- **Scheiding met kleur op een naad:** lijnen tussen twee kleurvlakken (de gezichtsschijf tegen de vacht) zijn de omlijningsbasis van het lichtste vlak, niet zwart. Dat geldt ook voor het indigo randje rond de schijf.
- **Recolor-regel 4: lichte kleuren houden een donkere omlijning.** Daarom heeft de lila wang links indigo en niet de lila schaduwtint. Die zou bij zo'n lichte kleur wegvallen.
- **Pikachu: het extreme hooglicht** (de schaduwkleur) gebruik je alleen op de allerlichtste randen. Dat is hier de kruin en de bovenkant van de spiraal.
- **Schaduwen iets naar blauw:** de violette ramp is naar blauw gedraaid en de lila schaduw ook (172,156,222).
- **Een staart achter het lijf** krijgt veel schaduw, behalve aan de bovenkant (Pikachu-revamp). Zo is de staartwortel en de buitenkant van de spiraal gedaan.
- **Oog = kraal:** "beady eyes should always have a white spot of shine and a coloured reflection opposite". Dat staat in de gids bij *Shine*. Hier is het iris + glans + weerkaatsing + pupil.
- **Niet groter dan nodig** (Scratch/Pixel-over): "don't make it larger than that for the hell of it". Het oppervlak is daarom teruggebracht van 1172 naar 1047. Zie hieronder.

## Eigen oordeel
- **Beter dan ronde 6:** hij oogt minder als een sticker. De 3/4-houding en de halfgesloten cyaan ogen geven de blik die Jordi in ronde 4–5 goed vond. De staart groeit zichtbaar uit het lijf en de spiraal leest op 1× als krul.
- **Nog zwak:** het oppervlak is met 1047 px groter dan de ±800–950 van de opdracht. Dat komt door de grote kop uit concept B (±54% van de hoogte) en de lange staart. Hij ligt tussen Umbreon (1069) en Espeon (1101), boven Treecko (967). Kleiner maken kost de tarsierkop of de spiraal: dat is een keuze voor Jordi.
- De hand-op-de-knie is klein en leest vooral als twee roze stipjes.
- De lila buik zit grotendeels achter de knieën.
- Of hij "op een Pokémon lijkt", blijft een blinde test voor de hoofdsessie (niet hier gedaan).

## Bestanden
- `anim_front.png` (64×128, 2 frames), `normal.pal`, `compare.png`
- `bron/nachtaap.py`: de rasters per lichaamsdeel en het palet. Draaien vanuit de repo-root: `python3 docs/concept/sprites/nachtaap/ronde7/bron/nachtaap.py docs/concept/sprites/nachtaap/ronde7`
- `bron/raster_f1.txt` en `raster_f2.txt`: het volledige eindraster per frame
- `bron/lib.py`: alleen rasters neerleggen en opslaan
- `bron/vellen.py`: de vergelijkingsvellen van beide soorten
