# Pinsir-evolutie (Bug/Ground) frontsprite, ronde 1

Bestanden: `pinsir_evo_r1.png` (64×64, geïndexeerd, index 0 transparant, 14 kleuren incl. transparant), `kaal.png` (kale reductie, zelfde palet), `bouw.py`, `vel.png` (r1 8× | kaal 8× | model op dezelfde schaal 8× / close-ups 12× kop+mond en kaken, poten+staart naast het model met spriteraster / 1× op wit, licht, donker naast Pinsir 1× + model 1×).
Gereedschap (`../gereedschap/`, gekopieerd van de Mightyena-evolutie en aangepast): `pitch.py`, `natief.py` (alleen meting), `model.py` (modelklassen per pixel + reductie), `gemeen.py` (palet, opslaan, tonen), `vel.py`, `kijk.py` (zone van sprite en model met spriteraster en coördinaten), `controle.py`, `zones.py`.
Bouwen: `cd pinsir_evo && python3 sprite_r1/bouw.py` (`kaal` toont alleen de kale reductie, `toon` print het raster). Vereist scipy.

## Metingen en methode
- **Raster:** pitch 10,24 (natief 99×99, figuur 95×73), maar Gemini tekende tanden, zaagtanden en klauwen fijner dan zijn eigen raster: de natieve mediaan verloor de tanden. Daarom geen natief raster/schrappen, maar reductie direct op het 1024-model.
- **Schaal:** de breedte bepaalt het (kaakpunt links x30 – staartpunt rechts x1003 = 974 px) → 974/64 = **15,22 modelpx per spritepixel**; figuur **x0–63, y13–61 = 64×49, 1688 px** (vult de breedte helemaal; hoogte volgt uit de modelverhouding). Niet gespiegeld (kijkt al naar links).
- **Kale reductie (`model.py`):** elke modelpixel krijgt een klasse (zwart <25; lijf 4 helderheidsbanden; kaak 3 banden binnen het warme kaakgebied; dekschild 3 banden binnen het schildgebied; crème = tand/oog). Per spritecel wint de klasse met de meeste pixels (zwart weegt 1,3× zodat de modellijnen blijven). Silhouet: cel hoort bij de figuur bij ≥ 35 % modeldekking (zodat dunne stekels, zaagtanden en klauwpunten blijven). Een warm-bruine buikvlek onder de kaakbasis telt als lijf, niet als kaak.
- **Silhouet = kale reductie, diff 0.** Modelgaten (tussen de kaken, tussen de poten) open.

## Palet (index: kleur)
0 transparant · 1 zwart (20,14,12) · lijf 2 (50,42,38) 3 (82,68,58; ook selout lijf) 4 (116,98,82) 5 (156,136,114) · kaak 6 (84,38,30; ook selout) 7 (128,68,50) 8 (164,104,78) · dekschild 9 vlek (90,52,26; ook selout) 10 (154,106,62) 11 (200,154,102) · 12 tand/oog crème (230,214,200) · 13 tandschaduw (168,150,138).
Kleur: modeltonen in dezelfde volgorde, het lijf iets opgelicht (model 36/72/96/128 → 46/69/99/135 gem.) zodat de lijftinten op 1× loskomen van de zwarte lijn ("Je mag met kleur altijd van het model afwijken"). Kaak = het bevroren donker roodbruin.

