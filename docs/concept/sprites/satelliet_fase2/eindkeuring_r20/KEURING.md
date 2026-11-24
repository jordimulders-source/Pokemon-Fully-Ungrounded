# Eindkeuring satelliet fase 2, r20 → r21 (Dragonfly Cave; kleurtinten, schaduw, lijnen), 24 nov

Te keuren: `../sprite/r20/sprite.png`. Model: `../paneel_varianten/panelen_80b.png`. Vorm is goedgekeurd door Jordi ("het gaat niet zo zeer erom dat elke pixel klopt, maar dat de vorm klopt"): silhouet en lijnposities blijven, oog b + pupil p2 blijven. Alleen tinten veranderd.
Reproduceerbaar: `python3 repareer.py` (r20 → `r21/sprite.png`, met asserts op oude waarde per pixel en silhouet-diff 0), daarna `python3 vel.py`.

## Oordeel
- **r20: BIJNA.** Volume en lichtrichting staan; vier technische punten: lijfladder bovenaan te dicht (F→2 = 19), lichtste lijftint tegen de zwarte schaduwrand rechts, linkerbovenpixel van beide antennebolletjes donkerder dan het midden, één gat en één lichte pixel in de omlijning.
- **r21: PASS** (binnen de bevroren vorm). Silhouet-diff 0; 9 pixels omgetint + 2 paletwaarden.

## Stap 1: Gen 3-studie (8×, `graphics/pokemon/*/anim_front.png` + `normal.pal`)
| Sprite | Ladder (helderheid Y) | Gemeten |
|---|---|---|
| Glalie (wit metaal/ijs) | 239 / 208 / 179 / 124 (+ 89, zwart 16) | stappen 31/29/55; tint koel 210→240, schaduw blauwer; binnenpixel naast de rechter buitenlijn altijd 179/124 (13/4×), nooit 239/208; buitenlijn linksboven 49 zwart + 20 outline base, rechtsonder 74 zwart |
| Metang (metaal) | 191 / 151 / 121 / 93 (+ glans 248) | linksboven 66 zwart + 38 navy; rechtsonder bijna alles zwart; rechter binnenpixel meest 93 |
| Claydol | 194 / 149 (licht), 106 / 82 / 65 (lijf) | buitenlijn linksboven grotendeels donkerbruin, zwart rechtsonder |
| Lunatone | 212 / 180 / 156 / 125 / 107 | buitenlijn geheel in eigen bruin (geen zwart) |
| Magneton | 233 / 200 / 149 / 88 | bollen: hooglicht (233) links van het midden (zwaartepunt x 28,0 tegen bolmidden 32,4) |
r20 zelf: buitenlijn linksboven 40 zwart / 95 eigen tint (8, 9, 6, 7), rechtsonder 69 zwart / 25 navy: in lijn met Glalie/Metang.

## Stap 2: keuring r20
**(a) Kleurtinten**
- Lijf: F 255 / 2 236 / 3 205 / 4 166 / 5 127 → stap F→2 = 19 (bijna gelijk; Glalie 31). Tint 249→268, koel wit; 4/5 lavendel zoals de onderkant van het model (model gemiddeld H 278).
- Panelen: 9 43 / A 87 / B 115 / C 169, navy-paars (H 246–252). A→B = 28 maar B is de glans in het donkere 9-veld (stap 72): leest. Geen wijziging.
- Gewrichten 6 168 / 7 112 / 8 75, lens E/D teal: in orde.

**(b) Schaduw/volume** (eerst volume getoetst): koepel heeft hooglicht op de bolling (F), lichte schaduw rechts (3), randlijn van de kap (4), onderlijf 4→5 als sikkel onderaan; panelen boven licht/onder donker met glansvlak, zoals het model. Geen pillow shading, banding of dambord. Fout: de onderwang rechts van de lens (rij 28–32) loopt in de lichtste lijftint tot tegen de zwarte schaduwrand (Glalie doet dat nooit). Antennebolletjes: linksboven 5 (Y127) naast 6 (Y168): de lichte pixel staat rechtsboven, en 5 is een tint uit de lijfgroep.

