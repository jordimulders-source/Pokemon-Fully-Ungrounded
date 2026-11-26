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
