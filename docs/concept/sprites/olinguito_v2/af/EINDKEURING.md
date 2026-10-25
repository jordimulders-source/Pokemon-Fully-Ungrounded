# Eindkeuring olinguito v2 (Dark-starter, fase 1)

Gekeurd: `af/olinguito.png` (64×64, geïndexeerd). Dit bestand is pixel voor pixel gelijk aan `kleur/ronde4/olinguito.png` (0 px verschil). De alpha-diff met het silhouet van ronde 5 is ook 0.

Keurder: vers en onafhankelijk. Ik heb eerst zelf geoordeeld en daarna pas `kleur/ronde3/KEURING.md` gelezen.

Maatstaven:
- het ontwerp (`referenties/ONTWERP_GEKOZEN.png`) en `SPEC.md`;
- SPRITE_WERKWIJZE stap 3, SPRITE_NORM, SPRITE_OPDRACHT §2, FAKEMON_CHECKLIST (viervoeter), SPRITING §0–§8 plus de lessen en FAKEMON_DESIGN.

Vergeleken met 12 echte Gen 3-sprites, telkens het eerste frame met `normal.pal`, op 1×, 4× en 6–8×, op licht en op donker: Linoone, Zigzagoon, Poochyena, Mightyena, Sentret, Furret, Rattata, Raticate, Sneasel, Meowth, Aipom en Purrloin.

Vergelijkingsplaatje: `af/eindkeuring_vgl.png`.
- **Bovenaan:** de sprite op 6×, op licht en op donker, naast het ontwerp. De rode kaders markeren de punten uit de reparatielijst.
- **Daaronder:** alle 13 sprites op 4× (licht en donker) en op 1× (licht en donker).

Coördinaten staan als (x,y). Paletindex: 1 zwart, 2 masker, 3/4/5 lijf (omlijningsbasis, basis, licht), 6/7/8/9 kop (basis, licht, snoet/schaduw, omlijningsbasis), 10/11/12 oog, C/D klauw, E/F roze.

**De bevroren punten zijn als gegeven genomen:** silhouet, pose, maskerband, helderheid en snoet. Die heb ik alleen op technische netheid getoetst.

## Hoofdvraag
**Leest hij op 1× als een echte Gen 3-sprite, en is het het gekozen ontwerp? Ja.**

Op 1× staat hij geloofwaardig tussen Linoone, Raticate en Purrloin. Alle kenmerken van het ontwerp zijn er:
- de kogelkop met één rond oor en een klein ver oor;
- de zwarte band met het rode oog;
- de oudroze neus;
- de reikende voorpoot met twee lichte klauwen;
- roze voeten;
- de lange staart met een haak bovenaan.

Het kleurwerk is Game Freak-achtig:
- selout aan de lichte kant, zwart aan de schaduwkant, licht van linksboven;
- een gebogen kap op de dij als hooglicht;
- een bolle kop zonder rechte naden.

Wat nog niet klopt, is klein en ligt bijna allemaal in het bevroren silhouet (losse 1-px-haakjes in curven en een spriet aan de klauw). Daarnaast leest de verre voorpoot op 1× te zwak.

## Metingen
| | olinguito | referenties |
|---|---|---|
| oppervlak | 1174 px (box 52×56) | Zigzagoon 1127, Linoone 1089, Poochyena 989, Sentret 982, Purrloin 759 |
| kleuren zonder index 0 | 15 (alle 15 slots gebruikt) | 11–15 |
| index 0 | (152,208,160), `transparency=0`, komt niet in de figuur voor | – |
| aandeel zeer donker (luma < 40) | 0,203 | 0,05–0,29 (Purrloin en Meowth 0,286, Mightyena 0,48) |
| omtrek (243 px) | 149 zwart, 71 lijf-omlijningsbasis, 23 kop-omlijningsbasis | – |
| open randen | **0** | – |
| tintstappen lijf (luma) | 105 / 78 / 55 / 18 | Purrloin 96 / 73 / 38; Sentret 144 / 125 / 102 / 73 |
| kophoogte | y 17–41 = 25/56 = 45% | fase 1: 40–55% |
| kopoppervlak | ±36% | ≤ 41% |

