# Ruimtestation sprite r10 (25 nov): rechteroog en consistente panelen

Jordi over r9: "weer een stap vooruit, oog rechts mag iets netter afgemaakt worden, de panelen mogen nog iets consistenter qua grootte, houd rekening met de hoek he".

r10 bouwt voort op r9, met dezelfde pijplijn: `model10.py`, dan `pijp/bouw7.py` + `maak10.py`, dan `herstel10.py`. Nieuw zijn:
- `pijp/geo10.py`: de paneelmaten.
- `kaal.py`: het modelkader staat vast op dat van r8/r9 (schaal 3,515625).

**Uitvoer:**
- `sprite.png` (+ `_8x`): 16 kleuren incl. transparant, transparency=0.
- `vel.png`: bovenaan r9, r10 en het model. Daaronder close-ups (boven r9, onder r10). Onderaan 1×/2× naast fase 2, op licht en op donker.
- `diff_herstel.png` en `w_r10/log_herstel10.txt`: elke pixel met zijn reden.
- Ten opzichte van r9 zijn 198 pixels anders. Het silhouet telt 1237 px (r9: 1281), omdat de achterste panelen kleiner zijn.

## 1. Rechteroog
- **Verschoven:** het oog staat 1 px naar rechts (plek x 49–54 in plaats van 48–53). Ten opzichte van het model is de verschuiving nu +1,39 / −0,47 px.
- **Vrij van de kraag:** tussen de ring en de kraag/buis links zit nu een kolom boltint. Regel: geen kraag-, buis- of lijnpixel als 8-buur van het oog, behalve de bolrand zelf.
- **Vorm:** ring 6 (rijen 4,6,6,6,6,4) met iris 4×4 en een pupil van 2×2 in het midden. De ring is overal 1 px dik, net als bij het voorste oog. In r9 was de iris 2,4,4,2, waardoor de ring in de hoeken 2 px dik was.
- **Bolrand:** rechts is de afwijking −0,43 … +0,49 px.
- **Linkeroog:** heeft dezelfde vorm gekregen, omdat de zij-ogen in dezelfde vorm moeten. Zijn plek is ongewijzigd. Dit was niet gevraagd; het is terug te zetten met `IRIS4` in herstel10.
- **Voorste oog:** ongewijzigd.

## 2. Panelen: maten met perspectief (`pijp/geo10.py`)
**Uitgangspunt:** in de ruimte zijn alle vier de liggende panelen (PA, PC, PD, PE; 4 vakken) even groot. In beeld zijn ze alleen verkleind met een perspectieffactor f. Richtingen en vakverdeling blijven die van het model, met vakken gelijk verdeeld binnen elk paneel.

**Perspectieffactor (uit de modelgeometrie):**
- **Hoofdas** (voorste bol → achterbol): over de hele arm ±0,75. De bollen geven 14,8/20,6 = 0,72, de kragen ±0,78. Tussen het voorste en het achterste paneelpaar is dat 0,89.
- **Dwarsarm** (linker/rechter oogbol): 10,75/11,98 = 0,90.
- **Per paneel:** PE (voor-rechts) 1, PD (voor-links) 0,90, PC (achter-rechts) 0,89, PA (achter-links) 0,80.
- **Maat bij f = 1:** die van PE uit r9 (lengte 50,0 × breedte 30,8 modelpx).

**Ankers:**
- Het binnen-einde (staafje/romp) blijft staan; de lengte verandert aan het buiteneinde.
- Uitzondering is PD: daar blijft het buiteneinde staan, anders valt hij buiten het kader. Zijn +1,3 px valt achter de bol.
- Het breedte-anker is hetzelfde als in r9.

**Mast PB/PF:**
- Beide 6,9 px breed (24,2 modelpx) met dezelfde vakmaat (47/3 = 15,7 modelpx).
- Breedte:lengte is in de ruimte dezelfde als bij de liggende panelen. De kijkhoek komt uit de bovenring van de knoopbol: een ellips van 17×6, dus elevatie ±21°, verticaal ×0,94 en dwarsas ×0,78.
- PF heeft dezelfde vakmaat als PB, maar is afgekapt op 36 (zoals het model; Jordi: "zal in de sprite onder een ander paneel vallen"). De vakgrenzen liggen op 15,7 en 31,3 van boven.
- Bij de volle lengte (47) zou PF rechts naast PE tot y 156 uitsteken.

**Lengte × breedte in spritepx:**

| paneel | f | r9 | r10 |
|---|---|---|---|
| PE (voor-rechts) | 1,00 | 14,2 × 8,8 | 14,2 × 8,8 |
| PD (voor-links) | 0,90 | 12,4 × 8,4 | 12,8 × 7,9 |
| PC (achter-rechts) | 0,89 | 15,0 × 7,6 | 12,7 × 7,8 |
| PA (achter-links) | 0,80 | 15,2 × 8,2 | 11,4 × 7,0 |
| PB (mast boven) | – | 13,4 × 5,9 | 13,4 × 6,9 |
| PF (mast onder) | – | 10,2 × 7,7 | 10,2 × 6,9 (vakmaat = PB) |

**Paneelpixels:** die zijn net als in r9 uit het parallellogram + recept gezet, alleen nu met de r10-geometrie. Treden van de lange randen (per kolom):

| paneel | boven | onder |
|---|---|---|
| PA | 4,3,3 | 3,3,4 |
| PC | 4,4,4 | 3,4,4 |
| PD | 2,3,3 | 3,3,2,3 |
| PE | 3,3,3 | 3,3,3,2 |

Mastranden zijn recht. Bij PD zit in de korte rand één trede van 5 (hoek bij de bovenrand).

**Kruising PF/PE:** PF ligt achter PE. De bovenrand van PE loopt geometrisch recht door (navy), met daaronder de lichte rand c van PE. Daardoor zit er tussen de vakken van PF en PE altijd een lijn.

**Losse pixels:** een losse romppixel binnen een paneelvlak zonder rompbuur wordt paneel. Dat ging om een staafjerest midden in PF.

## Afwijkingen en aandachtspunten
- **PA is duidelijk kleiner** (−25 % lengte). Dat volgt uit de gemeten f = 0,80. Met een mildere factor (bijv. alleen de hoofdas, 0,89) wordt PA 12,7 × 7,8, gelijk aan PC. Eén getal aanpassen in `geo10.F`.
- **Het eind van PC** ligt nu bij x 50, deels achter de rechterbol. De bovencontour van de rechterbuis is daar opnieuw omlijnd (romp uit de kale modelreductie).
- **Nog geen keurder geweest.**
