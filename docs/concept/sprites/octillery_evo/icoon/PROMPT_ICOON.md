# Krassault: icoon via een chibi-model op spritegrootte (18 nov)

Jordi: "Ja, maar doe maar met een andere sprite, gezien de viscacha nu goed loopt" (op het voorstel: Gemini maakt een chibi-versie op 64×64 als model, wij verkleinen exact 2× naar het icoon en schonen op volgens `rug_icoon_studie/EISEN_ICOON.md`). Krassault gekozen als complex ontwerp (EISEN_ICOON "Complexe ontwerpen").

**Herkenningstekens van de front** (`../af/krassault_8x.png`), vooraf vastgelegd: hoge hoekige mantel die schuin naar rechtsboven wijst, met dwarse naden; boos geel oog met zware wenkbrauw; loopmond (kanonloop) voor het gezicht en twee kanonlopen aan zijtentakels; tentakels met gele zuignappen; rupsbanden onderaan; donkerrood met lichtere rode vlakken.

Nieuw gesprek, alleen bijlage `../af/krassault_8x.png`.

## Prompt r1
> This is a Pokémon battle sprite of my creature. Draw a chibi version of it, the way its tiny party menu icon would simplify it, but at the same size as this sprite (64×64 pixels, shown enlarged so every pixel is a square).
>
> Chibi means: the mantle and the face are bigger compared to the rest, the tentacles and treads shorter and stubbier, small details left out, a compact shape that fills the canvas, rounded outlines. Keep it clearly the same creature: same colors, the tall angled mantle pointing up to the right with its seams, the angry yellow eye with the heavy brow, the cannon-barrel mouth in front of the face, the two cannon barrels on the side tentacles, the yellow suckers on the tentacles, and the tank treads at the bottom. Same pose and same viewing angle as my sprite. Do not add anything new.
>
> Gen 3 pixel art, black outline, plain white background, no ground, no shadow, no effects, no text.

## Daarna
Raster terughalen (verwacht 16 px), exact 2× verkleinen naar 32×32 (Krassault-methode `../sprite3/half2.py`), in een icoonpalet zetten, opschonen tot `icoon_check.py` OK geeft; herkenningstekens afvinken.

## Gemini r1 (18 nov)
Gemini maakte geen pixel art maar een gladde chibi-illustratie (beeld kwam niet als bestand binnen). Jordi: "gemini begrijpt het niet vgm". Wel herkenbaar Krassault: hoge mantel met naden, boze gele ogen, kanonmond, twee kanontentakels met gele zuignappen, rupsbanden. Idee: als model gebruiken (zelf verkleinen naar ±22 px en in het icoonpalet zetten), want de vorm is het moeilijke deel en die klopt.
