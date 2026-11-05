# Eindkeuring nachtaap fase 2, kleur ronde 11 (onafhankelijke keurder, 3 nov)

**Oordeel: TERUG.** Er zijn twee kleine FAILs, samen ±14 px:
- **F1, de achterste wig.** Jordi: "de achterste lijn bij de staart is nu wel slordig". Dat klopt: in de wig zitten licht en lila door elkaar, en er staat een losse lichte pixel in.
- **F2, de kin.** De onderkant van de kop is een rechte zwarte lijn van 12–13 px, met een verticale rechterflank. Daardoor oogt de kop op 1× als een doosje.

De rest is in orde. De wiggen 1 en 2 zijn een duidelijke verbetering ten opzichte van de kené, en leesbaar op 1×.

Gekeurd: `nachtaap.png` + `normal.pal`. Vel: `eindkeuring_vgl.png`. Het toont de nachtaap, fase 1, Growlithe, Slakoth, Vigoroth, Lairon, Sableye, Misdreavus, Espurr, Aipom, Grumpig, Natu, Abra en Zigzagoon, op 3× en 1×, licht en donker. Uitsneden staan in `eindkeuring/` (`kop16.png`, `rug14.png`, `achterwig24.png`, `staart16.png`, `poten12.png`, `zoom8_*.png`).

## 1. Harde eisen SPRITE_NORM

| # | Eis | Oordeel | Waarom |
|---|---|---|---|
| 1 | Leest op 1× als een echte Pokémon | PASS | Naast Lairon, Slakoth en Sableye leest hij als een gehurkt, gestreept Pokémon met een maankop en een krulstaart. |
| 2 | 3/4 links-voor, kop meer naar de kijker | PASS | Lijf 40°, kop 80° (A2, bevroren). Er zijn twee ogen met de snoet ertussen. |
| 3 | Ledematen tellen | PASS | Nabije hand, verre hand, achtervoet en staart zijn allemaal verbonden (r6, bevroren). |
| 4 | Geen Escher | PASS | De kop ligt voor het lijf, met een eigen kruinlijn (y35–37). |
| 5 | Curven, geen doos, geen recht ≥ 4 px in rond | **FAIL** (F2) | De kinlijn y54 x9–20 is 12 px recht (zwart). De rechter kopflank x25 y42–47 is 6 px verticaal recht, met x26 y38–41 erboven. De linkerflank x4 y42–49 is ook recht, maar die hoort bij het bevroren silhouet. Samen vormen ze op 1× een afgeronde rechthoek. |
| 6 | Kop | PASS | ±19 van de 55 rijen. Fase 2, dus het lijf is groter. |
| 7 | Ogen geïntegreerd | PASS (bevroren r10) | Zwart vlak bovenlid y43, iris donker boven en licht onder, glans 8, ronde pupil. Starend en rood. |
| 8 | Kenmerken op 1× leesbaar | PASS | De maan, de ogen, de spiraal, drie wiggen en de crème vingers lezen alle op 1×. |
| 9 | Omlijning, licht linksboven, open randen | PASS | Het zwart-aandeel van de rand is 0,46. Er zijn 0 open randen in violet. De 19 "open" randpixels zijn allemaal E, de omlijning van de crème groep in de bevroren handen en voeten. |
| 10 | Geen Chernobyl | PASS | Het gezicht is rustig en de mond neutraal. Er zijn geen vlakken uit het niets. |
| P | Patroonregels (dik, eigen kleurgroep, vlak, geen bevel, loopt door tot schaduw/contour, eigen logica) | **FAIL** (F1, alleen wig 3) | Wig 1 en 2 voldoen aan alle regels: F (168,196,236) is een eigen toon, de wiggen zijn vlak, 3–8 px breed, zonder bevel, en worden in de schaduw 6. Wig 3 voldoet niet, zie F1. |

## 2. §0-checklist SPRITING.md
| # | Punt | Oordeel |
|---|---|---|
| 1 | Lijf én blik diagonaal | PASS |
| 2 | Ledematen, oren en ogen geteld en verbonden | PASS |
| 3 | Geen rechte lijnen | **FAIL** (F2, de kin). Over de rest van het silhouet: zie "Voor Jordi". |
| 4 | Ogen geïntegreerd, verre oog geen kopie | PASS |
| 5 | Silhouet leest als de soort | PASS, met een kanttekening (zie "Voor Jordi": aap of lori) |
| 6 | Formaat | PASS: 1459 px = 1,54× fase 1 |
| 7 | Pose niet stijf | PASS |

