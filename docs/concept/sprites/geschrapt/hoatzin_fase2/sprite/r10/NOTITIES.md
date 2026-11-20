# Hoatzin fase 2, r10 (19 nov), maker: Gen 3-kleurronde per onderdeel, opnieuw vanaf r9

`sh alles.sh` bouwt alles opnieuw. `vel.png` = r10 | r9 | model | Archeops | Braviary (8x) + 1x/2x licht/donker, onderaan kop 12x r10 | model | r9.
Geometrie afgelezen op het model met `modelgrid.py` (spritecoördinaten); `modelcel.py` = gemiddelde modelkleur per spritecel.

## Studie (8x: Archeops, Braviary, Talonflame, Honchkrow, Mandibuzz, Staraptor, Toucannon, Decidueye, Pidgeot, Skarmory)
- **Pennen**: Braviary houdt de vleugel vlak (1 middentint) en scheidt pennen met korte donkere streepjes vanaf de achterrand + inkepingen in de zwarte buitenlijn; Talonflame/Pidgeot: per pen lichte bovenrand, midden, donkere scheiding. Belangrijker dan per-pen-detail: **grote licht/donker-indeling** (handpennen licht, dekveren donker, verre vleugel donkerder).
- **Kuif**: Staraptor/Pidgeot/Archeops: weinig grote plukken, punt taps, lichte bovenkant, basis versmelt met de kop als één massa; omlijnd.
- **Poten**: schenen 2-3 tinten met licht links, tenen met lichte bovenrij en donkere onderrij, zwarte klauwpunt; verre poot donkerder.
- **Les uit deze ronde**: 6 plukken of 8 pennen die elk licht/midden/donker krijgen geven tijgerstrepen; licht alleen op het buitenste deel van een pen (Braviary) en de kruin als massa houdt het rustig.

## Wat r10 doet (per onderdeel)
| onderdeel | hoe | bron vorm |
|---|---|---|
| nabije vleugel | 8 handpennen P1-P8, 4 dekveren C1-C4, voorrand I1-I3 en arm A1-A3 als middellijnen (`geom.py`, Voronoi); per pen licht bovenrand / midden / donkere 1-px scheiding; niveau per pen uit de modelhelderheid (handpennen licht L5/M4/D3, dekveren donker D3/D2/zwart, arm midden); zwarte scheiding pas op de buitenste helft | pentoppen en inkepingen uit pencapsules op het model |
| verre vleugel achter de kop | 5 lobben F1-F5 met ronde top, een stap donkerder (M4/D3/D2) | lobben uit het model |
| staart | 3 veren, D3 bovenrand / D2 / zwarte scheiding (buitenste helft) | r9-silhouet |
| kuif (`kuif.py`, met de hand) | 6 plukken (punten 6,9 · 11,10 · 16,10 · 23,7 · 26,12 · 29,19 uit het model), lichte kant 7, midden 6, schaduw 2; kruin als één massa met 2 plukgrenzen; hele haardos omlijnd (1 schaduwkant, 2 lichtkant, 2 over de verre vleugel) | model (kopm) |
| kop (`kop.py`, met de hand) | rond blauw gezicht 7x7 rond het oog (9 vlak, 8 rand rechtsonder); oog 5x5 rond (Sharpedo-vorm), zwarte ring, rode iris, zwarte pupil, glanspixel; snavel 3 grijstinten + omlijning | model |
| nek/lijf | modeltoon (lichte voorhals, donkere nekband) + licht linksboven, D2-lijn waar de vleugel over het lijf valt | model |
| buik | variant D, hooglicht-ovaal linksboven, sikkel onder/rechts | r9 |
| poten (`poten.py`, met de hand) | schenen 3 px (nabij F/E/2, ver E/2), tenen licht boven / donker onder, zwarte klauwen | model (legs.png) |

Palet (15 + transparant): lijn, mauve 4 (lum 46/81/125/163), bruin 2 (75/115, donker = mauve 2), blauw 2, rood, buik D 3, grijs 2.

## Afwijking t.o.v. r9 (kleur per pixel)
1868 px anders (bijna alles herkleurd); silhouet 232 px anders: pentoppen en inkepingen van de waaier, ronde lobben van de verre vleugel, kuifplukken en poten, allemaal naar het model.
Per zone anders/totaal: vleugel 739/781, verre vleugel 214/214, staart 170/170, lijf 201/232, buik 65/146, kop+kuif 512/868, poten 200/585.

## Eerlijk oordeel / zwakke punten
- Beter dan r9: scherp (geen vlakgemiddelde meer), oog rond, gezicht als blauwe vlek rond het oog, kuif als omlijnde bruine plukken, waaier met echte pennen en donkere dekveren, poten met klauwen.
- Nog zwak: het gebied tussen nek en vleugel (x 20-27, y 20-30) is een groot donker D2-vlak (in het model zwart met lichte streepjes; streepjes weggelaten tegen korrel). Snavel kleiner dan in het model (gezicht valt over de basis). De kuif blijft druk door 6 plukken; minder plukken zou van het model afwijken.
- Oogring zwart (oog A) gekozen i.p.v. donkerblauw: donkerblauw verdween tegen het blauwe gezicht.
- 1-px-diagonalen (penranden, plukranden) tellen als losse pixels in `vlek.py` (352 vs r9 343); geen dambord of om-en-om gevonden op het oog bekeken, niet per script getoetst.
