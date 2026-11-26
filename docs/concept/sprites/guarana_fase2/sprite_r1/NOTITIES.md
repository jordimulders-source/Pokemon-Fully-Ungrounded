# Guaraná fase 2, ronde 1 (maker)

Bestanden: `guarana2_r1.png` (64×64, geïndexeerd), `normal.pal` (JASC, = palet fase 1 `../../guarana/af/normal.pal`, ongewijzigd), `vel.png`
(sprite 8× | model 8×, close-ups van de drie trossen 12× naast het natieve model, 1× op 5 achtergronden + model 1×), `kaal.png`/`kaal_8x.png` (kale reductie),
`model_64.png` (model op spriteschaal), `natief_r10.png` / `natief_model.png` (natieve rasters), scripts hieronder.
Volgorde om te bouwen (vanuit `guarana_fase2/`): `python3 sprite_r1/natief.py && python3 sprite_r1/kaal.py && python3 sprite_r1/bouw.py && python3 sprite_r1/controle.py && python3 sprite_r1/vel.py`.

## Wat ik deed
1. **Rasterpitch r10** (kamscore randsterkte, zelfde meting als `guarana/gereedschap/pitch.py`): cel = **5,12 px** (1024/200), randen op 4,1 + k·5,12 in x én y.
   Score op het raster 3,0–3,2, een halve cel ernaast 0,18–0,19: het raster is echt. (10,24 en 15,36 scoren ook hoog, maar zijn veelvouden van 5,12; op 4× zoom zijn de blokjes ±5 px.)
   Let op: fase 1 gebruikte 10,24 (2× deze cel).
2. **Compositie opnieuw op het raster** (`natief.py`, logica van `plak/dubbel.py`, nu per natieve cel): offsets [(45,40),(-45,45),(-45,40)] px afgerond op hele cellen
   → (9,8),(-9,9),(-9,8) cellen = (46,1|41,0), (-46,1|46,1), (-46,1|41,0) px (max. 1,1 px verschil met `model.png`). Van elke tros wordt alleen de samenhangende
   hoofdmassa (≥ 20 cellen, 8-buren) gekopieerd: de **losse plakrestjes** (o.a. links van de middelste tros) zijn daarmee weg. Resultaat: `natief_model.png` (199×199, `natief_model_5x.png` om te bekijken).
3. **Maat**: figuur natief 176×146 → schaal 62/176 → sprite **62×51** (x1–62, y1–51), onderkant op y51 zoals fase 1. De bovenkant van de grote lus raakt y1.
4. **Kale reductie** (`kaal.py`): per spritepixel de dekking per klasse (zwart/rood/groen/oogwit, `klassen2.py` = regels van fase 1 `klassen.py`);
   zwart bij ≥ 40 %; donkerrood (L<72, de modellijnen tussen de vruchten) + zwart ≥ 45 % in rood → lijnrood 2; vultint rood uit het aandeel licht/schaduw in het
   vruchtvlees (drempels fase 1 r3); groen = dichtstbijzijnde groentint bij de gemiddelde groene modelkleur. Niets getekend.
5. **Regels op de reductie** (`bouw.py`, aantallen = pixels anders dan de reductie):
   - gaatjes van 1–2 px (witte modelspleetjes, ingesloten) dicht → binnenlijn: **15 px** (alpha-diff t.o.v. kaal = precies deze 15):
     (30,10) (22,14) (23,14) (21,15) (12,19) (13,19) (13,21) (16,21) (7,22) (38,22) (42,25) (50,26) (32,29) (52,45) (39,47).
   - lijnkleur: zwart binnenin → eigen lijntint (rood 2 / groen 6); buitenlijn zwart alleen met achtergrond rechts/onder, lichtkant = eigen lijntint;
     randpixels met een binnenbuur worden lijn: **526 px** (alleen hertinten/lijn maken van modelpixels, geen vorm).
   - wit/grijs buiten de ogen → lijntint van de buren: 6 px. Losse vultintpixels (geen 4-buur met dezelfde tint) → buurtint: 84 px.
   - dunne delen (rand zonder binnenbuur) met midden/licht → schaduwtint als selout: 14 px.
