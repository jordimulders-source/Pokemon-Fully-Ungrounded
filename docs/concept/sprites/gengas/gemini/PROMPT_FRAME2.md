# Gemini-prompt: Gengas, tweede pose (frame 2), 16 nov

Jordi: "Ik wil dat de ledematen/manen daar bewegen, check of hoopa unbound ook zoiets doet."
Hoopa Unbound (expansion, `graphics/pokemon/hoopa/unbound/anim_front.png`, gif in `frame2_studie/hoopa_unbound.gif`): ja, nog sterker: in frame 2 zijn alle zes losse armen weg (in de portalen getrokken), alleen lijf, kop en staart blijven.

Bijlage: **de sprite zelf**, `../af/gengas_8x.png` (bij de viscacha hield Gemini zo exact het pixelraster aan; lijf en staart vielen pixel voor pixel samen met frame 1).

## Prompt

> Edit the attached pixel-art sprite. This is the first frame of a Pokémon battle sprite; make the second animation frame. Keep the pixel-art style, the pixel grid and the exact color palette. The round gas body, the cloud bands, the gas ears, the red eyes and the white grin stay exactly the same, pixel for pixel, in the same place.
>
> Change only the four floating grey moons, which are its detached hands and feet: each moon moves noticeably to a new position along its orbit around the body, as if the hands and feet are swinging. Keep each moon's exact shape, size, colors and craters; do not redraw them.
>
> Plain white background, no glow, no effects, no text.

## Daarna
- Terugzetten naar 64×64 zoals bij de viscacha (middelste pixel per 16×16-vak), kleuren op het palet van `af/gengas.png`; alleen de manen overnemen, de rest blijft frame 1.
- Tekent Gemini de manen anders (andere vorm, vingers): opnieuw genereren, niet zelf repareren (SPEC: "jij kan geen handen en voeten tekenen").
