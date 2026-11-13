# Krassault – keuring tentakels en rupsbanden (r2)

Gekeurd: `r2.png` tegen `../nat_A.png` (spritepixel (x,y) = modelblok vanaf (24+2x, 21+2y)). Vel: `keur_tentakels.png` (zones 1–8). Alleen Jordi's twee vragen. Alle reparaties liggen binnen het silhouet (elke genoemde pixel is nu al gevuld). Tinten: 1 = zwart, 2 = lijnrood, 4 = schaduw (S), 5 = basis (B).

## Vraag 1: komen alle tentakels logisch uit het lichaam?

**VOLDOET: nee, nog niet.** Zeven van de tien kloppen; drie plekken laten twee tentakels in elkaar overlopen. Het zijn steeds lijnen van 1 modelpixel die bij het halveren zijn weggevallen (4 losse pixels) plus één tintkeuze uit r2.

| Tentakel | Model: komt vandaan | Sprite | Oordeel |
|---|---|---|---|
| Linker kanonarm | van onder het lijf, achter de mondring langs, voet op de linkerrol (16–19, 46–48) | doorlopende buis x 12–18, rij 30–47; voet loopt taps toe tussen gaatje en mondring, onder dicht met (16–18,48) | LOGISCH |
| Dunne tentakel langs de kop | van achter de bovenkant van de mondring (20–22, 38–39), omhoog langs de koprand, punt naar links (14–19, 21–23) | één doorlopende baan, beide randen aanwezig, zwarte lijn (18,34–37) tegen de kanonarm, voet staat op de mondring | LOGISCH |
| Kleine haaktentakel links (7–12, 38–44) | van ACHTER de kanonarm: zwarte armrand loopt door tot rij 45 | armrand (13,40–43) stopt een rij te vroeg: op rij 44 loopt de voet (12,44) zonder lijn over in de arm (13–15,44) | ONDUIDELIJK (zone 1) |
| Lage tentakel links (0–15, 44–48) | één dikke tentakel; wortel loopt ONDER het gaatje door (8–16, 47–49) achter de armvoet; basistint loopt van rij 45 tot 49 door | r2 heeft rij 46 schaduw gemaakt en rij 47 licht: leest als twee gestapelde tentakels; de bovenste eindigt bij de zuignap (10–11,45) tegen het gaatje en hangt nergens aan | ONDUIDELIJK (zone 2) |
| Rechter kanonarm | van onder de mondring, lichte band over de rechterrol (36–44, 45–47), bij x 44–47 omhoog naar de loop | band en bocht aanwezig en doorlopend; MAAR rechts mist de afsluitende lijn (zone 5) en op rij 37 zit een gat in de rechterrand (zone 3) | LOGISCH, twee lijnpixels open |
| Hoge tentakel rechts (54–59, 20–45; het is er één, met zuignappen aan beide kanten) | buigt bij rij 37–40 naar links en verdwijnt ACHTER de kanonarm; loopt als schaduwstrook (51–53, 40–44) uit in een punt, afgesloten door een zwarte lijn op rij 45 | baan klopt; punt is onder open: (52–53,45) loopt door in de schaduw eronder | LOGISCH, punt open (zone 4) |
| Lage tentakel rechts + omhoog gekrulde punt (54–63, 40–47) | wortel in schaduw (48–55, 46–48) ACHTER de voet van de kanonarm, gescheiden door een zwarte diagonaal (49,46)→(47,48) | diagonaal ontbreekt helemaal: voet kanonarm, punt van de hoge tentakel en wortel van de lage tentakel zijn één schaduwvlek; de lage tentakel lijkt uit de kanonarm te groeien | ONDUIDELIJK (zone 5) |
| Punt van die tentakel (61–63, 40–44) | zelfde tentakel, punt krult omhoog | kolom x 62 met rand links/rechts, sluit aan op rij 44 | LOGISCH |
| Rupsband links | aanhechting niet te zien: lijf en tentakels rusten erop, contactlijn op rij 48–49 | idem | LOGISCH (conform model) |
| Rupsband rechts | idem, contactlijn rij 48–49 | idem | LOGISCH (conform model) |

Niet in het model en dus ook niet in de sprite: "2–3 tentakels rechts". Rechts zitten de kanonarm, één hoge tentakel en één lage met opgekrulde punt.

## Vraag 2: is de binnenkant van de rupsband logisch vormgegeven?

**VOLDOET: nee.** De opbouw is goed (lange rol, kopvlak met zuignapringen, gesloten ovaal op de zijkant), maar de krul is in beide rollen niet af en de spiraal valt weg, waardoor je op 2× een boomstam met nerven leest in plaats van een opgerolde tentakel.

