# Viscacha frontsprite, kleur ronde 2 (maker-agent)
Reparaties volgens `kleur_r1/vel.png.keuring.md` (FAIL). r1 is niet aangeraakt. Alle wijzigingen staan per zone in `reparaties_r2.py` (handraster-stukken op het r1-raster); `controle.py` toont de diff.

## Per zone (pixeldiff r1→r2: 226 px)
| zone | px | wat |
|---|---|---|
| 1 wangpluk/achterkop | 44 | Geel onder rij 32 weg. Korte halve maan op x13–23, rij 26–32; alleen de punt (20–24,26–27) steekt buiten de kop. Achterrand van de kop is een tapse binnenlijn in 2 op (21,28)–(18,33), geen zwart langs het geel. De 4/3-banden achter de kop zijn weg (achterkop is 4, 3 alleen als korte schaduw onder de kaak, 19–23, rij 28–34). |
| 2 snuit | 14 | Geel weg op (1–5,26–29). Snuitpunt in 5 met selout 2, neus 2 px (1–2,29), oude neus (3,31) → 2. Kinhoek (6,36) → F. |
| 3 rug | 78 | Bult (35–38,26) en dip (37,28) weg; rug als één boog (28–36,27) → (37–38,28) → (39–40,29) → (41–42,30) → (43,31) → (44,32); selout 2 aan de lichtkant, zwart pas vanaf (44,33). Lichte rugband kleiner (taps naar linksonder), dij-hooglicht nu een smalle glans (36–39,32–33 en 37–38,34). Dijlijn 3 begint dun op (35,34) en loopt op in de schaduw onderaan. |
| 4 buik | 47 | Crème ovaal weg; crème strook langs de onderrand van de buik (bovenkant rij 44, x27–34), loopt door tot tegen de buitenlijn (23–24,48–50); schaduw 6 als sikkel rechtsonder; geen rechte rij 48 meer. |
| 5 oren | 14 | Toppen rond, 2 px breed in selout 2 (7–8,12) en (20–21,12). Het verre oor is 1 px breder (x9 op rij 13–15) en heeft een binnentint C op (8,14–17). |
| 6 voorpoot | 21 | Nabije voorpoot: front-binnenlijn verspringt van x18 naar x19 (elleboog), pols op rij 43–44 (achterlijn x22→x21), poot rij 45–50 met teenlijn (19,49); lijnen beginnen taps (rij 37 zonder voorlijn, x23 eerst 3). |
| 7 staart/voet | 8 | Staartlinkerrand doorlopend B (ook 53–55,42–44). Trap rechts zachter: r28 eindigt op x59, r29 op x60. Pluimtop met gele kern (57,12) A. Verre voet: teenlijn (26,57). |

## Silhouetwijzigingen t.o.v. r1 (21 px, alleen in de toegestane zones)
- Oren: (6,12) en (22,12) weg; (20,12), (9,13), (9,14) en (9,15) erbij.
- Rug: (35–38,26) en (37,27) weg; (38,28), (40,29), (42,30), (43,32), (44,32) en (44,33) erbij.
- Staart: (60,28) en (61,29) weg.
- Snuit: (1,26) en (2,26) weg. Dit zijn de punten van het gele plukje zelf; zonder het geel zouden ze als losse zandpunten blijven staan. Dit valt buiten de opgegeven silhouetzones; ik meld het expliciet.
- Het nieuwe silhouet staat in `silhouet/silhouet_r2.txt`; `silhouet/silhouet.txt` (r1) is niet gewijzigd.

## Controle (`controle_uitvoer.txt`)
Open randen 0, losse pixels 0. Clusters < 3 px: alleen het oog (E, D) en de gele kern (57,12) in de pluimtop, die de keuring zelf vroeg (1 px geel in de punt). Kleuren: 15 + transparant = 16. png = raster.

## Eerlijke zwakke punten
1. De halve maan loopt nog schuin van de punt naar de wang; op 1× is hij veel korter en ligt hij op de kop, maar een keurder kan er nog een rest van de kraag in zien.
2. De dijlijn (33–35,34–44) is nog ±10 rijen lang, al is hij taps aan de top.
3. De neus (1–2,29) zit op de buitenrand van de snuitpunt en leest op 8× als een donker stukje omtrek.
4. De kinlijn (6–10,37) is nog vrij recht (alleen de hoek (6,36) is verzacht).
5. Het formaat is ongewijzigd (62 px breed), zoals gevraagd.
Niets gecommit.
