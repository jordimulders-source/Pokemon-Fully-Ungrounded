# Hitmongroove: sprite naar het Gemini-model, ronde 2 (maker)

Basis: `ronde1/capoeira.png`. Het model is bevroren (`referenties/gemini_gekozen_capoeira.png`). Opdracht:
- de benoemde reparaties: kop, steunarm, romp en de glans op de voeten;
- Jordi's feedback op ronde 1 (letterlijk): "ja de kop is niet meer herkenbaar hitmontop, het lichaam heeft een beetje een gekke vorm, het geelgroenpatroon is een beetje saaitjes en de lijnen mogen wat dynamischer. De arm onderin heeft nog geen goede vorm, zijn vooral rechte lijnen, de vuist sluit niet lekker aan en de band ook niet, maar je bent op de goede weg, blijf werken".

## Opgeleverd
| Bestand | Wat |
|---|---|
| `capoeira.png` + `raster.txt` | Variant A: benen zonder wit. 64×64, geïndexeerd, 16 kleuren, index 0 transparant. |
| `capoeira_B.png` + `raster_B.txt` | Variant B: benen met wit. Verder pixel voor pixel gelijk aan A. |
| `vel.png` | Rij 1: r2 A, r2 B, r1 en het model, allemaal op 8× in hetzelfde kader. Rij 2: de benen A, B en het model op 8×. Rij 3: de kop r2, het model en r1 op 12×. Rij 4: de romp en de steunarm r2 naast het model op 12×. Rij 5: A op 1× en 2×, licht en donker. |

Het tekenwerk staat als met de hand geschreven pixelruns in `hand_*.txt`. Ze worden in deze volgorde toegepast: kop, ogen, romp, benen A (en B), steunarm, netjes. Het armdeel van `hand_romp_arm.txt` is vervangen door `hand_steunarm.txt`. De scripts in `gereedschap/` doen alleen raster→png, montage, controle en metingen:
- `fijn.py`: modeltint per 1/3 spritepixel;
- `dek.py`: aandeel zwart/wit per pixel;
- `omtrek.py`: de modelomtrek over de sprite;
- `plak.py`: montage;
- `vel.py`: het vel.

Gewijzigde pixels ten opzichte van r1 (A):

| Zone | Pixels |
|---|---|
| Benen | 83 |
| Kop | 46 |
| Steunarm | 41 |
| Romp | 20 |

## 1. Kop: opnieuw getekend op de gemeten modelposities
Ik heb Hitmontop (`graphics/pokemon/hitmontop/anim_front.png`) naast het model bestudeerd. Hitmontops kenmerken zijn: zwarte ogen met een wit puntje, een lichte gezichtsplaat met een donkere lijn die het gezicht afbakent, en een puntje (hoorn). Elke lijn is 1 px, doorlopend en heeft één kleur.

Per onderdeel, vergeleken op 12× met het model:
- [x] **Kopomtrek.**
  - Bovenrand: één rij selout (5) tegen het gat, rij 33, kolom 15-19.
  - Rechts: de lijn kop/romp loopt in één diagonaal van (21,34) naar (26,40), als binnenlijn (5). Vanaf rij 41 wordt het de buitenlijn (1).
  - Onder: de silhouet van r1 (masker van het model).
  - De vuistrand en de linkerkant van de kop sluiten nu aan: (13,32-36), (12,37) en (11-10,38). In r1 zat daar een gat.
- [x] **V-lijn (haarlijn).** Eén doorlopende lijn in donkerbruin 5, gemeten op het model: (13,38) (13,39) (14,40) (15,41) (16-17,42), dan het punt op (18,43) tussen de ogen. Daarna loopt hij in één rechte lijn naar achteren: (17,44-48), tot in de onderrand. In het model is het verticale deel zwart. Ik heb één kleur gekozen, zodat het één lijn leest en niet versmelt met het zwarte rechteroog dat er vlak naast staat.
- [x] **Ogen.** Beide hebben dezelfde vorm, 111/161/.11: zwart met een wit puntje, op de gemeten pixels.
  - Oog 1: kolom 16-18, rij 38-40.
  - Oog 2: kolom 18-20, rij 45-47. Volgens de meting staat dit oog 1 kolom meer naar links dan in mijn eerste schets; het wit staat op (19,46).
- [x] **Mond.** Eén kort zwart streepje: (21,39) (21,40) (22,41) (22,42).
  - Het model heeft verder naar onderen nog een los streepje, bij (23,44)-(24,45). Dat heb ik niet als lijn getekend, omdat het als los lijnstukje leest. Het zit nu in de toongrens van de schaduw (de 4 begint daar). Weglaten mag eigenlijk niet: graag een oordeel van Claude of Jordi.
- [x] **Knot + witte band.**
  - Een rond bolletje op kolom 8-11, rij 40-45, met selout 5 aan de lichte kant en zwart onderaan.
  - Een witte band in de lengte op kolom 10 (rij 41-43 wit, rij 44-45 grijs), zoals in het model.
- [x] **Hoorn.** Een puntje naar linksonder: de punt op (8,48), rij 47 licht (3), rij 48 schaduw (4). De scheidingslijn naar de flap loopt via (12,48) (13,47) (14,47), met het inkepinkje op (13,48) zoals in het model.
- [x] **Tweede (onderste) plooi/flap.** Het vlak tussen de knot, de V-lijn en de hoorn: boven licht (3), onderaan in de schaduw (4, rij 46-48). De gezichtsplaat heeft een glans linksboven (2) en een schaduwsikkel rechts en onder (4). Elk vlak heeft ≤3 tinten.

