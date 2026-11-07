# Eindkeuring nachtaap fase 2, kleur ronde 7 (onafhankelijke keurder, 2 nov)

**Oordeel: TERUG.** Er is één FAIL, de kené. Op 1× leest het patroon als drie glimmende ribbels of schildsegmenten (gordeldier, pissebed), niet als een patroon. De rest van de sprite is technisch in orde en leest naast echte sprites als een Pokémon.

Gekeurd: `nachtaap.png` + `normal.pal`. Vellen:
- `eindkeuring_vgl.png`: 12 sprites op 1× en 3×, licht en donker (nachtaap, Lairon, Sableye, Misdreavus, Aipom, Grumpig, Natu, Abra, Mightyena, Zigzagoon, Umbreon, Xatu).
- `patroonstudie.png`: 20 sprites op 1× en 4×, licht en donker.
- `eindkeuring/patroon_crops_7x.png`: uitsneden op 7×.

Scripts: `eindkeuring/meet.py` (uitvoer in `meet_uitvoer.txt`), `vellen.py`, `crops.py`. Gen 3-sprites zijn gebruikt als `anim_front_gba.png` + `normal_gba.pal` waar die bestaan.

## 1. Patroonstudie (Jordi: "vergelijk het vooral met andere pokemon sprites, ook hoe zij patronen doen")

Bekeken op 1× en 4–7×, met indexdumps van Linoone, Furret, Golett, Umbreon, Arbok en Xatu.

| Sprite | Bandbreedte | Tinten in het patroon | Contrast met de basis | Eigen omlijning? | Buigt mee met de vorm | Aan de schaduwkant |
|---|---|---|---|---|---|---|
| Linoone | 5–8 px | 3 per kleur (bruin 2/3/4, wit A/9) | groot: wit tegen bruin | nee, de kleuren grenzen direct aan elkaar | ja, de banden volgen de S van het lijf | wit wordt crème (9), bruin wordt donkerbruin (2) |
| Furret | 3–5 px | 2–3 (7/8/9) | groot: donkerbruin op crème | nee | ja, de ringen zijn bogen om de cilinder | de ring wordt donkerder (8/9) |
| Zigzagoon | 3–5 px | 2 | middel: donkerbruin op lichtbruin | nee, de rand is gekarteld als vacht | ja, de zigzag volgt de haarrichting | donkerder naar onder |
| Seviper | 3–6 px | 3 (geel, oker, donker) | zeer groot: geel op zwart | ja, een donkere okerrand | ja, de sikkels buigen met de kronkels | dezelfde band in oker |
| Umbreon | 2–3 px | 3 (B/A/9) | zeer groot: geel op zwart | nee | ja, ringen om oor, poot en staart | de ring wordt oker (9) |
| Raikou | ±2 px, taps | 1–2 | groot: donker op geel | nee | ja, de wiggen lopen schuin over het lijf | lopen door op donker oker |
| Liepard (rozetten) | 1–2 px ring om een kern | 2 | zeer groot: geel op violet, dus een andere kleurtoon | nee | ja, ze worden smaller op de flank | rozet in donkerder geel |
| Spinda | 1 px | 1–2 | groot: rood-bruin op crème | n.v.t., het is lijntekening | nee, vlak op het gezicht | n.v.t. |
| Golett | 1–2 px | 2 (9/D) | groot: crème op teal | nee | nee, vlak paneel | lichte tint blijft |
| Arbok (buikgezicht) | ±20 px groot vlak | 3–4 | zeer groot | **ja, zwart** | ja, volgt de borstplaat | rechterhelft donkerder |
| Xatu (borstogen) | 3–4 px | 2–3 | groot: rood/zwart op wit | gedeeltelijk, met de donkerste tint als rand | licht | donkerder tint |
| Sigilyph (zigzag) | ±2 px | 1–2 | zeer groot: wit op zwart/groen | ja | ja, om de buik | grijs |
| **Nachtaap r7 (kené)** | **2 px kleur (6/7) + 1 px rand (5)** | **3 (7/6/5), ook binnen één band** | **klein in kleurtoon**: hetzelfde violet, lichter | nee | **nee**: rechte verticalen | **stopt** op y 39–40, allemaal op dezelfde hoogte |

