# Krassault – kleurfase r1 (LOG)

Uitgangspunt `basis.png`; model `../nat_A.png` (spritepixel (x,y) = modelblok vanaf (24+2x, 21+2y); gecontroleerd: silhouetverschil 0 alleen bij die offset). Silhouet niet aangeraakt. Reproduceren: `python3 maak_r1.py` (raster als data, stopt als het silhouet afwijkt), vel: `python3 maak_vel_r1.py`.

**Vondst:** de vulkleuren van `basis.png` wijken op plekken af van het model (het ontkorrelen heeft o.a. de rand van het rechterkanon en de onderlip van de mond weggeveegd). Voor de vlakken is daarom het model zelf gemeten (per spritepixel het 2×2-blok), niet basis.png.

## Palet (GBA-waarden, veelvouden van 8)
| idx | rol | RGB | helderheid |
|---|---|---|---|
| 1 | omlijning | 24,8,16 | 14 |
| 2 | lijnrood | 72,16,32 | 35 |
| 3 | diepe schaduw (onderkant, onder het lijf) | 96,24,40 | 47 |
| 4 | schaduw | 120,32,48 | 60 |
| 5 | basis | 160,48,64 | 83 |
| 6 | licht | 200,96,104 | 128 |
| 7 | hooglicht (alleen glans) | 232,144,144 | 170 |
| 10 | geel donker | 176,120,40 | 128 |
| 11 | geel midden | 232,192,96 | 193 |
| 12 | geel licht | 248,232,160 | 228 |

10 kleuren + transparant. Model gemeten: schaduw (108,35,48) h58, basis (149,50,65) h81, licht (176,95,104) h120; kleurfamilie gehouden (karmijn), stappen iets vergroot (60 → 83 → 128 → 170). Verdeling: B 578, S 527, K 461, L 260, H 184, D 77, W 9, geel 136.

