# Gengas sprite v3 (15 nov) – v2 + reparaties uit `../sprite_v2/keuring/KEURING_v2.md`

Niets from scratch: elke gewijzigde pixel komt uit het model (`model_64_geschrapt.png`, gekwantiseerd met het v3-palet),
uit het verschoven modelgezicht (zoals v2: +5 kol, +1 rij) of, voor de krul, uit het natieve model (`gekozen_v3_natief.png`).
Keten: `./bouw.sh` = `v3.py` (zones, log in `raster.txt.log`, zones in `zones.json`) → `manen.py` (log `tussen/manen.log`)
→ `maak.py` → `controle.py` → `diff.py` → `vel.py`.

## Palet
v2-palet met één ruil (MOET 5): **w** (kern lichtvlek 220,172,176; 18 px) eruit → **v**; **u** (121,70,91, gedempt mauve,
mediaan Lab-cluster in het model) erin. Gemeten (heel model, 16 → 15 tinten): zonder w gem. ΔE 2,84; alleen E (oogrood donker)
weglaten kost minder (2,79) maar sloopt het oog; m als vervanger van u is slechter dan b (gem. ΔE 33 vs 20 op de u-pixels).

## Per keuringspunt
| punt | wat | bron |
|---|---|---|
| MOET 1 | (51,22),(52,22) (x,y) transparant | model: ingesloten gat (wit 255) |
| MOET 2 | rechts van de grijns, rij 42-47: model op zijn eigen plek → bandgrens diagonaal (43,32)→(47,27) | model ongeschoven |
| MOET 3 | vrijgekomen strook: maskerrand schuin (36,8)→(37,10)→(38,14) naar de mondhoek; rij 29-32 loopt de u-wig van de rand (rij 25-28) versmallend door; rij 45-46 de m-band van het model (`Klmllm`, `Krmmmm`) → l→m→r naar de rand | modelbanden dezelfde rijen |
| MOET 4 | krul = natief rij 38-45 × kol 43-51 op sprite rij 32-39 × kol 36-44 (geschrapt worden nu de effen natief rij 46 en kol 42/52 i.p.v. rij 40 en kol 45/50 die door de spiraal liepen); lijn één tint b | natief model |
| MOET 5 | wig u terug: model rij 25-28 kol 10-13 op eigen plek, tussen/naast de ogen verschoven mee met het gezicht | model |
| MAG streep | rij 29: verschoven kopie van modelrij 28 weg; alleen kol 19-23 licht als verbinding tussen streep (rij 28) en wigtop (rij 30) | model |
| MAG manen | losse 1-px korrels binnenin: lichte → buurtint, donkere met donkere buur → g (krater); K binnenin (kraterkernen, teenlijnen) bevroren; silhouet/omlijning ongemoeid | model |
Gengar-vorm uit v2 behouden: pupil rechteroog, bovenlip als doorlopende zwarte lijn, tandschaduw één tint.

## Controles
- `diff.py` (v2 → v3): 18 paletruil, 2 MOET 1, 80 gezichtszone (rij 25-47, kol 8-33), 47 krul (rij 32-39, kol 36-44),
  4 manen; **buiten de zones gewijzigd: 0**.
- 15 kleuren + transparant. Silhouet t.o.v. model: (10,32) (v2) + het gat (22,51-52) (y,x), dat in het model wit/achtergrond is.
- Cirkelfit bol: rms 0,32 px, max 0,70 px (r 22,6) – onveranderd.
- Kraters (g-vlekjes binnenin): boven 2 (+ zwarte kraterkern), links 3, rechts 1 groot donker vlak (model), rechtsonder 2 (+ G-ring).

## Zwakke punten
- Lichtvlek heeft nu één tint (v) i.p.v. kern + rand: de prijs van de wig (meetbaar het goedkoopst na E).
- u ligt dicht bij b: de wig is subtiel, zoals in het model, maar op 1× nauwelijks te zien.
- Lichte strook links van de grijns is boven rij 45 nog effen l (het model heeft daar ook alleen l).
- Manen blijven iets korrelig (randselout g, K-kraterkernen bewust bevroren); de rechtermaan heeft geen losse kraters,
  maar één groot donker vlak zoals het model.
- De krul is nu 1 px breder/hoger dan in v2 doordat de spiraal niet meer geschrapt wordt (effen rijen/kolommen ernaast vielen af).