## SPRITE_NORM: de 10 harde eisen
| # | Eis | Oordeel | Zone en reden |
|---|---|---|---|
| 1 | Leest op 1× als een Pokémon | PASS | Zie de hoofdvraag. |
| 2 | 3/4 links-voor, lange snuit dus één oog | PASS | Eén oog. De neus zit vooraan links. Het lijf loopt schuin weg. De kop draait meer naar de kijker. |
| 3 | Alle ledematen tellen op 1× | **FAIL** | De verre voorpoot is een strook van 2 px (`4 3`, x 24–26, y 43–49) naast de nabije poot. Het pootje eindigt in een diagonaal lijntje van 1 px roze: (26,48), (25,49) en (25,50). Op 4× tel je hem nog, op 1× leest de voorpoot als één ledemaat met een schaduwstreep, dus je telt 3 poten. Dit is de les uit SPRITE_OPDRACHT §4: "staat er, maar leest als schaduw". Reparatie 1. |
| 4 | Geen Escher | PASS | De verre achterpoot (x 33–38) staat links van en hoger dan de nabije (voet y 49 tegen 51/52). De nabije delen liggen over de verre. |
| 5 | Lijf over een skelet, geen rechte lijnen ≥ 4 px waar het dier rond is | **FAIL** (silhouet) | Het kleurwerk is schoon. In het bevroren silhouet zitten drie haakjes ("besluiteloosheid", SPRITING §3). Elk is 1 px:<br>• **achterkant van de kop:** een inkeping op (29,24); de rand loopt x 29, 29, 29, 29, 29, **28**, 29, 29, 29.<br>• **voorhoofd:** de runs van de omtrek zijn 2, 2, 3, **2**, 3, 5 (x 12 → 7); de run op x 9 (y 30–31) is te kort.<br>• **staart, linkerrand:** de runs zijn 5, 4, **2, 3**, 1 (y 13–27) in plaats van aflopend.<br>Reparatie 3. De lange rechte stukken (kin y 41, 8 px; rug y 27, 7 px) zijn de vorm van het bevroren silhouet; zie "voor Jordi". |
| 6 | Kop fase 1 40–55%, oppervlak ≤ 41% | PASS | 45% van de hoogte, ±36% van het oppervlak. |
| 7 | Ogen geïntegreerd | PASS | Het oog is 3×2 (x 20–22, y 32–33). De glans zit linksboven, donkerrood erboven, lichter rood midden-onder, en het masker vormt het bovenlid. Het boogje `999` (y 29) ligt direct op de maskerrand en zweeft dus niet. |
| 8 | Kenmerken op 1× leesbaar | PASS | Masker, staarthaak, oor en klauwen lezen. De klauwen hebben per stuk licht (C) en schaduw (D) en eindigen onderaan iets verticaal. Zie ook "voor Jordi". |
| 9 | Omlijning per kleurgroep, zwart aan de schaduwkant, geen open randen | PASS | 0 open randen, gescand per randpixel. Lijf, staart, poten en de kop bovenaan hebben aan de lichte kant de omlijningsbasis (3/9); rechts en onder zijn ze zwart. |
| 10 | Geen Chernobyl, geen losse of zwevende delen | **FAIL** (1 px) | (19,59) is een losse zwarte pixel onder de zwarte rand van de rechterklauw (17–19,58). Op 6× en 8× leest hij als een sprietje, zoals de les "losse zwarte 1-px-sprietjes lezen als vliegjes". Hij zit in het silhouet. Reparatie 2. |

## SPRITE_WERKWIJZE stap 3: valkuilen
| Valkuil | Oordeel | Toelichting |
|---|---|---|
| Kop als helm | PASS | De naad tussen grijs en kruin is een boog, de schaduw achteraan loopt verspringend uit en het masker heeft geen bruin randje meer. Op 1× leest de kop als een bolle schedel met een band erover. Een lichte vizier-indruk blijft over door het vlak 7 linksboven en door de dikke band; die band is goedgekeurd. |
| Ruis | PASS | Grote rustige vlakken. De 12 pixels zonder gelijke buur zijn allemaal bedoeld: glans, oog, neushooglicht, staartschaduw, de hoek van de staartkrul en de dijlijn. |
| Plat (2D) | PASS | De kop is bol, met licht linksboven en schaduw rechts. De dij heeft een gebogen kap. Staart en poten zijn cilinders met een lichte en een donkere kant. |
| Mini-oog op een donkere kop | PASS | Glans plus een lichtere iris tegenover de glans; geen witte stip. |
| Verre ledematen in de schaduwtint, gescheiden met de omlijningsbasis | PASS (achterpoot) / FAIL (voorpoot, zie eis 3) | De scheiding is goed (3, niet zwart). De verre voorpoot is alleen te smal om op 1× te lezen. |
| Klauwen als gebogen haakjes met licht/schaduw | PASS, met een kanttekening | Licht en schaduw zijn er, en de punten buigen 1 rij omlaag. Het blijft wel een 1-op-1-diagonaal uit het silhouet (zie "voor Jordi"). |
| Open randen en losse pixels | PASS / FAIL | 0 open randen; 1 losse spriet (eis 10). |

