# Picapau sprite_v2 kleur r5: notities (maker, 5 nov)

Basis: `kleur_r4`. Ik heb ronde 5 afgewerkt en niet opnieuw getekend. De kop rechts komt terug uit `kleur_r2`.

Bestanden:
- `teken.py`: r4 + kop rechts uit r2 + de wijzigingen per zone → `raster.txt`
- `bouw.py`: palet r4 (ongewijzigd) → `picapau.png` en `normal.pal`
- `controle.py` → `controle_uitvoer.txt`
- `krabbel.py` → `krabbel_over_r5.png`: Jordi's krabbel in magenta over r2 en over r5, 8x
- `closeup.py` → `closeup.png`: per zone 16x render | oud | r5, met blauwe lijnen om de 5 px
- `vel.py` → `vel.png`: 8x render | r4 | r5 | Taillow | Pikachu, plus 1x/2x
- `model_vs_sprite.png`

## Bevroren (0 px, bewezen in controle_uitvoer.txt)
Ongewijzigd t.o.v. r4:
- oog, wang
- snavel en verre oog (x13–23, r16–24)
- kop links van het oog
- borstomtrek (eerste pixel per rij, r29–45)
- vleugel (145 px)
- staart

Het palet is identiek. Totaal 855 px; 192 px gewijzigd t.o.v. r4.

## Zone 1: kop rechts (kuif, kruin, achterkant tot de nek)
**Werkwijze (Jordi):** de basis is r2, de versie waarop hij zijn krabbel tekende. Alleen op de plekken van zijn twee lijnen heb ik de sprite aangepast, en alleen zoals de render en de toonkaart daar laten zien. Mijn eigen r4-ontwerp in deze zone (bredere kegels, lobben, kopschaduw) is volledig weg.

**De zone:**
- rij 3–11 helemaal (beide kegels en de zwarte toppen)
- rij 12 vanaf x25
- rij 13–24 vanaf x29 (rechts van het oog van r2, x25–28)
- wangpixels blijven r4

**Naad:** op 3 pixels net buiten de zone sluit het hooglicht van het r4-voorhoofd aan op dat van r2: (28,14), (27,15) en (28,15) worden `1`. Anders zou er een losse 1-pixel blijven.

**Verschil met r2 in de zone: 7 px.**

**Terugrekening van de krabbel:** de omhullende van de r2-sprite in zijn screenshot is x13–50 → 1047–1338 px en y3–57 → 45–465 px. Dat geeft schaal 7,68/7,65 en offset (947, 22). De strepen zijn de pixels met helderheid < 45 in het rechterpaneel.
- **Lijn 1 (schuin):** van (34,9) naar (30,13).
- **Lijn 2 (verticaal):** x≈35,8–36,3, van r10 tot r15.

Beide staan in `krabbel_over_r5.png`.

### Lijn 1: (34,9) → (30,13)
- **Render (toonkaart, tonen 1 donker … 4 licht):**
  - r9: x30–31 licht (voorste kegel), x32–33 donkere naad, x34–35 licht (de achterste kegel, belicht), x36 schaduw.
  - r10: x29–30 licht, x31–32 naad, x33–34 licht.
  - r11: x29–30 licht, x31 naad, x32–33 licht.
  - r12: x30 naad, x31–33 licht.

  De voorste kegel valt dus met een schuine naad óver de achterste kegel. Die naad loopt van de inkeping tussen de kegels schuin naar linksonder tot op de kruin, en rechts ervan is de achterste kegel belicht.
- **r2:**
  - De naad stond alleen in r9: (33,9) `3` en (34,9) `4`. Daaronder liep alles door in één `2`-vlak, waardoor voorste kegel, achterste kegel en kop samensmolten.
  - De achterste kegel stond in r9–10 in schaduw (`3`), waar de render hem belicht.
- **Veranderd (5 px):**
  - Naad doorgetrokken in donker geel `3`: (32,10), (31,11) en (30,12). Smal, en hij loopt dun uit naar de kruin.
  - Achterste kegel belicht: (35,9) en (34,10) van `3` naar `2`.
