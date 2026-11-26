# Keuring + eindkeuring: gaucho-Ludicolo (25 nov)

Basis: `../sprite/r1/ludicolo_gaucho_0.png` (Jordi: "de eerste" = variant 0, de kale reductie). Model: `../r6/gemini_r6.png`. Familie: `../../af/lotad_gaucho.png`, `../../lombre/af/lombre_gaucho.png`.
Resultaat: `ludicolo_gaucho_e.png` (64×64, P, index 0 transparant, 14 kleuren incl. transparant, slots 14–15 vrij), `ludicolo_gaucho_e_8x.png`, `vergelijk.png` (voor | na | model per spritepixel op 8×; 1× en 2× op licht en donker naast gaucho-Lotad, gaucho-Lombre, Gen 3-Ludicolo (`_gba`), Dundragoon, Skinguin, Zapacha en Princadee).
Oogvarianten (Jordi: "het rechteroog heeft nog niet de perfecte vorm" ... "mag iets ovaler"): `oog_A.png`, `oog_B.png`, vel `oog_vel.png` (e | A | B | modeluitsnede op 20×, plus 2× op licht/donker).
Scripts: `meet.py` (gemiddelde modelkleur/-helderheid per spritepixel: de kale reductie is een vlakstemming, dus per spritepixel de cel van `../sprite/r1/natief.png` die hij bedekt), `e1.py` (alle wijzigingen, per stap geteld → `e1_uitvoer.txt`), `oog.py`, `controle.py` (→ `controle_uitvoer.txt`), `clusters.py`, `uit.py`, `vel.py`.

## Stap 1: keuring (twee eisen)
**(1) Accuraat op het model: ja.** Elke pixel van variant 0 is een modelkleur uit de vlakstemming (0,68×); silhouet, pose, hoed met spitse kroon en olijf band, brede rand, snavel met mondlijn, ogen in het olijf masker, poncho met bladlijnen, olijf vuisten, benen en voeten volgen het model. Gemeten (meet.py): per paletindex ligt de modelhelderheid op de tint (rood diep/donker/mdonker/midden: ML 84/97/113/139; olijf 74/84/118; geel 143/184). Afwijkingen van de kale reductie zijn alleen die van de maker (gezicht 7 px naar het model, buitenlijn, losse pixels).
Gevonden kwantiseerfout: de slagschaduw onder de hoedrand (rechts van het gezicht) en de schouderstrook zijn als **rode lijn** (2) gestemd, als vlak van 2+ px dik (model ML 66–90, 111,51,39 e.d.): de lijntint werkte daar als vulling.
**(2) Gen 3: voldoende, met kanttekeningen.** Op 1× leest hij als een gaucho-Ludicolo: grote hoed, snavel, poncho, vuisten. Maar: veel zwart binnen het rode lijf (18,6 % zwart), vooral de lange zwarte verticale lijn links in de poncho (x19, y40–50) en de bladlijnen eromheen, die van de poncho een mozaïek van losse stukken maakten; dubbele lijnen (2 px) op ±12 plekken (onder de hoedband, onderkant hoedrand rechts, schouder rechts, bladlijnen langs de linkerarm); rode vlaktinten met stappen van maar 16–21 (L 81/97/118/137), dus modderig naast de maatstaven; snavelgeel feller dan de rest van de lijn.

## Stap 2: eindkeuring (127 pixels gewijzigd, alleen indexwissels; niets hertekend, gezicht diff 0)
Gids (`dragonflycave_spriting_guide.txt` r. 80–170, 340–470): "The 'outline shadows' are always black (or ever-so-slightly off-black)"; "the relative luminosity of the shades on the original sprite should always be maintained"; "The outline base and outline highlight colors are also colors. When you're recoloring, you must also recolor the outlines"; "The outlines must be reasonably dark"; "we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide"; "place pixels of the outline highlight color on the inside of the outline rather than the outside".

