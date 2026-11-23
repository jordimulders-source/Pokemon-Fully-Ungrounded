# Gnometrotter Ice – hybride model (knippen en plakken)

- **Basis** (omtrek/pose/maat): `../r3/gemini_r3_lijf.png`. **Donor** (materiaal): `../r1/gemini_r1.png` ("ice perfect").
- **Resultaat:** `model_hybride.png` (1024×559). Vergelijking: `vergelijk.png` (basis | hybride | donor). Script: `python3 maak_hybride.py` (functies in `knip.py`, identiek aan die van Grass). Maskers ter controle: `debug_maskers_basis.png`, `debug_maskers_donor.png`.
- **Niets getekend** (Jordi: "je gaat niks of zo weinig mogelijk opnieuw tekenen"): elke vervangen pixel is een donorpixel (NEAREST, geen blur, geen kwantiseren nodig).

## Werkwijze
1. Basismaskers per onderdeel op kleur (roze: r>g en b≥g; blauw: verzadigd blauw, dus niet het grijsblauwe ijs van riem/zolen) binnen een kader per onderdeel. Pixels donkerder dan lum 105 vallen erbuiten: **alle zwarte lijnen van de basis blijven** (buitenomlijning, rand van schouder-/elleboogschijf, naad nek/romp, been/voet). Vlakken die via een gaatje in een lijn aan elkaar hangen worden eerst gesplitst (2 px eroderen). Dunne witte barstlijnen en kleine gaten horen bij het vlak.
2. Donormaskers idem, zonder de zwarte buitenrand en grijze anti-aliaspixels van het donorstuk; donkere naden binnenin blijven (dat is het ijsblokpatroon).
3. Per onderdeel: donorstuk (kader) geschaald op het kader van het basisonderdeel en alleen binnen het basismasker geplakt. Valt een bemonsterde pixel buiten het donormasker (baard ervoor), dan gespiegeld in de dichtstbijzijnde rand (textuur loopt door) of anders de randpixel ("noodvulling", per onderdeel gemeld).
4. Silhouetbewaker: waar het silhouet toch zou veranderen gaat de basispixel terug (0 px nodig).

| Onderdeel | Donorstuk | Schaal (donor→basis, ca.) | Noodvulling |
|---|---|---|---|
| voorhand | voorste bolhand | 1,2 × 0,8 | 4 % |
| voorarm | voorste armstuk (deels achter baard) | 0,6 × 0,55 | 26 % |
| schouder (schijf) | achterste schouderbol | 1,1 × 0,8 | 3 % |
| elleboog (schijf) | achterste bovenarm | 0,7 × 0,8 | 2 % |
| achterhand | achterste bolhand | 0,9 × 0,75 | 1 % |
| nek (2 stukjes onder snor) | romp naast de snor (540–592, 215–272) | ≈1 × 1,1 | 10 % |
| romp | zichtbare romp rechts van de baard (508–630, 228–336) | 1,6 × 1,4 | 5 % |
| linkerbeen + heup | linkerbeen | ≈1 × 1,1 | 12 % |
| linkervoet | linkervoet | 0,8 × 1 | 6 % |
| rechterbeen | rechterbeen | 0,9 × 0,9 | 16 % |
| rechtervoet | rechtervoet | 0,7 × 1,1 | 14 % |

Muts, baard, snor, neus, riem, rugkam, zolen, stok en gezicht: 100 % basis.

## Controle
- **Omtrekverschil (silhouet, alle niet-witte pixels met dichte binnengaten): 0 px.**
- Niet-witte pixels inclusief binnenglim: 663 px verschil (witte glimpixels binnen roze/blauw die nu donorkleur zijn; geen omtrek).
- Op 64 px (BOX-verkleining) leest het lijf als de donor: egale roze/blauwe ijsblokken, de diamantglim van de basis is weg.

## Zwakke punten
- De omtrek is heilig, dus schouder en elleboog blijven **ronde schijven** (vorm van de basis) met ijsblokvlakken erin; de donor heeft daar cilinders. Netter kan alleen door de omtrek te veranderen.
- Romp: de donorromp zit grotendeels achter de baard; het zichtbare stuk is ±1,5× uitgerekt (blokken van ±7 px i.p.v. 5).
- Voorarm: donorvoorarm zit achter de baard (26 % noodvulling); klein onderdeel.
- Benen: donornaden lopen niet precies mee met de basisvormen (heupvlak links heeft een paar losse donkere strepen); op spritemaat nauwelijks zichtbaar.
- Geen variant met donoronderdelen buiten het lijf gemaakt (baard/muts van r1 passen niet in de omtrek).
