# Zandloper-lijn fase 2 (brein breekt uit) – besluiten

Lijn: fase 1 zandloper met ogen (`../fase1/af/`) → fase 2 → fase 3 zand-djinn (`../fase3/af/`). Ground/Psychic.

## Model (27 nov)
- Jordi: "de zandloper nu gebroken is (zoals in fase 3) en er zand uit ontsnapt, daar komt een relatief groot brein uit, met de ogen niet eraan vast, maar iets eronder en boven het brein ook in zand een vraagteken en uitroepteken, dit is allemaal verbonden aan elkaar".
- Over r1: "het moet 1 zandwolk zijn, zandloper kleiner en op de grond. Hij gebruikt de uitroepteken en vraagtekens als handen".
- Over r2: "zandloper is niet kapot en niet op de grond, het brein is een tekening en niet de vorm, verder wel prima".
- **Model = `model.png` = Gemini r3** (Jordi: "nice"). Prompts en rondes: `gemini/PROMPTS.md`.

## Sprite
- Maat: Jordi "maak de sprite van r3, maar wel kleiner" → koos **0,80** van het natieve raster (pitch 10,24) uit 4 maten (`sprite/maten/vel_maten.png`). Fase 1 wordt in een ander gesprek aangepast (Jordi).
- r1–r3 door een maker (alles uit het natieve model, palet van fase 1/3), r2 en r3 gekeurd (BIJNA); r4 = r3 + de laatste 3 keurderpunten (8 pixels, alleen tint). `sprite/r4/zandloper_fase2_r4.png`, 14 kleuren + transparant.
- Fase 1 is inmiddels op 0,70 (andere sessie, op main).
- Jordi over r4: "fase 2 is wat hard omlijnd". Gemeten: 47 zwarte binnenhoekjes van trapjes (lijn plaatselijk 2 px dik; fase 1: 4, fase 3: 1). r5 = r4 met die hoekjes in de vulling van hun buur (8-verbonden lijn, ogen ongemoeid, silhouet gelijk): `sprite/r5/`.
- Jordi: "het gaat niet om dunnere lijn maar kleur" → r5 vervalt; r6-varianten op r4 (ogen ongemoeid): A zwart → donker zandbruin, B zwarte buitenlijn → selout 2, C zwart alleen aan de onderkanten (`sprite/r6/vel_kleur.png`).
- Jordi: "prima, behoud r4 maar en stuur naar de eindkeuring" → r4 naar de DC-eindkeuring (`eindkeuring/`).
- Eindkeuring (DC, 66 px t.o.v. r4): 53 zwarte binnenpixels → lijnkleur van het eigen onderdeel, buitenrand zwart aan de schaduwkant, 13 outline highlights; silhouet en ogen diff 0. `eindkeuring/zandloper_fase2_ek.png`. Wacht op Jordi.
- **Af (Jordi, 27 nov):** "ja commit en push naar main" → `af/zandloper_fase2.png` (= eindkeuring). Op het overzichtsvel. Naam open.
