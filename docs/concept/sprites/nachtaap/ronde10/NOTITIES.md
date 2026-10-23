# Nachtaap (Psychic-starter fase 1), ronde 10: reparatieronde (basis ronde 9)

Geen herontwerp: lijf en kop zijn gebleven (Jordi tevreden). Uitgevoerd: punt 1 t/m 5 uit `ronde9/KEURING.md`, Jordi's kleur- en uitdrukkingswensen en een deel van polijstpunt 6. Alles met de hand als tekstrijen (`bron/delen.txt` + `bron/patches/*.txt` via `zet.py`, gebouwd met `bouw9.py`); de nieuwe spiraal is als heel blok met de hand getekend. Vergelijking: `compare.png` (ronde 9 en 10, beide frames, 3× en 1× op licht en donker).

## Wat er veranderde
| Punt | Ronde 9 | Ronde 10 |
|---|---|---|
| 1. Oor en Nazca-krul | De krul zat achter het oor, met 2 px zwart naast elkaar, een gaatje dat als oogje las en een binnenkrul die aan de buitenring vastzat ('9') | Nieuwe spiraal (x 44–56, y 21–35), met de hand getekend. Kolom x 43 is in beide frames helemaal leeg, dus er zit 1 px lucht tussen oor en krul. De buitenring is 3 px en de steel 4 px. De binnenkrul is 3 px breed (O-v-K), stijgt vanaf de onderkant op en eindigt in een vrij, rond kopje (x 48–51, y 26–28) met overal ≥ 1 px lucht. Er zit geen gaatje meer in. Op 1× leest hij als een spiraal |
| 2. Ogen | Bijna-zwarte pupil (K), even zware ring rondom, afgerond vierkant, verre oog een kopie | De pupil is nu **diep pruim** (76,16,72), op de vrije paletplek 14. De iris verloopt van donker boven (m, a) naar licht onder (A), met een donkere onderrand. Het **bovenlid** is de donkerste lijn (K), zwaarst aan de buitenhoek met m aan de binnenhoek. De rijen zijn 5-7-7-7-7-5-3, dus het oog is rond. Het verre oog is 6 breed met een lid naar rechts en 1 px glans, het nabije 7 breed met 2–3 px glans |
| 3. Verre arm en flank | Arm even breed en licht als de nabije, met een basistintkolom aan de schaduwkant | Flank x 30–31 (y 42–50) in schaduwtint V, met een K-scheiding op x 32. De arm is 3 px breed (V V K, 1 v op de schouder) en de schouder heeft een bovenrand. Het handje is vooral crème-schaduw met 1 px C |
| 4. Open randen | (44,28), (49,32), (37,48), (20,54), (33,41) en in frame 2 (36,46) | Het staartpuntje en het spiraalgat zijn vervallen met de nieuwe spiraal. Het staarteind loopt achter de verre arm door tot x 36 en sluit met K, dus er is geen gaatje meer tussen arm en staart, ook niet in frame 2. (20,54) is K geworden, (33,41) heeft een K-rand erboven. `bouw9.py` meldt geen open randen |
| 5. Kinschaduw frame 2 | Weg: de kop zakte op de basistint | Nieuw deel `kinschaduw` (x 22–29, dy2 = +1): in frame 1 valt het samen met de bestaande D-rij en in frame 2 schuift het mee onder de kin |
| 6. (polijsten, deel) | L-streep over de hele nabije arm | Het hooglicht staat alleen nog op de schouder (y 40–43). De armvorm zelf (pols, elleboog) is niet aangepast |
| 7–8 | | Niet gedaan: het voorhoofd en de knie/voet vragen om vormwerk aan de kop en het lijf, waar Jordi tevreden over is |

**Kleuren (Jordi):** het violet heeft dezelfde tint (±265°) maar is verzadigder. De basis gaat van (160,128,200) naar **(156,112,216)**, verzadiging 0,36 → 0,48, met een helderheid gelijk aan Aipom. De schaduw wordt (118,76,172) (0,56), de omlijningsbasis (80,44,128) en het hooglicht (194,160,242). Het crème gezicht is lichter: basis (252,236,206), schaduw (224,194,160) en hooglicht (255,252,238). In totaal 14 kleuren + transparant; plek 15 is vrij.

**Uitdrukking (Jordi):** de glimlach is weg. Er staat nu een klein neutraal mondje van 2 px in crème-omlijning (E). Met het vlakke, zware bovenlid, de kleine pruimpupillen met iris rondom en een blik die schuin naar links-voor gaat, kijkt hij stil en starend. De vorm blijft lief, de blik is net iets vreemd ("ziet er eng uit, maar geneest"). Twee tussenstappen vielen af: opgewipte flicks lazen als verdrietig (p1), en een lid plus een volle donkere irisrij las als halfdicht en slaperig (p2). Zie `bron/patches/`.

## Checklist §0 (SPRITING.md)
1. **Lijf en blik diagonaal:** de blik staat nu 3/4 naar links-voor (beide pupillen 1 px naar links). Het lijf is deels 3/4: de verre arm is smaller en in schaduw, de verre flank donker en het verre oog smaller. **Niet volledig:** de zithouding en de middenstreep op de kop staan frontaal. Dat bleef zo omdat dit een reparatieronde is en Jordi tevreden is over lijf en kop. **Voor Jordi:** als hij het lijf ook schuin wil, wordt het een vormronde (kop en romp 1–2 px naar rechts draaien, middenstreep naar x 25–26).
2. **Geteld en verbonden:** 2 oren, 2 ogen, 1 mond, 2 armen met handen, nabije knie en voet, verre voet en 1 staart. De staart zit vast (achter de verre arm) en de spiraal is één doorlopende band. Ok.
3. **Rechte lijnen:** de bovenrand van de kop (8 px) en de onderkant waar hij zit zijn ongewijzigd. De linkerkant van de spiraal is 5 px en de verre arm loopt 10 px recht: het is een smalle buis achter het lijf. Een knik zou de steel raken. Verder ok.
4. **Ogen geïntegreerd:** bovenlid, gekleurde iris en pupil, glans en roze reflectie onder, en een oogkas in crème-schaduw. Het verre oog is geen kopie (6 breed, eigen lid en glans). Ok.
5. **Silhouet op 1×:** zittende aap met grote ogen en een spiraalstaart. De krul leest nu als spiraal, niet meer als '9'. Ok.
6. **Formaat:** 1033 px (ronde 9: 1041). Aipom 856, Mankey 872, Treecko 967. Iets groot voor fase 1, maar niet blokkerend (keuring r9).
7. **Pose:** zittend en vrij symmetrisch. De twee armen zijn nu wel ongelijk (de verre arm is donker en smal) en de nabije knie staat naar voren. Meer beweging (gewicht op één hand, kop scheef) zou een vormronde zijn: voorstel voor Jordi.

## Bestanden
- `anim_front.png` (64×128, 2 frames), `normal.pal`, `compare.png`.
- `bron/delen.txt`, `bron/palet.txt`, `bron/raster_f1.txt`/`raster_f2.txt`, `bron/bouw9.py`, `bron/zet.py`, `bron/patches/p1`–`p6`, `bron/vergelijk10.py` (python3 bron/vergelijk10.py <nachtaapmap>).

## Oordeel Jordi (23 okt)
Pose goedgekeurd: "hij lijkt dynamisch genoeg zo, we zitten er niet frontaal op." Geen vormronde nodig.