## Pixels die afwijken van de kale reductie: 273 van 1688 px (16 %), silhouet-diff 0
Per zone (`zones.py`): kopschild + stekels 49, lijf 21, dekschild 62, kaken 28, gezicht (ogen, mond) 27, poten en staart 86. Per stap (`bouw.py`):
- **1 tintvlekjes 113 + 1b draadjes 1:** tintvlekjes < 3 px (ruis van de reductie op de gestreepte modeltextuur) nemen de meest voorkomende buurtint van hetzelfde materiaal aan. Geen nieuwe tinten, geen vorm.
- **2 losse zwarte stukjes 10 + 7 controle 1:** zwarte 8-clusters ≤ 3 px midden in een vlak (niet aan de rand, buiten het gezicht) → buurtint.
- **3 dekschild 42:** schorsvlekken als minder, grotere vlekken op de modelplekken: per cel het modelaandeel vlek/licht, 3×3 gemiddeld, midden als grond, vlek bij ≥ 50 %, licht bij ≥ 30 %; vlekjes < 3 px weg. (3 drempelvarianten naast het model gelegd; deze lijkt het meest.)
- **4 mond + ogen 27 — gereconstrueerd, niet 1-op-1 uit het model:** het model heeft 5 tandrijen in 2 kolommen; bij 15 modelpx per spritepixel liepen ze dicht (kaal: 4 vage crème vlekjes). Gemeten modeltanden: x17,1–18,4 en x19,2–20,8, y30,1–34,2. Opbouw zoals de Gen 3-Pinsir (tanden en zwarte scheidingen om en om): zwart kader x16/x22, boven y29 (x17–21), onder **y35** (1 rij lager dan de modeltanden, nodig voor 3 tandrijen); tandrijen y30, 32 (crème 12) en y34 (tandschaduw 13; model: onderste tanden kleiner/grijzer) op x17 en x19–20, scheiding x18 en rijen y31/33 zwart; x21 = grijze wang (4) binnen het kader zoals het model. **Dus 3 tandrijen i.p.v. 5.** Ogen: links (16,27) zoals kaal; rechts 3 px crème (21–23,28) gemeten x20,9–23,5 — de kaal hield 2 px, **(23,28) is erbij gezet** (27 % dekking).
- **5 buitenlijn 68:** randpixels worden lijn: schaduwkant (achtergrond onder/rechts) zwart, lichtkant (alleen boven/links) selout in de donkere tint van het materiaal (kaak 6, schild 9, lijf 3); losse selout tussen zwart → zwart (geen om en om).
- **6 binnenlijnen 59 — kleur, geen vorm:** zwarte modellijn binnenin die alleen aan lichter lijf (3/4/5) grenst → 2, alleen aan kaak → 6, alleen aan schild → 9 (Gen 3: binnenlijn in de donkere tint van het vlak). Waar materialen of de donkere lijfmassa samenkomen blijft zwart. Lijnen blijven op hun modelplek.
- **8 klauwen 7:** zwarte cel binnenin de poten (y ≥ 52, niet aan de rand) waar het model ≥ 35 % belichte klauw/pantsertint heeft → die modeltint (de klauwen werden anders één zwarte vlek). Onderrand blijft zwart.
- Verder geen pixels die niet uit het model komen. Kaken, kopschild, stekels, zaagtanden, staart en poten: vorm = kale reductie.

## Controle (`controle.py`)
64×64, mode P, transparency 0, 14 kleuren incl. transparant (≤ 16). Geen lichte kleur op de buitenrand, geen losse zwarte pixels binnenin, geen selout/zwart om en om. Kaak 3 tinten + selout, schild 3 tinten, lijf **4 tinten** (2/3/4/5: donkere lijfmassa 2/3 + pantserplaten 3/4/5, zoals het model; 4 komt maar 44× voor). Zwart **31 %** van de figuur. Tintvlekjes < 3 px (4-samenhangend) die over zijn: vooral diagonale seloutlijnen (kaakbovenrand, 8-samenhangend één lijn), stekelpunten en klauwpunten (dunne modeldelen), mond/ogen (bewust).

## Resterende twijfels (eerlijk)
- **Zwart 31 %** (Gen 3 ±12–19 %): het model is een bijna zwart lijf met dikke zwarte segmentlijnen. Binnenlijnen naast lichter lijf zijn al donkerbruin; die in de donkere lijfmassa zijn zwart gebleven, anders verdwijnen de segmenten. Op een donkere achtergrond valt het lijf daardoor weg.
- **Mond:** 3 tandrijen i.p.v. 5 en 1 rij langer dan de modeltanden; leest als Pinsir-mond, maar is wel een reconstructie. Ogen zijn klein (links 1 px, rechts 3 px), zoals het model op deze schaal.
- **Zaagtanden van de kaken** lezen als trapjes in de zwarte rand (model: blokvormige zaagtanden van ±1–2 spritepixel); geen losse pixels, maar ook geen duidelijke tandjes.
- **Poten** zijn op 64 px druk (veel kleine pantserplaten en zwarte lijnen uit het model); knieplaten en klauwpunten zitten op hun modelplek, maar het onderste deel leest minder schoon dan kop, kaken en schild.
- Lijf heeft 4 tinten (zie controle).