## FAKEMON_CHECKLIST (viervoeter)
| # | Oordeel | Toelichting |
|---|---|---|
| A1 silhouet leest | PASS | Bevroren; leest als een marter of olinguito. |
| A2 dominant kenmerk breekt de omtrek | PASS | De staarthaak en de klauwen. |
| A3 diagonale compositie | PASS | De kop links, de staart rechtsboven als tegenwicht. |
| A5 niet symmetrisch | PASS | – |
| A6 geen zuil/doos/stok | PASS (kleurwerk) | De staart heeft maximaal 5 rijen evenwijdige randen (y 13–17), onder de grens van 6. |
| B1/B2/B4 | PASS | Lange snuit, één oog, oog-as en snuit-as wijzen links-voor. |
| B5 oren volgen de draai | PASS | Het verre oor is een klein bultje op (17–19,18–19), het nabije oor rond met een lichte binnenkant. |
| B7 gezicht compleet | PASS | Oog, neus, en een mondlijntje op (9–10,38). |
| C1 alles geteld | **FAIL** | De verre voorpoot, zie eis 3. |
| C2 4 voethoogtes | PASS | y 52, 50, 49 en 51/52. |
| C3/C5 aanhechting | PASS | – |
| C4 gewrichten | voor Jordi | De nabije voorpoot is een rechte reikende plank, in het bevroren silhouet. |
| C8 staart | PASS | Hij sluit aan op de heup en buigt met een haak. |
| D1/D4 formaat | voor Jordi | 1174 px en 52 px breed; bevroren, vergelijkbaar met Zigzagoon (1127 px, 50 px breed). |
| E1 verre kant donkerder | PASS | – |
| E2 overlap in de omlijningsbasis | PASS | – |
| E3 zwart-aandeel | PASS | 0,20, binnen de band; voor een Dark-type mag het hoger. |

## SPRITING §0–§8
- **§0 checklist (1–7):** PASS, behalve 2 (verre voorpoot leest niet op 1×).
- **§1/§2 met de hand:** PASS. Geen tekenen van filters of automatische shading.
- **§3 curven:** FAIL, op de 3 silhouethaakjes van 1 px. De kleurnaden zijn schoon.
- **§4 palet:** PASS. Per groep 3 tinten plus omlijning, met gelijke stappen.
  - **Kanttekening:** masker 2 (36,23,18) en zwart 1 (26,15,11) zijn bijna gelijk (luma 26 tegen 18). Daardoor loopt de band vooraan zonder rand de omtrek in, zoals bij Zigzagoon. Dat is bewust en hoort bij de goedgekeurde band.
- **§5 licht:** PASS. Licht van linksboven, consequent.
- **§6 ogen:** PASS.
- **§7 vacht:** PASS. Glad lijf, past bij een simpele Pokémon.
- **§8 omlijning:** PASS. Selout, 1 px breed, geen anti-aliasing aan de buitenkant.
  - **Klein schoonheidsfoutje:** (46,28) is zwart op de bovenkant van de rug. Het ligt in de hoek tussen rug en staart, en daar mag slagschaduw.

## Technisch
| Punt | Oordeel |
|---|---|
| 64×64, P-modus, `transparency=0`, 16 slots | PASS |
| Index 0 transparant, niet in de figuur | PASS |
| Open randen | PASS (0) |
| Losse pixels | FAIL: (19,59) |
| Jaggies in curven | FAIL: (29,24), voorhoofd x 9, staart links y 22–26 (allemaal silhouet) |
| Banding | PASS. De staart is een buis met een gelijke doorsnede, zoals de staarten van Rattata en Raticate. Er loopt geen kussenstrook langs de omtrek. |
| Rechte lijnen in ronde vormen (kleurwerk) | PASS. De maskerranden zijn de goedgekeurde band. |
| Zwart-aandeel | PASS (0,20) |
| Frame 2, rug, icoon, shiny | Nog te doen (volgens SPEC). Dit valt buiten deze keuring. |

## Naast de vorige keuring (ronde 3)
Ronde 3 was "NIET GOED" met 6 reparaties (A–F). Op deze versie:

| Punt uit ronde 3 | Nu |
|---|---|
| A. Kop als helm, rechte naden, bruin lijntje boven het masker | **Opgelost.** De naad is een boog, het lijntje is weg en de banden achteraan lopen uit. De dikte van het masker is nu door Jordi goedgekeurd. |
| B. Verre voorpoot `KbK` (1 px tussen zwart) | **Half opgelost.** De scheiding is nu de omlijningsbasis en de poot is 2 px breed. Op 1× leest hij nog niet als poot; dat blijft mijn enige kleur-FAIL. |
| C. Klauwen als eetstokjes | **Grotendeels opgelost.** Ze hebben licht en schaduw en de punten buigen omlaag. De rechte diagonaal zit in het silhouet. |
| D. Dij als streep | **Opgelost.** Nu een gebogen kap. |
| E. 11 open randen | **Opgelost** (0). |
| F. 2 losse pixels | **Opgelost.** |
| Optioneel: maskertint los van zwart | Niet gedaan; dit valt nu onder de goedgekeurde band (voor Jordi). |

