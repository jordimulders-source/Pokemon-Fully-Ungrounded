# Eindkeuring kolibrie ronde 5 (25 okt, nieuwe onafhankelijke keurder)

**Gekeurd:** `kolibrie.png` (Ghost/Flying, eindvorm). Eigen oordeel gevormd vóór het lezen van `KEURING.md` (ronde 5) en `ronde4/KEURING.md`; de vergelijking staat onderaan.

**Vel:** `eindkeuring_vergelijking.png`.
- Boven: de kolibrie op 3× naast Crobat, Venomoth, Honchkrow, Murkrow en Swellow, op licht en op donker.
- Onder: 1× op licht en donker (ronde 5, eind, Crobat, Venomoth, Honchkrow, Murkrow, Swellow, Corviknight, Yanma, Mismagius) en de kuif op 10×.
- Daarnaast bekeken (scratchpad, niet bewaard): 1× en 3× op licht en donker naast 16 sprites (Swellow, Honchkrow, Murkrow, Fearow, Crobat, Ho-Oh, Articuno, Venomoth, Yanma, Ninjask, Corviknight, Kilowattrel, Drifblim, Mismagius, Skarmory, Beautifly), eerste frame met `normal.pal`. Ook 8× op licht en op donker.

## Technisch nagemeten
| punt | meting | oordeel |
|---|---|---|
| Formaat | 64×64, P-modus, `transparency=0` | PASS |
| Palet | 16 kleuren, na 15-bit (GBA, >>3) nog steeds 16 unieke | PASS |
| Index 0 | (152,208,160), dezelfde groene achtergrond als `graphics/pokemon/*/normal.pal` | PASS |
| Silhouet t.o.v. `eind/kolibrie.png` | 0 alpha-verschillen, 1000 px; 102 omkleuringen, alle binnen de omtrek | PASS (bevroren omtrek intact) |
| Losse pixels | geen enkele pixel zonder buur (8-buren) | PASS |
| Zeer donker aandeel (`1`+`2`) | 0,18 (band 0,10–0,25) | PASS |
| Open randen | Randpixels naast transparant: `1` 92, `b` 82, `5` 60, `4` 36, `c` 33, `7` 7, `2` 6, `d` 4, `e` 3. Geen `3`, `6`, `8`, `9`, `a`, `f`. Alle `7`, `d` en `e` aan de rand zitten in de **kuif** (x 12–20, y 12–17). | zie eis 9 |
| Jaggies | Snavel 3-2-2-2-1 (recht, mag); verre vleugel 1-2-1-1-2 (rechte vleugelrand); voorrand nabije vleugel 4-4-3-2-3-3-2: kleine wiebel, op 1× onzichtbaar; buikboog 3-4-7-5-4 | PASS |
| Banding | Geen evenwijdige tintbanden; vleugelverloop donker → bleek met aderlijnen `b` | PASS |
| Past bij het spriteformaat van de game | Het frame past. Voor de ROM ontbreken nog frame 2 (`anim_front` 64×128), back, icon en shiny-palet. Dat is geen fout van deze ronde. | PASS (frame) |

## SPRITE_NORM: de 10 harde eisen
| # | eis | oordeel | toelichting |
|---|---|---|---|
| 1 | Leest op 1× als een echte Pokémon | PASS | Op 1× licht en donker meteen een kolibrie: naaldsnavel, V-vleugels, slepende staart. Naast Yanma, Ninjask en Crobat geen insectlezing. |
| 2 | 3/4 naar links-voor | PASS | Lijf diagonaal, kop links, één oog bij de lange snavel. |
| 3 | Ledematen | PASS | Twee vleugels, nabij groter en lager; geen poten (vliegende kolibrie, Ghost zonder grondlijn, zoals Crobat en Yanma). |
| 4 | Geen Escher | PASS | Verre vleugel boven en smaller, nabije vleugel ervoor; slierten ver boven, dichtbij onder. |
| 5 | Geleidelijke curven | PASS | Kop, borst en buik gebogen. Rechte delen zijn snavel, vleugelranden en staartveren: die zijn ook echt recht. |
| 6 | Kop | PASS | Kophoogte 13 van 53 rijen = 25 % (eindvorm 20–30 %). |
| 7 | Ogen geïntegreerd | PASS | 2×3: zwart lid, glans linksboven (10,26), pupil (11,26), iris donker blauwgroen (10,27) en licht (11,27) tegenover de glans. Corviknight/Kilowattrel-patroon; op 1× een klein kraaltje, geen gaatje en geen bril. |
| 8 | Kenmerken op 1× leesbaar | PASS | Snavel, kuif, glans op de keel, doorschijnende vleugeltoppen, drie vlammetjes. |
| 9 | Omlijning, licht linksboven, geen open randen | **FAIL (klein)** | Zone **kuiftoppen**: (13,12) `e`, (14,12) `d`, (16,13) `e`, (13,13) `d`, (15,14) `d`, (19,15) `d`, (20,15) `e` liggen zonder omlijning tegen transparant. Op donker gloeien ze mooi, maar op licht (e = 240 tegen 248) vallen de toppen weg: de veren ogen korter en de losse bleke puntjes lezen als stofjes (zie de 10×-uitsnede op het vel). De vlammetjes in de staart hebben wél een eigen omlijning in `c`; de kuif niet, dus het is ook inconsistent. De `7` aan de linkerkant van de kuif (12,14–16) is pseudo-omlijning van een veer van 2 px en mag (§8). Licht linksboven: overal consequent (ook sliert 3 klopt: `5` bovenkant, `1` onderkant). |
| 10 | Geen Chernobyl | PASS | Gezicht rustig, geen losse delen, geen vreemde vlakken. |

