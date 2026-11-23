# Pinsir-evolutie frontsprite, ronde 11 (laatste serieuze poging)

Jordi (letterlijk): "Ik wil dat je nog een hele serieuze poging doet om er iets van te maken, anders schrap ik dit idee".

Bestanden: `pinsir_evo_r11_A.png` (dekschild A), `pinsir_evo_r11_B.png` (dekschild B), `bouw.py`, `controle.py` (vlekjes en tinten), `vel.png`.
Bouwen: `cd pinsir_evo && python3 sprite_r11/bouw.py [raster]`; controle: `python3 sprite_r11/controle.py`.
Formaat: 64×64, geïndexeerd, index 0 transparant, 16 kleuren (palet r10; alleen o/x/w/v, die alleen in het dekschild voorkomen, zijn aangepast).

## Bevroren (script-check, diff 0)
Arm, verre arm, been, ver been, staart, romp, kaken, mond (r7-delenkaart) en het gezicht/de ogen van r10 (25 px). Kopsilhouet = r10, op één pixel na: (33,13) weg, zodat de punt van S5 1 px is (model: punt x32,3-33,2).

## 1. Kopschild en kam
- Per cel de modelklasse met de meeste pixels, na een modusfilter van 11 modelpx tegen de Gemini-ruis (geen celmediaan meer). In het kopschild (modelvlak 12) beperkt tot de vlakken van het model: lichte afschuining c, middenvlak b, donkere onderkant L, hooglicht d.
- Benoemde correcties (`KOPVLAK`), elk met de gemeten licht% (aandeel modelpixels ≥ 80):
  - hooglicht (17,21) en (18,21): 88 / 95 %;
  - lichte rand rechtsboven (32-33,23): 59 / 63 %;
  - lichte onderrand van de punt naar het gezicht (15,25) en (16,25): 45 / 87 %;
  - (13,24) en (14,25) b, (37,21) L.
- Tintvlekjes kleiner dan 3 px weggehaald (8-samenhangend, zodat een schuine rand als vorm telt). Kop: 8 over (r10: 21), allemaal stekel- of kegelflanken.
- Een kleine gradient in het middenvlak (achterkant één stap donkerder) is geprobeerd en geschrapt: die gaf een losse donkere vlek.

## 2. Stekels en kegels
Plek en maat komen uit het r10-silhouet (= modelmasker); per pixel staan dekking en licht% in de commentaren van `bouw.py`. De opbouw volgt Gen 3: Tyranitar (gekleurde selout aan de lichte kant, donkere onderflank), Cacturne (punt K, dan [selout, licht, K]) en Pinsir.
- Punt: 1 px K.
- 2 px breed: [c, K], dus een lichte flank links. Geen enkele 2-px-stekel is nog helemaal zwart.
- 3 px breed: [c, b, K] (S5) of [a, c, K] (S6; het model heeft daar links een zwarte lijn).
- Kegels in de donkere kam (K1-K3) als lichte flank c met een donkere flank a. Daarbij de lichte bovenrand van de rugplaat (30-31,18).

## 3. Rugdoorns en silhouet rechts
Het r10/r8-silhouet rechts van het schild was 1-4 px breder dan het model (dekking 0 op bijvoorbeeld (49,26), (50,28) en (51,28)). Het had ook 5 zelfgezette doorns.
- Nieuw silhouet = modelmasker (dekking ≥ 0,35). Daardoor vallen er 42 px af en komt er geen pixel bij.
- Rugdoorns op de modelplekken, met de punt gemeten: RD1 (48,24), RD2 (51,29), RD3 (52,33), RD4 (54,37). Opbouw zoals de stekels hierboven.
- Rij 23-28 rechts van het schild blijft donkere rug, zoals in het model.

## 4. Dekschild
**Studie Gen 3, wat ik overneem:**
- Heracross: één bolle vorm met een brede schaduwkant rechts en een donkerder lijn vóór de omtrek.
- Ledian: een lichte rand langs de bovenkant.
- Shuckle: de vlekken volgen de bolling (in de schaduw worden ze donkerder).
- Beautifly: weinig, grote vlekken zonder zwarte omlijning, met een tussentint aan één kant.
- Mega Pinsir: weinig grote vlakken, geen lijntjes.

**Vorm.** Het schildvlak is het modelschild (modelvlak 35, gesloten omtrek, ≥ 50 % per cel). Vanaf rij 29 loopt het tot de buitenomtrek: dat is de omgeslagen rand van het model, waar r10 een donkere 'rugrand' in lijftinten had.

**Belichting:**
- de lichte omtrek s van r10 links/boven blijft;
- lichte rand o (1 px) linksboven, hooglicht d op (39-40,26) en (39,27);
- basis x;
- schaduwsikkel w (1 px);
- omgeslagen rand v;
- omtrek K aan de schaduwkant.

**Palet,** naar de modeltinten met stappen van ±33: o (200,154,104), x (164,118,74), w (124,84,50), v (86,52,28), s (66,36,18). Een sikkel van 2 px maakte het schild te donker en is teruggebracht naar 1 px.

**Vlekken:** één stap donkerder dan hun ondergrond (x→v, in de schaduw s), met eigen schaduw s aan de rechterkant.
- **A**: de vijf hoofdvlekken van het model als strepen langs de schildas (richting 0,43 / 0,90): streep links, streep midden, twee middenvlekken en de grote vlek onderaan.
- **B**: vier grotere ronde schorsvlekken met een zoom w links (Beautifly) en schaduw s rechts.

**Vlekjes kleiner dan 3 px** in schild en rechtergebied: 6 (r10: 13). Dat zijn de flanken van de rugdoorns en 2 omtrekpixels van r10 bij de punt.

## Controle
- 16 kleuren, index 0 transparant; heropend en vergeleken.
- Zwart: 309 px (r10: 331).
- Tinten per vlak: kop K L a b c d, schild K s v w x o d (≥ 3 vultinten per vlak).
- Anders dan r10: A 264 px, B 255 px.

## Zelf zwak gevonden
- Het kopschild is schoner dan r10, maar blijft een modelvertaling: links een lichte wig met de Y-rug, rechts het middenvlak. Op 2× leest het nog iets onrustig rond de voorste stekels. De Y-rug en de onderrand zijn 1 px dun.
- Het lijf (bevroren) blijft donker en vlekkerig naast Gen 3. Daardoor leest de hele sprite op 1× nog doffer dan Pinsir en Heracross.
- Het dekschild is donkerder dan in r10, door het modelpalet en de schaduwkant. A leest als schors, B meer als 'gaten'.
- RD3 is een stompje van 2 px zwart (1 px breed in het model, er is geen plek voor een lichte flank).