## 3. Per onderdeel (op 1×)
- **Kop:** **FAIL** (F2), alleen de kin en de rechterflank.
- **Maan:** PASS op techniek. Hij is wit, met schaduw in 7 rechts, de holte tussen de ogen in 4 en de punten langs de ogen omlaag. Op 1× leest hij eerder als witte kap of hoofdband dan als sikkel; zie "Voor Jordi".
- **Ogen:** PASS. Bevroren, en sterk.
- **Snoet en mond:** PASS. De lichte neusbrug loopt van x11 tot x16. Neus y50, mond y52: neutraal.
- **Oortjes:** PASS. Bevroren; het nabije is een knopje x4–6 y37–40, het verre zit op x24 y39–40.
- **Handen:** PASS. Bevroren; de crème vingertoppen lezen.
- **Achtervoet:** PASS.
- **Spiraal:** PASS. Hij leest als krul. De binnenwinding is dun (1 px kleur tussen de omlijning), wat bij een staartpunt kan (Aipom).
- **Wig 1 (voor):** PASS. Hij begint breed op de rugtop (6–8 px) en loopt dan als steel van 3 px omlaag tot y38. Op 1× is het een duidelijke lichte streep die om de bol buigt.
- **Wig 2 (midden):** PASS, met een kanttekening. Op y33–34 loopt hij door de schaduwplooi bij de staartwortel en wordt hij daar 6. Daarna is hij weer F. Dat is fysiek juist. Op 1× zie je een kleine knik, geen breuk.
- **Wig 3 (achter, staartwortel):** **FAIL** (F1).
- **Volume:** PASS. Licht linksboven, schaduw 3 rechtsonder.
- **Selout:** PASS. Bovenop donkerviolet 2, rechts en onder zwart 1.

**Leest hij als Psychic?** Ja, matig. Het violet, de spiraal en de starende rode ogen werken. De rode ogen en het donkere violet trekken ook richting Dark/Ghost (Sableye), maar dat past bij "lijkt gevaarlijk, maar is zachtaardig".

**Als volgende fase van fase 1?** Ja. Hij houdt het violet, de spiraalstaart, de oortjes en de crème tenen. De kop is bewust anders.

**Als aap?** Redelijk. In de Lairon-pose leest hij eerder als lori of maki dan als aap. De spiraal en de handen redden het.

## 4. FAILs: zone, wat te doen, budget

**F1: achterste wig (zone x42–46, y34–38). Budget: 4 px.**

Wat er nu staat:
```
y34  x42-43 = 66 (lila), x44-45 = FF (licht)
y35  x43 = F (losse pixel), x44-45 = 66
y36  x44-46 = 666
y37  x45-46 = 66
y38  x46 = 6
```
Het licht zit rechtsboven en het lila linksonder; licht en schaduw staan dus andersom dan in de rest van de sprite. De losse F op (43,35) maakt er een dambord van. Bovendien steekt (42,34) als uitstulping naar links, richting de lila plooi van wig 2.

De hele wig ligt in de schaduw van de staartwortel. Volgens de patroonregel ("de band als geheel geschaduwd") wordt hij dus vlak 6, net als het schaduwdeel van wig 2. Wijzig deze vier pixels:

| Pixel | Nu | Wordt |
|---|---|---|
| (42,34) | 6 | 3 |
| (44,34) | F | 6 |
| (45,34) | F | 6 |
| (43,35) | F | 6 |

Daarmee wordt de wig per rij 3-3-3-2-1 breed (x43–45, 43–45, 44–46, 45–46, 46): een schone, tapse lila wig die parallel loopt aan wig 2. Een proef staat in `eindkeuring/proef_w3_voor_na.png` (alleen een vergelijkingsplaatje; de sprite zelf is niet gewijzigd).

Wil de maker liever de top in F houden: dan alleen de bovenste rij x43–45 F, nooit F en 6 naast elkaar in dezelfde rij. Volgens mij leest dat als een glansrandje, dus ik raad het vlakke lila aan.

