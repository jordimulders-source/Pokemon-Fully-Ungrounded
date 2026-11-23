# Gnometrotter Grass – hybride model (knippen en plakken)

- **Basis** (omtrek/pose/maat): `../r4/gemini_r4_lijf.png`. **Donor** (materiaal): `../r1/gemini_r1_handen_gewisseld.png` ("echt heel vet de grass").
- **Resultaat:** `model_hybride.png` (1024×559). Vergelijking: `vergelijk.png` (basis | hybride | donor). Script: `python3 maak_hybride.py` (functies in `knip.py`, identiek aan die van Ice). Maskers: `debug_maskers_basis.png`, `debug_maskers_donor.png`.
- **Niets getekend:** elke vervangen pixel is een donorpixel (NEAREST). Jordi's toestemming om "ietsje van het model af te werken" is alleen gebruikt voor het spiegel-herhalen van de romptextuur (zie onder).

## Werkwijze
Zelfde als Ice (`../../gnometrotter_ice/hybride/RAPPORT.md`), met voor Grass:
- Roze = r>g en b≥g, zodat bruin hout (riem, zolen, stok, rugkam) er nooit bij hoort.
- Zwarte lijnen (lum < 80) die **helemaal binnen één onderdeel** liggen (plankennaden, jaarringen, noesten op romp/schijven/benen) worden ook vervangen; zwarte lijnen die iets anders raken (achtergrond, blad, riem, ander onderdeel) zijn omlijning en blijven. Ingesloten noesten tot 900 px vallen binnen het onderdeel.
- Romp: geen uitrekken maar een schoon donorstukje (561–632, 278–295; plank met verticale nerf) op schaal 1:1, gespiegeld herhaald over de romp.

| Onderdeel | Donorstuk | Schaal (donor→basis, ca.) | Noodvulling |
|---|---|---|---|
| voorhand | voorste bolhand boven de stok | 1 × 1,4 | ±13 % |
| voorarm | geribbelde bovenarm van de achterste arm (voorarm donor zit achter hand/baard) | 0,55 × 0,9 | 1 % |
| schouder (schijf) | achterste bovenarm (horizontale ribbels) | 0,7 × 0,7 | 3 % |
| elleboog (schijf) | achterste onderarm | 0,6 × 0,65 | 3 % |
| achterhand | achterste bolhand | 0,85 × 0,8 | 2 % |
| romp | plankstuk 71×17, 1:1 gespiegeld herhaald | 1 | 0 % |
| linkerbeen + heup | linkerdij (382–505, 380–452) | 1,2 × 0,95 | 4 % |
| linkervoet | onderbeen (425–502, 430–478) | 1,25 × 0,8 | 16 % |
| rechterbeen | rechterbeen | 0,9 × 0,9 | 11 % |
| rechtervoet | blauwe rechtervoet | 0,8 × 1,2 | 7 % |

Muts, bladbaard, neus, riem, rugkam met takje, zolen en stok: 100 % basis.

## Controle
- **Omtrekverschil (silhouet): 0 px.** Niet-witte pixels inclusief binnenglim: 4 px.
- Op 64 px leest het lijf als de donor (egaal roze hout met nerf, geribbelde blauwe broek); de houtschijven met jaarringen en noesten van de basis zijn weg.

## Zwakke punten
- Romp: herhaling van het kleine plankstukje is zichtbaar op modelmaat (regelmatig stippel-/streeppatroon); op spritemaat leest het als nerf. Een groter schoon donorstuk bestaat niet (de rest zit achter de bladbaard of loopt tegen zwarte randen).
- Schouder en elleboog blijven ronde schijven (omtrek van de basis) met geribbelde textuur; de donor heeft daar lange cilinders.
- Benen: zwarte donornaden worden losse diagonale strepen in de basisvorm (geprobeerd ze weg te laten: dan blijven grijze kartellijntjes over, dat was lelijker). Rechterbeen heeft aan de riemrand een paar lichtblauwe kartelpixels.
- Voorhand: lichtere, blokkerige ronde hand; de ribbels van de donorhand zijn grotendeels weg door het formaat.
