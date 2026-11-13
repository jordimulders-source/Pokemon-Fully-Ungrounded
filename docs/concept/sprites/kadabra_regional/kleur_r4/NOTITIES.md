# Regionale Kadabra: kleur r4 (schuine kaart, positie van de schoppen, ogen)

Basis: `basis_r2.txt` (= `../kleur_r2/raster.txt`), zoals r3. Jordi over r3, letterlijk:
- "de kaart moet niet rechtop staan, de schoppen zijn allemaal niet mooi omdat ze niet op de juiste positie van het hoofd staan"
- "het is meer dat door het vergroten van het schoppen symbool dat het me opvalt dat wanneer je het hoofd zou draaien hij niet goed ertussen staat, kijk hoe de sprites van kadabra het doen met de ster, neem dat als voorbeeld"
- ogen: "bij de ogen heb je bij 3 alleen het pupil veranderd toch? zo ja, dat is dan de beste, want dat was mijn vraag ook" → oog_3 verandert meer dan de pupil; de variant met alleen de pupil is **oog_1** (4 px), die staat in de volledige sprite.

Bouwen: `python3 r4.py pos_P1 oog_1 kaart_K2` (alle `var_*`, `raster.txt`, png's; drukt pixeldiff buiten de zones en silhouet af), `python3 vel.py`. Zones (eindes exclusief): pos 23,14–33,23 · oog 21,19–33,25 · kaart 0,14–12,33.

## Studie: de ster bij Kadabra
Bronnen: `graphics/pokemon/kadabra/anim_front_gba.png` (Gen 3, van voren) en `../referenties/kadabra_sprite_a.png` / `_b.png` (zelfde kop, driekwart naar links).
- Gen 3 (van voren): ster 5×4 op x25–29, y17–20, as x27. Binnenranden van de ogen x23 en x31: 1 px geel links en 1 px rechts van de sterarmen. Binnenste oorbases x25 en x31 (midden x28); schedelrand rij 13, 3 rijen geel boven de ster. Ogen beginnen op rij 21: **0 rijen** tussen ster en ogen.
- Referentie a/b (driekwart): ster 5×5; de as staat recht boven de lichte strook van de neusrug. Verre oog ±1 px links van de linkerarm, nabije oog ±1–2 px rechts van de rechterarm: de ster vult de ruimte tussen de ogen. Hij ligt ±1,5 px links van het midden tussen de oorbases, dus op de lijn oorbases → neusrug. 0–1 rij geel tot de ogen, ±3 rijen tot de schedelrand.
- **De ster vervormt niet** met de draaiing: in alle drie symmetrisch en rechtop, geen kortere punt. Alleen de plek schuift mee met de middellijn; linksboven de ster ligt een hooglichtvlak.
- Regel: teken op de middellijn, midden op ±70 % van schedelrand naar ooglijn, onderkant direct boven de ogen, breedte = de ruimte tussen de ogen.

## 1. Schoppen op het hoofd
Middellijn van onze kop: midden tussen de oorbases (30,14) → neusrug op ooghoogte (25,22) → snuitpunt (25,29). De kop is gekanteld, dus de lijn loopt 5 px naar links over 8 rijen (bij Kadabra 1,5–2 px). Kadabra-verhouding op die lijn: midden van het teken op ±(27,18), onderkant op rij 20 (lidrij = 21).
| variant | plek | vorm | |
|---|---|---|---|
| pos_P1 | as x27, x25–29, y15–20 | 5×6 recht (vorm van schoppen_3) | Kadabra-verhouding |
| pos_P2 | as x28, x26–30, y15–19 | 5×5 recht (lobben 1 rij; 5×6 past daar niet onder de inkeping tussen de oren) | 1 px hoger langs de middellijn |
| pos_P3 | as x26, x24–28, y16–21 | 5×6 recht | 1 px lager langs de middellijn; dit **is** de r3-plek |
| pos_P4 | as x25, x24–26, y16–20 | 3×5 recht, smal | recht boven de neusrug, zoals de ster in referentie a/b boven de neusrug staat |
| pos_P5 | plek van P1 | 4×5, meegekanteld (punt rechtsboven, voet linksonder), verre lob 1 px korter | "meegedraaid"; Kadabra doet dit zelf niet |
De r3-plek lag dus 1 px te laag en te ver links op de middellijn; de punt van P1 zit 1 rij onder de oorlijn (26,15). Hooglicht en schaduw op het voorhoofd zijn niet aangepast (alleen de klaver gewist).

## 2. Ogen
- oog_1 (in de sprite): 4 px tegen r2: (28,22) o→w en (29,22) w→o (pupil 1 px naar rechts, wit ervoor), ver oog (22,21) a→d en (22,22) a→w.
- oog_3: 8 px: als oog_1 plus (28,23) b→d, (29,23) en (30,23) b→w, (31,23) b→c.
Op het vel naast elkaar met een diff-plaatje (roze = anders dan r2). oog_2 is van het vel.

## 3. Kaart, schuin
Hoek in het model (`../model/grid10.py`): linkerrand cel x3 (rij 28–30) → x4 (31–33) → x5 (34–35) → x6 (36): 3 cellen opzij over 9 rijen = ±18°, bovenkant naar links. In de sprite: 1 px opzij per 3 rijen (trappen 3‑3‑3), linker- en rechterrand evenwijdig, bovenrand 1 px omhoog per 3–4 kolommen. De schoppen zelf staat rechtop (gekanteld las hij als een "2").
| variant | maat (schuin) | schoppen | silhouet tegen r2 |
|---|---|---|---|
| kaart_K1 | 6 breed, y19–26 (modelmaat) | 3×3 + steel, raakt de rechterrand (geen ruimte voor wit) | +3: (5,19), (1,20), (6,21); −1: (1,23) |
| kaart_K2 | 8 breed, y16–26 | 3×5 met voet, wit rondom | +37 |
| kaart_K3 | 10 breed, y16–27 | 5×6, wit rondom | +60 |
(lijsten per pixel: uitvoer van `r4.py`.) K2 en K3 beginnen op x0 (box 63 breed).
**Hand:** de gestrekte vinger ligt vóór de kaarthoek rechtsonder: vingertop met zwarte rand (6–7,24) op de kaart, nagel w verplaatst van (6,24) naar (6,25), de kaartrand loopt bij K3 achter de vinger door (wit rechts van de vinger op (8–9,24), (9,25)). De lichtgrijze strook (3–4,25) en de gebogen vingers zijn ongewijzigd; 3 vingers.

## Beste combinatie: pos_P1 + oog_1 + kaart_K2 (`raster.txt`)
- Pixeldiff tegen r2: 81 px, **buiten de zones 0**; silhouet +37 (alleen kaart), niets eraf.
- `controle.py`: 11 kleuren + transparant, open randen 0, losse o 0; clusters < 3 px: (3–4,25) a (strook onder in de kaart, stond al in r2 maar hing daar aan (3,24)), (20,25) n en (5–6,28) b (beide r2). Lichtkant 16 % zwart.

## Zwakke punten
- **Middellijn is een schatting** uit oorbases en neusrug; de kop is gekanteld, dus 1 px verschil (P1/P2/P3) is een smaakkeuze.
- P1: de punt staat tegen de oorlijn (26,15) aan; de voet (26–28,20) ligt schuin tegen het ooglid (29,21).
- De schoppen op het hoofd blijft 5×6 tegen 4×4 voor de klaver in het model.
- **Kaart K2** is groter dan het model (K1 = modelmaat leest als wit vlekje met kruisje). De schoppen staat rechtop op een schuine kaart.
- De schuine bovenrand is kort (4 px + 2 px): de hoek lees je vooral aan de zijranden.
- **Nagel** (6,25) leest op 1× niet als nagel.
- oog_1: de pupil is 1 pixel; op 1× op een donkere achtergrond zichtbaar maar klein.
- Niet onafhankelijk gekeurd.
