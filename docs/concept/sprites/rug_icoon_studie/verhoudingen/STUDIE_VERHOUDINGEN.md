# Meetstudie: verhoudingen front → icoon (18 nov)

Vraag van Jordi: "kan je daar gemiddelden uithalen qua afwijkingen, en welke ledematen hoeveel procent vergroot of verkleind raken" · "dan wordt het geen giswerk meer".

## 1. Opzet
- **Bron:** in-game set (`graphics/pokemon/<soort>/anim_front.png` frame 1 + `normal.pal`; `icon.png` frame 1 + `icon_palettes/pal<iconPalIndex>.pal`). De GBA-set is niet gebruikt: de soorten die op onze fakemon lijken zijn vooral Gen 4+.
- **31 soorten:** 26 viervoeters/knaagdieren (rattata, raticate, zigzagoon, linoone, sentret, furret, eevee, pikachu, raichu, pachirisu, skwovet, yungoos, bunnelby, buneary, meowth, persian, glameow, purrloin, litten, rockruff, poochyena, electrike, mudbray, sandshrew, nickit, dedenne), 3 vogels (pidgey, taillow, starly) en 2 tweevoeters (riolu, mankey). Minccino is overgeslagen (frontaal, oorlobben en kop niet van elkaar te scheiden); lopunny niet gedaan.
- **Punten met de hand afgelezen** op uitvergrote roosters (`rooster.py`, met de indexrasters uit `laad.py` waar het nauw luisterde) en per soort gecontroleerd op een vel: `vel_punten_1.png`, `vel_punten_2.png` (front 4× | icoon 8×, dus 1 icoonpixel = 2 frontpixels; paars = kop, rood kruis = oog, rode lijn = oortop, blauw = romp/buik, groen = onderkant poten, oranje = staart).
- **Wat er gemeten is** (afspraken bovenaan `punten.py`): kopkader zonder oren (snuitkant tot achterkant kop/kraag, kopboven tussen de oren tot kin), oogmidden en oogmaat, oortop (oorlengte = kopboven − oortop), romp (lijflengte), buiklijn en onderkant van voor- en achterpoot (pootlengte = onderkant − buik), staartkader (langste zijde).
- **Rekenwijze:** algemene schaal S = icoonhoogte / fronthoogte. Een onderdeel heeft "×1,25" als het in het icoon 25% groter is dan bij gewone verkleining met S. Oogplek: horizontaal 0 = snuitkant, 1 = achterkant kop; verticaal 0 = kopboven, 1 = kin.
- **Groepen:** "zijaanzicht" = viervoeters in 3/4 of profiel zonder posewissel (15 soorten; de bouw van onze fakemon, ook de viscacha). Frontale soorten tellen niet mee voor de snuit en de horizontale oogplek.
- **Nauwkeurigheid:** ±1 px in het icoon. Op een icoonkop van ±10 px is dat ±10%. Daarom staat bij elke regel de spreiding (p25–p75 = de middelste helft van de soorten).

Data: `data/punten.json` (alle punten), `data/metingen.csv` (per soort alle maten en verhoudingen), `data/samenvatting.json` (statistiek per groep). Opnieuw rekenen: `python3 analyse.py`.

## 2. Uitkomst

