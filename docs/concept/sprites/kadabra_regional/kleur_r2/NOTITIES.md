# Regionale Kadabra: kleur r2 (reparaties keurder)

Basis: `basis_r1.txt` (= `../kleur_r1/raster.txt`). Keurder: eis 1 PASS, eis 2 FAIL (toon te licht, lichtkant te zacht). Silhouet bevroren, alpha-diff 0.

Bouwen: `python3 r2.py` (controleert bij de benoemde pixels eerst de oude letter, schrijft `raster.txt`), `python3 r2.py klaver_A`, `python3 r2.py klaver_B` (varianten voor het vel), `python3 pal.py raster.txt kadabra_charlatan.png kadabra_charlatan_8x.png`, `python3 vel.py`. Meten: `stat.py`, `lichtkant.py`, `controle.py`.

## Meting
| | a | b | c | grijs gem. | lichtkant zwart |
|---|---|---|---|---|---|
| kleur_r1 | 15,6 % | 19,5 % | 7,3 % | 194,8 | 2 % |
| **kleur_r2** | **7,2 %** | **20,3 %** | **14,7 %** | **181,5** | **12 % (15 van 124)** |
| charlatan-Alakazam | 5,8 % | 18,6 % | 14,5 % | 179,9 | 18 % |

Percentages van alle figuurpixels; grijs gem. = helderheid van alleen de a/b/c-pixels (`stat.py`).

## Gedaan (alle verwachte oude letters klopten; `r2.py` meldde 0 afwijkingen)
1. **Grijs een stap donkerder.** Per spritepixel het model gemeten (`meet.npz`: licht ≥ 176, midden < 176).
   - Kop: x26–31, y15–23 a → b; a blijft op de strook x24–25 (voorhoofd, neusrug), de rand x22–23 en het linkeroor (24,11–14). Rechterhelft waar het model middengrijs is b → c: (32–33,17), (32–34,18–19), (32–36,20–21), (31–37,22), (32–37,23), (30–35,24), wang (30–31,25), (28–29,26), snuit rechts (26,27–28), (25,28), (24–25,29).
   - Rechteroor: (32–33,14) a → b; de lichte strook (36,11), (35,12), (34,13) blijft.
   - Staart: a alleen nog een strook van 2 px onder de bovenrand (rij 37–43, 18 px); daaronder b; sikkel c onderlangs, breder naar de wortel.
   - Dijen: links hooglicht 1 px (25,42), (24,43), (23,44), (22,45), c rechtsonder; rechts hooglicht (35,43–45), c langs de rechterrand.
   - Handen, schenen, voeten: a → b (hooglicht alleen (22,52–54) en (40–41,56–58)); c op de schaduwkant. Bovenarm onder de rechterplaat c.
   - Wit ongewijzigd (oog, borst, buik, kaart, klauwtjes). Het oogwit (29–30,22) ligt nu tussen pupil o en c.
2. **Zwarte omlijning:** de 12 benoemde pixels d → o (kaart, klauwtjes open hand, linkervoet, oorpunten). **Eigen aanvulling** om de lichtkant boven 10 % te krijgen: duimtop (45,27), (46,26), vingertop (4,28), staartpunt (60,37), rechterteen (38,59), (38,60) d → o. Zonder die 6 is de lichtkant 9 %.
3. **Linkerplaat:** (21,24), (21,25), (20,26) n → m; (23,25), (23,26) d → o.
4. **Onder de kin:** (28,27), (28,28) m → o; (27,29) m → k. Rechtersnorstreng blijft b (de snuit ernaast is nu c).
5. **Klaver:** (26,21) a → s. Zie hieronder.
6. **Nagel:** ongewijzigd. Tussen nagel (6,24) en kaart staat al zwart: (6,23) o erboven, (7,24) o rechts, (5,24) d links. (5,24) ook zwart maken laat de nagel versmelten met het schoppensymbool, dus niet gedaan.
7. Losse tintvlakjes uit `controle.py` opgeruimd (11 px: snuitpunt c, (25–26,30–31) k, bovenarm, dijen, voet).

## Klaver op 1×
Leest op 1× als rood vlekje met donkere voet, niet duidelijk als klaver en ook niet meer als plusteken. Twee varianten op het vel (12×, 1×, 3×; `klaver_A.txt`, `klaver_B.txt`):
- A (4×4): lage bovenlob, zijlobben twee rijen hoog, voet 2 px.
- B (5×5): drie lobben met donkere kern en steel; groter dan het model (model = 4×4 px).
Hoofdsprite = de r2-versie (model-trouw); keuze aan Jordi.

## Pixeldiff tegen r1 (218 px, alpha 0)
| zone | px | wat |
|---|---|---|
| oren + schedel (y9–17) | 17 | a→b 13, b→c 2, d→o 2 |
| gezicht, klaver, snuit | 58 | a→b 19, b→c 29, a→c 1, a→s 1, d→o 2, m→o 2, m→k 2, n→m 2 |
| kaarthand + arm | 12 | a→b 2, b→c 4, d→o 5, n→m 1 |
| open hand + arm | 25 | a→b 12, b→c 7, d→o 6 |
| platen, romp, borst | 1 | m→k 1 |
| staart | 46 | a→b 22, b→c 23, d→o 1 |
| benen + buik | 36 | a→b 18, b→c 18 |
| voeten | 21 | a→b 13, b→c 4, d→o 4 |
| buiten de zones | 2 | oorpunten (23,9), (38,9) d→o |

## Controle
- 11 kleuren + transparant; open randen 0; losse o 0; alpha-diff 0; box 62×54.
- Clusters < 3 px: 2: (20,25) n (opdracht: alleen die blijft n) en (5–6,28) b (eerste gebogen vinger).

## Zwakke punten
- **Klaver** leest op 1× niet als klaver (varianten op het vel).
- **Nagel** leest op 1× nog steeds niet.
- **Kop rechts** is nu één vlak c van 30+ px; de vouwlijn d van het oor valt daarin minder op dan in r1.
- **Zwart** is ongewijzigd m/k en blijft blauwgrijs; niet in de opdracht.
- (20,25) n is een los hooglichtpixel op de linkerplaat.
