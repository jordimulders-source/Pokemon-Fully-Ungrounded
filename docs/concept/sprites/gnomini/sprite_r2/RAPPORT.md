# Gnomini – sprite r2 (22 nov)

Basis: r1 variant A (`r1.png` = kopie van `../sprite_r1/gnomini_A.png`); B afgewezen door Jordi. Alleen de 5 reparaties uit `../keuring_r1/KEURING.md`, uitgevoerd door `r2.py`.

| # | zone | px gewijzigd |
|---|---|---|
| 1 | roze schaduwsikkel q (213,102,136): (39–40,41), (38–40,42), (37–39,43), (37–38,44), (36–37,45) | 12 / 12 |
| 2 | roze hooglicht s: rij 41 x28 raakt de neuslijn (x26–27), dus een rij lager: (28–30,42), (27–31,43), (28–30,44); vrijgekomen lenspixels → r | 14 / 18 (4 waren al gelijk) |
| 3 | binnenlijn arm L/lijf (20,41) → p (172,72,102) | 1 |
| 4 | muts (26,33) → c (184,163,211) | 1 |
| 5 | (41,52) → (56,109,142) | 1 |

Pixeldiff t.o.v. r1 buiten deze zones: **0** (bewezen in `r2.py`). Totaal 29 px gewijzigd.

Bestanden: `gnomini.png` (64×64 geïndexeerd, 14 kleuren), `gnomini_8x.png`, `vel.png` (r2 | r1 | model op schaal, 8×; 1× op licht/groen/donker).

## Leest het lijf als bol?
Beter dan r1: het roze heeft nu licht linksboven en een sikkel rechts die in de blauwe sikkel overloopt. Het blijft wel een zwak punt dat de grens tussen roze en blauw een rechte schuine streep is (uit het model). Daardoor leest het lijf op 1× nog als twee banden en niet als één bol. Dat valt buiten deze opdracht. Een mogelijke volgende stap is die grens licht laten buigen met de bol mee, maar dat raakt het model en moet Jordi eerst goedkeuren.
