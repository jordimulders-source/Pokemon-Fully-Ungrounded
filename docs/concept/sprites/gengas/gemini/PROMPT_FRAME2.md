# Gemini-prompt: Gengas, tweede pose (frame 2), 16 nov

Jordi: "Ik wil dat de ledematen/manen daar bewegen, check of hoopa unbound ook zoiets doet."
Hoopa Unbound (expansion, `graphics/pokemon/hoopa/unbound/anim_front.png`, gif in `frame2_studie/hoopa_unbound.gif`): ja, nog sterker: in frame 2 zijn alle zes losse armen weg (in de portalen getrokken), alleen lijf, kop en staart blijven.

Bijlage: **de sprite zelf**, `../af/gengas_8x.png` (bij de viscacha hield Gemini zo exact het pixelraster aan; lijf en staart vielen pixel voor pixel samen met frame 1).

## Prompt (v2, Jordi 16 nov: "het zou tof zijn als gengas zijn hoofd ietsje hoger gaat, een soort knikbeweging, naast wat de manen doen")

> Edit the attached pixel-art sprite. This is the first frame of a Pokémon battle sprite; make the second animation frame. Keep the pixel-art style, the pixel grid and the exact color palette. Do not redraw anything; only move parts.
>
> 1. The round gas body with its face (its head) moves a little higher, a few pixels up, like a small nod. Its shape, cloud bands, gas ears, red eyes and white grin stay exactly the same, pixel for pixel; only its position changes.
> 2. The four floating grey moons, which are its detached hands and feet, each move noticeably to a new position along their orbit around the body, as if the hands and feet are swinging. Keep each moon's exact shape, size, colors and craters.
>
> Plain white background, no glow, no effects, no text.

## Ronde 1 (Jordi, 16 nov): mislukt, "hij doet niks met de instructies, dus die moeten specifieker"
`frame2_ronde1.png` / `.gif`: de bol is platgedrukt (bovenkant bleef staan, onderkant 4 px omhoog) in plaats van verplaatst; de manen staan bijna op dezelfde plek (alleen de voet iets omhoog).

## Prompt v3 (specifiek, posities op de klok en in pixels)

> Edit the attached image. It is a 64×64 pixel-art sprite shown at 16× scale: every sprite pixel is a 16×16 block. Keep that exact grid, the exact colors and the white background. Do not redraw, reshape, squash or stretch anything: you only cut parts out and paste them somewhere else, unchanged. Everything that is not mentioned stays exactly where it is.
>
> The creature has 5 separate parts: one big round gas body with ears, eyes and grin, and 4 small grey rocky moons floating around it.
>
> 1. BODY: move the whole round body, including ears, eyes and grin, straight UP by 3 sprite pixels (48 image pixels). Its height and width stay exactly the same; the bottom edge moves up by the same amount as the top. The space that appears under the body becomes white.
> 2. TOP MOON (now above the head, at 12 o'clock): move it 6 sprite pixels to the LEFT, so it floats above the left ear.
> 3. RIGHT MOON (now right of the head, at 3 o'clock): move it 5 sprite pixels UP, so it floats next to the tip of the right ear.
> 4. LEFT MOON (now at the left of the grin, at 8 o'clock): move it 6 sprite pixels UP, so it floats next to the left eye.
> 5. BOTTOM MOON (now under the right side, at 5 o'clock): move it 6 sprite pixels to the LEFT and 2 sprite pixels UP, so it floats more under the middle of the body.
>
> Each moon keeps its exact shape, size, colors and craters. The moons stay in front of the body where they overlap. No glow, no effects, no text.

De nieuwe plekken van de manen zijn een voorstel van Claude; pas getallen of richtingen aan als je een andere beweging wilt.

## Daarna
- Terugzetten naar 64×64 zoals bij de viscacha (middelste pixel per 16×16-vak), kleuren op het palet van `af/gengas.png`; alleen de manen overnemen, de rest blijft frame 1.
- Tekent Gemini de manen anders (andere vorm, vingers): opnieuw genereren, niet zelf repareren (SPEC: "jij kan geen handen en voeten tekenen").

## Ronde 2 (prompt v3): mislukt (`frame2_ronde2_v3.png`)
Manen niet verplaatst maar **bijgetekend** (zes in plaats van vier, één over het linkeroog, nieuwe ronde stenen in plaats van de hand-/voetvormen); bol weer platgedrukt in plaats van omhoog geschoven.
Waarom het bij de viscacha wel lukte: zie `frame2_studie/STUDIE.md` §9.
