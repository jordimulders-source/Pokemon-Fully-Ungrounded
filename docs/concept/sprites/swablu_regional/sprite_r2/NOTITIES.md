# Onweerswolk-Swablu frontsprite, ronde 2

Jordi over r1: "swablu is nog wat blurry".
Bestanden: `swablu_r2.png` (64×64, geïndexeerd, index 0 transparant, 15 kleuren incl. transparant), `swablu_r2_8x.png` (8× op wit), `vel.png` (r2 8× | r1 8× | model op schaal 8× / close-ups 12× kop+voelsprieten en staartje, sprite | model / 1× licht, crème, donker, zwart + model 1×), `bouw.py` (bouwt op `sprite_r1/swablu_r1.png`; draaien vanuit `swablu_regional/`).

## Oorzaak van de blur (gemeten)
r1 koos per spritepixel de paletkleur bij de **gemiddelde** modelkleur. Waar twee modelvlakken samen in één spritepixel vallen, werd dat een middentint, dus verloop i.p.v. vlakken. Daarbij lagen de wolktinten dicht op elkaar (L 148/166 en 109/119). Het model zelf staat al in duidelijke banden: lichte bollen ~200/~165/~138, onderwolk ~138/~112/~84.

## Wat r2 doet (silhouet bevroren: alpha-diff met r1 = 0)
1. **Toonstemming** (321 px): per spritepixel stemmen de natieve modelpixels op hun modelband (oppervlaktegewogen) en de meest voorkomende band wint. Grenzen: wolk ≥188 wit, ≥152 licht, ≥124 midden, ≥97 donker, anders diep; vogel ≥145 licht, ≥105 midden, anders donker. Zo ontstaan vlakken zoals in het model.
2. **Naden** (10 + 10 px): waar het model een lijn heeft die wegviel. Donkere naden (zwart/donkergrijs L<70, ≥15 %, rug van de lijn) worden zwart (als het model daar zwart is) of wolk diep. Grijze naden in de lichte bollen (L<124, ≥20 %, rug) worden wolk midden. Alleen binnen de figuur.
3. Buitenlijn (31 px), dezelfde regel als r1: lichte bol → midden, onderwolk/vleugel → diep, vogel → donker.
4. Ontkorrelen (20 px): tintvlekjes < 3 px → buurtint van dezelfde groep.
5. Bevroren uit r1: de voelsprieten (8 px terug) en de r1-reparaties: oog, kruin, snavelrand, zwarte lijn onder het staartje (2 px terug).
6. Staartje (2 px): de grijsblauwe vulling (45–48,45) wordt wolk diep, de band van de onderwolk eromheen (model L~85).
7. Snavelbovenrand (3 px): (22–24,27) één tint wolk midden (er stonden drie tinten door elkaar).
8. **Hooglicht kop** (3 px): (27,25) (25,26) (26,26) → vogel licht, naast de 3 lichte modelpixels (26,24) (25,25) (26,25). Samen een klein vlak op de bolling linksboven. Het model is daar vlak; Claude stond dit toe.
9. **Vonken** (5 px): feller palet. Oker alleen op de buitenhoek rechtsonder (lucht rechts én onder), fel geel waar de pixel aan lucht grenst, lichtgeel alleen binnenin (geen lichte buitenrand). r1 had 10 okerpixels, r2 heeft er 6.

**Afwijkend van r1: 299 px.** Per zone: onderwolk+staartje 228, vleugel+wolk rechts 43, wolk links 13, kop+oog+snavel 10, voelsprieten+vonken 5. Bijna alles is toonstemming (een andere band op dezelfde plek). Getekend is alleen het hooglicht op de kop (3 px, toegestaan).

## Palet r2
0 transparant · 1 zwart (13,17,24) · wolk 2 diep (68,78,96) 3 donker (96,108,126) 4 midden (126,138,156) 5 licht (164,176,192) 6 wit (210,216,228) · vogel 7 donker (68,90,110) 8 midden (106,130,152) 9 licht (150,174,194) · geel 10 oker (200,158,40) 11 geel (248,214,64) 12 lichtgeel (255,246,160) · 13 snavelwit (214,220,230) 14 glans (250,251,253).
Stappen in de wolk: L 210 → 170 → 136 → 106 → 77 (±30–40). Lichte bollen: 6/5/4. Onderwolk: 4/3/2 + zwart.

## Controle
15 kleuren incl. transparant; per materiaal ≤ 3 tinten + selout; geen lichte kleur op de buitenrand; geen losse zwarte pixels; zwart 15,4 %. Overgebleven vlekjes < 3 px zijn selout-/naadpixels, spriet (1 px) en vonken.

## Twijfels
- **Onderwolk:** drie horizontale banden (midden boven, donker, diep onderaan), zoals de modelbanden. Daardoor lezen de bulten van de onderwolk vooral als banden, met maar enkele naden (bij x22 en x27–30). Een keurder kan dat banding noemen. Het model heeft daar wel aparte bulten met lichtere toppen.
- Naden in de lichte bollen: maar 10 px kwam boven de drempel. De bollen scheiden zich vooral door licht/schaduw, niet door lijnen (zoals in het model).
- De vonken hebben nog maar 5 px lichtgeel; ze zijn feller, maar ze zijn smal.
