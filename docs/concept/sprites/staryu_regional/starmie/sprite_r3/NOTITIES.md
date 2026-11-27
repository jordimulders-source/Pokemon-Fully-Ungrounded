# Regionale Starmie, frontsprite ronde 3 (C1/C2)

Bestanden: `starmie_r3_C1.png` (schaal 0,60), `starmie_r3_C2.png` (schaal 0,55), `kaal_starmie_r3_C1.png` / `kaal_starmie_r3_C2.png` (voorste ster na de r1-stappen + ruwe achterster, vóór lijnen en chips), `vel.png` (8×: C1 | C2 | r2 A | r1 | model op schaal | Gen 3 Starmie; 6× naast elkaar; 1× op wit en donker + model, Gen 3, Staryu, maatstaf; 2×), `bouw.py`, `log_C1.txt`, `log_C2.txt`.
Bouwen: `cd starmie && python3 sprite_r3/bouw.py 0.60 -1 3 starmie_r3_C1` en `python3 sprite_r3/bouw.py 0.55 -1 1 starmie_r3_C2`; vel: `python3 gereedschap/vel2.py sprite_r3/vel.png sprite_r3/starmie_r3_C1.png sprite_r3/starmie_r3_C2.png sprite_r2/starmie_r2.png`.

## Opdracht (Claude, r3)
Voorste ster uit het model kleiner (verhouding van de echte Starmie), juweelmidden op de Gen 3-kern, daarachter de verticaal gespiegelde donkere Gen 3-achterster op ware grootte, zo verschoven dat de vijf punten even ver uitsteken; herbelichting en chips zoals r2; voorste ster opnieuw reduceren met de r1-stappen.

## Metingen
- **Tips van de lichte voorste Gen 3-ster** (afstand tot de kern): 26,2 / 27,5 / 27,4 / 28,2 / 26,6 px (gem. 27,2). Tips van de donkere achterster: 23,3 / 27,7 / 28,2 / 28,4 / 26,6.
- **Tips modelster** (natief, tot het juweelmidden): boven 37,0, rechts 36,7, rechtsonder 41,3, linksonder 42,4, links 38,8 (gem. 39,2). Armpunten even ver als de Gen 3-voorste ster → **schaal 27,2/39,2 = 0,69**, dus groter dan r2 (0,66). Dat lost het niet op: in de Gen 3 reiken beide sterren even ver, en het verschil zit in de dikte van de armen (de koekster heeft brede, ronde armen en ondiepe inkepingen, de Gen 3-ster smalle punten).
- Daarom gemeten op **oppervlak**: de voorste Gen 3-ster + kern is 1120 px; de modelster heeft dat bij schaal ±0,61 (0,60 → 1066 px). **C1 = 0,60.** **C2 = 0,55** (900 px), om de punten verder uit te laten steken.
- **Uitsteken in de echte Starmie** (zelfde maat: grootste afstand van een achterpixel tot de dichtstbijzijnde pixel van de voorste ster): 8,2 / 10,0 / 12,0 / 12,0 / 10,6 (gem. 10,6); 553 px achterster zichtbaar.
- Verschuiving per schaal gezocht over DX −1…1, DY −1…4 (zo klein mogelijke spreiding, geen losse delen, zo min mogelijk gaten).

## Uitsteeklengtes per punt (px buiten de voorste ster)

| | onder | rechtsonder | rechtsboven | linksboven | links | gem. | spreiding | achterster zichtbaar |
|---|---|---|---|---|---|---|---|---|
| Gen 3 Starmie | 8,2 | 10,0 | 12,0 | 12,0 | 10,6 | 10,6 | 3,8 | 553 px |
| r2 A (0,66, DY+3) | 7,6 | 9,8 | 6,7 | 8,9 | 7,2 | 8,0 | 3,1 | 324 px |
| **C1 (0,60, DX−1 DY+3)** | 8,5 | 10,0 | 7,6 | 10,2 | 9,2 | 9,1 | 2,6 | 399 px |
| **C2 (0,55, DX−1 DY+1)** | 7,6 | 11,0 | 10,8 | 12,1 | 9,2 | 10,1 | 4,5 | 438 px |
| (0,50, DX+1 DY+3) | 11,7 | 14,0 | 11,4 | 10,3 | 9,9 | 11,5 | 4,1 | niet gebouwd |
| (0,45, DX+1 DY+2) | 12,1 | 15,0 | 13,6 | 11,7 | 10,6 | 12,6 | 4,4 | niet gebouwd |

