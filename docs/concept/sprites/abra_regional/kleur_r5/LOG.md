# Regionale Abra, kleur_r5 (maker-agent, 13 nov)

Uitgangspunt: `../kleur_r4/abra_r4.png`. Opdracht = Jordi over r4 (letterlijk):
"linker oog mag iets diagonaler, is nu teveel een horizontaal streepje. desnoods doe je de linkerpixel 1 omhoog, kijken hoe dat eruit ziet. Verder is het lijnen werk niet overal even mooi. Linkerarm is veel te recht. rechter oor heeft een rare witte pixel en ook het hoofd plus rechts de staart hebben teveel rechte lijnen, controleer de hele sprite kritisch daarop en kijk naar de vorm van het model"

## Reproduceren
`python3 maak_r5.py` → `abra_r5.png` (oog A) en `abra_r5_oogB.png` (`-v` geeft elke pixel); `python3 maak_vel.py` → `abra_r5_8x.png`, `vel.png`, `closeup.png`.
Meten: `python3 ov.py PNG x0 y0 x1 y1 Z uit.png` (sprite | model met spriteraster, in de tempmap), `python3 lum.py x0 x1 y0 y1` (helderheid van de 4 modelpixels per spritecel), plus `../kleur_r3/cel.py`.
Spritepixel (x,y) = natief modelblok vanaf (2x−1, 2y−14).

**Meetvalkuil gevonden:** de r1-scripts tellen modelpixels met min(RGB) ≥ 215 als achtergrond. Het hooglicht van het model is 212–223, dus `cel.py`/`naast.py` tonen hooglicht soms als `.`. Zo is in r1 een gat (31,18) in het rechteroor beland waar het model hooglicht heeft. Lees daarom twijfelgevallen met `lum.py` (echte waarden; achtergrond ≈ 253).

## Diff t.o.v. r4: 42 pixels (oog A), 42 (oog B)
oog 2 · oor 9 · kop 11 · kin 2 · linkerarm 8 · staart 10.
**Silhouet: 3 pixels**, alle richting de modelvorm:
- (31,18) erbij: het modelblok is volledig hooglicht (213–218), geen achtergrond (zie de meetvalkuil);
- (55,51) en (55,57) weg: het modelblok is half (de modellijn ligt op de linker helft); zo wordt de buitenrand van de staart rond in plaats van 7 px recht.

## Per punt
### 1. Linkeroog (Jordi: "iets diagonaler")
Het model meet (lum.py) een schuin streepje van (22,30) via (23,30) naar (23,31) (donker 52/12/10/7), dus schuin naar rechtsonder, richting de snuit.
| variant | pixels | |
|---|---|---|
| **A (in abra_r5.png)**: Jordi's voorstel | (22,30) K→b, (22,29) b→K | oog = (22,29)+(23,30). Zelfde richting als het model, 1 px hoger begonnen. Los van de kaak (b op (23,31)) |
| B: modelplek | (23,30) K→b, (23,31) b→K | oog = (22,30)+(23,31), precies de modeldiagonaal. **Let op:** (23,31) raakt de kaaklijn K (23,32), dus het oog plakt weer aan de kaak (het punt van de keurder in r3). Zie closeup |
Vrijgekomen pixel = b: modelblok licht (129–196), buren b.

### 2. Rechteroor (Jordi: "rare witte pixel")
De rare pixel was **(34,16) b**: een losse lichte pixel bij de oorpunt, ingeklemd tussen L (33,16), K (34,15) en K (35,16). Het model heeft daar een lichte strook langs de linkerrand en een binnenlijn als boog; de r4-oorlijnen waren een rechte hoek (x31 verticaal + 31–33 horizontaal) met een dubbele lijn op rij 18–19.
| x,y | r4 → r5 | reden (model) |
|---|---|---|
| 34,16 | b → s | de witte pixel; rechterhelft van het oor ligt in de schaduw (model 129/125 rechts) |
| 31,17 | K → L | lichtkant buitenrand, model grijs (80–118), geen zwart |
| 33,17 | h → b | begin binnenlijn in het model (165/168, donker 40 in de hoek) |
| 30,18 | K → L | lichtkant buitenrand, model grijs 79/80 |
| 31,18 | . → h | **silhouet +1**: modelblok 217/218/213/217 = hooglicht (vulde het gat in de rand) |
| 32,18 | L → b | model 216/163/217/180: licht, de binnenlijn ligt op x33 |
| 30,19 | b → h | model 191/216/219/216 |
| 31,19 | L → b | model 214/173/215/155; de binnenlijn ligt hier op x32 |
| 31,22 | L → s | model 131/18/133/131: de lijn buigt hier naar x32–33 |
Binnenlijn nu (33,18)→(32,19)→(31,20)→(31,21)→(32,22)→(33,22): een boog zoals het model, geen rechte hoek meer. Lichtstrook (32,17)→(31,18)→(30,19) loopt schuin langs de rand. (33,16) blijft L: erboven is het transparant, hooglicht op de buitenrand mag niet.

