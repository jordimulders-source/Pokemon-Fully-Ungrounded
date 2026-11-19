# Soulibri r2 (19 nov)

**Jordi over r1 (letterlijk):** "frame 2 moet alleen nog klein beetje scheiding tussen de rechtervleugel en de staart, qua belijning/schaduw/kleur. Verder uitstekend".

**Wat er gebeurde:** r2 is r1 met één kleine kleurwijziging in frame 2 (`scheiding.py`). In de zone x 45–52, y 10–22 (waar de rechter, nabije vleugel tegen de opkrullende staart ligt) worden de staartpixels in middenviolet (5), die links/boven/onder aan vleugelpixels grenzen, een tint donkerder (2). Zo krijgt de staart daar een donkere randlijn/schaduw tegen de lichte vleugel. De lichte middenstreng van de staart (7) blijft, en de vleugel zelf is niet veranderd.

**Diff t.o.v. r1 (bewezen met asserts in `scheiding.py` en `lever2.py`):**
- frame 1: 0 px
- frame 2: 10 px, alle 10 in de zone, buiten de zone 0. Pixels (x,y): (49,12) (49,13) (48,14) (51,18) (51,19) (51,20) (51,21) (48,22) (49,22) (51,22), allemaal index 5 → 2.
- Silhouet, kop, kuif en vleugelvlakken zijn gelijk aan r1. Palet: gelijk aan r1 (`normal.pal`).

**Bestanden:** `frame1.png`, `frame2.png`, `anim_front.png`, `anim.gif`, `normal.pal`, `vel.png` (frame 2 r1 | r2 op 8× met de zone in rood, close-up 12× r1 | r2), `frame2_r1.png` (ter vergelijking), `scheiding.py`, `lever2.py`.

De aanzet tot de eerdere reparaties 1–3 (kop rond, kuif uit frame 1, vleugel glad) is op aanwijzing weggegooid en zit niet in r2.