**Wat ik vond en ronde 3 niet:**
- de losse spriet (19,59);
- de drie 1-px-haakjes in het silhouet.

Ronde 3 toetste het silhouet bewust niet, omdat het bevroren was. Dezelfde les als bij de kolibrie: een verse keurder vindt nog randdetails.

**Waar ik het niet mee eens ben:** ronde 3 telde de helderheid en de maskerdikte als FAIL. Jordi heeft beide goedgekeurd, dus die tellen hier niet meer.

## Eindoordeel: **NIET AF** (bijna af: één kleine schoonmaakronde van ≤ 7 px)
Twijfel is FAIL. De sprite is als ontwerp en als Gen 3-sprite geslaagd, maar vier kleine punten staan open.

**De reparaties raken bijna allemaal het bevroren silhouet (±1 px elk). Volgens SPRITE_WERKWIJZE stap 4.3 is dat een vraag aan Jordi**, geen opdracht die de maker zelf mag uitvoeren. Alleen reparatie 1 blijft binnen het silhouet.

### Reparatielijst (op prioriteit)
1. **Verre voorpoot leesbaar op 1×.**
   - Wat: maak van het pootje een roze vlekje in de schaduwtint F, in plaats van een diagonaal lijntje van 1 px: (25,48) 3 → F en (24,49) 4 → F.
   - (24,50) blijft 3 als scheiding met de nabije voet.
   - Budget: 2 px. Alpha-diff blijft 0.
   - Toets: op 1× tel je twee voorpoten.
2. **Losse spriet aan de klauw.**
   - Wat: (19,59) wordt transparant.
   - Budget: −1 px silhouet, dus Jordi's akkoord nodig.
3. **Haakjes in curven** (elk ±1 px silhouet, dus Jordi's akkoord nodig):
   - **Achterkant van de kop:** (29,24) wordt nieuw zwart en (28,24) gaat van 1 naar 3. De rand wordt dan x 29 van y 19 tot 27.
   - **Voorhoofd:** (9,29) wordt nieuw 9 en (10,29) gaat van 9 naar 6. De runs worden dan 2, 2, 2, 3, 3, 5.
   - **Staart, linkerrand:** (51,24) wordt transparant en (52,24) gaat van 5 naar 3. De runs worden dan 5, 4, 3, 2, 1.

Ik heb alle reparaties uit 1–3 samen als proef doorgerekend, buiten de repo. Resultaat: 0 open randen en geen nieuwe losse pixels.

Na de reparaties:
- opnieuw scannen op open randen (moet 0 blijven);
- 1× naast Linoone en Zigzagoon zetten;
- dan is hij voor mij **AF**.

Kiest Jordi ervoor het silhouet niet meer aan te raken, dan is alleen reparatie 1 nodig. De punten 2 en 3 zijn op 1× vrijwel onzichtbaar.

## Voor Jordi (smaak, geen afkeur)
- **Klauwen:** twee evenwijdige, rechte diagonalen (uit het silhouet). In het ontwerp zijn het gebogen haken. Een echte haak (de onderste 2 rijen recht omlaag) kost ±4 px silhouet. Wil je dat?
- **Maskerband:** de bovenrand heeft een recht stuk van 8 px (y 31, x 10–17), en de band versmelt vooraan met de zwarte omtrek (maskertint ≈ zwart). Een iets lichtere maskertint, bijvoorbeeld ±(52,36,30), maakt de voorkant van de kop leesbaarder zonder de band te veranderen. Dit is jouw goedgekeurde band, dus alleen als je het wilt.
- **Kin en snuitfront:** de onderkant van de kaak is een recht stuk van 8 px (y 41) en de voorkant van de snuit 5 px verticaal (x 7). Het ontwerp is daar ronder. Dat zit in het bevroren silhouet.
- **Nabije voorpoot zonder elleboog** (rechte reikende plank): uit het silhouet. Bij een reikende pose is dat verdedigbaar.
- **Formaat:** 1174 px en 52 px breed ligt boven de norm voor fase 1 (700–950 px, ≤ 48 px). Het is bevroren en Zigzagoon is even groot.
- **Kleurstappen:** het lijf heeft stappen van ±25 luma, net als Purrloin. R/S gebruikt vaak meer hooglicht (Sentret, Raticate). De helderheid is goedgekeurd, dus dit is alleen een observatie.
