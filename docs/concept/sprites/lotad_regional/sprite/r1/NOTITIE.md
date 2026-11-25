# Gaucho-Lotad, frontsprite ronde 1 (maker, 25 nov)

Model: `r8/gemini_r8_1.png` (onaangeroerd). Kleuren: r1 (Jordi: "we pakken de kleuren van r1"). Ogen: Gen 3-Lotad (Jordi: "de ogen komen uit de bestaande lotad, dat zijn witte cirkels met een zwarte stip erin").

## Bestanden
- `lotad_gaucho.png`: hoofdversie, 64×64, P, index 0 transparant, figuur **43×41** (1148 px), onderste rij 62, **14 kleuren incl. transparant**.
- `lotad_gaucho_klein.png`: kleine variant, figuur **40×38** (980 px), zelfde palet.
- `kaal.png` / `kaal_klein.png`: kale reductie (vóór opschoning en ogen).
- `vel.png`: r1 | klein | kaal | model op dezelfde schaal (8×); kop 12× naast model en Gen 3-Lotad; 1× op wit/crème/groen/donker naast Lotad; r1 naast Lotad op 8×.
- Scripts (uitvoeren in deze map): `natief.py` (raster), `klassen.py` (materiaal per modelpixel), `r1_tinten.py` (r1-kleuren meten), `tonen.py` (toonkaart), `half2t.py` (kale reductie), `bouw.py` (`python3 bouw.py` / `python3 bouw.py lotad_gaucho_klein.png klein`), `schrap.py`, `controle.py`, `kijk.py`, `vel.py`.

## Werkwijze
1. **Natief raster:** pitch 4,264 px (kam 8,525 scoort met fase 8,0 en 3,75 even hoog → echte cel = de helft). Natief 239×130, figuur x75–159, y23–103 (85×81).
2. **Materiaal per modelpixel** (maskers uit `r8/kleur_r1.py`, op het natieve raster): zwart, hoed, kop, snavel, kraag, poten, oog. Bijgesteld: de snavel-schaduwlijn hoort bij de snavel (niet groen), poten = bruin (R ≥ G+7, B < 122), de groene borst-V onder de kin = kop.
3. **Toon per modelpixel:** 4 modeltonen per materiaal gemeten (k-means op helderheid: hoed 72/94/134/164, kop 90/106/134/144, snavel 101/152/188–198, kraag 94/146/176/200, poten 92/102–109/11x/147). Elke modeltoon krijgt de r1-tint van dezelfde rang. De lichtverdeling is dus die van het model, de kleuren komen uit r1. Daarna een 3×3-modusfilter binnen hetzelfde materiaal (alleen meerderheid, geen middeling en geen nieuwe tinten) tegen de Gemini-ruis.
4. **Kale reductie, exact 2×2** (Krassault-methode, fase OY=1 OX=1). Lijn als ≥ 2 van 4 modelpixels lijn zijn, of als er 1 lijnpixel is van een lange modellijn (≥ 6 pixels) die anders breekt of op de rand ligt. Korte streepjes (< 6 px, de haarlijntjes in hoed en kraag) vallen weg. Verder: de meest voorkomende toon van het hoofdmateriaal.
5. **Kleine variant:** 3 kolommen en 3 rijen geschrapt (de minst verschillende, ≥ 6 uit elkaar, niet aan de uiteinden en niet door de ogen): kolommen op 6, 33, 23 en rijen op 35, 13, 29 (figuurcoördinaten). Daarna dezelfde opschoning.

