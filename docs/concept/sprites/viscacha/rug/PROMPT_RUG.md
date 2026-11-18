# Gemini-prompt: viscacha, rugsprite (18 nov)

Werkwijze: `../../rug_icoon_studie/STUDIE.md` §5A. Nieuw gesprek in Gemini, twee bijlagen:
1. `../af/viscacha_8x.png` (onze goedgekeurde front)
2. `rugbuur_raticate_8x.png` (Raticate's echte Gen 3-rugsprite, alleen als voorbeeld van het standpunt)

## Prompt
> The first image is a Pokémon battle sprite of my creature (front view). The second image is the official Gen 3 (Ruby/Sapphire/Emerald) back sprite of Raticate, only as an example of how back sprites are drawn.
>
> Draw the back sprite of MY creature (first image) in exactly the same way as the Raticate example: seen from behind and slightly above on the left, the body facing away from the viewer toward the upper right, the head turned in profile over its shoulder so that one eye, the cheek tuft and the whiskers are visible at the right side. Zoomed in like the example: the body is larger than in the front sprite and the bottom is cut off by a straight horizontal line, with nothing below it.
>
> Keep my creature exactly as it is: same species, same colors, same ears, eye, whiskers, yellow cheek tuft, fur colors and yellow jagged tail tuft, same art style and outline as the first image. Show its back and tail; the belly is not visible from behind. Do not add anything new, do not redesign it, and do not copy Raticate's shape or colors.
>
> Gen 3 pixel art, plain white background, no ground, no shadow, no effects, no text.

## Daarna
- Jordi kiest (of vraagt een nieuwe poging; bij afwijkingen: nieuw gesprek, niet laten repareren).
- Overnemen naar 64×64 (rug ±1,16× de frontbreedte, ongeveer even hoog, vlak afgesneden), in het palet van `../af/normal.pal`, maker schoont op; keurder; Jordi.

## Ronde 1 (18 nov) → bijstuurprompt r2
Jordi over r1 (`gemini_r1.png`): "Staart en kop/oren ben ik het idd mee eens, maar wederom positief verrast hoe goed die in 1 poging al is" · "misschien 1 prompt om licht te verbeteren en kijken wat die doet?"
Fouten in r1: staart is een lange lus die terug omlaag krult en het geel is een gladde band (front: kortere staart omhoog met getande gele pluk); kop te klein, oren te kort en te ver uit elkaar, linkeroor lijkt uit de nek te groeien.

Prompt r2 (hetzelfde gesprek, één bijsturing):
> Very good, keep this exact image: same viewpoint, body, back, cheek tuft, whiskers, colors and the straight cut at the bottom. Fix only two things, using my first image (the front sprite) as the reference:
> 1. The tail: make it like in my front sprite. A shorter tail that rises upward from the rump in one curve and ends in a spiky, jagged yellow tuft like a small flame. The tail does not loop back down, and the yellow is only the jagged tuft at the end, not a band along the tail.
> 2. The head: make the head bigger, the same size as in my front sprite, with the same long upright ears close together on top of the head. Both ears grow from the top of the head, not from the neck; the nearer ear (left) partly overlaps the far one.
> Change nothing else.
