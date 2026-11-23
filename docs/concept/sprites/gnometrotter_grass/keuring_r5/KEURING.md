# Keuring Gnometrotter Grass r5 (verse keurder, 23 nov)

Gekeurd: `../sprite_r5/gnometrotter_grass.png` · model `../hybride/model_hybride.png` (gedeelde geometrie, `gnometrotter_rock/sprite/kijk.py`) · zusje `gnometrotter_rock/af/gnometrotter_rock.png`.
Vel: `vel.png` (model | sprite, 8×). Alle coördinaten (x,y) in spritepixels; indexen naar het palet van de sprite.

## Oordeel: **FAIL**

## 1. Blind (1× en 8×, vóór het makerrapport)
- Leest als dezelfde kabouter als Rock: silhouet, pose, stok, rugpaal en zolen kloppen met het model.
- Wat meteen opvalt: de muts is één groot effen middengroen vlak, de bladbaard is plat lichtgroen met donkere nerven, de romp is links licht met verticale streepjes en rechts een effen blok, de riem en de zolen zijn effen bruin. Het lijf oogt nog vlak en "gekleurd", niet rond. Dat is wat Jordi slordig noemt.

## 2. Trouw aan het model en aan Rock af
| Onderdeel | Gemeten | Oordeel |
|---|---|---|
| Neus | Vorm en roze tinten 1-op-1 gelijk aan Rock af, **behalve de neusboog**: Rock af heeft op 8 px de zeer donkere roze tint (Rock-index 12 = 118,40,68), Grass heeft daar index 6. Het Grass-palet heeft die tint niet (index 12 is hier groen). | FOUT (Jordi r17: "zeer donkere roze tint") |
| Linkerhand | Gelijk aan Rock af, op 2 px na: (16,28),(17,28) zijn 5 (bladlijn), Rock heeft 6. | Bijna |
| Rechterschouder | Silhouet gelijk op 1 px na ((53,34) is 6, Rock 0). Binnenin 46 px anders: de bovenkant (40–43, 19–21) is licht 8 waar Rock schaduw 7 heeft (schaduw van muts/haar valt niet op de schouder), het binnenvlak (40–43, 27–32) is omgekeerd licht/donker, en **de zwarte buitenlijn rechts van de bovenarm ontbreekt**: (51,26),(52,27),(53,27),(54,28),(54,29),(55,30),(55,31),(55,32),(53,33),(54,33) zijn roze 6 tegen de achtergrond, terwijl er een zwarte lijn op (51,30),(51,31) binnenin de arm staat. | FOUT |
| Rest (muts, blad, rugpaal, stok, riem, benen, zolen) | Vormen volgen het model; niets toegevoegd of weggelaten gezien. | OK |

## 3. Gen 3-techniek per kleurzone
Telling per zone (px per index):

| Zone | Tinten | Volume | Oordeel |
|---|---|---|---|
| Muts (x17–40, y1–15) | 13: 155, 12: 67, lijn 5: 70; hooglicht 14: 2 | **Effen vlak**: één samenhangend 13-vlak van 151 px (grootste vlak van de hele sprite; bij Rock af is het grootste mutsvlak 71 px). Geen hooglicht, geen sikkel; alleen links licht / rechts schaduw met nerflijnen. Het model heeft hier wel verloop: luminantie ±115–123 linksboven, ±85–95 langs de middennerf (x 28–31) en onderaan. | FAIL |
| Bladbaard + wangblad (x15–41, y13–37) | 14: 122, lijn 5: 83, 13: 13 | **Effen**: elk blad is één lichte vlakkleur met donkere nerven; feitelijk 1 vultint. Het model heeft per blad een lichte en een donkere helft (lum ±150–170 tegen ±105–125). | FAIL |
| Romp roze (x17–50, y19–36) | 8: 123, 7: 132, 6: 69, F: 22 | 4 tinten, maar geen ronde bolling: grens 8/7 loopt als rechte verticale lijn op x 42/43 (rijen 24–31), rechts één effen 7-vlak van 61 px (x36–47). Naden als kaarsrechte kolommen (x 31, 35 in 6; x 37 in 7) over 9–16 rijen: banding-achtig, geen kromming. **Geen schaduwsikkel onderaan** boven de riem (rij 33–35 is 7, niet 6) en geen schaduw van de baard/muts op de romp. | FAIL |
| Riem bruin (x17–50, y33–42) | 3: 101, 2: 40, 4: 22 | 104 px effen 3; 4 alleen als horizontale band op rij 38 (parallel aan de rand). Rechterkant (x 42–50), die van de kijker af draait, is even licht als de voorkant. | FAIL |
| Benen blauw (x16–50, y41–56) | 11: 151, 10: 142, 9: 38 | Dijen: licht/mid-verdeling werkt redelijk. **Laarzen**: alleen 11 en 10; 9 alleen als lijn aan de linker (licht)kant (bv. (16,51),(16,52),(17,50)), geen donkere sikkel rechts/onder. Rock af heeft daar 9 aan de schaduwkant. Grootste 11-vlak 80 px (x31–48, y39–47). | BIJNA |
| Zolen bruin (y53–58) | 3: 51, 2: 20, 4: 3 | **Effen**: linkerzool rijen 54–55 = 3 over de hele breedte; 4 alleen op (44–46,57). Model: lichter bovenvlak linksboven (lum ±105–115 op x16–21). | FAIL |
| Stok, rugpaal | 2/3/4 alle drie gebruikt | Voldoende. | OK |

