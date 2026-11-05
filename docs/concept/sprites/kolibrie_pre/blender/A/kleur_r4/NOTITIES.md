# Kolibrie pre-evo – kleur r4 (maker)

Jordi over r3: "het nieuwe oog is geen pokemon oog" · "rechts vind ik wel iets beter, maar nog steeds erg slordig shading werk, op hoofd, vleugel etc, nog niet zoals andere pokemon sprites" · "al vind ik ook de poten rechts nog niet ideaal" · "kijk vooral naar de bronnen".

Bronstudie: `STUDIE.md`. Werkwijze: alle pixels binnen de omtrek met de hand opnieuw geschreven in `rijen.txt` (y, x0, pixels; per kleurzone, met `toonkaart_8x.png` ernaast), `bouw.py` → `raster.txt` + `kolibrie_pre.png` (snavel pixel voor pixel uit r3), `palet.py` → `normal.pal`, `controle.py`, `ogen.py` → oogvarianten, `vel.py` → `vel.png`. 179 px gewijzigd t.o.v. r3.

## Controle (`python3 controle.py`)
- **alpha-diff met `kleur_r3/silhouet_r3.txt`: 4 px, alle in de toegestane zones**: (45,42) spijkertje weg; (28,45), (29,45), (31,45) erbij = donkere onderrand van de teentjes ((30,45) bestond al). Daarbuiten 0. 605 px (was 603). Nieuwe omtrek: `silhouet_r4.txt`.
- Snavel: 0 px afwijkend in vorm; kleur alleen oude `A` (64,56,82) → `2` (70,52,104), vrijwel gelijk, omdat `A` nu de donkere iris is.
- Open randen: 0. Schaduwkant rechts/onder niet zwart: 0.
- "Losse" pixels die het script meldt zijn bedoeld: de kapselout-diagonaal (26,14)(27,15)(28,16), de glans in het oog (22,18), de knik in de nekplooi (29,25), de vleugelhoek (38,27) en de veerstreepjes (35,36)(36,37)/(38,41)(39,42) (diagonale streepjes van 1 px per rij).
- Palet: 16 kleuren (index 0 transparant), niet groter geworden.

## Palet (wijzigingen t.o.v. r3)
- `A` (was snavel-donker, maar 7 px) → **iris smaragd donker (52,150,108)**; `8` → **iris smaragd licht (116,214,160)**. Verhouding licht/donker zoals Latias' goud (B/D). Snavel-donker is nu `2`.
- Rest gelijk: lila 5/4/3/2, buik 7/6 (schaduw via 5/3), kap en vleugel B/E, poot C/D/9.

## Per opdrachtpunt
1. **Schaduw opnieuw** (toonkaart als gids; toon 3/2/1/0 → per zone licht/basis/schaduw/diep):
   - *Kop*: voorhoofd en wang in één groot vlak `5` (licht valt hier volgens de toonkaart vol), `4` als ring onder/achter het oog, schaduwsikkel `3` onder-achter het oog naar de nek; kap één vlak `B` met een smalle `E`-sikkel aan de achterkant en een zwarte rand. Geen losse `4`-pixels meer in het `5`-vlak.
   - *Hals*: keel wit `6` als één vlak; alleen een kleine plooi `5` bij de inkeping links (21–22,27) en rechts tegen de nek; slagschaduw van de kop op de schouder `3` met een tapse `2`-plooi (30–32,23)→(28,25).
   - *Lijf*: buik `6` als grote schijf met klein hooglicht `7` (7 px) linksboven; schaduwsikkel `5` linksonder langs de buik, `3` als één groot vlak onderaan, `2` alleen als slagschaduw onder de vleugel. Flank `4` tussen buik en vleugel; buikrand bolt nu uit (x29 op rij 32–33) in plaats van een rechte verticale grens.
