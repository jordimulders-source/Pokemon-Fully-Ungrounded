# Potoo eind_r4: bovenkant kop bol in plaats van recht (7 nov)

Opdracht (Jordi): "het valt mij op dat de bovenkant een rechte lijn is, dat moet wat meer boller. Houd voor de rest alles hetzelfde".
Bedoeld: de kruin (rij y2 was een kaarsrechte buitenlijn x23–36). Zone x18–42, y0–5. Start `eind_r3/potoo.png`, palet ongewijzigd.

## Wat
- `wijzig.py`: 26 indexwissels, elk met controle op de oude waarde (0 afwijkend). Diff buiten de zone: 0; rijen y≥6 identiek.
- Koepel (buitenlijn per rij): y2 x23–24 | y1 x25–27 | y0 x28–31 | y1 x32–34 | y2 x35–36 | y3 x37–38 (bestaand): trappen 2-3-4-3-2-2, naar het midden langer, symmetrisch rond x29,5. Midden 2 rijen hoger.
- Selout als voorheen: lichtkant 4 (hoekpixel 3 op x24 y2 blijft), rechts 4 → 2 → zwart (x35–36 y2 ongewijzigd). Geen zwart bovenop.
- Binnen: 8 (y1 x28–31, y2 x25–33); schaduw 4 op x34 y2 naast de zwarte rand, zoals x36 y3.
- Haartjes (model): oud y1 x24 en x26–28 → nu y1 x23 + y0 x24–25, één streng schuin omhoog-links boven de rand (links van het midden, zoals in het model).
- Zelf gerepareerd (poging 2): poging 1 had de haartjes op y0 x25–26; met de koepeltop y0 x28–31 las dat op 1× als een nieuwe rechte bovenlijn. Nu 2 px gat tussen streng en top.

## Controle (`controle.py` → `controle.txt`)
- Gewijzigd 26 px, buiten zone 0, palet gelijk, 12 kleuren (gelijk), 1 samenhangend deel.
- Lichte kleur naast transparant: 15 vóór en na, 0 in de zone.
- Clusters < 3 px: 147 → 148 (losse pixels 97 → 96). Nieuw in de zone: selout 4 op x32–33 y1 (2 px lijnstuk), 2 op x34 y1 en schaduw 4 op x34 y2 (1 px elk; zelfde opbouw als de oude x34 y2 / x36 y3).

## Zwakke punten (eerlijk)
- De schaduwpixel 4 op x34 y2 en de 4 op x36 y3 raken elkaar niet (x35 y3 is 8): de sikkel is daar onderbroken, zoals hij in r3 ook al los stond.
- De kop is 2 px hoger aan de bovenkant; oog en snavel liggen daardoor relatief iets lager in de kop (bewust, binnen "midden een of twee rijen hoger").

`vel.png`: eind_r3 8× | eind_r4 8×, daaronder 1× licht/donker (`vel.py`, maakt ook `potoo_8x.png`).
