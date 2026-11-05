# DJ Rotom – kleur5 (kleur4 + reparaties 1–5 uit `../kleur4/CONSISTENTIE.md`)

Jordi over kleur4: "best goed al". Niet aangeraakt: gloedkleur, navy speakers, extra plasma, verticale plek (vragen voor Jordi).

## Bestanden
- `dj_rotom.png` (64×64, geïndexeerd, transparency=0), `normal.pal` (nieuw: game-waarden), `vel.png`.
- `bron/bouw_kleur5.py`: neemt het tekstraster van kleur4 en voert de reparaties uit. Elke stap telt zijn eigen pixels.
- `bron/dj_rotom.txt` (resultaat), `bron/palet.py`, `bron/controle.py`, `bron/render.py`, `bron/vel.py`.

## Reparaties (pixels t.o.v. kleur4)
| # | reparatie | px | wat |
|---|---|---|---|
| 1 | contour binnen de gloed | 146 | **Schaduwzijde:** elke `7` met gloed rechts of onder → zwart `8`. Dat zijn de rechterkant van de rechterspeaker (x55–59 y27–60) en de onderkanten (y56 x4–10, y57 x11–35, y58 x36–38, y59 x39–50, y60 x51–57). Samen 96 px zwart tegen de gloed (Wash 71, Frost 68, Mow 74). **Lichte zijde:** elke `6` met gloed links of boven → `7`: linkerspeaker links en boven, kop links en boven, de trap boven de rechterspeaker. De spits valt erbuiten. (14,38) blijft `7`, anders wordt het een losse zwarte stip. |
| 2 | spits vrij, bliksem 3 omhoog | 164 | Bliksem identiek aan kleur4, 3 rijen omhoog (y7–22). Het staarteinde (y22) sluit met gloed `1221`, zodat de kern stopt en de bliksem de spits niet raakt. **Spits y23–32** (10 rijen), opgebouwd zoals bij Wash: punt `7`, lichtstreep `4` op x26 van y26 tot y32, links `6`, midden `5`, rechts `7`/`6`, basis x24–29. De gloed loopt 2 px mee (`1` buiten, `2` binnen). |
| 3 | losse tanden | 1 | (24,43) → zwart; twee witte tanden op (23,43) en (25,43). |
| 4 | hooglicht als vlekjes | 50 | `4` → `5`, behalve op deze plekken: kop x18–21 y33 + x17 y34–35; rechterspeaker x36–42 y31–33 + x36 y34–35; linkerspeaker x6–9 y39–40 + x5 y41–42; de spitsstreep; de wangvlekjes van het Frost-oogsjabloon. Hooglicht nu 32 px = 4,5 % van het oranje (game 3–7 %). Verdeling: midden 44 %, donker 36 %, donkerst 16 % (game 41–51 / 26–37 / 9–21). |
| 5 | palet op game-waarden | 0 | 0 → 152,208,160; 4 → 248,168,128; 5 → 232,112,40; 6 → 192,72,24; 7 → 120,56,32; 11 (grijs) → 184,184,184; 15 (wit) → 248,248,248. Gloed, navy, iris en equalizer gelijk aan kleur4. |
**Totaal 361 px = 164 + 1 + 50 + 146**. Geen enkel pixel buiten deze reparaties is gewijzigd (de som per stap is gelijk aan de totale diff met kleur4).

## Controles (`bron/controle.py`)
- Open randen: **geen**.
- Losse pixels: 21 totaal. Nieuw t.o.v. kleur4: alleen de twee witte tanden (23,43) en (25,43). Die zijn bewust los, zoals bij Wash en Heat. Geen enkele losse pixel opgelost of verdwenen; de rest is zoals in kleur4 (Frost-ogen, glanspixels, equalizer).
- Twee bijna-nieuwe losse pixels voorkomen: de spitspunt is `7` gemaakt in plaats van `6`, en (14,38) is `7` gebleven.

## Toets op 1×
- Naast Frost en Wash staat hij nu als een Rotom-vorm uit dezelfde game:
  - zwarte binnenlijn aan de schaduwkant;
  - donkerbruin aan de lichte kant;
  - vrije oranje spits met een lichtstreep;
  - hooglicht als vlekje linksboven;
  - exact hetzelfde oranje.
- Bliksem met noot blijft leesbaar (zelfde pixels als kleur4). De spits leest nu als de Rotom-punt.
- De tanden lezen op 3× als twee tandjes; op 1× is het een lachje.

## Wat nog openstaat (bij Jordi, niet in deze opdracht)
- Gloedkleur voller, speakerfronten navy of game-grijs, extra plasma-ledematen, verticale plek (enemyMonElevation).
- Naden zwart (reparatie 6 uit het rapport), shiny.pal (7), frame 2 / rug / icoon.

## Lessen
- De contourladder van de game is: gloed → zwart (schaduwzijde) / donkerst oranje (lichtzijde) → lijf. Eén stap te licht maakt de hele sprite zachter dan de familie.
- Hooglicht als randlijn leest als "plastic"; GF zet het als 2–6 px vlekje linksboven per volume.
- Tel per reparatiestap de gewijzigde pixels; als de som gelijk is aan de totale diff, is "de rest ongewijzigd" bewezen.
- Een kleurregel (bijvoorbeeld 7→8 naast de gloed) kan losse hoekpixels maken; controleer daarna op losse pixels en repareer die met de hand.
