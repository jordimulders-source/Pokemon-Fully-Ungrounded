# Keuring regionale Abra, kleur_r7 (verse eindkeurder, 13 nov)

Getoetst: `basis_F.png` tegen `../referenties/gemini_gekozen.png` via `../kleur_r1/natief.png` (spritepixel (x,y) = natief (2x−1, 2y−14)), op 1× en 8× naast het model op dezelfde schaal en naast de Gen 3-sprites abra, kadabra, sneasel, mightyena en umbreon (`graphics/pokemon/*/anim_front_gba.png`, eerste frame). Jordi's vraag: "schaduw, kleuren en belijning". Bevroren: silhouet, ogen ((22,28)(23,29)(24,30)(24,31), (30,27)(29,28)(28,29)(28,30); in basis_F gecontroleerd, K met L-uiteinden), pose, vorm.

## Hoofdvraag: is dit een nette Gen 3-sprite die trouw is aan het model?
**Bijna.** De vertaling volgt het model per modelblok (vlekjes en streepjes zitten erin). Wat het nog geen eindversie maakte: een vulpixel op de buitenrand, drie plekken waar de lijnkleur op één rand wisselt, en twee bijna-dubbele tinten in het palet (m naast b, I naast 3). Die laatste gaven op de snuit banding (h|b|m|s in vier kolommen van 1 px). Na de MOET-punten hieronder: ja, voor zover de techniek gaat. De drukte in de rechterhand zit in het model (vingers van 1 px) en blijft.

## Schaduw
- Licht linksboven is consequent: kop links h/b, rechts s; platen 3 met 1 aan de onderkant/rechts; linkerarm lichte band links, rechterbovenarm een lichte streep (b) in de donkere plaat; staart licht aan de binnenkant van de lus en aan de bovenkant van het onderste stuk. Geen pillow shading: het hooglicht op de kop (21–25, 22–26) zit linksboven, zoals in het model.
- Banding: snuit rij 32–34, x24 h | x25 b | x26 m | x27 s (MOET 2).
- Losse ruispixels: alle clusters < 3 px vallen samen met modelvlekjes of knokkels in de hand (modelblokken gecontroleerd); niet weggepoetst ("behoud die vibe").

## Kleuren
- 11 kleuren + transparant. Huid had 4 vultinten (h 207, b 179, m 158, s 127) + T 101 + I 90. **m** is een bijna-dubbel van b (Δ21) en **I** (90) is visueel gelijk aan **3** (89). Na r7: 9 kleuren; huid h/b/s + T (lichte selout) + L (lijn), platen 3/2/1 + K.
- Stappen huid: 207 → 179 → 127 → 101 → 57 (Taillow-norm ±30–40; b→s is met 52 groot, dat zijn de modeltonen: zie B).
- Hue-shift: schaduw (s, T, L) violetter dan het licht, binnen de modelkleuren (het model meet onder s gemiddeld (130,127,151), onder h (211,207,221)). Geen wijziging in A.
- Jordi: "zelfde huidskleur wel als de rest". Keuze voor Jordi: **A** = modeltonen; **B** = huidreeks van de regionale Kadabra (220/185/145/94, lijn (66,64,86)). B is lichter en iets violetter in de schaduw, met een gelijkmatigere reeks (36/40/51). Claude kiest niet.

## Belijning
- 1 px, geen 2×2-lijnblokken op één na in de plaatrand (44,32) die het model zo heeft; geen 2×2 zwartblokken.
- Selout: lichtkant L/T (kop links/boven, linkerarm, voet, staart bovenkant), schaduwkant K. K op een lichtkant op: bovenrand platen (25–27), kaak/kin (20,32)(24,36–37), oorpunt (34,15), staartbovenkant onder het lijf (45–49,46–47) en het teenpuntje (8,50): donker materiaal of slagschaduw onder het lijf, zoals het model. Goed zo.
- Wisselende lijnkleur op één rand: vingertop (29,51), gatrand (29,39)/(30,42–43), vingertop-onderrand (30,58) (MOET 4–6).
- Zwart 21,6 % (Gen 3: abra 18,0, kadabra 18,7, mightyena 17,7, umbreon 12,8). Boven de norm door de zwarte plaatnaden en kaak van het model; geen dikke binnenlijnen gevonden. Ter info, geen fout.

## MOET
| # | pixels (x,y) | nu → voorstel | reden |
|---|---|---|---|
| 1 | (24,51) | I → K | vulkleur op de buitenrand; model sK/sK, sluit de K-rand (25,50)–(25,52) |
| 2 | m: (27,27)(27,28)(26,29)(27,29)(26,30)(26,31) → s; (26,32–34)(26–28,45)(40,47) → b; (41,47)(40,48) → s | m weg | bijna-dubbel met b; huid ≤3 vultinten; snuitbanding weg. Per pixel op modelmediaan (≥153 b); de schuine plooi naast het rechteroog en de snuitgrens naar s (modelblokken half b, half s 123–133: de donkere helft is het streepje) |
| 3 | I: (34,27)(31,40)(11–13,49)(22,51)(22,52)(30,60) | I → 3 | bijna-dubbel (90 vs 89); vlekjes en plooien blijven, zelfde toon |
| 4 | (29,51) T → L, (29,52) K → L | vingertop rechterhand | T geïsoleerd tussen K's; model (29,52) licht (253/100): lichtkant L, onderkant (30,53) blijft K |
| 5 | (29,39) L → K; (30,42)(30,43) T → L | rand van het gat arm/lijf | was L K K L T T op één rand; nu K (oksel/boven) → L (buikkant). Model (29,39) 96/95/7/49 |
| 6 | (30,58) | I → K | onderrand vingertop, model KK/.. (= KEURING_r3 MAG a, nooit uitgevoerd) |

## MAG
| # | pixels | voorstel | reden | uitgevoerd |
|---|---|---|---|---|
| a | (52,52) | s → 3 | ringstreepje staart, model 83 (r3 c) | ja |
| b | (53,52)(52,53) | b → s | staartring, donkere modelhelft 67–77 (r3 f) | ja |
| c | (22,50) | b → 3 | top vingerplooi links, model 57 (r3 d) | ja |
| d | (39,40) | s → b | lichte streep bovenarm loopt door, model 183 (r3 g) | ja |
| e | (15,54)(15,55) | K → L | linkerrand scheen is lichtkant | ja |
| f | (27,30)(13,50) | s → 3 (r3 e) | vibe-vlekjes | **nee**: (27,30) ligt tegen het bevroren rechteroog en verlengt het; (13,50) verdubbelt de teenplooi |
| g | (28,20) | b → s (r3 g) | modelmediaan 129 | **nee**: zou een losse s-pixel in het b-vlak geven (ruis) |
| h | (52,54)(52,55) | L → T | één lijnkleur in de staartlus | **nee**: L → T verloopt geleidelijk (geen om-en-om), model is daar zwart |

## Status r3-punten
Alle 11 MOET-punten van r3 zitten in basis_F (via r4–r6). Van de 8 MAG-punten was alleen b uitgevoerd; a, c, d, f, g(39,40) nu wel; e en g(28,20) bewust niet (zie boven); h vervalt (de hand volgt het model).

## Na uitvoering (controle `maak_r7.py`)
Silhouet-diff 0, ogen ongewijzigd, 37 pixels gewijzigd, 9 kleuren, geen vulkleur op de buitenrand, geen geïsoleerde lijnkleur meer op de buitenrand. Op 8× naast het model nog één keer bekeken: geen nieuwe slordigheid; de rechterhand blijft druk zoals het model.