### Schaduw (64 px)
- **S1 slagschaduw (64 px, 2 → 3):** pixels van de rode lijntint die in een 2×2-blok lijntint liggen én modelhelderheid ≥ 66 hebben, buiten het gezicht: de band onder de hoedrand (x36–50, y25–33) en de schouderstrook (x40–42, y39–40). Nu rood diep (L 74 ≈ model 70–79). De lijntint is daarmee alleen nog lijn; de relatieve helderheid blijft (band 74 < rood donker 97 ernaast). Het deel van die band boven de ogen (x23–27, y24–26) ligt in het bevroren gezichtsvak en is niet aangeraakt.
- Verder volgen de tinten per pixel de modelhelderheid (vlakstemming); niets gladgestreken of gemiddeld.

### Belijning (63 px netto)
- **B1 Jordi's punt: "let op de zwarte lange verticale lijn in de poncho" (40 px, 1 → 2).** Gevonden lange zwarte verticale lijnen binnen het ponchovlak (zwart in het ponchomasker van de maker, alle buren rood en binnen de poncho): **x19, y40–50 (11 px, de lange)**, x14–18 y42–49 (bladlijn langs de linkerarm), x28 y43, x30–32 y41–45 en x35 y46 (bladlijn midden), x39 y38–41 en x40–43 y36–38 (schouderlijn rechts). Een binnenlijn binnen één onderdeel is volgens de gids niet zwart maar de eigen lijntint: allemaal **rode lijn (2), 1 px**. **Zwart blijft waar vorm over vorm valt**: de lijn loopt vanaf y51 als zwart verder waar de poncho over de linkervoet valt (x18–22, y51–55); poncho over rechterbeen (x27–37, y46–54), armgrenzen (x13, x43–44) en de buitenlijn blijven zwart. Niets verschoven, alleen omgekleurd (binnen Jordi's ruimte "alleen het lijnenwerk van de poncho mag afwijken ... anders inkleuren").
- **B2 dubbele lijnen in de poncho → 1 px (12 px, vlaktint volgens de modelhelderheid):** schouder rechts, strook naast de lijn (43,37) (44,37) (42,38) (43,38); 2×2-knoop links (18,42); bladlijn langs de armgrens (14,42) (16,47) (16,49) (17,49); bladlijn midden (32,42) (33,45) (35,46). Telt netto 7 extra, 5 ervan waren al B1-pixels.
- **B3 dubbele lijnen in de hoed → 1 px (17 px):** onder de hoedband lag rij 17 (x29–33) als tweede zwarte rij onder de bandlijn (rij 16), terwijl het model daar randvlak is (ML 95–96, x33 ML 70) → rood donker/diep (5 px); rij 17 x34–42 blijft zwart (enige lijn, ML ≤ 34). Onderkant hoedrand rechts: rij 25 (x40–51) is de buitenlijn, rij 24 (x40–51) lag er als tweede zwarte rij boven → rood diep (12 px), zodat de rand een donkere onderzijde heeft in plaats van een 2 px zwarte balk.
- Getoetst en goed gelaten: buitenlijn rechts/onder zwart (outline shadow), links/boven selout in de lijntint per materiaal (rood 2, olijf 8) zoals Lotad/Lombre; zwarte kreuk in de hoedkroon (x36–37, y5–6) = punt vóór punt, vorm over vorm.
- Zwart-aandeel 18,6 % → 15,7 %.

