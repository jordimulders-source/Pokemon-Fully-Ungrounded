# Gaucho-Lombre, frontsprite ronde 1 (maker, 25 nov)

Model: `../../r1/gemini_r1.png` (onaangeroerd, bevroren). Mond: Gen 3-Lombre (`graphics/pokemon/lombre/anim_front_gba.png`, frame 1), gespiegeld, in de snaveltinten van de gaucho-Lotad (Jordi: "de kleur die de snavel van lotad heeft").

## Bestanden
- `lombre_gaucho_A.png`, `_B.png`, `_C.png`: 64×64, P, index 0 transparant. Figuur **42×57** (x11–52, y6–62; voeten op rij 62), A/B 1549 px, C 1558 px. **15 kleuren incl. transparant** (index 14 is vrij). Buiten het mondvak (x17–38, y27–34) zijn de drie varianten pixelgelijk (diff A↔B 22 px, A↔C 89 px, alleen in dat vak).
- `*_8x.png`: elke variant op 8× op wit.
- `zonder_mond.png`: alles behalve de mond (gemeenschappelijke basis).
- `kaal.png`: kale reductie (alleen kwantiseren + schrappen, snavel nog geel).
- `vel.png`: A 8× | model op dezelfde schaal | kale reductie; kop 12× (A | model | Gen 3-Lombre gespiegeld); 1× A/B/C/Lombre/gaucho-Lotad op wit en donker; mond A/B/C op 8×.
- Scripts (volgorde): `pitch.py` (rastermeting), `natief.py` (natief raster), `kmeans.py` (modelkleuren), `quant.py` (paletindex per modelpixel), `kaal.py` (schrappen), `bouw.py` (opschoning + mond, schrijft A/B/C), `controle.py`, `vel.py`, `raster.py` (uitsnede met raster, hulpmiddel). `gemeen.py` = palet.

## Werkwijze
1. **Natief raster:** kamscore op de randsterkte geeft pitch **10,24 px = 1024/100** in x én y (fase 9,25). Natief 100×100, spreiding binnen een cel gemiddeld 0,7 (raster klopt precies). Figuur natief x21–74, y12–85 = **54×74**.
2. **Kleuren:** k-means (18) op de figuurpixels; elke modelpixel krijgt de dichtstbijzijnde modelkleur, bijna-gelijke modeltinten met dezelfde rol samengevoegd (zie palet). Geen middeling, geen nieuwe tinten.
3. **Verkleinen = schrappen** (Gengas-methode, niets hertekenen): 54×74 is te groot voor 64×64 en 2× (27×37) te klein, dus 17 rijen en 12 kolommen weg → 42×57 (factor 0,77). Per gelijk vak van de figuur één rij/kolom: die met het kleinste verschil met een buur, niet naast een eerder geschrapte, niet door het oog (rijen 36–41, kolommen 45–51 beschermd). Weg (figuurcoördinaten, natief = +12 rijen / +21 kolommen): rijen 2, 8, 10, 17, 19, 23, 30, 32, 37, 39, 46, 48, 55, 58, 62, 65, 72; kolommen 1, 5, 11, 15, 18, 23, 31, 33, 36, 42, 48, 52. Elke overgebleven pixel is een modelpixel.
4. **Opschoning** (`bouw.py`, basis voor alle varianten), zie hieronder.
5. **Mond:** het Lombre-mondstuk (Lombre-rijen 23–29, x30–45, gespiegeld) geplakt op de plek van de snavel; oogpixels worden nooit overschreven.

## Pixels die NIET uit het model komen (basis: 191 px verschil met de kale reductie)
- **Snavel weg (74 px):** alle snavelpixels → gezicht rood midden (4), de tint van het gezicht naast/boven de snavel in het model; ook de zwarte snavellijnen in het snavelvak (x18–29, y30–34).
- **Kopcontour onder de snavel (23 px):** het model laat daar geen kop zien (snavel ervoor). Voorkant op x20 recht door tot rij 31, dan een boog (21,32) (22,33) (23–26,34) naar de bestaande kinlijn; buiten de boog transparant. Schaduwsikkel rood donker (3) op rij 33 x23–29 en (22,32). In A/B/C is een deel hiervan weer overschreven door de Lombre-onderkaak.
- **Buitenlijn (78 px):** rand die alleen boven/links aan de achtergrond grenst = selout in de lijntint van het materiaal (rood 2, olijf 7), ook waar het model zwart heeft (zoals de gaucho-Lotad); rand rechts/onder = zwart, ook waar de schrapping een gekleurde randpixel overliet.
- **Binnenlijnen (22 px), alleen hertint:** zwart binnen één materiaal → lijntint (rood 2, olijf 6); zwart tussen rood en olijf blijft zwart. De kop (x18–36, y22–35) niet aangeraakt.
- **Losse tintpixels (21 px):** tintpixel zonder gelijke 8-buur → meest voorkomende buurtint uit dezelfde kleurgroep (geen lijntinten, geen middeling).
- **Nagels in de vuisten:** het model heeft daar snavelgeel; omgezet naar de Lotad-snaveltinten 13/12 (7 natieve px; dezelfde rol als de mond, en het modelgeel past niet meer in het palet).
- **Mond:** A 65 px, B 74 px, C 108 px (incl. de buitenlijn die na het plakken dicht moest: een niet-lijnpixel rechts/onder aan de achtergrond → zwart).

