# Satelliet fase 2, r13: afwerkingsronde kleur, schaduw, lijnen + eindkeuring (24 nov)

Basis `../r12/sprite.png` (= r11 var_a + rode lijn). Script: `bouw_r13.py` (draaien vanuit deze map), controle `check13.py`, vel `vel_r13.py`, studie `studie.py` → `studie_gen3_6x.png`.
Bevroren en gecontroleerd: **silhouet-diff 0**, alle lijnposities en onderdelen gelijk; alleen tinten van bestaande vlakken + palet. 169 pixels anders dan r12 (lijf boven 87, koepel 40, groot paneel 43, klein paneel 44; zones overlappen). Oog b en pupil p2 ongewijzigd (alleen de glanspixel is het nieuwe puur wit).
Palet: 15 kleuren + transparant (slot F was vrij, nu hooglicht).

## 1. Studie Gen 3 (GBA-sprites, `normal_gba.pal`, op 6×)
| Sprite | Hoofdvlak | Hooglicht | Schaduw/sikkel | Stappen (L) | Omlijning |
|---|---|---|---|---|---|
| Glalie (wit/grijs bol) | 5 tinten: 255/231/206/166/125 | groot wit vlak linksboven op de bolling, 1–2 px basis tussen hooglicht en rand | brede 3-zone, 4-sikkel rechts/onder, 5 dun tegen de rand; linksonder weer 3 (teruggekaatst licht) | 24/25/40/41 | bijna overal donker (41,41,57), rechtsonder zwart |
| Magneton (licht metaal, bollen) | 1 wit + B basis + C + D | ovaal wit vlakje linksboven, niet tegen de rand | C-sikkel rechtsonder, D diepst | 22/33/28 | **bovenkant/links in eigen donkere tint E/D, ook waar de bol over de zwarte magneet ligt**; zwart rechtsonder |
| Magnemite | idem Magneton, 3 tinten op de bol | 1 klein wit vlakje | C/D rechtsonder | ±30 | E links, zwart rechts |
| Claydol (vlakke banden) | 3 tinten per vlak, banden lichter boven | lichtste tint op de bovenrand van elke band | donker aan de onderzijde van elke band | ±25–45 | eigen donker (82,82,41) rondom, zwart weinig |
| Beldum/Metang (blauw metaal) | 4–5 tinten | lichtblauw (9) als streep op de bolling linksboven | brede D/E rechtsonder | ±30 | E/zwart rechtsonder, lichte kant eigen tint |
| Lunatone (rond vlak) | 6 tinten | 1–2 lichtste op de linker binnenrand | sikkel donker langs de rechterrand | 15–20 per stap, veel stappen | eigen bruin, zwart alleen rechts |

Overgenomen: Glalie's toonladder (255/231/206/166/125 → r13 255/232/207/170/127) en zijn verdeling (groot hooglicht linksboven, brede schaduwzone, sikkel, lichte rand linksonder); Magneton's hooglicht als ovaal vlak los van de rand en zijn lijfomlijning in eigen donkere tint aan de lichte kant; Claydol's "licht boven, donker onder" voor de panelen; Metang/Magneton bol-opbouw (hooglicht linksboven, schaduw rechtsonder) voor alle bolletjes.

