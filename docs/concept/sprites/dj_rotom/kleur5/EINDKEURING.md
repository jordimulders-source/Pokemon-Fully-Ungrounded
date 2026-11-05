# DJ Rotom kleur5: eindkeuring (5 nov)

Gekeurd: `dj_rotom.png` (64×64, P-modus, transparency=0). Vel: `eindkeuring_vel.png`: 1× en 3× op licht en donker, naast Rotom, Heat, Wash, Frost, Fan en Mow (frame 1) en Magnezone, Bronzong, Klinklang en Cofagrigus.
Mijn oordeel stond vast vóór ik `SPEC.md`, `kleur2/KEURING.md`, `kleur4/CONSISTENTIE.md` en `kleur5/NOTITIES.md` las.

## 1. Hoofdoordeel: **PASS**
- **Op 1× staat hij naast de zes game-Rotoms als een vorm uit dezelfde game.** De kenmerken die de familie bepalen zijn er allemaal:
  - exact hetzelfde oranje;
  - een gloed van 2 tinten zonder zwarte buitenlijn;
  - zwart aan de schaduwkant, donkerst oranje aan de lichte kant;
  - een vrije spits met een lichtstreep;
  - ogen als het Frost-sjabloon;
  - een grijns met losse tandjes;
  - het licht van linksboven.
- **Massa:** 1953 px, box 60×56. Dat valt binnen de familie (Frost 2173, Wash 1681) en naast Magnezone (1649), Bronzong (1775) en Klinklang (2417) is hij niet te groot of te klein.
- **Herkenbaarheid als DJ Rotom uit de bron:** de speakers lezen meteen, de linker laag en de rechter hoog met twee conussen. Ook het zwarte display met de groene equalizer, het snoer, de grijns en de bliksem uit de spits lezen.
- **Wat op 1× afwijkt van de familie:** hij is de enige die zwaar en laag oogt, door de navy fronten, de bleke gloed en de lage plek in het vak. Dat zijn Jordi's eigen keuzes. Ze staan als vraag in §6 en tellen niet mee.

## 2. Harde eisen (SPRITE_NORM), bij een apparaat naar analogie
| # | eis | oordeel | reden |
|---|---|---|---|
| 1 | leest op 1× als een echte Pokémon | PASS | Staat tussen 10 echte sprites (6 Rotoms + 4 apparaten/kasten) zonder te schuren, op licht en donker. |
| 2 | 3/4 naar links-voor | PASS | Rechts zijn de zijvlakken donker (kop x33–34, rechterspeaker x54–59). De nabije speaker is groter, de verre lager en kleiner. De boven- en onderlijnen stijgen naar rechts. Het gezicht kijkt naar de kijker. |
| 3 | ledematen (hier: plasma en kasten) | PASS | De bliksem hangt via de gloed aan de spits, zoals het plasma van de game-Rotoms. De kasten sluiten aan op de kop: de naden lopen op x15 en x35. Er zijn geen zwevende delen. |
| 4 | geen Escher | PASS | Wat dichtbij is overlapt wat ver weg is: de kop staat vóór de linkerspeaker, de rechterspeaker vóór de kop. Het snoer loopt over de naad heen. |
| 5 | skelet, curven | PASS | Het zijn kasten, dus rechte lijnen mogen (Frost doet het ook). Hoeken en dakranden lopen als trap mee met het perspectief. |
| 6 | kop | PASS | Het middenstuk is groter, zoals Jordi vroeg. Het gezicht staat op de as van de spits, zoals bij alle Rotoms. |
| 7 | ogen | PASS | Met een script vergeleken: ze zijn pixel voor pixel het Frost-oog (W-schuinte boven, iris donker boven en licht onder, K aan de zijkant, grijs plus wit onderaan), alleen in teal. |
| 8 | kenmerken op 1× leesbaar | PASS | De bliksem, speakers, conussen, equalizer en grijns lezen op 1×. De noot (x24–28, y8–13: steel x26, vlag (27,8)/(28,9), kop x24–26 y12–13) is op 1× een witte kern in de bliksem en op 2–3× een ♪. Dat werkt zoals de witte plasmakern bij de game-vormen. |
| 9 | omlijning, licht, open randen | PASS | Er zijn 0 open randen. Zwart ligt alleen aan de schaduwkant (rechts en onder), donkerst oranje aan de lichte kant, en het licht komt van linksboven. Alleen de naden zijn bruin in plaats van zwart, zie reparatie A. |
| 10 | geen Chernobyl | PASS | Eén aaneengesloten vorm, geen beige vlakken uit het niets, een heel gezicht. |

## 3. Technische checks (script)
- **Formaat:** 64×64, P-modus, transparency=0. Index 0 is 152,208,160, gelijk aan de game-Rotoms. Geen pixels op de rand van het vak. Box x2–61, y7–62.
- **Kleuren:** 15 plus transparant, dus alle 16 slots zijn in gebruik (er is geen vrij slot meer).
- **Game-waarden, exact gelijk aan alle zes de Rotoms:**
  - oranje: 248,168,128 / 232,112,40 / 192,72,24 / 120,56,32;
  - zwart: 16,16,16;
  - wit: 248,248,248;
  - grijs: 184,184,184.
