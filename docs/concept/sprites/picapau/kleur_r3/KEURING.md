# Picapau kleur r3: onafhankelijke keuring (5 nov)

Keurder: verse agent, eerst blind (alleen `picapau_A.png`/`picapau_B.png` op 1×, 2×, 3× en 8× naast Taillow, Pikachu, Trumbeak, Starly, Pikipek, Swellow, op wit en op het groene gevechtsgroen), daarna SPRITE_KERN, SPRITE_NORM, SPEC en `controle_B.txt`. Coördinaten zijn (x, y) in het 64×64-vlak.

## Blinde indruk
- **Wat ik zie:** een roomgele vogel die rechtop zit, schuin naar links-boven, kop in profiel naar links, snavel schuin omhoog. Eén zwart oog dat naar links-voor kijkt, rode wangvlek onder het oog, twee kleine zwarte punten boven op de achterkop plus een rafelige kuif naar rechts, een bruine vleugel dicht op de rug en een stijve roodbruine staart die schuin naar beneden steekt. Vogelpootjes onderaan, tegen het lijf.
- **Dier:** een specht of een andere klimvogel (de rechte houding en de steunstaart verraden het); met de gele kleur en de rode wang ook meteen "Pikachu als vogel".
- **Wat niet leest op 1×:**
  - De snavel van A: een dun, bleek streepje. Op groen valt hij bijna weg, en hij oogt eerder als een stokje dat in het gezicht steekt dan als een beitelsnavel. B leest als snavel.
  - De zwarte kuiftoppen zijn op 1× twee donkere spikkels; de "Pikachu-oren" herken je pas op 3×.
  - De poten zijn op 1× een grijze veeg; die van A lezen niet als twee voeten.
  - De sprite is bleek en zwak van contrast vergeleken met de referenties: de goudbruine lijn aan de lichtkant (152,100,24) is veel lichter dan Pikachu's selout (98,49,8), en de sprite "drijft" op het groen.
- **Wat niet als een echte Gen 3-sprite oogt:**
  - Het lijf is een schuine buis: voorkant, schaduwband, vleugel en staart lopen als evenwijdige diagonale banen van linksboven naar rechtsonder. Taillow, Pikipek en Starly hebben een ronde borst die naar voren bolt; Picapau niet.
  - De lichtvlekken op kop en borst zijn smalle stroken die de rand volgen, geen vlekken op de bolling.
  - Naast Trumbeak (tweede fase) is hij klein en smal (829 px, bbox 36×55) voor een middelste vorm.

## Hoofdvraag
| vraag | oordeel |
|---|---|
| Leest het op 1× als Pokémon? | **Ja, net.** De wang en het oog maken hem een Pokémon; door het lage contrast en het buislijf blijft hij minder sterk dan de referenties. |
| Als specht? | **Ja.** Rechtop, steunstaart, snavel omhoog. Bij A lijdt de snavel. |
| Pikachu-achtig? | **Ja, door kleur en wang.** De kuiftoppen dragen op 1× bijna niets bij (bevroren silhouet, dus geen kleurfout). |

