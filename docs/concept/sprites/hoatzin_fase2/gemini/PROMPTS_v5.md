# Hoatzin fase 2: Gemini-prompt v5 (19 nov)

Op v4 r1, Jordi (met Cornell-foto: hoatzin op tak, vleugels hoog gespreid, kop laag naar voren, staart omlaag): "ik zou een meer open pose willen, misschien de veren op het hoofd wat meer bruin zoals de echte hoatzin, dit zou wel een hele vette pose zijn, maar weet niet of dat gaat lukken".
v5 = v4 + die twee wijzigingen. Nieuw gesprek; bijlagen: de Cornell-foto (pose) + het kopportret (kuif/gezicht). v4 r1 níet meesturen (Gemini kopieert dan de oude pose).

```
Draw a REAL HOATZIN as an official Gen 3 Pokémon front sprite (Ruby/Sapphire/Emerald style). Two photos of a real hoatzin are attached. Copy its anatomy, crest, face and proportions as faithfully as possible. This animal is already strange enough; it only needs these few changes:

1. POSE: copy the pose of the first photo: perched, both wings raised high and spread wide open above its back like a fan, body leaning forward, head low and pushed forward, long tail hanging down. Two wings only, one on each side.
2. Colors: the body is recolored in the typical Poison-type purple. Keep the real hoatzin's pattern (darker wing coverts with pale streaks, paler neck and chest, streaked neck, darker tail with a pale tip), just in purple shades instead of the rufous and buff.
3. Crest: BROWN like the real hoatzin's (see second photo), shaped like the photo (long, thin, stiff spiky feathers fanning up and back), but bigger and uglier: longer, more ragged and messier.
4. Face: keep the bare BLUE face skin exactly like the photo, and the real hoatzin eye: solid RED with a small black pupil, NO white of the eye, alert and watchful.
5. Belly: slightly more bulging than the real bird, a little rounded paunch.

Type: Poison/Dark. Everything else stays as on the photos: small head, short thick beak, long neck, big wings, very long tail, big clawed feet.
Style: 64x64, max 16 colors, 3/4 view facing left, clean dark outline, white background.
No effects: no gas, smoke, glow or stink lines; no ground, shadow or branch.
AVOID: crow, parrot, cockatoo, turkey, chicken, hair instead of feathers, a white ring around the eye, cute plush look, extra wings.
```

Uitslag v5 r1 (`v5_r1.webp`), Jordi: "pose is nu goed, maar de haren kloppen nog niet he". Kuif = dunne bruine haartjes over een donkerpaarse veerwaaier (twee kuiven door elkaar).

## v5 bijsturen: alleen de kuif (zelfde gesprek, of nieuw gesprek met v5_r1 + kopportret als bijlage)
```
Keep this sprite exactly as it is (pose, wings, body, colors, face, tail): change ONLY the crest.
Remove both the dark purple feather fan behind the head and the thin brown hairs. Replace them with ONE crest like the real hoatzin in the attached head photo: about 12 to 15 separate, stiff, spiky FEATHERS growing from the top of the head and radiating up and backward in a messy fan. Each feather is a thin shaft that widens slightly to a pointed tip. Color: rufous orange-brown with darker brown tips, like the real hoatzin. Make it bigger, more ragged and uglier than the real one: uneven lengths, some bent or sticking out sideways. Not hair, not strands, not a mohawk.
```

Jordi (19 nov) met een illustratie van een hoatzin (`ref_kuif_illustratie.png`): "moeten meer zo" (de kuif). Bijstuurprompt v2:
```
Keep this sprite exactly as it is (pose, wings, body, colors, face, tail): change ONLY the crest.
Remove both the dark purple feather fan behind the head and the thin brown hairs. Replace them with ONE crest copied from the attached illustration: a fan of many thin, stiff, spiky feathers that grows from the top of the head and spreads upward and backward, rufous orange at the base with dark brown tips. Draw it as clear pixel-art spikes (not single-pixel hairs), a bit bigger, more ragged and uglier than in the illustration. Not hair, not a mohawk, not a separate feather fan behind it.
```

Uitslag v5 r2 (`v5_r2.webp`, kuif als grote oranje bos), Jordi: "te overdreven, ik zal het nog een keer doen met een bronfoto, in nieuw gesprek". Prompt nieuw gesprek (bijlagen: v5_r1 + bronfoto van Jordi):
```
Attached: (1) a Pokémon sprite, (2) a photo of a real hoatzin.
Redraw sprite (1) exactly as it is (pose, wings, body, colors, blue face, red eye, tail, feet, size): change ONLY the crest.
Remove the dark purple feather fan behind the head and the thin brown hairs. Replace them with the crest of the real hoatzin in photo (2): copy its shape, size, number of feathers and colors as closely as possible (rufous orange feathers with dark tips, fanning up and back from the top of the head). Do NOT exaggerate it: not bigger, not denser, not a big bush. Clear pixel-art feathers, not single-pixel hairs.
Style stays: official Gen 3 front sprite, 64x64, max 16 colors, white background, no effects.
```

Uitslag v5 r3 (`v5_r3.webp`: kuif als brede potloodveren met rode band, vleugelpunten ook oranje), Jordi: "dit gaat fout".
Plan (Claude): kuif als los asset laten tekenen en zelf op v5_r1 plakken (les mate-kano / vuurwerk asset voor asset). Assetprompt (nieuw gesprek; bijlagen: v5_r1 + kopportret):
```
Attached: (1) a Pokémon sprite, (2) a photo of a real hoatzin's head.
Draw ONLY the head of sprite (1), at exactly the same pixel size, angle and colors (blue face, red eye with black pupil, grey beak, purple neck feathers), on a white background. Give it the crest of the real hoatzin in photo (2): about 12 to 15 thin, stiff feathers that fan up and back from the top of the head, each 2 pixels wide, rufous orange with dark brown tips, uneven lengths, spaced apart so you can see between them. Same size as in the photo, not exaggerated: not a bush, not a fan of broad feathers, no red band, no hair.
Style: official Gen 3 front sprite pixel art, max 16 colors, clean dark outline, no effects.
```

Uitslag v5 r4 (`v5_r4.webp`, Jordi via Gemini: kuif bruin): goede stand. Jordi: "nu wil ik nog nadenken over de rest van het design, ik twijfel een beetje over de kleuren, hij is wel erg paars".
