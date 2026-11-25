# Glitch-lijn fase 1 "glitch": Gemini-prompts
Besluiten en citaten: `docs/concept/IDEEEN.md` → "Glitch → bug → virus". Lessen van fase 2 (r1–r10): `fase2_bug/gemini/PROMPTS.md`.
Vast (Jordi): Electric; puur digitaal wezen, een glitch die sentient wordt; al sentient, vaag gezicht; "een glitch met weinig vorm, er is wel het een en ander in af te lezen, maar erg missingno achtig"; glitcht als hij beweegt (animatie, later); corruptie doen wij zelf, Gemini maakt de intacte basis; geen comic-achtige blije menselijke ogen ("dat maakt het niet digitaal genoeg").
Eigen invulling Claude (schrappen bij twijfel): ogen als twee felle vierkante blokjes, geen mond of een klein kartellijntje, onregelmatige stapel blokken (geen L-vorm, afstand tot MissingNo), donker + één felle kleur.

## r1 (nieuw gesprek, zonder bijlage): basis voor fase 1
```
Design an original Pokemon as an official Gen 3 front sprite (Pokemon Ruby/Sapphire/Emerald), 64x64. Type: Electric. It is the first stage of a line: a purely digital creature, a glitch in the game's graphics that has just become sentient. Drawn without glitch effects (the corruption is added later by hand).

BUILD (most important): it has almost no shape. It is an irregular, lopsided stack of flat rectangular blocks, like a chunk of broken graphics data that happens to stand upright, NOT an L-shape and NOT a neat box. Only a few things in it can be read as a creature: something like a head at the top, and two short stubs that could be arms.

FACE: vague and not human. Two eyes that are just small bright square blocks, like single pixels of light, no pupils, no eyelids, no expression lines. No mouth, or only a tiny jagged line. It does NOT look happy or cute.

COLORS: a dark main color with 2 to 3 flat shades, plus one bright color for the eyes.

STYLE: real pixel art, max 16 colors, hard straight edges, dark outline, no smooth curves, no gradients. White background, no ground, no shadow, no effects, no glow.

AVOID: a cartoon or comic face, human eyes, big round eyes, a smile, a cute mascot, a blob, a ghost, a robot, a box or toaster, insects, screens, text or symbols, MissingNo's exact shape, Porygon, Unown.
```

## Ronde 1 (25 nov)
- `r1/r1.png`. Jordi: "te blokkerig, te kleine mond, te vierkante ogen".

## r2 (nieuw gesprek, zonder bijlage): prompt r1, alleen bouw, ogen en mond aangepast
Eigen invulling Claude: "ragged, jagged mass" in plaats van rechthoeken; ogen onregelmatig en smal; mond als grote kartellijn over het gezicht; benen/golem in AVOID (r1 kreeg benen).
```
Design an original Pokemon as an official Gen 3 front sprite (Pokemon Ruby/Sapphire/Emerald), 64x64. Type: Electric. It is the first stage of a line: a purely digital creature, a glitch in the game's graphics that has just become sentient. Drawn without glitch effects (the corruption is added later by hand).

BUILD (most important): it has almost no shape. It is an irregular, lopsided mass of broken graphics data that happens to stand upright: ragged, jagged, uneven edges, NOT built from neat rectangles or boxes, NOT an L-shape. Only a few things in it can be read as a creature: something like a head at the top, and two short stubs that could be arms. No legs.

FACE: vague and not human. Two small bright eyes with irregular, uneven shapes (narrow, slanted or ragged), NOT square and NOT round, no pupils, no eyelids. A big jagged mouth: a wide zig-zag crack that runs across most of the face. It does NOT look happy or cute.

COLORS: a dark main color with 2 to 3 flat shades, plus one bright color for the eyes and mouth.

STYLE: real pixel art, max 16 colors, dark outline, no smooth curves, no gradients. White background, no ground, no shadow, no effects, no glow.

AVOID: square eyes, round eyes, human eyes, a cartoon or comic face, a smile, a cute mascot, a blob, a ghost, a robot or golem figure, legs, neat rectangular blocks, a box or toaster, insects, screens, text or symbols, MissingNo's exact shape, Porygon, Unown.
```

## Ronde 2 (25 nov)
- `r2/r2.png`. Jordi: "nu is het een soort crumbled afvalpoppetje".
- Analyse Claude: r1 en r2 zijn allebei een fysiek voorwerp (3D-blokken, brokkelsteen); digitaal = plat grafisch beeld van pixels, geen materiaal.

