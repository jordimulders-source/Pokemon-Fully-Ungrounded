# Capykart r17: model overnemen (Dundragoon-methode)

Bestanden: `capykart.png` (64×64, geïndexeerd, index 0 transparant, 16 kleuren incl. transparant) + `capykart_8x.png`; `kaal.png` (kale reductie, 17 tinten vóór paletreductie) en `kaal16.png` (zelfde op het eindpalet); `capykart_tandcreme.png` (+`_8x`): pixels identiek, alleen index 9 = r15b-crème (zie Open); `vel.png` (8×: r17 | kaal | model op dezelfde schaal | Dundragoon | Zapacha | Skinguin | r15b; daaronder dezelfde reeks 1× op wit, crème, donker); `controle.txt`, `zones.txt`.
Scripts (alles vanuit `capykart/` draaien): `natief.py` (raster), `klassen.py` (materiaal per modelpixel), `gemeen.py` (schaal, overlap, palet), `kaal.py` (kale reductie), `bouw.py` (opschonen + bovenlaag + palet), `zones.py` (afwijkingen per zone/stap), `controle.py`, `vel.py`.
Bouwen: `cd docs/concept/sprites/capykart && python3 sprite/r17/bouw.py && python3 sprite/r17/zones.py lijst && python3 sprite/r17/vel.py`.

Opdracht na de laatste woorden van Jordi (24 nov): "probeer maar zoveel mogelijk het model over te nemen, vergeet wat we eerder zeiden"; "het Capybarrel-gezicht, de morrillo, de Bibarel-tanden — deze blijven"; over de toren: "nu zie ik het, de blokken zijn opnieuw getekend" / "en helemaal niet overgenomen vanuit het model". Dus: alles uit de kale reductie van `referenties/model_r5.png` in modeltonen, alleen het gezicht (oog + wenkbrauw, morrillo, tanden) als bovenlaag uit r15b. Geen kleurverschuiving van hout/vacht, niets van de toren uit r13–r16.

## Metingen
- **Rasterpitch: 10,24 px** (1024/100), fase x 9,20 / y 9,20. De kamscore geeft 20,48 net iets hoger, maar dat is een harmonische: op een uitvergroting van het oog zijn de modelpixels ±10 px (oogglans = 1 cel van ±10 px) en het raster op 20,48 verliest de buitenlijn (`natief.py` meet nu tussen 10,20 en 10,28). Natief raster 99×99, figuur x12–84, y11–82 (**73×72**, 3176 px).
- **Schaal 62/73 = 0,849** (1,18 natieve px per spritepixel). Figuur in de sprite **x1–62, y2–62 (62×61), 2295 px**; zelfde maat als r15b (x1–62, y2–61, 2262 px). Niet gespiegeld.

## Kale reductie (`kaal.py`)
Klassen per natieve modelpixel (`klassen.py`, alleen indelen op modelkleur): zwart (L<50), bruin (vacht én hout: in het model één kleurfamilie), hoepel (grijs), en in het torenvak (natief x62–80, y10–48) per tint: groen, blauw, rood (tot rij 40), geel blok (tot rij 29, incl. zijn bruine zijkant en olijfranden), grijs telt nooit als toren.
Per spritepixel oppervlakteweging over het natieve raster: achtergrond als < ½ pixel figuur; **zwart wint vanaf 30 %**; anders de klasse met het grootste oppervlak. Tint:
- **bruin**: drempels op de gemiddelde modelhelderheid binnen de klasse. Modelclusters (k-means op alle bruine modelpixels): L 69/85 (112,53,43)·(137,66,48) | 107 (164,88,56) | 125 (183,107,67) | 146 (214,125,77) | 162 (221,145,95) → grenzen 96/116/136/154 → 5 tinten (lijn, schaduw, midden, licht, hoog). Daarmee komen nerf, plankranden, de schaduw onder de kop, de bolling van de wielen en de lichte bovenkant van de neus van de auto rechtstreeks uit het model.
- **hoepel**: L<110 donker, anders licht.
- **toren**: gemiddelde modelkleur van die klasse in de spritepixel → dichtstbijzijnde modeltoon van dat blok (geel: geel / bruine zijkant / olijfrand; rood: licht / donker / rand; blauw: boven / licht / donker / rand; groen: nok / licht / donker / rand).

## Pixels die afwijken van de kale reductie: 159 px (silhouet-diff 0)
Per zone (`zones.py`, lijst per pixel in `zones.txt`):
- **toren (blokken + dak): 20 px, uitsluitend techniek** — buitenlijn 15 (rechterrand geel-zijkant en rood blok: modelselout → zwart aan de schaduwkant; (44,16) olijfrand → zwart), ontkorrelen 4 ((53,18) rood licht→donker, (45,26) (46,27) (50,27) de 3 px blauw-boven → blauw licht/donker), losse zwarte pixel 1 ((48,18), zwart stipje in het rode blok). **Verder 0 px afwijking: vorm en tinten van alle blokken en het dak zijn de kale reductie van model_r5.**
- **kop: 56 px** — ontkorrelen 33, buitenlijn 5, morrillo 6, oog + wenkbrauw 11, modeloog weg 1.
- **kin/tanden: 26 px** — tanden 20, ontkorrelen 6.
- **auto + hoepels + wielen + nek: 57 px** — ontkorrelen 56, buitenlijn 1.

