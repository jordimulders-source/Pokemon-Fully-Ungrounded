# Spooktrein fase 3 (Steel/Ghost), frontsprite

Model: `model/model.webp` (= `gemini/r9/v11.webp`, prompt v11). Lijn, besluiten en alle citaten: `docs/concept/IDEEEN.md` (Trein-/spooktrein-Pokémon); prompts en rondes: `gemini/`.

## Jordi (letterlijk, 15 nov) bij het model
- "Beter, zou dit vertalen naar een sprite? Inclusief de geest bovenop, ik vind zijn mond geniaal. Hij zou wel iets anders gevormd mogen worden nog, maar de hele pose is onmiskenbaar een geest die geniet van de snelheid en dat is het doel"
- Eerder: "het moet echt een stuk schroot zijn dat zonder de geest van ellende uit elkaar zou vallen, maar nu is het een razendsnel voertuig geworden, en de geest heeft er ontzettend veel lol in, een beetje zoals rotom"
- Kleur: roestbruin met een beetje donkergrijs; het groen is de geest.

## Werkwijze
Gemini-model namaken (`docs/lessen/SPRITE_WERKWIJZE.md`, `GEMINI.md`, `SPRITE_KERN.md`): eisen alleen (1) accuraat op het model, (2) Gen 3.
- `model/natief.py`: eigen raster terug (pitch 10,24 → 99×99, wezen 86×83).
- `model/schrap.py`: 22 kolommen en 21 rijen geschrapt → `model_64.png` (64×62, elke pixel een modelpixel). Ruwe onderlaag: gezicht iets vervormd, kleine geest en vage wolken zijn ruis; dat lost de makerronde op.
- Open: hoe de kleine geest "iets anders gevormd" moet (vraag aan Jordi). Vage, halfdoorzichtige wolken: in Gen 3 als egale lichtgroene wolkvormen met omlijning (vertaling, geen ontwerpwijziging).

## Goedgekeurd (bevroren)
- 16 nov, r9: "al het groen is goed nu, nu de trein zelf nog" (kleine geest, wolken, geestwielen, groene kieren).
