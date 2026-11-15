# Regionale Abra, kleur_r9 (verse eindkeurder + maker, 15 nov)

Jordi over r8 (letterlijk): "nu zitten er rechts op de schouder een paar overbodige pixels, laat een agent daarnaar kijken tezamen met de laatste eindkeuring".
Basis: `../kleur_r8/abra_r8.png` en `../kleur_r8/abra_r8_curve.png` (Jordi kiest nog; beide identiek behandeld). Bevroren: ogen (8 px, assert), pose, kleuren A, vlekjes, rand-zwart ±40–45 %.

Reproduceren (vanuit `kleur_r9/`): `python3 maak_r9.py` (edits als data, oude waarde = assert, reden per pixel) → `abra_r9.png`, `abra_r9_curve.png`; `TMPDIR=<scratch> python3 maak_vel.py` → `abra_r9_8x.png`, `abra_r9_curve_8x.png`, `vel.png`, `schouder.png`; `python3 randmeting.py <png>...`.

## Opleveringen
- `abra_r9.png` (= r8 + schouder), `abra_r9_curve.png` (= r8_curve + schouder). In de schouderzone (x 34–47, y 24–41) zijn ze nu pixelgelijk; ze verschillen alleen nog op de 13 curve-pixels van r8_curve (kop links, linkerarm binnen, rechterarm, lijf rechts rij 39).
- `vel.png`: r9 8× | r9_curve 8× | r8 8× | model zelfde schaal | echte Abra 8× | 1×/2× licht/donker/groen.
- `schouder.png`: r8 | r9 | model op 12× (x 32–49, y 18–41), tweede rij r8_curve | r9_curve | model; geel = gewijzigd, rood = r9-silhouet over het model.
- `KEURING.md`: eindkeuring Dragonfly Cave / Gen 3 met MOET/MAG.

## 1. Schouder rechts: wat er mis was (r8, op 12× naast het model)
Rijen x 40–46 in r8 (K zwart, L lijnkleur huid, 1/3 plaattinten):
```
     40 41 42 43 44 45 46
 30   3  3  3  3  3  K  .
 31   3  3  3  1  1  1  K     <- (46,31): 1-px-punt, (45,31) plaatvulling op de rand
 32   3  3  1  1  K  K  .     <- (44,32)+(45,32): plaatnaad en buitenlijn naast elkaar
 33   1  1  1  K  L  K  .     <- (44,33): losse L tussen twee evenwijdige zwarte lijnen
 34   K  K  K  1  K  .  .     <- (43,34): 1-pixel ingesloten door 4 x K
 35   L  s  L  K  K  .  .
```
Modelrand rechts (natief, `../kleur_r1/natief.png`, in sprite-eenheden): rij 28 44,75 · 29 45,75 · 30 46,25 · 31 46,5 · 32 46,25 · 33 45,75 · 34 44,75. Het model is hier een **ronde bult van een halve pixel** over vijf rijen, geen punt; de plaatnaad (zwart, x43–44 rij 32–34) loopt in het model **samen** met de buitenlijn tot één zwarte massa. Ontstaan: al in de onderlaag (r1, 2×-reductie van een halve-pixelpunt en een zwarte massa); r8 heeft hier niets aan veranderd, maar de lichtere randen elders lieten de knoop meer opvallen. In r8_curve kwam er (45,34) bij (r8 LOG: "~1 px buiten het model"), waardoor de rand onder de schouder nóg een bultje kreeg.

## 2. Pixels (beide versies)
| pixel | oud → nieuw | silhouet | reden |
|---|---|---|---|
| (46,31) | K → transparant | ja (−1) | spijkertje: 1-px-punt in de bocht (DFC: "nooit een punt in een curve"); model daar 50 % (46,5). Rand rechts nu x45 rij 29–33 = één boog |
| (45,31) | 1 → K | nee | buitenlijn sluit waar de punt weg is (anders plaatvulling op de rand) |
| (44,33) | L → K | nee | losse lijnkleur tussen plaatnaad en buitenlijn (dubbele lijn K L K); model zwart (K1/KK): de plaatnaad loopt nu in de buitenlijn |
| (44,32) | K → 1 | nee | voorkomt een 2×2-zwartklont (44–45, 32–33); plaatvulling tot de buitenlijn (model 1K/KK) |
| (43,35) | K → 1 | nee | (43,34) was een ingesloten 1-pixel; model (43,35) 1K/1K = half vulling. De donkere lijfstrook x43 (rij 34–40) loopt nu door tot de plaatnaad |

Alleen in r8_curve (bestaat in r8 niet):
| pixel | oud → nieuw | silhouet | reden |
|---|---|---|---|
| (45,34) | K → transparant | ja (−1) | uitsteeksel onder de schouder; model rij 34 = 44,75 (buiten het model). Met (45,33) erboven zou de rand anders x45 rij 29–34 zijn (6 recht) |
| (44,34) | 1 → K | nee | buitenlijn terug naar x44, zoals r8 |

Resultaat (x 40–46):
```
     40 41 42 43 44 45 46
 30   3  3  3  3  3  K  .
 31   3  3  3  1  1  K  .
 32   3  3  1  1  1  K  .
 33   1  1  1  K  K  K  .
 34   K  K  K  1  K  .  .
 35   L  s  L  1  K  .  .
```
- Schouderrand van boven naar onder: horizontale runs 3,2,2,1 (rij 25–28), dan verticaal x45 rij 29–33 (5, de bult van het model), dan x44 vanaf rij 34. Plaatonderrand 3,3,2 loopt geleidelijk in de buitenlijn.
- r9_curve lijf rechts nu: x45 rij 29–33, x44 rij 34–38, x43 rij 39–44 (5,5,6: oplopend, de bedoeling van de curve-variant blijft).

## Metingen
| | r8 | r9 | r8_curve | r9_curve | echte Abra |
|---|---|---|---|---|---|
| gewijzigd | – | 5 px | – | 7 px | |
| silhouet | – | −1 px (46,31) | – | −2 px (46,31)(45,34) | |
| figuur | 1065 | 1064 | 1065 | 1063 | 951 |
| rand-zwart | 42,7 % | **42,7 %** (248 px) | 42,5 % | **42,5 %** (247 px) | 40,3 % |
| zwart totaal | 17,5 % | **17,4 %** | 17,4 % | **17,3 %** | 18,0 % |
| kleuren | 9 + transp. | 9 + transp. (zelfde palet/indexen) | | 9 + transp. | |

## Controle (script)
- Ogen (22,28)(23,29)(24,30)(24,31), (30,27)(29,28)(28,29)(28,30) ongewijzigd (assert, beide).
- Geen vulkleur (s/b/h/1/2/3) op de buitenrand, geen 2×2-zwartblokken, geen randpixel die alleen tussen de andere lijnkleur ligt (beide).
- Kleine tintclusters (< 3 px, s/b/h/1/2/3/T): 67, allemaal al in r7 A (vlekjes van het model, bewust behouden); 0 nieuw, 2 minder ((43,34) en (53,57)).
