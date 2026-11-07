# Keuring poedelmot kleur_r15 (verse keurder, blind geoordeeld)

Bron: `referenties/samengesteld.png`, mapping uit `silhouet/sil.py` (x 139–854 → 62 px, offset (1,17)); per-pixelgemiddelde `silhouet/gids_gemiddeld.png`. Vergeleken met Dustox en Venomoth (`graphics/pokemon/*/anim_front_gba.png`).
8×: `scratchpad/keur_r15/naast8.png`; 12×/16× per zone met overlay (rood = sprite 1/2/B, geel = sprite 3 over het model): `kop16.png`, `spriet.png`, `sprR.png`, `vleugelR.png`, `m_achter.png` (model met spriteraster), `vleugelL.png`, `poten16.png`; 1× naast Gen 3: `vergelijk.png`.
1×: kop, ogen en sprieten lezen meteen goed en als het model. De onderste helft (kraag, achtervleugel, poten) loopt over in één zachte crème massa. In het model zijn dat losse, zwart omlijnde donsbollen.

## Per onderdeel
| Onderdeel | Lijkt op / wijkt af in |
|---|---|
| Ogen | **Accuraat.** Rechteroog x25–32 y33–40, glans 2×2 (27–28,34–35), olijfglinster (28–30,37–38) en tan ring (x33, y32, y40), alles zoals in het model. Linkeroog x16–19 y32–40 is 1 rij hoger/langer dan het model (y33–39). Klein punt. |
| Kop/kin | **Accuraat.** De kinlijn (19–20,41) → (21–26,42) → (28–29,41) en (25–27,40) valt op de donkere boog van het model (21–25,42 / 25–29,41). |
| Sprieten | **Plaats, vorm en middennerf accuraat** (nerf links (3,18)→(19,28), model (6.7,18)→(19.7,28.7); in het midden ±1 px lager). **Wijkt af in de baardjes:** in het model zijn het doorlopende, steile tan strepen (±50/50 zwart/tan, periode ±2 px). De sprite heeft losse 4-stipjes met periode 3 onder 45°, waardoor de sprieten donkerder en gestippeld lezen in plaats van geveerd. |
| Bontkraag | **Vorm accuraat.** De onderrand naar de poten (y47–48, x23–31) is een enkelpixel-zigzag 3/A/3/A. Het model heeft daar donspunten met een doorlopende donkere lijn bij (18–19,48–49) en (24–25,48–49). |
| Linkervleugel | **Accuraat** (rand in 3 = selout, inkeping y37, tan banden rij 28–30). |
| Rechter voorvleugel | **Grotendeels accuraat** (geschulpte rand, inkepingen y24/y29, schubjes). **Wijkt af in de onderrand (naad met de achtervleugel):** het model heeft een rechte zwarte lijn op y35 van x42 tot 51, die daarna zakt naar (53–54,36) en (55–56,37). De sprite maakt er schulpen van: dalen op y36 bij x40–42, 45–47 en 50–53. Daardoor ligt de lijn op x45–47 en x50–51 1 px te laag en heeft hij bogen die het model niet heeft. |
| Rechter achtervleugel | **Wijkt af in de linkerrand:** model x42 (y38–41) → x41 (y42) → x42–44 (y43–45). Sprite (43,42), (43,43), (44,44), (45,45) ligt 1–2 px te ver rechts, met als grootste verschil 2 px op y42. Verder accuraat. |
| Middenstuk | **Wijkt af:** het model is hier donker grijsbruin met plaatnaden (lum ±80–150; (32,49) 82, (31,52) 80). De sprite heeft een lichte grijze strook: 8 (196,176,164) op x31–33 y49–53 en 9 (164,142,130) op x30–34 y53–56. Op 1× leest dat als een lichtgrijze vlek midden tussen de poten. |
| Poot A | Plaats accuraat (x15–20 y46–54, klauw 19,55). **Wijkt af:** de A/B-naad is in het model één doorlopende donkere lijn (19,49)→(20,50)→(21,51)→(22,52–54). De sprite heeft (18–19,49) en (20–22,50) en daarna niets op y51–52 (alleen 7/6). Het stuk (21,53–54) staat 1 px te ver links. A en B smelten zo samen. |
| Poot B + B2-plukje | B accuraat (x22–30, rechternaad x31). **Wijkt af:** de B/B2-naad ligt in het model op y55 (x22–30). In de sprite ligt hij op x25–27 op y56, met lichte 7 op (25–26,55): het plukje is in het midden doorgesneden. |
| Middenpootje | **Wijkt af:** model (31,55)=33, (31,56)=28, (32–33,55–56) donker. Dat is het donkere pootje tussen B2 en C. In de sprite staat daar lichtgrijs 9 (30–34,54–56); alleen (32–34,57–58) is donker. Het pootje is grotendeels weg. |
| Poot C | **Accuraat** (x35–41 y53–60, klauwen 24242 op y60, linkerrand x35). De bovenrand is half gesloten (36,52)=5. |
| Poot D | **Accuraat** (x42–48 y50–57, klauw 43–46). De C/D-naad heeft een gat op (41,54)=6; het model is hier donker (40,53–55). |
| Belijning algemeen | Buitenlijn 1 px en zonder open randen. De binnenlijnen tussen de poten zijn in het model zwart en doorlopend, in de sprite 3/6/5 en onderbroken. Dat is de hoofdoorzaak van de massa op 1×. |

## Gen 3 (naast Dustox/Venomoth)
- Netheid: de crème-groep gebruikt A, 7, 6, 5 (9 px) en 4 (schub 51–53,33 en 18,41): meer dan 3 tinten. Dat kan alleen als 5 en 4 als lijn gelden.
- Kraagrand y47–48: om en om 3 en A per pixel geeft ruis op 1×. Dustox en Venomoth hebben doorlopende naden.
- De onderkant mist vormscheiding. Bij Gen 3 heeft elke vorm die over een andere valt een gesloten donkere binnenlijn (Venomoth: lijf over vleugel).
- Kop, ogen, sprieten, licht linksboven en de selout aan de lichtkant zijn wel in orde.

## Top-5 reparaties
1. **A/B-naad doorlopend maken:** 2 of 3 op (21,51), (22,52), (22,53), (22,54) en (21,53) terug naar 7. De lijn loopt dan als (19,49)→(20,50)→(21,51)→(22,52–54).
2. **Middenpootje terugzetten:** (31,55), (31,56), (32,55), (32,56) en (33,55) in 2/1 (donker pootje), aansluitend op de klauwen (32–34,57–58). 9 alleen houden waar het model licht is (30,54) en (34,54).
3. **Middenstuk donkerder:** 8 op x32–33 y49–53 naar 4/9-niveau (model ±110–150 lum). Daarmee is de lichtgrijze strook weg.
4. **Naad tussen voor- en achtervleugel recht:** y35 doorlopend van x42 tot 51 in 3/2, dan (52–54,36) en (55–56,37). Haal de dalen (45–47,36) en (50–51,36) weg (crème van de voorvleugel blijft boven, dons van de achtervleugel eronder).
5. **Linkerrand achtervleugel 1 px naar links:** (42,42), (42,43), (43,44), (44,45) in plaats van (43,42), (43,43), (44,44), (45,45). Daarnaast de C/D-naad sluiten op (41,54) of (40,54), en de B/B2-naad op y55 (x25–27) leggen in plaats van y56.

Kleiner: sprietbaardjes als doorlopende steile tan strepen in plaats van stipjes; kraagzigzag y47–48 als donspunten met een doorlopende lijn.

Oordeel: FAIL