Per stap (`bouw.py`):
1. **buitenlijn (23 px):** geen open of lichte rand; schaduwkant (achtergrond rechts/onder) zwart, lichtkant eigen donkerste tint (bruin-lijn, hoepel-donker, rood-donker, blauw-donker, groen-donker). Zwart uit het model blijft zwart.
2. **ontkorrelen (103 px):** tintvlekjes < 3 px (bruin-hoog, hoepel-licht, geel, blauw-boven < 2) nemen de meest voorkomende buurtint uit dezelfde groep aan; lijntinten (bruin-lijn, hoepel-donker) zijn nooit het doel en worden zelf niet ontkorreld.
3. **losse zwarte pixels (4 px)** → buurtint; daarna **3b: neusgat (20,23) en mondpixels (18,29), (20,30) terug naar het model (3 px)** — stap 3 haalde ze weg, het model heeft ze (het linker neusgat valt samen met de buitenlijn).
4. **gezicht, bovenlaag uit r15b, pixel voor pixel** (r15b-index → rol in dit palet: 1 zwart → zwart, 4 donkerste vacht → bruin-lijn, 8 blauwgrijs → hoepel-donker, 9 crème → geel):
   - modeloog (3×3 zwart) eerst terug naar de vachttint eromheen (9 px gezet, 1 blijft anders dan kaal: (30,21) → bruin-licht);
   - **blije Capybarrel-oog + wenkbrauw**: r15b x28–31, y16–20 (zwart + donkerste vacht) op het modeloog, verschuiving (+1,+1) (11 px anders dan kaal);
   - **morrillo**: r15b (22–24,15), (21–23,16) op de snuitrug van het model, (0,+1), net binnen de buitenlijn zoals in r15b (6 px);
   - **Bibarel-tanden**: r15b x18–23, y30–33 (zwart kader, crème, grijs) onder de bovenlip van het model, (0,+2) (20 px). De verschuivingen volgen uit het verschil tussen r15b en het model: kop 1 rij lager, snuitpunt gelijk, oog 1 px verder naar rechts, snuitonderkant 2 rijen lager.
5. **palet naar 16:** blauw-boven bleef na het ontkorrelen 0 px over (het model toont maar een reepje bovenkant van het blauwe blok: 3 px op deze maat) en valt weg.
Geen andere pixels die niet uit het model of de r15b-bovenlaag komen.

## Palet (index: kleur)
0 transparant (152,208,160) · 1 zwart (24,17,28) · bruin 2 lijn (112,53,43) 3 schaduw (164,88,56) 4 midden (183,107,67) 5 licht (214,125,77) 6 hoog (221,145,95) · hoepel 7 licht (142,142,146) 8 donker (76,74,84) · 9 geel (240,208,84) · rood 10 licht (246,99,90) 11 donker (205,61,65) · blauw 12 licht (87,140,202) 13 donker (76,109,168) · groen 14 licht (92,163,92) 15 donker (74,135,83).
Alle tinten = gemeten modeltonen (clustercentra / gemeten blokkleuren). Gedeeld: de bruine zijkant van het gele blok = bruin-licht en de olijfrand = bruin-lijn (het model kleurt die zijkant houtbruin); tanden = geel; morrillo = hoepel-donker. Palet vol (16).

## Controle (`controle.txt`)
64×64, mode P, transparency 0, 16 kleuren incl. transparant; geen lichte kleur op de buitenrand; zwart 21,2 % van de figuur. Losse zwarte pixels: alleen neusgat (20,23) en mond (18,29), (20,30), uit het model. Overgebleven tintvlekjes < 3 px: bruin-lijn en hoepel-donker zijn lijnen (nerf, plankranden, hoepelrand); verder (29,17), (29,18), (30,21) tussen wenkbrauw en oog (naad van de bovenlaag) en enkele 1-px vlekjes die alleen aan lijntinten grenzen ((51,35), (33,36), (34,51), (8,57), (16,35), (17,34), (47,19)); die staan op modelplekken.

## Eigen blik (8× en 1× naast Dundragoon, Zapacha, Skinguin, r15b)
- Leest als het model: kop, plankauto, wielen met hun kruis/vierkant, hoepels en toren zitten op de modelplekken; schaduw, nerf en bolling komen uit de modelhelderheid, niet uit rechte banden. Blokken: rood licht links / donker rechts, blauw licht / donker, geel met bruine zijkant, dak licht / donker; een echte lichte bovenkant heeft alleen het blauwe blok in het model (3 px), die viel weg.
- **Zwakke punten, eerlijk:**
  1. **Tanden in het blokgeel** (240,208,84): palet vol, dus de crème van r15b kon er niet bij. Ze lezen op 1× als een geel vlekje onder de kin. Variant `capykart_tandcreme.png` (alleen palet: index 9 = (252,232,150), ook het gele blok wordt dan crème zoals in r15b). Keuze voor Jordi; niet zelf besloten.
  2. **Vacht en hout lopen op 1× in elkaar over**: dat is het model (één bruinfamilie); Jordi liet de kleurverschuiving vallen. Naast Zapacha/Dundragoon oogt de sprite daardoor eentoniger bruin.
  3. **Wenkbrauw van r15b** maakt links van het oog een donker verticaal streepje (r15b x28, y18–20); 1-op-1 overgenomen, niet aangepast.
  4. Morrillo als donkergrijze vlek op de snuitrug en de tanden over de bovenrand van de auto: zoals in r15b, op de modelplek.
  5. Onder het dak zitten 2 rijen zwart boven de bruine zijkant van het gele blok: dat is de schaduw onder het dak in het model.
