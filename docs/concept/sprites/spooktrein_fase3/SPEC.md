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
- 16 nov, r13: "de koeienvanger isn nog steeds niet mooi" → Jordi tekende lijnen (`jordi/koeienvanger_lijnen.png`); "Schuif maar 2 pixels naar rechts, maar zorg wel dat de vlammen niet afgekapt worden"; "de kleuren en schaduw op het hoofd zijn ook nog niet mooi".

## Af (16 nov)
`af/spooktrein.png` (+ `_8x`) = r19: eindkeuring PASS (`af/eindkeuring.md`). Open voor Jordi: losse zwarte pixel (25,31) in de bevroren gezichtslijnen weg of houden; lichtbruine tint 14 op de kop.
- 16 nov (na af): "losse pixel mag weg, evenals rechts van de mini geest is er een lijntje en er zijn 2 losse pixels onder de koeienvanger, die koeienvanger moet trouwens nog beter" → r20 (pixels weg), koeienvanger volgt.
- 16 nov, r23 (na tweede schets `jordi/koeienvanger_lijnen2.png`, "veel klopt al wel hoor"): "alleen de rechtse < moet iets kleiner".

## Af, versie 2 (16 nov)
`af/spooktrein.png` = r24 (losse pixels weg, koeienvanger volgens Jordi's schets, "<" 3 px; keuring PASS `af/keuring_r24.md`).
- 16 nov: strenge keuring vond twee even lichte groentinten; Jordi: "ja, breng daar ook meer verschil in" (paletronde metaal + groen, r26).

## Af, versie 3 (16 nov)
`af/spooktrein.png` = r27: strenge eindkeuring (schaduw, kleuren, lijnen, Dragonfly Cave) PASS na r25 (8 px) en paletrondes r26/r27 (metaal + groen meer contrast, grijs weer grijs). Keuring: `af/strenge_keuring_r27.md`.
- 16 nov: "de zwarte lijnen in het gezicht en de koeienvanger voelen nog wat hard" → r28 A/B; Jordi: "A is het beste" (binnenlijnen index 15 = (62,32,26)).
