# Ruimtestation sprite r12 (25 nov): mastpanelen om de stok, PC en PE compleet

Jordi over r11: "ik vind de ogen nu goed anders. Bovenste paneel moet alleen ietsje naar links, omdat het nu op een vlag lijkt, maar de stok moet in het midden zitten ipv helemaal links, zelfde voor onderste paneel. Verder lijkt onderste en rechtsboven allebei nog lichtjes afgekapt he. Ik snap dat ze overlappen, maar zijn nog een paar pixels leeg waar ze niet overlappen".

**Basis:** `r11/sprite.png`, met reparaties in `herstel12.py`. Het paneelrecept staat in `recept.py`; dat is herstel10 als functie en reproduceert alle zes de panelen van r11 met 0 afwijkingen.

**Wat er veranderd is:**
- Ten opzichte van r11 zijn 169 pixels anders, allemaal tussen x 31–60 en y 12–55.
- De ogen zijn niet aangeraakt: 0 pixels verschil in alle drie de oogvakken.
- Per pixel de reden: `log_herstel12.txt`, en als beeld `diff_r11.png`.
- `sprite.png` heeft 16 kleuren incl. transparant (transparency=0); het palet is ongewijzigd.

**Uitvoer:**
- `sprite.png`
- `sprite_8x.png`
- `vel.png`: r11, r12 en het model op 8×. Daaronder close-ups van de ogen (ongewijzigd), mast PB, PF/PE-punt en PC-punt. Onderaan 1×/2× naast fase 2.

## 1. Mastpanelen om de stok
**Verschuiving:** PB en PF zijn met de halve paneelbreedte teruggeschoven langs hun breedterichting, −(L−T)/2:
- PB: −3,01 / −1,67 spritepx
- PF: −3,20 / −1,28 spritepx

De stok (de oude linkerrand, x = 34,1) loopt daardoor nu over de middellijn van het paneel. Waar de stok het paneel raakt, blijft op dezelfde hoogte. Lengte, vakken, kleuren en omlijning volgen het recept.

**Voor/achter:** PB ligt vóór PA en achter de romp. PF ligt achter de voorbuis en achter PE.

**PB:** steekt nu evenveel links als rechts van de stok uit, x 31–36, top op rij 12.
- Wat hij eerst bedekte (x 37–39) is transparant geworden.
- Waar de romp daar aan transparant grenst, staat nu omlijning: (37,26) zwart, (38,27) en (39,27) navy.

**PF:** de linkerhelft valt nu achter de voorbuis, de onderkant achter PE.
- Zichtbaar blijft een strook van 3 px breed (x 34–36, y 41–46): navy rand, vak, zwarte rand.
- Het uitstekende stukje onder PE uit r11 (x 39–40, y 52–55) is weg, omdat het paneel nu volledig achter PE valt.

## 2. Afgekapte punten compleet
De lege pixels binnen het parallellogram zijn nu paneel; daarvóór haalde een regel de scherpe hoekpunten weg.

| paneel | nieuw paneel | rand verschuift mee (recept) |
|---|---|---|
| PC (rechtsboven) | (60,32), (58,34), beide rand zwart | (58,32) lichte rand, (59,32) en (58,33) vak |
| PE (onderste, rechterpunt) | (41,49) | (40,49) vak |
| PE (onderste, onderpunt) | (36,55) | (36,54) vak, (34,47) lichte rand |

PF heeft geen lege pixels meer waar hij niet overlapt wordt.

## Aandachtspunten
- **PF is grotendeels uit beeld.** Met de stok in het midden en PF achter de voorbuis (zoals gevraagd) blijft maar een smalle strook over. Als Jordi meer PF wil zien, kan PF vóór de voorbuis, maar dat wijkt af van het model.
- PB staat nu direct op de knoopring. Een los stuk stok is niet zichtbaar, net als in r11.
- Nog geen keurder geweest.
