# Keuring pitahaya-draak fase 1, sprite r2 (verse keurder, 16 nov)

Getoetst: alleen (1) trouw aan het model en (2) nette Gen 3-sprite. Gezicht (x 18–34, y 22–34: ogen, mond, tandje) alleen ter info.
Vel: `vel.png` (r2 8× met markeringen | natief model op hetzelfde raster | r1/r2 op 1× en 2× | Bagon, Treecko, Larvitar, Oddish op 2×).
Scripts: `meet.py` (modelblok per spritepixel), `stats.py`, `klont.py`, `rand.py`, `lijn.py`, `dunlijn.py`, `doel.py`, `naast.py`, `vel.py`.
Coördinaten zijn (x, y) in de 64×64-sprite. "Modelblok" = de 3×3 natieve modelpixels van die spritepixel (natief col = 1 + 3·(x+1), rij = 3·(y+2)).

## Oordeel: **FAIL** (klein: 33 px, alleen lijn- en tintwissels, silhouet blijft)

### Eerst op het oog
- **r2 tegenover r1 (1× en 2×): r2 is iets beter, niets is slechter.** Het lijf heeft nu links licht en rechts schaduw, zoals het model, en het groen heeft meer contrast. De kop is nauwelijks anders. Dambord gaat van 12 naar 7 (de rest zijn diagonale lijnen).
- **Naast het model:** het silhouet en de verdeling van licht en donker kloppen. Silhouet-diff met de kale reductie is 0, en met "≥ 5/9 modelpixels" is het silhouet-diff ook 0 (zelf nagemeten). Op de kop is links 20 helderheid lichter dan rechts, in de sprite 19,5. Niets is toegevoegd of weggelaten.
- **Hoofdvraag:** op 2× naast Treecko en Larvitar is de lijn veel zwaarder en is de kop onrustig. Losse zwarte en donkerroze pixels liggen midden in de vlakken, op plekken waar het model een dunne lijn heeft (≤ 1/3 spritepixel breed) of helemaal geen lijn. De regel "≥ 2 zwarte modelpx → zwart" verdikt de dunne modellijnen ongeveer 3×.

### Metingen
| | r2 | r1 | Bagon | Treecko | Larvitar | Oddish | Cacnea |
|---|---|---|---|---|---|---|---|
| zwart van de figuur | 19,7 % | 20,5 % | 6,2 | 18,1 | 12,0 | 11,7 | 17,5 |
| zwart binnen de figuur (geen randpixel) | **10,2 %** | 11,0 % | 0,9 | 4,1 | 5,0 | 2,6 | 7,7 |
| losse zwarte pixels (geen zwarte 4-buur) | **13** | 14 | 2 | 4 | 1 | 4 | 8 |
| zwart op de buitenrand | 62,8 % | 62,8 % | 31 | 61 | 42 | 43 | 54 |
| 2×2 zwarte klonten | 9 (4 in de ogen) | 9 | 0 | 1 | 3 | 0 | 16 |

- **Tinten per groep:** roze 3/4/5 + selout 2, groen 9/10/11 + 8, mauve kin 1 tint, amber 2, wit 1. Voldoet. Idx 8 is zowel selout als donkerste groen; dat is in Gen 3 gewoon.
- **Contrast** (paletwaarden; vlakpixels hebben precies die waarden): roze 62 → 90 → 133 → 168 (stappen 28 / **43** / 35), groen 67 → 99 → 132 → 169 (stappen 32 / 33 / 37). Alleen roze 3→4 ligt net boven 40 (zie KAN).
- **Buitenlijn:** zwart en selout wisselen nergens om en om (0). Aan de schaduwkant is alles zwart (71/71). Aan de lichtkant zijn 53 van 68 pixels selout; de 15 zwarte zitten onder de kop (overschaduwd, mag), aan de ooghoek (gezicht, info) en op linkerbeen en -voet (M4).
- **Vlakjes < 3 px buiten het gezicht:** 29. Het grootste deel is kenmerk: groene schubpunten van 1–2 px (idx 11) en klauwtenen (y 52–53). Zie KAN 4.
- **Licht en schaduw:** licht linksboven, sikkel rechts en onder op kop en lijf. Geen pillow shading of banding gevonden.

## MOET (33 px; silhouet-diff 0, gezicht niet aanraken)
Het doel staat steeds als "neem over uit het model". "Vul lum" is de gemiddelde helderheid van de niet-zwarte modelpixels in het blok; de doeltint is de dichtstbijzijnde paletwaarde.

1. **Losse roze naadpixels zonder modellijn in de kop** (idx 2, 0/9 zwart in het modelblok, hooguit 1 lijnbuur). Het model toont daar vulling, dus neem de vultint over:
   - (37,10) 2 → 3 (vul lum 94)
   - (36,15) 2 → 3 (lum 111)
   - (29,18) 2 → 3 (lum 104)
   - (35,19) 2 → 3 (lum 96)
   - (38,27) 2 → 4 (lum 117)