## Harde regels
| regel | A | B | pixels / toelichting |
|---|---|---|---|
| Tinten per kleurgroep ≤ 3 + omlijning | PASS | PASS | geel 1/2/3 + selout 4; vleugel l/b/d plus r als accent; snavel h/g; poot g/G. |
| Clusters < 3 px (behalve glans) | PASS | PASS | Script 0; ik zie op 8× ook geen losse vlekjes. |
| Geen banding / pillow shading | **FAIL** | **FAIL** | Borstlicht: strook `1` op (27–28,29), (27–29,30), (28–30,31), (28–29,32), (29,33), loopt evenwijdig aan de voorrand met één rij `2` ertussen (4‑2‑1‑2‑3: banding). Een licht streepje van 1 px op (31,10)–(31,11) in de kuifsteel. Koplicht (24–31, 12–16) is een diagonaal lint langs de rand, op het randje; na de borstreparatie opnieuw bekijken. Geen pillow shading. |
| Licht linksboven | PASS | PASS | Licht links/boven, schaduw `3` als sikkel langs de vleugel, dieper `4` onder de vleugel (39–42, 40–45). |
| Zwart alleen aan de schaduwkant | PASS | PASS | Lichtkant `4`, schaduwkant `k`; de `k` linksonder (29,43)–(29,44) zit aan de onderkant en mag. Kleine opmerking: snavelpunt zwart op (15,17)–(15,18), aan de lichtkant; mag als donkere punt. |
| Geen open randen / geen lichte kleur op de buitenrand | **FAIL** (klein) | **FAIL** | Beide: lichtgrijze `g` van de nabije poot raakt transparant op (29,46) (erboven) en (28,47) (eronder). B: schaduwtint `G` van de verre poot raakt transparant op (34,47), (36,47), (38,47). |
| Geen zwart/gekleurd om en om op één rand | PASS (net) | **FAIL** | B, verre poot, rij 47: `G k G k G` op (34–38,47) is een hark. Nabije poot (A en B) rij 47: `k g k` op (30–32,47) is klein en mag. |
| Oog | PASS | PASS | (25–28,18–21) is pixel voor pixel Pikachu's oog (k i.p.v. 41,41,41): rond, glans w (26,19) linksboven. Kijkt naar links-voor. |
| Pootjes in perspectief, vast aan het lijf | PASS (zwak) | PASS | A: nabije poot (26–32,45–48) met een verre teen in `G` (33–34,45–47), vast aan de buik; op 1× een veeg. B: verre poot in een eigen kolom (34–38,45–47), kolom 33 lucht, 1 rij hoger en in schaduwtint; afgezien van de hark (zie boven) beter. |
| Geen rechte stukken waar het dier rond is | **FAIL** | PASS* | A: buikonderkant is een vlakke zwarte lijn van 8 px op (36–43,46). B rondt die af naar de verre poot. *Beide (bevroren silhouet, ter info voor Jordi): voorrand recht op x 26 (y 31–35, 5 px) en x 28 (y 38–41, 4 px); rug/vleugelrand een rechte trap van (41,27) tot (49,45). |
| Snavel ≥ 2 px, leest | PASS (zwak) | PASS | A: 2 px dik met een transparante inkeping tussen snavel en voorhoofd op (17–18,17) en (18,18): leest als stokje. B: basis 3–4 px (17–21,18–22), sluit op de kop aan, leest als beitelsnavel. |
| Silhouet volgt het bevroren silhouet | PASS | **wijkt af** | A: 0 px buiten de zones. B: 9 px buiten de zones (snavelbasis (18,18), (17,22), (18,23); buik/poot (42–43,46) eraf, (37–40,47) erbij). Zonder akkoord van Jordi mag dat niet. |

## Oordeel
- **A: NIET GOED.** Snavel leest op 1× niet als snavel, buikonderkant is een rechte lijn van 8 px, borstlicht in banen.
- **B: NIET GOED (dichtbij).** Snavel en buik zijn opgelost; wat overblijft is de hark van de verre poot, open randen bij de poten en het borstlicht. De silhouetwijziging moet Jordi eerst goedkeuren.

**Keuze: B.** De twee grootste problemen van A (snavel, platte buik) zitten in het silhouet en lossen zich met kleur niet op; B lost ze op met 9 px die de massa niet raken (snavelbasis en onderrand van de buik). De fouten in B zijn kleurfouten in een klein gebied en makkelijk te repareren. Voorwaarde: Jordi keurt de 9 px buiten de zones goed (laat hem B en het bevroren silhouet naast elkaar zien).

## Reparatielijst (op B)
1. **Verre poot (34–38,45–47):** geen `G k G k G` meer op rij 47. Maak er twee of drie korte, gesloten teentjes van in `G`, onderaan omlijnd met `k`, zodat er nergens `G` tegen transparant ligt.
2. **Nabije poot:** `g` op (29,46) en (28,47) wordt `k` (of schuif de `g` een pixel naar binnen), zodat er geen lichte kleur op de buitenrand ligt.
3. **Borstlicht:** vervang de strook op (27–30,29–33) door één vlek van `1` op de bolling van de borst (bijv. 3×3–4×3 rond (29–31,29–31)), los van de rand, met `2` tussen vlek en selout breder dan 1 px aan de onderkant. Dat suggereert ook een ronde borst. Haal het streepje (31,10)–(31,11) weg (`1` → `2`).
4. **Contrast op 1× (aanbevolen):** maak de selout aan de lichtkant (`4`, nu 152,100,24) donkerder, richting Pikachu's (98,49,8), en meet tegen Taillow/Pikachu (±30–40 per tintstap). Het geel zelf blijft roomgeel.
5. **Daarna:** controlescript opnieuw draaien, vel op 1× en 8×, en B samen met het bevroren silhouet aan Jordi voorleggen voor akkoord op de 9 px.

## Ter info voor Jordi (geen kleurfout, valt binnen het bevroren silhouet)
- Formaat: 829 px voor de middelste vorm; de norm zegt fase 2 ≈ 1,5–1,7× fase 1. Naast Trumbeak oogt Picapau klein en smal. Vraag of dat zo bedoeld is (bijv. als Picapau toch fase 1 is).
- De kuiftoppen zijn op 1× te klein om als Pikachu-oren te lezen; de Pikachu-associatie komt nu van de kleur en de wang.
- De voorrand is vrij recht (de buik bolt niet naar voren), waardoor het lijf een buis lijkt. Reparatie 3 helpt; echt rond wordt het alleen met een kleine silhouetaanpassing.
