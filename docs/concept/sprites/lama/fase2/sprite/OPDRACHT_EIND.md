# Eindronde Llamauler: Dragonfly Cave-keuring + kleine reparaties (19 nov)

## Jordi (letterlijk)
- Over r5: "verder vind ik hem wel prima en als dat goed is mag die naar de eindkeuring" (r6 = r5 met kleed uit r4b en geleidelijkere achterste poot, `r6/NOTITIES.md`).
- Eerder: "ik zie heel veel overdreven rechte lijnen" · "de poten zijn nog veel te blurry" · "de vorm is goed" · "nu nog de kleuren en schaduwen consistent maken".

## Basis
`r6/lama.png` + `r6/normal.pal`. Model ter controle: `../gemini/poten/model_v3.png`.
Silhouet, pootstand, kop, gezicht, kleding blijven (alfa-diff met r6 = 0), tenzij een losse pixel aan de rand volgens Dragonfly Cave weg moet (meld die exact).

## Opdracht
1. **Keur eerst zelf** volgens Dragonfly Cave (`docs/lessen/SPRITING.md`, `docs/lessen/bronnen/`, `docs/lessen/FAKEMON_CHECKLIST.md`), naast 4–5 Gen 3-sprites (`graphics/pokemon/mareep`, `flaaffy`, `ponyta`, `girafarig`, `stantler`): kleurramps (contrast tussen tinten), schaduw (lichtbron linksboven, geen pillow shading, geen banding), belijning (selout, geen jaggies, binnenlijnen niet te zwaar, geen losse/verdwaalde pixels of dambordjes). Alleen uitvoering, geen herontwerp; ontwerpvragen alleen "ter info voor Jordi".
2. **Voer de MOET-punten uit** (kleine pixelreparaties, met coördinaten). MAG-punten alleen als ze zeker beter zijn; anders melden.
3. ≤16 kleuren incl. transparant.

## Lever
`r7/`: `lama.png`, `normal.pal`, scripts, `NOTITIES.md` (DFC-punten met MOET/MAG en pixelcoördinaten, wat je per punt deed, alfa-diff met r6), `vel.png` (model | r7 | r6 op 8×; 1× en 2× op licht en donker naast de Gen 3-voorbeelden). Lees eerst `docs/lessen/SPRITE_KERN.md`. Geen git commit/push.
