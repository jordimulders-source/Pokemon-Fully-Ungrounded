# Keuring mug sprite r1 (verse keurder, 21 nov)

Te keuren: `sprite_r1/mug_r1.png`. Model: `referenties/gemini_gekozen_r1.png` / `maat/natief.png`.
Eerst blind geoordeeld (vergelijkingsbeelden hieronder), daarna pas `reparaties.txt` gelezen.

Beelden in deze map:
- `naast_8x.png`, `naast_2x.png`, `naast_1x.png`: model (natief, BOX-verkleind naar de bbox van de sprite) links, sprite rechts
- `kop_16x.png`: kop/vizier/ogen close-up (x10–39, y13–31), `natief_kop_10x.png`: kop in het natieve raster
- `romp_12x.png`: borststuk + achterlijf (x22–51, y14–49)

## Verdict: BIJNA

Trouw is goed: silhouet, maat en plek van alle onderdelen kloppen met het model. Het model toont **3 vleugels** (lange links, lange rechtsboven, korte rechtsonder; geen vierde zichtbaar) en de sprite ook: niets toegevoegd of weggelaten. Poten: dezelfde 5 als het model (klauwpoot bij de naald, poot met gele knie bij (23,35), poot met gele knie bij (23–25,44–46), twee lange achterpoten tot (36,60) en (53,63)). Het enige echte probleem is het linkeroog (vraag C); daarnaast een paar Gen 3-netheidspunten.

## A. Hoofdvraag
Ja. Op 1× en 2× leest het als hetzelfde beest als het model: grijze koepel met paarse band en zwart vizier, naald schuin naar linksonder in aanvalshouding, paars borststuk met gele beugel, donker achterlijf met paarse panelen en gele ringen, grijze vleugels met gele randen. Pose en verhoudingen zijn één op één het model. Leest als een nette Gen 3-sprite; de ogen zijn het zwakste punt.

## B. Volume
- Koepel: goed (hooglicht w linksboven (18–20,16–18), g-vlak, d-naad en schaduw naar rechtsonder, paarse band zoals model).
- Naald: goed (w-lichtkant boven, d-schaduw onder, k-rand), 3–4 px breed en taps.
- Vleugels: goed voor vlak vlies (w-voorrand, g-vlak, d-aders diagonaal zoals model, gele rand).
- Borststuk: voldoende (q licht linksboven (25–29,19–21), p, schaduw k/# rechtsonder).
- Poten: l + i (licht aan de bovenkant) + lijn; voldoende voor dunne delen.
- Achterlijf: het zwakste vlak. Panelen zijn alleen p, de schaal alleen k + één 1-px d-lijn (42,32)–(44,35); geen hooglicht op de bolling, de lichtere zone zit alleen als dunne lijn langs de rand. Zie MAG 1.

## C. Ogen (\ /)
Model per spritecel (natief-raster per cel bemonsterd): linkeroog loopt schuin \ (bovenpunt links bij x13–14 op y22, onderkant breder naar rechts tot x15–16 op y24–25); rechteroog loopt schuin / (boven x21–23, onder x19–21). Paars met roze kern klopt.
- Rechteroog (19–22,22–26): leest als /, komt overeen met het model. OK.
- Linkeroog (14–15,22–25): een rechte kolom van 2 px breed, op 1× en 2× leest het als `|`, niet als `\`. Samen geeft dat `| /` in plaats van `\ /`. Het model heeft hier de schuine onderkant naar rechts. **MOET 1.**

## D. Naald en poten op 1×
Lezen allebei. Naald 3–4 px met lijn, punt bij (4,42); poten 3–4 px inclusief lijn, de lange achterpoten 3 px ("#l#"/"#ll#"). Niet dunner maken.

## E. Netheid
- Tinten: grijs w/g/d + k (k is ook vizier/selout), paars q/p/P, poten i/l, geel y/Y, oog e/E. Binnen ≤3 + lijn, maar P (86,48,102) komt maar **1×** voor: (27,29). Zie MAG 2.
- Clusters < 3 px: bijna allemaal 1-px diagonale lijnen (vleugeladers, naald, pootranden): dat is lijnwerk, geen ruis. Echte losse vlekjes: P (27,29), en het losse `#` in het achterlijf (45,37).
- Belijning: **k en # om en om op de linkerrand van de linkervleugel** (lichtkant): y1–4 k, y5 `#` (21,5), y6–9 k, y10–12 `#` (22,10),(23,11),(23,12), y13–14 k. **MOET 2.**
- Gele knie (23,44),(23,45): geel Y op de buitenrand zonder lijn (links ervan transparant). Model heeft hier een donkere omtrek rond het gewricht. **MOET 3.**
- Trapjes/rechte stukken: buik/achterlijfrand rechts (47–49, 37–46) loopt in nette stappen; geen rechte stukken waar het model rond is. OK.
- Geen banding of pillow shading, behalve de dunne d-lijn langs de achterlijfrand (MAG 1).
- Zwart: `#` = 29 % van de figuur, `#`+k = 43 %. Hoog, maar komt uit het model (zwart vizier, donker achterlijf, veel dunne poten die lijn nodig hebben). Geen FAIL.

## MOET
1. **Linkeroog (14–16,22–25) moet \ lezen.** Neem de oogvorm over uit het model: de onderkant loopt in het model naar rechts door (cel (16,24): ±30 % oogroze/violet volgens de makermeting, de reductie gaf antraciet k). Zet (16,24) op de oogtint E (of e als kern) zodat de vorm 1–2–3 breed schuin naar rechtsonder loopt, gespiegeld aan het rechteroog. Controleer op 1× dat het paar `\ /` leest.
2. **Linkervleugel linkerrand: één soort rand.** (21,5), (22,10), (23,11), (23,12) zijn `#` tussen k-selout. Lichtkant: maak ze k (zoals de rest van die rand), of de hele rand `#`; niet om en om.
3. **Gele knie (23,44),(23,45) zonder buitenlijn.** Neem de omtrek over uit het model (donker rond het gewricht): de transparante buren (22,44),(22,45) krijgen `#`, of de randpixels zelf worden lijn met de gele tint één px naar binnen. Silhouet verandert maximaal 2 px.

## MAG
1. **Achterlijf volume:** panelen (38–45,36–46) zijn alleen p. Waar het model de panelen lichter paars heeft (bovenste/linker deel van elk paneel), neem dat over als q; de schaal mag een breder d-vlak linksboven (42–45,32–36) krijgen in plaats van de 1-px d-lijn, zoals het model lichter grijs op de bolling heeft.
2. **Lone P (27,29):** enige pixel van die tint; maak hem p of q (buurtint, model is daar donker + lichtpaars), of gebruik P echt als schaduwtint van het borststuk (rechtsonder, nu k) zodat paars 3 tinten heeft in plaats van p/q + grijs k als schaduw.
3. **Los `#` (45,37)** in het achterlijf tussen k-pixels: k maken, tenzij het model daar een naad heeft (dan zo laten).

## Makerrapport (achteraf gelezen)
`reparaties.txt` klopt met wat ik zag: silhouet 0 afwijkingen, oogpixels per cel gemeten, (16,24) bewust k gelaten omdat antraciet in de cel won. Dat verklaart MOET 1: de meerderheidsregel haalt de schuine oogpunt weg; de \ zit in het model in de minderheidspixels van die cel.