### Verhouding icoon : front t.o.v. gewone verkleining (mediaan, p25–p75)
| onderdeel | zijaanzicht (n) | alle 31 (n) | vast genoeg voor een regel? |
|---|---|---|---|
| algemene schaal S (hoogte) | **0,45** (0,43–0,47) (15) | 0,45 (0,43–0,49) (31) | ja |
| schaal in de breedte | 0,50 (0,44–0,54) | 0,50 (0,45–0,55) | ja: het icoon is relatief breder |
| kopbreedte | **×1,27** (1,08–1,31) (15) | ×1,21 (1,05–1,33) (31) | ja |
| kophoogte | **×1,25** (1,13–1,45) (15) | ×1,25 (1,09–1,46) (31) | ja |
| kop als deel van de figuurhoogte | front 0,39 → icoon **0,50** | 0,36 → 0,50 | ja |
| kop t.o.v. lijf | **×1,33** (1,17–1,50) (15) | ×1,23 (1,12–1,49) (27) | ja |
| snuit (snuitpunt → oog) | **×1,27** (1,01–1,38) (15) | ×1,18 (0,99–1,36) (21) | ja |
| lijflengte | **×0,95** (0,84–1,05) (15) | ×0,95 (0,84–1,13) (27) | ja: lijf = gewone verkleining |
| staart (langste zijde) | ×1,11 (0,98–1,18) (13) | ×1,07 (0,93–1,17) (26) | ja, maar zie lange staarten |
| oorlengte | ×1,25 (0,95–1,89) (13) | ×1,25 (1,07–1,99) (27) | **nee** als factor; wel als pixelregel (zie 3) |
| oogmaat | ×1,40 (1,08–1,68) (15) | ×1,33 (1,08–1,72) (31) | als pixelregel (oog is 1–3 px) |
| voorpoot | ×1,17 (1,04–1,28) (14) | ×1,04 (0,77–1,20) (26) | als pixelregel (kort groeit, lang krimpt) |
| achterpoot | ×0,79 (0,54–0,98) (10) | idem | **nee**: weinig soorten, vaak verborgen |

### Oogplek in de kop
| | front | icoon | verschuiving (p25–p75) |
|---|---|---|---|
| horizontaal (snuit 0 → achterkant 1), zijaanzicht | 0,61 | 0,58 | **−0,01** (−0,07…+0,05) |
| horizontaal, alle niet-frontale | 0,61 | 0,58 | −0,01 (−0,04…+0,03) |
| verticaal (kopboven 0 → kin 1), zijaanzicht | 0,57 | 0,61 | **+0,05** (0,00…+0,11) |
| verticaal, alle 31 | 0,57 | 0,54 | +0,04 (−0,05…+0,11) |

Het oog **verschuift dus niet** binnen de kop: het blijft op dezelfde relatieve plek, hooguit een halve pixel lager. Omdat de kop als geheel ×1,25 groter wordt, schuift het oog in absolute pixels wel mee naar achteren en omlaag (de snuit voor het oog groeit even hard mee: ×1,27).

### Pose en kijkhoek
- **27 van 31 houden de pose en kijkhoek van de front** (3/4 blijft 3/4, profiel blijft profiel, frontaal blijft frontaal). Geen enkele is gespiegeld.
- **4 van 31 krijgen een eigen pose** (`posewissel` in de data): linoone (lang plat lijf → staart rechtop, lijf ingekort), furret (rechtop → opgerold/liggend), raichu en purrloin (staart van links naar rechts achter het lijf). Steeds om het figuurtje compact te maken of de staart achter het lijf te leggen; de kop houdt dezelfde kijkhoek.
- Bij yungoos en zigzagoon komt de staart iets meer omhoog; persian en mudbray houden de pose maar met veel kortere poten.

## 3. Rekenregels voor het icoonscript
Volgorde: eerst de hele figuur met S verkleinen, dan per onderdeel bijstellen. Pixelregels komen uit een rechte lijn door alle 27 soorten zonder posewissel (icoon = a + b × front, in pixels); "rest" is de typische afwijking van een soort tot de lijn.

