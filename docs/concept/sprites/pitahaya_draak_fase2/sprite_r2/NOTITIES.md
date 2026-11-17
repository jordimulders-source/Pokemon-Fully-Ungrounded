# Pitahaya-draak fase 2, sprite r2 (maker), op r1

Alleen de vier benoemde reparaties, alles uit het model (`natief.png` + `groepen.py` van r1). Script: `maak_r2.py` (aanroep `python3 maak_r2.py`), wijzigingen per pixel in `pitahaya2_r2_afwijkingen.txt`.
**Bewijs:** het script assert dat elke pixel die verschilt van r1 in een van de vier zones ligt (buiten zones: **0**) en dat het silhouet gelijk is (**0**). Maat 58×33, palet ongewijzigd (12 kleuren + transparant). Zwart binnen de figuur **6,5 %** (r1 8,6 %).

## Wijzigingen t.o.v. r1: 52 px (zone: aantal)
| Zone | px |
|---|---|
| 1 bek (X 5–19, Y 43–56, binnenpixels, geen groen) | 19 (8 vlees, 13 roze/lijn, 7 pit-pixels; deels dezelfde pixels) |
| 2 kaaklijn + tanden | 4 |
| 3 naden roze lijf | 20 |
| 4 kop-roze | 9 |
Poten, staart (incl. gat), groene schubpunten, oog, silhouet: 0.

## 1 Bek
- **Gemeten in het model** (natief, 3×3 per spritepixel): de binnenkant is grijs (vlees, lum 190–198, rijen 88–105) bovenin en wit (231–236, rijen 106–121) onderin; ertussen loopt links een dunne roze strook (de verre lip), rondom een lipband van 2 spritepx (buiten donker (113,43,55), dan (177,40,84), binnen lichtroze (244,148,167)). De grijze bovenkant is dus echt de modeltint (191,189,192), geen lichtgrijs; die heb ik niet veranderd.
- **Regel:** vlees bij ≥ 4 van 9 wit/pit-px (toon: gem. wit ≥ 215 → licht, anders grijs), lijn bij ≥ 3 zwart, anders roze (blokgemiddelde → dichtstbijzijnde roze toon). Daardoor: (12,43) lijn → grijs vlees (palatum sluit aan op de bovenlijn), (13,43)/(9,44)/(14,44) lijn → roze, lipband binnenrand lichter: (8,50) → lichtroze, (9,48)/(9,54) → roze. Pixels waar r1 een pit had en het model geen pit-zwaartepunt, worden weer vlees.
- Geprobeerd en verworpen: vlees alleen bij meerderheid t.o.v. roze. Dat maakt de dunne roze strook van het model 1 px breed diagonaal door de ovaal en splitst die in twee (leest slechter dan het model, waar de strook dun is).
- **Pitjes (7)**, uit de modelposities: elke pitcomponent van het model (30) → spritepixel van zijn zwaartepunt; grootste eerst; alleen op vlees, hooguit 1 niet-vlees-buur, nooit 8-naast elkaar, en geen twee op dezelfde rij of kolom op 2 px (dat gaf het dobbelsteenpaar (51,9)/(51,11) in r1). Posities: gehemelte (44,11) (46,13) (47,11) (47,15); wit (49,14) (50,12) (51,9). Kleur: model-pitten hebben mediaan lum 42 (helft zwart 13–20, helft grijs ±100–130 door anti-aliasing): de pittint (44,42,46) is die mediaan, ongewijzigd.

## 2 Kaaklijn
- Rij 42 X 3–9 doorlopend zwart: (4,42) roze → zwart, (5,42) wit → zwart (de r1-tand), (8,42) roze → zwart. **Let op, niet uit het model:** in het model zijn (4,42) en (8,42) het roze tandvlees boven elke tand (1 resp. 0 zwarte modelpx); zwart gezet op jouw opdracht "doorlopende lijn".
- Tanden 1 px wit op de modeltanden: (4,43) zwart → wit (model: 3 witte px, hoektand x 16–18) en (8,43) (al wit in r1, 8 witte px). (9,43) blijft zwart zodat de achterste tand niet in het grijze gehemelte opgaat. Geen ander wit in de rand.

## 3 Naden in het roze lijf
- **Gemeten:** de modelnaden zijn echt zwart (lum 11–40), maar 1 natieve px breed naast ±6 roze px per blok; het blokgemiddelde ligt het dichtst bij de donkerste roze (113,43,55). Regel: binnenzwart in een blok zonder groen en met ≥ 4 roze px, X ≥ 19, buiten de bek → (113,43,55). 20 px.
- Zwart blijft waar een blok groen heeft (poot over lijf, randen van de groene punten) en aan de buitenlijn.

## 4 Kop-roze
- Binnenvulling roze van de kop (X ≤ 24, Y ≤ 42, buiten het oog, geen blok met ≥ 3 zwarte px) opnieuw uit de modelluminantie per blok (σ 0,8), drempels uit de modelverdeling van dezelfde kopzone: 29 % (177,40,84) / 56 % (231,78,123) / 15 % lichtroze (244,148,167). 9 px: lichtroze op de snuitbult (5,40) (6,38) (7,38) (8,37) en (16,36), donkerder op (10,37) (11,42) (14,35), (11,39) lichter.

## Zelf vergeleken (vel.png)
- Bek: één wit/grijs vlak met pitjes binnen een roze lipband; kaaklijn doorlopend met 2 witte tandjes; rug minder zwaar, schubvlakken lezen als vrucht; kop iets meer licht op de snuit.
- **Zwakke punten:** (a) het grijze gehemelte blijft een duidelijk grijs vlak boven het witte, omdat het model daar echt grijs (191) is; lichter maken zou van het model afwijken (vraag aan Claude/Jordi als dat gewenst is: alleen een paletwaarde). (b) Onder de kaaklijn is het silhouet tussen de tanden transparant ((2–3,43), (6,43)); op een lichte achtergrond leest de tandenrij daardoor nog wat stippelig. Silhouet is bevroren, dus niet aangepast. (c) 7 pitjes tegenover ±28 in het model; meer kan niet zonder dat ze elkaar raken. (d) Tanden zijn 1 px; in het model zijn het duidelijke hoektanden.
