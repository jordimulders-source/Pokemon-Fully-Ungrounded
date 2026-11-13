# Regionale Kadabra (charlatan-leerling): kleur r1

Model: `../model/model_B_hand3.png` (Jordi: "ja prima", "deze is nu goed"). Toegestane afwijking (Jordi): "al moet de kaartvinger nog een nagel hebben, maar dat kan in de sprite, weet niet hoe goed die vertaalt met pixels".

Bouwen: `python3 cellen.py` (model → 100×100 cellen), `python3 meet.py` (meting per spritepixel, `meet.npz`), `python3 onderlaag.py` (→ `onderlaag.txt` = `basis0.txt`), `python3 ../silhouet/sil.py` (in `../silhouet/`), `python3 hand.py basis0.txt raster.txt`, `python3 pal.py raster.txt kadabra_charlatan.png kadabra_charlatan_8x.png`, `python3 vel.py`. Meten: `controle.py`, `lichtkant.py`, `lijnkaart.py`, `q.py x0 y0 x1 y1` (modelcellen onder een sprite-uitsnede), `zij.py` (sprite | model op dezelfde schaal), `r.py` (raster met liniaal).

## Formaat
- Model: figuur 94×82 cellen (x 3–96, y 10–91). Schaal 31/47 = 0,66 → **62×54 px**, x 1–62, y 9–62 (onderaan in het kader).
- Echte Kadabra (Gen 3): 53×53, y 6–58. Charlatan-Alakazam: 56×63. De Kadabra is 9 px lager dan de Alakazam en breder door de gespreide armen (richtlijn 60–62 × 52–54).
- 1 spritepixel = 1,516 modelcel. De handen kunnen dus niet letterlijk cel voor cel over; ze zijn per cel gemeten en op de spritepixels gezet (zie Zwakke punten).

## Gedaan
1. **Silhouet** (`../silhouet/silhouet.png`, bevroren): dekking ≥ 0,5 per spritepixel + 13 px met de hand in dunne delen waar het model dekking 0,3–0,5 heeft (lijst in `sil.py`: kaartrand, duim, onderlijnen van klauwtjes, tweede gebogen vinger, hielklauw). Gaten die in het model achtergrond zijn blijven open: onder de duim van de open hand, tussen kaartarm en romp, de inkeping tussen de twee vingers van de open hand.
2. **Onderlaag** (`onderlaag.py`): per spritepixel de fractie zwart (L<20), donkerpaars (model-selout), zwart materiaal (L 20–95, neutraal), wit en rood, en de mediaan van de rest. Lijn waar zwart + donkerpaars ≥ 0,34.
3. **Palet** = charlatan-Alakazam (`pal.py`, 11 kleuren + transparant): o; zwart materiaal k/m met licht n (= kleur d); grijs a/b/c met selout d; wit w; rood t/r/s.
4. **Toonkeuze:** het model heeft twee grijzen (licht ±187, midden ±148). Die zijn gemapt op **a en b** (niet b en c), zodat het lijf even licht is als bij de Alakazam; c is met de hand gezet als schaduw (rechterhelft rechteroor en kop rechts, onderkant staart als sikkel, onderkant dij tussen de benen, handpalm rechtsonder, hiel). Zwart materiaal: model-basis → m, model-licht → n (klein, linksboven), k als schaduw rechtsonder.
5. **Handwerk per zone** (`hand.py`, elke regel is een rijstuk op het raster):
   - **Kop:** oren met lichte strook links en vouwlijn d in het rechteroor (gemeten: (36,12) → (35,13) → (34,14–15) → (33,16) → (34,17) → (35,18)); bovenlijn tussen de oren op rij 14; wenkbrauw d (29–31,21) + (31,20); oog dichtbij: pupil (28,22), wit (29–30,22); ver oog: lid (23,22), wit (23,23); neusrug: lichte strook a (24–25,24–25) → (24,26–27) → (23,28) met lijn d rechts ervan ((26,24–25), (25,26–27), (24,28)); mondhoek (29,25); snuitpunt (24–25,29).
   - **Klaver:** bovenste lob (25–26,18–19), zijlobben (24–27,20), steel (25,21); t als glans linksboven, s rechts en in de steel. In het model 6×6 cellen = 4×4 px.
   - **Platen/romp/borst:** scheidingslijn plaat–romp op x35 (rij 25–29), onderrand rechterplaat op rij 30; snorstrengen links (22,27) → (21,28–30) en rechts (30,27) → (30–31,28) → (31,29), elk met omlijning; witte borst met a-rand en de zwarte boog (28–30,34); buikvlek wit vanaf rij 38.
   - **Kaarthand:** kaart x1–6, y19–26, schoppen (4,22), (3–5,23), (4,24); gestrekte vinger (6–7,25) → (7–8,26) → (8–9,27) met **nagel w op (6,24)**; eerste gebogen vinger (5–6,28) met punt d (4,28); tweede gebogen vinger (7–8,31).
   - **Open hand:** vinger omhoog (54,21–22) → (53,23–24) met klauwtje (55,20); vinger schuin rechts (58–59,24) met klauwtje (60,24); duim (47–48,26) met klauwtje (47,27); inkeping tussen de vingers open; plooi in de palm (53,27).
   - **Benen/voeten:** dijlijn d/o (27,41) → (28,44); kruislijn x33 (rij 41–44); knieën zwart met eigen omlijning; linkervoet: lange teen met klauwtje (16,57), twee klauwtjes (17,58) en (18,59), hielklauw (27,56); rechtervoet: klauwtjes (39,61) en (46,60).
