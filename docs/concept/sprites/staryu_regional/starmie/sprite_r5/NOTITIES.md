# Regionale Starmie, frontsprite ronde 5 (model r4)

Model: `gemini/r4_starmie.webp` (Jordi: "doe maar r4"; "Deze was bijna goed, alleen geen driekwartpose en de punten zijn te puntig, dat moest meer als de normale starmie, alleen de punten minder puntig maken"). Pose zoals r4; de enige vormwijziging is het afstompen van de vijf achterpunten.

Bestanden:
- `starmie_r5_licht.png`: punten licht afgestompt (snede waar de punt 4 px breed is).
- `starmie_r5_sterk.png`: sterker afgestompt (5 px).
- `starmie_r5.png`: zonder afstompen (de reductie van het model na de technische stappen).
- `kaal.png`: kale samenstelling: voorste ster en achterpunten zoals de reductie ze geeft, vóór reparaties.
- `vel.png`: 8×: licht | sterk | zonder afstompen | kaal | model r4 op schaal | Gen 3 Starmie; 6× naast elkaar; 1× op wit en donker + model, Gen 3, Staryu, maatstaf; 2×.
- `bouw.py`, `stomp.py`, `gereedschap/` (`natief.py` → `natief_r4.png`, `voor_r4.py` (grenzen voorste ster/achterpunten), `puntmaat.py` (puntmeting), `vel5.py`, `pnaam.npy`), `log_licht.txt`, `log_sterk.txt`, `log_zonderstomp.txt`.

Bouwen: `cd starmie && python3 sprite_r5/bouw.py starmie_r5_licht 0.66 licht`, `python3 sprite_r5/bouw.py starmie_r5_sterk 0.66 sterk` en `python3 sprite_r5/bouw.py starmie_r5 0.66`. Vel: `python3 sprite_r5/gereedschap/vel5.py sprite_r5/vel.png sprite_r5/starmie_r5_licht.png sprite_r5/starmie_r5_sterk.png sprite_r5/starmie_r5.png sprite_r5/kaal.png`.

## Metingen
- **Raster r4:** pitch 10,24, fase x 9,25 / y 9,20; natief 99×99, figuur x7–90, y6–90 (84×85). Glazuur, zigzag, hagelslag en juweel zijn gelijk aan r3 (30 van 2971 cellen verschillen); de koekrand van de voorste ster heeft scherpe tips (boven, links, rechts), en er zijn vijf achterpunten (ook onder).
- **Grens voorste ster/achterpunten** per rij gemeten op het natieve raster (`voor_r4.py`; de achterpunt loopt tot de buitenlijn van de voorste ster): linksboven, rechtsboven, links-laag, rechts-laag, onder (onder pas vanaf rij 76, daarboven is het de koekrand van de inkeping).
- **Schaal 0,66** (zelfde als r1). Figuur zonder afstompen x3–57, y2–56: **55×55**, 1778 px; licht 55×54 (1752 px); sterk 55×53 (1733 px). De Gen 3 Starmie is 55×51. Het model is vierkant (84×85), dus bij 55 breed wordt hij ±55 hoog; 51 hoog zou schaal ±0,60 vragen (dan 50 breed). Niet gedaan, want de breedte is gelijk aan de Gen 3 en de voorkant blijft op de schaal van r1.

## Werkwijze (zoals r1/r4)
- **Voorste ster:**
  - kale reductie (oppervlakgewogen, klassen wit/hagelslag/paarse lijn/paars/zwart/koek);
  - zigzag geprojecteerd en uitgedund tot 1 px;
  - juweelfacetten geprojecteerd;
  - ontkorrelen;
  - koek in glazuur 1 px.
- **Achterpunten:**
  - reductie van het model: zwart, chip of koektint naar de modelhelderheid.
  - **Chips:** de chips in r4 zijn donkerder dan in r3 (deels < L60). Daarom geldt: een compacte donkere cluster (≤ 8 cellen) die niet aan de voorste ster of de achtergrond grenst = chip. Zo krijgen alle vijf punten hun modelchips: linksboven 6, rechtsboven 5, links-laag 2, rechts-laag 2, onder 2 px, allemaal op modelplekken; geen bijgezet.
  - Na de reductie: ontkorrelen.
- **Lijnen:** buitenlijn rechts/onder zwart, links/boven koek donker; binnenlijn achterpunt tegen voorste ster; losse zwarte pixels → koek donker.
- **Palet:** zoals r2–r4 (geel hagel samen met koek licht (250,218,128); 15 = chocolade (124,80,56)), 16 kleuren incl. transparant.

