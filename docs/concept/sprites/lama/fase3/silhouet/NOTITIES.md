# Silhouet lama fase 3, ronde 1 – notities

**Opdracht:** het hele silhouet overtrekken van het bevroren poppetje (`fase3_r4('Y')`, pose C2: camera yaw 45, kop +18, pitch 8;
`bron.py`) op de 50%-dekkingsgrens, max. 1 px afwijking, alleen korrels weghalen. Werkwijze zoals fase 2 ronde 6. Niets ontworpen of verbeterd.

## Meting
- Model bij 50% (`model50.txt`): 1288 px, box 37×62, 27 korrels (8 uitsteeksel-px, 8 inkeping-px, 11 tanden).
- **Ronde 1 (`ronde1.txt`): 1286 px.** Alleen ronde 1: 6 px, alleen model: 8 px; **14 afwijkingen, 0 afwijkingen > 1 px** van de 50%-grens
  (`diff_model.txt`, script `diff_model.py`, nu tegen `alpha.npy` van fase 3).
- `korrel.py ronde1.txt`: **0 uitsteeksel-px, 0 inkeping-px, 0 tanden** (`korrel_uitvoer.txt`). Eén component, 0 losse px, 0 gaten.
- Gekozen per korrel: de kleinste set flips (1–2 px, elk naast de 50%-grens) die de korrel weghaalt, bij gelijke uitkomst de flip
  waarvan de dekking het dichtst bij 50% ligt (som |dekking − 0,5| over alle 14: 1,56).

## Afwijkingen per onderdeel (alle 14, elk max. 1 px)
- **Kop / oren / bombín (y0–13):**
  - +x25 y1 (25%): **uitzondering dun deel (oor)**: de top van het verre oor was een diagonale trap van 1 px (x24 y1 los boven x24–25 y2, dan
    x25–26 y3); nu 2 px breed doorlopend. Gemeld: aanvulling van een dun deel.
  - −x23 y5 (76%): 1-px inkeping tussen de oren (x24 y5) dichtgemaakt door de V 1 px breder te maken, niet door hem te vullen
    (vullen zou x24 y5 met 10% dekking kosten).
  - −x18 y9 (56%): uitsteeksel van 1 px aan de achterkant van de kop.
  - +x26 y11 (19%) en −x28 y13 (57%): inkeping en uitsteeksel aan de achterkant van kop/bombín-rand samen gladgemaakt.
    x26 y11 is de grootste afwijking qua dekking (19%), maar ligt direct naast de grens (y10 en y12 zijn op x26 gevuld).
  - De bombín zelf breekt de omtrek niet (hij zit tussen/vóór de oren binnen de kopvorm); 0 afwijkingen nodig.
- **Vlechten (y12–40, voorkant hals/borst):** 0 afwijkingen; ze liggen binnen de omtrek (hooguit de bobbel x14–15 y16–17 en de
  borstlijn x14 y32–38). Niets aangevuld.
- **Hals / halsband (y14–27):** +x28 y17 (42%): 1-px uitsteeksel-rij x28 y18 aan de achterkant van de hals; nu 2 rijen.
- **Lijf / cape / riem / rok (y26–45):** +x35 y27 (45%): 1-px inkeping in de rug tussen schouder en staart; −x50 y42 (58%):
  1-px uitsteeksel aan de achterkant van de rok.
- **Staart (x44–46, y25–27):** 0 afwijkingen, precies het model.
- **Voorpoten (x17–30, y45–62):** +x32 y45 (48%): 1-px inkeping bovenaan de opening tussen voor- en achterpoten; de opening begint
  nu op y46. Verder 0 afwijkingen.
- **Achterpoten (x33–48, y45–60):** −x40 y52–55 (4× 58%): de spleet tussen de twee achterpoten was 1 px breed (x41); nu 2 px
  (x40–41), zoals hij in het model al bestaat (y56 is daar ook 2 px). Geen nieuwe opening, alleen 1 px breder. +x46 y60 (44%): de
  hoef van de rechterachterpoot was een 1-px punt (x45 y60); nu 2 px.

## Wat op 1× niet leest (eerlijk; niet opgelost)
- **De twee voorpoten zijn één blok** (x17–30, 13 px breed): in pose C2 valt de verre voorpoot vrijwel helemaal achter de nabije
  (plus de windsels); op 1× leest er één dikke voorpoot. Samen met de twee achterpoten leest de lama als **driepoot**.
- **De achterpoten** zijn gescheiden door een spleet van maar 2 px (y52–57); op 1× leest het bijna als één achterblok met een kerf.
- **Vlechten en bombín** zijn in het silhouet niet te zien (binnen de omtrek); Jordi wil ze "echt duidelijk" zien, dat moet dus
  helemaal uit kleur/omlijning komen. Het silhouet zelf geeft alleen de twee oren met een ondiepe V.