## Pixels die NIET direct uit het model of uit Lotads oog komen (hoofdversie, 185 px verschil met de kale reductie; klein 154)
- **Buitenlijn (39 px):** aan de lichte kant (alleen achtergrond boven/links) een selout in de lijntint van het materiaal (terra-lijn; bruin-donker bij kraag/snavel), ook waar het model zwart heeft; rechts/onder zwart. Zoals de maatstaf-sprites (Skinguin 3 %, Dundragoon 24 % zwart boven/links).
- **Binnenlijnen (102 px), alleen hertint, zelfde plek:** zwart binnen één materiaal (rand- en kroonlijn van de hoed, scheidingen tussen de kraagpunten) → lijntint van dat materiaal. Zwart tussen twee materialen (hoed/kop, mond/kin, kop/kraag) blijft zwart.
- **Ontkorrelen (32 px) + losse tintpixel (1 px):** tintvlekjes < 3 px nemen de meest voorkomende buurtint van dezelfde kleurgroep aan. Geen middeling, alleen bestaande tinten.
- **Ogen (11 px):** Lotad-oog 1-op-1. Nabij oog 3×3 (lichtblauw ×3 / wit-zwart-wit / lichtblauw-wit-lichtblauw) op het midden van het modeloog (30,40); ver oog wit + lichtblauw rechts ervan (19–20,40), zoals Lotad (23–24,41). De overige pixels in de oogvakken van het model hebben de mediane kophelderheid gekregen (= kop-middentoon), zodat het modeloog verdwijnt.
- **Paletkleur terra-midden (188,113,78):** niet uit r1 gemeten. r1's hoed, kop en poten hebben in feite maar twee tinten (156,90,59 en 213,137,101); de midden-tint ligt daar tussen in, omdat het model op hoed en kop 3–4 tonen heeft. Alle andere tinten zijn r1-metingen; lichtblauw (148,180,222), wit en zwart komen uit het Lotad-palet.

## Palet
0 transp · 1 zwart (20,16,18) · terracotta (hoed/kop/poten) 2 lijn (111,59,33), 3 donker (156,90,59), 4 midden* (188,113,78), 5 licht (213,137,101) · 6 bruin-donker (88,68,46) (kraag donker = pootonderkant = snavellijn) · kraag 7 (120,108,77), 8 (161,132,92), 9 hooglicht (223,195,127) · snavel 10 (179,155,90), 11 (228,199,123) · 12 wit · 13 Lotad-lichtblauw. 14 kleuren, 2 vrij (index 14 is gereserveerd voor r1's tweede pootonderkant-tint, maar wordt niet gebruikt).

## Zwakke punten (eerlijk)
1. **Kraag:** het model heeft lichte bladpunten met donkerolijf scheidingslijnen. Na de 2×-reductie blijven die scheidingen maar gedeeltelijk over. Midden en rechts leest de kraag als een gevlekte mix van geel, bruin en zwart in plaats van als enkele duidelijke punten. De onderrand heeft wel zwarte tanden. Ook neemt r1's hooglicht (223,195,127, in r1 maar 4 % van de kraag) hier de grootste lichte toon van het model over, waardoor de kraag geler/strooiiger leest dan de kleurproef.
2. **Ogen:** het lichtblauw van Lotad leest op terracotta als een blauw kadertje om het oog. Het is 1-op-1 overgenomen; het gaat om een kleuroordeel voor Jordi, ik heb geen eigen variant gemaakt.
3. **Onder de snavel** liggen mondlijn en kinlijn op 2× tegen elkaar: een zwarte band van 2 px in plaats van twee lijnen met de kop ertussen.
4. **Binnenste randlijn van de hoed links** is een trapje van losse stukken, geen vloeiende boog zoals in het model.
5. **Donkere band direct onder de hoedrand** op de kop (komt uit het model, de schaduw van de rand), maar die maakt het voorhoofd smal en donker.
6. **Poten:** het model heeft vrijwel geen aparte donkere onderkant (alleen de zwarte buitenlijn). De "donkerbruine onderkant" van r1 komt hier alleen terug waar het model zijn donkerste pootpixels heeft (rechts/onder).
7. **Formaat:** 43×41 (exact 2×) in plaats van 44 breed. Naast Lotad (39×30) is hij duidelijk hoger, door de hoedkroon en de poten van het model.
8. Er is nog geen keurder en geen DC-eindkeuring gedaan (schaduw/volume van de kop en de kraag zijn de kale modeltonen).
