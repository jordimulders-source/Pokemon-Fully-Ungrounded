# Eindronde Palpaca: kleur, schaduw en belijning (Dragonfly Cave), 19 nov

## Jordi (letterlijk)
- Over r4: "ja de hele sprite is echt veel beter nu, ik vind hem goed genoeg om naar de eindronde te sturen voor kleur, schaduw en belijning, dragonflycave. Alleen de torso mist nog een beetje perspectief"
- Eerder: "het gaat vooral om perspectief" · "dat de kop hoekig leest moet je oplossen met kleurgebruik en schaduwen" · "Je mag echt veel meer het model gaan namaken" · "hij moet een cute starter zijn"

## Basis
- `r4/palpaca.png` + `r4/normal.pal` (goedgekeurd als basis). Model: `../model/model.png`.
- Silhouet en pootstand blijven (alfa-diff met r4 = 0 px), tenzij een losse pixel aan de rand volgens Dragonfly Cave weg moet (meld die exact).
- Vorm, gezicht, kuif, oog en binnenlijnen uit r4 blijven; alleen uitvoering verbeteren.

## Opdracht
1. **Torso-perspectief** (Jordi's punt): de romp moet als een rond, driekwart gedraaid volume lezen, door kleur en schaduw zoals het model: borst naar de kijker (lichter, licht linksboven), verre flank en buik in schaduw, schaduwovergang die de ronding volgt (sikkel), schaduw waar de nabije voorpoot en de nabije achterpoot in het lijf overgaan, de verre kant donkerder. Kijk naar het model waar licht en schaduw op de romp liggen.
2. **Dragonfly Cave-eindronde** (`docs/lessen/SPRITING.md`, `docs/lessen/bronnen/`, `docs/lessen/FAKEMON_CHECKLIST.md`): kleurramps (genoeg contrast tussen tinten, geen te dicht bij elkaar liggende tinten), schaduw (consistente lichtbron linksboven, geen pillow shading, geen banding), belijning (selout: gekleurde lijn aan de lichtkant, donker aan de schaduwkant; geen jaggies; binnenlijnen niet te zwaar; geen losse/verdwaalde pixels; de losse vlekjes op lijf en poten bij y 43 en y 47–49 weg). Alleen uitvoering, geen herontwerp.
3. ≤16 kleuren incl. transparant; kleuren blijven die van het model (r4-palet), tinten mogen bijgesteld worden voor contrast.

## Lever
`r5/`: `palpaca.png`, `normal.pal`, scripts, `NOTITIES.md` (DFC-punten met MOET/MAG en pixelcoördinaten, wat je per punt deed, alfa-diff met r4), `vel.png` (model | r5 | r4 op dezelfde hoogte 8×; torso close-up 12× model | r5 | r4; kop 12× r5 | r4; 1× en 2× op licht en donker). Geen git commit/push.
