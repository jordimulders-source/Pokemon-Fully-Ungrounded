# Keuring picapau sprite_v2 kleur r6 (dezelfde keurder, 5 nov)

Gekeurd: `kleur_r6/picapau.png`, 854 px. Dezelfde maatstaf en tekens als `kleur_r5/KEURING.md`. Niets aan de sprite veranderd.

## Diff met r5
- 83 px verschil: precies reparaties 1–5 (`repareer.py`, 0 mismatches).
- Buiten de opdracht niets gewijzigd. Staart, wang en omtrek zijn 0 px veranderd; de enige omtrekwijziging is (24,30), uit reparatie 5.
- Palet gelijk.

## 1. Blind (1×, 3×, 8×, naast r5, Taillow en Pikachu)
- **Kop:** leest nu als een bal. Er ligt een lichte schijf rond het oog, een dunne basisring op x29–31 en een schaduwsikkel vanaf x32/33. De band langs de bovenrand is weg. Op 3× is dit het grootste verschil met r5.
- **Snavel:** leest als een snavel. Lichte rug op (16–17,18) en (17–19,19), midden `g`, donkere onderkant `G` (19–21, 22–24). Hij steekt nu duidelijk af tegen het lichte gezicht. De donkere voet is fors, maar volgt de render (zie §2).
- **Vleugel:** heeft nu licht op de voorrand (34–35,29) en (34,30). De stippen zijn gedempt, op één felle stip linksboven na. Het "koekje" is weg en de vleugel volgt de bolling. De stippen blijven zichtbaar op 1×.
- **Borst:** halsplooi van 2 rijen (r29–30 op x25). De voorkant begint niet meer als een wand direct onder de kin.

## 2. Tegen het model
| onderdeel | r6 |
|---|---|
| kop (vorm) | gelijk (ongewijzigd) |
| kop (licht) | **gelijk aan de toonkaart:** `1` waar toon 4, `2` ring op x29–31 waar toon 3, `3` vanaf x32/33 en onder de kin waar toon 2/1. De 72 afwijkende cellen van r5 zijn verwerkt. |
| kuif | vorm en naad gelijk. Het licht op de kegelvlakken wijkt nog af (reparatie 6, Jordi's zone, bewust niet gedaan). |
| oog | gelijk. De ankers in `2` geven een overgang zonder donkere ring, zoals in het model (oog in een licht gezicht). |
| wang | gelijk (ongewijzigd) |
| snavel | **gelijk aan toonkaart en render:** rug toon 4 = `h`, r20–21 toon 2 = `g` (render 144,140,114), r22–23 toon 1 = `G` (render 67,62,48). |
| borst/buik | licht ongewijzigd (gelijk). Omtrek r28–30 nu gelijk aan de render (x23, x25, x25). r31–41 blijft bewust 1–2 px vóór de render (Jordi: r4-lijf "beter"). |
| vleugel | **gelijk:** voorrand licht waar de toonkaart toon 4 heeft. Stippen in renderhelderheid: alleen (35,27) licht, de rest ≈ `g`. |
| poten, tenen, staart | gelijk (ongewijzigd) |

## 3. Harde regels
| regel | oordeel |
|---|---|
| ≤ 3 tinten per groep | PASS |
| contrast | PASS. Snavel tegen gezicht nu `g`/`G` tegen `1` (helderheid 140/65 tegen 244). |
| clusters < 3 px | **PASS.** Nieuw zijn alleen: de oogankers (24,18), (27,18), (24,21) en (27,21) (anti-aliasing van het oog, één per hoek, hoort bij het oog), en `2` op (19,17) en (19,18), een 1-px-scheiding tussen snavelvoet en gezicht (vorm over vorm). De stip `g` (42–43,35) was in r5 al 2 px (als `h`). Geen losse of alleen-diagonale pixels (controle: 0). |
| geen banding / pillow shading | **PASS** (was FAIL). De kop heeft geen lichtband langs de rand meer; het licht volgt de vorm. |
| licht linksboven | PASS |
| zwart alleen schaduwkant | PASS |
| geen open randen | PASS (0 lichte kleur op de buitenrand) |
| vloeiende curven | **PASS** (was FAIL). Voorkant 2-5-2-2-2-1-1-1, oplopend dan aflopend, zelfde ritme als de render (1-5-2-3-3). |

## 4. Jordi's punten
| punt | r6 |
|---|---|
| "volledig 2d, geen drie kwart" | **ok:** de kop is nu belicht als bal. Het verre oog, de hogere verre voet en het lijf volgen het model. |
| "klauwen afgeknapt" | ok (ongewijzigd) |
| "shading niet goed" | **ok:** kop, snavel en vleugel volgen nu de toonkaart en de render, net als het lijf al deed. |
| "snavel weg" | **ok:** grijze snavel met lichte rug en donkere onderkant, duidelijk los van het gezicht. |
| "het lichaam moet echt bol" | **ok:** lichtovaal, sikkel, dij en een ronde aanzet onder de hals. |
| krabbellijnen 1 en 2, borst- en vleugelboog | ok (ongewijzigd t.o.v. r5) |
| "kop rechts geen hallucinatiewerk" | ok. Kop rechts wijkt 23 px af van r2: de 7 uit r5 (Jordi's lijnen) plus 16 van reparaties 1–2 (gezichtslicht en schaduwsikkel), elk uitgelegd met de toonkaart. De omtrek van kop rechts is niet aangeraakt. |

## 5. Oordeel: **GOED** (klaar om aan Jordi te tonen)

Ik zie geen nieuwe fouten. Alle FAILs uit r5 zijn opgelost, en elke wijziging komt terug op een toon of kleur van het model.

Open punten, ter melding aan Jordi, geen reden om af te keuren:
- **Reparatie 6 (lichte kegelvlakken in de kuif)** is niet gedaan, omdat het zijn zone is. Het is uit te leggen met de toonkaart (toon 4 op (35,9), (33–34,10), (32–33,11), (31–33,12), (31–32,13) en op (31,9), (30,10), (30,11)). Het voorstel kan aan hem worden voorgelegd.
- **De donkere snavelvoet (19–21, 22–24)** is zwaar, maar staat zo in de render. Als Jordi hem te donker vindt, is (19–20,22) `G` → `g` de kleinste stap; dat wijkt wel van de toonkaart af (toon 1).