- **Waarom dichter bij het model:** de naad staat nu op dezelfde cellen als in de render, en de belichte achterste kegel rechts ervan geeft net als in de render twee aparte kegelvormen in plaats van één gele massa. (34,9) blijft `4`: dat is de buitenrand (de inkeping erboven is transparant).

### Lijn 2: x35–36, r10–15
- **Render:** donkerste toon (1) op x36 in r11 en r13–15 en op x36–37 in r15. Dat is de schaduwkant achter op de kop, waar de achterste kegel en de achterpunt van de kop loskomen. Rechts ervan is lob A in r12–13 weer lichter (toon 3).
- **r2:** x35–38 was in r12–15 één egaal `3`-vlak, dus geen scheiding tussen de kop en wat erachter ligt.
- **Veranderd (2 px):** (36,13) en (36,14) van `3` naar `4`, de donkerste tint uit de gele groep.
  - Kort en dun uitlopend: r12 en r15 blijven `3`.
  - In r10–11 valt Jordi's streep samen met de bestaande buitenrand (k op x36), dus daar is niets toegevoegd.
- **Waarom dichter bij het model:** de render heeft precies daar zijn donkerste plek. Daarmee leest de achterkant van de kop als een eigen ronde vorm met de kuif erachter, en niet als één rechte rand die naadloos in de kuif overgaat.

**Niet veranderd, uit twijfel:** de buitenomtrek rechts (r12–24) en de bruine randpixels van r2, (37–39,12), (38,16) en (39–40,17). De render geeft daar geen eenduidige pixels die anders moeten.

## Zone 2: vleugel (de opdracht vroeg om hem groter te maken; niet gedaan, met bewijs)
- **Render, gemeten in pixels:**
  - Wing-labels in `bron/bron_labels.txt`, plus de kleuren in `B1/b1.png` (bruin ≈ (70,53,36), olijf ≈ (150,140,80)).
  - r25–34: de schouder, x34–45, 10 px breed.
  - Vanaf r35 een strook van 3–5 px: r36 x44–46, r38 x44–47, r40 x45–48, r42 x45–49.
  - Bijvoorbeeld (40,38) = (130,121,65), olijf: dat is het lijf in de schaduw, geen vleugel.
- **r4:** valt samen met de V-cellen. 112 van de 137 V-cellen liggen in de vleugelkleuren; de overige 25 zijn de zwarte buitenrand rechts, die er in r4 al staat.
- **Veranderd:** niets.

  Een grotere vleugel (9–10 px tot over de staartbasis) zou verder van het model af staan. De vleugel lijkt in de render groter omdat het lijf ernaast donker olijf is (zie zone 3). Wil Claude of Jordi toch een grotere vleugel, dan is dat een ontwerpkeuze buiten het model; graag eerst bevestigen.

## Zone 3: lijfvolume (r29–43), volgens `blender/B1/toonkaart_1x.png`
- **Render/toonkaart:**
  - Licht (4) op de bolling van de borst: x28–34, r30–35, midden ±(31,32).
  - Slagschaduw onder de kin: r29 x25–29.
  - Basis (3) in het midden en aan de voorkant.
  - Schaduw (2) vanaf x40–41 tegen de vleugel (r35–38), daarna vanaf x39 → 37 → 36 (r40–42).
  - Een lichte dij-bult: x32–34, r40–42 (render (33,42) = 173 tegen 150 eromheen).
  - Een donkere naad vóór de dij: x28–30, r40–41.
  - Donker onderaan de buik: r43–45.
- **r4:**
  - Het hooglicht stond te ver links en te klein (x26–28).
  - Het schaduwvlak begon al op x33–34, waar de render nog basis heeft. Het lijf was daardoor twee grote vlakken, half licht en half schaduw.
  - Geen kinschaduw, geen dij.
- **Veranderd (alleen binnenkant; de omtrek is 0 px gewijzigd):**
  - Hooglicht `1` als ovaal op x28–32, r30–35.
  - Kinschaduw `3` op r29 x26–29.
  - Basis `2` breed in het midden.
  - Schaduw `3` als sikkel vanaf x40/41 (r35–38), daarna x40 → 39 → 37 → 36 → 35 naar onder.
  - Dij-bult als klein hooglicht `1` op (32–34, 40–42), met een korte boog in schaduwgeel ervoor: (28–29, 40–41) en (29,42).
