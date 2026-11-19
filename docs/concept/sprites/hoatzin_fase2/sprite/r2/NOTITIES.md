# Hoatzin fase 2, r2 (19 nov), maker

Reparaties van Claude op r1 (vleugelveren, buitenlijn, vlakken, kuif, oog B, achterste vleugel). Alles opnieuw: `sh alles.sh`.
Bestanden: `hoatzin.png` (64×64, 16 kleuren, index 0 transparant), `hoatzin_8x.png`, `normal.pal`, `onderlaag.png`, `vel.png` (r2 | r1 | model | Pidgeot, 1×/2×, kop 12×), `lijnkaart.png`, `pennen.png`, `buik/`.

## Wat er anders is (alles regels op modelmetingen, niets met de hand)
1. **Vleugelveren** (`lijnkaart.py`, `pennen.py`, `r2.py` stap 1): op het natieve model de scheidingslijnen gemeten (pixel ≥ 14 donkerder dan het 7×7-gemiddelde én < 72 % ervan) en de lichte strepen (≥ 30 lichter, L ≥ 140). Daarmee de vleugel op het model in **pennen** gesegmenteerd (38 pennen: de waaier, de donkere armpennen, de dekveren, de achterste vleugel achter de kop, de staart). Elke spritecel krijgt de pen met het grootste aandeel; cellen op een scheidingslijn groeien naar de dichtstbijzijnde pen. **Pengrens = 1 px lijn** (rechts/onder) in de donkerste vleugeltint (#321E30), in de donkere armpennen zwart. **Eén toon per pen** (70e percentiel van de pen in het model, zonder lijn/streep). **Hooguit één lichte streep per pen**: de grootste verbonden streepcel-groep op de modelplek. Geen losse vlekken meer in het vleugelvlak.
2. **Buitenlijn**: elke randpixel rondom (4-buur aan achtergrond), lichtkant gekleurde selout in de donkerste tint van de groep (mauve #321E30, bruin, blauw, buik #7A5270, grijs nu donkerder #46425A), schaduwkant zwart; om-en-om weggepoetst. Contour: inkepingen dicht waar de modelcel ≥ 35 % gevuld is (3 px), uitsteeksels weg waar < 60 % (0 px).
3. **Lijf en nek**: tonen uit een gladde toonkaart (model per zonegroep gemiddeld in een venster van 9×9 natieve px, lijnen/strepen niet meegeteld), dan drempels; zwarte modellijnen in lijf/nek nemen de toon van de omringende zone. Clusters < 4 px naar de buurtint.
4. **Kuif**: drempel streng 0,50 (r1 0,35); strengen blijven waar het model ≥ 50 % bruin is, ertussen de tint erachter.
5. **Oog**: variant B (3×3 rond de donkerste modelpixel, onderhoeken donkerblauw) + glanspixel linksboven (#868298; modeliris is daar lichter).
6. **Achterste vleugel achter de kop**: valt onder dezelfde pensegmentatie (VLEUGEL = natief x ≥ 92 of y < 60).

## Afwijkingen t.o.v. de onderlaag (stap A = onderlaag in paletkleuren), per zone
| Zone | px | afwijkend | waardoor |
|---|---|---|---|
| lijf/vleugel (M) | 891 | 534 | pentoon 331, pengrenzen 209, buitenlijn 126, gladde toonkaart (rest) |
| vleugelstrepen (W) | 178 | 142 | pentoon 86, pengrenzen 65, streep 58 (overlap) |
| kuif (C) | 124 | 18 | buitenlijn, drempel |
| gezicht (F) | 27 | 11 | oog 3×3, toonkaart blauw |
| oog (E) | 7 | 3 | oog B + glans |
| snavel (S) | 15 | 1 | buitenlijn |
| buik (P) | 161 | 26 | buitenlijn 13, toonkaart |
| poten (T) | 73 | 30 | buitenlijn 21, clusters 7 |
| staart (D) | 120 | 36 | pennen, buitenlijn |
| modellijn (K) | 219 | 111 | buitenlijn 87, pengrens, buurtint |
| buiten silhouet | – | 3 | inkepingen dicht (modelcel ≥ 35 %) |
| **totaal** | 1815 | 915 | silhouet 3 px |

## Buikvarianten (`buik/`, Jordi via Claude)
Alleen paletplekken 11–13 anders, pixels identiek (assert in `buik.py`): A huidig #7A5270/#8E6280/#A57A98 · B Poison-paars #6A3A80/#8A50A6/#AE74C8 · C paars + gifgroene glans #7A5270/#8E6280/#A2B862 · D diep naar giftig #4C2860/#7C4498/#B47CD6. `buik/vel.png`: 4× en 1× op licht/donker.

## Resterende twijfels
- Pengrenzen zijn op enkele plekken onderbroken (1–2-px lijnstukjes, 48 clusters van index 2); de bovenste waaierpennen lezen nu wel als losse pennen.
- De dekveren (voorrand van de vleugel) zijn één lichte pen geworden zonder de vele strepen van het model.
- Buikvariant D: de buik is vooral middentint met een kleine lichte vlek linksboven; het verloop onder→boven is daardoor beperkt zichtbaar (zelfde pixels als eis).
- Variant C: de gifgroene hooglichttint beslaat maar ±6 px (de lichtvlek van het model).