## r3 (nieuw gesprek, zonder bijlage): prompt r2, alleen de bouw aangepast (plat, grafisch, geen materiaal)
```
Design an original Pokemon as an official Gen 3 front sprite (Pokemon Ruby/Sapphire/Emerald), 64x64. Type: Electric. It is the first stage of a line: a purely digital creature, a glitch in the game's graphics that has just become sentient. Drawn without glitch effects (the corruption is added later by hand).

BUILD (most important): it is NOT a physical object and NOT made of any material: no stone, rubble, trash, clay, cracks or texture. It looks like a flat piece of video game graphics, a shape made of pixels and flat color areas, like a sprite of something that should not exist. It has almost no shape: an irregular, lopsided pixel shape that happens to stand upright, with stepped pixel edges, not neat boxes and not crumbly. Only a few things in it can be read as a creature: something like a head at the top, and two short stubs that could be arms. No legs.

FACE: vague and not human. Two small bright eyes with irregular, uneven shapes (narrow, slanted or ragged), NOT square and NOT round, no pupils, no eyelids. A big jagged mouth: a wide zig-zag crack that runs across most of the face. It does NOT look happy or cute.

COLORS: a dark main color in large flat areas with very little shading, plus one bright color for the eyes and mouth.

STYLE: real pixel art, max 16 colors, dark outline, no smooth curves, no gradients. White background, no ground, no shadow, no effects, no glow.

AVOID: stone, rocks, rubble, trash, crumbling, cracks, texture, 3D blocks, square eyes, round eyes, human eyes, a cartoon or comic face, a cute mascot, a blob, a ghost, a robot or golem figure, legs, a box or toaster, insects, screens, text or symbols, MissingNo's exact shape, Porygon, Unown.
```
- r3 hierboven niet gebruikt: AVOID verbood schermen; Jordi: "hij moet oorspronkelijk in het computerscherm zitten", koos A (gemaakt van schermbeeld, geen scherm te zien).

## r4 (nieuw gesprek, zonder bijlage): gemaakt van schermbeeld
Eigen invulling Claude (schrappen bij twijfel): scanlijnen door het lijf, rood/groen/blauwe beeldpuntjes aan de randen, lichtgevende kleuren op donker.
```
Design an original Pokemon as an official Gen 3 front sprite (Pokemon Ruby/Sapphire/Emerald), 64x64. Type: Electric. It is the first stage of a line: a purely digital creature that originally lived inside a computer screen. It is a glitch in the image on the screen that has become sentient and has come loose from it. Drawn without glitch corruption (that is added later by hand).

WHAT IT IS MADE OF (most important): it is made of the image on a screen, not of any material. Its body is light and pixels: it looks like a piece of a computer screen's picture that walks around on its own. Thin horizontal scanlines run through the whole body, the colors are glowing screen colors on a dark base, and at the edges you see tiny red, green and blue screen dots. The screen itself, the monitor or a frame, is NOT visible: only the picture.

BUILD: it has almost no shape: an irregular, lopsided shape of screen image that happens to stand upright. Only a few things can be read as a creature: something like a head at the top, and two short stubs that could be arms. No legs.

FACE: vague and not human. Two small bright eyes with irregular, uneven shapes (narrow, slanted or ragged), NOT square and NOT round, no pupils, no eyelids. A big jagged mouth: a wide zig-zag crack across most of the face. It does NOT look happy or cute.

STYLE: real pixel art, max 16 colors, no gradients. White background, no ground, no shadow, no glow halo around it.

AVOID: a monitor, a TV or a frame around it, a physical object, stone, rubble, trash, clay, 3D blocks, square eyes, round eyes, human eyes, a cartoon or comic face, a cute mascot, a blob, a ghost, a robot or golem figure, legs, insects, text or symbols, MissingNo's exact shape, Porygon, Unown, Rotom.
```

## Ronde 4 (25 nov)
- `r4/r4.png`. Jordi: "wat is dit? Dit is toch totaal niet wat we besproken hebben". Claude: prompt vroeg een vormloze "shape of screen image" en hield MissingNo in de AVOID; afgesproken was "bijna missingno achtig".

## r5 (nieuw gesprek, zonder bijlage): from scratch (Jordi: "maak nu eens een goede prompt, from scratch")
Alleen Jordi's besluiten; geen eigen lichaamsdelen (geen kop/armstompjes/benen-regels meer), geen concept in de AVOID. Eigen invulling: kleurbeperking "like old game graphics".
```
Design an original Pokemon: an official Gen 3 front sprite (Pokemon Ruby/Sapphire/Emerald), 64x64 pixels, max 16 colors, white background.

WHAT IT IS: Type Electric. The first stage of a three-stage line (glitch, then bug, then virus). It is a purely digital creature: a glitch that lived inside a computer screen and has become sentient. It is made of what is shown on a screen: broken, corrupted video game graphics data. It is not a physical object, not made of any material, and no monitor or screen frame is visible.

THE LOOK (most important): it is the same kind of thing as MissingNo, the famous glitch Pokemon of the first games: a heap of scrambled pixel data with garbled patterns inside, where you can hardly tell what it is. But it is clearly its own design: NOT a rectangle, NOT a column, NOT an L-shape and NOT built from square tiles. It has an irregular, unpredictable outline. It has very little shape; only a few things can just be made out in it, above all a vague face.

FACE: vague and digital, part of the scrambled data, not a drawn cartoon face. The eyes are NOT human, NOT happy, NOT round and NOT square. A clearly visible mouth, not tiny.

COLORS: a limited palette like old game graphics.

AVOID: a cartoon, comic or mascot face, human or happy eyes, a ghost, a blob, a slime, rubble, stone, trash, a robot, a golem, a box, a toaster, a neat or symmetric shape, a rectangle, square tiles, a copy of MissingNo, Porygon, Unown, Rotom.
```