| regel | waarde | spreiding | hardheid |
|---|---|---|---|
| figuurhoogte | **0,45 × front** | 0,43–0,47 | vast |
| figuurbreedte | 0,50 × front (relatief breder, compacter) | 0,44–0,54 | vast |
| kop (breedte en hoogte) | **×1,25 t.o.v. S**, dus ±0,56 × front | ×1,08–1,45 | vast |
| kop in pixels | breedte = 5,6 + 0,31 × front; hoogte = 5,5 + 0,26 × front | rest ±1,1–1,2 px | vast; kleine koppen groeien relatief meer |
| kop t.o.v. lijf | **+33%** | +17…+50% | vast |
| kop beslaat | **de helft van de icoonhoogte** (front 39%) | 43–57% | vast |
| lijf | ×1,0 (gewone verkleining) | ×0,84–1,05 | vast |
| snuit (punt → oog) | ×1,27, dus groeit mee met de kop | ×1,01–1,38 | vast |
| oog binnen de kop | **zelfde relatieve plek als de front**; verticaal hooguit +0,05 (een halve pixel lager) | horizontaal −0,07…+0,05, verticaal 0…+0,11 | vast |
| oogmaat | 1,0 + 0,26 × front-oog (px). In de praktijk: front-oog ≤ 3 px → 1×2 of 2×2; 3–4,5 px → 2×2 of 3×2 | rest ±0,4 px | vast |
| oor (boven de kopboven) | 2,0 + 0,29 × front. Kort oor (≤ 4 px) ×2,4; middel (5–8) ×1,24; lang (≥ 9) ×1,08 | rest ±1,3 px | **als factor te los**; als pixelregel redelijk |
| voorpoot | 1,2 + 0,28 × front: kort (≤ 4) → 2 px (×1,17), middel (5–8) → 3 px (×1,09), lang (≥ 9) → ±4 px (**×0,71**) | rest ±0,9 px | redelijk; minimaal 2 px |
| achterpoot | ±0,7 × gewone verkleining, minimaal 2 px | ×0,54–0,98, n = 10 | **los**: alleen als richtlijn |
| staart | 3,0 + 0,32 × front (×1,1 bij 10–33 px) | rest ±1,9 px | redelijk; heel lange staarten (> 33 px) krimpen meer dan de factor zegt |

Het patroon achter alle regels: **kleine onderdelen krijgen een minimummaat (2–3 px), grote onderdelen worden juist relatief kleiner**, en de kop (met oog en snuit) groeit als geheel ±25% ten koste van poten en romp. Waar de factorspreiding groot is (oren, poten, oog) komt dat door die minimummaat; de pixelregel vangt het wel.

**Waar de spreiding te groot is voor een regel:** oorlengte als percentage (×0,5 tot ×4,6), achterpoten (te weinig zichtbaar, n = 10) en de pose zelf (posewissel is een ontwerpkeuze per soort, geen formule). Frontale soorten (10) passen in de kop- en oogregels, maar niet in de snuitregel.

## 4. Controle: viscacha
Script: `viscacha_controle.py`; vel: `vel_viscacha.png` (front 4× | `icon_a2_af` 8×; paars = kop, rood kruis = oog nu, blauwe cirkel = voorspeld oogmidden, blauw kader = p25–p75).

**Frontpunten uit `gelijkenis.py` → FRONT['viscacha'] gecontroleerd** tegen de pixels van `viscacha/af/viscacha.png`: snuit (8,5; 34), wangpluk (7,5; 30,5), kraag (22,5; 32), kin 38,5, oor_ver (12; 15) en oor_nabij (25; 16) kloppen binnen een halve pixel. Twee afwijkingen: het oog (zwart blok x 14–18, y 29–31, glans (16,30)) heeft zijn midden een halve pixel verder rechtsonder dan (16,0; 30,0); en **kopboven 25,5 is de oorbasis van het nabije oor, niet de schedel**: tussen de oren (x 15–17) ligt de bovenrand op y 23. In deze studie geldt y 23 (dezelfde afspraak als bij alle 31 soorten).

Gebruikte front-maten: kop x 7–24, y 23–39 (18 × 17), oog midden (16; 30), 4×3, oortop y 15 (oor 8 px), voorpoot 7 px, achterpoot 11 px, staart 36 px, fronthoogte 49.

