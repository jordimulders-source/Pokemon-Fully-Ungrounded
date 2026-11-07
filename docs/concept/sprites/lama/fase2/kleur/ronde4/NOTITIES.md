# Lama fase 2: kleur ronde 4 (verse maker, 3 nov)

Kleur op het goedgekeurde **silhouet ronde 6**, met de hand in een tekstraster (één letter per pixel). Model = het 3D-poppetje (`silhouet_r5/onderlaag_256.png`). Oog in drie varianten; `lama.png` gebruikt **oog B**.

## Bestanden
- `lama.png` (indexed, 16 kleuren, index 0 transparant), `normal.pal`, `raster_grid.txt` (= lama.png als letters).
- `oog_A.png`, `oog_B.png`, `oog_C.png`: de hele sprite, alleen de oogzone x19–23 y11–15 verschilt.
- `diff_silhouet.txt`: elke afwijking van ronde 6, met de dekking van het model en de reden.
- `studie.png`: Game Freak-studie. `vel.png`: alleen deze ronde.
- `bron/lama_raster.txt`: **het met de hand getypte raster** (64×64). `bron/oog_A.txt`, `oog_B.txt`, `oog_C.txt`: de oogzone per variant (met de hand).
- Scripts (alleen bouwen, controleren en kijken): `bron/bouw.py` (letters → png, oog alleen binnen de oogzone), `bron/controle.py` (+ `controle_uitvoer.txt`), `bron/masker.py` (masker tegen ronde 6 tijdens het typen), `bron/vel.py`, `bron/studie.py`, `bron/bron_zones.py` (kaart waar de onderdelen van het model per pixel liggen: `bron_zones.txt`, en de lichtkant: `bron_licht.txt`; alleen als leidraad gebruikt, er wordt niets automatisch ingekleurd).

## Game Freak-studie (`studie.png`)
Bekeken in `graphics/pokemon/*/anim_front.png` + `normal.pal` (palet en aandeel per kleur gemeten):
- **Mareep:** wol licht `ffffbd` 28%, midden `eecd73` 20%, schaduw `cd9c52` 10%; omlijning bruin `9c6220` rondom de hele wol, ook onderaan. Zwart (12%) alleen rond het blauwe gezicht en de poten. De middentint ligt als wolkranden (bolletjes) tegen het licht aan, niet als losse klonten.
- **Flaaffy:** witte wol met een lichte blauwgrijze omlijning aan de lichtkant, donkerder alleen onderaan; binnenin alleen een krul als lijntje.
- **Girafarig:** verre poten in een eigen donkere tint, hoef 2 rijen (blauwgrijs), zwart alleen aan de schaduwkant.
- **Ponyta:** poten 3–4 px inclusief omlijning; nabije poot licht, verre poot bruin; hoef 2 rijen met 1 lichte pixel.
- **Numel:** oog in middenbruin, alleen de voorrand zwart, glans als klein verticaal streepje laag in het oog.
- **Slakoth:** de luiheid zit in de vorm die afhangt (de bruine vlek), niet in het oog zelf.
- **Camerupt:** zwaar lid in een donkere huidkleur (geen zwart), pupil direct tegen het lid.

### Regels die ik toepas
1. Wol: **licht is de hoofdtint** (l ±23%, h als wolpunten), midden (b) als een sikkel rechtsonder, diepe schaduw (s) alleen onder de buik; geen klonten binnenin.
2. **Omlijning van de wol in bruin (d), rondom**, ook aan de schaduwkant (Mareep). Zwart (k) alleen aan de schaduwkant van poten, kaak/lip, handschoenen, hoeven en doek. Dat is de "zachte omtrek".
3. Fluffy via de **grens licht/midden als wolbogen** (kleine bolletjes naar beneden, Mareep) en een ritme van lichte wolpunten langs de lichtkant van de hals; geen eigen schaduwranden binnenin.
4. Poten en kop een tint **donkerder dan de wol** (model: kop A86A3A, poot B57A45, wol C88E55): poot en kop op b, wol op l.
5. **Verre poten een eigen donkere tint** (s/d), nabije licht (l/b), gescheiden door één zwarte lijn; hoef 2 rijen met 1 lichte pixel (Ponyta/Girafarig).
6. Oog: **rechte lidlijn, iris tegen het lid, bruin in plaats van zwart, licht laag**; geen wit oogwit, geen zwarte ring rondom (Numel/Camerupt/oogstudie).
7. Licht van linksboven: borst en voorkant hals licht, achterwerk rechts en buik in de schaduw, teruggekaatst licht (b) in de onderste buikrij.
8. Accessoires met een eigen omlijning per kleurgroep: doek in donkerrood (m) aan de rode kant en zwart aan de blauwe kant; handschoen r/o/m + k.

