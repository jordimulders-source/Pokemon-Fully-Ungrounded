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
