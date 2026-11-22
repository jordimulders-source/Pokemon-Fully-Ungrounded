# Nocticue (nachtaap fase 1): nieuwe frontsprite naar Gemini r4 (19 nov)

## Jordi letterlijk (19 nov)
- "Laten we Nocticue nog wat oppoetsen, belangrijk, ik ben echt fan van het design, dus het is puur de pose. De cuteness moet niet weg" · "ook de positie van zijn armen" · "dus puur de hoek".
- "en hij moet niet glimlachen" · "het gelaat was goed" · "eigenlijk was alles prima, behalve de hoek en wat details in het spritewerk".
- Over Gemini r2: "Het rechteroog mag ronder, dat was een van de dingen die in de originele sprite niet perfect zijn".
- Over r4: "ik vind ronde 4 eigenlijk wel goed, flinke vooruitgang, ik twijfel alleen nog een beetje over het kleurgebruik tussen de twee ogen in".
- "lukt het niet, dan doen we het in de sprite fase" (de streep tussen de ogen) · "nee dit lukt hem niet, ga maar beginnen met de sprite, r4 als model".

## Model
- `referenties/gemini_gekozen_r4.png` = bevroren model (vorm, pose, hoek, onderdelen). Gemini-raster ±16 px per pixel; natief ±37×36 px, even groot als de oude sprite (44×36 met staart), dus natief raster 1-op-1 overnemen, niet verder verkleinen.
- Oude sprite (`referenties/oude_sprite_*`): het goedgekeurde design. Kleur mag altijd van het model afwijken (SPRITE_KERN); voorstel Claude: palet en tinten van de oude sprite.

## Toegestane afwijkingen van het model (alleen deze)
1. **Streep tussen de ogen** (Jordi: kleurgebruik tussen de ogen; Gemini r6 lukte niet): smaller, 2–3 px, twee violette tinten zoals in de oude sprite, volgt de ronding van de kop, geen rechte horizontale onderkant; de vrijgekomen ruimte wordt crème gezichtsschijf zodat het verre (linker) oog ook een smalle crème rand aan de binnenkant krijgt.
2. **Rechteroog rond** (Jordi): in r4 al rond; houden zo, geen platte/hoekige bovenkant.
3. Kleur/schaduw/belijning naar Gen 3 en de oude sprite.
