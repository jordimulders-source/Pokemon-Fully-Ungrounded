# Keuring viscacha kleur ronde 3 (onafhankelijke keurder, 7 nov)
- Bron: docs/concept/sprites/viscacha/referenties/gemini_gekozen_ronde6.png (en verkleind kleur_r3/gemini64.png); vergeleken met graphics/pokemon/{pachirisu,emolga,dedenne,sandshrew}/anim_front.png (bovenste 64×64), kleur_r2/viscacha.png, kleur_r2/vel.png.keuring.md, kleur_r3/NOTITIES.md, raster.txt en controle_uitvoer.txt.
- Bekeken: kleur_r3/viscacha.png op 8× (nearest), 1× op wit, lichtgroen, donker (40) en zwart; kop+lijf 10× met raster per 5 px naast gemini64.png; rij voor rij in raster.txt.

## Blind (vóór SPEC/bron/notities)
- Op 1×: een zandkleurig springknaagdier naar links, voorpoten op, achterpoten gebogen, lange omhoogkrullende staart met gele gekartelde pluim. Leest als officiële Pokémon-sprite in de Pachirisu/Dedenne-hoek; Electric door het geel.
- De gele pluk zie ik nu als een kleine gele punt/sikkel achter de wang die boven de nek uitsteekt, niet meer als band rond de hals. Hij zit wel laag bij de kop-nekovergang, dus heel even "kraagje"-twijfel, maar geen riem.
- Op 8×: netjes, licht linksboven, rugboog vloeiend, schaduw als sikkel om de bil. Grote lichte vlakte op de romp zonder vormgeving; crème vlek op de buik als koepel. Oren smal en vrij puntig. Ondergrens staartaanzet en de achterpoot zijn nog recht.

## Per onderdeel (na SPEC en bron)
- **Pose / massa**: lijkt op Gemini (gespannen, voorpoten op, achterpoten gebogen, staart krult omhoog) / wijkt af in: niets wezenlijks. Hoofdvraag: PASS.
- **Kop**: lijkt op Gemini (profiel, ronde wang, crème borst eronder, eigen kopcontour nu via de tapse lijn 2/3 achter de wang) / wijkt af in: de gele pluk op de snuitpunt uit Gemini (±(1–3,26–28) in gemini64) ontbreekt en wordt niet gemeld in NOTITIES (alleen de snorharen). Zie "voor Jordi". Kopbovenkant tussen de oren is een vlak stukje (rij 20 x10–14, rij 21 x6–9); in Gemini ook vrij vlak, geen reparatie.
- **Oog**: Emolga-oog, leest als Pokémon-oog. Gemini heeft een smaller, vastberaden amandeloog met wenkbrauw; ronde Emolga-vorm is cuter en techniek-correct. OK.
- **Wangpluk**: lijkt op Gemini (sikkel "(" op de wang, punt naar achter-boven die buiten de kopcontour uitsteekt, met een inkeping tussen punt (20–24,26–27) en rugaanzet (28,27)) / wijkt af in: kleiner en hoger dan Gemini (gemeld, bewust). Licht A links, 9 rechts, 8 als selout: klopt met linksboven. **Kraagvraag: opgelost**; geen parallelle strepen meer, taps, de voet ligt op de wang. Coördinator-observatie bevestigd.
- **Oren**: lijken op Gemini qua plaats en de donkere binnenschelp van het nabije oor (nu gedaan) / wijken af in: smaller en spitser dan Gemini; het nabije oor in gemini64 is ±8 px breed met ronde top (x15–23, rij 12–20), de sprite 6 px met punt (x16–22, top 2 px op rij 12). Silhouetzaak, zie "voor Jordi".
- **Lijf / rug**: lijkt op Gemini (overwegend licht zand 5, oker/terracotta rechts en onder) / wijkt af in: niets wezenlijks. Rugboog loopt nu 4–6–4–3–2–1–1, vloeiend (r2-punt 2 opgelost). Het 5-vlak is groot (±208 px in x22–41, rij 27–41) en zonder vormgeving; coördinator-observatie half bevestigd: het oogt vlak op 8×, maar op 1× maakt de bilsikkel de romp rond, en Gemini is daar ook vlak. Geen techniekfout (geen banding, geen pillow shading), hooguit verfijning.
- **Schaduw**: sikkel om de bil, dun boven (42,31), breed onder/achter; dijlijn-naad weg. r2-punt 3 opgelost.
- **Buik / crème**: koepel met boogvormige bovenrand (rij 41–44), donkere crème 6 als sikkel eronder; leest als de lichte vlek van Gemini. r2-punt 4 opgelost.
- **Snuit/mond**: losse stip weg, mondlijn aansluitend, neus op de punt. r2-punt 5 opgelost op de kinlijn na (gemeld).
- **Voorpoten**: verre poot opgeheven, nabije met pols; omlijnd. OK.
- **Achterpoten**: perspectief klopt / wijkt af in: r2-punt 6 niet gedaan (gemeld): onderrand verre voet rij 58 x22–29 recht (8 px), scheen nabije achterpoot rij 55–58 x45–49 vier identieke rijen `24331` (rechte buis).
- **Staart + pluim**: één geheel, pluim gekarteld en leest op 1× als één ding / wijkt af in: onderrand van de staartaanzet rij 48 x47–54 is een rechte lijn van 8 px `11111111`; in Gemini een boog.
- **Belijning**: 1 px; 2 aan de lichtkant, 1 aan de schaduwkant, één overgang rechts (rij 32→33 bij x44), geen om-en-om. OK.
- **Netheid/contrast**: controle.py klopt: 0 open randen, 0 losse pixels, kleine clusters alleen oog en pluimkern; 16 kleuren; per kleurgroep 3 tinten + lijn.

## Reparaties (klein, techniek; geen nieuwe ontwerpronde nodig)
1. Staartaanzet onderrand (47–54,48): recht stuk breken tot een flauwe boog, bv. (47–49,48) houden en (50–54) één rij hoger laten aansluiten op (54–56,47), zodat de lengtes 3–3–2 aflopen.
2. Verre achtervoet (22–29,58): hiel en teen 1 px ronden (bv. (22,58) en (29,58) transparant, contour 1 rij hoger).
3. Scheen nabije achterpoot (45–49,55–58): één rij met 1 px verspringing of de 3-strook taps laten eindigen, zodat het geen buis met drie evenwijdige strepen is.
4. Optioneel: in het 5-vlak één zachte schouderlijn/overgang 4 (bv. een korte sikkel ±(22–25,33–38) achter de voorpoot), zodat de romp ook op 8× rond leest. Massa niet veranderen.

## Voor Jordi (geen FAIL-reden)
- Gele pluk op de snuitpunt uit Gemini is weggelaten (niet gemeld). Op 64 px zijn dat 2–3 gele pixels op de neus, die snel als vonk lezen ("ik wil geen elektriciteit zien"). Erbij of niet?
- Oren smaller en spitser dan het Gemini-plaatje (dat heeft een grote ronde schelp); wil Jordi ze ronder, dan is dat een silhouetwijziging.
- Wangpluk bewust kleiner dan bij Gemini (tegen het kraageffect).
- Kop klein t.o.v. het lijf en sprite 62 px breed, groter dan Pachirisu/Dedenne; zelfde verhouding als Gemini.

Oordeel: PASS
