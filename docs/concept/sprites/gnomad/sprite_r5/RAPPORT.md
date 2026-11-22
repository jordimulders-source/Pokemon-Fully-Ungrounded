# Gnomad – sprite r5 (maker-agent, 22 nov)

Basis: `../sprite_r4/gnomad.png`. Script: `r5.py`. Een assert bewaakt dat er alleen pixels in lijf, broek, riem en gesp veranderen.
Jordi: "de riem is nu wel wat blurry en de gesp is nu niet goed in perspectief met de rest van het lichaam, gezien het driekwart is". Zwart: "dat doet de eindkeuring".

## 1. Riem rustiger
- Elke kolom heeft dezelfde opbouw: zwarte lijn, 3 rijen band, zwarte lijn. Er zijn geen kolommen meer waar de band 1–2 px dun wordt of waar zwart verdubbelt.
- De band is één tint donkerbruin (104,68,48).
- Glans: alleen de bovenste bandrij links (x15–21), in lichtbruin (174,130,90).
- De boog is iets vlakker (zakt 2,6 px in plaats van 3,4), zodat de trappen langer en rustiger zijn. Rechts geen extra schaduwtint: de zwarte omlijning doet daar het werk.
- Roze en blauw rond de riem krijgen dezelfde belichting als in r1. De broekrij onder de riem blijft in schaduw.

## 2. Gesp in driekwart
- Naar links verschoven, naar het buikmidden onder de neus/snor-as: x18–23 (in r4 x21–28).
- Ingekort tot 6 breed × 7 hoog. Hij steekt 1 px boven en onder de band uit.
- De voorkant is 4 px breed: crème schaduw met een glanspixel crème licht linksboven, en een staand gat van 1×3 waar de bruine band doorheen zichtbaar is.
- De rechterkolom is lichtbruin, als de zijkant (dikte) van de gesp.
- Een proef met een 1 px lagere rechterhelft (scheef, volgens de boog) las rommelig en is verworpen.

## Diff t.o.v. r4
| zone | px |
|---|---|
| riem + roze/blauw eromheen | 68 |
| gesp | 36 |
| muts, neus, snor, armen, voeten | 0 |

Controle: 16 kleuren, geen lichte kleur op de buitenrand, geen losse zwarte pixels. Zwart is 21,6 % (r4: 21,7 %), dus niet erger.

## Eigen zwak punt
- Het gat in de gesp is door de inkorting nog maar 1 px breed. Het leest als een staande gleuf, niet meer als een vierkant gat.