- **Staart** is een bultje van 3×3 px boven de rug; op 1× een hoekje, geen staart.
- **Formaat:** 1286 px, maar 9 % groter dan fase 2 (1184 px) en ver onder de Gen 3-zwaargewichten op het vel (Camerupt 2039,
  Tauros 1931, Donphan 2096, Rhyhorn 1702); de norm noemt fase 3 ≈ 2,4× fase 1 (±2000+). De hoge hals vult de 64 in de hoogte
  (box 37×62), dus fase 3 leest op 1× niet als "duidelijk zwaarder" dan fase 2; het lijkt vooral een rechtop blok.
- Cape, riem en rok vallen binnen de lijfomtrek; dat komt pas met kleur.
- Dit zijn eigenschappen van het poppetje in deze pose/camera. Wil Jordi het anders, dan moet het poppetje (of de camera) veranderen,
  niet het silhouet.

## Bestanden
- `ronde1.txt`, `ronde1_1x.png` (zwart op wit), `diff_model.py` / `diff_model.txt`, `korrel_uitvoer.txt`,
  `vel_ronde1.py` → `vel_ronde1.png` (onderlaag | ronde 1 4× | omtrek over de onderlaag | 1×; onder: Camerupt, Tauros, Donphan,
  Rhyhorn (Gen 3 `anim_front_gba.png`, frame 1), lama fase 2 (`fase2/af/lama.png`) en ronde 1 op 1× en 2×).

## Lessen
- Korrels weghalen kan met een klein zoekscript: alle 1- en 2-px-flips naast de 50%-grens rond elke korrel proberen, kiezen op
  minste korrels en daarna kleinste |dekking − 0,5|; 27 korrels → 0 met 14 flips, alle ≤ 1 px.
- Gen 3-referenties staan in `graphics/pokemon/<naam>/anim_front_gba.png` (64×128, bovenste frame); `front.png` bestaat hier niet.

---

# Ronde 2 (poppetje W3: lijf, hals en poten dikker, lengtes gelijk)
Bron opnieuw (`bron.py`): `model50.txt` 1509 px, box 40×63, 22 korrels (5 uitsteeksel-px, 8 inkeping-px, 9 tanden). De bron van ronde 1
staat in `ronde1_bron/`. **Jordi over ronde 1:** de voorpoten als blok is akkoord ("de voorpoten moeten gewoon netjes gekleurd en geshade worden").

## Meting
- **Ronde 2 (`ronde2.txt`): 1512 px.** Alleen ronde 2: 7 px, alleen model: 4 px; **11 afwijkingen, 0 > 1 px** van de 50%-grens
  (`diff_model.txt`; `diff_model.py` neemt nu het bestand als argument, standaard `ronde2.txt`).
- `korrel.py ronde2.txt`: **0 / 0 / 0** (`korrel_uitvoer_ronde2.txt`). Eén component, 0 losse px, 0 gaten.
- Zoekscript nu in de map: `opt.py` (`python3 opt.py ronde2.txt`); daarna met de hand één keuze omgedraaid (achterpoten, zie onder).
- Let op: `diff_model.txt` hoort nu bij ronde 2 (de afwijkingen van ronde 1 staan hierboven); `vel_ronde1.py` opnieuw draaien zou
  de nieuwe onderlaag gebruiken, dus `vel_ronde1.png` niet opnieuw maken.

## Afwijkingen per onderdeel (alle 11, elk max. 1 px)
- **Oren (dunne delen):** +x20 y1 (29%): top van het nabije oor was 1 px (x21); nu 2 px. +x25 y1 (49%) en +x24 y2 (42%): top van
  het verre oor was een trapje van 1 px (x24 y1 los boven x25–26 y2); nu doorlopend 2 px. Alle drie gemeld als aanvulling van een dun deel.
- **Kop / bombín:** +x24 y5 (30%): 1-px inkeping onderaan de V tussen de oren gevuld (de V loopt nu y1–4). −x18 y9 (52%):
  uitsteeksel achter de kop. +x26 y11 (44%) en +x28 y12 (36%): inkeping/trap aan de achterkant van de kop gladgemaakt.
  De bombín breekt de omtrek niet; 0 eigen afwijkingen.
- **Vlechten, hals/halsband, lijf/cape/riem/rok, staart:** 0 afwijkingen.
- **Voorpoten / opening naar de achterpoten:** in het model is de opening x32 y49–52 maar 1 px breed met trapjes (x31 y51, y53–55).
  +x32 y49 (31%): de opening begint nu op y50. −x31 y50 (69%) en −x31 y52 (62%): de opening is nu over y50–55 gelijk 2 px breed (x31–32).