**(c) Lijnen**: 1 px, schaduwkant zwart, lichtkant eigen tint; geen zwart/donkerlila om en om op één rand (script: alle buitenrandpixels nagelopen). Fouten: gat in de selout lijf/klein paneel op x=20 (paneel A raakt lijf 2 direct), en (12,35): lichte framelijnkleur A op de buitenrand van het kleine paneel, ingeklemd tussen zwart.

## Stap 3: reparaties (r21), alleen tinten
| Zone | Wijziging | Verantwoording |
|---|---|---|
| Z1 lijfladder (palet) | slot 2 (236,235,242) → (226,225,238); slot 3 (207,201,222) → (198,191,217) | Ladder 255/227/196/166/127 = stappen 28/31/30/39, zoals Glalie 31/29; koel (H 245 / 256), niet lavendeler dan r20. Het hooglicht F leest nu als hooglicht. Geldt overal waar 2/3 staan (koepel, lensring, onderwang, glans in de bolletjes). |
| Z2 antennebolletjes | (35,8) en (48,10): 5 → 6 | Licht linksboven (KERN/DC; Magneton: hooglicht links van het bolmidden); weg met de lijftint uit de gewrichtengroep. Bolletje nu 6/6/6/7 binnen 8/1-lijn. |
| Z3 selout linksboven | (20,21): 2 → 5 | Sluit de lichtkant-lijn tussen klein paneel en lijf (eigen donkerste lijftint, zoals de rest van die rand); trapje wordt 1-3-2-2. |
| Z4 sikkel rechterrand onderwang | (36,28) (36,29) (37,30) (37,31) (36,32): 2 → 3 | Glalie: binnenpixel naast de rechter (schaduw)buitenlijn altijd een schaduwtint. Sluit aan op de 3 langs de koepelrand erboven (rij 23–27): één doorlopende sikkel. |
| Z5 hoek klein paneel | (12,35): A → 9 | Geen lichte kleur op de buitenrand aan de schaduwkant; 9 = paneelbasis/outline base, geen zwart klontje. |

Niet aangeraakt: lens/oog (oog b, pupil p2), panelen, alle lijnposities.
Controle: silhouet-diff 0; pixels <3 die over zijn: glanspixels in de bolletjes (29,17) (38,20) (33,33), oogglans (18,34), lensringovergangen (16,27) (26,38), en (31,44) (zie hieronder).

## Ter info voor Jordi (ontwerp/vorm, niet uitgevoerd)
1. **Losse paneellijn (31,44)**: één B-pixel in het donkere onderste paneelvlak; in het model loopt daar de lichte framelijn langs de linkerrand van het grote paneel, in de sprite alleen in stukjes (33–34,40–41), (31,44), vanaf rij 48. Doorlopend maken of weghalen = lijnpositie, dus jouw keuze.
2. **Zwarte lijnen van de lens aan de lichtkant**: de bovenlijn van het lenshuis (rij 26, x15–20) en de ringen zijn zwart, ook linksboven. Gen 3 (Claydol, Lunatone) kleurt daar vaak de eigen donkere tint; hier niet gedaan omdat de lens (oog b) bevroren is.
3. **(13,31)–(13,32)**: twee paarse pixels buiten de zwarte lenslijn tegen het kleine paneel (rand 2 px dik). Komt uit r18-links; vorm.
4. Rij 27 (x30–33): de kaprand als kort recht stukje 4 midden op de koepel; in het model een schuine lijn. Vorm.

## Bestanden
`repareer.py`, `vel.py`, `r21/sprite.png`, `r21/sprite_8x.png`, `vel.png` (r20 8× | r21 8×, omgetinte pixels rood omrand | model op spriteraster; r21 2× naast Glalie, Magneton, Claydol, Metang, Lunatone; 1× r21/r20 op licht en donker).