## Afstompen (alleen weghalen)
**Gen 3 Starmie gemeten** (`puntmaat.py`; breedte loodrecht op de as kern → tip, inclusief buitenlijn), alle tien punten:

| | 1 px van de tip | 2 px | 3 px | 4 px | 6 px | tiphoek (uit breedte op 2 en 6 px) |
|---|---|---|---|---|---|---|
| bereik | 3,0–5,2 | 4,6–6,1 | 5,0–6,8 | 6,0–7,7 | 7,0–9,2 | 28–55° |
| mediaan | 4,6 | 5,5 | 6,0 | 6,9 | 7,9 | ±35° |

De Gen 3-punten eindigen in een plat, stomp eind van ±4–5 px (bijv. linkerpunt: 4 px hoog plat eind) en worden daarna langzaam breder (±0,5 px per px). Lengte/voetbreedte: de punten zijn ±2× zo lang als hun breedte op 8 px van de tip (8–10 px).

**r5 zonder afstompen** (zelfde meting): 1 px van de tip 1,9–4,0, 2 px 3,2–5,0: puntiger dan de Gen 3 (vooral links-laag en rechts-laag 1,9).

**Werkwijze (`stomp.py`):**
- As = juweelmidden → tip van de modelpunt; de richting blijft.
- De punt wordt loodrecht op de as afgesneden op de eerste plek (vanaf de tip) waar hij minstens W px breed is: licht W = 4, sterk W = 5.
- Alles voorbij de snede wordt transparant. Er komt geen pixel bij, en de voet en de richting blijven die van het model.
- Facetkleuren blijven die van de reductie; de nieuwe rand krijgt de gewone buitenlijn.

| punt | richting | lengte model | licht: weg / lengte | sterk: weg / lengte |
|---|---|---|---|---|
| linksboven | 129,3° | 28,4 | 6 px / 26,4 | 9 px / 25,9 |
| rechtsboven | 55,7° | 26,6 | 6 px / 24,6 | 8 px / 24,1 |
| links-laag | −155,2° | 28,6 | 6 px / 26,1 | 10 px / 25,1 |
| rechts-laag | −27,6° | 25,9 | 4 px / 24,4 | 10 px / 22,9 |
| onder | −94,4° | 26,1 | 4 px / 25,1 | 8 px / 24,1 |
| totaal | | | 26 px | 45 px |

Breedte na afstompen, 1 px / 2 px van de nieuwe tip: licht 4,2–6,0 / 6,0–6,4 (≈ Gen 3, iets breder); sterk 5,5–6,4 / 5,5–8,0 (stomper dan de Gen 3). **Licht komt het dichtst bij de Gen 3.**

## Afwijkingen per zone (t.o.v. `kaal.png`)

| | voorste ster | juweel | achterpunten | silhouet |
|---|---|---|---|---|
| zonder afstompen | 208 | 42 | 103 | 0 |
| licht | 208 | 42 | 123 | −26 (weggehaald) |
| sterk | 208 | 42 | 142 | −45 (weggehaald) |

- **Voorste ster:** wit 85 (projectie + uitdunnen), ontkorrelen 137, koek in glazuur 1, buitenlijn.
- **Juweel:** 23 lijnpixels geprojecteerd, plus mengpixels.
- **Achterpunten:** ontkorrelen 46, buitenlijn/binnenlijn, losse zwarte pixels → donker (7), plus het afstompen.
- **Pixels die niet uit het model komen:** geen. Afstompen haalt alleen weg; chips staan op modelplekken.

## Controle
Beide varianten:
- 64×64, mode P, transparency 0, 16 kleuren.
- Geen lichte kleur op de buitenrand, geen losse zwarte pixels; zwart 9,7 %.
- Kleine vlekjes: de L-reeks (27,9)…(22,19) is de 1-px randglans op de linkerkant van de bovenarm (diagonaal), (38,23) en (39,46) zijn lichtgele hagelslag; M (14,14) (15,15) zijn een diagonale glanslijn in de punt linksboven.

## Twijfels
1. **Hoogte:** de figuur is 54–55 hoog (model vierkant); de Gen 3 is 51.
2. **De snede is een recht, plat eind** loodrecht op de as, zoals de Gen 3-tips. Bij de onderpunt in "sterk" blijft weinig punt over (leest als stompje).
3. **De tips van de voorste ster** (boven, links, rechts) zijn in r4 scherp en zijn niet aangepast: Jordi's opmerking ging over de achterpunten.
4. **De voorste ster verschilt 299 px van r1:** het glazuur is gelijk, maar de koekrand van r4 heeft een andere vorm (scherpe tips) en de grens met de achterpunten ligt anders.
