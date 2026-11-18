# Gemini-prompt: viscacha, party-icoon (18 nov)

Jordi: "laten we de viscacha blijven gebruiken als voorbeeld, de versie in het pokemon menu, zullen we die met gemini testen? Het icoontje". Werkwijze: `../../rug_icoon_studie/STUDIE.md` §3 (icoon = mini-ontwerp) en §5B; Jordi: pose mag afwijken, "volg vooral game freak daarin".
Nieuw gesprek, alleen bijlage `../af/viscacha_8x.png` (geen voorbeeld-icoon: bij de rug zat Raticate in de weg).

## Prompt r1
> This is a Pokémon battle sprite of my creature. Draw its party menu icon, the tiny 32×32 pixel icon that Pokémon Ruby/Sapphire/Emerald show in the party screen and the PC boxes.
>
> How Game Freak makes these icons: not a shrunken copy of the battle sprite, but a simple chibi version. The head is big (the largest part), the body short and compact, the pose simple, often seen from the side, facing left, standing on all fours or sitting. Only the most recognizable features stay, drawn big and clear; small details are left out. Thick dark grey outline, about 8 colors, flat colors with one shade, no dithering.
>
> Keep my creature recognizable: same colors, the two long upright ears, the yellow cheek tuft, a few whiskers, and the tail with the spiky jagged yellow tuft at the end. Do not add anything new.
>
> The whole creature fits in about 22×22 pixels inside a 32×32 canvas, feet near the bottom. Show it enlarged so every pixel is clearly visible as a square. Plain white background, no ground, no shadow, no effects, no text.

## Daarna
Terug naar 32×32 (natief raster), in het best passende icoonpalet (`../../rug_icoon_studie/icon_onderlaag.py` geeft de foutscores; voorlopig 5 of 2), omlijning index 15, frame 2 per script (bovenkant 1 px lager) + één klein verschil.
