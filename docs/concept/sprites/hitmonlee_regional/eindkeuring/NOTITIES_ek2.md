# Eindkeuring 2 (ek2) – regionale Hitmonlee (glas, omhaal)

Keurder: verse, onafhankelijke eindkeuring (schaduw + belijning + kleurtinten), 27 nov. Basis: `ek1.png`.
Bestanden: `ek2.png` (64×64, geïndexeerd, palet ongewijzigd: 15 kleuren + index 0), `ek2_8x.png`, `vel2.png` (ek1 8× | ek2 8× | model r2 natief raster op dezelfde schaal; 1× licht/donker).
Gemeten tegen `sprite/natief.png` (via `sprite/raster.py`) en `sprite/M_gem.npy` / `M_donker.npy` / `M_zonderlijn.npy` (r13-raster = ek-x − 2).
Eigen oordeel gevormd vóór het lezen van `NOTITIES.md` (ek1).

## Oordeel
- **Eis 1, accuraat op het model: PASS.** Pose (omhaal, trapbeen boven, standbeen rechts, armen naar de grond), silhouet, beide ogen (nabij ovaal met oranje iris en glans, ver oog klein met glans), ringen op beide benen, polsring, dunne vingers, kussentjes, teentjes van de rechtervoet, de inkeping tussen romp en trapbeen en het doorschijnende kickbeen in de romp volgen het model. Steekproeven per pixel (oog, trapvoet, rechtervoet, verre hand, overgang romp/dij) kloppen met de modelmeting. Geen toevoegingen.
- **Eis 2, Gen 3: PASS.**
  - Belijning: 1 px, donkerrood selout boven/links, zwart rechts/onder; scan op om-en-om langs de rand: 0 treffers. Zwart binnenin alleen bij ogen, lijn romp/dij, vingers verre hand, teentjes en knie (allemaal waar het model een donkere lijn heeft). Eén kartelpixel gevonden en hersteld (zie onder). Uitstekende pixels bij de ringen (trapbeen links, standbeen rechts) zijn de ribbels van het model, net als bij de Gen 3-Hitmonlee: blijven.
  - Schaduw: licht linksboven (witte glans op koepel, schouderbol, trapvoet, ogen), gloeiend geelwit hart dat naar rood afkoelt naar de randen; doorschijnend been zichtbaar door de romp. Glas leest als glas op 1× (licht en donker).
  - Kleurtinten: 15 + transparant; ramps oplopend zonder trapjes-banding; geen losse spikkels buiten de ringen/glanspunten.

## Wijziging (1 px, silhouet 0 px veranderd)
| pixel (64×64) | oud → nieuw | reden | meting |
|---|---|---|---|
| (30,3) | 1 → 2 | punt van de hiel van de trapvoet stak als losse zwarte kartelpixel uit (1 buur); nu doorlopende donkerrode selout zoals de rest van de voetbovenkant | M_donker (28,3) = 2 |

## Open (bewust niet gedaan)
1. **Linkerwand van de romp loopt ±10 px recht** waar het model een rondere koepel heeft (gevolg van rijen/kolommen schrappen). Vormwerk, geen kleine reparatie; ter info voor Jordi.
2. **Romp is "van binnen naar buiten" belicht** (heet hart, alle randen donkerder): lijkt op pillow shading, maar is precies wat het model doet (gloeiend glas). Laten staan.
3. **Doorschijnende dij boven de romp** gebruikt bruinmauve (13) en tan (14): op 1× iets grijzig vergeleken met het bleke model, maar het zijn de gemeten modeltinten; aanpassen = palet/interpretatie. Jordi laten kijken.
4. **Ringen 1 donker / 1 licht** met tintwissels binnen een lichte band (bv. rij 12): volgt het model (glansstreep per ring), geen ruis. Laten staan.
5. **Zwarte vingerlijnen in de verre hand** (model meet daar donkerrood 2): gehouden omdat de vingers op het donkerrood anders wegvallen; ek1 koos hetzelfde.
6. Eerdere open punten uit ek1 (schouderbol en vingertopbolletjes lezen op 1× niet als aparte bolletjes) onderschreven: vergt vorm, niet tint.