(Punten genoemd naar hun plek na spiegelen; in de Gen 3 heten ze top/r/br/bl/l.)

## Figuurmaat
- C1: x4–54, y8–56, **51×49, 1465 px**; C2: x4–54, y6–54, **51×49, 1338 px** (Gen 3 Starmie 55×51 / 1673). **±55×51 is met een ongeschaalde Gen 3-achterster niet te halen:** de gespiegelde achterster zelf is 51 breed, en in de Gen 3 komt de rest van de breedte van de lichte voorste ster, die hier de kleinere koekster is. Groter worden kan alleen door de achterster te schalen (niet gedaan, opdracht: ware grootte) of de koekster groter te maken (dan steken de punten minder uit, zie r2).

## Stappen en afwijkingen (C1 / C2)
- **Voorste ster** opnieuw uit het model op de nieuwe schaal, zelfde regels als r1: kale reductie, zigzag projectie + uitdunnen tot 1 px (C1 77 px, C2 zie log), juweelfacetten projecteren (C1 18 px), ontkorrelen (C1 112 px), koek in glazuur (C1 1 px: (19,43)).
- **Achterster:** gespiegelde Gen 3-set A, herbelicht zoals r2 (C1 398 px).
- **Gaten gevuld: C1 1 px (25,48), C2 4 px (43–44,36–37 e.o.).** Daar lag in de Gen 3 de voorste ster of kern over de achterster en nu niet meer; tint van de dichtstbijzijnde achterpixel. Dit zijn de enige pixels buiten de Gen 3-silhouet.
- Buitenlijn (C1 102), binnenlijn achter (C1 23), losse zwarte pixels → donker (C1 7), chips (18 px per variant: 2 per punt, onderpunt 1). Alle coördinaten in de logs.
- Palet zoals r2 (gele hagelslag samen met koek licht (250,218,128), 15 = chocolade (124,80,56)); 16 kleuren incl. transparant.

## Controle
Beide 64×64, P, transparency 0, 16 kleuren; geen lichte kleur op de buitenrand; geen losse zwarte pixels; zwart C1 10,6 %, C2 12,4 %. Kleine vlekjes: facetlijnen van de Gen 3 in de achterster, lichtgele hagelslag (L), M-glanspixels op de koekrand.

## Wat leest er nog op de kleinere maat
- **C1 (0,60):** zigzaggen lezen nog als zigzag op alle armen (5 lijnen, doorlopend); juweel nog een achthoek met licht facet linksboven en donkere onderfacetten; hagelslag allemaal aanwezig (1–4 px); koekrand 2–3 px, onderrand dikker.
- **C2 (0,55):** zigzag in de bovenarm wordt een klein "A"-vormpje en de andere lijnen worden korte haakjes; juweel nog achthoekig maar met minder facetten; hagelslag staat dichter op elkaar; koekrand op plekken 1–2 px. Zwart neemt toe (12,4 %) omdat de rand een groter deel van een kleinere ster is.

## Twijfels
1. Het verschil met de echte Starmie zit in de vorm van de koekster (dikke armen), niet in de maat: bij gelijke tipafstand bedekt hij veel meer van de achterster. C1 komt in oppervlak en uitsteken het dichtst bij de Gen 3 (gem. 9,1 tegen 10,6); C2 haalt de Gen 3-lengtes bijna (10,1) maar levert detail in.
2. Figuur is in beide 51×49, kleiner dan de Gen 3 (55×51).
3. De onderpunt blijft de kortste (7,6–8,5), net als in de Gen 3 (8,2).
4. Rechtsboven in C1 (7,6) is korter dan de rest; een andere verschuiving maakt dan links of onder korter.
