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
