# Nachtaap fase 1 (Psychic-starter): front-sprite

Bestanden: `anim_front.png` (64×128, 2 frames, 16 kleuren, index 0 transparant), `normal.pal` (JASC), `compare.png` (naast Treecko/Torchic/Mudkip/Zigzagoon en buren met hetzelfde oppervlak, op 3× en 1×). Nog geen back en icoon.

## Ontwerp
- **Dier en proporties:** een jonge nachtaap (grijsbruine vacht, oranje borst/buik, kleine ronde oren) met de bouw van een tarsier: kop zo breed als het lijf met de dijen, ogen van 10×10 px (samen bijna de hele kopbreedte), een klein lijfje, lange dunne vingers met crème kussentjes en lange voeten.
- **Nachtaap-gezicht:** witte halvemaanvlekken boven de ogen, een donkere middenstreep op het voorhoofd, een zijstreep aan de verre kant en een lichte snuit met een kleine neus.
- **Eng maar zacht:** in frame 1 kijkt hij met **kleine pupillen** (de starende tarsierblik, licht van boven overschaduwd door de "oogleden"). In frame 2 worden de **pupillen wijd**, gaat zijn mond open en steekt hij een hand op met gespreide vingers (een groet, of een Psychic-gebaar). Het contrast tussen de twee frames vertelt het karakter: hij ziet er eng uit, maar is lief.
- **Nazca-spiraal:** de dunne staart loopt achter het lijf omhoog en eindigt in een opgerolde krul van ±1¼ slag. In frame 2 komt de krul 2–3 px hoger.
- **Maan:** de onderste rand van de iris is lichter (index 11) en vormt een sikkelmaantje onder de pupil. Een zilveren variant (index 11 = #e6eef6) is geprobeerd, maar leest als oogwit onder de iris (een "bezorgde" blik). Daarom bleef het bleekgoud. Het maanmotief kan later met de varianten/shiny sterker worden.
- **Pose:** driekwart naar links, zittend als een kikker (tarsierhouding): de handen liggen op de knieën en de voeten staan met de tenen naar buiten op dezelfde rij (y 57). Frame 2 springt niet: de kop gaat 1 px omhoog en de nabije arm omhoog.
- **Stijl:** licht van linksboven, selout (boven/links de donkerste tint van het eigen onderdeel, rechts/onder zwart), 1 px lijnen, ramps van 3–4 tinten, een smalle dithering-overgang (1–2 px) op kop en dijen, de omlijning #101010 op index 15.

## Paletindeling (recept-formaat, §5)
```
'nachtaap': {'vacht': [1, 2, 3, 4], 'creme': [5, 6, 7], 'buik': [8, 9, 10], 'ogen': [11, 12, 13], 'wit': [14]}
```
| index | kleur | onderdeel |
|---|---|---|
| 0 | #94cd9c | transparant |
| 1–4 | #e6d5c5 #b4a494 #8b7b7b #625262 | vacht licht→donker (basis = 2; 4 = selout, strepen, contourlijnen) |
| 5–7 | #fff6de #decdac #a4947b | crème: vlekken boven de ogen, snuit, vinger- en teenkussentjes |
| 8–10 | #ffcd8b #e6a45a #a46239 | oranje borst/buik (10 ook de binnenkant van de open mond in frame 2) |
| 11–13 | #ffee94 #eeac31 #a45a18 | iris: 11 = sikkelmaantje onderaan, 13 = schaduw onder het ooglid |
| 14 | #ffffff | glans in de ogen (alleen daar) |
| 15 | #101010 | omlijning, pupillen, neus, mondlijn |

De basistint is per ramp de meest gebruikte (vacht 2: 267/307 px tegen 3: 249/264). De ogen hebben een eigen groep, net als de kussentjes (crème) en de buik.

## check.py (`--stage 1`)
- Geen FOUT.
- LET OP **rand: aandeel zwart 0,625** (Hoenn fase 1 p90 0,578): bewust, volgens het in-game-contrast uit §0 van het plan (in-game sprites hebben ±55–58% zwart). Het zit vooral onder de voeten, aan de rechterkant van de kop en in de staart.
- LET OP **geen back.png / icon.png**: niet gevraagd in deze stap.
- OK: hoogte 49, breedte 44, oppervlak 1302 (Hoenn fase 1: mediaan 40 / 42 / 912; Treecko is 48 hoog), 15 kleuren, lichtrichting −0,31/−0,21, schaduw 0,47, dithering 0,05, 21 losse pixels, zwarte binnenlijnen 0,10 (ogen), frameverschil 0,43.
- species_info: `.frontPicSize = MON_COORDS_SIZE(56, 56)`, `.frontPicYOffset = 6`.

## Wat nog beter kan
- Hij is **zwaarder dan Torchic/Mudkip** (oppervlak 1302 tegen ±900) door de brede dijen en de lange staart. Een babytarsier mag kleiner en ijler: de dijen kunnen 2–3 px smaller en het lijf 1–2 px lager.
- De **handen op de knieën in frame 1** lezen als streepjes. De lange vingers zijn pas in frame 2 echt te zien (de opgeheven hand).
- De verre arm valt aan de schaduwkant weg tegen het lijf.
- Bron: de schets en de handrijen staan in de scratchpad (`sprite_nachtaap/build.py`, `f1.py`, `f2.py`). De vormen worden procedureel getekend, de kop, ogen, ledematen en handen per pixel als tekstrijen.
