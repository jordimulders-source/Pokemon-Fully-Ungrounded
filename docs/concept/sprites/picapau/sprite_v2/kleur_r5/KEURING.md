# Keuring picapau sprite_v2 kleur r5 (verse keurder, 5 nov)

Gekeurd: `kleur_r5/picapau.png` (855 px, 15 kleuren). Ik heb niets aan de sprite veranderd.
Coördinaten zijn (x,y) in de 64×64-sprite. De tekens zijn die van `raster.txt`:
- geel: `1` licht, `2` basis, `3` schaduw, `4` goudbruine omlijning
- vleugel: `l` licht, `b` basis, `d` donker
- grijs: `h` licht, `g` midden, `G` donker
- `k` zwart, `c`/`C` wang, `w` glans

"Toon" is de toon in `blender/B1/toonkaart_1x.png`, van 4 (licht) tot 1 (donker). Het lijf van deze sprite volgt de vertaling 4→`1`, 3→`2`, 2/1→`3`. Die vertaling gebruik ik hieronder als maatstaf voor het model.

## 1. Blinde indruk
Bekeken op 1×, 3× en 8×, naast Taillow, Pikachu, Trumbeak en Starly.

**Wat werkt:**
- Op 1× leest hij meteen als een gele vogel met een Pikachu-wang en zwarte kuiftoppen.
- Houding en massa zitten in dezelfde klasse als Taillow en Starly.
- De omlijning is grotendeels gekleurd (goudbruin aan de lichtkant, zwart aan de schaduwkant). Daardoor oogt hij zachter en minder 2D dan een volledig zwarte rand.

**Wat niet leest, of niet als Gen 3 oogt:**
1. **De kop is plat.** Het licht ligt als een band langs de bovenrand van de kop (r13–16). Het oog, de wang en de snavel staan in egaal basisgeel, en de rechterhelft is één schaduwvlak. Daardoor oogt de kop als een schijf, niet als een bal.
2. **De snavel heeft weinig contrast met de kop.** Het lichte hoorn `h` (helderheid 229) ligt naast basisgeel `2` (213). De snavel bestaat alleen dankzij de grijze rand en leest op 1× als een bleek hoorntje.
3. **De vleugel oogt als een "koekje" op de rug.** Het is een egaal bruine lob met vijf even felle roomwitte stippen, zonder licht/donker binnen de vleugel.
4. **De borst heeft een rechte wand.** De voorkant is van r30 tot r35 een recht stuk op x24, direct onder de hals. Daaronder volgt een regelmatige trap van 2-2-2. Het lijf leest daardoor eerder als een peer dan als een bol.
5. **De tenen zijn klein maar aanwezig.** Op 1× zie je een grijs "harkje". De verre voet staat hoger (r47) dan de nabije (r48–49): het perspectief is goed.
6. Het hooglicht op de dij (32–34, 40–42) leest op 3× los als een "vlekje". Het klopt met het model, zie §2.

## 2. Tegen het model (B1-render en toonkaart)