### Regels die ik eruit afleid
1. **Het patroon is een eigen kleurgroep.** Het verschilt in kleurtoon (geel op violet: Liepard, Seviper, Umbreon) of in een grote waardesprong (wit op bruin, donker op licht). Het ligt nooit op de hooglichtladder van het lijf zelf. Een lichtere tint van de vachtkleur leest als glans.
2. **Een band is vlak en wordt als geheel geschaduwd.** Op de lichtkant is de hele band licht, aan de schaduwkant de hele band een tint donkerder. Geen enkele GF-sprite geeft elke band een eigen bevel (licht randje links, kern, donker randje rechts). Dat maakt van een streep een opstaande ribbel.
3. **Dikte: grote banden zijn 3–6 px.** Dunne lijnen van 1–2 px komen alleen voor als gesloten tekentje met een heel groot contrast (Spinda, Golett, de rozetten van Liepard). Dat strookt met Jordi's "een patroon zou altijd dikker moeten".
4. **Banden volgen de bol.** Ze zijn gebogen (de ringen van Furret, de S van Linoone, de sikkels van Seviper). Ze lopen door tot in de schaduw of tot aan de contour, en worden daar smaller of donkerder. Ze stoppen niet allemaal recht op dezelfde hoogte midden op de flank.
5. **Een eigen omlijning hoeft alleen bij grote grafische vormen** (Arbok, Seviper). Bij banden op vacht grenzen de kleuren direct aan elkaar, en het contrast doet het werk.
6. **Het motief leest op 1× als zijn eigen logica**, of dat nu ring, zigzag, spiraal of rozet is. Bij een kené betekent dat: een middenlijn op de ruggengraat, met getrapte zijbanden die symmetrisch van die lijn af lopen.

### Toets van de kené aan de regels
| Regel | Kené r7 | |
|---|---|---|
| 1 eigen kleurgroep | 6/7 zijn lichtere tinten van hetzelfde violet. 7 is ook het lichtste hooglicht van de sprite (lum. 0,78 tegen basis 0,31). | **FAIL** |
| 2 vlak per band | Elke band is 7 \| 6 \| 5: een licht randje links, de kern, een donkerder randje rechts. Daardoor leest hij als ribbel of schildplaat. | **FAIL** |
| 3 dikte ≥ 3 px | Van de 81 kené-pixels (6/7) hebben er 17 een kleinste doorsnede van 1 px en 45 van 2 px. Alleen met de rand in 5 erbij komt de band op 3 px. | **FAIL** |
| 4 volgt de bol, loopt door in de schaduw | x30–31, y33–39 en x36–37, y35–39 zijn 7 px recht verticaal. Alle banden houden op y 39–40 op, op de lichtkant van de flank. | **FAIL** |
| 5 omlijning | geen eigen omlijning; dat is correct | PASS |
| 6 motief leest op 1× | Alleen de linkerband heeft één trede. Op 1× zie je drie glimmende verticale strepen. Een middenlijn op de ruggengraat ontbreekt: de rugband loopt maar tot x31. Daardoor leest het niet als kené en niet als "gecentreerd van bovenaf". | **FAIL** |

## 2. Harde eisen SPRITE_NORM

| # | Eis | Oordeel | Waarom |
|---|---|---|---|
| 1 | Leest op 1× als echte Pokémon | **FAIL** (alleen door de kené) | Naast Lairon, Aipom, Sableye en Grumpig leest hij als gehurkte aap met maankop. De rug leest door de ribbel-kené als gesegmenteerd schild. |
| 2 | 3/4 links-voor, kop meer naar de kijker | PASS | lijf 40°, kop 80° (A2); twee ogen met de snoet ertussen |
| 3 | Ledematen tellen | PASS | nabije hand, verre hand, achtervoet en staart zijn allemaal vast aan het lijf (bevroren in r6) |
| 4 | Geen Escher | PASS | De kop ligt voor het lijf. Er loopt een eigen kruinlijn over de maan (y35 x14–17, y36 x12–13 en x18–19), met 1 px violet ertussen. |
| 5 | Curven, geen doos | PASS (techniek) | De kruin is nu een boog. Rechte omtrekstukken zitten alleen in het bevroren silhouet (zie "Voor Jordi"). |
| 6 | Kop | PASS | fase 2, lijf naar verhouding groot |
| 7 | Ogen geïntegreerd | PASS | Zwart bovenlid (y43), iris donker boven (9) en licht onder (B), glans (8) linksboven, ronde pupil. Het verre oog heeft een eigen schaduw (A binnen, tegen 9 buiten bij het nabije), dus geen kopie meer (17 van 49 px verschillen). Rood en starend, zoals Jordi vroeg. |
| 8 | Kenmerken op 1× leesbaar | **FAIL** | De maan, spiraal, ogen en handen lezen. De kené leest niet (zie regels 1–6). |
| 9 | Omlijning, licht linksboven, open randen | PASS | Zwart-aandeel van de rand is 0,46 (112 zwart, 113 donkerviolet, 19 bruin E bij het crème). Er zijn 0 open randen in de violette groep. De crème vingers hebben hun groepsomlijning E (zie "Voor Jordi"). Het licht valt van linksboven, ook op de maan. |
| 10 | Geen Chernobyl | PASS | Het gezicht is rustig en de mond neutraal. Er zijn geen beige vlakken uit het niets. |
| 11 | Patronen dik (≥ 3 px, geen 1-px-lijnen) | **FAIL** | zie regel 3 |

