# Pinsir-evolutie frontsprite, ronde 9

Jordi bij r8 (letterlijk): "wat is er gebeurd met het hoofd?", "lekker opnieuw tekenen want dat kan je zo goed", "gewoon het model volgen", "je moest alleen de ogen een paar pixels aanpassen".

Bestanden: `pinsir_evo_r9_<oog>_<schild>.png` (A_A, A_B, B_A, B_B; 64×64, geïndexeerd, index 0 transparant, 16 kleuren, palet = r7/r8), `bouw.py` (`cd pinsir_evo && python3 sprite_r9/bouw.py [raster]`), `vel.png`.

## Opbouw (per script gecontroleerd in bouw.py)
- **Kop = r7 met kopstekels** (`sprite_r7/pinsir_evo_r7.png`), pixel voor pixel. Dat geldt voor het kopschild, de stekels, het gezicht en de rug boven het schild. Kopzone: rij ≤ 23 tot en met x45, plus rij 24–28 tot en met x44 zonder het dekschild. Diff met r7 buiten de oog- en naadpixels: **0**.
- **Rest = r8** (`sprite_r8/pinsir_evo_r8_A_<schild>.png`). Dat zijn de kaken, de mond, de romp, de arm, het been, de staart, de rugdoorns langs het schild en het dekschild A of B. Diff met r8 buiten de 4 naadpixels: **0**.

## Pixels die niet uit r7 of r8 komen
**Ogen** (puntiger, niet kleiner, zoals het model: wig met de punt naar het midden). Notatie (x,y), oud→nieuw, T = oogwit, K = zwart:

| Pixel | Oog | Variant | Wijziging | Gevolg |
|---|---|---|---|---|
| (22,27) | nabij | A en B | K→T | De rij erboven komt erbij. Het oog wordt een wig met de punt links (x21, onderrij) en de hoge kant rechts, zoals het model. |
| (23,27) | nabij | A en B | K→T | idem |
| (22,28) | nabij | alleen A | T→K | Pupil onderin het midden, zoals Gen 3 Pinsir en r8 A. Het model heeft daar ook een donkere scheiding. |
| (17,28) | ver | alleen B | K→T | De onderrij wordt naar het midden verlengd en het oog wordt een wig. |
| (18,28) | ver | A en B | K→T | idem. In A blijft de r7-zwarte (17,28) staan als pupil. |

- Nabij oog: 3 px (r7) → B 5 px, A 4 px + pupil.
- Ver oog: 2 px → B 4 px, A 3 px + pupil.
- De plek van de ogen is niet verschoven.

**Naad** tussen de r7-rug en de eerste r8-rugdoorn: de r8-rugrand lag 2 px verder rechts.
- (20,46) en (21,46): de losse r8-lijnresten zijn weg (→ transparant).
- (22,45) en (22,46): lijn (K), om de r7-buitenlijn door te trekken naar de voet van de doorn.

## Opmerkingen
- De kop is weer de r7-kop. Die heeft de kleur en de gewelfde vorm van het model. Alles wat Jordi bij r7 over de kop zei ("de vorm van het hoofd is niet mooi", "de stekels zijn nergens echt netjes") is dus ook weer terug. Volgens Jordi's laatste instructie is aan de kop alleen het oog veranderd.
- Vel: kop op 12× (r9 | r8 | r7 | model), r9 oog B en A met het modelmasker als rode omtrek, 1× alle varianten op licht en donker, en de hele sprite r9 | model op 8×.