### Kleurtinten (palet; ≤ 16: nu 14 incl. transparant, slots 14–15 vrij)
| index | rol | was | nu | L was → nu | hue |
|---|---|---|---|---|---|
| 2 | rode lijn | 108,44,30 | ongewijzigd (= Lombre) | 62 | 11 |
| 3 | rood diep | 136,60,42 | 128,54,38 | 81 → 74 | 11 |
| 4 | rood donker | 160,74,50 | ongewijzigd (= Lombre-schaduw) | 97 | 13 |
| 5 | rood mdonker | 186,94,64 | 192,98,66 | 118 → 122 | 15 |
| 6 | rood midden | 204,114,80 | 214,126,88 | 137 → 148 | 18 |
| 7 | rood licht (alleen oogglans, 5 px) | 230,154,112 | ongewijzigd (= Lombre) | 172 | 21 |
| 12 | geel donker | 193,143,41 | **180,150,86** | 146 → 152 | 41 |
| 13 | geel licht | 240,200,73 | **232,204,124** | 197 → 203 | 44 |
Zwart (1) en olijf (8–11, al = Lombre) ongewijzigd.
- **Rood, 5 vlaktinten (meer dan ≤ 3 per kleurgroep):** beslist volgens de gids, regel 1 ("Do not recolor two different shades with the same shade"; relatieve helderheid behouden): niet samengevoegd. Rood licht (7) zit alleen in de oogglans (5 px), dus het lijf heeft 4 vlaktinten; de Gen 3-Ludicolo zelf heeft er ook 4 voor zijn groen (L 127/174/199/236). Wel uit elkaar getrokken: stappen 23/25/26 (was 16/21/19), hue shift oplopend 11 → 18 (schaduw roder, licht geler), donker = Lombre-schaduw. Samenvoegen zou detail weghalen (pixelblur-risico).
- **Geel = lijntinten (Jordi, besluit: "het geel moet zoals de rest van de lijn, afwijken van model"):** genomen: geel donker 12 = (180,150,86) = mond/nagel midden van de gaucho-Lombre (`lombre/af/`, index 12) = snavel midden van de gaucho-Lotad (`af/`, index 10); geel licht 13 = (232,204,124) = mond/nagel licht van de gaucho-Lombre (index 13) = snavel licht van de gaucho-Lotad (index 11). Alleen een paletwissel; de verdeling licht/donker over de pixels blijft. (Lotads extra snaveltint 223,195,127 is niet nodig: de Ludicolo-snavel heeft twee tinten.)

## Rechteroog iets ovaler (oog.py; ter keuze, niet in `ludicolo_gaucho_e.png`)
Rechteroog = rechts op de sprite; pupil (28,25–26) en iris (27,26)/(29,26) blijven, verder niets aan het gezicht. Model: roze ovaal ±3 breed × 4 hoog, pupil links-boven in het ovaal.
- **oog_A (2 px):** ovaal 3 breed rond de pupil (x27–29): (27,27) olijflijn → rood mdonker (tweede irispixel links), (29,28) rood licht → olijf donker (hoek rechtsonder rond; model daar olijfmasker 116,100,65).
- **oog_B (2 px):** ovaal naar rechts (x28–30), pupil links zoals in het model: (30,26) olijf diep → rood mdonker, (30,27) olijf diep → rood midden; hoeken (30,25) en (30,28) blijven masker.
Mijn indruk: B lijkt het meest op het model (pupil links in een breder roze vlak); A is ronder en symmetrischer. Jordi kiest.

## Bevroren zones (controle.py, uitvoer in `controle_uitvoer.txt`)
- Alpha-diff 0 (silhouet).
- Indexdiff 0 in: linkeroog, rechteroog, snavel/mond en het hele gezichtsvak x15–35, y22–34. `e1.py` weigert elke wijziging in het gezichtsvak (assert). De paletwissel van geel en van rood 3/5/6 geldt ook in het gezicht (zelfde indexen, andere tint); zwart en rood licht (oogglans) zijn ongewijzigd.
- Gewijzigd: hoed 20, poncho (masker) 93, romp/armen/benen buiten de poncho 14; totaal 127.

## Ter info voor Jordi (geen wijziging gedaan)
1. **De poncho leest nu als één doek met rode bladlijnen** in plaats van losse zwarte stukken; de bladvorm zelf staat nog precies op de modelplek. Wil je hem nog minder als bladeren, dan is de volgende stap de bladvorm met wat pixels schuiven (jouw eerdere ruimte), als aparte ronde met varianten.
2. **Het lijf heeft geen lichte tint** (rood midden is het lichtst; rood licht zit alleen in de oogglans); het model ook niet. Gen 3 zou een hooglicht linksboven op schouder/hoedkroon geven; dat is tekenwerk buiten het model, niet gedaan.
3. **Ogen** zijn op 1× klein en zwak (pupil 1×2 met rode iris in het olijf masker), zoals het model; leesbaar op 2×. Alleen het rechteroog is als variant aangepakt (zie boven).
4. **Snavel** is met de lijntinten minder fel en contrasteert minder met het rood dan in het model; dat is je besluit, hij past nu bij Lotad en Lombre.
5. Kleine tintvlakjes < 3 px: 154 (was 134); de toename is de rode lijntint van de nieuwe binnenlijnen (diagonale lijnstukjes, geen ruis).
