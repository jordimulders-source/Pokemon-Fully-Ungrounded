# Fruitvampier (Emolga-lijn fase 3) – sprite r1 (maker)

Leveringen: `A0.png` (trouw model, alleen technisch opgeschoond), `A.png` (C vizier + A kap met V, gele voorhoofdvlekje weg),
`A_geel.png` (C + A, gele voorhoofdvlekje blijft op de kap), `vel.png` (A0 | A | A_geel | model op dezelfde schaal | model verkleind,
alles 8×; daaronder 1× op licht/donker en 2×). Alle drie 64×64, geïndexeerd (16 paletplaatsen, 13–14 gebruikt), index 0 transparant.
Maat: x19–44 × y0–63 = **26 × 64 px** (voeten tegen de bovenrand, oren tegen de onderrand), 3/4 naar links zoals het model, niet gespiegeld.

## Werkwijze (overnemen, niet hertekenen)
Scripts in `gereedschap/`, in deze volgorde: `natief.py` → `rek.py` → `bouw0.py` → `bouw1.py` → `bouw2.py` → `varianten.py` → `vel.py`
(controle: `controle.py`, telling: `telling.py`, kijken: `kijk.py`).
1. **Natief raster uit r6** (`gemini/r6.png`, niet uit het opgerekte model): pitch 10,24 px, fase 9,05/9,20 → `natief_r6.png` (99×99).
2. **De rek van het lijf teruggemeten** (`rek.py`): Claudes +25 % is niet om één vast punt gedaan; per modelrij gemeten
   x' = c + (x−c)/s (s loopt boven en onder af van 1,04 via 1,25 naar 1,01, het centrum schuift 438–540). Elke modelpixel krijgt zo de
   klasse van zijn eigen natieve r6-cel: **kop, oren en voeten komen exact uit het natieve raster** (identiek), het lijf via de rek.
3. **Kale reductie** (`bouw0.py`, → `tussen/kaal.png`): silhouet rechtstreeks uit `model.png` (spritepixel = figuur als < 50 % van zijn
   16×16-blok achtergrond is), kleur = meerderheidsklasse van de natieve cellen, eerst per kleurgroep (zwart+donker samen), zwart wint
   vanaf 35 % (1-px modellijnen). Randmengsels (lichte cel tussen zwarte lijn en witte achtergrond) en de kier tussen de poten zijn
   achtergrond.
4. **Reparaties per pixel naar het model** (`bouw1.py`), daarna **technische opschoning** (`bouw2.py`: buitenlijn zwart aan de
   schaduwkant/selout aan de lichtkant, niet om en om, tintvlakjes < 3 px weg, losse zwarte stipjes weg). Elke wijziging staat met zone
   en reden in `tussen/log1.pkl` / `log2.pkl`.

## Afwijkingen van de kale reductie (A0 t.o.v. `tussen/kaal.png`: 269 van 1025 px)
| zone | px | wat |
|---|---|---|
| poten (rij 0–9) | 34 | tint op de modelmediaan (zwart/donker/grijze tenen en lichte linkerrand van de poten), kier tussen de poten (32,6) open zoals het model (enige silhouetwijziging), gele rand rechts begint op 35,7 (model) |
| vleugelpakket + buik (rij 10–37) | 121 | rechter gele rand als 1-px lijn op de gemeten modellijn met zwarte omlijning erbuiten (53 px); linker gele lijnen A (vleugelpunt → splitsing), A' (→ hals) en B (→ links omlaag) als 1-px lijnen op de gemeten modellijn (31 px); zwarte vouwlijn van de witte ovaal schuin naar rechtsonder op de modellijn (16 px; viel in de reductie in stipjes uiteen); buitenlijn en korrels |
| kop/gezicht (rij 38–51) | 79 | ogen (gemeten modelzwart), glans per oog op de lichtste modelpixel, mondlijn, gele snuitvlek, masker met omlijning rondom (zoals het model), wit/wangplukken op de modelmediaan, gele voorhoofdstreep 4 px op de modelbedekking |
| oren (rij 50–63) | 35 | grijze lichtrand links op beide oren (model 54–137), buitenlijn |