## 2. Wat er per zone veranderde
- **Palet lijf**: 2 (242,240,238) → (232,231,238) basis; 3 → (208,205,220); 4 (188,177,208) → (172,166,190); 5 (146,126,170) → (130,122,152); nieuw F = (255,255,255) hooglicht. Minder lavender (B−G van 31 naar 24, R−G van 11 naar 6: koel grijs zoals Glalie), meer contrast (stappen 23/25/37/43).
- **Lijf (bovenvlak + zijkant)**: het effen witte vlak heeft nu volume: ovaal hooglicht F (±36 px) op de bolling linksboven met 2 px basis tot de contour; basis 2 eromheen; schaduw 3 als boog rond het hooglicht; sikkel 4 rechts; diepste 5 (2 px) tegen de zwarte rand. Het lijf naast de koepelrand (was een losse witte streep) volgt nu dezelfde bol. Lijf telt **5 tinten (F/2/3/4/5)**: 4 vultinten + 5 als diepste tint én lichte lijn, zoals Glalie; benoemd.
- **Koepel**: binnenste witte ring krijgt het hooglicht F linksboven (8 px), rechts 2→3, onder 3→4 (bleef); buitenring rechts 2→3→4→5 (bleef, tinten lopen mee via het palet); onderkant linksonder een smalle 3-rand (teruggekaatst licht, Glalie), rechtsonder 5.
- **Groot paneel**: bovenste celrij loopt diagonaal van B (linksboven) naar A; tweede rij A met een 9-driehoek rechtsonder (donkerder naar rechtsonder i.p.v. twee vlakke helften); glansrij (B-glans uit het model) en onderste rijen ongewijzigd; rasterlijnen lopen mee: C in het licht, B in het donker, A in de donkerste hoek linksonder/rechtsonder. Framelijnen ongemoeid.
- **Klein paneel (achter)**: een sleutel donkerder: bovencel A (groot paneel: B), binnenlijnen in de onderste cellen B → A; framelijn B blijft (leesbaar op donker).
- **Bolletjes**: één opbouw overal: rand 8 boven/links, hooglicht 3 linksboven, 6, 7, schaduw 8, zwart rechts/onder. Linker antennebol 6/7/7/8 → 3/6/6/7 (gelijk aan de rechter); gewricht bij de koepel had het hooglicht in het midden (kussen) → nu linksboven, schaduw onderaan. Grote gewricht boven en kleine rechts hadden de opbouw al.
- **Lijnen**: lijfcontour linksboven (9 px, tegen het kleine paneel) zwart → 5 (lichte kant, eigen donkerste tint, zoals Magneton); hoek (21,17) zwart → 8 zodat 5-lijn en 8-rand zonder los zwart pixel in elkaar overgaan. Zwart blijft rechts/onder en als boog linksonder om de koepel.

## 3. Eindkeuring (FAKEMON_CHECKLIST E + gids omlijning)
- **Volume eerst**: lijf: hooglicht op de bolling, tintverdeling binnenin (niet alleen langs de rand), sikkel die de vorm volgt: ja. Koepel: ring met licht linksboven en schaduw rechtsonder: ja. Panelen: verloop linksboven → rechtsonder i.p.v. twee vlakke helften: ja, bescheiden (alleen 9/A/B beschikbaar).
- **Netheid**: ≤16 kleuren; geen pillow (hooglicht uit het midden, sikkel alleen rechts/onder), geen dambord. Nieuwe vlakjes < 3 px zijn alleen lijntrapjes (5-contour, A-paneellijnen) en glanspixels van bolletjes/lens; drie losse vlakjes uit de eerste versie gerepareerd ((27,28) 2→3, (44–45,25) A→B, (12,26) A→B). Geen lichte pixels op de buitenrand.
- **E1 verre kant donkerder**: klein paneel een sleutel donkerder dan het grote: ja.
- **E2 overlap**: lijf over klein paneel in eigen tint 5, koepelrand over lijf 5→zwart (één overgang), gewrichten 8.
- **E3 donker aandeel**: zwart 11,4 % (r12 12,0 %); met de navy panelen 31,5 % (ontwerpkleur, zoals bij r7 gemeld).
- **Om-en-om**: nergens zwart en donkerlila afwisselend op één rand (op 8× nagelopen langs lijf, koepel en panelen).
- **1×** (vel, licht en donker): lijf leest als wit bolvormig metaal, panelen blijven afgetekend.

## Oordeel: PASS, met twee aandachtspunten voor de keurder
1. De lijfcontour linksboven in 5 i.p.v. zwart is zachter tegen de B-framelijn van het kleine paneel (Magneton doet het zo; regel "zwart alleen aan de schaduwkant"). Terugdraaien = één regel in `bouw_r13.py` (sectie LIJNEN).
2. De sikkel rechts (3/4/5) volgt de bijna rechte rechterrand en is daardoor vrij recht; geen banding rondom (links/boven zitten hooglicht en basis), maar een keurder mag het op 8× bekijken.

## Bestanden
`sprite.png`, `sprite_8x.png`, `r13.npy`, `vel.png` (r12 8× | r13 8× | model; r13 2× naast Magnemite, Magneton, Claydol, Glalie, Beldum, Metang, Lunatone; 1× op licht en donker), `studie_gen3_6x.png`, scripts hierboven.
