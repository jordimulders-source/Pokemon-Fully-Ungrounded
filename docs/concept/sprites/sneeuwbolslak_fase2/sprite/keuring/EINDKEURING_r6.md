# Eindkeuring r6 – sneeuwbolslak fase 2

Getoetst: `sprite/maker/r6.png` / `raster_r6.txt` / `pal6.py` tegen het model `sprite/r8_bol_r7.png`. Gemeten met `meet/px.py`, `recht.py` en `bewaak.py`, met een telling van de tinten per stap en de tintvlakjes. Daarnaast gelegd: Glalie, Regice en Sealeo (Gen 3) en fase 1. Toegevoegd: Jordi's punten "kijk ook naar bolinhoud, de binnenkant is niks uit te halen momenteel" en "het lijkt nu gewoon op een bevroren bol, je ziet niet meer wat er binnenin gebeurt".

**Oordeel: FAIL.** Lijf, kop, ring en staart zijn klaar voor Jordi. De binnenkant van de bol niet: die leest als massief ijs en niet als glas met een storm erin.

## Eerste indruk (blind)
- Op 1× leest de sprite als het model: kop met oog en blauwe wang, de ronde bol met barst en ijspunten, de rode ring, de flap en de staart in scherven.
- Het silhouet is identiek aan het bevroren silhouet (diff 0).
- Er zijn 21 rechte stukken, het langste 5 px. De zijkanten van de bol (4 px verticaal op x 21, 41 en 42) passen bij een cirkel met straal 10,6.
- Naast Glalie en Regice is het geheel bleek, en de bol is het zwakste deel. Het is een lichte ijsbal met een zwarte barst. Je ziet niet wat er binnenin gebeurt.

## Controle MOET-punten r5
| Punt | Status | Toelichting |
|---|---|---|
| 1. Aansluiting/ringeinde | Opgelost | Het ringeinde is dicht met (24,40) `#` en (25,41) `r`. (22,38) en (23,39) zijn `a`, niet `d`/`#`. De maker koos dat om geen nieuwe rechte stukken te maken; dat is akkoord, want de rand sluit. |
| 2. Ring | Opgelost | Grondtint `r`, `s` alleen op (27–32,42), geen `t` meer. |
| 3. Staartnaad | Opgelost | De naad loopt door van (48,30) tot (44,42). |
| 4. Kopschaduw | Opgelost | De grens is nu een boog. |

## De binnenkant van de bol (Jordi: telt als MOET)

### Wat het model daar laat zien
Gemeten per spritepixel met `px.py` en daarna gladgestreken om de grote vormen te zien:
1. **Glanslicht linksboven.** Een lichte vlek op x 24–28, y 25–28 (L ±230).
2. **Lichte rand en bodem.** Een lichte binnenrand langs links (x 22) en rechts (x 39–41, y 28–37, L 185–225). Een heldere bodemband op y 36–39, x 23–39, die rechtsonder doorloopt tot (38–39,36–37).
3. **Donkere banen van de storm**, als bogen op een middentint. De doorkijktint is overwegend `b`/`c`: het model telt in de binnenschijf 76 `b`, 82 `c` en maar 26 `e`.
   - Boog A bovenlangs: y 24 x 28–32, dan y 25 x 30–39.
   - Baan B op y 30, x 23–29, die linksom afbuigt naar een donkere massa op x 22–25, y 31–34.
   - Gespikkelde baan C rechts, x 37–40, y 27–36.
4. **Lichte kern** rechts onder de barstvork, x 31–35, y 31–35.
5. **Barst.** Model-L 76–111, dus de tint is `d` en geen zwart. De barst loopt van (35,26) omlaag naar de vork bij (34–36,29). De linkertak gaat via (33,30) naar (30,33). De rechtertak gaat via (37,32) en (36,34–36) naar (37,37).

### Waarom het in r6 niet leest
- **Glas zonder glaskenmerken.** Rechts staat een kolom `a` (x 40, y 26–37, en x 39, y 33–37) evenwijdig aan de rand. Het model heeft daar `c`/`e` (L 160–225, gemiddeld 50–90 lichter). Daardoor is de bol gearceerd als een ondoorzichtige ijsbal (en dat is banding). Glas leest juist andersom: licht valt door het glas en maakt de binnenrand aan de schaduwkant en de bodem licht.
- **Te licht.** r6 heeft in de binnenschijf 56 `e` tegen 26 in het model, en 48 `b` tegen 76. De storm heeft geen donkerdere doorkijktint om tegen af te steken. Het resultaat is berijpt ijs.
- **Ruis in plaats van vormen.** In de bol staan 44 tintvlakjes van minder dan 3 px. Het zijn losse spikkels `b`/`e` zonder richting, dus er is geen wervel te zien. Dat is de "pixel blur".
- **De barst is zwart.** De barst is `#` (15 px) en het enige echte contrast in de bol. Hij leest als een kras op het oppervlak, en Jordi zei eerder "veel zwart".