- **Open randen:** 0. Een open rand is hier een niet-gloedkleur (index 4–15) naast transparant of naast de vakrand.
- **Losse pixels** (geen 4-buur met dezelfde index): 76, alle bewust.
  - Trappixels van de gloed langs diagonale randen, bijvoorbeeld (24,8), (22,11), (16,31), (60,60).
  - De witte noot: (28,9).
  - De punt van de spits: (26,23), bruin.
  - De hoeken van de contour: (55,27) zwart, (13,37) bruin (de dakhoek van de linkerspeaker in perspectief), (17,33) bruin.
  - De ogen: het Frost-sjabloon, W/t/T/K/grijs.
  - De twee tanden: (23,43) en (25,43).
  - De ringen en glanzen van de conussen: (9,43), (8,50), (44,38), (44,49) en de navy hoekjes.
  - De toppen van de equalizerbalkjes.
  - Allemaal hangen ze diagonaal aan hun groep of zijn ze bedoeld als losse glans. Er is geen ruis.
- **Gloed:** de buitenste ring is index 1 en daarbinnen ligt index 2, net als bij alle zes game-Rotoms (2 tinten, ±2 px dik).

## 4. Wat de eerdere keurders misten, of waar ik het oneens ben
- **Kleur2-keuring, eis 8 (de noot):** die is opgelost. Ik ben het niet eens dat de noot op 1× als noot moet lezen. Als witte kern werkt hij op 1× juist goed, en vanaf 2× leest hij als noot.
- **Consistentie kleur4, reparatie 6 (zwarte naden)** is in kleur5 niet uitgevoerd en staat nog open. De game zet zwart tussen volumes (de deur van Frost, kop tegen maaier bij Mow). Bij DJ is de naad bruin (x15 y39–56 en x35 y32–58). Op 1× leest de scheiding toch goed, omdat er donker oranje (f) aan weerszijden ligt. Daarom alleen aanbevolen (A).
- **Gemist: equalizer en shiny.** De toppen van de balkjes gebruiken index 2, de lichte gloedtint, op (23,50), (27,50), (21,51) en (25,52). In het shiny-recept van de game wordt index 2 perzik (240,200,160) en blijft index 14 groen. In de shiny krijgt de equalizer dan **perzikkleurige toppen op groene balkjes**. Kleur4 merkte op dat de balkjes perzik worden, maar niet dat ze tweekleurig uiteenvallen. Er is geen vrij paletslot. Dit moet beslist worden vóór de shiny (B).
- **Gemist: het palet zit vol** (16/16). Frame 2, shiny en rug moeten met deze 15 kleuren toe. Dat is geen fout, maar houd het in gedachten bij frame 2 (geen nieuwe tint voor de pompende conussen).
- **Kleur2, eis 2 (de kop doet niet mee in 3/4):** is opgelost. De kop heeft nu een eigen zijvlak (x33–34 f) en rechts naast het rechteroog blijft oranje over.
- Verder ben ik het eens met kleur5/NOTITIES: de contourladder, de spits, de tanden, het hooglicht als vlekjes en het palet zijn goed uitgevoerd.

## 5. Reparaties
Voor "af" (frame 1) is **niets nodig**.

| # | reparatie | coördinaten | nodig vóór "af"? |
|---|---|---|---|
| A | Naden zwart, zoals Frost/Mow: index 7 → 8 op de naad tussen de volumes. Kijk daarna op 1× of het niet te zwaar wordt naast de navy fronten; zo ja, alleen de onderste helft. | x15 y39–56 (achter de linkerspeaker); x35 y32–58 (kop tegen de rechterspeaker). Het snoer op (15,51) is al zwart. ±45 px. | Nee, aanbevolen (het enige stijlpunt dat nog van de familie afwijkt) |
| B | Equalizer losmaken van de gloedindex, zodat de shiny klopt: de toppen van index 2 naar 14 (dan zijn de balkjes één groen) of naar 13 (licht teal, blijft gelijk in de shiny). | (23,50), (27,50), (21,51), (25,52): 4 px. | Nee, vóór shiny.pal |

## 6. Vragen voor Jordi (bewuste keuzes; geen fout)
- **Gloed en speakers:** op 1× is DJ de enige met een bleke gloed en (bijna) zwarte vlakken. Daardoor oogt hij naast de felle game-gloeden iets zwaarder en doffer. Blijft dat zo (trouw aan de bron)?
- **Plek in het vak:** hij zit laag (bodem y62, zwaartepunt ±y43, tegen ±y33 bij de rest). Bij het invoeren via `enemyMonElevation` laten zweven, net als de andere Rotoms?