## 3. §0-checklist SPRITING.md
| # | Punt | Oordeel |
|---|---|---|
| 1 | lijf én blik diagonaal | PASS |
| 2 | ledematen, oren en ogen geteld en verbonden | PASS |
| 3 | geen rechte lijnen | PASS in de kleurlaag; in het silhouet zie "Voor Jordi" |
| 4 | ogen geïntegreerd, verre oog geen kopie | PASS |
| 5 | silhouet leest als de soort | PASS (aap; geen Aipom door de maan, de ogen en de spiraal) |
| 6 | formaat | PASS: 1459 px |
| 7 | pose niet stijf | PASS |

## 4. Per onderdeel (op 1×)
- **Kop:** PASS. Het is een eigen bol met een boogkruin.
- **Maan:** PASS. Hij leest als witte sikkel met de punten omlaag langs de ogen. Op 4× is hij netjes, met lila schaduw aan de rechterkant.
- **Ogen:** PASS, rood en starend.
- **Snoet en mond:** PASS. De lichte snoet en de mond (2 px) zijn neutraal.
- **Oortjes:** PASS, kleine bultjes, bevroren.
- **Handen:** PASS (bevroren). Op 1× lezen de vingertoppen als crème.
- **Achtervoet:** PASS.
- **Spiraal:** PASS. Hij leest als krul van meer dan één slag.
- **Kené:** **FAIL.**
- **Volume:** PASS. De bol is licht linksboven en heeft schaduw rechtsonder, met een donkere ondertint (3). Alleen de kené breekt het volume.
- **Selout:** PASS. Bovenop is de rand donkerviolet (2), rechts en onder zwart (1).

## 5. FAIL: zone, wat te doen, pixelbudget
**F1 Kené opnieuw als vlak, gebogen patroon** (zone: lijf x17–49, y24–50; niet in de kop x≤24/y≥36, niet in de armen, de staart of de omlijning).

**Budget:** ±150–190 px. De alpha-diff blijft 0 en buiten de zone verandert 0 px.

1. **Kleur:**
   - Op de lichtkant: alleen **7** (lichtlila), vlak.
   - Waar het lijf in de schaduw ligt (rechts en onder de evenaar): de hele band in **6**.
   - Geen 5-rand en geen 7-randje per band: weg met de bevel.
   - Het vachthooglicht 5 mag de band niet raken. Houd rond de banden 1 px basis 4 aan; de bol krijgt zijn hooglicht via het patroon en de 5-vlakken ernaast.
   - Het palet blijft gelijk.
2. **Vorm (naar het poppetje, `pop3d/poppetje_goedgekeurd_256.png`):**
   - **Middenlijn op de ruggengraat**, 3 px dik. Hij loopt vanaf achter de kop (±x19, y32) over de top van de bol (±x28, y26) tot de staartwortel (±x46, y31), en volgt de bovencontour op 1–2 px afstand.
   - Vanaf die lijn **3–4 zijbanden** omlaag over de nabije flank. Elk is 3 px dik, met één of twee treden van 2 px. Tussen de banden zit 3–4 px vacht.
   - De banden zijn **schuin en gebogen**: bovenaan liggen ze vlakker, lager staan ze steiler, zodat ze om de bol lopen.
   - Ze lopen door tot ±y44–48, en worden in de schaduw 6 en smaller (2 px aan het uiteinde mag).
   - Hun eindpunten liggen niet op één hoogte.
   - Op de verre kant, boven de middenlijn, alleen korte stompjes van 2–3 px. Dat geeft de "van bovenaf gecentreerd"-logica.
