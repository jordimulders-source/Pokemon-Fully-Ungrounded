# Sneeuwmonster fase 2: keuring + eindkeuring (26 nov)

Bron: `../sprite_r4/sneeuwmonster2_r4.png`. Model (bevroren): `../model.png` (r1a + stenen r3a). Vergeleken op 8× en 1× naast het verkleinde model, fase 1 (`../../sneeuwmonster/af/`), de maatstaf (Skinguin, Dundragoon, Zapacha, Princadee) en Gen 3 `_gba`: Glalie, Snorunt, Absol, Seel (palet gemeten).
Bevroren (index-diff 0, assert in `bouw.py`): silhouet, beide ogen, de mond.

## Deel 1: keuring (twee eisen)
**Oordeel r4: BIJNA** (één punt, in deel 2 opgelost; daarna PASS).
- Accuraat op het model: silhouet, emmer ondersteboven met één band (licht schuin, zoals het model), donkere rechterhelft van de emmer, dichte ogen in grijze kassen, golvend mondje, baardfranje, de korte armen met de hand rechts over het lijf, de voeten en beide stenen op de modelplekken: niets toegevoegd of weggelaten.
- Gemeten (vlakpixels tegen de mediaan van het modelblok): wit lijf w L247 ↔ model 245, schaduw s 149 ↔ 150, donker hout 90 ↔ 91, licht hout 155 ↔ 146. Klopt.
- **Punt: de stenen lezen op 1× oranje-geel, in het model donker met een gloeiende rand/scheuren.** Gemeten: gloed 41 van 87 steenpixels in de sprite tegenover 28 % gloed in het model; vooral het geel (11 px, model 245,191,81 maar dun) en het felle oranje maken het licht. De plekken kloppen (randgloed rechts/onder, scheuren), het is de tint en de verdeling over r/o/y. Zie S1/K3.
- Gen 3: buitenlijn 1 px, gekleurde selout aan de lichtkant, zwart aan de schaduwkant, geen lichte kleur op de rand, geen zwart/lijntint om en om. Restpunten van belijning: zie deel 2.

## Deel 2: eindkeuring vooraf (r4)
**Kleurtinten.** Sneeuwramp w 247 / h 222 / m 186 / s 149 / l 100 / K 32. Gen 3 witte soorten (`_gba`): Glalie outline base 52526a L84, Seel 415283 L82, Absol 5a5a83 L94; fase 1 (eindkeuring) l L90. De lijntint is met L100 te licht (DC regel 4: "The outlines must be reasonably dark") en anders dan fase 1. De ramp draait naar de lichte kant groen (hue 206 → 190 bij w); fase 1 is overal ±210. Hout 155/115/90 met 7 als vulling én omlijning: past bij het model (gemeten), zie twijfels. Gloed te fel (zie deel 1).
**Belijning.**
- Dubbele rand (lijntint direct binnen de zwarte buitenlijn): kop rechts (48,22), elleboog rechts (54,37)(54,38), linkervoet onder (18–21,55) (rij l boven rij K), linkerarm onder (10,43).
- Zwart binnen de figuur (binnenlijnen horen niet zwart): handrand (41,46)(42,47)(50,47)(51,46), tussen de voeten (28,53) (K op K).
- Klontjes: zwarte hoek rechtsonder (51,50) (lijn 2 px), lijnklontje 2×2 bij de hand rechts (51,44).
- Geen outline highlights op de belichte kant.
**Schaduw.** Volgt het model: licht links/boven, de sikkel onderaan het lijf en rechts, nekschaduw van de baard; grenzen gebogen, geen pillow shading. Niets gladgestreken (regel "rustiger = pixelblur"); de losse s-pixels in de vacht zijn taps uitlopende modelstrengen.

## Uitgevoerd (`bouw.py`, 38 px index-diff + 8 paletkleuren)
| stap | px | wat |
|---|---|---|
| K1 palet | – | l (72,108,136) L100 → (62,96,140) L90 = lijntint fase 1 (outline base + binnenlijnen + mond) |
| K2 palet | – | sneeuwramp naar de tint van fase 1, helderheid gelijk: s (118,158,186) → (120,156,190); m (160,194,214) → (162,191,222); h (204,228,240) → (208,226,244) = fase 1 m; w (240,250,252) → (244,250,255) = fase 1 w |
| K3 palet | – | gloed minder fel, naar de modelgloed: o (240,136,40) → (232,124,44); y (248,208,64) → (244,192,80) |
| B1 | 1 | kop rechts (48,22) l → s (dubbele rand weg; model L194) |
| B2 | 4 | handrand (41,46)(42,47)(51,46)(50,47) K → l (binnenlijn niet zwart; model zwart, dus lijntint) |
| B3 | 1 | (51,44) l → m (2×2 lijnklontje; model L173) |
| B4 | 2 | elleboog (54,37)(54,38) l → s (dubbele rand; model L180/178) |
| B5 | 1 | (51,50) K → s (2 px dikke zwarte hoek; model L122) |
| B6 | 1 | (28,53) K → l (zwart op zwart tussen de voeten) |
| B7 | 1 | (10,43) l → s (lijnklontje boven de zwarte onderrand van de arm; model L102) |
| B8 | 4 | linkervoet (18–21,55) l → m (2 px donkere onderrand; model L243/244/198/189, schaduwtint aan de onderkant) |
| B9 | 5 | outline highlights (DC: "on the outlines in the very most highlighted parts") in s: kop linksboven (21,15)(22,15)(20,16), schouder links (9,35)(8,36) (model L209–252) |
| S1 | 18 | stenen: elke gloedpixel krijgt zijn tint uit het gloedaandeel van het model per spritepixel (≥55 % geel als het model daar geel heeft, anders oranje; 35–55 % oranje; 15–35 % rood; <15 % steen/zwart aan de rand). Gevolg: geel 11 → 6, oranje 13 → 15, rood 17 → 18, 2 randpixels links onder (21,47)(21,48) rood → zwart (model 7 %). Pixels: (21,47) (21,48) (22,39) (23,45) (24,40) (24,46) (25,36) (25,37) (25,48) (25,49) (26,36) (26,45) (26,47) (27,36) (27,38) (27,45) (27,47) (28,38) |