- **Achterpoten:** het model heeft tussen de achterpoten alleen een 1-px kerf op y57 (x41) en 2 px op y58. `opt.py` koos +x41 y57
  (27%, kosten 0,23); met de hand vervangen door **−x40 y57 (76%, kosten 0,26)**, bijna gelijk, maar zo blijft de kerf die het model
  heeft (2 rijen) bestaan in plaats van tot één rij te krimpen.

## Wat op 1× niet leest (eerlijk; niet opgelost)
- **De voorpoten zijn één blok** (x17–30); akkoord van Jordi, op te lossen met kleur en schaduw.
- **De achterpoten zijn bijna één blok:** de kerf ertussen is maar 2 rijen hoog (y57–58); op 1× lezen ze als één achterpoot.
  Silhouet = twee poot-massa's (voor en achter) onder een groot lijfblok.
- **Bombín en vlechten** blijven binnen de omtrek; alleen de oren met een ondiepe V steken uit. Leesbaarheid moet uit kleur komen.
- **Staart:** bultje van ±4×3 px (x44–47 y21–23); op 1× een hoekje aan de rug.
- **Formaat:** 1512 px (fase 2: 1184, +28 %); dichter bij de Gen 3-zwaargewichten (Rhyhorn 1702, Tauros 1931), maar nog kleiner.
  De poten zijn kort t.o.v. het lijf: op 1× leest het als een zwaar, stompig blok (past bij "stompig"), minder als lama-op-poten.
- Cape, riem en rok vallen binnen de lijfomtrek; komt pas met kleur.

## Bestanden ronde 2
`ronde2.txt`, `ronde2_1x.png`, `diff_model.txt`, `korrel_uitvoer_ronde2.txt`, `opt.py`, `vel_ronde2.py` → `vel_ronde2.png`
(onderlaag W3 | ronde 2 4× | omtrek over de onderlaag | 1×; onder: Camerupt, Tauros, Donphan, Rhyhorn, fase 2, ronde 1 en ronde 2 op 1× en 2×).

## Lessen ronde 2
- `opt.py` kiest puur op dekking; bij een bijna gelijke keuze (verschil < 0,05) de flip nemen die een opening uit het model
  behoudt in plaats van dichtmaakt, en dat melden.

---

# Ronde 3 (spritebron K3: kop 1,2×, bombín 1,3× en naar links, vlechten 1,3× en naar buiten)
Verse maker. Bron (`bron.py`, `SPRITE`): `model50.txt` 1487 px, box 39×63, 20 korrels (2 uitsteeksel-px, 10 inkeping-px, 8 tanden).
De bron van ronde 2 staat in `ronde2_bron/`. Opdracht als ronde 1–2: hele model overtrekken op de 50 %-grens, max. ±1 px, alleen korrels weg,
geen eigen vormeisen, openingen niet dichtmaken; let op bombín (bol + rand links) en vrije oren.

## Meting
- **Ronde 3 (`ronde3.txt`): 1488 px**, box 39×63 (x13–51, y1–63). Alleen ronde 3: 7 px, alleen model: 6 px; **13 afwijkingen, 0 > 1 px**
  van de 50 %-grens (`diff_model_ronde3.txt`). Eén component, 0 losse px, 0 gaten.
- `korrel.py ronde3.txt`: **0 / 0 / 0** (`korrel_uitvoer_ronde3.txt`).
- Werkwijze: eerst `opt.py` (gaf 12 flips, 0 korrels), daarna met de hand drie keuzes vervangen (bombín links, vlecht, opening/kerf; zie onder),
  steeds met de exacte dekking per pixel (niet `dekking.txt` op het oog: die is lastig te lezen, ik las hem eerst 1 kolom verschoven).
- Kop (y0–13) 122 px tegen 102 in ronde 2 (+20 %); hals/borst (y14–27) 292 tegen 300. Totaal 24 px minder dan ronde 2 (model 1487 tegen 1509).

## Afwijkingen per onderdeel (alle 13, elk max. 1 px)
- **Oren (dunne delen):** +x25 y2 (40 %): top van het verre oor was een 1-px trap (x25–26 y1 boven x26–27 y2); nu doorlopend. **Gemeld als
  aanvulling van een dun deel.** −x24 y4 (88 %): de 1-px inkeping x25 y4 tussen bombínbol en ver oor is niet dichtgemaakt (vullen kostte even
  veel, 20 %) maar 1 px breder: de V tussen de oren loopt nu y1–4 door, zodat het verre oor vrij blijft van de bol.