**Pixels die niet 1-op-1 uit het model komen** (benoemd):
- Rechter gele rand: in 6 rijen (10, 12, 13, 21, 30, 34) staat het geel 1 px naar binnen t.o.v. het afgeronde modelmidden, omdat de
  buitenste pixel de zwarte omlijning werd (silhouet blijft gelijk). Rij 7–8 (begin van de rand op de poot) is donkergeel op de rand.
- Zwarte punt op 21,18 (begin lijn A): omlijning om de vleugelpunt; het model heeft daar zwart om het geel.
- 27,51 zwart i.p.v. de staart van de gele voorhoofdstreep (de streep ligt daar op de buitenrand; model heeft er een zwarte rand om).
- Kleuren zijn Gen 3/fase 2-tinten (lijf D/E/K, geel y/Y/L, wit B/W/w uit `emolga_evo/af/model.png`; masker in staalblauw M/N/O naar
  het model), niet de modelkleuren zelf.
- Niets getekend: geen eigen ogen, mond of vormen. Ogen zijn uit het model gemeten (nabij 4×4 met glans op 28,46; ver 2×4 met glans op
  22,46); leesbaar, dus geen Gen 3-oog geleend.

## Varianten (bovenlaag op A0, `varianten.py`)
- **C** (74 px samen met A): masker → leigrijs van het vizier van fase 2: opvulling/licht → G (98,96,114), omlijning → E (64,64,82).
  De letterlijkere omzetting (opvulling E, omlijning D) maakte het zwarte oog onleesbaar (zwart op 64/64/82), vandaar G/E.
- **A**: zwarte kap over de kruin (rij 50, x24–30, plus 26,51) met de V-punt omhoog op 25,49; het witte voorhoofd (rij 48 x24–26,
  rij 49 x23–24/26–28) blijft als witte band tussen masker en kap. Licht linksboven op de kap: 24,50 in E (niet uit het model).
  Probeersel met de punt hoger (25,48, tegen de maskerbrug): `tussen/A_v1.png`; daar bleven twee losse witte stipjes onder het masker
  over die als slagtanden lazen.
- **Geel voorhoofdvlekje**: de V valt er precies overheen. `A.png` = vlekje weg (kap), `A_geel.png` = vlekje blijft op de kap
  (verschil 4 px: 25,49 L · 25,50 Y · 26,50 Y · 26,51 y). Keuze voor Jordi.

## Zwakke punten (eerlijk)
1. **Voeten**: de gekrulde tenen van het model worden op 64 px een donker blokje met twee grijze teenvlekjes; geen echte tenen.
2. **Mondlijn** (24–27,39 + haakje 28,40, begin 23,39 lichter): staat in het model als dunne zwarte boog; op 64 px is het een
   streepje van 5 px dat zwaar kan lezen (als wenkbrauw). Lichter maken (w) kan, maar wijkt dan van het model af.
3. **Vleugelpakket effen**: rechterdeel egaal donker, linkerpaneel egaal grijs, zoals het model; bij fase 2 vond Jordi het zwart "erg
   effen". Een volumeronde (kleur, niet vorm) kan, is niet gedaan.
4. **Binnenste zwarte lijn langs de rechter gele rand** (model: geel tussen twee zwarte lijnen) is niet gezet; binnen ligt D, dus het
   geel heeft alleen buiten een zwarte lijn. Het dunne gele streepje op de linkerpoot (31,7–8, ±0,3 px breed) viel weg.
5. **Variant A/C**: de onderste helft van de kop wordt één donkere massa (vizier + kap); de ogen blijven leesbaar door de glans en de
   G-opvulling, maar de V is klein (1 px punt boven een volle rij). Op 1× leest de kap vooral als "donker voorhoofd".
6. Wangplukken rechts (x34–37) zijn met de buitenlijn grotendeels dichtgezet; de pieken van het model zijn deels weg (inkeping op 37,43 blijft).