- **Waarom dichter bij het model:**
  - Elk vlak ligt nu op de plek van dezelfde toon in de toonkaart.
  - De bolling van de borst krijgt zijn licht waar de render het heeft.
  - De schaduw zit, zoals in de render, aan de vleugelkant en onderaan in plaats van over de halve buik.
  - De dij is een eigen bult.

## Zone 4: tenen
- **Render:**
  - Nabije voet: twee korte ovale tenen, x25–29.5 (r47.5–48.5) en x28.5–33 (r48–49).
  - Verre voet: één oval, x33–38 (r47.4–48.1).
- **r4:** de nabije tenen waren lijnen van 6 en 4 px (r48 x27–32, r49 x32–35).
- **Veranderd (16 px in r47–49):**
  - Teen A: (27–28,48) `g` + (26,49) `k` punt + (27–28,49) `G`.
  - Teen B: (30–31,48) `g` + (30–32,49) `G` + (33,49) `k` punt.
  - Daartussen (29,48) `G` als scheiding.
  - De verre voet blijft (34–37,47) met donkere punt.
- **Waarom dichter bij het model:** twee korte ovaaltjes van 2 rijen hoog, elk met een donkere punt, op de plekken van de render-tenen. Geen lange strepen meer.

## Render ↔ r5 per onderdeel (model_vs_sprite.png)
- **Kop:** links gelijk aan r4. Rechts is het r2 + Jordi's twee lijnen. Wijkt af: de buitenomtrek rechts is die van r2 (zigzag van r2).
- **Kuif:** r2-kegels. De naad tussen de voorste en de achterste kegel volgt nu de render (lijn 1). Wijkt af: de kegels zijn op 64 px smaller aan de basis dan in de render (r2-maat, bewust teruggezet).
- **Oog:** gelijk (bevroren).
- **Wang:** gelijk (bevroren).
- **Snavel:** gelijk aan r4.
- **Borst/buik:** licht, schaduw en dij volgen de toonkaart. De omtrek steekt bewust tot 2 px vóór de render uit.
- **Vleugel:** gelijk aan de render (zie zone 2).
- **Poten/tenen:** gelijk in plaats. De tenen zijn korte ovalen zoals in de render.
- **Staart:** gelijk (bevroren).
- **Licht:** volgt de toonkaart.

## Controle (controle_uitvoer.txt)
- Lichte kleur op de buitenrand: 0. Losse pixels: 0. Alleen-diagonaal verbonden: 0.
- **Tintclusters < 3 px:**
  - In het r5-werk alleen teen A, (27–28,48): het teentje zelf.
  - In de kop-rechts-zone de 1-px-lijn van lijn 1 (bewust een lijn) en r2-pixels.
  - Verder alleen in bevroren delen (oog, snavel, vleugelstippen).
- **Buiten het silhouet:** 53 px, maximaal 2 px.
- Niet-omlijningskleur op de rand: alleen de dunne delen in `g` (snavelrand, nabij been, tenen).

## Eerlijk
- Het lijf heeft nu drie niveaus, maar het `2`-vlak in het midden blijft groot. De keurder moet beoordelen of het "echt bol" genoeg leest.
- Met de kop rechts terug op r2 komt de r2-zigzag in de omtrek ook terug. Die heb ik op Jordi's aanwijzing niet aangeraakt.

## Lessen
- Een krabbel terugrekenen via de omhullende van de sprite in de screenshot (schaal ≈ 7,7) gaat in één stap. Filter de sprite-omlijning eruit met helderheid < 45 (Jordi's stift is zwarter dan `k`).
- Controleer een opdracht eerst tegen de bron. De "grote vleugel" bleek op pixelniveau olijf lijf in de schaduw (render (40,38) = (130,121,65)). Meten met kleurwaarden voorkomt dat je verzint.
- Kop-rechts terug naar r2 met een masker. De zichtbare naad met het r4-voorhoofd los je op met 3 pixels hooglicht net buiten de zone.
