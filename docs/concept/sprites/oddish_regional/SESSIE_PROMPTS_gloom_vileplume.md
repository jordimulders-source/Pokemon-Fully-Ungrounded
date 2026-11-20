# Sessieprompts voor de Gloom- en Vileplume-sprites (20 nov)
Voor losse Claude Code-sessies (Jordi: "geef ook maar prompts voor gloom en vileplume, dan zet ik losse gesprekken daarvoor aan het werk in claude code").

## Gloom
```
Maak de frontsprite van de regionale Gloom (onderwater-Oddish-lijn, Water/Fire) naar een bevroren Gemini-model.

Haal eerst de branch claude/wonderful-cannon-0ypwq9 binnen (git fetch origin claude/wonderful-cannon-0ypwq9) en werk vanaf die stand: daar staan het model, de SPEC en de lessen van vandaag. Lees docs/concept/sprites/oddish_regional/SPEC.md (onderaan "Bevroren modellen").

Volg de vaste werkwijze "Gemini-model namaken" (docs/lessen/SPRITE_KERN.md, SPRITE_WERKWIJZE.md, GEMINI.md): één maker-agent, model OVERNEMEN en verkleinen, niet hertekenen; daarna een onafhankelijke keurder; pas dan naar mij, op 64×64 én 8×.

- Model: docs/concept/sprites/oddish_regional/referenties/gemini_gekozen_gloom.png. Dieprood gelatineus lijf met vinnetjes, dichtgeknepen ogen, open mond met gloeiend oranje kwijl, bovenop één zwarte lavabrok met gloeiende kieren, slap hangende verschroeide kelp links en rechts.
- Formaat: als de Gloom in de game (graphics/pokemon/gloom/anim_front.png, bovenste 64×64: x7–54, y12–52, ±48×41 px), zelfde onderkanthoogte.
- Let op: bij gewoon verkleinen verdwijnen het kwijl, de mond en de kieren in het rood/zwart. Kies in het palet een fel oranje-geel voor alleen die gloeiende delen (de modelkleur, niet donkerder), zodat Fire leesbaar blijft.
- Voorbeeld van dezelfde lijn: de Oddish-sprite in docs/concept/sprites/oddish_regional/oddish_sprite/ (zelfde methode en gereedschap in gereedschap/).
- Werkmap: docs/concept/sprites/oddish_regional/gloom_sprite/. Commit en push na elke ronde, changelogsectie bij oplevering.
```

## Vileplume
```
Maak de frontsprite van de regionale Vileplume (onderwater-Oddish-lijn, Water/Fire) naar een bevroren Gemini-model.

Haal eerst de branch claude/wonderful-cannon-0ypwq9 binnen (git fetch origin claude/wonderful-cannon-0ypwq9) en werk vanaf die stand: daar staan het model, de SPEC en de lessen van vandaag. Lees docs/concept/sprites/oddish_regional/SPEC.md (onderaan "Bevroren modellen").

Volg de vaste werkwijze "Gemini-model namaken" (docs/lessen/SPRITE_KERN.md, SPRITE_WERKWIJZE.md, GEMINI.md): één maker-agent, model OVERNEMEN en verkleinen, niet hertekenen; daarna een onafhankelijke keurder; pas dan naar mij, op 64×64 én 8×.

- Model: docs/concept/sprites/oddish_regional/referenties/gemini_gekozen_vileplume.png. Wit/parelmoer lijfje op twee lange dunne steltpoten, bovenop vijf rode/oranje open zeeanemonen in een ring rond een zwarte krater die oranje gloeit.
- Eén toegestane afwijking (mijn akkoord, optie A): de vele dunne tentakels per anemoon worden op 64×64 rode ruis. Klonter ze tot ±8–10 dikke, korte tentakels per anemoon, op de plekken en in de richting van het model, met een donkere rand om elke anemoon. Verder niets veranderen.
- De krater moet leesbaar blijven: zwarte rand, fel oranje-gele binnenkant (modelkleur).
- Formaat: als de Vileplume in de game (graphics/pokemon/vileplume/anim_front.png, bovenste 64×64: x4–59, y5–56, ±56×52 px); de steltpoten maken hem hoger, dus laat de breedte van de top ±die van Vileplume zijn en controleer dat alles binnen 64×64 past.
- Voorbeeld van dezelfde lijn: de Oddish-sprite in docs/concept/sprites/oddish_regional/oddish_sprite/ (zelfde methode en gereedschap in gereedschap/).
- Werkmap: docs/concept/sprites/oddish_regional/vileplume_sprite/. Commit en push na elke ronde, changelogsectie bij oplevering.
```