## Mondvarianten (de rest is pixelgelijk)
- **A:** Lombre-mond 1-op-1, gespiegeld. Lip 7 → 12 (179,155,90), lip licht b → 13 (228,199,123), zwart blijft zwart; de Lombre-onderkaak (bij Lombre teal) → gezicht rood midden. Lombre-kolom c → x = c+17, rij r → y = r+4: lip direct onder de ogen, punt 1–2 px voor de kopvoorkant, zoals bij Lombre.
- **B:** als A, maar de onderkaak ook in Lotad-snavel licht (13). Bij Lombre is de onderkaak lichter dan het gezicht; zo is de hele Lombre-mond (lip + kaak) in de snavelkleur van de Lotad.
- **C:** alleen in de breedte 1,5× (3× opblazen, exact 2× verkleinen, zwart wint bij de helft, zodat lijnen 1 px blijven), zo breed als de modelsnavel; 1 rij lager en 1 px verder naar voren zodat hij vrij blijft van het oog.
- Een 1,34× / 1,5× in beide richtingen heb ik geprobeerd: de lip overlapt dan het oog en de zwarte puntjes van de lippunt worden blokken. Niet opgeleverd.

## Palet (index: kleur, herkomst)
0 transparant · 1 zwart (20,16,18, Lotad-zwart; model 1,1,0) · rood: 2 lijn (118,48,31; k8+k13), 3 donker (159,69,46), 4 midden (201,111,77), 5 licht (211,125,90) · olijf: 6 lijn (46,36,22; k7+k14), 7 donker (92,80,48; k5+k16), 8 (118,99,65), 9 midden (145,130,78), 10 licht (174,157,100) · 11 oogwit crème (222,193,160, model) · 12 mond midden (179,155,90) en 13 mond licht (228,199,123) = Lotad-snavel · 14 (88,68,46) Lotad-snavellijn, **niet gebruikt** (de Lombre-mond heeft alleen zwarte lijnen) · 15 wit (model: nabij oog en ver oog). Bruin (72,42,24, 35 natieve px verspreide lijnpixels) is in rood lijn opgegaan.

## Zwakke punten (eerlijk)
1. **Mond leest deels als snor** (vooral A): de Lotad-snaveltint is een gedempt kaki dat op het rode gezicht minder contrasteert dan Lombre's rood op groen. B (lichte kaak) leest meer als mond. Kleur = Jordi's keuze, niet aangepast.
2. **Lippunt:** de zwarte puntjes van de Lombre-lippunt (1-op-1) zijn op 1× wat rommelig naast het verre oog; rond het verre oog (x20–22, y24–27) zit veel zwart bij elkaar (verre oog + kopvoorkant + bovenlijn van de lip). Het verre oog zelf (wit puntje met zwart) is het model.
3. **Kop onder de snavel is verzonnen** (contour + kaak), omdat het model daar alleen snavel heeft. Gehouden aan Lombre's kopvorm (voorkant recht, ronde kin).
4. **Schrappen op 0,77:** 1-px-details van het model worden soms dikker of breken: de hoedband leest drukker (zwart/olijf in plaats van een nette band met twee lijnen), vingerlijnen in de vuisten zijn minder duidelijk dan in het model. Alles staat nog op een modelpixel; niets bijgetekend.
5. **Gemengde lijnen uit het model:** het model heeft losse rode lijnpixels tussen zwarte lijnen (controle telt 44 "losse" pixels, vrijwel allemaal lijnpixels van een andere lijntint naast elkaar). Op de buitenrand is het nu consistent (selout links/boven, zwart rechts/onder); binnenin heb ik ze laten staan.
6. **Formaat:** 42×57, 1549 px (Gen 3-Lombre 41×45, 1072 px; gaucho-Lotad 1148 px). Hoogte zoals gevraagd (54–58); het meeste komt door de brede hoedrand.
7. Rood licht (5) ligt dicht bij rood midden (4) (helderheid 147 tegen 134), zoals in het model; voor Gen 3-contrast (±30–40) zou een lichtere hooglichttint beter zijn. Niet aangepast (kleurronde/keuring).
8. Nog geen keurder en geen DC-eindkeuring.
