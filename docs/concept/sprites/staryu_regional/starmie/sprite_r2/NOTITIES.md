# Regionale Starmie, frontsprite ronde 2

Bestanden: `starmie_r2.png` (A, achterster DY+3), `starmie_r2_varB.png` (B, DY+2), `vel.png` (8×: A | B | r1 | model op schaal | Gen 3 Starmie; 6× naast elkaar; 1× op wit en donker + model, Gen 3 Starmie, Staryu, maatstaf; 2×), `bouw.py`, `log_A.txt`, `log_B.txt`.
Bouwen: `cd starmie && python3 sprite_r2/bouw.py` (A) / `python3 sprite_r2/bouw.py 0 2 starmie_r2_varB` (B). Vel: `python3 gereedschap/vel2.py sprite_r2/vel.png sprite_r2/starmie_r2.png sprite_r2/starmie_r2_varB.png`.

## Opdracht (Claude, r2)
Voorste ster, juweel, glazuur, zigzag en hagelslag van r1 blijven; de achterpunten worden de **achterste ster van de Gen 3 Starmie** (de donkere punten, set A in `gen3.py`), **verticaal gespiegeld**, met het middelpunt op het juweel, op Gen 3-schaal; herbelicht met licht linksboven; chips op het lichte vlak in een eigen chocoladetint.

## Achterster
- Gen 3-pixels van set A (paars 1–4 en zwart), gespiegeld om de kern (y → 60 − y; kern Gen 3 (31,5; 30), juweel sprite (31,30)), alleen waar de voorste ster ze niet bedekt. Geen pixel buiten de gespiegelde Gen 3-silhouet.
- **Positie:** precies op het juweel (DY 0) worden de punten ongelijk, omdat de armen van de modelster niet symmetrisch om het juweel liggen (de onderste inkepingen liggen lager). Lengte buiten de voorste ster per punt (grootste afstand van een achterpixel tot de dichtstbijzijnde voorste-sterpixel); de punten zijn genoemd naar hun Gen 3-naam, de plek na spiegelen staat erbij:

| verschuiving | onder (top) | rechtsonder (r) | rechtsboven (br) | linksboven (bl) | links (l) | spreiding |
|---|---|---|---|---|---|---|
| DX0 DY0 | 5,0 | 10,0 | 9,5 | 9,5 | 5,0 | 5,0 |
| DX0 DY+1 | 5,8 | 10,0 | 8,5 | 9,2 | 5,7 | 4,3 |
| **B: DX0 DY+2** | 6,7 | 10,0 | 7,6 | 9,1 | 6,4 | 3,6 |
| **A: DX0 DY+3** | 7,6 | 9,8 | 6,7 | 8,9 | 7,2 | **3,1** |
| DX−1 DY+3 | 7,2 | 8,9 | 6,3 | 9,8 | 7,8 | 3,5 |
| DX0 DY+4 | 8,5 | 9,5 | 5,8 | 8,5 | 8,1 | 3,7 |

  A (3 px lager dan het juweel) geeft de gelijkste punten; B (2 px lager) ligt dichter bij het juweel. In de echte Starmie verschillen de zichtbare punten ook (5–10 px). Geen gaten tussen achterster en voorste ster bij A en B.
- Pixels per punt (A): onder 53, rechtsonder 73, rechtsboven 63, linksboven 79, links 56 (B: 44, 73, 75, 86, 51).
- **Herbelichten:** per punt de as kern → tip; elke Gen 3-vlaktoon (1, 2, 3 en donkerste paars binnen de punt) hoort bij de kant van de as waar hij grotendeels ligt. De kant die naar linksboven kijkt wordt licht: lichtste toon daar = koek midden, de rest oranje; schaduwkant: donkerste toon = koek schaduw, de rest oranje. Donkerste paars op de rand van de punt = koek donker (lijn), zwart = zwart. De facetgrenzen zijn dus de Gen 3-grenzen (gespiegeld), alleen de tinten zijn omgedraaid.
- Daarna: buitenlijn rechts/onder zwart, links/boven koek donker; binnenlijn koek donker waar de achterster aan de voorste ster grenst; losse zwarte pixels → donker (A 2, B 5).
- **Chips:** 2 per punt, 2 px, in de nieuwe chocoladetint, op het lichte facet (koek midden), op pixels waarvan de 4 buren ook vulling zijn, zo dicht mogelijk bij de tip en ≥ 3 px uit elkaar (A: 18 px; onderpunt A heeft 1 chip, te smal voor 2). Plaatsing door script, geen bronpixel (het model heeft chips op andere plekken; zie r1).

## Palet (wat is samengevoegd)
**Gele hagelslag (15) samengevoegd met koek licht (6)**, nieuwe tint (250,218,128) (was koek licht (250,220,152), geel (250,214,40)). De drie gele hagelslagjes worden lichtgeel, de randglans van de koek iets geler. Plek 15 = **chocolade (124,80,56)** (de modelchip meet ±(128,84,56)), duidelijk anders dan de lijntint koek donker (116,58,24). Verder palet als r1. 16 kleuren incl. transparant.

## Diff per zone t.o.v. r1
- **Voorste ster (glazuur, zigzag, hagelslag, juweel): 0 indexwijzigingen** behalve de randpixels hieronder; de 6 gele hagelpixels hebben index 15 → 6 (samenvoeging, zelfde plek).
- **Rand voorste ster: A 26 px, B 28 px**, alleen waar r1 aan een achterpunt grensde en nu aan transparant (of omgekeerd): buitenlijn zwart rechts/onder (o.a. (35,14–18), (49–51,30–32), (45,33–35), (37,51)), koek donker links/boven (o.a. (14–17,20), (37–39,21), (15,39), (14,40), (14,43–44)). Lijst in `log_A.txt` / `log_B.txt`.
- **Achterster:** helemaal nieuw (A 324 px herbelicht, 59 buitenlijn, 24 binnenlijn, 18 chips); geen r1-achterpixel bewaard.
- A en B verschillen 215 px (alleen achterster en die randpixels).

## Metingen
- A: figuur x5–55, y6–56, **51×51, 1619 px**; B: 51×50, 1624 px (Gen 3 Starmie 55×51, 1673; r1 54×52, 1665). De gespiegelde Gen 3-achterster steekt minder ver uit dan de punten van r1.
- Controle (beide): 64×64, P, transparency 0, 16 kleuren; zwart 10,0 %; geen lichte kleur op de buitenrand; geen losse zwarte pixels. Vlekjes < 3 px in de achterster zijn de schuine 1-px facetlijnen van de Gen 3 (gespiegeld); L (38,23) en (39,46) zijn de lichtgele hagelslag; de overige zoals in r1.

## Twijfels
1. A ligt 3 px lager dan het juweelmidden (B 2 px); op het juweel zelf (DY 0) zijn onder en links maar half zo lang als de andere punten.
2. Na spiegelen hebben sommige punten een stompe, plankachtige vorm (vooral linksboven, de gespiegelde Gen 3-linksonderpunt): zo zien de zichtbare delen van de achterste Gen 3-ster eruit. Niet bijgewerkt.
3. Herbelichten is een ruil van de Gen 3-tinten per kant, geen nieuwe facetgrenzen; bij de onderpunt ligt toon 3 bijna op de as (−0,2), dus die facet is grotendeels schaduw.
4. De samengevoegde tint maakt de gele hagelslag bleker en de koekglans iets geler; alternatief is koek licht in koek midden opnemen (geel blijft dan fel, de randglans verdwijnt).
5. Chips blijven klein (2 px) en staan op het lichte facet, op 1× als stipjes.
