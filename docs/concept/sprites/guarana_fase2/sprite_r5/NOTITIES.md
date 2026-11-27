# Guaraná fase 2, ronde 5: alleen de pupillen

Jordi (letterlijk): "de ogen zien er nu niet goed uit omdat ze allemaal precies dezelfde richting hebben, kijk naar hoe de eerste fase het deed";
"ja zorg dat er iets meer ogen naar linksonder kijken maar idd verschillende richtingen". Jordi koos variant A (oogrand lijnrood): "links is wat netter" → alleen A.

Bestanden: `guarana2_r5_A.png` + `normal.pal` (= r4), `voor_jordi_r5_8x.png`, `vel.png` (r5A | r4A | fase 1 op 8×, de drie trossen 12× r5A | r4A, 1× licht/donker).
Bouwen vanuit `guarana_fase2/`: `python3 sprite_r5/kaal.py && python3 sprite_r5/bouw.py && python3 sprite_r5/alleen_ogen.py && python3 sprite_r5/vel5.py`.

## Wat ik deed
- Kijkrichting per oog gemeten in het model (`kijkrichting.py`: pupilzwaartepunt t.o.v. het oogmidden, genormeerd; + = rechts/onder):
  M1 −0,09/+0,06 · M4 +0,31/+0,15 · R1 +0,37/−0,23 · L2 −0,04/−0,11 · R2 +0,09/−0,03 · L1 −0,39/+0,52 · R3 −0,33/−1,00 · R5 −0,19/+0,05 ·
  L4 +0,32/+0,05 · R6 −0,32/+0,04 · L5 +0,32/+0,05 · L3, M2, M3, R4 niet meetbaar (half dicht/verstopt).
- Elk oog een eigen pupilplek binnen het wit (`KIJK` en `PUPOPT` in `bouw.py`); maten als r4 (2×2 groot, L van 3 px middel, 1–2 px klein/half dicht).
  12 van 15 kijken naar links/linksonder/onder in gradaties: L1 l, L2 lo, L3 lh, L4 l, L5 mo, M3 l, M4 lo, R2 mo, R3 lh, R4 l, R5 l, R6 lo.
  3 kijken een andere kant op, zoals in fase 1: M1 rechts, M2 midden, R1 rechtsboven (= modelrichting). Buren staan nooit gelijk.
  (l = links-midden, lo = linksonder, lh = linksboven, mo = midden-onder, m = midden, r = rechts, rh = rechtsboven.)
- Witvorm groot: onderste rij `.KWWWK.` zoals fase 1 (in r4 stond daar de pupil).
- Pixeldiff t.o.v. r4A: 52 px, allemaal in de ogen; **buiten de ogen 0**. `alleen_ogen.py` zet r4A terug buiten het oogmasker, want de ruisstappen in
  `bouw.py` lieten 4 tinten buiten de ogen meeschuiven.
