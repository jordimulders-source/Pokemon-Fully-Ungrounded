# Hoatzin fase 2, r6 (19 nov), maker

Op r5 (`r5.png`), alleen kleur/toon; **silhouet 0 px anders** (assert in `r6.py`), niets getekend. `sh alles.sh` bouwt alles; log `r6.log`.
`vel.png` = r6 | r5 (buik D) | model | Taillow | Pidgeot, 8× en 1×/2× op licht en donker.

## Wat er gedaan is (Jordi: "D is het mooiste, maar de hele sprite is nog erg blurry")
1. **Buik D**: 11–13 = #4C2860 / #7C4498 / #B47CD6 (L 57 / 94 / 151).
2. **Toonstappen** (helderheid): mauve 2/3/4 + streep 5 = 42 / 82 / 125 / 177 (was 50 / 72 / 109 / 159; stap 40–52 i.p.v. 22–50, zoals Taillow/Swellow 51/81/108/141). Kuif licht 7 → #AC6032 (L 98 → 113, beter los van het mauve erachter, "kuif wat bruiner"). Overige tinten ongewijzigd (blauw 68/121, poten 69/133, kuif donker 64).
3. **Vulling mauve (lijf/vleugels, niet staart/strepen/lijnen/buitenrand)** opnieuw uit een gladde toonkaart van het model (venstergemiddelde r = 4 natieve px zonder lijnen en strepen); drempels uit de eigen toonverdeling: 1D-k-means 3 klassen (centra 42 / 84 / 104 → drempels 63 / 94). 329 px.
4. **Lijnen**: 2×2-zwartblokken binnen de figuur → lichtste modelcel naar de vlaktint (1 px). Zwart binnen de figuur (niet op de buitenrand) was al 3,7 % en is 3,6 % (Gen 3: Taillow 5,1, Pidgeot 3,5, Swellow 2,6); de 15 % voor index 1 is bijna helemaal buitenlijn (Gen 3 index-zwart incl. buitenlijn 8,5–12 %). Verder bleken de binnenlijnen al 1 px; niets meer verdund.
5. **Vlekjes < 6 px** (mauve en buik, 4-verbonden, buitenrand/selout overgeslagen) samengevoegd met de buurtint: 28 px. Vlekjes < 6 px in 2/3/4: 95 → 35 (rest: selout op de buitenrand en staart; kuifstrengen en strepen zijn bedoelde lijnen en bleven).

## Donker voor/na
| | r5 | r6 |
|---|---|---|
| index 1 (zwart) hele figuur / binnen | 15,0 % / 3,7 % | 15,0 % / 3,6 % |
| index 2 (donkerste mauve) hele figuur | 33,3 % (605 px) | 19,8 % (360 px; 150 daarvan staart, model daar ±35) |

## Afwijkingen per zone (px; figuur 1818)
| zone | px | t.o.v. r5 | t.o.v. onderlaag (stapA) |
|---|---|---|---|
| lijf/vleugel | 891 | 228 | 365 |
| vleugelstrepen-zone (alleen niet-streep-cellen herkleurd; streep 5 zelf 0) | 178 | 70 | 124 |
| kuif | 124 | 0 (alleen paletkleur 7) | 21 |
| gezicht / oog / snavel | 27 / 7 / 15 | 0 / 0 / 0 | 9 / 4 / 9 |
| buik | 161 | 4 (+ palet D) | 35 |
| poten | 73 | 0 | 30 |
| staart | 120 | 4 | 29 |
| modellijn | 219 | 34 | 110 |
| **totaal** | 1818 | **340** | 739 |

## Geprobeerd en niet gehouden
- Pengrenzen in de vleugelwaaier uit een modelgroefkaart (modelpixels ≥ 18 donkerder dan hun omgeving) als 1-px lijn: gaf weer korrel en donkere klonten (zelfde probleem als r5), dus weggelaten. De pennen lezen nu via de lichte strepen en het gekartelde silhouet.

## Resterende punten (voor de keurder)
- Bovenste waaier van de nabije vleugel is nu één rustig middenvlak met de bestaande strepen; minder "pennen" dan het model, wel scherp.
- Mauve heeft 3 vlaktinten + streeptint 5 (tekening, zoals Pidgeots strepen) + lijn.
- Staart blijft één donkere tint met de 1-px veerlijn, zoals het model (±35, egaal).
