# Picapau kleur r4 (alleen B): notities (maker, 5 nov)

Basis: `kleur_r3/raster_B.txt`; reparaties 1–4 uit `kleur_r3/KEURING.md`. Bestanden: `repareer.py` (handgekozen wijzigingen → `raster.txt`), `bouw.py` (→ `picapau.png`, `normal.pal`), `controle.py` → `controle_uitvoer.txt`, `vel.py` → `vel.png` (1x boven, 8x onder: Taillow, r3-B, r4, Pikachu).

## Reparaties
1. **Verre poot**: rij 46 x35–37 gesloten G (teen), rij 47 x34–38 helemaal k (onderrand). Geen G meer tegen transparant, geen G/k-afwisseling.
2. **Nabije poot**: (29,46) en (28,47) g → k.
3. **Borstlicht**: de strook 1 langs de voorrand (11 px) → 2; nieuwe vlek 1 (8 px, ruitvorm) op (30,29), (29–31,30), (29–31,31), (30,32): 3–4 px binnen de selout. Kuifsteel (31,10)–(31,11) 1 → 2.
4. **Lijn aan de lichtkant**: selout 4 van (152,100,24) naar **(112,64,16)**, alleen een paletwaarde, geen pixels. Luma 73: tussen Pikachu's twee selouts (95 en 59) in. Geel 244/213/179 blijft (Pikachu 239/218/188); stap geel-schaduw → lijn 106 (Pikachu's buitenlijn springt van 153/188 naar 95/59, vergelijkbaar).

## Controle (controle_uitvoer.txt)
- Silhouet-diff tegen r3-B: **0**.
- 20 gewijzigde pixels (oud → nieuw), alle in de lijst: 2 kuifsteel, 13 borst, 2 nabije poot, 3 verre poot.
- Open randen 0, losse pixels 0, clusters < 3 px 0, grijs tegen transparant 0. 829 px.
- Kuiftoppen, oog, vleugel, snavel: 0 pixels gewijzigd (gecontroleerd met de lijst).

## Bijwerking van reparatie 4 (geen pixelwijziging, wel zichtbaar)
Kleur 4 is ook de diepe schaduw op 11 binnenpixels: (19,18) (lijn snavel/voorhoofd), onder de vleugel (39,40) (39,41) (40,42) (40,43) (41,43) (41,44) (42,44) (41,45) en boven de buikboog (39,46) (40,46). Die zijn nu ook donkerder: onder de vleugel staat daardoor een donkerbruine schaduwlijn naast de vleugelrand. Op 8x oogt dat als slagschaduw. Moet het lichter, dan kunnen die pixels 3 worden (dat valt buiten deze opdracht, dus niet gedaan).

## Zwakke punten (eerlijk)
1. **Verre poot**: gesloten en netjes, maar op 1x/8x een donker blokje; **twee aparte tenen lezen niet**. Met 3 px breed en een zwarte onderrand kan het alleen met een binnenlijn (G k G), en die afwisseling vroeg de keurder juist weg te halen. Oplossing kan alleen met 1–2 px extra silhouet (een teen naar voren op rij 47).
2. **Borstvlek** is een kleine ruit; hij leest als lichtvlek op de bolling, maar de voorrand blijft recht (silhouet), dus de borst bolt niet echt.
3. De donkere schaduwlijn onder de vleugel (zie hierboven).
4. Koplicht (24–31, 12–16) is nog steeds een lint langs de rand (de keurder: "na de borstreparatie opnieuw bekijken"); niet aangeraakt.

## Lessen
- Een paletwaarde veranderen raakt elke pixel met die index: vóór het donkerder maken van een selout de binnenpixels met dezelfde index opsommen en melden.
- "Geen G tegen transparant" en "geen afwisseling" samen laten op 3 px breed maar één gesloten teen toe; voor twee tenen is silhouetruimte nodig.
