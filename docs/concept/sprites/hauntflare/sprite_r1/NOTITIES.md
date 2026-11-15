# Hauntflare sprite r1 (maker, 15 nov)

Vorm: `../model/model_claude_natief.png` (99×99), niets getekend. Elke pixel is een modelpixel met een paletkleur, of een Haunter Gen 3-pixel (gezicht).

## Reproduceren (vanuit de repo-root)
```
python3 docs/concept/sprites/hauntflare/sprite_r1/schrap.py        # -> model64.png + schrap.json
python3 docs/concept/sprites/hauntflare/sprite_r1/gezicht.py k4r2o # -> gezicht_k4r2o.npy (Haunter-blok)
python3 docs/concept/sprites/hauntflare/sprite_r1/bouw.py          # -> hauntflare_r1.png, _8x, bouw_log.json
python3 docs/concept/sprites/hauntflare/sprite_r1/vel.py           # -> vel.png
python3 docs/concept/sprites/hauntflare/sprite_r1/meet.py          # controles
```

## Stap 1: verkleinen (schrappen)
- Inhoud natief x8–87, y14–83 (80×70). Doel ≤62 breed (1 px marge): uniform 18 kolommen + 16 rijen geschrapt → 62×54, offset (1,9): x1–62, y9–62 (onderkant 1 px boven de rand).
- Geschrapte **rijen** (natief): 14, 21, 26, 28, 32, 35, 41, 45, 48, 53, 60, 63, 67, 73, 77, 81.
- Geschrapte **kolommen** (natief): 11, 13, 16, 21, 29, 34, 36, 39, 46, 51, 53, 57, 60, 67, 69, 75, 82, 85.
- Keuze: per gelijk verdeeld doel de goedkoopste rij/kolom (meest gelijk aan de buur) binnen ±2, ≥2 uit elkaar, en alleen als de losse delen los blijven en de witte gaten in de ring blijven (componenten-check).
- **Rechterhand: 0 px verschoven.** Getest dx 1–8 × dy −3…+3 (natief): elke verschuiving raakt de staart (spleet is natief maar 1 px, bij y59) of de ring. Het verkleinen zelf brengt de hand binnen het frame (rechts x62, 1 px marge); witte spleet naar ring en staart blijft (3 losse delen).
- **Afwijking van de opdracht:** er zijn rijen/kolommen door het modelgezicht geschrapt (rijen 35, 41, 45, 48; kolommen 29, 34, 36, 39, 46). Met het gezicht beschermd (variant `PROT=1 OUTN=variant_gezicht_beschermd python3 …/schrap.py`) moesten alle schrappingen buiten het gezicht vallen: de bol werd bovenaan plat en de rechterhand smaller. Omdat het modelgezicht toch vervangen wordt, is de uniforme versie trouwer aan het model.

## Stap 2: gezicht (Haunter Gen 3, frame 1)
- Haunter-blok x13–34, y28–45; klassen: oogwit, zwarte lijn (alleen tegen oog/mond, niet Haunters kaak-/hoofdomtrek), donkere lijn (index 5 → bol-selout), mond donker/licht; tanden en huid zijn bij Haunter huidkleur → bolroze (huid: de bol eronder; tanden: bol midden/schaduw).
- Gemeten: modelgezicht na verkleinen ±17×14 px (x14–30, y25–38); Haunters gezicht 21×18. Per-kleurlaag-schaal (0,8/0,9, methode `gengas/gezicht_groter/schaal.py`) gaf een rommelige mond, en 1,0 past niet tussen bolrand en ring. Daarom het blok **geschrapt** zoals het model (elke pixel blijft een Haunter-pixel): Haunter-kolommen 20, 24, 28, 33 en rijen 28, 30 weg (rijen door het nabije oog y31–36 gespaard) → **17×16** (`gezicht_k4r2o_12x.png`). Komt overeen met schaal ±0,81 breed / 0,89 hoog.
- Geplaatst met linksboven op (14,24) = linksboven van het modelgezicht. Oude modelgezicht (lijnen, mond, oogwitten) eerst weg: herkleurd met de bol-tint van de buren, van buiten naar binnen.

