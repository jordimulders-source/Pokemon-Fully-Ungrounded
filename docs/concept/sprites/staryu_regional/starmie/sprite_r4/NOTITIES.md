# Regionale Starmie, frontsprite ronde 4 (model 1-op-1)

Koerswijziging (Jordi via Claude): "waarom neem je het model niet over?", "je maakt hem ook steeds rechter", "steeds minder driekwart pose". De Gen 3-achterster en de kleinere voorste ster (r2/r3) zijn eruit. Het hele model `gemini/r3_starmie.webp` is overgenomen, voorste én achterste ster, op schaal 0,66 (zoals r1), met de perspectief van het model.

Bestanden: `starmie_r4_A.png` (achterpunten = reductie van het model), `starmie_r4_B.png` (idem, achterpunten puntiger binnen hun eigen modelsilhouet), `kaal_starmie_r4_A.png` / `kaal_starmie_r4_B.png` (voorste ster na de r1-stappen + kale reductie van de achterpunten, vóór de lijnen), `vel.png` (8×: A | B | r1 | model op schaal | Gen 3 Starmie; 6× naast elkaar; 1× op wit en donker + model, Gen 3, Staryu, maatstaf; 2×), `bouw.py`, `puntig.py` (alleen B), `log_A.txt`, `log_B.txt`.
Bouwen: `cd starmie && python3 sprite_r4/bouw.py starmie_r4_A` / `python3 sprite_r4/bouw.py starmie_r4_B`; vel: `python3 gereedschap/vel2.py sprite_r4/vel.png sprite_r4/starmie_r4_A.png sprite_r4/starmie_r4_B.png`.

## Werkwijze
- **Voorste ster:** precies de r1-stappen op schaal 0,66 (kale reductie, zigzag projectie + uitdunnen tot 1 px, juweelfacetten projecteren, ontkorrelen, koek in glazuur).
- **Achterpunten (A):** oppervlakgewogen reductie van het natieve model (figuur buiten de voorste-stermasker). Klassen per modelcel: zwart (L < 60), chip (grijsbruin: b ≥ 40, r < 150, L < 115; alleen compacte clusters ≤ 6 cellen die niet aan de voorste ster of de achtergrond grenzen, de rest zijn lijnen) en koek. Regels: zwart ≥ 30 %, chip ≥ 30 %, anders een koektint naar de gemiddelde modelhelderheid (zelfde drempels als de rand van de voorste ster). Daarna ontkorrelen (72 px), buitenlijn (rechts/onder zwart, links/boven koek donker), binnenlijn koek donker waar een achterpunt aan de voorste ster grenst, losse zwarte pixels → koek donker.
- **Chips uit het model:** 17 px chocolade, alleen op de punten linksboven en rechtsboven, op de modelplekken (het model heeft op de onderste punten geen chips). Er zijn geen chips bijgezet.
- Palet zoals r2/r3: gele hagelslag samen met koek licht (250,218,128); plek 15 = chocolade (124,80,56). 16 kleuren incl. transparant.
- In het model zijn vier achterpunten zichtbaar (linksboven, rechtsboven, links-laag, rechts-laag); de vijfde zit onder de ster verborgen en is dus ook in de sprite niet te zien.

## Perspectiefmeting (driekwart van het model blijft)
Hoek en lengte van elke armpunt vanaf het juweelmidden (model natief × 0,66 tegen sprite A):

| arm | model hoek | sprite hoek | model lengte | sprite lengte |
|---|---|---|---|---|
| boven | 94,6° | 97,1° | 24,5 | 24,2 |
| rechts | 14,0° | 14,6° | 24,5 | 23,8 |
| rechtsonder | −58,3° | −57,5° | 26,4 | 26,1 |
| linksonder | −124,4° | −124,8° | 28,0 | 28,0 |
| links | 168,1° | 166,5° | 25,6 | 25,7 |
| achter linksboven | 126,3° | 124,8° (B 127,7°) | 27,9 | 28,0 (B 27,8) |
| achter rechtsboven | 57,1° | 55,7° (B 55,7°) | 26,7 | 26,6 (B 26,6) |
| achter rechts-laag | −25,3° | −25,6° (B −23,5°) | 26,3 | 25,5 (B 25,1) |
| achter links-laag | −153,4° | −154,4° (B −156,3°) | 28,0 | 27,7 (B 27,3) |

