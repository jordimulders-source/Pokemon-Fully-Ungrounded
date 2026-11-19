# Llamauler r5 (19 nov): vanaf r4b, kleuren/schaduw consistent en minder rechte lijnen

Jordi over r4b, letterlijk: "beter, nu nog de kleuren en schaduwen consistent maken, plus de rechte lijnen minder recht maken, bovenop de rug bijv, of aan de rechterkant tussen staart en poot". Eerder: "de vorm is goed" (poten) · "de kuif heeft een rechte lijn, evenals de rug is ook een volledig rechte lijn, ik zie heel veel overdreven rechte lijnen".

## Bestanden
- `lama.png` (64×64, index 0 transparant), `normal.pal` (15 kleuren + transparant).
- `vel.png`: r5 | r4b | model (8×) · close-ups 12× model op spriteraster | r5 | r4b van rug/achterwerk en kop/kuif · 1× en 2× (r5, r4b) op licht en donker.
- Scripts (`scripts/`, draaien met `python3 maak.py`): `stap1_vacht.py` (vachttonen), `stap2_bogen.py` (wolbogen in de omtrek), `stap3_lijnen.py` (binnenbogen, kleedrand, buitenlijn), `stap4_kleding.py` (kleed, polsbanden, handschoenen, losse pixels), `maak.py` (keten, png/pal, alfa-diff per zone), `vel.py`, `check.py`; meting: `meet.py`/`meet_toon.py` (modeltoon per spritepixel), `profiel.py` (modelomtrek per kolom/rij, subpixel), `naast.py`, `palet.py`.

## 1. Kleuren en schaduw consistent
- **Vacht van lijf, hals en kop** (rij 7–46; poten van r4b blijven): één ramp 6 licht / 5 basis / 4 schaduw, licht linksboven.
  - Grote vormen uit het model: modeltoon per pixel (wol zonder lijnen) glad over 3×3; ≥ 163 → licht, < 136 → schaduw (lichte borst, voorpoot-schouderbol en kap; donkere buik, romp-achterkant).
  - Lichtrichting: ≤ 2 px van de omtrek linksboven → licht, ≤ 3 px van de omtrek rechtsonder → schaduw (de schaduwsikkel langs de achterkant van hals en kop, de onderbuik en het achterwerk). Bij beide beslist het model.
  - Rust: 3×3-meerderheid, vlakjes < 4 px weg, losse vachtpixels naar de buur. Alle oude mengtonen en losse binnenlijnen in de vacht zijn weg; gezichtslijnen (mond, neusgat, kaak), oog, oren en kwastjes blijven.
- **Buitenlijn**: lichtkant (lege buren linksboven) zachte lijn 2, schaduwkant donker 1, gladgestreken (niet om en om). Kleedrand blijft 1.
- **Kleed** (model: boven helderheid 100–120, onder 70–80): boven rood 10 met licht 11 op de bovenkant links, zijkanten van de omslag 9; onder 9 met de twee gemeten lichte strepen (x 34, 39) in 10. Geen vlekken meer. Onder en naast het kleed een donkere rand 3 op de wol (de zwarte kleedrand van het model).
- **Polsbanden**: nabij als band licht (8, nieuw) / grijs 15 / donker 1 van boven naar onder; ver een stap donkerder (15 boven, 1 onder), op de plek van de modelband (rij 55–56).
- **Handschoenen**: per pixel licht/basis/schaduw uit de afstand tot de rand: nabij 11/10/9, ver 10/9/9. Twee grijze nagels onder de verre handschoen (23,61) en (25,61); crème nagels nabij zoals r4b.
- **Palet**: index 8 (iris) wordt het licht van de polsband, 129 118 117 (model-grijs helderheid 100–140); de iris (18,15) wordt grijs 15. Overige kleuren gelijk aan r4b.

## 2. Rechte lijnen minder recht (wolbogen, gemeten in model_v3)
Modelomtrek per kolom/rij met `profiel.py`; bulten (uitstulping) en inkepingen op de gemeten plekken, 1 px diep, met binnenin een korte boog (3) vanuit elke inkeping (Mareep-schulp).
- **Rug**: wolboog x 44–45 een rij hoger (model top 26,90/26,71); inkeping x 42 (model 27,44; x 43 was al ingekeept, 27,76); x 49 een rij lager vóór de staart (27,35), zodat de rug in een boog naar de staart loopt. Kleedbult x 35–37 een rij hoger (model 26,90/26,71/26,71: het kleed ligt over een wolbult). Bogen binnen: (43,29)(43,30), (48,29).
- **Achterwerk** (rechts tussen staart en achterpoot): inkepingen rij 35 (onder de staart, 49,34), rij 40 (49,18) en rij 43–44 (48,58/48,55), zodat er drie bogen zijn (rij 36–39, 41–42, 45–46). Bogen binnen: (46,40)(45,39), (46,43)(45,43).
- **Kuif/kap**: de rechte binnenlijn onder de kap (rij 12, x 12–19) is vervangen door drie bollen met een ronde onderkant (model: bollen x 11,5–14 / 14–16,5 / 16,5–19, onderrand y 12,0–12,5): lijn op (12,11)(13,12)(14,12)(15,11)(16,12)(17,12)(18,11)(19,12), bovenkant van de bollen licht. De bovenomtrek van de kap volgde het model al (x 15–17 rij 7, 18–19 rij 8).
- **Hals achter**: de omtrek had al inkepingen op rij 17, 21 en 24 (model 24,19 / 24,12 / 24,25); nu met een boog naar binnen (22,17)(21,18), (22,21)(21,22), (22,24)(21,25).
- **Hals voor**: boog rij 24–25 (12,25 erbij; model 12,50/12,53), inkeping rij 26 (12,72) met boog (14,26)(15,27).
- **Onderbuik**: inkeping x 29 (model 47,58; x 32 was al ingekeept) met bogen (29,45)(30,44), (32,44)(33,43).
- Binnen ook geen lange rechte lijnen meer in de wol: schouderbol tegen de borst als boog (20,40)…(17,46) en de achterbol boven de achterpoot als boog (36,42)…(36,46).
- Poten (vorm), kop, oren, gezicht, halsband en kleedvorm: silhouet ongewijzigd.

## Alfa-diff met r4b per zone (13 px)
| zone | px | welke |
|---|---|---|
| rug | 7 | + (35,26)(36,26)(37,26) kleedbult, + (44,26)(45,26) wolboog, − (42,27) inkeping, − (49,27) vóór de staart |
| achterwerk | 4 | − (49,35), (48,40), (48,43), (48,44) |
| hals | 1 | + (12,25) |
| buik | 1 | − (29,47) |
| kop, poten, kleding | 0 | |

Kleur anders dan r4b: 275 px. Box 43×62, 1396 px. 15 kleuren + transparant.

## Zwakke punten
- De kleedbult (x 35–37) is gemeten, maar oogt op 8× als een rechthoekig opstapje; zonder bult is de bovenkant van het kleed weer recht (x 27–39). Keuze voor Jordi/Claude.
- Kleed is nu rustig maar vrij effen (twee vlakken + 2 strepen); het motief van het model is weg.
- Wolbogen in de omtrek zijn 1 px diep (het model heeft op deze schaal ±0,3–0,5 px); dieper zou verder van het model gaan.
- De lichte kant van hals en borst is een smalle strook 6 langs de omtrek (lichtrichting-regel); kan als banding lezen.
- Poten van r4b niet aangeraakt (alleen polsbanden, handschoenen en nagels).
- Niet gekeurd.
