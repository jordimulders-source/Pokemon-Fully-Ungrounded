# Picapau kleur r5 (B): notities (maker, 5 nov)

Basis `kleur_r4/raster.txt`. Bestanden: `repareer.py` (handgekozen wijzigingen → `raster.txt`), `bouw.py` (→ `picapau.png`, `normal.pal`, palet ongewijzigd t.o.v. r4), `controle.py` → `controle_uitvoer.txt`, `vel.py` → `vel.png` (1x boven, 8x onder: Taillow, r4, r5, Pikachu).

## Wijzigingen (27 px, lijst oud→nieuw in controle_uitvoer.txt)
1. **Verre poot, twee teentjes**: (35,47) en (37,47) k → G (teentoppen), met zwarte onderrand op **(35,48) en (37,48): +2 px silhouet**. B-budget nu **23/30**. Een teen "naar voren" op rij 47 kon niet: links van de verre poot ligt kolom 33 (lucht) en daarnaast de nabije poot. De teentjes wijzen nu naar beneden/voren, met (36,47) zwart ertussen.
2. (niet gevraagd, niet aangeraakt)
3. **Schaduwlijn onder de vleugel**, per pixel:
   - (39,40) (39,41) (40,42) (40,43) (41,43) (41,44) (42,44) (41,45): 4 → 3 (gewone schaduw; de vleugel heeft zijn eigen donkerbruine rand, dus geen vorm-over-vorm-lijn nodig).
   - (39,46) (40,46): 4 → 3 (schaduw boven de buikboog; de zwarte onderrand eronder blijft).
   - **(19,18) blijft 4**: dat is de lijn waar de snavel over het voorhoofd ligt (vorm over vorm).
4. **Koplicht**: het lint langs de rand (11 px 1 → 2, o.a. (30–31,12), (27–29,13), (25,14), (29,14), (24,15), (24–25,16)) vervangen door één vlek van 9 px op de bolling: (26–28,14), (25–28,15), (26–27,16). Die ligt 2 px onder de bovenrand en 3–4 px van de voorrand.

## Controle
- Silhouet-diff tegen r4: alleen (35,48) en (37,48).
- Open randen 0, losse pixels 0, clusters < 3 px 0, grijs tegen transparant 0. 831 px.
- Kuiftoppen, oog, vleugel, snavel, borst, nabije poot: 0 px gewijzigd.

## Zwakke punten (eerlijk)
1. **Verre poot**: de twee teentjes lezen op 8x duidelijk, op 1x net. Door de teentoppen reikt de verre poot nu tot rij 48, net als de nabije poot: aan de teentoppen is hij niet meer "1 px hoger". Hij blijft wel rechts/achter, in schaduwtint en los van de nabije poot (kolom 33).
2. Ter info, uit het bevroren silhouet (geen kleurfout): de voorrand is vrij recht, dus het lijf is buisvormig; de kuiftoppen zijn op 1x klein; formaat 831 px voor de middelste vorm (keurder: naast Trumbeak klein).
3. B wijkt 23 px af van het bevroren silhouet (10 buiten de zones): Jordi moet dat goedkeuren, met B naast het bevroren silhouet.

## Lessen
- Een teen laten lezen zonder hark: de teentop in de schaduwtint met zwart eronder en ernaast; dat kost 1 px silhouet per teen onder de onderrand.
