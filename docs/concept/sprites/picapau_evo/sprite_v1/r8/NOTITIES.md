# Picapau-evolutie: sprite r8 (alleen de snavel, varianten A en B op r7)

r7 (`../r7/`) blijft staan. Alles buiten de snavelzone is bevroren op r7.

## Jordi letterlijk
- Over r6: **"ik wil beide krullen bovenop naar achteren en die snavel is geen snavel, kijk bijv naar fearow of andere vogels, echt lelijk. Voor de rest is die wel prima. Alleen de buik is niet meer mooi ovaal. De pose is prima"**
- Over de snavel van r7: **"niet mooi, past niet bij het hoofd en is niet zo mooi als bij normale pokemon sprites"**

## Diagnose van r7 (coördinator)
- (a) Een lange dunne stok die los voor een ronde, mollige kop steekt, met een smalle voet. Hij groeit dus niet uit het gezicht.
- (b) Zes horizontale stroken maken hem streperig en technisch. Echte sprites tekenen een snavel als één volume, met 2–3 tinten die de vorm volgen.

## Werkwijze
- `basis.txt` = de r7-tekening zonder het snavelblok.
- `snavel_A.txt` en `snavel_B.txt` zijn met de hand ingetypt.
- `maak.py A B` plakt ze aan elkaar tot `tekening_<V>.txt` en draait daarna `zet.py`, `bouw.py`, `controle.py` en `diff.py`.
- Uitvoer: `raster_<V>.txt`, `picapau_evo_<V>.png`, `controle_uitvoer_<V>.txt` en `diff_uitvoer_<V>.txt`.
- `platen.py` maakt `kop_A.png` en `kop_B.png` (kop op 16× naast Picapau, Staraptor en Pidgeot op 16×) en `vel.png` (1× en 8×: A, B en r7).
- `ref_snavels.py` maakt `ref_snavels.png` (8×, met r7, A en B erbij).
- Het palet is gelijk aan r7 (`normal.pal`).

## Bevroren: bewijs
- `diff_uitvoer_A.txt` en `diff_uitvoer_B.txt`: **0 px verschil buiten de snavelzone** (x6-22, y7-15), in het raster én in de png.
- Binnen de zone veranderen 53 px (A) en 33 px (B); de lijst per pixel staat in die bestanden.
- Waar de snavel kleiner is dan in r7, is de verre vleugel weer dicht gemaakt met de vleugelregels uit r6.

## Controle (beide varianten)
- Geen lichte kleur op de buitenrand.
- Geen losse pixels.
- Geen tintclusters kleiner dan 3 px.
- 15 kleuren + transparant, 1759 px.

## Variant A: familie (snavel van Picapau)
**Picapau** (`../../../picapau/af/picapau.png`, rij 17-24), cel voor cel:
```
r0  G g g k G        punt linksboven, bovenkant g
r1    G a a g        licht a
r2      G a a a g
r3        G g g g G
r4        k g g g G  schaduw onder, zwart alleen aan de schaduwkant
r5-6        k G G G
r7            k G G
```
**r8A**:
- Dezelfde opbouw en tinten, ±1,25× breder, 10 px lang (x12-21).
- Punt linksboven (2 px G), bovenkant g, licht a als wig in het midden-boven, schuine onderrand in G en schaduw G onder.
- Licht open: een mondspleet k van 4 px, de mondhoek 3 px rood en een ondersnavel van 3-4 px (korter).
- Net als bij Picapau loopt de grens tussen snavel en kop schuin. Het gezicht (oranje 1/2) komt in rij 8-10 naar voren en de snavel groeit eruit.
- De voet raakt de kop van rij 8 tot 14 (7 rijen), zonder gat of zwarte voeg.

**Zwakke punten A:**
1. **Klein**: op 1× is het een klein grijs wigje. Hij leest als snavel van dezelfde familie als Picapau, maar heeft weinig massa bij deze grote kop.
   - De gevraagde 1,3–1,5× paste niet in de hoogte: Picapau's snavel is 8 rijen hoog, en hier zit tussen oog en keel maar 7 rijen.
   - Daarom alleen in de lengte vergroot.
2. **Richting**: hij wijst iets omhoog (punt linksboven zoals Picapau), naar de verre vleugel. Grijs tegen bruin leest wel, maar de punt plakt aan de vleugel.
3. **Ondersnavel**: erg kort, op 1× nauwelijks zichtbaar. "Licht open" leest vooral als een donker streepje.
4. **Bovenrand**: bovenop ligt (18,8) als donkere kopomlijning (4) tussen snavel en gezicht, zoals Picapau's k op die plek. Op 16× is dat een klein donker hoekje.

## Variant B: Gen 3-stijl (Staraptor/Pidgeot)
- Stevig, kort en spits, 10 px lang (x12-21). De voet is 7 rijen hoog (rij 8-14) en loopt zonder voeg in het gezicht over.
- **Bovenrand** gebogen (G, trappen 2-1-1-1). De punt maakt een haakje van 2 px over de ondersnavel heen.
- **Licht**: a als vlek op de bovensnavel bij de voet (geen band), g in het midden, G aan de rand en onder.
- **Licht open**: een mondspleet k tot in de haak. De ondersnavel is korter (vanaf x13/14): g boven, G schaduw, met een zwarte onderrand aan de schaduwkant. Mondhoek rood.

**Zwakke punten B:**
1. **Wangvlek**: die raakt de snavel niet. Hij ligt op x25-29, buiten de snavelzone (x ≤ 22). Daarvoor moet de bevriezing van het gezicht open; ik heb dat niet gedaan.
2. **Mondspleet**: een rechte zwarte lijn van 6 px. Op 8× lijkt dat een beetje een grijns. Staraptor heeft een kortere.
3. **Zwart**: de onderrand onder de ondersnavel (rij 14) is zwart over 2 px, naast G. Dat mag volgens de regel (schaduwkant), maar het is wel zwart en G op één rand.
4. **Kop**: de bovenrand begint direct onder het verre oog (rij 8). De voet is daardoor hoog, maar het verre oog lijkt op de snavel te staan.

## Mijn oordeel (eerst blind, daarna naast de referenties)
- **B** leest op 1× het meest als een echte Pokémon-vogelsnavel en past bij de ronde kop.
- **A** past qua familie het beste bij Picapau, maar is op deze kop klein.
- Allebei zijn ze minder streperig dan r7 en groeien ze uit het gezicht.
- Er is nog geen onafhankelijke keuring gedaan.

Er is niets gecommit en niets verwijderd (alleen r8-kopieën die ik zelf net had gemaakt, vóór het werk).
