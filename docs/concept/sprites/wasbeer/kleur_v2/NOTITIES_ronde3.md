# Kleur ronde 3 (maker-agent, 2 nov)

Basis `ronde2.txt`; de punten uit `KEURING_ronde1.md` die in ronde 2 nog niet slaagden, met de hand als pixellijsten per zone in `rijen_ronde3.py` → `ronde3.txt`, `ronde3.png`, `ronde3.pal` (palet = ronde 2). 193 px gewijzigd t.o.v. ronde 2. Alpha-diff met `direct_s1a.txt` = 0, geen open randen. Vergelijkingsvel `vel_ronde3.png` (`vel3.py`): per onderdeel 8x-uitsneden naast Sneasel/Zangoose/Sandslash (klauw), Zangoose/Ursaring (onderarm), Linoone/Sentret/Furret/Zigzagoon (staart), Zangoose/Ursaring/Teddiursa (volume), Zigzagoon/Linoone (oog op masker); hele sprite 2x/1x naast 6 echte sprites.

| Zone | wat | aanpak van de echte sprites |
|---|---|---|
| nabije klauw | 2 klauwen (x 22–23, 25–26): links 9, rechts 8, bovenkant a, omlijning 1 rechts en onder, inkeping 1 alleen bij de punt (24, 32–33) | Sneasel/Sandslash: lichte klauw in 3 tinten, licht linksboven, donkere rand onder/rechts |
| nabije onderarm | donkere buis: glans 4 boven, 2 midden, 1 onder | Zangoose/Ursaring: arm als buis, licht boven, schaduwrand onder |
| bovenarm | vanuit de schouder (x 30–36, y 21–33) in vachtgrijs: 4 voorrand, 7 licht, 6, 5, kernschaduw 4 naar de rug | Ursaring: arm los van de romp door een donkere voorrand |
| buidel | zakmond 3x2 (1 boven, 2 onder) met lichte boven- en onderlip d; plooi = lichte rug d + schaduw b (vouw) | geen Gen 3-voorbeeld; foto 15 |
| staart | haakkop met licht 4/8 bovenop en kernschaduw 1 rechts; ringen in het midden 1 px hoger dan aan de randen, licht a/9 links, 8 rechts | Furret/Sentret: gebogen ringen, 3 tinten per ring |
| volume | hooglicht 3 groter (kop y 5–6, schouder/borst y 21–25), kernschaduw 4 aan de schaduwkant van de kop (x 28, y 9–13) | Zangoose/Teddiursa: hooglicht geconcentreerd linksboven, schaduw volgt de bolling |
| oog | oogkas-wal onder het nabije oog terug naar masker 2 | Zigzagoon/Linoone: iris donker boven/licht onder met glans, direct in het masker |

Niet veranderd (opdracht): klauwvorm, masker-idee, kleurtemperatuur, crème handen, verre oog, buidelkleur.

## Eigen zwakke punten (eerlijk)
- **Onderarm/bovenarm:** de nabije onderarm leest op 1x nog als donkere vorm. De bovenarm is grijs op grijs en valt op 1x weg, dus de arm "uit de schouder" leest pas op 4x.
- **Staart:** de haakkop is op 1x een groot donker blok; de haak (punt die terugkrult) leest nog als knots. De ringen buigen maar 1 px.
- **Nabije klauw:** op 2x een klauwpaar; op 1x vooral een lichte vlek met een donker streepje.
- **Zakmond:** op 4x een opening, op 1x een klein donker streepje.
- **Volume:** levendiger dan ronde 2, maar nog niet op het niveau van Coathief/Ursaring (minder contrast tussen hooglicht en kernschaduw).
- **Oog:** zonder oogkas leest het bovenlid (1 op 2) niet. Zigzagoon heeft een lichtere ring direct om de iris; dat heb ik niet gedaan, omdat de vorige keurder de oogkas een wal vond.
- **Vel:** de 8x-uitsneden van de referenties zijn met de hand gekozen vakken van 16x16 en zitten niet allemaal precies op het onderdeel.

## Lessen
- Grijs op grijs (bovenarm 6/7 op een romp 6/5) leest op 1x niet; een ledemaat vóór het lijf heeft een donkere voorrand of een andere tint nodig (Ursaring).
