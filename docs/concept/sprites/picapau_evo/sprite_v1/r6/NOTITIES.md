# Picapau-evolutie: sprite r6 (reparaties op r5, alles in de sprite)

r5 (`../r5/`) blijft staan. Geen modelwerk en geen nieuwe render.

## Jordi letterlijk (over r5)
**"de snavel zijn rechte lijnen, dat lijkt me niet de bedoeling. De krullen bovenop het hoofd zijn links ook weggevallen. Verder mag die nog iets meer achterover leunen, buiten dat vind ik het al goed in de buurt komen"**

Eerdere woorden (r4/pose): zie `../r5/NOTITIES.md`.

## Werkwijze
1. **`schuin.py`** (achterover leunen):
   - Het neemt de met de hand getekende segmenten van `../r5/tekening.txt` en schuift het bovenlijf per rij naar rechts: schuif(y) = round((38 − y) · tan 8°), dus 5 px bovenaan en 0 bij de heup (rij 38). Dat is een scheve draaiing van 8° om de heup.
   - De kop met snavel en oren schuift als één geheel (4 px), anders breken oog en spiraal.
   - Poten, onderbuik/dijen, steunstaart, staartlus en bliksem blijven staan.
   - Uitvoer: `tekening_basis.txt`.
   - Een echte draaiing met dichtstbijzijnde pixel heb ik ook geprobeerd (`draai_proef.py`, niet gebruikt). Die brak oog, spiraal en stippen.
2. **`tekening.txt`** = die basis, daarna met de hand bijgewerkt: de snavel, het verre oor en de naden die het schuiven maakte (voorrand van de vleugel, verre vleugel achter de snavel).
3. **Bouwen en controleren:**
   - `zet.py` → `raster.txt`, `bouw.py` → `picapau_evo.png` en `normal.pal` (palet gelijk aan r5).
   - `controle.py` → `controle_uitvoer.txt`.
   - `vel.py` → `vel.png`: naast r5, Raichu Gen 1, Pidgeot, Picapau, Taillow en de R2-render.
   - `vel_leunen.py` → `vel_leunen.png`: r5 en r6 met een hulplijn van de heup naar de kop, naast Raichu Gen 1.
4. Draaien: `python3.11 schuin.py` (alleen om de basis opnieuw te maken; overschrijft tekening.txt niet), daarna `python3.11 zet.py && python3.11 bouw.py && python3.11 controle.py && python3.11 vel.py && python3.11 vel_leunen.py`.

## Per punt
1. **Snavel: geen rechte balken meer.**
   - Het is een beitelsnavel die schuin naar links-onder taps toeloopt, zoals de wigvorm van Picapau.
   - De bovenrand (culmen) is een boog in G: 4 px bovenop bij de kop, dan stappen van 2 px naar beneden tot de punt (11,12).
   - Binnen de bovensnavel zit licht (a) aan de bovenkant en g in het midden, met een donkere G-rand aan de basis.
   - De ondersnavel loopt ook taps toe (g met een G-onderkant en een zwarte bolle onderrand).
   - De mondspleet is licht open en volgt de kromming: een smalle zwarte lijn van de punt tot de basis, waar hij één rij omhoog buigt. Rood (C) zit alleen in de mondhoek (3 px).
2. **Krullen: twee in beeld.**
   - Het verre oor (links op de kop) heeft nu een eigen zwarte spiraal van 1 px met een gat (6 × 5 px), boven de kop en linksboven.
   - Het nabije oor houdt zijn spiraal rechts. Op 1× zie je twee krullen.
3. **Meer achterover:** het bovenlijf staat 8° verder naar achteren (zie `vel_leunen.png`).
   - In r5 helde de lijn heup–kop naar voren; in r6 staat de kop recht boven de heup.
   - Raichu Gen 1 leunt nog verder: daar staat de kop achter de heup.

## Controle (`controle_uitvoer.txt`)
- Geen lichte kleur op de buitenrand.
- Geen losse pixels.
- Geen tintclusters kleiner dan 3 px.
- 15 kleuren + transparant, 1719 px.
- Alleen-diagonaal verbonden zijn 2 px: lijnen van de twee spiralen.

## Eerlijke zwakke punten
1. **Leunen.** Met 8° staat hij rechtop, maar hij leunt nog niet zo ver achterover als Raichu Gen 1. Wil Jordi meer, dan kan `schuin.py` met 12–14°. Dan schuift de kop 1–2 px verder naar rechts en raakt de nabije oorspiraal de vleugeltop (rij 3–9, x 33–40). Daarvoor moet ik eerst ruimte maken.
2. **Snavel.**
   - De snavel is nu wigvormig en gebogen, maar nog vrij donker: veel G aan de randen.
   - De ondersnavel is iets langer dan de bovensnavel, dus op 1× kan hij als een licht geopende bek lezen.
3. **Verre oorspiraal.** Hij staat vlak bij de punt van de verre vleugel. Op 1× lezen de twee zwarte lijnen samen een beetje druk.
4. **Uit r5 blijven staan:**
   - de poten (balk van de verre voet, de nabije voet zonder losse tenen);
   - de stippen (kruisjes);
   - de smalle flank;
   - de vleugel als donker vlak.

Er is niets gecommit en niets verwijderd.