## Palet (16 incl. transparant)
| letter | kleur | gebruik |
|---|---|---|
| . | 98d0a0 | transparant |
| k | 2a161a | omlijning schaduwkant, lid, pupil |
| d | 6c3a20 | omlijning wol/kop, verre poot |
| s | a8683a | schaduw |
| b | d69a52 | basis kop/poten, wolschaduw |
| l | efc27a | basis wol |
| h | f8e2a8 | licht, wolpunten, crème lichtje (oog C) |
| o | f0604a | rood licht (handschoen, kwast, doek) |
| r | d8243c | rood (handschoen, kwast, halsband, doek) |
| m | 98203a | donkerrood (schaduw/omlijning rood) |
| n | 4a4048 | polsband, hoef, grijsbruine iris (oog C) |
| y | f2b02a | geel (halsband, pompon) |
| g | 2e9c5a | groen (halsband) |
| p | e85a9a | roze (bovenrand doek) |
| u | 2f5fb8 | blauw (doek) |
| v | 968c96 | lichtgrijs: nagels, glans polsband, hoef |

Vachtramp f8e2a8 / efc27a / d69a52 / a8683a / 6c3a20 ongewijzigd (goedgekeurd). Verdeling: l 23%, b 17%, d 15%, s 13%, k 10%, rest accessoires.

## Wat er per onderdeel gebeurde
- **Wol (lijf + hals):** één zachte massa. Licht linksboven over borst, schouder en achterwerk; een sikkel in b rechtsonder; s alleen in de onderste buikrijen; teruggekaatst licht in b op de buikrand. De grens licht/midden loopt in 4 kleine wolbogen (y37–38). Hals kaarsrecht als één cilinder: wolpunten (h) in een ritme langs de lichtkant, b/s rechts. Omlijning bruin rondom.
- **Kop:** zoals het model een tint donkerder dan de hals (b). Voorhoofd en snuitrug licht, kaakschaduw van onder het oog naar de kin, neusgat (k) op (15,15), korte mondlijn vooraan, kleine hangende onderlip (y18–19). Het oog zit hoog achter op de kop, zoals op het model.
- **Oren:** banaanoren met rode kwasten aan de buitenkant (o/r/m), zoals het model. Het nabije oor is 2 px breed; daar is de lichtkant als pseudo-omlijning gedaan (§8).
- **Staart:** pluim van 4×3 px met eigen omlijning, licht bovenin; los van de rug door 1 px lucht ervoor en een vlakke rug ervoor (zie diff).
- **Halsband:** drie strepen groen/geel/rood zoals het model, rechts 1 px omhoog waar hij achter de hals verdwijnt; twee pompons (geel, rood) hangen eronder.
- **Aguayo:** doek over de rug: roze bovenrand, blauw, rood (licht linksboven), zoom in donkerrood, ronde hoeken; geen koffer-slot, geen grijs blok.
- **Poten:** voor: nabije poot licht (l/b), verre poot donker (s/d), één zwarte lijn ertussen; zwarte polsband met een glanspixel, rode MMA-handschoen (o/r/m), twee lichte nagels onder de nabije handschoen en één onder de verre. Achter: nabije poot met hak, hoef als donkere punt (v/n + k); de verre achterpoot als donkere strook rechts (zoals het model, zie hieronder).

## Oogvarianten (alleen x19–23 y11–15)
- **A (Numel-basis, minder emotie):** vlak zwaar lid (d-k-k-k), huidplooi (b) erboven, mat donkerbruin oog met alleen de voorrand zwart, klein laag lichtje (h), geen oogwit.
- **B (gekozen):** als A, maar het lid zakt achteraan 1 px en eronder ligt een zachte wal (s) die naar achteren uitloopt. Droogst: Numel-oog met de Slakoth-luiheid in 3/4, zonder donkere vlek.
- **C (recept A uit de oogstudie):** lidlijn van 4 px + wimper omhoog achteraan, grijsbruine iris (n) met liggende pupil (kk), crème lichtje vóór-onder.
- Bewijs: `oog_B` 5 px en `oog_C` 9 px verschil met `oog_A`, **0 px buiten de oogzone** (`controle_uitvoer.txt`).

## Controles
```
mode P | transparency 0 | palet 16 | kleuren gebruikt (incl. transparant): 16 | pixels 1160 | box 40x62
silhouet t.o.v. ronde 6: +2 / -5 px (totaal 7, alle <= 1 px van de 50%-grens van het model)
open randen: 0 (bewuste pseudo-omlijning §8: oor 2 px breed op x17 y3/7/8, nagels van 1 px op (22,60), (14,62), (16,62))
oog_B / oog_C: 0 px verschil buiten de oogzone
```
Afwijkingen van ronde 6 (`diff_silhouet.txt`):
- +x48–49 y23: staartpluim 1 rij hoger (staart leesbaar).
- −x46 y25: 1 px lucht links van de pluim (staart leesbaar).
- −x43–45 y25: losse bult van 3 px tussen doek en staart weg; de reeks doek-dip-bult-gat-staart was het schokkerigste stuk van de rug (glad).
- −x51 y26: rechterbovenhoek van het achterwerk afgerond (glad).
Verder geen vormwijziging. Pixels en verhoudingen van ronde 6 (kop, hals, poten, halsband) zijn gebleven.