| onderdeel | oordeel |
|---|---|
| **kop (vorm)** | **Gelijk.** De omtrek ligt overal binnen 1 px van de render: links r12–17 en rechts r12–24 (achterpunten r12 en r17–18, render x40/x40, sprite x40/x41). |
| **kop (licht)** | **Wijkt af (72 cellen).** Zie de toelichting onder de tabel. |
| **kuif** | **Vorm gelijk.** Toppen (34,3) en (38,4), render (34,3) en (39,4). De naad (Jordi's lijn 1) ligt op de cellen van de render. **Licht wijkt af:** de lichte vlakken van beide kegels staan in `2`, waar de render toon 4 heeft. Achterste kegel: (35,9), (33–34,10), (32–33,11), (31–33,12), (31–32,13). Voorste kegel: (31,9), (30,10), (30,11). |
| **oog** | **Gelijk** in plaats en maat: 4×4 op x24–27 r18–21, render-middelpunt (25,9; 19,6). De glans (25,19) staat linksboven. De ankers in `3` op (24,18), (27,18), (24,21) en (27,21) geven een donkere ring die in het model niet bestaat: daar zit het oog in een licht gezicht. |
| **wang** | **Gelijk** (x24–28, r23–27; render x23–28, r23–27). `C` rechtsonder is in orde. |
| **snavel** | **Vorm gelijk.** Punt (14,17), render (15,18): 1 px verder, dat mag voor de leesbaarheid. **Licht wijkt af:** de toonkaart heeft een lichte rug (15,17), (16,18), (17,19) en daaronder toon 2 en 1 (r20–23, x17–20). De renderkleur van het lijf van de snavel is (144,140,114) ≈ `g`, de onderkant (67,62,48) ≈ `G`. De sprite heeft daar `h` tot en met r21. |
| **borst/buik** | **Licht gelijk** aan de toonkaart: ovaal x28–32 r30–35 (render x28–34), kinschaduw r29, dij (32–34, 40–42), schaduwsikkel vanaf x40/39. **Omtrek wijkt af:** r30–41 ligt 1–2 px vóór de render (render x25, 26, 26, 26, 26, 26, 27, 27, 28, 28, 28, 29; sprite x24, 24, 24, 24, 24, 24, 25, 25, 26, 26, 27, 27). Dat is bewust en Jordi vond het lijf van r4 "beter", dus dat laat ik staan. Wel: de render heeft een halsplooi van 2 rijen op x25 (r29–30), de sprite springt op r30 al naar x24. |
| **vleugel** | **Vorm gelijk.** Voorrand x33–34 (render x34), onderkant van de lob r34 x36–40 (render r33 x35, r34 x36, r35 x40). De stippen staan op de plekken van de render. **Licht wijkt af:** zie de toelichting onder de tabel. |
| **poten/tenen** | **Gelijk binnen 1 px.** Nabij been x31–32 (render x30–31,5), verre been x34–35 (render x33–34,5). Tenen: korte ovalen van 2 rijen op r48–49 (render r47,5–49), verre voet r47 (render r47–48). Elke teen heeft een donkere punt. |
| **staart** | **Gelijk:** punt (50,57), knobbel r47–49, licht links en donker rechts, zoals de render. |
| **licht/schaduw** | Lijf, staart en kuifnaad: gelijk. Kop, snavel en vleugel(stippen): wijken af, zie hierboven. |

**Kop (licht), toelichting:**
- In het model is het hele gezicht rond het oog licht: toon 4 op x20–30, r14–23. Basis (3) zit alleen in een dunne ring op x30–32. Toon 2/1 zit in een sikkel op de rechterrand (x33–38) en onder de kin (r24–28).
- De sprite heeft `1` alleen op het voorhoofd (r13–17). Het gezicht rond het oog en boven de wang staat in `2` (r16–23, x20–30).
- De schaduw `3` loopt onderaan 1–2 px te ver naar links: (32,20), (31,21), (30–31,22), (29–30,23), (29,24).
- Onder de snavelbasis staat `3` (22–23, 22–25), waar het model toon 4/3 heeft.

**Vleugel (licht), toelichting:**
- In de render vangt alleen de stip linksboven licht: (35,27), renderkleur (189,180,152). De andere stippen zijn gedempt beige:
  - (40,26): (132,124,102)
  - (37,31): (141,134,109)
  - (41,31): (116,109,88)
  - (42,35): (121,114,92)

  Die liggen allemaal bij `g` (150,140,116). De sprite heeft vier van de vijf stippen in fel `h`.
- De toonkaart heeft licht op de voorrand van de schouder: (34–35,29) en (34,30). De sprite heeft daar `b`.

## 3. Harde regels
| regel | oordeel | pixels |
|---|---|---|
| ≤ 3 tinten per groep | **PASS** | geel 1/2/3 (+4), vleugel l/b/d, staart r/l/b (+d), grijs h/g/G, wang c/C |
| contrast per stap | **PASS** | geel 244 → 213 → 179 (stappen 31 en 34, Taillow-klasse) |
| geen clusters < 3 px (behalve glans) | **PASS met kanttekening** | Wat overblijft is bedoeld: 1-px-lijnen (kuifnaad (32,10), (31,11), (30,12); vleugelstrook), oogpixels en teen A (27–28,48). Het blokje `b` (41–42,34) klopt met de toonkaart (toon 2/3). |
| geen banding / pillow shading | **FAIL (kop)** | Kop: het `1` ligt als een band van 2–3 px evenwijdig aan de boven- en linkerrand (r13 x25–27, r14 x23–29, r15 x21–29, r16 x20–24, r17 x20–21). Dat is randlicht in plaats van de vorm. Lijf: PASS (geen donkere rand rondom; de voorrand blijft `2`). |
| licht linksboven | **PASS** (overal), maar op de kop alleen als band (zie hierboven) | |
| zwart alleen aan de schaduwkant | **PASS** | `k` rechts en onder. Goudbruin `4` aan de lichtkant (kop, borst, kuiflijnen). Zwart bij de kuiftoppen is kleur (Pikachu-oor). (18,16) en (17,17) zijn het verre oog. |
| geen open randen | **PASS** | Volgens de controle 0 lichte kleur op de buitenrand. `g` op de rand alleen bij dunne delen (snavelrug (15–16,17), nabij been x31, tenen), dus pseudo-omlijning. |
| vloeiende curven | **FAIL (borst)** | Voorkant: x24 op r30–35 is een recht stuk van 6, dat direct na de halsinkeping (25,29) begint. Daarna volgt een regelmatige trap van 2-2-2 (r36–41). Kopomtrek links (4-2-2-1-1) en buikonderkant (3-5-6): PASS. |

## 4. Jordi's punten
| punt | oordeel |
|---|---|
| "volledig 2d, geen drie kwart, perspectief klopt niet" | **Niet ok (deels).** Silhouet, houding, verre oog (18,17) en de hoger geplaatste verre voet volgen het model. Maar de kop is met de lichtband plat belicht en leest als een schijf (reparaties 1–2). |
| "klauwen afgeknapt" | **Ok.** Er zijn twee tenen van 2 rijen met donkere punten (26,49) en (33,49), plus een verre voet (34–37,47) met punt. Het perspectief is in orde. |
| "shading niet goed" | **Niet ok.** Lijf en staart: ok, volgens de toonkaart. Kop: 72 cellen wijken af. Snavel en vleugelstippen: geen modellicht (reparaties 1–4). |
| "snavel weg" | **Deels.** De snavel staat er (r17–24, punt (14,17)), maar `h` naast het gele gezicht heeft weinig contrast. De render is daar grijs (reparatie 3). |
| "het lichaam moet echt bol" | **Deels ok.** Licht-ovaal, schaduwsikkel en dij volgen het model. De rechte wand op x24 onder de hals werkt de bolling tegen (reparatie 5). |
| krabbel lijn 1 (kuifnaad) | **Ok:** naad op (33,9), (32,10), (31,11), (30,12), dezelfde cellen als de render. |
| krabbel lijn 2 (achterkant kop) | **Ok:** (36,13) en (36,14) staan op de donkerste plek van de render. |
| krabbel boog borst/buik | **Ok:** rondere voorkant en buikonderkant r44–46. Omtrek 0 px gewijzigd sinds r4, waarvan Jordi zei: "lichaam is beter". |
| krabbel boog vleugelvoorrand | **Ok:** de lob eindigt op r34 x36–40, zoals de render (r33–35). |
| "kop rechts … hallucinatiewerk" | **Ok:** 7 px verschil met r2, alle 7 uitgelegd met de render (NOTITIES zone 1). |
| "het gaat vooral om afwerking" | Precies daar zit het: kop-licht, snavel en stippen. |

## 5. Oordeel: **NIET GOED**

Pose, silhouet, lijf, staart en poten volgen het model. Het werk zit in de afwerking:
- De kop is het enige grote vlak dat niet volgens de toonkaart belicht is, en juist de kop bepaalt of het geheel 3D leest.
- Snavel en vleugelstippen negeren het licht van de render.

## 6. Reparatielijst (alleen dingen die ik met het model kan uitleggen)

1. **Gezichtslicht als schijf rond het oog.** Zet `2` → `1` op deze cellen:
   - r16: x25–29
   - r17: x22–30
   - r18: x20–23 en x28–30
   - r19: x21–23 en x28–29
   - r20: x22–23 en x28–29
   - r21: x22–23 en x28
   - r22: x24–27
   - r23: x24

   Zet daarnaast `3` → `1` op (22–23,22) en (22–23,23). Zet de oogankers (24,18), (27,18), (24,21) en (27,21) van `3` naar `2`, als overgang tussen `k` en `1`. Het oog zelf blijft ongewijzigd.

   *Waarom dichter bij het model:* de toonkaart heeft op precies deze cellen toon 4. Het lijf van deze sprite gebruikt al dezelfde vertaling (4→`1`), dus de kop wordt daarmee op dezelfde manier belicht als het lijf. Het licht wordt een bal rond het oog in plaats van een band langs de rand. Dat haalt ook de FAIL bij banding weg.

2. **Schaduw op de kop als sikkel aan de rand.**
   - `3` → `2` op (32,20), (31,21), (30–31,22), (29–30,23) en (29,24).
   - `3` → `2` op (22–23,24) en (21–23,25), onder de snavelbasis.
   - `2` → `3` op (33,16) en (33,17).

   De ring `2` blijft dan op x30–32 staan, de sikkel `3` vanaf x33 (r16–20) en x31–32 (r21–23). De kinschaduw r26–27 blijft `3`.

   *Waarom dichter bij het model:* de toonkaart heeft op die cellen toon 3 (basis) of, op x33, toon 2. De donkere zone ligt in het model alleen op de rechterrand en onder de kin.

3. **Snavel met het licht van de render.**
   - (18,20), (19,20), (20,20), (19,21) en (20,21): `h` → `g`
   - (19,22), (20,22), (19,23) en (20,23): `g` → `G`

   De lichte rug `h` blijft op (16–17,18) en (17–19,19).

   *Waarom dichter bij het model:*
   - In de toonkaart is alleen de bovenrug van de snavel licht (toon 4 op (15,17), (16,18), (17,19)). r20–21 heeft toon 2 en r22–23 toon 1.
   - De renderkleuren zijn (144,140,114) ≈ `g` en (67,62,48) ≈ `G`.
   - De grijze snavel steekt dan af tegen het (na reparatie 1) lichte gezicht. Dat beantwoordt "snavel weg".

4. **Vleugel: alleen de stip linksboven fel, en een lichte schoudervoorrand.**
   - De stippen (39,26), (40,26), (40,27), (36,31), (37,31), (36,32), (37,32), (42,35) en (43,35): `h` → `g`. De stip (35–36, 27–28) blijft `h`.
   - (34,29), (35,29) en (34,30): `b` → `l`.

   *Waarom dichter bij het model:*
   - In de render is alleen de stip op (35,27) licht (189,180,152). De andere stippen meten 116–141, en dat is `g`. De sprite gebruikt `g` al voor de stip op (41–42,31).
   - De toonkaart heeft toon 4 op de vleugelvoorrand (34–35,29) en (34,30).
   - De vleugel krijgt zo het licht linksboven van het model, en de stippen blijven Jordi's stippen.

5. **De halsplooi 2 rijen, zodat de borst niet als wand begint.**
   - (24,30): `4` → transparant
   - (25,30): `2` → `4`

   *Waarom dichter bij het model:* de render-omtrek is r28 x23, r29 x25, **r30 x25**, r31 x26. De halsplooi is in het model 2 rijen diep voordat de borst naar voren bolt. Het rechte stuk op x24 wordt 5 in plaats van 6, en de curve loopt 2-5-2-2-2 in plaats van 1-6-2-2-2. De bolling blijft zoals Jordi die bij r4 "beter" vond.

6. **(Als 1–5 akkoord zijn; kop rechts is Jordi's zone.)** Geef de kuifkegels hun lichte kant:
   - achterste kegel: (35,9), (33–34,10), (32–33,11), (31–33,12) en (31–32,13): `2` → `1`
   - voorste kegel: (31,9), (30,10) en (30,11): `2` → `1`

   De naad `3` van lijn 1 blijft staan.

   *Waarom dichter bij het model:* de toonkaart heeft op al deze cellen toon 4. Met licht aan weerszijden van de naad worden het twee aparte kegels, en dat is precies wat Jordi met lijn 1 aanwees.

**Niet voorstellen** (niet uit te leggen met het model of al door Jordi beslist):
- de borstomtrek terugzetten naar de render (Jordi: lijf r4 "beter")
- de donkere voorrand van de toonkaart op de borst (r34–41, toon 2): dat zou pillow shading aan de lichtkant geven
- de vorm van de vleugel, de staart en de tenen
- de omtrek van kop rechts

Na de reparaties opnieuw keuren: kop op 1× naast Taillow, en controleren dat er geen nieuwe clusters < 3 px zijn.

Hulpbeelden van deze keuring (scratchpad, niet in de repo): `naast_1x.png`, `naast_3x.png`, `sp8.png` en `overlay.png` (sprite-omtrek over de render).