## SPRITE_OPDRACHT §2 (Jordi's vaste feedback)
| punt | oordeel |
|---|---|
| Lijf en blik 3/4 links-voor | PASS |
| Snuit/snavel één vorm, één oog | PASS |
| Alles verbonden, niets geamputeerd | PASS (alle drie de slierten vast aan de staartbasis, beide vleugels aan de rug) |
| Pose niet stijf, één houding | PASS (zweven, vleugels V) |
| Lijf op een echt skelet, geen doos | PASS (omtrek uit Jordi's foto, bevroren) |
| Formaat t.o.v. echte sprites | zie D1 |
| Kenmerken op 1× | PASS |
| Geen rechte lijnen waar rond | PASS |
| Ogen geïntegreerd, niet volledig zwart | PASS |
| Omlijning per kleurgroep, geen open randen | **FAIL**, alleen de kuiftoppen (zie eis 9) |
| Kleuren naast hetzelfde type | PASS: violet als Crobat, Mismagius; fluweelzwart als Honchkrow |
| Wat Jordi goedkeurde letterlijk | PASS: omtrek 0 px verschil met `eind` |

## FAKEMON_CHECKLIST (vogel, zwevend)
- **A1** PASS (kolibrie in één kleur). **A2** PASS (staart en snavel breken de omtrek). **A3** PASS (kop linksonder-midden, staart rechtsonder, vleugels rechtsboven als tegenwicht). **A4** PASS (veel lucht tussen vleugels, slierten en snavel). **A5** PASS. **A6** PASS.
- **B1** PASS (vogelkop in profiel met één oog, zoals Fearow en Swellow; lijf 3/4). **B2** PASS. **B4** PASS. **B6** PASS. **B7** PASS (oog, snavel; mond niet nodig bij een naaldsnavel).
- **C1** PASS. **C6** PASS (verre vleugel smaller en hoger). **C7** PASS (zwevend, geen grond). **C8** PASS (staart uit het achterlijf, in het verlengde van de lijflijn).
- **D1** **FAIL op het getal**: 1000 px. Eindvorm (fase 3) vraagt 1700–2600, een losse soort 1200–1600. De box (63×53) is wel die van een eindvorm. Gen 3 heeft dunne vliegers die er ook onder zitten: Crobat 1096 (fase 3), Yanma 966, Murkrow 937. Op 1× oogt hij lichter dan Crobat, Swellow en Honchkrow, maar niet te klein. Het silhouet is bevroren en het formaat stond al open voor Jordi, dus dit is **geen reparatie voor de maker** maar een besluit voor Jordi (zie onderaan).
- **D2** PASS (25 %).
- **E1** PASS (verre vleugelwortel donkerder). **E2** PASS. **E3** PASS (0,18).

## SPRITING §0 en §1–§8
| punt | oordeel | toelichting |
|---|---|---|
| §0.1 diagonaal | PASS | |
| §0.2 alles geteld en verbonden | PASS | |
| §0.3 geen rechte lijnen | PASS | |
| §0.4 ogen | PASS | |
| §0.5 silhouet op 1× | PASS | |
| §0.6 formaat | zie D1 | |
| §0.7 pose niet stijf | PASS | |
| §1 met de hand, geen vormgereedschap | PASS | geen ellipsranden; treden onregelmatig zoals handwerk |
| §3 lijnen en curven | PASS | geen spijkertjes in de curven van kop en buik |
| §4 kleuren (3 tinten + omlijning per groep) | PASS | violet 8-7-6-5, fluweel f-3-2-1 (+ lichtrand 4), vleugel/vlam e-d-c-b, keel a-9 |
| §5 licht linksboven, evenaar | PASS | kop: kapje `f` linksboven, schaduw `2` onder een schuine evenaar; borst: ovaal hooglicht `8`, buikband `6`; slagschaduw van kop en vleugel |
| §6 glans en ogen | PASS | glans + gekleurde reflectie tegenover elkaar |
| §7 texturen | PASS | geen schubben/ruis; vleugeladers als lijnen |
| §8 omlijning | **FAIL (klein)** | kuiftoppen zonder omlijning (eis 9). Verder: zwart aan de schaduwkant, `5` en `4` aan de lichtkant, 1 px breed, geen klonten |
| Lessen onderaan (mini-oog, slierten naar achteren, kop minder rond) | PASS | oog volgt de les van 24 okt; ruimte onder de buik is leeg |

## FAKEMON_DESIGN
- Geen "vogel met een hoed": kolibrie + jeguaka + zielevlammetjes vormen één geheel. PASS.
- Beperkt palet (zwart, violet, blauwgroen + bleek Ghost-lavendel). PASS.
- Simpel: geen details die op 64 px niet passen. PASS.

## SPEC
| onderdeel | oordeel |
|---|---|
| Pose en silhouet (goedgekeurd) | PASS, 0 px verschil |
| Slepende staart (goedgekeurd) | PASS |
| Kuifvorm (goedgekeurd) | PASS als vorm; de toppen zie eis 9 |
| Vleugels naar de punt doorschijnend (Venomoth) | PASS: donker fluweel bij de wortel, via `c`/`d` naar bijna wit aan de punt, met aderlijnen; de omlijning `b` blijft staan |
| Racketpunten als bleke zielevlammetjes | PASS: bleek met eigen omlijning; bovenste leest als vlammetje, de andere twee als liggende vlam/racket |
| Kop Ho-Oh/Fearow-stijl, klein oog | PASS |
| Palet fluweelpaarse kroonkolibrie, mystiek en niet eng | PASS: fluweelzwarte kop, violet lijf, blauwgroene keel, bleke gloed; blauwgroen oog oogt vriendelijk, niet eng |

## Hoofdvraag
**Leest hij op 1× overduidelijk als een mystieke Ghost/Flying-kolibrie die past tussen echte Gen 3-sprites?** Ja. De naaldsnavel, de V-vleugels en de slepende staart maken hem op 1× meteen een kolibrie. De bleke vleugeltoppen en vlammetjes geven hem op donker een duidelijke geestgloed, en het violet past bij Crobat en Mismagius. Hij is dunner en lichter dan de meeste vogels in de rij (zie D1). Het enige wat op 1× echt misgaat, zijn de kuiftoppen op een lichte achtergrond.

## Eindoordeel: NIET AF (één kleine reparatie)
**Reparatielijst (geprioriteerd, minimaal):**
1. **Kuiftoppen omlijnen in de vlamtint (eis 9, §8).** Budget ≤ 5 px. Alleen omkleuren, 0 alpha-verschil. Zet de buitenste top van elke veer op `c`, zoals de vlammetjes in de staart: (13,12) `e`→`c`, (16,13) `e`→`c`, (20,15) `e`→`c`. Zet eventueel ook (14,12) `d`→`c` (bovenrand). Binnen blijft `d` als gloed. Toets op 1× op licht: de drie veren moeten even lang blijven lezen als op donker.

Daarna is hij **AF** zonder herkeuring van de rest. Voorwaarde: Jordi kiest bij D1 voor het huidige formaat.

## Voor Jordi (smaak of besluit, geen fouten van de maker)
- **Formaat (D1):** met 1000 px zit hij onder de norm voor een eindvorm (1700+). Crobat (1096) en Yanma (966) laten zien dat dunne vliegers zo kunnen. Op 1× oogt hij lichter dan Swellow, Honchkrow en Crobat. Groter maken betekent het bevroren silhouet loslaten. Mijn advies: zo laten, tenzij je hem in het gevecht zwaarder wilt laten ogen.
- **Lichte rand om de kop (`4`, 118,116,176):** dit is een omgekeerde omlijning (lichter dan het fluweelzwart). Op donker is het een mooie geestgloed; op licht oogt het als een zachte grijze rand in plaats van een scherpe omtrek. Zat al in de versie die je "erg mooi" vond, dus ik laat het staan.
- **Vlammetjes:** het bovenste leest als vlam, het middelste op 1× meer als sterretje of racket. Wil je meer "vlam", dan kan een warmere of lichtere kern aan de staartkant met een paar pixels, binnen de omtrek.
- **Oogkleur:** blauwgroen sluit aan op de keelglans en is niet eng. Prima, maar het blijft een keuze.

## Vergelijking met de vorige keuringen (pas na mijn oordeel gelezen)
- **Ronde 5 (`KEURING.md`) gaf GOED zonder reparaties.** We zijn het eens over het silhouet, de shading, het oog en de lichtrichting. Ik verschil op één punt: daar heten alle kuifpixels aan de rand "pseudo-omlijning". Voor de violette `7` van een veer van 2 px klopt dat. Voor de bijna-witte toppen `d`/`e` niet: die verdwijnen op een lichte achtergrond, en de staartvlammen hebben voor precies dat probleem wel een `c`-rand. Ronde 5 keek naar de kop op donker en licht, maar niet ingezoomd naar de kuif op licht.
- **Ronde 4 en 5 noemden het formaat PASS ("Crobat-niveau").** Ik noem het een FAIL op het getal, maar niet voor de maker: dat is een besluit voor Jordi.
- De open rand (18,37) uit ronde 4 is gerepareerd (`1`).