2. **Oog: Latias** (`graphics/pokemon/latias`, x12–17 y17–22), pixel voor pixel, op x21–25 y16–21 (1 rij hoger dan r3, de bron is 6 hoog). Kleuromzetting: rand 6→`2`, iris donker B→`A`, iris licht D→`8`, pupil 3→`1`, glans C→`7`, oogwit C en licht 4→`6`, schaduw 5→`3`, gezicht A→huidkleur `5/4`. Varianten op 8× (bron naast resultaat in de kop): `oog_latias_8x.png`, `oog_combusken_8x.png` (Combusken x29–33 y18–22), `oog_skarmory_8x.png` (Skarmory x9–14 y25–27), samen in `ogen_8x.png`. Gekozen: Latias (enige met glans én oogwit én twee iristinten; Skarmory heeft geen glans, Combusken is kleiner en kijkt boos door de schuine rand).
3. **Pootjes**: nabije poot (28–29,43) `D` met teentjes `C`/`D` (28–29,44), verre poot donkerder (31–32,43) `9`, teentje (31,44) `9`; zwarte scheiding (30,43–44) en zwarte onderrand op rij 45.
4. **Vleugel**: dekveren als één rond `B`-vlak (rand loopt 38,38,38,37,37,36), onderrand gekarteld in twee tongen (32–33 tot rij 35, 35–36 tot rij 34); slagpennen `E`; één tapse lichte veerrij `B` (35,36)(36,37)(36,38) en een tweede bij de punt (38,41)(39,42); onder-/voorrand van de vleugel `2` (geen zwart), achterrand zwart. Bovenrand zonder lijn (kleurgrens `B` tegen lila `4`).

## Checklist §0
1. 3/4 links-voor: ok (ongewijzigde omtrek). 2. Ledematen: twee pootjes, staart, vleugel geteld: ok. 3. Geen nieuwe rechte lijnen in de omtrek: ok; buik-flankgrens nu gebogen. 4. Oog: bovenlid `2`, iris twee tinten, glans, oogwit; niet opgeplakt (rand alleen boven/voor/onder, zoals de bron). 5. Silhouet: ongewijzigd. 6. Formaat: 605 px. 7. Pose: ongewijzigd.

## Eerlijke zwakke punten
1. **Oog op 1×**: leest als een groen stipje met een lichte streep erachter; het oogwit (6) is een kolom van 4 px en kan op 4× als "zijwaarts kijkend" of te realistisch lezen. Dat is hoe Latias het doet, maar op een lila gezicht (in plaats van Latias' rode masker) is de rand minder duidelijk.
2. **Flank** `4` tussen buik en vleugel loopt als een lange smalle baan van schouder tot onderkant; het is een kleurzone van het model, maar op 4× leest hij bijna als een streep.
3. **Schouder/nek** (x29–37, y23–26) blijft het drukste stuk: plooi `2`, schaduw `3`, schouderlicht `5` (3 px) en bovenrand `2` op kleine ruimte.
4. **Pootjes** zijn door de omtrek klein (2×2 en 2×1 met onderrand); teentjes lezen pas op 4×, op 1× zijn het twee oranje stipjes, nu wel met donkere onderrand.
5. **Contrast** is lager dan bij Taillow (veel lichte lila); de sprite leest zacht, vooral op lichte achtergrond.
6. Geen tweede frame, rug, icoon of shiny (niet gevraagd).

## Lessen
- Een toonkaart van het 3D-model per 8×8-blok uitlezen naar een tekstraster (0–3) en die naast het raster leggen maakt schaduw plaatsen per rij controleerbaar; vertaal per kleurzone (wit: 7/6/5/3, lila: 5/4/3/2, kap/vleugel: B/E/2/1) in plaats van één ramp over de hele sprite.
- Gekleurde-iris-ogen in Gen 3 zitten bij Latias/Latios, Combusken, Skarmory, Noctowl, Hoothoot, Treecko, Celebi; Latias (6×6) is de beste bron voor een vriendelijk 3/4-oog met glans, oogwit en twee iristinten.
- Een paletplek vrijmaken door een bijna gelijke kleur samen te voegen (snavel `A` ≈ `2`) kost visueel niets en geeft een tweede iristint.
- `palet.build` in het bouwscript zelf aanroepen; anders render je per ongeluk een oude PNG.