Diff per zone: silhouet 0, ogen 0, mond 0 (assert). Overige 38 px: kop 4, armen/hand 11, voeten 5, stenen 18. Emmer 0 px.
RGB: K, hout, grijs (band, ogen), steen en rood ongewijzigd (assert); de mond en de ooglijn-omgeving veranderen alleen via K1/K2 (index gelijk).

## Palet na (16 incl. transparant)
0 transp · 1 K (24,32,56) · 2 l (62,96,140) L90 · 3 s (120,156,190) L149 · 4 m (162,191,222) L185 · 5 h (208,226,244) L222 · 6 w (244,250,255) L248 · 7/8/9 hout (132,78,42)/(160,104,56)/(204,144,88) · 10/11 grijs · 12 steen (52,50,58) · 13 r (216,72,32) · 14 o (232,124,44) · 15 y (244,192,80).
Sneeuw = w/h/m/s + l + K: dezelfde tinten en opbouw als fase 1 (daar w/m/s/9/l/K), één extra schaduwtrap omdat het model meer volume heeft.

## Controles na
Geen zwart binnen de figuur buiten ogen, stenen en de emmernaad x44; geen lichte kleur op de buitenrand; geen dubbele rand meer langs kop, arm, hand en voet. Stenen: gloed 39 / donker 48 (r4 41 / 46), op 1× nu donkere stenen met een gloeiende rand, zoals het model.

## Ter info voor Jordi / resterende twijfels
- **Emmer:** donker hout (7) is zowel vulling van de rechterhelft als outline base van de emmer (palet vol, 16 kleuren). Daardoor zijn de naden x39/x40 in de rechterhelft onzichtbaar en is de naad op x44 zwart (een zwarte binnenlijn, tegen de regel; het model heeft daar wel zwarte naden). Niet aangeraakt: een aparte donkerste houttint kan alleen als er een paletplek vrijkomt (bijv. door een sneeuwtint te schrappen, wat volume kost). Op 1× leest de emmer als houten emmer met band.
- **Gloedtinten:** K3 + S1 maken de stenen donkerder; wil Jordi ze feller (meer "gloeiend") dan het model, dan is r4 de fellere variant.
- **K2** is subtiel (helderheid gelijk), maar trekt het lijf iets blauwer, gelijk aan fase 1.
- Losse s-pixels in de vacht (o.a. (40,34), (41,36), (39,40)) zijn taps uitlopende strengen uit het model; bewust laten staan.

Bestanden: `sneeuwmonster2_ek.png`, `sneeuwmonster2_8x.png`, `vel.png` (r4 | ek | model 8×; daaronder 1× en 2× op licht en donker naast fase 1, Skinguin, Dundragoon, Zapacha, Glalie `_gba`), `bouw.py`.

## Ronde ek2 (26 nov): ooglid + stenen
Jordi: "bijna helemaal tevreden, ooglid is een horizontale lijn en de stenen zijn nog niet helemaal herkenbaar als stenen". Bron `sneeuwmonster2_ek.png`, script `ek2/bouw.py`, uitvoer `ek2/sneeuwmonster2_ek2.png`, `ek2/sneeuwmonster2_ek2_8x.png`, `ek2/vel.png` (ek | ek2 | model 8×; ogen en stenen 12× naast het model; 1× en 2× op licht en donker naast fase 1 en de maatstaf). Palet ongewijzigd. Assert: silhouet, mond, emmer (7–9), vacht (2–6) index-diff 0; alleen pixels in de oogvakken en het steeninterieur (1/10/11/12) mogen wijzigen. Totaal 18 px.