## Per zone
- **Mantel/vin:** lichte strook linksboven per segment (H), basis, schaduw als strook rechts langs de as (S); segmentringen en kraag in lijnrood; rechtervin vlak B met S tegen de as. Vouwlijn van de linkervin doorgetrokken (model).
- **Kopkoepel:** één lichtvlek linksboven (H, rijen 24–29) met glans (W, 3 px); schaduw rechts achter het kanon en onder het rechteroog; wenkbrauwbulten H boven beide ogen. Ogen: pixels van basis.png behouden (geel, pupil, lid); alleen het bovenlid rechts gesloten.
- **Rechterkanon (ver):** rand weer een ring: boven/links/rechts H, onder B, binnenwand S, opening zwart. Geen W (verder weg).
- **Linkerkanon (dichtbij):** rand H met glans W linksboven en op de belichte binnenwand; opening zwart; arm: lichte bovenkant, S-baan in de slagschaduw van het kanon, B rechts.
- **Mond:** lip als gesloten ring (boven H met W, rechts H, links H→B, onder B), opening zwart met twee schaduwstrepen (S) zoals het model, drie ribbels rechts ervan gescheiden door lijnrood/zwart; dal van 1 px (B) tussen lip en eerste ribbel.
- **Tentakels:** lichte bovenkant/linkerrand, S aan de onder-/achterkant; verre tentakels (achter de kop, onder het kanon) grotendeels S.
- **Onder het lijf:** het grote blok dat in basis.png lijnrood was (rijen 46–51, x 24–33) is in het model een donkere schaduw, geen lijn: nu vultint D. Onderkant van de rollen (rijen 57–60) ook D.
- **Rupsbanden:** kopvlak B met S onderaan, bovenband van de rechterrol B met H-streep, lijf S; spiraallijnen zwart (op S is lijnrood te vaag: Jordi's "lijnen te weinig gedefinieerd"), scheidingslijn kopvlak/lijf lijnrood. Rechterrol kreeg een zwarte linkerrand zodat de twee rollen los lezen.
- **Omlijning:** elke silhouetrand is nu omlijning (128 randpixels waren vulkleur, vaak de lichtste tint): boven/links lijnrood, onder/rechts zwart. Uitzondering: wratten op de rand houden geel (donker geel aan de schaduwkant).

## Wratten en zuignappen
- **Wratten (tentakels):** één recept: licht (c) linksboven, midden (b), donker (a) rechtsonder/tegen de contour. Plek ongewijzigd; alleen (56,40) erbij (wrat was in het model 2 breed).
- **Zuignappen (kopvlakken van de rollen):** de rommelige vlekjes zijn nette ringetjes van 4 px (ruit: c boven, b links/rechts, a onder) met donker midden (lijnrood), op de plekken van het model: links (14,51) en (14,56); rechts (33,53) en (33,57). Half zichtbare ringen tegen de linkerrand als staafje van 2 px: links (11,52–53) en (11,55–56), rechts (30,56–57). Rechterrol boven: de gele boog langs de rand zoals het model, (30,52)–(31,51)–(32..35,50). Onderaan elk één liggend streepje: (17–18,60) en (36–37,61).
- Geel erbij: (56,40) (14,50) (33,50) (13,51) (15,51) (11,52) (11,53) (33,54) (11,56) (13,56) (14,57) (30,57) (17,60) (36,61). Geel weg: (15,50) (12,51) (14,51) (15,52) (34,52) (14,53) (12,55) (12,56) (14,56) (15,57) (16,57) (31,57) (15,58) (34,58) (17,59) (19,60) (35,60).

## Lijnpixels (t.o.v. basis.png)
**Erbij op de silhouetrand: 128** (vulkleur → omlijning, zie boven).
**Erbij binnen: 41**, elk met het model als bron:
- vouwlijn linkervin (45,7) (44,8) (43,9) (41,11); kraag (40,12) (39,13); ring 1 (39,16); ring 2, gat gedicht (38,24) (39,25) (40,26)
- wenkbrauw rechts (36,30) (37,30) (35,31); bovenlid rechts (38,33) (40,33) – (38,33) ligt een halve pixel hoger dan in het model om het lid te sluiten; neuslijn (26,36); rand linkerwenkbrauw (22,31) (22,32)
- linkerkanon binnenring (5,27) (ruil met (4,27), zie weg); rechterkanon opening (50,27)
- mond: (25,39) (31,39) ribbel-/liplijn boven; (24,42) opening; (29,42) (31,42) ribbellijnen doorgetrokken; (23,45) (21,46) (25,46) opening; (24,49) onderrand
- (4,46) vouw linkertentakel; (55,43) bovenrand tentakel; (38,48) (44,49) (47,49) bovenlijn rechterrol aaneengesloten; (29,52) linkerrand rechterrol; (35,58) scheidingslijn kopvlak doorgetrokken; (19,60) onderrand
- midden van de zuignapringen (14,51) (14,56) (33,53) (33,57)
**Zwak bewijs (1 van 4 modelpixels donker, gezet voor een doorlopende lijn):** (31,39) (38,48) (44,49) (29,52) (35,58) (4,46).
**Weg: 38:**
- 31 px schaduwblok onder het lijf (rijen 46–51, x 24–33): was lijnrood als vlak, nu vultint D
- (4,27): binnenring linkerkanon 1 px naar binnen (naar (5,27)), anders lag hij dubbel tegen de omlijning
- (21,43) (22,43) (20,46): mondopening, nu schaduwstreep/lip zoals het model
- (23,48): onderlip (model: half lip), (33,49): schaduw, (41,49): los zwart puntje in de lichte bovenband
**Omgekleurd 1↔2: 48** (ringen/plooien naar lijnrood, onder- en rechterranden naar zwart).

## Controle
- Clusters < 3 px (4-buren): 25 over, allemaal bewust: glans (W), de ribbels en lipring van de mond (1 px breed), lichtstreepjes op tentakels van 2 px breed, restjes tussen spiraallijnen.
- Geen vulkleur op de silhouetrand behalve gele wratten.

## bewaak.py
```
silhouet-diff: 0
geel-diff (plek): 31 (mag binnen mond/zuignappen, verantwoord in LOG.md)
lijnpixels weg: 38 erbij: 169 (binnenlijnen mogen scherper; elk blok verantwoord in LOG.md met het model als bron)
omgekleurd 1<->2: 48 | vulpixels gewijzigd: 692 | kleuren: 10
OK
```

## Zwakke punten (eerlijk)
1. **Donkerder en minder licht dan echte Gen 3-sprites** (zie onderste rij van het vel): de basis ligt bewust bij het model (h83); Octillery/Scizor hebben veel meer lichte tint. Alleen via het palet op te lossen (B/H lichter) als Jordi dat wil.
2. **Mond:** leest als ring met opening, maar de drie ribbels zijn elk 1 px en lezen op 1× niet als ribbels.
3. **Rupsbanden:** spiraallijnen zijn druk; de lijnposities zijn die van basis.png, niet opgeschoond.
4. **Linksonder (x 7–13, rij 38–48):** kleine tentakels blijven een drukke plek; kleur kan dat niet oplossen.
5. Ogen zijn niet van een echte sprite overgenomen (pixels van basis.png behouden).
