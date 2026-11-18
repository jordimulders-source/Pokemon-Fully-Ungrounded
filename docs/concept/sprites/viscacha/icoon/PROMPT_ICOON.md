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

## Ronde 1 (18 nov)
`gemini_r1.png` (32-px raster, kaal terug: `r1_kaal_32.png`, 24×21, past in de maat; vergelijking `r1_vs_echte_iconen.png`). Goed: grote kop, lange oren, wangpluk, snorharen, zittend van opzij naar links, getande staartpluk. Zwak: donkerbruine vlekken op de rug (staan niet in de front), staartpluk erg groot, omlijning overal even grijs (Gen 3: boven bijna zwart, onder grijs).
Jordi: "misschien een voorbeeld icoon erbij doen?"

## Prompt r2 (nieuw gesprek; bijlagen: 1 `../af/viscacha_8x.png`, 2 `voorbeeld_zigzagoon_icoon_8x.png`)
> The first image is a Pokémon battle sprite of my creature. The second image is the official Gen 3 (Ruby/Sapphire/Emerald) party menu icon of Zigzagoon, only as an example of the drawing style of these icons: pixel size, outline (near-black at the top, grey at the bottom for depth), few flat colors, chibi proportions.
>
> Draw the party menu icon of MY creature in that style. Big head, short compact body, seen from the side, facing left, sitting or on all fours. Keep my creature recognizable: same colors, the two long upright ears, the yellow cheek tuft, a few whiskers, and the tail with the spiky jagged yellow tuft at the end. No dark patches on the back. Do not add anything new and do not copy Zigzagoon's shape, fur or colors.
>
> The whole creature fits in about 22×22 pixels inside a 32×32 canvas, feet near the bottom. Show it enlarged so every pixel is clearly visible as a square. Plain white background, no ground, no shadow, no effects, no text.

## Ronde 2 (18 nov): afgekeurd
`afgekeurd_r2.png` (met Zigzagoon-voorbeeld): geen chibi meer maar een verkleinde front op een fijner raster, losse staartpunt bovenin. Jordi: "dit lukt gemini dus niet". Les: ook bij iconen werkt een voorbeeldplaatje tegen; r1 (alleen de front, stijl in woorden) is de basis.

## Icoon uit onze front (maker, 18 nov)
`maker/icon.png` (pal5, 28×21). Jordi: "hij is nu erg plat en wat aan de grote kant, het icoon" · "plat van kleur" → meer schaduw/binnenlijnen/detail zoals echte Gen 3-iconen, en kleiner.
Jordi: "zigzagoon heeft een perspectief" · "de viscacha niet" → het icoon moet diepte krijgen zoals Zigzagoon (driekwart, verre delen kleiner/donkerder/hoger, nabije delen voor), zoals de front.
