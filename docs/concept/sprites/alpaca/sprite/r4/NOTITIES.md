# Palpaca r4 (19 nov): vanaf r3B, meer naar het model (perspectief, binnenlijnen, kleuren)

Jordi (letterlijk): "De snuit heeft niet genoeg definitie, dat zorgt ervoor dat het hoofd plat is. Evenals de definitie bovenin bij de oren. De lijnen mogen wat verder het hoofd in, zoals bij andere sprites. Nek is prima. waar de staart vast zit aan het lichaam mag ook meer definitie. Het oog is twee pixels te lang aan de onderkant. De haardos heeft geen bolling boven de neus en daar hoort juist wat schaduw op. Je hebt de haardos rechts van het oog weer weggehaald ook, dat is geen verbetering. Linkeroog is weg. Bovenin het voorste achterpoot zit geen schaduw. Je mag echt veel meer het model gaan namaken" · "Dit is misschien wel de slechtste model namaak poging tot nu toe qua kleurgebruik" · "ik heb niks over kleur gezegd, maar meer richting model gaan is prima, het gaat vooral om perspectief, dat ontbreekt vooralsnog het meeste, ik denk dat je deze toch teveel op het originele ontwerp hebt gebaseerd, waar het model echt een vooruitgang is".

## Bestanden
- `palpaca.png` (r4, met verre oog), `normal.pal`, `r3B_nieuwpalet.png` (r3B met alleen het nieuwe palet, om het kleurverschil los te zien).
- `vel.png`: model | r4 | r3B met nieuw palet | r3B (8×, zelfde hoogte) · kop 12×: model op spriteraster | r4 | r3B · 1× en 2× op licht en donker.
- `scripts/bouw_r4.py` (keten), `scripts/extra.txt` (handreparaties kop), `scripts/px.py` (modelmeting per spritepixel), `scripts/modelkop.py`, `scripts/vel.py`.

## Werkwijze
1. **Palet gemeten in het model** (natief raster, mediaan per zone/helderheidsband): wol 252 248 236 / 240 233 214 / 214 205 182 / 180 168 146 (neutraal crème, niet roze); lijn 124 112 92 (zachte modellijn) en 52 44 36 (donkerste modellijn, bruingrijs); verre poot 154 137 113 / 124 109 88; handschoen en kwastjes 244 108 98 / 218 64 68 / 158 36 56 / 84 24 34; kraag geel 236 206 100, turkoois 62 176 156; oorbinnenkant/kraagroze 222 160 164. Oog: donker 52 44 36, bruine onderkant 124 112 92, glans 252 248 236. 16 kleuren incl. transparant.
2. **Binnenkant uit het model**: elke wolpixel die niet op de rand ligt krijgt de toon van het model op die plek (gem. helderheid ≥236 → 2, ≥216 → 3, ≥196 → 4, ≥165 → 5, anders binnenlijn 6); verre poot idem (≥140 → licht, anders donker). Zo komen de binnenlijnen (kuif, wang, poot- en dijaanzetten) en de schaduwkanten uit het model, niet uit r3.
3. **Handwerk** alleen waar de reductie ruis gaf of Jordi iets noemde (hieronder).
- Silhouet: **alfa-diff met r3B/r2 = 0**. Ook aan de snuit was geen silhouetwijziging nodig: de modelomtrek ligt daar op dezelfde pixels (dekking x 17, y 28–31 = 0,62–0,93; de kin in het model op y 33 heeft maar 0,22–0,29 dekking).
- r4 t.o.v. r3B: 245 px anders.

## Per punt
1. **Snuit**: definitie uit het model: de kuif hangt over de snuit (schaduw 5 eronder op y 23–24, lijn 6 op y 25 van de rand naar binnen), snuitrug licht (x 18–19, y 28), neusgat 6 op (19,29) (model gem. 212, min 104), mond 6 op (18,31)(19,31) met opkrul (21,31), kaakonderkant 5 (y 32). Lijnen lopen vanaf de omtrek het hoofd in.
2. **Oren**: aanzet linkeroor als lijn 6/5 (x 19–21, y 18–19; model 6155), rechteroor: lijn 5/6 langs de binnenkant (x 28–31, y 18–22; model 4665/5656/465616).
3. **Staartaanzet**: lijn 6 onder de staart (41,40)(42,41) (modellijn x 41–42), bovenaanzet (38,38) in 5; rest van de staart uit het model.
4. **Oog**: onderste rij (24,29)(25,29) weg (nu wol 4). Oog is nu 2×3: glans + donker / donker / donker + bruin (model 3,4 rijen hoog). De lijn direct boven het oog lichter (4) zodat het oog los leest.
5. **Haardos**: bolling boven de neus met schaduw eronder (zie 1). Haardos rechts van het oog terug: wanglijn 5 op x 26–27, y 26–28, onderaan naar rechts (model x 26–30, y 26–30).
6. **Verre oog**: (18,26)(18,27) donker 1, (19,26) 6 (model: 0,78 / 0,56 / 0,33 donker). Leest als een donker inkepinkje op de rand.
7. **Voorste achterpoot**: schaduw bovenin uit het model: y 50 x 35–39 = 5 4 4 5 (35,36,39 in 5), y 51 = 5 4 5 6, y 52 x 37–38 = 5, y 53 = 4 5.
8. **Nek**: niet aangeraakt (y 33–36, x 21–29 = r3B).

## Zwakke punten
- Het silhouet is nog dat van r2 (bevroren). Het model heeft een rondere, wolligere kopomtrek en grotere oren; het perspectief van kop en lijf zit voor een deel in die omtrek. Meer perspectief vraagt een nieuwe reductie van het model (dan wijzigt het silhouet): dat is een keuze voor Jordi.
- Het nabije oog is klein (2×3) naast het model (oog ±2,1 × 3,4 px met grote glans); leest op 1× als kraaloog.
- Verre oog blijft een klein inkepinkje op de rand.
- Lijf en poten zijn modeltonen zonder extra opschoning: hier en daar kleine vlekjes (y 43, y 47–49).
- Niet gekeurd door een onafhankelijke keurder.