6. **Selout** (`hand.py` → `selout`): buitenlijn aan de lichtkant o → d naast grijs/wit en o → k naast zwart materiaal; kaartrand en de rechterrand van het linkeroor blijven o.

## Vingers geteld in de sprite
- **Open hand: 3** (duim naar links, vinger omhoog, vinger schuin naar rechts), elk met een wit klauwtje (3 witte pixels: (47,27), (55,20), (60,24)).
- **Kaarthand: 3** (gestrekte vinger langs de kaart met nagel, twee gebogen vingers eronder).

## Nagel op de kaartvinger
- Met nagel (hoofdsprite): (6,24) w, de vinger eronder b in plaats van a zodat het wit loskomt. Zonder nagel: `variant_zonder_nagel.txt` ((6,24) d, vinger a). Beide op 12× en 3× op het vel.
- Op 12× is de nagel te zien als wit puntje tussen de kaartrand en de vinger. **Op 1× leest hij niet als nagel:** hij ligt tegen de witte kaart en het zwarte schoppensymbool en valt daarmee samen.

## Afwijking van de onderlaag per zone (pixels anders dan `basis0.txt`)
| zone | px | anders | waarvan lijn↔vlak | waarom |
|---|---|---|---|---|
| oren + schedel (y9–17) | 96 | 38 | 10 | selout d op de randen, lichte strook en vouwlijn, schaduw c rechts |
| gezicht, klaver, snuit | 191 | 40 | 9 | oog, wenkbrauw, klaver in drie tinten, neusrug als strook + lijn, schaduw c op de wang |
| platen, romp, borst | 107 | 31 | 5 | scheidingslijn op x35, k-schaduw, minder n, a-rand van de borst |
| kaarthand + arm | 130 | 39 | 22 | kaartrand, schoppen, nagel, gebogen vingers als vlak met omlijning |
| open hand + arm | 159 | 45 | 11 | klauwtjes omsloten, selout boven op de vingers, palm in b/c |
| benen + buik | 275 | 63 | 18 | dij- en kruislijn doorgetrokken, knieën omlijnd, schaduw c onder de dij |
| staart | 166 | 43 | 2 | sikkelschaduw c, bovenrand in één tint d |
| voeten | 84 | 23 | 10 | klauwtjes omsloten, teenlijnen |

## Controle
- `controle.py`: 11 kleuren + transparant; open randen 0; losse o 0; **alpha-diff 0** met `../silhouet/silhouet.png`; box 62×54, 1208 px.
- Clusters < 3 px (zonder lijnen d, klauwtjes/oogwit w en de klaver): 3, alle in vingers en tenen van 2 px: (58–59,24) a, (5–6,28) a, (17–18,57) a.
- `lichtkant.py`: 3 van 124 = **2 % zwart aan de lichtkant** (doel ≤ 25 %; echte Kadabra 23 %, Alakazam 7 %). Over: (28,14) binnenhoek linkeroor, (1,22) kaartrand, (6,30) vingertop.
- `lijnkaart_r1.png` (drempel 0,34): 355 lijnpixels gelijk, 32 rood (alleen model), 64 blauw (alleen sprite). Rood: de randen die k-selout werden (telt de kaart niet als lijn), de vijf klauwtjes die op een modellijn liggen, (24,24) en (29,22). Blauw: bijna alleen de verplichte buitenlijn waar het model een halve pixel lijn of geen lijn heeft.

## Afwijkingen van het model
- Nagel op de kaartvinger (toegestaan door Jordi).
- Tonen een stap lichter dan het model (a/b in plaats van b/c) en c-schaduw met de hand; het zwart is m met k, zoals bij de Alakazam, en daardoor grijzer dan in het model.
- Silhouet +13 px in dunne delen (zie boven).
- Weggelaten omdat ze kleiner zijn dan een spritepixel: de tweede lijn links op de neusrug (24,24), het gaatje van 1 cel tussen dij en kruis, het gaatje tussen kaart en gebogen vingers.
- Oog dichtbij: pupil links, twee pixels wit rechts ervan; het witte puntje linksonder de pupil uit het model past er niet bij.

## Zwakke punten
- **Handen:** op 0,66 schaal zijn de vingers 1 pixel vulling met omlijning. De drie vingers per hand zijn te tellen op 8×; op 1× leest de kaarthand als kaart + vuist. De tweede gebogen vinger is 2 pixels.
- **Nagel** leest op 1× niet (zie boven).
- **Klaver:** 4×4 px; op 8× een klaver (lob, twee zijlobben, steel), op 1× een rood kruisje.
- **Zwart:** platen en romp lezen blauwgrijs in plaats van zwart, vooral op een donkere achtergrond. Dat is gelijk aan de Alakazam, maar donkerder kan (basis k in plaats van m).
- **Linkerplaat** (links in beeld) is klein en valt bijna weg achter de snuit; in het model ook, maar daar is hij zwarter.
- **Snorstrengen** naast de snuit zijn 1 pixel breed met omlijning; onder de kin is het druk (lijn, streng, lijn).
- **Lichtkant 2 %** ligt onder het bereik van de echte sprites (3–23 %): er staat bijna geen zwart meer aan de lichtkant; de randen zijn daardoor op een lichte achtergrond wat zacht.
- Nog niet gekeurd door een onafhankelijke keurder.