6. **Ogen** (245 px, de enige pixels die niet uit het model komen): oogplekken afgelezen op het natieve model met het spriteraster erover (`rooster.py`), maat per oog
   zoals in het model, kijkrichting zoals in het model. Opbouw en kleuren = het fase 1-oog (lijnrood 2 boven/links, zwart rechts/onder, oogwit 10, pupil 2×2 zwart):
   - **groot** (L4, L5, M4, R5, R6; model 7×6 incl. rand): het fase 1-oog (7×7) min één pupilrij: `..OOO.. / .OWWWK. / OWWWWWK / OWWWWWK / .KWWWK. / ..KKK..`, pupil 2×2.
   - **middel** (L2, M1, R1, R2; model 5×5): 6×5 (`.OOOO. / OWWWWK ×3 / .KKKK.`), pupil 2×2. Een 5×5-versie gaf een wit L-vormpje (pupil smolt met de rand).
   - **half dicht** (L1, M2, M3, R4; het model heeft daar een ooglid): zwarte lidrand bovenaan, één rij oog eronder, pupil 2×1 (L1) of 1 px (M2, M3, R4).
   - **klein/deels verstopt** (L3, R3): 4×4, pupil 1 px.
   - Volgorde achter → voor zoals in het model; stempels blijven binnen het silhouet van de reductie (zoals fase 1), oogwit dat daardoor op de buitenrand komt → rand.
   - Namen/plekken (linkerbovenhoek stempel): L1 (6,26) L2 (12,22) L3 (16,25) L4 (12,28) L5 (15,32) · M1 (30,12) M2 (24,16) M3 (20,19) M4 (29,19) · R1 (46,22) R2 (52,22) R3 (42,25) R4 (49,26) R5 (46,29) R6 (41,32).
   - **M5** (een wit spleetje van ±1,5 px tussen de vruchten van de middelste tros, `ogen2.py`) heb ik níet als oog gezet: op 64 px is er geen plek; nu donker zoals de reductie.

## Metingen (`controle.py`, op de png)
- 62×51, **10 kleuren incl. transparant** (palet fase 1; index 9 lichtgroen en 11 oogwit-grijs worden niet gebruikt).
- Lichte/midden tint op de buitenrand: 0. Losse zwarte pixels: 0. Alpha-diff t.o.v. kaal: 15 (de dichte gaatjes).
- Zwart met alleen achtergrond links/boven: 4 px, alle vier oogpixels op de rand: L1-pupil/lidrand (7,26)(7,27)(7,28) en R4-lidrand (51,26).
- Anders dan kaal: tros L 125 (ogen 68), tros M 142 (ogen 56), tros R 163 (ogen 90), rank/blad/rest 297 (ogen 0).

## Zwakke punten (zelf gezien)
- **Trossen zijn zwaar zwart**: oogranden + modellijnen samen geven donkere klonten, vooral in de rechtertros (R1/R4/R5) en onder L4/L5. De losse vruchten zijn op 8×
  maar half te onderscheiden; op 1× lezen trossen met ogen wel.
- **Ogen zijn hoekiger dan in het model** (stempels; ronde modelogen van ±5 px worden blokjes). Op 1× lezen ze als wit oog met zwarte pupil.
- **Half dichte ogen** (L1, M2, M3, R4) lezen op 1× als donkere streepjes met een wit puntje, niet als oog.
- **Getwijnde liaan**: de twijnlijnen komen als groene binnenlijnen door, maar de strengen zijn minder duidelijk dan in het model; vlekkerig groen in de stam.
- Rode vruchten hebben weinig hooglicht (licht rood 5 = 44 px); het model is lichter/oranjer in de trossen.
- Rasterbasis 5,12 px i.p.v. 10,24 van fase 1: bewust (gemeten), maar anders dan in fase 1.

## Open vragen voor Jordi
1. Half dichte ogen (4×, het model heeft daar een ooglid): zo laten (half dicht, zoals het model), of als open fase 1-oog?
2. Het mini-oogje M5 in de middelste tros (±1,5 px in het model) is weggelaten: akkoord?
3. Ogen bij grote overlap (L4/L5): L4 ligt nu vóór L5 (L5 is aan de rechterkant afgesneden door de rand van de tros). Goed zo?
