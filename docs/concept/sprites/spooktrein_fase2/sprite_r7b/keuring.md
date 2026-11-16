# Keuring spooktrein fase 2, sprite_r7b (16 nov)

**Oordeel: PASS** (met drie kleine opschoonpunten; geen nieuwe keurronde nodig, een pixeldiff-controle is genoeg).

Hoofdvraag: ja. Op 1× en 3× leest hij naast haunter, banette, shuppet en magneton als een nette Gen 3-sprite van het model. Pose, juichende vuist, wagen met staanders en scheuren, de twee wielen, de donkere onderkant en de wolk kloppen met `sprite_r2/model_geschaald.png`. Gemeten: het donkere blok links van het spookwiel (x13–20, y52–55, index 5 = 103) volgt het model (100–135), en de onderkant van de wagen (y44–49) ook. Buitenlijn gesloten (geen vulpixel grenst aan transparant). Licht linksboven, selout (5) links en boven, zwart rechts en onder.
Niet beoordeeld: het gezicht (x25–41, y9–26), de weggegumde onderdelen, de staart en de vorm van het spookwiel (de uitvoering is netjes: ring 1 px in 5, vlak egaal 4, naaf 3).

Helderheid per index: 2=217, 6=203, 3=174, 11=162, 4=142, 7=137, 12=123, 5=103, 8=95, 13=74, 9=48, 1=33. Groen 217/174/142/103: stappen 43/32/39. IJzer 162/123/74: 39/49.

## Opschoonpunten (op 1× nauwelijks zichtbaar, daarom geen FAIL)
1. **Punt van de wolkstaart (x55–63, y49–57): selout en zwart om en om** langs één rand: (55–58,50)=5, (59,50)=1, (58,51)=1, (59–60,52)=5, (61–63,53)=1, (60,54)=1, (60–63,55)=5, (63,56)=1. Daarbij is (61–63,53) een zwart lijntje van 1 px zonder vulling erachter en zit er een inham op (61–63,54), terwijl het model hier één dichte punt heeft (rij 53–57 gevuld tot x62–63). Eis: één doorlopende rand, eerst 5 bovenop en dan 1 vanaf de punt. Neem de punt over uit het model: (61–62,54) wordt vulling, en de lijn loopt alleen om de dichte punt.
2. **Onderrand links van de wolk (x14–18, y55–57):** een zigzag van 1 px. (16,57) en (18,57) hangen als losse zwarte tandjes onder de rand, met (17,57) transparant ertussen. (14,55)=5 staat alleen tussen zwart. Eis: een vloeiende onderlijn in 1, zonder trapjes en niet om en om.
3. **Lichte rij onder het onderstel (x23–27, y46):** de rij is 3,3,6,6,3. Dat geeft snippers van 1 tot 2 px in twee lichte tinten. Eis: geen vlakjes < 3 px. Maak de rij één tint, zoals het model (licht groen, ±170, dus 3).

## Punten uit r6c
1. Zebra in het spookwiel: **opgelost** (vlak egaal 4).
2. Donkere tinten in de flank, 13 tegen 9: **verbeterd** van 13 naar 26. Dat is net onder ±30 en op 1× niet storend, dus acceptabel. Ter info: 8 tegen 13 scheelt 21, maar het verschil in tint (bruin tegen grijs ijzer) houdt de staanders leesbaar.
3. Roest tegen plankbruin: **vervallen**, want ze zijn bewust samengevoegd (8). Index 10 wordt niet meer gebruikt.
4. Snippers: **grotendeels opgelost**. Wat overblijft zijn scheur- en glanspixels (lime 6, 1–2 px) en (35–36,44)=4. Die laatste is op 1× onzichtbaar.
