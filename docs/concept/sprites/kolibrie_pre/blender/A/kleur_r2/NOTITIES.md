# Kolibrie pre-evo – kleur r2 (maker)

Jordi over r1: "snavel is prima, linkerkant van de buik is idd niet mooi, misschien iets boller? voor de rest prima, is het vooral afwerking, shading, spritewerk, dragonfly cave gebruiken, agent laten controleren etc".

Bestanden: `rijen.txt` → `bouw.py` → `raster.txt`; `palet.py` → `kolibrie_pre.png` + `normal.pal`; `controle.py`; `vel.py` → `vel.png` (r2 1×/3×/4× licht+donker, model_open, Fletchling, Starly, Taillow, r1); `silhouet_r2.txt` (nieuwe omtrek).

## Wijzigingen t.o.v. r1 (87 px)
1. **Buik links boller (enige silhouetwijziging, +13 px, 603 px):** linkerrand was x21 voor y28–37; nu x21, 20, 20, 19, 19, 19, 19, 19, 20, 21 (y28–37). Een vloeiende boog van keel naar onderkant; de inham onder de kin (y28) blijft. Diff buiten x18–21/y28–37: **0**.
2. **Banding weg op de kop:** de `E`-strook langs de hele achterrand (y16–18) is nu `B`; `E` alleen nog onderaan de nek (kernschaduw). Kruinhooglicht `5` als vlek binnen de kop (y15–16), niet langs de omtrek; bovenop de kop een paar pixels outline-hooglicht `3` (Dragonfly Cave: schaduwkleur als outline-hooglicht op de meest belichte rand, binnen de lijn).
3. **Vleugelvoorrand taps/onderbroken:** `E`-lijn alleen y28–32 (waar de vleugel echt over het lijf valt); y33–34 alleen kleurgrens (`4` → `B`); onderaan weer korte `E` waar de vleugelrand in de schaduw ligt.
4. **Onderflank volume:** de schaduwgrens `3`/`2` loopt nu als kromme die naar rechts stijgt (y39 x34–35, y40 x32–36, y41 x29–36), in plaats van een horizontale band.
5. **Onderbuik:** `5`-schaduw in een gebogen vlak onderaan de buik (y36–40), hooglicht `7` linksboven; de bol leest nu als een bal met het licht linksboven.
6. **Pootjes:** `F` lichter (130,122,156)→(150,142,174), teentjes `F`/`A` tussen zwart, beter te zien op 1×.
7. **Staartje:** lichtere lob `4`/`3` naast de donkere vleugel `E` (y35–40, x41–43), zodat het als apart stompje leest.
Ongewijzigd: snavel, Starly-oog (pixel voor pixel), kap als kleurgrens zonder lijn, palet verder gelijk aan r1.

## Controles (script)
- alpha-diff buiten de buikzone: **0**; in de zone 13 px toegevoegd, 0 weggehaald.
- open randen: **0**.
- schaduwkant-rand niet zwart: alleen (33,23) (bovenrand nek, selout) en twee teenpixels (dun deel).
- losse pixels: alleen bedoelde enkelingen (oog-omgeving, diagonale vleugelrand, outline-hooglicht op de kruin, glans op de vleugelpunt); geen ruis in de vlakken.

## Dragonfly Cave-checklist
| punt | PASS/FAIL | toelichting |
|---|---|---|
| Geen vormgereedschap, met de hand | PASS | rijenbestand met de hand |
| Outline donker genoeg, zwart aan de schaduwkant | PASS | `1` rechts/onder/achter |
| Selout (outline base per kleurgroep aan de lichtkant) | PASS | `2` bovenop kop, gezicht, links van slab/borst |
| Outline-hooglicht alleen binnen, op de meest belichte rand | PASS | 2 px `3` bovenop de kop |
| Geen anti-aliasing aan de buitenkant | PASS | script: geen lichte pixels naast transparant |
| Curven zonder jaggies (geleidelijke segmenten, geen hoek in een curve) | PASS | nieuwe buikboog 1-2-5-1-1; kop bovenkant 3-1-1-1 |
| Geen banding (tinten niet parallel aan de omtrek) | PASS met kanttekening | kop opgelost; de `E`-schaduw van de vleugel volgt rechts nog deels de omtrek, maar wordt naar onder breder |
| Geen pillow shading (licht linksboven, schaduw volgt de vorm) | PASS | hooglicht linksboven, kernschaduw rechtsonder |
| 3 tinten per kleurgroep + outline | PASS | lila 5/4/3+2, buik 7/6/5, vleugel 4/B/E |
| Veel hooglichtkleur (R/S-stijl, niet te donker) | PASS | |
| Binnenlijnen alleen waar een vorm over een andere valt | PASS | vleugelvoorrand, kop over borst |

## Eerlijke zwakke punten
1. De korte donkere lijn kop-over-schouder (y24–27, x26–31) is functioneel, maar leest op 4× als een schuine streep; op 1× valt het mee.
2. De vleugel is één rustige plaat zonder veertextuur (Taillow heeft lichte veerrijen). Bewust rustig gehouden na "willekeurige strepen"; Jordi kan meer veerwerk willen.
3. Pootjes blijven klein (silhouet): op 1× twee lichte stipjes onder de buik.
4. Ik heb geen onafhankelijke keurder kunnen inschakelen; dat moet de coördinator nog doen.

## Lessen
- Banding zit vaak in de kernschaduw langs de achterrand: zet de donkerste tint alleen waar de vorm echt wegdraait (onder/achter), niet over de hele omtrek.
- Een vleugelrand wordt zachter door de lijn alleen te tekenen waar de overlap het sterkst is en daarna over te gaan in een kleurgrens.