## 2. Steunarm, vuist en banden (Jordi: "vooral rechte lijnen, de vuist sluit niet lekker aan en de band ook niet")
- **Koordband en polsband** zijn nu ringen om de arm. De bovenrand is recht en de onderrand gebogen: het midden ligt een rij lager, zoals de onderrand van de polsband in het model. Ze zijn licht aan de linkerkant (8/9 en wit) en donker aan de rechterkant (A en grijs). De koordband heeft een vlecht van 8/9/A.
- **Arm:** een lichte streep links, de basistint in het midden en schaduw rechts. De schaduw rondt onderaan naar de pols. De arm is 1 px smaller dan de polsband aan de rechterkant, zoals in het model.
- **Bal:** de polsband ligt over de bal heen. De bal komt links en rechts onder de band uit (rij 54) en de band werpt een schaduwrij op de bal (rij 55). Daardoor sluit de vuist aan en hangt hij niet los onder een blokje. Verder is het een ronde bal: glans linksboven, selout 5 aan de lichte kant en een sikkel rechtsonder.

## 3. Romp (Jordi: "een beetje een gekke vorm")
- Ik heb de omtrek gemeten tegen het modelmasker (`omtrek.py`, en de rechterrand per rij). Het silhouet ligt binnen 1 px van het model; ik heb de omtrek daarom niet verlegd.
- Wat de vorm hoekig maakte, was de tekening:
  - **De dubbele randband (4 + 5) langs de rechterkant is weg.** Dat was banding.
  - **De schaduw is één sikkel** met een vloeiende binnengrens. De verticale runs zijn 3-2-1-1, daarna 2 horizontaal.
  - **De glans linksboven** heeft een rechtergrens in een curvepatroon: 28, 28, 27, 26, 24.

## 4. Benen (nu wel aangepast, op Jordi's feedback "saaitjes", "lijnen dynamischer")
- **Scheen (beide varianten):**
  - De modelbanden staan nu met toonverloop: lichtgroen B aan de lichte kant, een brede gele band met een glansstreep 8 aan de lichte kant, groen C aan de schaduwkant.
  - Aan het linkerbeen ontbreekt de lichtgroene rand op rij 11-13, zoals in het model.
- **Vanaf de knie** (waar het wit in het model schuin begint): de gele band wikkelt schuin om het been naar de schaduwkant (A) en verdwijnt achter het been.
  - Linkerbeen: rij 14-18.
  - Rechterbeen: rij 17-19.
  - Het dijbeen bij het kruis is groen: B licht, C basis, D schaduw.
- **A:** zonder wit.
- **B:** het wit uit het model als schuine band (wit 6 met grijs 7 aan de schaduwkant). De band loopt direct achter de gele wikkelband om het dijbeen. Bij het kruis zit geen wit, dus er is geen blok.
  - Linkerbeen: rij 15-20.
  - Rechterbeen: rij 17-20.

## 5. Palet en voetglans
Er komt geen tint vrij: alle 16 zijn nodig (bruin 4, wit/grijs 2, geel 3, groen 3, blauw 2, omlijning en transparant). De glans op de blauwe voeten is daarom **niet** gedaan. Vrij te maken alleen door een tint te schrappen, bijvoorbeeld grijs 7 te vervangen door blauw-donker of wit. Dat is een keuze voor Claude/Jordi.

## Controle (A en B gelijk)
- 16 kleuren, inclusief transparant.
- 0 losse omlijningspixels midden in een vlak.
- 0 randpixels zonder donkere rand.
- Silhouet tegen het model buiten de steunarmzone: 43 px, hetzelfde als r1. Daarvan:
  - 12 px zijn het witte gat tussen de vrije arm en de kop. In het model is dat ingesloten wit; in de sprite is het transparant, zoals in r1.
  - De rest zijn randpixels met een modeldekking van 0,1-0,44.
- Vlakjes van minder dan 3 px die overblijven zijn bedoeld:
  - lijnstukken van de diagonale V-lijn en kop/romp-lijn (1-2 px per trede);
  - de glimpjes in de ogen;
  - het vlechtpatroon;
  - de knotband;
  - de selout van de bal;
  - de lichte streep in de arm (2 px).

## Eerlijke zwakke punten
1. **Steunarm.** Tussen de twee banden zijn maar 3 rijen arm zichtbaar, dus het tapse kan in de omlijning nauwelijks: de arm is daar recht, 3 px breed. Een taps stukje (links 1 px in) gaf een inkeping bij de polsband en heb ik teruggedraaid. De ronding zit nu vooral in de banden en de schaduw.
2. **Ogen.** Ze zijn 3×3, zoals de modelmaat (Hitmontop zelf heeft 4×4). Op 8× leest het wit nog als een punt in het midden. Groter kan, maar dat wijkt 1 px af van het model.
3. **Het tweede mondstreepje** van het model is als toongrens verwerkt, niet als lijn (zie de kop).
4. **De wikkel in de benen** is mijn vertaling van "schuin/gebogen om het been". In het model lopen de banden op de scheen in de lengte; alleen de grens naar het wit is schuin. Graag laten toetsen of dit "zoals in het model" genoeg is.
5. **Romp.** Het silhouet is niet veranderd, omdat het binnen 1 px op het masker ligt. Als Jordi met "gekke vorm" iets anders bedoelt dan de hoekige tekening (bijvoorbeeld de platte bovenkant onder het koord): vragen.
6. **Voetglans** niet gedaan (palet vol).

Niet gecommit, geen keurder gestart.
