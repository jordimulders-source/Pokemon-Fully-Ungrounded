# Keuring r4 – sneeuwbolslak fase 2 (verse keurder, 15 nov)

Getoetst: `sprite/maker/r4.png` / `raster_r4.txt` / `pal4.py` tegen `sprite/r8_bol_r7.png` (via `meet/px.py`, `lijnkaart.py`, `recht.py`). Alleen de twee eisen: trouw aan het model en een strakke Gen 3-sprite. Vel: `keurvel_r4.png` (nummers = MOET-punten; 6 geldt voor de hele sprite).

**Oordeel: FAIL** (dichtbij qua vorm, maar Jordi's vier punten zijn nog zichtbaar: schaduw, belijning, kleur, rechte lijnen).

## (a) Eerste indruk (blind, 1× en 8×)
Op 1× leest hij goed als het model: kop met oog en blauwe wang links, bol met barst en rode ring, ijsstaart rechtsboven. De vorm klopt bijna overal met het model (barst, ring, flapcontour en nekenaad liggen op de modellijnen). Wat nog niet strak is, is de afwerking. De rechterkant van de bol en de hele staart bestaan uit evenwijdige strepen van 1–3 px (lijn, licht, midden, lijn), zodat het streperig en hoekig oogt in plaats van rond. Binnen in de bol liggen de sneeuwstrepen als vlakke horizontale balken. De ring en de staart wisselen zwart en donkerblauw op één rand af. De blauwen zijn paarser dan de cyaanachtige modeltinten en de donkerste rode tint is bijna zwart.

## (b) MOET (op volgorde van belang)
1. **Bol rechterkant: verticale banding.** (38,29)–(41,36) is een vaste band van 3 px `b` met een `c`-kolom op (38,31)–(38,36), direct naast de barst `#` op x 37 en de buitenlijn op x 41–42. Zo ontstaat een rij evenwijdige verticale strepen. In het model is dit vlak gevlekt middentoon b/c met lichte vlekken: (38–41,30) is in het model `e`, (37–41,31) is b/c gemengd. Gewenst: de modelvlekken overnemen en de schaduw alleen als sikkel langs de buitenlijn tekenen, 1 px boven (40,25)–(40,28), oplopend naar 2 px rechtsonder (39–40,33)–(38–39,37). Geen `c`-kolom evenwijdig aan de barst.
2. **Bol binnen: rechte horizontale balken.** Het gaat om (28–32,24) `b`, (30–35,25) `b`, (23–27,29) `c`, (24–28,30) `b`, (26–30,35) `b`, (27–31,36) `b` en (25–30,37) `wwwwww`. Het model heeft op die plekken wel strepen, maar dat is een wervelende sneeuwstorm. Gewenst: de strepen op hun plek laten, maar elke streep na 2–3 px 1 px laten op- of aflopen (kringelend). Wissel b en c af, zodat er geen drie gelijke rijen recht onder elkaar liggen (35–37). `w` alleen als kleine glans (≤ 3 px per vlek), niet als balk van 6 px.
3. **Staart, bovenste waaier: belijning en strepen.**
   - Op de zaagrand wisselen zwart en blauw elkaar af: (50,25)`d` (52,25)`d` (53,25)`#` (51,26)`#` (53,26)`#`, en verder (48–50,29)`ddd` (45–46,30)`dd` (47,30)`#`. De bovenkant van elke scherf wordt overal `d` (lichtkant), `#` alleen aan de rechter- of onderkant.
   - Er staan te veel volle binnennaden in `d`: x 50 (y 25–29), x 53 (y 27–28 en 31–32), x 49 (y 33–35), x 46 (y 35–36). Het model heeft naden op x 48–49 (y 26–30), x 53 (y 29–30), x 51–52 (y 31–33) en x 47 (y 32–35). Houd alleen die, en laat ze taps lopen (`d` in het midden, `a` aan de uiteinden).
   - Losse strepen van 1 px `e`/`c` tussen de naden: (52,26) (57,29) (56,30) (58,28) (55,28) (56,31) (57,30). Geef elke scherf twee tonen, licht links (e/c, 1–2 px) en `b` rechts, zonder eilandjes van 1 px.
4. **Staart, onderste segment: toegevoegde naad en diagonale banding.** De naad (47,35)–(47,39), (46,40), (45,41), (43–44,42) staat niet in het model. Het model heeft hier alleen een korte naad (48–49,35–37) en het donker op (43–44,42) en (46,42). Daarnaast lopen de banden `ee`/`cc`/`b` (41–46, 37–42) evenwijdig aan die naad en de band van 2 px `aa` langs de rechterrand (49–52, 41–47). Gewenst zoals het model: grond `b`, twee lichte strepen op x 43 (y 36–41) en x 48–49 (y 37–40), en de schaduw onderaan (y 45–48 `a`) in plaats van een vaste band langs de rand.
5. **Ring.**
   - De onderrand mengt `d` en `#`: (25–26,42)`dd` (27–29,43)`ddd` (30–33,44)`####` (34–36,43)`ddd` (37–40,42)`dddd`. Kies één tint voor de hele onderrand; het model is daar zwart, dus `#`.
   - De tint `r` (104,40,52; helderheid 65) is veel donkerder dan het model (≈139,62,72; helderheid 91) en geeft het "veel zwart"-effect. Gewenst: r ≈ (136,56,68), s ≈ (172,72,80); t (196,92,96) is goed.
   - Ruis: het lichte `t`-eilandje op (30–31,42) in de `s`-rij, en de losse (39,39)s (37,40)s (39,40)r (37,41)r (32,42)s (32,43)r. Gewenst: `t` linksboven (24–29,40–41), `s` in het midden, `r` alleen als smalle strook rechtsonder (33–38,42–43).
   - Het model heeft links 3 rijen rood. Maak (27–29,43) rood (`s`) en schuif de onderrand naar (27–29,44).
6. **Kleur: terug naar de modeltinten.** Gemeten als mediaan van het modelblok per tint: b (120,170,206) tegenover model (132,183,203), a (80,124,168) tegenover (82,141,168), c (166,210,232) tegenover (179,215,227). Het palet is blauwer en paarser gemaakt ("richting Regice"), maar het model is cyaanachtig. Gewenst: b ≈ (130,182,206), a ≈ (82,140,168), c ≈ (176,214,228), d evenredig ≈ (46,82,112). Houd de helderheidsstappen van ±35–40.
7. **Zijflap: één vlak plat `e`.** (34–41,44), (29–36,45), (28–33,46) en (27–33,47) vormen ±29 px in één tint. Het model loopt van e linksboven naar b rechtsonder: (34–38,46) is `b` (nu `c`), (31–34,47) is `b` en (35–36,47) is `c`.
8. **Lijfnaad als trap van 4–4–4.** (27–30,51), (31–34,52) en (35–38,51) zijn drie gelijke stukken van 4 px `dddd`. Teken één vloeiende boog met stappen van 2–3–4–3–2 (laagste punt rond x 32–33 op y 52), tapse uiteinden in `a`.
9. **Staartpunt: 4 gelijke rijen `dec#`.** (56–59,21)–(56–59,24): de `c`-kolom op x 58 maakt een rechte streep. Het model heeft hier 2 px licht en 2 px middentoon. Gewenst: (57,21)–(57,24) `e`, (58,22)–(58,24) `b`, de `c` alleen op (58,21) als overgang.

## (c) MAG
- Pootje (flipper) linksonder: zwart en blauw lopen door elkaar op (10–13,52)`####`, (13,53)`d`, (12,54)`d` en (11–12,55)`##`. Liever de hele bovenrand `d` en de onderrand `#`.
- Onder het oog heeft het model een tealkleurige pixel; (12,48) zou `b` kunnen worden in plaats van `c`.
- De ijsgroep gebruikt 5 tinten (a, b, c, e, w) plus `d`. Door `w` alleen voor glans te gebruiken blijft het per onderdeel bij 3 tinten.
- De onderrand van het lijf heeft stukken van 5 px: (23–27,57) en (28–32,58). Het silhouet is bevroren en het model is hier nog vlakker, dus alleen aanpakken als Jordi het noemt.

## (d) Goed, niet aanraken
- Silhouet (`sil56_r4.npy`) en de ronde bol: de zijkanten zijn 4–3–4 px, wat klopt voor een cirkel met straal 10,6.
- De barst ligt bijna pixel voor pixel op het model: stam (35,26)–(35,28), linkertak tot (30,33), rechtertak (37,31)–(36,35).
- Oog (11–13,45–47) met glans, en de blauwe wang u/v (14–18,46–50) op de plek van het model.
- Kopschaduw: `e` linksboven, `c` onder het midden, `b` langs de naad. Nekenaad x 22–23 (y 38–46) staat zo in het model.
- De ringvorm (halve maan onder de bol), de bovenrand van de ring (24–26,39), (27–29,40), (30–33,41), (34–36,40), (37–38,39) en de flapcontour (30–33,44), (34–36,43), (37–40,42) liggen op de modellijnen.
- Selout: links en boven `d`, rechts en onder `#` bij kop en bol. De ijspunten bovenop de bol staan op de plekken van het model.
- Het aantal donkere binnenpixels (158) is gelijk aan het model (151). Het "veel zwart" komt nu vooral van `r` en van de mengranden, niet van te veel lijnen.
