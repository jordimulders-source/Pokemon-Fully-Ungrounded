# Gnomad – sprite r2 (maker-agent, 22 nov)

Basis: `../sprite_r1/gnomad_A.png` en `gnomad_B.png`. Script: `r2.py` (bewaakt met assert dat er buiten lijf/broek/riem en de 6 neuspixels niets verandert), vel: `vel.py`.
Jordi: "de riem is nog iets teveel gewoon een lijn, verder bijna goed, rechts naast de neus iets teveel zwarte pixels, lijkt net een oog".

## 1. Riem (A bruin, B donkerblauw)
- Zelfde bovenrand en boog als in r1; dikte 4 px in het midden, 3 op de flanken (r1: 3 en 2).
- Opbouw: de bovenrij is licht, met een hooglicht links van het midden (x17–26). Daaronder de middentint, dan 1 px donkere onderrand. Het rechter derde (x ≥ 33) is donker.
- De broekrij direct onder de riem ligt in schaduw: blauw schaduw links, blauw donker rechts. Daardoor zit de riem "om" de bol.
- Hooglicht zonder extra kleur: A = crème schaduw (218,198,158), B = blauw schaduw (82,148,197). Er is niets opgeofferd; het blijft 16 kleuren.

## 2. Rechts naast de neus
Er stond een zwarte ring om (25,29)–(26,30), die als oog las. Die ring is opengebroken naar het model:
- (24,29) en (24,30): rechterrand van de neus, nu donkerroze.
- (27,30) en (28,30): schaduw onder de mutsrand, nu roze schaduw.
- (25,31): roze schaduw. (26,31): donkerroze.
- De mutsranden (25–26,28 en de rij 29 vanaf x26) en de neusonderrand (24,31) blijven zwart, zoals in het model.

## Diff t.o.v. r1 (A en B gelijk)
| zone | px |
|---|---|
| riem (nieuwe en herkleurde riempixels) | 48 |
| broek: schaduwrij onder de riem | 24 |
| neus/wang (geen oog meer) | 6 |
| muts, snor, armen, voeten, silhouet | 0 |

Controle: 16 kleuren, geen lichte kleur op de buitenrand, geen losse zwarte pixels.

## Eigen zwak punt
- In B ligt het hooglicht in hetzelfde blauw als de broek. De riem leest daardoor iets minder als los voorwerp dan in A.