- **Bombín links (rand):** in het model steekt de rand op y10–11 maar 1 px uit (x17), met daaronder een 1-px inkeping (x18 y12) tegen de kop.
  `opt.py` vulde alleen x18 y12 (22 %): dan wordt de rand een lipje van 1 px dat in de kop overloopt. Gekozen: **+x16 y10 (42 %), +x16 y11 (25 %)
  en +x18 y12 (22 %)**: de rand zelf loopt in de bron tot halverwege x16 (42 %), dus 1 px verder naar links trekken is nog op de grens; samen
  steekt de rand nu 2 px uit (x16–17, 2 rijen) boven de kop (y12–13 begint op x18). Kosten 0,61 tegen 0,28, maar de rand leest als rand.
  Alternatief overwogen: −x18 y13 (99 %, inkeping 2 rijen hoog): ook ≤ 1 px, maar haalt een vol kop-pixel weg; niet gekozen.
- **Bombín rechts:** −x28 y11 (83 %): inkeping x28 y12 tussen rand en kop aan de achterkant 1 rij dieper gemaakt i.p.v. dicht (vullen: 10 %).
- **Bombínbol:** 0 afwijkingen. De bol zelf (x19–27 y4–9) is in de omtrek géén eigen koepel: het nabije oor staat er recht bovenop (x20–22 y1–3)
  en het verre oor sluit rechts aan; zijn linkerkant is een rechte rand x19. Alleen de rand leest in het silhouet als hoed.
- **Vlechten:** +x14 y20 (35 %): 1-px inkeping in de linkerrand van de hals. `opt.py` haalde x14 y18–19 weg (53 % / 50 %, goedkoper: 0,03 tegen
  0,15); gekozen voor vullen, zodat de vlecht die in de bron naar buiten is gezet zijn breedte houdt (linkerrand x14 doorlopend y18–25).
- **Hals/halsband, lijf, staart, voorpoten:** 0 afwijkingen.
- **Rok:** +x50 y38 (47 %): 1-px inkeping achteraan de rok.
- **Opening voor-/achterpoten:** in het model x32 y50–53 maar 1 px breed. +x32 y50 (32 %): de opening begint nu op y51 (1 rij korter, zoals ronde 2);
  −x33 y51–53 (76 / 65 / 53 %): opening y51–56 gelijk 2 px breed (x32–33). `opt.py` hield y50 open met −x33 y50 (87 %), duurder (0,81 tegen 0,62).
- **Kerf tussen de achterpoten:** model x41 y57 1 px (43 %) boven x40–41 y58. `opt.py` vulde x41 y57 (kosten 0,07, kerf → 1 rij); gekozen
  **−x40 y57 (92 %, kosten 0,42)**, zoals ronde 2: de kerf blijft 2 rijen hoog (y57–58) en 2 px breed. Het verschil is hier groot (0,35);
  het enige argument is de opdracht "openingen niet dichtmaken".

## Wat op 1× niet leest (eerlijk; niet opgelost)
- **Bombín:** op 1× is de rand een knobbeltje van 2×2 px links aan de kop; de bol is niet als koepel te zien (oren erop). "Hoed" leest pas met kleur
  (donker vlak + rand). Wel beter dan ronde 2, waar de rand helemaal in de kop zat.
- **Oren:** vrij, twee punten met een V van 4 rijen (y1–4); het verre oor loopt rechts als bult door tot y8. Leest op 1× als twee oortjes.
- **Kop:** groter (+20 px), maar in het silhouet is de snuit niet te zien (kop driekwart naar voren, snuit binnen de omtrek); de kop leest als een
  rechtop blok met hoed en oren.
- **Vlechten:** maken de hals links breder (x14) maar zijn in de omtrek geen eigen vorm; alleen via kleur.
- **Voorpoten één blok** (akkoord Jordi), **achterpoten bijna één blok** (kerf 2 rijen), staart een bultje van ±4×3 px: als ronde 2.
- Formaat 1488 px (fase 2: 1184, 1,26×); iets kleiner dan ronde 2 (1512), omdat het model kleiner is (de grotere kop vult de 64 in de hoogte).

## Bestanden ronde 3
`ronde3.txt`, `ronde3_1x.png`, `diff_model_ronde3.txt`, `korrel_uitvoer_ronde3.txt`, `vel_ronde3.py` → `vel_ronde3.png` (onderlaag K3 | ronde 3 4× |
omtrek over de onderlaag | 1×; onder: Camerupt, Tauros, Donphan, Rhyhorn, fase 2, ronde 2 (goedgekeurd) en ronde 3 op 1× en 2×).
`vel_ronde2.py/png` en `diff_model.txt` (ronde 2) ongemoeid.

## Lessen ronde 3
- Lees de dekking als getallen (numpy, `c[y, x]`), niet uit `dekking.txt`: die rijen zijn makkelijk 1 kolom verkeerd af te tellen.
- `opt.py` kiest goedkoop maar kan een dun kenmerk (hoedrand) tot een 1-px lipje vlakmaken; bij kenmerken die de opdracht noemt de buurpixels
  met 25–45 % dekking aan de buitenkant meewegen (de echte rand loopt daar nog door).