Afwijking ≤ 2,5° en ≤ 0,8 px (rastermeting op de verste pixel). De kanteling blijft: de onderste armen zijn langer (26–28) dan de bovenste (24–25), en de armen staan niet op gelijke afstanden van elkaar (tussenruimtes 80°, 72°, 67°, 67°, 74°); niets is rechtgezet of symmetrisch gemaakt.

## Afwijkingen
- **Voorste ster tegenover r1:** 36 px, alleen randpixels waar de buur verandert (Gen 3-punt in r1 → modelpunt of transparant): buitenlijn/binnenlijn (o.a. (25–26,10–16), (34–35,10–13), (42–46,21), (10–15,30–33), (14–15,40–42), (14,47–49), (45,37–38), (45,47), (37,51)). Glazuur, zigzag, juweel en hagelslag 0 (gele hagelslag: zelfde plek, samengevoegde tint).
- **A tegenover de kale samenstelling:** voorste ster 36, achterpunten 130 (ontkorrelen 72, buitenlijn, binnenlijn, 3 losse zwarte pixels → donker); silhouetverschil 0.
- **B tegenover de kale samenstelling:** voorste ster 38, achterpunten 304; silhouetverschil 48 (alleen weggehaald).

## Versie B: puntiger binnen het modelsilhouet
Per punt (`puntig.py`): as = juweelmidden → zwaartepunt van de punt (richting van het model); tip = de silhouetpixel die het verst langs de as reikt (bij gelijke lengte die het dichtst bij de as); voet = de twee uiterste pixels die aan de voorste ster grenzen. Alles buiten de twee lijnen tip–voet wordt transparant; er komt geen pixel bij (B heeft 0 pixels buiten het A-silhouet). Kleur: de facet aan de kant naar linksboven koek midden, de andere oranje, gescheiden door de lijn voetmidden–tip, zoals het lichte en donkere vlak van de Gen 3 Starmie-punten; modelchips die blijven staan, blijven.
**Weg per punt:** linksboven 14 px, rechtsboven 11, links-laag 12, rechts-laag 11 (48 in totaal). Richting en lengte: zie de tabel (B-waarden).

## Metingen en controle
- A: figuur x6–54, y6–53, **49×48, 1753 px**; B: 49×48, 1705 px (Gen 3 Starmie 55×51 / 1673; r1 54×52). Op 0,66 is de figuur smaller dan ±55×51, omdat de achterpunten van het model nauwelijks buiten de voorste ster komen. 55 breed zou schaal ±0,73 vragen; dan wordt ook de voorste ster opnieuw gereduceerd (niet gedaan, r1-voorkant was goed).
- Beide: 64×64, P, transparency 0, 16 kleuren; geen lichte kleur op de buitenrand; geen losse zwarte pixels; zwart A 8,0 %, B 6,7 %. Kleine vlekjes: L = lichtgele hagelslag en randglans in de bovenarm (zoals r1), M = glanspixels op de koekrand.

## Twijfels
1. In A zijn de achterpunten bovenaan brede, ronde koeklobben (zoals het model), en onderaan korte stukjes die net buiten de ster uitsteken. Op 1× lezen vooral de twee bovenste.
2. In B worden de bovenste punten "kattenoren" met een scherpe hoek naar buiten; de facetsplitsing is een rechte lijn (licht/oranje), zoals de Gen 3. De onderste punten veranderen weinig, ze zijn klein.
3. De vijfde (onderste) achterpunt ontbreekt, zoals in model r3.
4. Figuur 49×48 is kleiner dan de Gen 3 Starmie.