3. **Controle:**
   - Op 1× naast Linoone, Furret en Zigzagoon. Leest het als patroon, en niet als glans, ribbels of schild?
   - Meet de kleinste doorsnede: ≥ 3 px op de lichtkant, behalve aan de uiteinden.

## 6. Voor Jordi (geen FAIL: bevroren vorm of smaak)
- **Contrast van de kené:**
  - Binnen het palet is 7 het lichtste wat kan zonder wit. Leest dat nog te zacht, dan is een eigen patroonkleur de enige echte oplossing (regel 1). Denk aan een zilverig blauwlila, of een andere kleurtoon zoals het geel van Liepard op violet.
  - Daarvoor moet er een paletslot vrij komen. Een kandidaat is 15 (226,200,160), die nu maar 9 px van het crème gebruikt.
  - Jordi vroeg "rustiger dan de maan". Dat blijft zo zolang het geen wit is.
- **Maan:** de buitenrand valt samen met de kopcontour. Op 1× oogt hij daardoor een tikje als witte kap. Op 3× en hoger is het duidelijk een sikkel. D2 is gekozen, dus niet aangepast.
- **Rechte stukken in het bevroren silhouet:**
  - rugtop y25 x23–32: 10 px recht;
  - spiraallus x48 y14–19 en x51 y13–20, waardoor de lus een afgeronde rechthoek wordt;
  - voetzolen y60 x3–8 en x32–39.
- **Crème vingers:** de onderste rand (y60–62) is in E (bruin) in plaats van zwart, terwijl de schaduwkant volgens de regel zwart moet zijn. Het gaat om 8–10 px. De handen zijn bevroren, dus alleen op Jordi's woord.

## 7. Wat ik mat (`eindkeuring/meet_uitvoer.txt`)
- Pixels, palet en alpha:
  - 1459 px, 15 kleuren;
  - alpha-diff tegen `silhouet_bevroren.npy`: **0**.
- Randen en omlijning:
  - 244 randpixels, waarvan zwart 0,46;
  - (1+2) in de hele sprite: 0,243;
  - open randen: 0 in violet. De 19 "open" randpixels zijn allemaal E, de omlijning van de crème groep in de bevroren handen en voeten.
- Losse pixels: 69 (4-buren), bijna allemaal anti-aliasing in de spiraal, de maanrand en de crème vingers. In de kené zitten 5 losse 5-pixels (x36–37, y28–29; x45–47, y30–32), die horen bij de bevel.
- Kené:
  - 81 px in 6/7;
  - kleinste doorsnede: 1 px ×17, 2 px ×45, 3+ px ×19;
  - luminantie: basis 0,31, hooglicht 5 0,45, kené 6 0,58, kené 7 0,78, wit 0,97.
- Ogen: het verre oog verschilt in 17 van de 49 px van het nabije.
- Diff ronde 6 → 7: 148 px, allemaal in x17–46, y27–40.

## 8. Na het oordeel gelezen: `ronde4/KEURING.md` en `ronde7/NOTITIES.md`
- **Ronde 4-keuring:** de punten F2 (kruin), F3 (oogkopie) en F4 (handen) zijn sindsdien opgelost: de kruin is een boog en het verre oog heeft een eigen schaduw. Dat bevestigt mijn PASS daar. De kené was toen "krassen", nu "ribbels". Het probleem is verschoven van dikte naar opbouw.
- **NOTITIES r7:**
  - De maker noemt de banden "3 px dik". Dat klopt alleen als je de schaduwrand in 5 meetelt: de patroonkleur zelf is 2 px. Juist die rand in 5 plus het randje in 7 maakt de bevel. Het patroon verloopt dus als ribbel, en dat zie je op 1×.
  - "Rustiger dan het poppetje, want rustiger dan de maan" verklaart het lage contrast in kleurtoon, maar lost regel 1 niet op.
  - Mijn oordeel verandert niet: **TERUG op F1**.