## SPRITE_OPDRACHT §0 / §2 punt voor punt
- **§0.1 Lijf en blik 3/4:** pose en hoek zijn die van het goedgekeurde model (lijf bijna zij, kop 3/4 naar de kijker, één oog). Niet veranderd.
- **§0.2 Alle ledematen, oren, ogen:** 2 oren met kwast, 1 oog (snuitdier), 2 voorpoten met handschoen, nabije achterpoot met hoef, verre achterpoot als strook (model). Staart.
- **§0.3 Geen rechte lijnen waar het dier rond is:** de rug is nu één vlakke lijn (lama: rug recht, SPEC); borst, buik en achterwerk volgen ronde 6.
- **§0.4 Ogen geïntegreerd:** lid, bruine iris, laag lichtje; geen kraal, geen brilring.
- **§0.5 Leest als de soort:** op 1× en 3× een lama (banaanoren, lange rechte hals, hangende lip, staartpluim).
- **§0.6 Formaat:** 1160 px, box 40×62 (= ronde 6).
- **§0.7 Pose niet stijf:** telgangpas van het model (kameelachtigen: toegestaan).
- **§2 Model = specificatie:** vorm 0 px veranderd buiten de 7 gemelde pixels; accessoires op de plek en in de kleur van het model (halsband g/y/r, roze-blauw-rood doek, rode kwasten, rode handschoenen met zwarte band, nagels).
- **§2 Omlijning per kleurgroep, zwart alleen aan de schaduwkant, licht linksboven, geen open randen:** ok (zie controles).
- **§2 Viervoeters diagonaal:** uitzondering kameelachtigen, model in telgang.
- **§2 Met de hand:** alles in `bron/lama_raster.txt` en `oog_X.txt` getypt; geen tintwissel- of shadingscripts. `bron_zones.py` is alleen een kaart (waar ligt welk onderdeel op het model).
- **Kleuren vergelijken met hetzelfde type (Fighting):** warme karamel, rood als accent; past naast de alpaca (fase 1).

## Eerlijk: wat nog niet (helemaal) leest
- **Fluffy zit aan de grens van wat kleur kan.** De wol is één zachte massa met bruine omlijning, wolbogen en wolpunten; naast Mareep/Flaaffy blijft het lijf een rechthoekig blok, omdat de omtrek van ronde 6 (= het model) recht is. Meer fluffy kan alleen met een bollere omtrek (silhouet), niet met de kleur zonder klonten.
- **Verre achterpoot:** in het model staat hij vrijwel helemaal achter de nabije. Op 1× leest hij als een donkere rand aan de nabije poot, niet als een eigen vierde poot. Dat is een eigenschap van het model (zo gemeld bij ronde 6); ik heb het silhouet daarvoor niet aangepast.
- **Handschoenen raken elkaar** onderaan (model). De zwarte lijn ertussen scheidt ze op 3×, op 1× lopen ze nog samen.
- **Oog:** het is klein (zoals het model: 3 px breed). Op 1× leest het als een donker, half gesloten oog; het verschil tussen A, B en C zie je pas op 3× en meer.
- **Doek:** een franje (losse kwastjes onder de zoom) heb ik geprobeerd, maar die las als druppels; teruggedraaid. De doek leest nu als een gestreepte deken op de rug, met de ronde onderkant van het model.

## Lessen
- Een volledig 64×64-letterraster werkt beter dan losse spans: fouten in de rijlengte zie je meteen, en `masker.py` vangt elke pixel buiten het silhouet tijdens het typen.
- Wol leest zachter met een **bruine omlijning rondom** (Mareep) dan met zwart aan de schaduwkant; zwart alleen op poten, gezicht en accessoires.
- Volg ook de **kleurvlakken** van het model, niet alleen de vorm: kop en poten zijn er een tint donkerder dan de wol. Lichte poten maakten het geheel vlak.
- Een donkere kaaklijn met daaronder een schaduw op de hals leest als een lange mond. De hals onder de kin licht houden, dan is de kaak een rand.
- Drie donkere rijen boven elkaar (schedelrand, schaduw, lid) maken een wenkbrauw. De rij boven het lid een tint lichter (b) houden.
- Franje onder een doek op 64 px leest als druppels; een rustige zoom in de donkere tint werkt beter.
- `git mv` stage't: niet gebruiken als je niet mag committen (gewoon `mv`).