**1. Ooglid (7 px).** Per kolom het donkergewogen zwaartepunt van de lidlijn in het model (L<70, binnen het oog, buiten de kasrand), in spriterijen: linkeroog x21 21,74 · x22–24 21,37–21,39; rechteroog x30 21,91 · x31 21,71 · x32 21,99 · x33 22,42 · x34 22,73. Het lid zakt dus naar de buitenhoek: links 1 px aan de buitenkant, rechts loopt het van rij 21 (x30–31) naar rij 22 (x32–34).
- O1 (6 px): linkeroog (21,22) → K, oude lidpixel (21,21) → g; rechteroog (30,21) (31,21) → K, oude (30,22) (31,22) → g (kas, model L79–109).
- O2 (1 px): (31,20) g → G: het licht van de kas boven het lid schuift mee (model L136).
Oogvorm, maat, plek en de kas zelf zijn hetzelfde gebleven.

**2. Stenen (11 px).** Per binnenpixel van de steen (rand blijft zwart, gloed blijft op de gemeten scheur- en randplekken: 39 px, ongewijzigd) de gemiddelde modelhelderheid van de niet-gloeiende steenpixels, met hergebruikte grijzen: ≥78 → G (160,166,176), lichte facetrand; 56–78 → g (88,92,104), licht facet; 30–56 → steen (52,50,58); <30 → K (scheur/diepste schaduw). Het model is gemeten mediaan L44 (p25 36, p75 64), dus de steentint 12 klopt en is niet aangepast.
- Boven: (24,35) G (model 79), (23,35) (24,36) (23,38) g (66/70/59), (22,38) K (28).
- Onder: (22,44) G (81), (23,44) (21,45) (22,46) (23,46) (25,46) g (66/72/76/61/57).
Resultaat: licht facet linksboven, donker naar rechtsonder, steen nu K 16 / steen 24 / g 8 / G 2 / gloed 39.

**Ter info voor Jordi (ek2):** de stenen zijn 5–6 px breed; hun omtrek is rond omdat de rand tegen de vacht ligt, en de vacht en het silhouet waren bevroren. Een hoekiger brokvorm (zoals in het model) kan alleen als er een paar vachtpixels rond de stenen mogen veranderen. Op 1× lezen ze nu als donkere brokken met een licht facet en een gloeiende rand. Of dat genoeg "steen" is, moet Jordi beoordelen.

## Ronde ek3 (26 nov): alleen de stenen, twee varianten
Opdracht: de gloed overheerste in ek2 (rechterhelft van elke steen oranje/geel/rood). Bron `ek2/sneeuwmonster2_ek2.png` (het ooglid van ek2 blijft), script `ek3/bouw.py`, palet ongewijzigd. Uitvoer: `ek3/sneeuwmonster2_ek3A.png`, `ek3/sneeuwmonster2_ek3B.png` (+ `_8x`), `ek3/vel.png` (stenen 16× ek2 | A | B | model; hele sprite 8×; 1× en 2× op licht en donker naast fase 1, Skinguin, Zapacha).
Steen per rij als tekstraster in `bouw.py` (K rand/diepste schaduw, steen, g licht facet, G lichte facetrand, r/o/y gloed), gelegd op de modelbrokken (16×-uitsnede met sprite-raster):
- **Boven:** lichte facetten linksboven (x22–25, r35–36) en een middengrijs facet onder de scheur (x23–24, r38); donker rechtsonder. De scheur loopt doorlopend over rij 37 (x23 r, x24 **geel**, x25 o) en via (26,36) o en (27,35) r naar de rand. Dunne gloedrand rechts (x28 r37–38, (27,39)) en onder ((26,40), rij 41).
- **Onder:** lichte facetten links (x21–23, r44–46). De scheur loopt van (22,44) r via (23,45) **geel** en (24,45) o naar (25,46) r. Dunne gloedrand rechts (x26–27, r44–48) en onder ((24–25,49)).

| variant | gewijzigd t.o.v. ek2 | steen px | gloed | geel | K / steen / g / G |
|---|---|---|---|---|---|
| ek2 | – | 89 | 39 (44 %) | 6 | – |
| **A** (zelfde omtrek) | 47 px, alleen binnen de stenen | 89 | 23 (26 %) | 2 | 34 / 19 / 11 / 2 |
| **B** (hoekige omtrek) | 54 px; vacht → steen: boven (26,34) (28,36) (28,39) (21,40), onder (20,47) (27,48) (22,49) | 96 | 26 (27 %) | 2 | 38 / 19 / 11 / 2 |

B volgt de modelbrok: boven een vlakke top tot x26, een rechte rechterflank op x28 (r36–39) en een scharpe hoek linksonder; onder een rechte linkerflank op x20 (r45–47), een vlakke onderkant (x22–25, r49) en een vierkante hoek rechtsonder (27,48). Dat is 4 en 3 px per steen (maximaal 6). Geen pixel steen → vacht.
Asserts: silhouet gelijk; alle wijzigingen binnen x19–29, y33–50; de nieuwe steenpixels grenzen direct aan de steen; ogen, mond, emmer (y ≤ 26) en de overige vacht hebben index-diff 0.

**Ter info voor Jordi:** in het model ligt de gloedrand deels buiten de zwarte rand en loopt hij rondom rechts. In A/B is hij 1 px dun en zit hij binnen de omtrek, zodat de steenmassa domineert. B leest op 1× het meest als een hoekige brok.