### Belijning
- Buitenrand links/boven in de eigen donkerste tint: muts in 5, maar **5 en 12 om en om** op de linker mutsrand: (21,6),(20,7),(17,12) zijn 12 tussen 5-pixels.
- Open randen (rechts, geen zwart): zie rechterschouder hierboven; daarnaast (60,36) rechterhand = 6 tegen de achtergrond (Rock: 1).
- Zwart binnenin: alleen (51,30),(51,31) is onnodig (zie schouder); (6,36),(8–10,35) onder de paddenstoelkop zijn gelijk aan Rock af en blijven.
- Trapjes/losse pixels: geen nieuwe gevonden buiten de lijn- en nerfpixels.

## 4. Reparaties
Vormen en silhouet blijven; niets hertekenen. Exacte pixels eerst, daarna zones.

**A. Rechterschouder = Rock af (exact, 46 px + 1).** Zet elke pixel op de waarde van Rock af:
(41,19)→7 (42,19)→7 (40,20)→7 (41,20)→7 (42,20)→7 (43,20)→7 (40,21)→7 (51,26)→1 (40,27)→7 (41,27)→7 (52,27)→1 (53,27)→1 (40,28)→7 (41,28)→7 (48,28)→7 (49,28)→7 (50,28)→6 (51,28)→8 (52,28)→15 (54,28)→1 (40,29)→7 (41,29)→6 (42,29)→8 (43,29)→8 (51,29)→7 (54,29)→1 (40,30)→6 (42,30)→8 (43,30)→8 (51,30)→7 (52,30)→8 (55,30)→1 (41,31)→8 (42,31)→8 (51,31)→7 (52,31)→7 (55,31)→1 (40,32)→8 (53,32)→7 (55,32)→1 (53,33)→1 (54,33)→1 (53,34)→0.

**B. Linkerhand = Rock af:** (16,28)→6, (17,28)→6.

**C. Neusboog = Rock af:** (17,20),(17,21),(17,22),(18,22),(19,23),(20,23),(21,23),(22,23) → zeer donker roze (118,40,68). Vereist een paletplek: liefst index 12 zoals bij Rock (gedeelde delen = zelfde indexen). Voorstel (beslissing coördinator): de twee lijntinten 2 (72,50,36) en 5 (38,70,42), die allebei alleen als donkerste eigen tint/lijn dienen, samenvoegen tot één donkere olijfbruine lijntint (± 54,58,38); het huidige groen van index 12 verhuist naar de vrijgekomen plek, en index 12 wordt (118,40,68).

**D. Mutsrand:** (21,6)→5, (20,7)→5, (17,12)→5. (60,36)→1.

**E. Groene ramp gelijkmatig maken** (kleur mag afwijken van het model): nu 14/13/12/5 = lum 169/111/71/50 (stap 58 tussen blad en muts). Voorstel ± 14 = (150,196,104), 13 = (110,156,82), 12 = (72,116,62), 5 blijft; stappen ±33.

**F. Muts (zone: alle 13-pixels in x17–40, y1–15):** volume uit het model overnemen als samenhangende vlakken (≥ 3 px): kleine hooglichtvlek 14 op de bolling van het linkerblad (rond x 21–26, y 4–9, waar het model het lichtst is), sikkel in 12 langs de middennerf (x 28–31) en langs de onderrand boven neus/baard (y 12–15), 13 blijft het middenvlak. Geen losse model-pixels: in de proef met een drempel op het model gaf dat tientallen losse pixels.

**G. Bladbaard en wangblad (alle 14-pixels in x15–41, y13–37):** per blad de schaduwhelft (rechts/onder van de middennerf, waar het model donker is) in 13; 14 blijft op de lichte helft. Nerven 5 blijven.

**H. Romp (6/7/8/15 in x17–50, y19–36):** naden laten staan; volume toevoegen: 6-sikkel van 1–2 px langs de onderrand boven de riem (rijen 33–35, x 29–41), de 8/7-grens als boog (niet de rechte kolom op x 42/43), en in het effen 7-vlak x 43–47 een donkerder rand naar rechts in 6 waar het lijf achter de schouder wegdraait. Schaduw onder de baard op de romp zoals Rock af.

**I. Riem (3-pixels in x17–50, y33–42):** rechts (x 42–50) donkerder (2-vlak, niet als lijn), linksvoor lichter; de 4-band op rij 38 laten verlopen in plaats van één rechte rij.

**J. Laarzen (x15–29, y49–53 en x39–50, y49–55):** 9-sikkel aan de rechter-/onderkant van elke laars (2–3 px breed, de bolling volgend), zoals Rock af.

**K. Zolen (3-pixels, y53–58):** bovenvlak linksboven in 4 (linkerzool ± x 16–21, y 54–55; rechterzool ± x 40–42, y 55–56), rechts/onder in 2.

Na de reparaties opnieuw keuren; de stand van A–D is met een pixeldiff tegen Rock af te bewijzen.
