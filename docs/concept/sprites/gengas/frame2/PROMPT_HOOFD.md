# Gemini-prompt Gengas frame 2: alleen de handeling van het hoofd (16 nov)

Combinatie (Jordi: "geef gemini de handeling en dan kunnen we met het script de manen laten bewegen"):
1. Gemini krijgt het lijf **zonder manen** (`lijf_zonder_manen_8x.png`, door `manen.py` gemaakt) en alleen een handeling.
2. Daarna zet het script de vier manen (`manen_lab.npy`) op nieuwe plekken; die plekken kiest Jordi.

## Prompt

> Edit the attached pixel-art sprite. It is the first frame of a Pokémon battle sprite; make the second animation frame. Keep the pixel-art style, the pixel grid, the exact color palette and the white background.
>
> The body is a round ball of gas. At the lower right its outline is cut off flat and open; complete it there as a round shape with the same dark outline and colors, so the whole body is round.
>
> The creature nods: it lifts its head a little higher, like a small nod. Its round gas body, ears, cloud bands, red eyes and white grin keep exactly the same shape, size and design.
>
> Do not add anything: no hands, no arms, no moons, no objects, no glow, no effects, no text.

- v2 (Jordi: "hij is niet rond"): rechtsonder, waar de voet over de bol lag, is de bol zonder manen afgesneden en open (rijen 51–55); Gemini moet dat afmaken, want het zit nergens in de sprite.
