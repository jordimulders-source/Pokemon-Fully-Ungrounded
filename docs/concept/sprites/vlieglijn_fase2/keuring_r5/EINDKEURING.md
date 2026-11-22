# Eindkeuring mug r5 (verse keurder, Dragonfly Cave / Gen 3, 21 nov)

Gekeurd: `sprite_r5/mug_r5.png` naast het model (`referenties/gemini_gekozen_r1.png` op het spriteraster, `celmeting.py`, DY 2) en Ninjask, Beedrill, Yanmega en Masquerain (eerste 64×64-frame).
Ik heb alleen de uitvoering gekeurd: kleur, schaduw en belijning. Vorm en silhouet zijn bevroren (Jordi: "de vorm is perfect" · "niks opnieuw tekenen" · "het is puur kleurgebruik" · "en belijning"). Alle wissels zijn tintwissels van bestaande pixels. `wissels.py` controleert per pixel de oude index en of de alpha-diff met r5 0 is.

## Verdict: BIJNA (PASS na MOET, 13 px)

1. **Hoofdvraag:** ja. Op 1× en 2× is dit een nette, scherpe Gen 3-sprite. De pose, de \ /-ogen, de naald en de vleugels lezen meteen. De arm/poot-driehoek klopt: de borstarm (bovenarm x33–34, gele elleboog (35,36), onderarm = de rechte poot met i-glans) staat voor, de knie-poot ligt donker erachter. Daar komt niets aan. Er zijn geen losse spikkels in de vlakken meer, en geen zachte middentint-randen in vleugels, koepel of poten. Er blijven twee plekken die op 1× nog troebel lezen:
   - het **achterlijf**: de lichtste paarse tint q staat in losse spikkels van 1–2 px op (37,37), (42,36–37), (44,41–42) en (35–36,40), zonder één samenhangend hooglicht. Daarnaast grenst paars p aan de grijze schaal L met bijna dezelfde helderheid (92 tegen 84), en grenst q aan de poot-i (146 tegen 143). Daardoor smelten paneel, schaal en poot ineen. Dat is het "patchwork" dat de vorige maker noemde.
   - het **onderste borststuk**: 11 px vlak q (x25–30, y29–30), zonder schaduwkant.
2. **Volume:**
   - Koepel: goed (L-selout, w-hooglicht linksboven, g, d).
   - Vleugels: goed (glansstrook links, aders d, geel achterrand).
   - Naald: goed.
   - Poten: goed (i/l/k, glans links).
   - Borststuk boven: volgt het model.
   - Borststuk onder en achterlijf: zie MOET A en B. Met A krijgt het achterlijf één hooglichtstrook langs de poot (x44, y41–45), dan p en dan een P-sikkel tegen de k-rand.
3. **Tinten en stappen:** elke groep heeft 3 vultinten plus lijn (geel 2, wat goed is voor zo'n klein vlak).

   | Groep | Tinten (L-waarde) | Stappen |
   |---|---|---|
   | Grijs | w 227 / g 164 / d 114 | 63 / 50 |
   | Paars | q 146 / p 92 / P 55 | 54 / 37 |
   | Poot | i 143 / l 85 / k 46 | 58 / 39 |

   Ter vergelijking: Ninjask (grijs 215/174/145/120/96, ±25–40), Beedrill (paars 215/180/131/91, ±35–50) en Yanmega (rood 133/84/62). De stappen zijn ruim genoeg, er is geen banding door te kleine stappen. Jordi's "2 vultinten max maakt blurry" is opgelost.
4. **Belijning:**
   - Rand: 269 `#`, 70 L-selout (lichtkant vleugels en koepel), 20 k (kin en naald aan de lichtkant) en 1 Y (knie-top, gele selout).
   - Nergens om-en-om, geen open randen, geen lichte kleur op de buitenrand.
   - Binnenlijnen staan in k, de donkerste vlaktint.
   - Zwart staat in het vizier en tussen de dunne poten, en dat volgt het model.
5. **Kleine vlakken:**
   - Ogen: LED-gloed van binnenuit, dat is goed.
   - Naaldpunt: goed.
   - Elleboog (35,36–37): goed.
   - Knie (23–25,44–46): de linkerkant staat in Y en de rechterkant in y. Dat is omgekeerd ten opzichte van licht linksboven, zie MOET C.
   - Ring op het achterlijf, schoudergewricht en klauw-elleboog zijn één tint geel zonder schaduwkant, zie MAG.
6. **Ledematen:** elk ledemaat leest als één geheel. Na A leest de achterste poot over het achterlijf (i-kolom x38–43) ook los van het paneel.

## MOET (indexen: 1 # · 2 k · 3 d · 4 g · 5 w · 6 P · 7 p · 8 q · 9 L · 10 l · 11 i · 12 Y · 13 y)
**A. Achterlijf, 8 px**
- (43,38) en (43,39): 7→6. Zo grenst p niet meer aan de schaal L met dezelfde helderheid.
- (45,41): 7→8. De bovenrand van het paneel onder de schaal wordt licht.
- (44,43), (44,44) en (45,45): 7→8. Het hooglicht loopt daarmee door als één strook langs de poot.
- (46,46): 7→6. Dit maakt de sikkel onderaan.
- (37,37): 8→7. Nu staat q niet meer tegen poot-i.

**B. Borststuk onder, 3 px**
- (30,29), (29,30) en (30,30): 8→7. Zo ontstaat een schaduwkant rechts, zoals in het model (model 138 → 113).

**C. Knie op lichtrichting, 2 px**
- (23,45): 12→13
- (25,45): 13→12

De top (23,44) blijft Y als gele selout.

## MAG (11 px)
- **Geel met een schaduwkant:**
  - ring achterlijf (40,34) en (40,35): 13→12
  - schoudergewricht (34,26) en (34,27): 13→12
  - klauw-elleboog (23,35): 12→13
- **Vleugeltip:** w tegen y (227/212) smelt op 1× tot één vlek. Wissel (55,18), (56,18), (57,18), (22,2) en (22,3): 5→4.
- **Ader:** (45,7) 3→5. Hier stond d tussen de selout en de glansstrook (L d w).

## Bestanden (keuring_r5/)
- `wissels.py`: MOET (ACHTERLIJF, BORSTSTUK, KNIE) en MAG (GEEL, VLEUGELTIP, ADER), met `--geen-mag`. Het script stopt als een oude index niet klopt of als de alpha-diff niet 0 is. Gecontroleerd: MOET 13 px, MOET+MAG 24 px, alpha-diff 0.
- `voorstel.png`: MOET+MAG, met hetzelfde palet.
- `voorstel_8x.png`
- `vel.png`:
  - rij 1: r5 | alleen MOET | MOET+MAG | model op 8×
  - rij 2: r5 en voorstel op 1× en 2× op licht en donker

## Ter info voor Jordi
- Het geheel is donker: `#` en k samen zijn ±42 % van de figuur. Dat komt van het zwarte vizier en de donkere poten van het model. Wil je hem lichter, dan kan l (slot 10) een stap omhoog. Dat is een paletkeuze en geen wissel.