### Hoe glas leest in Gen 3 (alleen op de plekken van het model)
- Een donkere buitenlijn.
- Daarbinnen aan de schaduwkant (rechts en onder) een **lichte** binnenrand: het licht dat door het glas valt.
- Eén scherp glanslicht linksboven (`w`-kern in `e`).
- Een heldere bodem/kaustiek.
- De inhoud in een iets donkerdere doorkijktint met eigen contrast.
- Geen vormschaduw van een massieve bol op de inhoud.

Regice werkt zo met lichte facetranden en donkerdere vlakken.

## MOET
De pixels zijn exact en per script toe te passen: `python3 sprite/keuring/eindkeuring_r6_moet.py uit.txt uit.png`, vanuit de werkmap. Alle "van"-letters zijn gecontroleerd op r6 (0 mismatches). Silhouet-diff blijft 0 en het aantal rechte stukken blijft 21.

**M1. Barst van zwart naar `d`** (het model is L 76–111):
- `#`→`d` op (35,26), (35,27), (35,28), (34,29), (36,29), (32,30), (33,30), (36,30), (31,31), (37,31), (30,32), (37,32), (37,33), (36,34) en (36,35).
- De onderste tak doortrekken zoals in het model: (36,36) `b`→`d`, (37,37) `b`→`d` en (37,36) `d`→`a`.

**M2. Rechterbinnenrand van glas** (licht in plaats van de `a`-kolom):
- (39,25) `a`→`b`
- (40,26) `a`→`b`, (40,27) `a`→`b`, (40,28) `a`→`c`
- (40,29) `b`→`c`, (41,29) `a`→`c`
- (41,30) `a`→`e`, (41,31) `a`→`e`, (41,32) `a`→`c`
- (39,33) `a`→`b`, (40,33) `a`→`c`, (39,34) `a`→`b`, (40,34) `a`→`c`, (39,35) `a`→`b`, (40,35) `a`→`c`
- (39,36) `a`→`e`, (40,36) `a`→`b`
- (38,37) `a`→`e`, (39,37) `a`→`c`, (38,38) `a`→`c`

Dit zijn de kaustiek rechtsonder en de doorlopende bodemband.

**M3a. Doorkijktint en stormbanen op de plekken van het model** (tinten verschuiven):
- **Boog A:** (35,24) `e`→`c`, (39,24) `e`→`c`, (34,25), (35,25), (37,25) en (38,25) `c`→`b`.
- **Lichte band:** (27,29) `b`→`e`, en (29,29), (30,29) en (31,29) `e`→`c`.
- **Baan B:** (23,30), (27,30), (28,30) en (29,30) `c`→`b`. Verder (31,30) `e`→`c`, (34,30), (35,30) en (35,29) `e`→`b`, en (25,32) `e`→`b`.
- **Lichte kern:** (34,34), (31,35) en (34,35) `c`→`e`. Verder (30,34), (35,34) en (35,35) `c`→`b`, en (37,34) `c`→`e` (de belichte kant van de barst).
- **Vlokken** (de modelpixels met de hoogste piek binnen een donkerder blok): (27,33) `c`→`w` en (33,37) `e`→`w`.

Na M1–M3a wijkt de binnenschijf op 121 van 207 px niet af van het model (r6: 91). Afwijkingen van 2 stappen of meer gaan van 32 naar 16.

**M3b. Opruimen (handwerk door de maker, binnen de bol)**
Na M3a staan er nog ±45 spikkels. Die bestonden al in r6. Teken de binnenkant als vormen:
- Boog A als één doorlopende band van 1–2 px `b`, langs de bovenrand.
- Baan B als één sikkel `b` van (23,30) tot (29,30), die langs de linkerrand afbuigt naar x 22–24, y 31–34.
- Baan C als een dunne `b`-boog op x 38–39, net binnen de lichte rand van M2.
- Daartussen alleen `c`.
- Lichte vormen als hele vlakken: het glanslicht (x 23–28, y 25–28), de lichte band op y 29, de kern (x 31–35, y 31–35) en de bodem.
- Binnen de bol hoogstens ±10 tintvlakjes van minder dan 3 px, en alleen `w`-vlokken mogen 1 px zijn: (27,33), (33,37) en hoogstens 2 extra op de lichte banden.
- Geen nieuwe tinten en niets buiten de bol veranderen. Diff 0 buiten x 22–41, y 23–38.

## MAG
- Een lichtpixel `e` op de belichte kant van de barst, waar het model licht is: (36,27) en (36,28). Zo leest de barst als een barst in glas.
- Het hele lijf ligt een stap lichter en zachter dan Glalie, Regice en Sealeo. Het klopt wel met het model (kop ±0, lijf +6). Laten zo.

## Ter info voor Jordi
- Het model zelf toont de storm op 64 px als gespikkelde banen. Een storm die je ook op 1× ziet vraagt daarom om gestileerde banen en vlokken op dezelfde plekken. Dat is wat M3 vraagt, zonder het ontwerp te veranderen.
