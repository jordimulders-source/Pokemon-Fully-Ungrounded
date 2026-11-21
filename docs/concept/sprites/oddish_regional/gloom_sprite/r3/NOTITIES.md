# Gloom-regional r3

Jordi (20 nov) over r2: "best netjes al, in het hoofd mag je wat meer kleurtinten/schaduw gebruiken voor de lava, voor de rest is het alleen afwerking".

Bestanden: `gloom_r3.png` (64×64, geïndexeerd, index 0 transparant, **16 kleuren incl. transparant**), `gloom_r3_8x.png` (wit, NEAREST 512), `vel.png` (r3 8× | r2 8× | model 8× / close-ups 12× / 1× licht en donker), `bouw.py` (r2 → r3, controleert oude waarden).
Basis: `r2/gloom_r2.png`. Vorm, silhouet en plek/breedte van de kieren zijn ongewijzigd: alleen tinten en 8 afwerkingspixels.

## Gewijzigd t.o.v. r2: 34 px (lavabrok 26, mond 6, vinnetje links 2)

### Lavabrok, 26 px, alleen tint
Elke kierpixel (was overal oranje 10) krijgt de tint van de gemeten modelgloed: het oppervlak-gewogen gemiddelde van de gloedcellen in die spritepixel.
- gemiddelde < 118 → diep (dieprode kierrand);
- 118–150 → oranje;
- ≥ 150 → geel (fel hart, kruisingen).

Meting: de kieren bovenin en rechts zijn in het model donker (105–125). Op de kruisingen is het model fel: (23–24,17) 163–193, (33,18–19) 165–171, (28–29,21) 159–165, (35,22–23) 183–191.

**Licht en schaduw:** in de schaduwkant van de brok (x ≥ 34 of y ≥ 23, licht linksboven) gaat elke kier één stap donkerder: geel → oranje → diep → sintel (nieuwe tint 15). De kieren rechts en onder lezen daardoor als gloed in de schaduw. De felste kruisingen zitten linksboven en in het midden.

Resultaat over alle 47 kierpixels: 9 geel, 21 oranje, 14 diep, 3 sintel (26 daarvan gewijzigd t.o.v. r2, de rest bleef oranje).

### Afwerking (8 px, `W` in bouw.py)
- **Mondring rechts (5 px):** het model heeft daar twee lijnen vlak naast elkaar, de zwarte binnenlijn van de opening en een donker bordeaux buitenring. De reductie maakte er losse zwarte pixels van.
  - Buitenring (32,35) (32,36) (33,37) (32,38): zwart → bordeaux-selout, zoals links.
  - (31,38): lijfschaduw → zwart. Daardoor loopt de binnenlijn door, zoals de doorgaande curve in het model.
- **Vinnetje links (2 px):** (14,40) en (15,40) waren een los 2-px schaduwvlekje en worden middentint. De schaduw blijft eronder op y41.
- **Mond (1 px):** (30,36) los diep-gloedpixel → oranje.

## Palet
| Index | Groep | Kleur |
|---|---|---|
| 0 | transparant | (152,208,160) |
| 1 | zwart | (16,12,12) |
| 2–4 | steen | (44,42,44), (74,72,74), (116,114,110) |
| 5–8 | lijf: selout, schaduw, midden, licht | (88,28,40), (128,48,64), (166,76,88), (198,108,116) |
| 9–11 | gloed: diep, oranje, geel | (204,74,40), (244,124,48), (252,184,80) |
| 12–14 | kelp: bruin, olijf, khaki | (78,62,40), (116,100,70), (160,148,110) |
| 15 | **sintel (nieuw)** | (150,40,32) |

De gloed heeft nu 4 tinten. In de mond en het kwijl worden alleen diep, oranje en geel gebruikt; de sintel alleen in de kieren aan de schaduwkant.

## Controle (`gereedschap/controle.py`)
- 16 kleuren; geen lichte kleur op de buitenrand; geen losse zwarte pixels; zwart 17,9 %.
- Tintvlekjes < 3 px die over zijn:
  - houtskool in de kelppunten (modelplekken);
  - glans op de brok, lip en vin;
  - selout- en lijnpixels;
  - kelpstrenglijntjes;
  - geel in het kwijl (glans);
  - 1-px tintstappen langs een kier (rand–hart–rand). Dat zijn lijnen, geen vlakken.
- Schaduwkant niet zwart: alleen (16,33). Dat is een hoekpixel aan de lichtkant (rechts van hem staat lijf, eronder achtergrond) met de bordeaux-selout uit r2; die heb ik zo gelaten.

## Twijfels
- De kruising rechts (x32–34, y17–19) heeft drie tinten naast elkaar (diep–geel–diep). Dat is de meting (dieprode randjes, fel hart), maar op 8× is het het drukste plekje van de brok.
- De kier rechtsonder (x34–35, y21–24) is in het model fel (183–191) en is door de schaduwregel donkerder geworden (oranje/sintel). Dat is bewust, voor licht en schaduw, maar het wijkt af van de modeltint.