2. **Zwart in het lichte kopvlak** (linkerhelft, lichtkant):
   - (25,14) 1 → 5. Het modelblok is 3/9 zwart (een dunne rand); de rest is licht roze met lum 158. Nu staat er een losse zwarte pixel midden in het licht.
   - (31,14) en (31,15) 1 → 2. Model: een dunne naad tussen twee schubben (2/9 en 4/9 zwart). Een binnenlijn aan de lichtkant hoort in de donkere tint van het vlak.
   - (30,13) 1 → 8. Het modelblok is overwegend groen (de onderrand van de schubpunt) met 4/9 zwart. Zonder deze wissel blijft hij als losse zwarte pixel over na de vorige stap.
3. **Lijf, lichtkant: dunne zwarte binnenlijnen naar het model** (modelblok 2–3/9 zwart):
   - (25,39) en (25,40) 1 → 8: een losse verticale zwarte streep op de borst, vul lum 86/73.
   - (33,39) 1 → 8: een losse pixel met 0 zwarte buren, vul lum 79.
   - Linkerklauwen: (20,43) 1 → 10 (vul lum 120), (17,45) 1 → 11 (vul lum 153). In het model zijn dit groene vingers, geen zwarte klont.
   - (21,43) en (21,44) 1 → 8.
   - Linkerbeen naar de buik: (24,50) en (25,51) 1 → 8 (3/9 en 2/9 zwart). Anders blijven het losse zwarte pixels.
4. **Buitenlijn aan de lichtkant van linkerbeen en -voet:** (23,49), (23,50) en (20,52) 1 → 8 (selout aan de lichtkant). (21,52) 1 → 10: dat is een binnenpixel met 2/9 zwart en vul lum 124.
5. **Dambord** van 9 en 8 op (38,39)–(39,40): (39,39) 8 → 9 en (38,40) 8 → 9. Model: 0–1/9 zwart, vul lum 79–104, dus één tint.
6. **Dunne zwarte binnenlijnen aan de schaduwkant** (modelblok 2–3/9 zwart) worden de donkere tint van het vlak; de buitenlijn blijft zwart. Hiermee komt het binnen-zwart rond 8 % (Gen 3: 1–8 %):
   - Kop rechts: (38,28), (38,29), (38,30) en (37,31) 1 → 2.
   - Rechterarm over het lijf: (35,39), (35,40), (36,40), (37,40) en (37,41) 1 → 8. (36,40) heeft 4/9 zwart; zonder deze wissel blijft hij los over.

Gesimuleerd in `sim_moet.png`: zwart van de figuur 17,3 %, binnen-zwart 8,1 %, dambord 3 (alle drie diagonale lijnen), losse zwarte pixels 8. Daarvan zitten er 4 in het gezicht; de andere 4 zijn echte modellijnen van 4–5/9 zwart: (31,10), (44,19), (42,27) en (40,30). Daarna opnieuw meten (losse lijnpixels, vlakjes, dambord) en r3 naast r2 op 1× en 2× leggen.

## KAN
1. **Roze stap 3→4 is 43.** Alleen een paletwaarde: idx 3 iets lichter (lum ±95). Controleer daarna dat de kleuraard gelijk blijft.
2. **Naadfragmenten in de kruin** die wel op een modelnaad liggen maar onderbroken zijn: (33,16)–(34,16), (42,15), (40,19), (43,23) en (41,24). Het model toont doorlopende schubranden. Sluit ze alleen waar het modelskelet loopt (modellijnen projecteren zoals bij spooktrein fase 3), of verzacht ze naar tint 3.
3. **Linkerbeen y 47–48, x 25–28:** idx 8, terwijl het model daar 13–36 lum lichter is. Eventueel 8 → 9 naar het model.
4. **Vlakjes < 3 px die geen kenmerk zijn:** 9 op (24,37), (29,38), (26,51) en (39,52), 10 op (20,44)–(20,45). Ze kunnen de meest voorkomende 4-buur uit dezelfde groep worden, als het model daar geen eigen vorm heeft.
5. **Dubbele rand rechtsboven** (x 43 zwart, x 44 groen, x 45 zwart, y 8–12): staat zo in het model (schubpunt met schaduwrand). Mag blijven; op 1× leest hij als streepjes.

## Ter info (geen keuring)
- **Ogen:** het verre oog is 1 px breed amber, het nabije oog heeft een glans op (31,25). Dit komt later apart met Jordi.
- **Mond en tand:** zwart op (31,31) (modelblok 2/9 zwart, lum 122) en op (21,31) en (22,32) in de mondlijn. Zit in het bevroren gezicht.
- **Grootte:** 31×49, 1087 px. Voor een fase 1 is dat groot (checklist D1: 700–950; Bagon 763); de hoogte is wel Bagon-maat.
