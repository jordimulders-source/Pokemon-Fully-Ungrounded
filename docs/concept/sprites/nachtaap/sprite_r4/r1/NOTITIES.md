# Nocticue r1: frontsprite naar Gemini r4 (19 nov)

## Wat ik deed (volgorde = scripts)
1. `raster.py`: natief raster gemeten op randsterkte: pitch 16,02 px, celgrens na modelpixel 14 (x en y gelijk). Controle: `raster_over_model.png` (rood raster over het model, valt op de pixelgrenzen; alleen rond oog en streep loopt Gemini een halve cel scheef).
2. `natief.py`: mediaan van het midden (8×8) van elke cel → `natief.png` (63×63, figuur 37×36, x14–50, y19–54; `natief_14x.png`). Niet verder verkleind.
3. `quant.py`: kale reductie naar het **oude palet** (`oude_normal.pal`, ongewijzigd): per kleurgroep (omlijning, pupil, oogroze, oogwit, crème, bruin, paars) op helderheid naar de oude tint. Achtergrond = floodfill vanaf de rand, dus het gat in de staartspiraal blijft gat. Daarna 1 px omlaag geschoven (onderkant y55, figuur x14–50, staart rechts).
4. `bewerk.py`: alle wijzigingen ten opzichte van de kale reductie, elk met coördinaat, zone en reden (`python3 r1/bewerk.py` drukt de lijst af).
5. `controle.py`: kleuren, lichte kleur op de buitenrand, tintvlakjes < 3 px, losse pixels, losse omlijningspixels. `vel.py` → `vel.png`.

## Afwijkingen van de kale reductie (96 px)
| Zone | px | Wat |
|---|---|---|
| kap (tintkeuze) | 27 | modeltoon L≈135 op de kap (y ≤ 27) → 4 i.p.v. 5; anders vallen de twee modeltonen (176 en 135) samen tot één vlak 5. Zo is de kap zoals de oude sprite: 5 linksboven, 4 de rest. Geen vormwijziging. |
| streep (toegestaan 1) | 45 | 3 px breed: 4 aan de lichtkant + 2 px kern 3 (de twee violette tinten van de oude sprite); begint op y24 als 2 px kern in de 4-kap, y25–28 op x22–24, op ooghoogte (y29–33) 1 px naar links (x21–23), y34 schuine punt (x22–23): volgt de kopronding, geen rechte onderkant. Vrijgekomen pixels (x20–21 en x24–25) → crème 7; het verre oog heeft nu een crème rand van 1 px (x20) aan de binnenkant. |
| kop boven (rand) | 5 | (22,21), (19,23), (18,24): 4 op de buitenrand → selout 3; (29,20), (30,20): 1 → 2 (de bovenrand ging 2,1,1,2,2,1 om en om). |
| oor L | 3 | (16,24), (17,24): halve randcellen (grijs in het model) → selout 2; (15,26): 3 tussen 2-en → 2. |
| oor R | 2 | (38,24): halve randcel → 2 zoals de buren; (36,26): 3 → 2 om de losse lijnpixel (36,27) aan het oorlijntje te verbinden. |
| oog R | 1 | (31,30): grijze antialiascel in de oogrand → oogrand 9. Verder alle oogpixels uit het model; ronde vorm (schuine hoeken) zat al in het model (toegestane afwijking 2 vergde niets). |
| kaak L | 3 | (18,37), (19,38): 4 op de buitenrand → 3; (21,39): 4 boven transparant → 1. |
| staart | 6 | (44,40–43): 5 op de buitenrand van de steel → 3; (44,39): losse 5 → 4; (47,37): 4 die aan het gat grensde → 2 (krulpunt dicht). |
| nek / been L / snuit | 3 | losse 1-px tinten weggepoetst: (25,41) 4→3, (23,50) 4→5, (21,36) 6→7. |
| gezicht, mond, poten, armen, knieën, handen, lijf | 0 | 1-op-1 uit het model (mond = 2 px bruin, neutraal). |

Geen pixel is getekend: alles komt uit de reductie, op de lijst hierboven na.

## Controle
- 14 kleuren + transparant (index 0), `anim_front.png` 64×128 P-modus, transparency=0, frame 2 = kopie. `normal.pal` = oude palet, byte-gelijk.
- Geen lichte kleur op de buitenrand; geen losse omlijningspixels.
- Tintvlakjes < 3 px die over zijn: oogdetails (glans C/B, pupil), 1-px selout op diagonale randen, het bruine oorvlekje (16,27), de bruine teenpixels en 1–2 px crème-schaduw onder het rechteroog (25–26,35) en de glans (20–22,35–36), (24,44): allemaal modelpixels.

## Zwakke punten die ik zelf nog zie (eerlijk)
- **Linkervoet**: de bruine teenpixels staan in het model als 2×2-schaakbord (D/7 op (19–20,52–53)). Model-trouw gelaten; leest op 1× als tenen, maar het is technisch een dambordje. Beslissing voor Claude/keurder.
- **Schaduw**: het model is vlak (rechterkant kop één toon), dus de sprite ook; geen sikkelschaduw zoals in de oude sprite. Bewust niet toegevoegd (opdracht: schaduw uit het model). Kleurronde naar Gen 3 kan later als Jordi dat wil.
- **Staartspiraal onderaan** (y38: 1,4,1,4,1) is de spiraalstructuur uit het model; op 8× druk, op 1× leest hij als krul.
- De stap van de streep op y28→29 (1 px naar links) is de enige "trap" in de streep; bedoeld als kopronding, maar een keurder kan hem hoekig vinden.
