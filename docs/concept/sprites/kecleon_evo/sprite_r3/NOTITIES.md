# Kecleon-evolutie, sprite r3 (maker-agent, 22 nov)

Opdracht: de 12 reparaties uit `../keuring/r2_dragonflycave.md` + Jordi over r2: "dit voldoet totaal niet aan de dragonflycave eisen denk ik?" en "Daarnaast zie ik de kecleon lijnen nog voldoende" → "niet voldoende bedoelde ik".
Gegeven en niet veranderd: silhouet (Jordi: "silhouet is prima") en de kleurbesluiten (geel/oranje hoofdkleur, roze aan de kaak, geen groen, wat groen was is oranje, gele lijnen geel).

## Werkwijze
- `rijen_r3.txt`: het hele raster opnieuw met de hand geschreven, rij voor rij (r2 alleen als kaart van de onderdelen). `|` is alleen leesbaarheid.
- `patch_r3.txt`: per-pixelreparaties na de eigen controle (regel `rij x tekens`; beeld-y = rij + 1).
- `bouw_r3.py` (raster → png, silhouet-assert tegen r2), `bouw_r3_palet.py`, `controle_r3.py` (metingen), `vel_r3.py`.
- Coördinaten hieronder zijn beeld-(x,y) zoals in de keuring.

## Palet (12 kleuren + transparant, alle tinten uit de r2-modelmeting, geen nieuwe families)
| | rgb | Y | rol |
|---|---|---|---|
| k | 23,19,19 | 20 | omlijning (model) |
| r | 143,55,53 | 81 | oranje lijn/selout (model r) |
| H | 182,76,66 | 107 | oranje schaduw (model H 166,63,64, iets lichter) |
| G | 226,112,74 | 142 | oranje midden (tussen model G en m) |
| F | 244,166,94 | 181 | oranje licht (model F 232,156,85, iets lichter) |
| E | 122,92,41 | 95 | mosterd lijn (model E) |
| C | 204,167,74 | 167 | mosterd schaduw (model C) |
| B | 240,196,100 | 198 | mosterd midden (model B 235,189,95, iets lichter) |
| A | 250,232,160 | 229 | mosterd licht (model A 241,216,128, lichter) |
| p / q | 232,160,152 / 204,102,109 | 181 / 133 | roze (model p/q) |
| w | 255,255,255 | | glans pupil |
Weggelaten: m (oranje tussentint) en D (donker mosterd), zoals de keuring vroeg.

## Reparatiepunten
1. **Ramp** ok: oranje F/G/H + r alleen lijn/selout (m weg); mosterd A/B/C + E alleen lijn (D weg). Stappen oranje 26/35/39, mosterd 31/31 (E→C 72, E is alleen lijn).
2. **Romp** ok: één middenvlak G; licht F als één schoudervlak linksboven (rij 20–28, vast aan de kop-/kaaklijn, loopt over in de bovenarm); schaduwsikkel H langs de rug rechts en onderaan. Losse F-eilanden (23–31,17–29), (31–35,39–41), (38,24), (40–41,28) weg. Op de verre dij één lichtvlak F linksboven (31–34,42–46), vast aan de buiklijn.
3. **Banding** ok: arm (licht 2–3 px linksboven, H-sikkel onderaan bij de pols), linkerbeen (F-vlak linksboven, H-sikkel rechtsonder, scheen klein F-vlak), rechterbeen (F-strook 2 px aan de lichte kant, H rechts).
4. **Buitenlijn** ok: E naast geel, r naast oranje, gecontroleerd met script (geen r naast alleen geel, geen E naast alleen oranje). Kruin zonder r/E-afwisseling (E alleen boven de gele band, r boven de oranje plaat). Onderkant kop en schaduwhoeken zwart. B op (5,5) → E.
5. **Doubles/klonten** ok: snuitpunt (1–3,23–24): mondlijn begint nu bij x4, de kaakpunt is geel; stekel (27–28,9–10) één pixel minder; (42–43,46–49) één lijn; zwarte klont (43–45,52–54) weg (alleen 1 px lijn; enige 2×2-zwart is de pupil).
6. **Binnenlijn arm/lijf** ok: taps H (boven) → r → k (onder), licht gebogen (x29 op y30–35 → x28 → x27 → x25–26 → x24 → hand).
7. **Buikklauwen** ok: drie klauwen van 2 px (B boven, C onder), gescheiden door E, met een doorlopende E-onderlijn; geen dambord meer.
8. **Buik** ok: A-lichtvlak groter linksboven (x11–15, y31–37), B midden, C-sikkel rechts/onder; kaakschaduw bovenaan de borst in C.
9. **Kop** ok: kuifstreep in 2 tinten (A/B); oogring gesloten, gelijkmatige r-lijn (ovaal, 1 px); gele band erbuiten (A aan de lichte kant, B onder, C aan de schaduwkant); glans naar de onderhoek van de pupil (16,18).
10. **Mond/kaak** deels: mondlijn golft (rij 23 → dip op rij 24 → mondhoek omhoog, taps k → r → H); roze 10 → 14 px (p boven, q eronder). De treden van de onderkaak (3,2,3,4) liggen vast in het silhouet (elke trede is buitenrand), dus niet regelmatiger te maken zonder het silhouet te wijzigen.
11. **Tenen** ok: per teen B boven, C eronder, zwarte onderlijn; geen E/B om en om.
12. **Inner-AA** ok: m bestaat niet meer.

**Jordi's punt, Kecleon-lijnen** (op 1× leesbaar, op licht en donker gecontroleerd):
- gele kuifrand langs de voorkant van de kuif en de snuit: E-buitenlijn + A-rand (was C/D);
- diagonale kuifstreep van de kuiftop naar de oogkegel: A/B (was B/C/D);
- ring om de oogkegel: gesloten r-ring met een gele band van 2 px eromheen;
- kaakstreep: gele onderlip die doorloopt langs de kaak (B/C);
- staart: drie heldere gele strepen (op de linkerkant van de krul en twee dwars over de staartbasis), spiraal als één lijn (r aan de lichte kant, k aan de schaduwkant).

## Metingen (`controle_r3.py`)
- Silhouet-diff met r2: **0 px**.
- Zwart 10,1% (doel 10–12) · p90 helderheid **198** (doel ≥195) · mediaan 142.
- Stappen: oranje 26/35/39, mosterd 31/31, roze 48.
- Losse pixels die over zijn: stekelpunten op de rug (1–2 px, onvermijdelijk zo klein), de taps uitlopende lijnen (mondhoek, kopachterlijn), toppen van de tenen/klauwen en twee hooglichtpunten op de kuif (20,2), (6,5). Geen ruis in vlakken.

## Resterende twijfels
- De romp is bewust rustig (G met één schoudervlak en een sikkel); een keurder kan hem nog wat effen vinden. Meer volume zou een extra vorm (borst/buikrand) in de romp betekenen die niet in het model staat.
- De gele band rechts van het oog (C, 3–4 px breed) leest als één mosterdstrook; zo staat het ook in het model (rechterrand van de kuif).
- De G-strook tussen de linker kuifplaat en de gele kuifstreep (x12–14, y4–10) is nodig voor contrast met A, maar ligt evenwijdig aan de streep.
- Onderkaaktreden: zie punt 10.
