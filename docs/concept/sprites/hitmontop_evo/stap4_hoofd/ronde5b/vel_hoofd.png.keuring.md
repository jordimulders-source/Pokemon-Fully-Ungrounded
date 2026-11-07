# Keuring stap 4, hoofd ronde 5b (6 nov)

Bron: `vel_hoofd.png` en `hoofd.png`. Referenties: `../../referenties/hitmontop_anime.webp` (op het vel) en `graphics/pokemon/hitmontop/anim_front.png` (spritekop op het vel). Bekeken op 8× (PIL nearest) en op 1× (het vel), plus een pixeldump van `hoofd.png`. Coördinaten zijn schermpixels. Getoetst tegen dezelfde eisen als ronde 5 en tegen de 4 reparaties uit `ronde5/vel_hoofd.png.keuring.md`.

## Per eis
| eis | voldaan |
|---|---|
| Kop, haar en punt hetzelfde materiaal en dezelfde kleur, geen streep ertussen | ja. De schedel loopt vanaf y26 zonder lijn door in knot en punt. |
| Geen kippenpoot (geen vertakte lijnen) | ja |
| Enige streep hoog, als een fade | ja. Hij is kort, op (11–15, 30–32), met D aan de uiteinden en E in het midden. Hij staat 3 px boven de ogen en raakt de omtrek niet. Het is eerder een korte schuine haal dan een V, maar dat is acceptabel. |
| Ogen: zwarte rondjes met een wit puntje | ja |
| Mond is gewoon een streepje, onder de ogen | ja. Een recht streepje van 4 px, (17–18,44) en (19–20,43), op de gezichtsas onder het punt tussen de ogen. Tot de omtrek is 2 px vrij. |
| Kleinere punt zichtbaar | ja. De tip zit op (8,22), de voet is 2 px. De punt is klein en ligt maar 1 px boven de knot. |
| Haar opgeknot, knot duidelijk | ja op 8×: een ronde knot linksboven op de kruin, met een lichtvlak. Op 1× is hij matig: een bult linksboven, zie de opmerkingen. |
| Hoofd tegen de klok in gedraaid | ja |
| Leest rechtop (niet kaal met baard en niet ondersteboven) | ja |
| Simpel, zoals alle Hitmons | ja |
| Gesloten omlijning | ja |
| Geen restpixels | ja. De spike op (0,28) en de bult rechts op ooghoogte zijn weg. De rechteromtrek loopt recht op x24, y33–40. |

## De 4 fouten uit ronde 5
1. Mond U-vormig en tegen de rand: **weg**.
2. Fadestreep raakte de omtrek: **weg**. Hij is nu kort en ligt vrij van de omtrek.
3. Restpixels (spike en bult): **weg**.
4. Knot leek een oor, punt een spriet: **opgelost**. De knot zit op de kruin, niet meer op oorhoogte, en de punt heeft een voet.

## Nieuw
- De keep tussen knot en punt loopt als een zwarte lijn van 2 px door, op (6,24–25), en eindigt open in de huid. Hij vertakt niet en leest op 8× als scheiding van twee bulten. Het is geen fout, maar houd het bij 2 px.

## Lijkt op en wijkt af in
- **Lijkt op Hitmontop in:** de ogen, de huidtinten, één doorlopende omtrek, de vlakke mond (zoals de anime) en de eenvoud.
- **Wijkt af in:** de strenge blik. Zonder fronslijn blijft het gezicht vriendelijk en wat leeg. Dat volgt uit Jordi's eis dat de streep hoog als fade staat, dus het is geen fout.

## Opmerkingen
- Op 1× smelten knot en punt tot één bult linksboven. Dat is pas echt te beoordelen als het hoofd op de vorm zit: kijk dan of de knot nog als knot leest naast het lijf.
- De fadestreep is op 1× bijna onzichtbaar. Dat past bij "een beetje als een fade".

Oordeel: PASS
