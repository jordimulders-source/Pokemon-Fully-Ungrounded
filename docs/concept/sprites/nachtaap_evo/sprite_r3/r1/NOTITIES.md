# Moonkey r1: frontsprite naar Gemini r3 (19 nov)

## Wat ik deed (volgorde = scripts, draaien vanuit `sprite_r3/`)
1. `raster.py`: natief raster gemeten op randsterkte: pitch 16,00 px, celgrens op modelpixel 15 (x en y gelijk). Controle `raster_over_model.png` (rood raster over de kop: valt op de pixelgrenzen; spreiding per cel max 8,5, geen enkele gemengde cel).
2. `natief.py`: mediaan van het midden (8×8) per cel → `natief.png` (63×63; figuur 58×54, natief x3–60, y7–60; `natief_10x.png`). Niet verder verkleind.
3. `quant.py`: kale reductie naar het **oude palet** (`oude_normal.pal`, ongewijzigd) per kleurgroep op helderheid (lijn/paars, wit, lichtblauw, rood, crème/bruin). Achtergrond = floodfill vanaf de rand (het lijngat links in de kop alleen voor de floodfill dicht). Figuur 2 px omlaag: x3–60, y9–62 (oud: x3–61, y8–62).
4. `bewerk.py`: alle afwijkingen van de kale reductie, elk met coördinaat, zone en reden (`python3 r1/bewerk.py` drukt de lijst af).
5. `controle.py` (kleuren, lichte kleur op de buitenrand, tintvlakjes, losse pixels, losse lijnpixels), `vel.py` → `vel.png`, `zoom.py` (uitsnede 14× naast het model).

## Afwijkingen van de kale reductie (150 px)
| Zone | px | Wat |
|---|---|---|
| staart | 25 | wit binnen de krul = ingesloten achtergrond van het model → transparant (zoals de oude sprite). |
| ogen (toegestaan 1) | 16 | oude oogpixels; de oude sprite 1 px links + 1 px omlaag valt precies op de oogplek van het model (pupillen, glans en rood zijn al pixel-gelijk). Verschil zit alleen in de wenkbrauwlijn y44 (8 px → 2) en de bovenste roodrij y45 (4 px), (10,46),(14,46) → B, (5,48),(6,49) → 9. |
| maan bovenkop y35–42 (toegestaan 2) | 31 | buitenrand = model (lijn, linkeroor, oor rechts). Wit tot aan de lijn zoals de oude maan. Rechterrand als in de oude sprite: rand 7 schuin van (15,35) via (17,36), (18,37) naar x19 (y38–42), dan paarse band 5/4 en een binnenlijn 2 op x22 (y40–42) tegen het verre oor; inham 77 op (13–14,42). 18 px wit → paars/lijn, 11 px wit ↔ 7, 2 overig. |
| maan + gezicht y43–52 (toegestaan 2) | 70 | rij voor rij de oude sprite (zelfde verschuiving als de ogen): voorhoofd, maanpunten langs de ogen (links x4, rechts x19–20, tot y49), snuit en mond. 52 px wit → paars: de witte ring van het model rond en onder de ogen verdwijnt; 8 px paars → wit (maanpunten), 6 wit ↔ 7, 4 tint. Buitenlijn en transparant blijven van het model (kin links 1 px smaller dan oud). |
| kop L | 1 | (3,42): gat in de buitenlijn van het model → lijn 2. |
| kin L | 1 | (6,53): 4 op de buitenrand → lijn 2 (sluit aan op (5,52)). |
| rug/staartaanzet | 2 | (42,34) 5, (43,34) 4 → 6: één lavendel hooglichtvlakje i.p.v. drie tinten op 2 px. |
| lijf R | 1 | (46,38) 2 tussen 1-en → 1 (geen zwart/donkerlila om en om). |
| arm L | 1 | (7,57) 3 op de bovenrand → selout 2. |
| voet midden | 2 | (17,61) crème hoekpixel zonder lijn → bruin 14 (zoals de teenrand (16,60)); (19,59) losse lavendel pixel in de teen → D zoals (18,59). |
| lijf, poten, staart (vorm), rugwiggen, linkeroor, kopvorm | 0 | 1-op-1 uit het model. |

Geen pixel is getekend buiten de lijst: alles komt uit de reductie, de oude sprite (ogen/maan/gezicht) of de technische reparaties hierboven.

## Controle
- 15 kleuren + transparant (index 0); `anim_front.png` 64×128 P-modus, transparency=0, frame 2 = kopie. `normal.pal` = oude palet, byte-gelijk.
- Geen lichte kleur op de buitenrand (bruin/donkerbeige op de teenranden telt als teenlijn, zoals in de oude sprite); geen losse omlijningspixels; geen open randen.
- Tinten per kleurgroep: paars 2–6 (lijn 1, selout 2, schaduw 3, basis 4, licht 5, hooglicht 6), wit 8 + 7, blauw F, rood 9/A/B, crème C/D/E.
- Losse pixels die over zijn, allemaal modelpixels of oude-spritepixels: oogglans (7,46),(16,46), neus (10,52), 1-px lijnstukjes op diagonale randen, de krulpunt van de staart (53,14), de oorpixel (23,38), de schouder-/heupdetails (31,45),(36,45),(38,47) en de teenpixels.
- Lavendel pixel (19,59) in de middelste voet (model) was een los vlekje: zelf gerepareerd (→ D).

## Zwakke punten die ik zelf nog zie (eerlijk)
- **Rug/staartaanzet (x40–48, y30–36)**: het model heeft hier een drukke overgang (laatste blauwe wig in stukjes, lavendel vlekje, lijnen). Model-trouw gelaten op 2 px na; leest op 1× als de rugbult die in de staart overgaat, op 8× wat rommelig.
- **Lijf vlakker dan de oude sprite**: kleur en schaduw komen uit het model (basis 4, sikkel 3 rechts/onder, licht 5 op de schouder); de oude sprite had meer volume op de bult. Geen kleurronde gedaan: die verandert het model, eerst vragen.
- **Binnenlijn rechts naast de maan (x22, y40–42)**: het model heeft daar geen lijn (wit raakt het verre oor); nodig omdat de paarse band anders in het oor overloopt. Benoemd als deel van toegestane afwijking 2.
