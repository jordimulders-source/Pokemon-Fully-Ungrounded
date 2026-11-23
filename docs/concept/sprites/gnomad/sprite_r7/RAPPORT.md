# Gnomad – sprite r7 (maker-agent, 22 nov)

Basis: `../sprite_r6/gnomad_A.png` en `gnomad_B.png`. Script: `r7.py A|B`. Een assert bewaakt dat er alleen pixels in x24–41, y38–51 en de 2 gesphoeken veranderen.
Jordi (krabbel `../sprite_r6/jordi_krabbel_riem.png`): "deze lijnen zijn te egaal en daar zitten pixel gaten" · "de gesp is nu beter" · "ik stel voor om op de andere 2 hoeken ook 1 zwarte pixel weg te halen bij de gesp".

## 1. Riem rechts van de gesp buigt weer mee
- Bovenlijn per kolom: rij 44 bij x24–27 (sluit aan op de gesp en op het stuk links, dus geen sprongetje), rij 43 bij x28–32, rij 42 bij x33–36, rij 41 bij x37–39.
- Dat zijn trapjes van 4-5-4-3 die korter worden naar de flank toe.
- De onderlijn loopt 4 rijen lager mee. De band blijft 3 rijen donkerbruin.
- Daardoor krijgt de broek rechts weer 1–3 rijen ruimte terug. Roze en blauw rond de riem krijgen dezelfde belichting als in r1, en de broekrij onder de riem ligt in schaduw.

## 2. Gaten aan het rechteruiteinde
- Waar de riem de rechterflank raakt, lopen boven- en onderlijn door tot in de buitenlijn. Bandpixels op de buitenlijn zijn zwart.
- Direct onder de riem rechtsonder is de blauwe selout van de buitenlijn zwart gemaakt (schaduwkant), zodat de onderlijn naadloos in de omtrek overgaat.
- Geen losse pixels, geen onderbroken lijnen.

## 3. Gesphoeken (aanvulling)
- **A:** linksboven (18,43) wordt lijftint en linksonder (18,49) wordt broek in schaduw. Rechtsboven en rechtsonder waren al weg, dus nu zijn alle 4 hoeken gelijk afgerond. A is daarmee gelijk aan B.
- **B:** had al 4 afgeronde hoeken; niets veranderd.

## Diff t.o.v. r6
| | riem rechts + roze/blauw/buitenlijn eromheen | gesphoeken | elders |
|---|---|---|---|
| A | 73 | 2 | 0 |
| B | 73 | 0 | 0 |

Controle: geen lichte kleur op de buitenrand, geen losse zwarte pixels. Zwart is 21,4 % (r6: 21,5 / 21,4 %).

Bestanden: `gnomad_A.png`, `gnomad_B.png`, `AB_8x.png`, `riem_detail.png` (zelfde uitsnede als Jordi's krabbel, r6 | r7, voor A en B).