| onderdeel | voorspeld (mediaan, p25–p75) | icon_a2_af | oordeel |
|---|---|---|---|
| figuurhoogte | 22,1 (20,9–22,8) | 22 | goed |
| kopbreedte | 10,3 (8,8–10,7) | 10 | goed |
| kophoogte | 9,6 (8,6–11,1) | 8 | 1–2 px te plat |
| oorlengte | 4,5 (3,4–6,8); pixelregel 4,3 | 5 | goed |
| oogmaat | 2,2 (1,7–2,6): 2×2 of 3×2 | 3×2 | goed |
| snuit (snuitpunt → oogmidden) | 5,4 (4,3–5,9) | 3,5 | **2 px te kort** |
| voorpoot | 3,7 (3,3–4,0); pixelregel 3,2 | 3 | goed |
| achterpoot | 3,9 (2,7–4,9) | ±4,5 | goed |
| staart | 18 (16–19); pixelregel 14,5 | 15 | goed (36 px valt buiten het gemeten bereik; de pixelregel past beter, en Jordi noemde de staart al perfect) |
| oog horizontaal in de kop | 0,52 (0,46–0,58) | **0,33** | buiten de spreiding |
| oog verticaal in de kop | 0,49 (0,44–0,55) | 0,50 | goed |

**Oogplek in pixels:** voorspeld oogmidden **x ≈ 10,7–10,9** (bereik 10,1–11,4) en **y ≈ 16,4** (16,1–16,8). Nu: x 9 (zwart blok x 8–10, glans (10,16)), y 16,5.

**Antwoord op "staat het oog genoeg naar rechts?": nee.** Het oogmidden hoort ±2 px verder naar rechts (zwart blok op x 10–12 in plaats van 8–10), op dezelfde hoogte (rijen 16–17). Dat volgt uit twee onafhankelijke regels die hetzelfde zeggen: de plek in de kop (front 0,53 → icoon nu 0,33; de spreiding over 15 soorten is maar ±0,06) en de snuitlengte (snuitpunt → oog 5,4 px voorspeld, nu 3,5). Omdat het oog tegen de kraag aan moet blijven ("het oog zit naast de wang maar kleiner"; oog → kraagmidden voorspeld 3,7 px, nu 3,3), schuift de gele kraag 1–2 px mee naar rechts; de kop wordt dan hooguit 1 px breder (binnen de spreiding). Zonder die verschuiving zit het oog nu te ver naar voren, op een derde van de kop in plaats van in het midden.

(`gelijkenis.py` meldde eerder het omgekeerde, "oog te ver naar rechts", omdat het de plek meet tussen snuit en kraagmidden: de kraag staat in het icoon te dicht op het oog, dus die maatstaf wijst de verkeerde kant op. Met de kop als kader, zoals bij alle 31 soorten, klopt het beeld wel.)

## 5. Bestanden
- `docs/concept/sprites/rug_icoon_studie/verhoudingen/`
  - `STUDIE_VERHOUDINGEN.md` (dit bestand)
  - `punten.py` (handmatige punten + afspraken), `laad.py` (front/icoon laden, tekstrasters), `rooster.py` (afleesrooster), `analyse.py` (rekenen), `vel_punten.py` (controlevellen), `viscacha_controle.py`
  - `data/punten.json`, `data/metingen.csv`, `data/samenvatting.json`
  - `vel_punten_1.png`, `vel_punten_2.png` (controle van alle punten), `vel_viscacha.png`
- Afleesroosters per soort (tijdelijk): scratchpad `studie_verh/r_<soort>.png`.

## 6. Beperkingen
- Eén meter (Claude), met de hand; ±1 px in het icoon. Kopkader en buiklijn zijn interpretatie (vooral bij gehurkte en frontale soorten); de vellen tonen wat er gemeten is.
- Gemeten op de in-game set (moderne iconen). De Gen 3 GBA-iconen kunnen iets afwijken (eerdere studie: S 0,41–0,44).
- Pootlengte "onderkant − buiklijn" is bij gehurkte knaagdieren (rattata, raticate) maar 1–2 px; die tellen in de pixelregel mee maar zeggen weinig.
