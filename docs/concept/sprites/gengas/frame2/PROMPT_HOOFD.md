# Gemini-prompt Gengas frame 2: alleen de handeling van het hoofd (16 nov)

Combinatie (Jordi: "geef gemini de handeling en dan kunnen we met het script de manen laten bewegen"):
1. Gemini krijgt het lijf **zonder manen** (`../sprite_v15/lijf_zonder_manen_v15_8x.png`; oud: `lijf_zonder_manen_8x.png`, door `manen.py` gemaakt) en alleen een handeling.
2. Daarna zet het script de vier manen (`manen_lab.npy`) op nieuwe plekken; die plekken kiest Jordi.

## Prompt

> Edit the attached pixel-art sprite. It is the first frame of a Pokémon battle sprite; make the second animation frame. Keep the pixel-art style, the pixel grid, the exact color palette and the white background.
>
> The creature nods: it lifts its head a little higher, like a small nod. Its round gas body, ears, cloud bands, red eyes and white grin keep exactly the same shape, size and design.
>
> Do not add anything: no hands, no arms, no moons, no objects, no glow, no effects, no text.

- v2 (Jordi: "hij is niet rond"): rechtsonder, waar de voet over de bol lag, is de bol zonder manen afgesneden en open (rijen 51–55); Gemini moet dat afmaken, want het zit nergens in de sprite.
- v3 (Jordi: "linksonder de mond is ook een puntje"): ook dat punt rond laten maken.
- v4 (16 nov): bijlage is nu `../sprite_v15/lijf_zonder_manen_v15_8x.png` (bol al rond gemaakt door maker-agents: links v14, rechtsonder + onder de gasarm v15); de alinea over rond maken is daarom weg.

## Ronde 1 knik: Gemini veranderde niets (`gemini_knik_r1.png`; op 11× i.p.v. 16×). Script-frame 2 (`frame2.py`) door Jordi afgewezen: "nee" / "nieuwe prompt, gemini heeft nog niks veranderd".

## Prompt v5 (zichtbaar maken)

> Edit the attached pixel-art sprite to make the second frame of its battle animation. The result must look clearly different from the attached image.
>
> The creature nods upward: the whole round body floats higher in the picture, closer to the top edge, leaving more empty white space below it. At the same time it tilts its head slightly backward: the face (red eyes and white grin) moves a little up on the ball, so it looks a bit more upward, and the two ears lean a little further back.
>
> Keep exactly the same size, the same pixel scale (every pixel stays a 16×16 block), the same pixel-art style, the same colors, cloud bands, eyes and grin design. Plain white background. Do not add anything: no hands, no moons, no objects, no glow, no effects, no text.

## Prompt v6 (Jordi: "nee, nieuwe prompt"): vel met twee frames

> Make a pixel-art animation sprite sheet with two frames side by side, using the attached sprite.
>
> LEFT frame: the attached sprite, copied exactly.
>
> RIGHT frame: the same creature in the next moment of a nodding motion. The round body has bobbed upward, so it sits clearly higher than in the left frame (its bottom edge is well above the bottom edge of the left one), and its head is tilted back a little: the eyes and the grin sit a bit higher on the ball and look slightly upward, the ears lean back.
>
> Both frames: identical size, identical pixel scale, same pixel-art style, same colors, cloud bands, eyes and grin. Plain white background, frames aligned on the same baseline. No hands, no moons, no objects, no glow, no text.

## v6 ronde 2 (`gemini_knik_v6b.png`): Jordi "deze is ook niet goed he, hele andere vorm" (smaller, oren en gasarm anders). "kan je niet nog accurater prompten?"

## Prompt v7 (draaien i.p.v. hertekenen, kenmerken opgesomd)

> Make a pixel-art sprite sheet with two frames side by side, both at exactly the same size and pixel scale as the attached sprite.
>
> LEFT frame: the attached sprite, copied exactly, unchanged.
>
> RIGHT frame: the LEFT frame, rotated backward (counter-clockwise) by about 10 degrees around its center and shifted a little upward, like a head nodding up. It is the same drawing, only rotated and moved: do not redraw it, do not change its shape, size, width or proportions.
>
> These must be identical in both frames, only rotated with the body:
> - the round ball shape, as wide as in the left frame
> - the left ear, ending in a thin wispy tip that points up and to the left
> - the right ear, pointing up and to the right
> - the dark gas trail that flows out from behind the right ear to the right
> - the light pink highlight on the upper left of the ball
> - the darker cloud bands that run across the ball
> - the angry, slanted red eyes
> - the wide white grin with its row of teeth
>
> Plain white background. No hands, no moons, no other objects, no glow, no text.

Terugval: knik via de engine (`frontAnimId`, bijv. `ANIM_ROTATE_UP_SLAM_DOWN`, `ANIM_V_SLIDE`, `ANIM_TIP_MOVE_FORWARD`) en frame 2 alleen de manen.