### 3. Kop (Jordi: "teveel rechte lijnen")
Rechterrand kop → schouderplaat: rij 25 had een recht stuk van 3 L met K erachter (L L L K), rij 27 een dubbele rand (K 41, L 42, K 43) en rij 28 L L K. Gelezen met lum.py:
| x,y | r4 → r5 | reden (model) |
|---|---|---|
| 35,24 | L → s | model 135/13/134/135: huid, de rand zit op x36 |
| 36,25 | L → s | model 133/18/134/136: huid |
| 37,25 | L → K | model 22/12/15/50: zwarte buitenrand |
| 38,25 | L → K | model 11/12/52/52: zwarte buitenrand |
| 38,27 | L → K | model 16/17/17/54: plaatlijn zwart (geen L/K-wissel) |
| 41,27 | K → 3 | model 94/17/91/89: plaat; haalt de dubbele rand weg |
| 42,27 | L → K | model 12/9/87/58: buitenrand zwart |
| 36,28 | L → s | model 131/132/133/15: huid |
| 37,28 | L → K | model 132/15/14/53: kop/plaat-lijn |
| 38,28 | K → 3 | model 16/90/86/90: plaat |
| 35,29 | L → K | model 132/14/17/17: kop/plaat-lijn |
Buitenrand nu 35 (23) → 36 (24) → 37–39 (25) → 40–41 (26) → 42–43 (27) → 44 (28), zoals het model; kop/plaat-lijn één diagonaal (38,27)→(37,28)→(36,29)→(35,29), geen L naast K meer.
**Kin** (onderlijn rij 36 was L K K L K): (24,36) L→K en (27,36) L→K; model 36b is zwart van 24,5 tot 28.
Niet veranderd: de bovenrand (18–21 op rij 19, 22–27 op rij 20) en de linkerrand (x20, rij 25–31). Die zijn in het model ook recht: de modelbovenrand zakt maar een halve spritepixel (rij 20,5 bij x24) en de linkerrand ligt per modelrij op 20–20,5. Meer kromming kan daar alleen door te tekenen wat het model niet heeft.

### 4. Linkerarm (Jordi: "veel te recht")
De rechterlijn van de arm liep 13 rijen recht op x26 (rij 36–48). Het model (natief) loopt eerst op 52 (rij 36–40), dan 51 (41–44), dan **50 (45–47)**, dan 51–52 (48) en 53 (49): een holle curve die bij de pols weer uitbuigt.
| x,y | r4 → r5 | reden |
|---|---|---|
| 25,45 / 25,46 / 25,47 | s/s/b → L | armlijn een pixel naar binnen, waar het model hem heeft (modelblok s/K, zwart op de rechterhelft) |
| 26,45 | L → m | dij, model m (mm/mm) |
| 26,46 / 26,47 | L → s | dij, model s |
| 22,41 / 22,42 | T → L | linkerrand van de arm in één lijnkleur (was L T T L); MAG-punt b van KEURING_r3 |
Lijn nu x26 (rij 36–44) → x25 (45–47) → x26 (48) → x27 (49): de arm wordt naar de pols iets smaller en buigt dan uit naar de hand. De linkerrand (23 → 22 → 22 → 21 → 20/21) volgde het model al.

### 5. Staart rechts (Jordi: "teveel rechte lijnen")
De buitenrand stond 7 rijen recht op x55 (rij 51–57). Het model ligt op rij 51 en 57 op de linkerhelft van cel 55 (54,5–55) en op rij 52–56 op de rechterhelft (55,5): een boog.
| x,y | r4 → r5 | reden |
|---|---|---|
| 54,51 | L → K | wordt de buitenrand (model sK/sK) |
| 55,51 | K → . | **silhouet −1**, modelblok half (K./K.) |
| 55,57 | K → . | **silhouet −1**, modelblok half (K./K.); (54,57) K is al rand |
Buitenrand nu 50 (47) → 51 → 52 → 53 → 54 (51) → 55 (52–56) → 54 (57) → 53 → 52 → 50–51 (60).
**Bovenrand staart** (van het lijf naar rechts, rij 45–47) wisselde L L L K / L L L K / L K: in het model overal zwart (rij 45b, 46a, 47a). (41–43,45), (45–47,46), (49,47) L → K.

### 6. Kritische ronde over de hele sprite (8× naast het model)
Gecontroleerd: kop, oren, platen, beide armen, handen, benen, staart. Wat nog recht of ruw oogt, maar zo in het model staat en daarom niet veranderd is:
- bovenrand kop en linkerrand kop (zie punt 3);
- bovenrand van het onderste staartstuk (T, x32–43 op rij 60) en de onderrand (3-3-7-4-3-2): het model heeft daar dezelfde loop;
- de V van het linkerbeen (scheen x15/x18, rij 53–56): model ook verticaal;
- rechteronderarm en rechterhand: druk, maar het model is daar even druk (vingers van 1 px).
Geen extra edits buiten de bovenstaande lijst.

## Controle
- Silhouet: 3 pixels (zie boven), verder diff 0.
- 11 kleuren + transparant (geen nieuwe).
- Geen vulkleur op de buitenrand; enige losse lijnpixel is het wangvlekje (34,27) (bewust, vibe).
- Zwart K 21,6 % (r4 20,7 %): omhoog doordat L op de staartbovenrand en de kop/plaat-lijn K werd, zoals het model. K+L 33,1 % (r4 33,9 %).

## Open punten
1. **Oog A of B**: Jordi kiest. B ligt precies op de modelplek maar raakt de kaaklijn.
2. Kop-bovenrand en linkerrand blijven vrij recht (zo staan ze in het model); verder krommen kan alleen door van het model af te wijken. Vraag aan Jordi of hij dat wil.
3. Zwart 21,6 %, net boven de Gen 3-norm; de nieuwe K's volgen het model.