## Stap 3: kleur (palet 15 + transparant)
| # | kleur | gebruik |
|---|---|---|
| 0 | (transparant) | |
| 1 | 24161a | omlijning (modelkleur) |
| 2 / 3 / 4 | 5a2a33 / 8a4e55 / b0747a | ring donker / midden (modelkleur) / licht |
| 5 | c8435b | bol-selout + handschaduw (beide deze modeltint: c8435b / c94051) + Haunters donkere ooglijn |
| 6 / 7 / 8 | f04482 / fa76a2 / f8aec2 | bol schaduw / midden / licht |
| 9 | f9ccd8 | bol glans (wervel) |
| 10 | 9a2a22 | donkerrood: vlam-selout, handlijnen, mond donker |
| 11 | d84030 | vlam rood (kern) + hand rood |
| 12 | f48659 | vlam oranje (r4_a-randkleur) + hand-oranje rand |
| 13 | f8b850 | vlam geel-oranje (enige nieuwe tint) |
| 14 | ffffff | oogwit (Haunter) |
| 15 | ee747c | hand licht (knokkels), mond licht |

- **Vlammen:** zelfde verdeling als het model, alleen warmer: modeloranje f8856c → geel-oranje (randen/punten), roze-rood e85f80 → oranje, karmijn cb435a → rood (kern), donker → donkerrood.
- **Handen:** modeltinten → licht/rood/schaduw/donker; plus het r4_a-kleurgebruik: oranje op de binnenrand van de bogen tussen vingers/duim (handpixels 4-buur van de omlijning rond zo'n gat) en op onderranden tegen de omlijning. 36 px, lijst in `bouw_log.json` → `hand_oranje`.
- **Ring:** r4_c (`../model/nat_r4_c.png`, zelfde raster en vorm, zelfde schrapping) helderheid per ringpixel, 3×3-gemiddeld binnen de ring, drempels op 30/80 % → donker/midden/licht. Achter de bol donker, voorkant lichter met glansband, licht linksboven.
- **Opruimen (regels, geen handwerk):** tintvlakjes < 3 px (4-verbonden, niet op de buitenrand, niet in het gezicht) nemen de meest voorkomende buurtint van de eigen groep: 58 px. Buitenrand: lichte tinten → gekleurde selout van het eigen vlak (bol → f04482, ring → donkerbruin, geel → oranje, oranje → rood, hand licht → donkerrood): 39 px. Zwart–donker–zwart op één rand → zwart: 11 px. Alle coördinaten in `bouw_log.json`.

## Handmatig gewijzigde pixels
Geen. Alles hierboven is regel-gebaseerd herkleuren op de plek (gelogd in `bouw_log.json`); geen randopruiming aan het silhouet.

## Controle (`meet.py`)
- Silhouet (alpha) tegen `model64.png` (verkleind model, zelfde schrapping): **0 afwijkende pixels**.
- 16 kleuren incl. transparant; geen lichte kleur op de buitenrand; geen zwart/donker om-en-om op een rand; 3 losse delen (lijf+ring+kuif+staart, linkerhand, rechterhand).

## Eigen zwakke punten / twijfels (eerlijk)
1. Gezicht 17×16 tegen modelgezicht ±17×14: 2 rijen hoger, omdat rijen door het nabije oog het oog te plat maakten (k4r3: oog 3 rijen).
2. Rijen/kolommen door het modelgezicht geschrapt (zie stap 1), tegen de letter van de opdracht in; reden en alternatief staan erbij.
3. Bol heeft 4 tinten + selout (glans f9ccd8 is een breed deel van het wervelpatroon uit r4_b, geen klein glanspuntje): boven de norm "≤3 tinten + omlijning". Samenvoegen met f8aec2 zou de wervel van het model wegvegen.
4. Het oogwit ligt in het lichte wervelvlak van het model; contrast oogwit/glans is klein, het oog leest vooral door Haunters lijnen.
5. Handrood is de vlamtint d84030 (oranjer dan het model e4505a) en de handschaduw deelt c8435b met de bol: bewust (vlammiger, palet vol), maar het is een kleurverschuiving t.o.v. het model.
6. Kuifpunten: de rand wisselt donkerrood/oranje (zoals het model karmijn/oranje) en er staan nog enkele 1–2 px tintvlakjes in vlammen en handen (meestal lijn- of randpixels; `meet.py` noemt ze).
7. Palet is vol (15 + transparant): geen ruimte voor een extra tint bij een volgende ronde zonder iets samen te voegen.
