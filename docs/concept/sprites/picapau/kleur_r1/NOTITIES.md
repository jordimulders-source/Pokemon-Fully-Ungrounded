# Picapau kleur r1: notities (maker, 5 nov)

Bestanden: `raster.txt` (met de hand, 64x64, één teken per palettekleur), `bouw.py` (raster → `picapau.png` geïndexeerd, index 0 transparant, + `normal.pal`), `controle.py` → `controle_uitvoer.txt`, `vel.png` (1x boven, 8x onder: Taillow, Picapau, Pikachu), `STUDIE.md`.

Palet (15 + transparant): k zwart · 1/2/3 roomgeel licht/basis/schaduw · 4 goudbruine selout · d/b/r donkerbruin/bruin/roodbruin · c/C wang · p snavel licht · w glans · g/G poot licht/schaduw · e iris.

## Controle (controle_uitvoer.txt)
- Silhouet: **0 px verschil buiten de zones**. In de zones 1 afwijking: **(16,17) +1 px, snavelpunt** (de snavelpunt was 1 px dik en las als een draadje; nu 2 px bij de punt).
- Open randen: 2 lichte teenpixels op de rand, **(29,46) en (28,47), tenen-zone** (zoals Taillow `6c6c6`; met omlijning blijft er geen teen over). Verder alle randpixels omlijningskleur (k, 4, d, G).
- Losse pixels: 0. Clusters < 3 px: 0 (uitgezonderd glans en het overgenomen Pikachu-oog).
- 819 px, bbox 36x55 (staart en kuif maken hem hoog; silhouet bevroren).

## Checklist (SPRITE_NORM / KERN)
| punt | stand |
|---|---|
| Leest op 1x als Pokémon / specht / Pikachu-achtig | ok: gele vogel met zwarte kuiftoppen, rode wang en Pikachu-oog leest meteen "Pikachu-achtig"; stijve staart + rechtop = specht. |
| 3/4 links-voor, kop meer naar kijker, één oog bij snavel | ok (uit het bevroren silhouet/model). |
| Ledematen vast aan het lijf | ok: pootjes groeien onder de buik uit, verre poot in schaduwtint G. |
| Ogen geïntegreerd, overgenomen | ok: Pikachu-oog 4x4 pixel voor pixel. |
| Licht linksboven, schaduw als sikkel | ok: hooglicht als vlek op kop en borst, sikkel onder de kop en langs de onderkant. |
| ≤ 3 tinten + omlijning per groep | ok (geel 3 + selout, bruin 3, rood 2, snavel p + geel, poot 2). |
| Zwart alleen schaduwkant, gekleurde selout lichtkant, niet om en om | ok: links goudbruin (rij 12–42), daaronder zwart; geen afwisseling. |
| Binnenlijnen in donkere tint van het vlak | ok: vleugelrand d, kop/snavel 4, knik in de staart d. |
| Geen open randen / lichte kleur op rand | ok behalve 2 teenpixels (gemeld). |
| Contrast ±30–40 per tint | ok (zie STUDIE). |
| Geen Pikipek-kopie | ok: andere kleuren, andere bouw. |

## Zwakke punten (eerlijk; Claude/keurder beslissen of het terug moet)
1. **Snavel is klein en dun** (3 px band in het silhouet): leest als snavel, maar niet als krachtige beitelsnavel. Dikker kan alleen door het silhouet te wijzigen (bevroren).
2. **Vleugel** is een lange, gelijkmatige strook langs de rug (zo in het model); de schubjes zijn kleine u-vormen en lezen op 1x als roomkleurige spikkels, niet duidelijk als schubben.
3. **Pootjes**: nabije en verre poot staan op dezelfde hoogte (silhouet) en lezen op 1x als één grijs plukje; alleen de tint onderscheidt ze.
4. **Buikonderkant**: rij 46 is een rechte zwarte lijn van 8 px (silhouet), dus daar een vlakke onderkant.
5. **Kuiftoppen** zijn 1–2 px breed: lezen als dunne zwarte puntjes, minder als Pikachu's brede oortoppen (±1 px in de kuiftoppen-zone kan ze iets verbreden als Claude/Jordi dat wil).

## Lessen
- Een hooglicht langs de bovenrand wordt meteen banding; leg het als vlek 1–2 px binnen de rand (kop en borst).
- Bij een 3 px dunne snavel kost omlijning aan beide kanten bijna alle vulling: bovenrand in de selout, onderrand zwart, en de ±1 px-zone bij de punt gebruiken.
- Het controlescript vond 16 mini-clusters (losse schaduwpixels, randpixels) die op het oog niet opvielen: eerst draaien, dan pas kijken.