Model, per rol: gesloten buitenovaal; één middenlijn die van rechts naar links door de zijkant loopt, linksboven de ovaal raakt en aan de kant van het kopvlak eindigt in een krul (tegen de klok in, open rechtsboven). Alles in zwart.

**Rechterrol (dichtbij): ONDUIDELIJK**
- Ovaal: gesloten en gelijkmatig. Boven (45–56,51) (40–45,52), links (38–39,53) (37,54–57) (38,58), onder zwart (39–42,59) (43–47,58) (47–51,57) (51–54,56) (55–56,55), rechts (57,52–54). Klopt met het model.
- Middenlijn: (51–54,53) (46–51,54) (44–46,55) (43,54) (42,53). Klopt met het model; het rechter einde loopt in het model ook dood (haakje), dat is goed.
- Krul: (41,54) (40,55) (40,56) en een losse pixel (42,56). De onderkant ontbreekt: model heeft die op (40,5–41; 57). Nu is het een haakje plus een losse stip (zone 6).
- Leesbaarheid: lijnrood (2) op schaduw (4) valt weg op 2× en 1×; alleen de zwarte onderboog blijft over.
- Stompje (36,59) (37,60): rest van de rand tussen kopvlak en zijkant, begint uit het niets (zone 8).
- Zuignapringen: staan op het kopvlak (x 30–34) zoals in het model; boog bovenaan (32–35,50), halve ringen links (30,52) (30,56–57), nap onderaan (36–37,61). Ringen staan 1 rij lager en zijn 1 rij hoger dan in het model (rij 52–55 / 57–60 tegen 51,5–54 / 56–59); leest goed, geen reparatie.

**Linkerrol (ver): ONDUIDELIJK**
- Ovaal: gesloten. Boven (21–23,51), links (20,52) (19,53) (18,54–55) (19,56–57), onder zwart (20–24,58) (25–29,57); rechts dicht tegen de rechterrol.
- Middenlijn (24,52) (25,53) (26–27,54) → (28,54): klopt, sluit rechts aan.
- Krul: (22,53) (21,54) (21,55) (22,56) met een losse stip (23,55). De krul hangt niet aan de middenlijn: in het model lopen ze samen op (23–24; 52,5). Nu leest het als een "c" met een punt erin (zone 7).
- Zuignapringen: op het kopvlak (x 11–15), rij 50–53 en 55–58 zoals het model; 1 px links van het model, geen reparatie.

## Reparatielijst (volgorde = belang)

1. **(13,44) → 1.** Armrand (13,40–43) doortrekken naar (12–14,45): kleine haaktentakel zit dan achter de kanonarm.
2. **(48,46) (47,47) (46,48) → 1.** De zwarte run (49–51,45) schuin naar linksonder doortrekken tot de rollijn op rij 49: voet van de rechter kanonarm ligt dan vóór de wortel van de lage tentakel.
3. **(52,45) → 1.** Sluit de punt van de hoge tentakel rechts af (zelfde run als (49–51,45), tot aan (53,44)).
4. **(53,37) → 1.** Rechterrand van de rechter kanonarm, tussen (53,36) en (52,38).
5. **(7–10,46) → 5** en **(10–12,48) → 5.** Lage tentakel links weer één massa van rij 45 tot 48 (model: basistint). (4–6,46) blijft schaduw boven de zwarte lijn (4–6,47); (13–15,48) blijft schaduw onder de arm. Mag erbij, model heeft daar een lijntje: (9,48) → 2.
6. **(41,57) → lijn.** Onderkant van de krul in de rechterrol; de krul loopt dan (42,53) (41,54) (40,55–56) (41,57) (42,56).
7. **(23,52) → lijn.** Verbindt de krul van de linkerrol met de middenlijn: (24,52) (23,52) (22,53) (21,54–55) (22,56) (23,55).
8. **Middenlijn + krul in beide rollen van 2 naar 1** (rechts: de pixels onder "Middenlijn" en punt 6; links: (24,52) (25,53) (26–27,54) en punt 7). Buitenovaal blijft zoals hij is. Past in de eigen lijnregel van r2: overlap met aan beide kanten schaduwtint is zwart. Model: zwart.
9. **(36,59) (37,60) → 4** (stompje weg; de tintgrens 4/3 blijft de rand). Laagste prioriteit.

Gecontroleerd met een proef in de scratchpad (niet in de repo): met punt 6–8 lees je op 2× in beide rollen een krul.