**F2: kin (zone x8–26, y52–55). Budget: ≤ 10 px.** Het silhouet en de handen blijven ongewijzigd (alpha-diff 0).
- Maak de onderrand van de kop rond, in plaats van 2-13-2:
  - y54: de zwarte lijn blijft van x10 tot x18;
  - x8–9 en x19–20 gaan één rij omhoog naar y53, zodat de lijn verloopt als 1-2-…-2-1;
  - de vrijgekomen pixels op y54 krijgen de kleur van de arm eronder (3).
- Breek de rechterflank x25 y42–47: één pixel inspringen op y46–47 (x24). Dan loopt de flank naar de kin toe als curve en niet als een verticale wand.
- Controle: op 1× naast Slakoth en Grumpig moet de kop als bol lezen, niet als doosje. Het gezicht (ogen, maan, snoet) blijft pixel voor pixel gelijk.

## 5. Voor Jordi (bevroren vorm of smaak, geen FAIL)
- **Maan D2 op 1×:** de buitenrand valt links samen met de kopcontour (x5). Daardoor leest hij op 1× als witte kap of hoofdband. Op 3× en hoger is het een sikkel. Dat stond ook al in de keuring van ronde 7.
- **Kleur van de wiggen:** F (168,196,236) leest naast het violet als ijsblauw, niet als zilver. De maan is puur wit. Een grijzer blauwlila (±190,196,224) zou de wiggen meer aan de maan binden. Dat is smaak.
- **Rechte stukken in het bevroren silhouet:**
  - linker kopflank x4 y42–49 (8 px);
  - staartsteel x51 y13–20 en x48 y14–19 (lijkt op de afgekeurde "rechte staart" van fase 1);
  - rugtop y25 x23–32 (10 px);
  - voetzolen y60.
- **Crème vingers:** de onderrand (y60–62) is E in plaats van zwart, terwijl de schaduwkant zwart zou moeten zijn. De handen zijn bevroren.

## 6. Wat ik mat (`eindkeuring/meet.py` → `meet_uitvoer.txt`)
- **Palet en alpha:**
  - PNG in modus P, transparency 0, palet gelijk aan `normal.pal`;
  - 1459 px;
  - alpha-diff 0 tegen `silhouet_bevroren.txt` en tegen `.npy`.
- **Kleurgebruik:**
  - 15 kleuren;
  - wigkleur F 92 px, lila 6 28 px (inclusief oortjes en de lila delen van wig 2 en 3);
  - zwart 1 = 10,8 % van de sprite, 1+2 = 22,8 %.
- **Rand:**
  - 244 randpixels, waarvan zwart 0,46;
  - open randen: alleen 19× E (crème groep, bevroren).
- **Losse pixels:** 69, bijna allemaal anti-aliasing in de spiraal, de maan, de ogen en de vingers. In het patroon zit er één: **(43,35) F**, in wig 3.
- **Rechte stukken ≥ 4 px:**
  - intern: **y54 x9–20 (12 px)**, **x25 y42–47 (6 px)**, verder korte stukken in de ogen en de armen;
  - silhouet: zie "Voor Jordi".
- **Gekeken naar:** de bovenste 64×64 van anim_front + normal.pal van 12 echte sprites, op 3× en 1×, licht en donker.

## 7. Na het oordeel gelezen: `ronde7/EINDKEURING.md`
- **Patroonregels:** daar afgeleid en nu in SPRITE_NORM. Wig 1 en 2 volgen ze. De suggestie van ronde 7 voor een eigen patroonkleur ("zilverig blauwlila") is met F uitgevoerd.
- **Maan, rechte silhouetstukken en E-randen bij de vingers:** ronde 7 noemde dezelfde punten onder "Voor Jordi". Dat bevestigt dat ik ze daar laat staan.
- **Kop:** ronde 7 gaf een PASS ("eigen bol met een boogkruin") en noemde de kinlijn y54 niet. F2 is dus een nieuwe bevinding van mij. Hij gaat over de onderrand, niet over de kruin. Ik houd hem aan, omdat de norm twijfel als FAIL telt en de kop op 1× naast Slakoth en Grumpig hoekig oogt. Het is een kleine reparatie (≤ 10 px).
- **Mijn oordeel verandert niet: TERUG op F1 (4 px) en F2 (≤ 10 px).**
