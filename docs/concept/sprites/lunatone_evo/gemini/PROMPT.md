# Gemini-prompt: Lunatone-evolutie "bloedmaan", startprompt v1 (22 nov)

Regels: `docs/lessen/GEMINI.md`. Tegenhanger: Solrock-evolutie "corona" (`docs/concept/sprites/solrock_evo/`, branch fervent-hamilton; model = Gemini v5).
Bijlage: `bijlage_lunatone_gen3.png` (Lunatones eigen Gen 3-frontsprite, 8× vergroot).

## Jordi (letterlijk)
- 17 nov: "lunatone zou wel moeten lukken"; "Ik zat ook te denken om Lunatone en Solrock misschien een gezamenlijke eclipse evolutie te geven, of misschien een Accelgor/Escavalier achtige evolutie"
- 22 nov: "lunatone evolutie, kijk bij fervent hamilton voor wat je kan prompten voor gemini"
- Overgenomen van Solrock (22 nov, wat daar werkte): "dus de stenen zijn echt los en zweven eromheen" · "qua kleur echt eclipse creëren, dan lijkt die krachtiger" · "Punten afbreken ook wel een goed idee, ouder en gehavender ook"

## Voorstel Claude (nog niet besloten)
- Spiegel van Solrock: Lunatone evolueert met een Solrock in het team; bij een totale maansverduistering wordt de maan koperrood (bloedmaan), dus geen zwarte kern maar diep rood gesteente.
- Lessen uit de Solrock-rondes al verwerkt: geen lava/kristallen (Jordi vroeg of Gemini die zelf verzon), geen embleem/symmetrie, 3/4 gekanteld, eigen gezicht exact uit de bijlage, geen diagonale ring (werd een Saturnusring).

```
Design the evolution of the Pokémon LUNATONE and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE ATTACHED SPRITE IS LUNATONE (the pre-evolution). Copy its single red eye exactly, and keep its crescent-moon shape and its craters recognizable.

CONCEPT
- Lunatone is a meteorite of stone in the shape of a crescent moon. Its evolution is that meteorite coming apart: pieces of stone are now truly loose and float around the crescent.
- It evolves when the sun (Solrock) is with it: a total lunar eclipse made of stone, the "blood moon". Older, battered and more powerful than Lunatone.

DESIGN
- Body: Lunatone's crescent, now cracked and scarred, with chips missing from its edges and its two points broken off.
- Eclipse colors: the stone has turned a deep coppery blood red, darkest on the inner curve of the crescent and lighter red-orange on the outer edge, like the moon during a total lunar eclipse.
- Floating stones: chunks of the crescent (including the broken-off points and pieces with craters) have broken loose and float around the body, none of them touching it. Between them float smaller fragments.
- The eye: Lunatone's own red eye with dark surround, in the same place on the crescent.

POSE
- Three-quarter view facing left, tilted like Lunatone's own sprite, floating. Not straight-on, not symmetrical.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO soft glow or halo behind the creature, no floor, shadow, sparkles or effects. One single creature, no extra views.

AVOID
- Not an emblem, badge, logo or symbol: no flat, symmetrical, straight-on layout.
- Not a full round moon, not a sun. No lava, no gems or crystals, no fire.
- No arms, legs, wings, mouth or human features. No glossy 3D render, no plush or mascot look.
```

## Reactie op v1 (`r1/gemini_v1.png`), Jordi (22 nov, letterlijk)
- "lijkt wel teveel op de echte lunatone he, hoe kunnen we het anders maken dan een pallette swap"
- Claude stelde voor: A spiegel van Solrock-corona (rode volle maan met de sikkel als gezichtsplaat), B sikkel in stukken als baan om een kern met het oog, C volle maan in aardschaduw met een dun licht stukje sikkel. Wacht op Jordi.
- Jordi (22 nov): "misschien een volle maan? is een lunar eclipse/blood moon altijd vol?" (ja: een maansverduistering kan alleen bij volle maan)
- Jordi (22 nov): "A"

---

# Prompt v2 (22 nov): NIEUW gesprek, startprompt, bijlage alleen `bijlage_lunatone_gen3.png` (geen v1)

Keuze A: rode volle maan met Lunatones sikkel erop als gezichtsplaat met het oog (spiegel van Solrock-corona v5), losse brokken eromheen.

```
Design the evolution of the Pokémon LUNATONE and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE ATTACHED SPRITE IS LUNATONE (the pre-evolution). Copy its crescent with the single red eye exactly: that crescent becomes the face plate of the evolution.

CONCEPT
- Lunatone is a meteorite of stone in the shape of a crescent moon. Its evolution has grown into a FULL MOON during a total lunar eclipse: the blood moon. Lunatone's crescent is still there, but now as a plate on the front of a big round moon.
- It evolves when the sun (Solrock) is with it. The meteorite is also coming apart: pieces of stone are truly loose and float around it. Older, battered and more powerful than Lunatone.

DESIGN
- Core: a big round full moon of stone in deep coppery blood red, darker on the shadow side, covered in craters and cracks, with chips missing from its edge.
- Face plate: Lunatone's own crescent, in its own pale yellow stone color, set on the front of the red moon like a plate, with the red eye in the same place as on Lunatone. The crescent is old and battered: a crack runs through it and one of its points is broken off.
- Floating stones: chunks of the moon have broken loose and float around the core, none of them touching it. Between them float smaller fragments.

POSE
- Three-quarter view facing left, tilted, floating. Not straight-on, not symmetrical.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO soft glow or halo behind the creature, no floor, shadow, sparkles or effects. One single creature, no extra views.

AVOID
- Not the same crescent silhouette as Lunatone: the overall shape is a round full moon.
- Not an emblem, badge, logo or symbol: no flat, symmetrical, straight-on layout.
- Not a sun. No lava, no gems or crystals, no fire.
- No arms, legs, wings, mouth or human features. No glossy 3D render, no plush or mascot look.
```

---

# Prompt v3 (22 nov): NIEUW gesprek, startprompt, bijlage alleen `bijlage_lunatone_gen3.png`

## Jordi over v2 (`r2/gemini_v2.png`, letterlijk)
- "teveel lunatone erop geplakt, dat hele halve maan idee moet weg, hij is nu de brokkelende blood moon. Hij behoudt alleen oog en neus"

```
Design the evolution of the Pokémon LUNATONE and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE ATTACHED SPRITE IS LUNATONE (the pre-evolution). From it, keep ONLY two things: its single red eye with the dark surround, and its pointed nose (the stone point sticking out in the middle of the crescent). Nothing else of Lunatone: no crescent shape, no crescent plate, no pale yellow.

CONCEPT
- The evolution is a crumbling blood moon: a full moon of stone during a total lunar eclipse, falling apart.
- It evolves when the sun (Solrock) is with it. Older, battered and more powerful than Lunatone.

DESIGN
- Body: one big round full moon of stone in deep coppery blood red, darker on the shadow side, covered in craters and deep cracks. It is crumbling: chunks are missing from its edge.
- Face: Lunatone's red eye and pointed nose, set directly in the red moon, made of the same red stone.
- Crumbling pieces: broken chunks of the moon float loose around it, none of them touching it, with smaller fragments between them.

POSE
- Three-quarter view facing left, tilted, floating. Not straight-on, not symmetrical.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO soft glow or halo behind the creature, no floor, shadow, sparkles or effects. One single creature, no extra views.

AVOID
- No crescent moon anywhere: not as the body, not as a plate, not as a cut-out shape.
- Not an emblem, badge, logo or symbol: no flat, symmetrical, straight-on layout.
- Not a sun. No lava, no gems or crystals, no fire.
- No arms, legs, wings, mouth or human features. No glossy 3D render, no plush or mascot look.
```

---

# Prompt v4 (22 nov): NIEUW gesprek, GEEN bijlage

## Jordi over v3 (`r3/gemini_v3.png`, letterlijk)
- "teveel halve maan nog"

## Analyse Claude
De Lunatone-bijlage trekt Gemini steeds naar de sikkel; daarom zonder bijlage (zoals bij de vuurduivel), oog en neus in woorden.

```
Design a new Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art). It is the evolution of Lunatone.

CONCEPT
- A crumbling blood moon: a FULL moon of stone during a total lunar eclipse, falling apart. Older, battered and powerful.

DESIGN
- Body: one big, completely round full moon of stone, a full disc, in deep coppery blood red, darker on the shadow side, covered in craters and deep cracks. It is crumbling: a few small chunks are missing from its edge, but the overall outline stays a full circle.
- Face, exactly like Lunatone's face: one single round red eye with a thick black ring around it, and next to it, on the left, a short pointed stone nose that sticks straight out sideways from the surface of the moon, like a small horizontal spike. Same red stone as the moon. No other facial features.
- Crumbling pieces: broken chunks of the moon float loose around it, none of them touching it, with smaller fragments between them.

POSE
- Three-quarter view facing left, the sphere slightly tilted, floating.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO soft glow or halo behind the creature, no floor, shadow, sparkles or effects. One single creature, no extra views.

AVOID
- No crescent moon, no half moon, no C-shape, no Pac-Man shape: nothing is cut out of the disc.
- Not an emblem, badge, logo or symbol. Not a sun. No lava, no gems or crystals, no fire.
- No arms, legs, wings, mouth or human features. No glossy 3D render, no plush or mascot look.
```

---

# Prompt v5 (22 nov): zelfde gesprek als v4, bijsturen (reactie op `r4/gemini_v4.png`)

## Jordi (letterlijk)
- "de neus komt dus uit de bolling ook, of misschien uit een stuk afgebrokkeld, maar hij moet niet zo smooth halve maan zijn"

## Analyse Claude
Goed: volle rode bol, oog, losse brokken. Mis: links nog steeds een gladde C-vormige uitsparing waar de neus in zit. Eén wijziging.

```
Better. Keep the red moon, the eye, the cracks, the colors and the floating chunks exactly as they are. Change only one thing:

The left side. Remove the smooth curved hollow around the nose: there is no half-moon shape cut out of the disc. The left edge of the moon bulges outward, round like the rest of the sphere, and the nose sticks straight out of that round bulging surface. Where the nose comes out, the stone may be rough and crumbled, with a few jagged broken chips, but never a smooth curve.

Same Gen 3 sprite style, plain white background.
```

---

# Prompt v6 (22 nov): NIEUW gesprek, GEEN bijlage

## Jordi over v5 (`r5/gemini_v5.png`, letterlijk)
- "niet goed" (vrijwel gelijk aan v4, uitsparing bleef)

## Analyse Claude
Het woord "Lunatone" (en "crescent" in AVOID) roept de sikkel op. Daarom nergens Lunatone of halve maan noemen; de vorm als bol/bal beschrijven, oog en neus alleen in woorden.

```
Design a new Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- A crumbling blood moon: a living ball of moon rock during a total lunar eclipse, falling apart. Old, battered and powerful.

DESIGN
- Body: a perfect round ball of stone, like a planet seen from space, in deep coppery blood red, darker on the shadow side, covered in craters and deep cracks. Its outline is a full, unbroken circle all the way around.
- Crumbling: a few chunks have broken off the ball and float loose around it, none of them touching it, with smaller fragments between them.
- Face: one single round red eye with a thick black ring around it, set in the surface of the ball, slightly right of center. Left of the eye, a short pointed stone nose grows straight out of the curved surface of the ball, like a small horizontal spike pointing left. Around the base of the nose the stone is rough, cracked and crumbled. No other facial features.

POSE
- Three-quarter view facing left, floating.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO soft glow or halo behind the creature, no floor, shadow, sparkles or effects. One single creature, no extra views.

AVOID
- No notch, hollow, cut-out or open mouth in the ball: the ball is solid and round everywhere, also around the nose.
- Not an emblem, badge, logo or symbol. Not a sun. No lava, no gems or crystals, no fire.
- No arms, legs, wings, mouth or human features. No glossy 3D render, no plush or mascot look.
```

---

# Prompt v7 (22 nov): NIEUW gesprek, GEEN bijlage

## Jordi over v6 (plaatje niet gestuurd, letterlijk)
- "het brokkelige rondom de neus wel, maar blijft de halve maan vorm"

## Analyse Claude
Zolang de neus aan de linkerrand zit, snijdt Gemini er een C-vorm omheen. Daarom oog en neus midden op de bol, neus schuin naar de kijker/links, zodat de omtrek achter de neus gewoon doorloopt. Plan B: de uitsparing zelf dichtmaken in de sprite (zoals bij Solrock "dan kunnen we zelf in de sprite spelen"), alleen als Jordi dat wil.

```
Design a new Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- A crumbling blood moon: a living ball of moon rock during a total lunar eclipse, falling apart. Old, battered and powerful.

DESIGN
- Body: a perfect round ball of stone, like a planet seen from space, in deep coppery blood red, darker on the shadow side, covered in craters and deep cracks. Its outline is a full, unbroken circle all the way around.
- Crumbling: a few chunks have broken off the ball and float loose around it, none of them touching it, with smaller fragments between them.
- Face, in the MIDDLE of the ball, well inside its outline: one single round red eye with a thick black ring around it. Just left of the eye, a short pointed stone nose grows out of the front of the ball and points toward the viewer and slightly left, like a small spike. The round outline of the ball continues unbroken behind the nose. Around the base of the nose the stone is rough, cracked and crumbled. No other facial features.

POSE
- Three-quarter view facing left, floating.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO soft glow or halo behind the creature, no floor, shadow, sparkles or effects. One single creature, no extra views.

AVOID
- No notch, hollow, cut-out, bite or open mouth in the ball: the ball is solid and round everywhere, also around the nose. Nothing touches the edge of the ball.
- Not an emblem, badge, logo or symbol. Not a sun. No lava, no gems or crystals, no fire.
- No arms, legs, wings, mouth or human features. No glossy 3D render, no plush or mascot look.
```

---

# Prompt v8 (22 nov): NIEUW gesprek, GEEN bijlage, zonder gezicht

## Jordi over v7 (`r7/gemini_v7.png`, letterlijk)
- "nee dit is het ook niet, doe een prompt zonder lunatone erin, kunnen we daarna wel knippen en plakken"
- Dus: oog en neus van Lunatone worden later in de sprite geplakt.

```
Design a new Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

CONCEPT
- A crumbling blood moon: a living full moon of stone during a total lunar eclipse, falling apart. Old, battered and powerful.

DESIGN
- Body: a big round full moon of stone in deep coppery blood red, darker on the shadow side, covered in craters and deep cracks. It is crumbling: chunks have broken off its edge.
- Crumbling pieces: the broken chunks float loose around the moon, none of them touching it, with smaller fragments between them.
- No face: no eyes, no nose, no mouth.

POSE
- Three-quarter view, the sphere slightly tilted, floating.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO soft glow or halo behind the creature, no floor, shadow, sparkles or effects. One single creature, no extra views.

AVOID
- No notch, hollow, cut-out or bite in the moon.
- Not an emblem, badge, logo or symbol. Not a sun. No lava, no gems or crystals, no fire.
- No arms, legs, wings or human features. No glossy 3D render, no plush or mascot look.
```

---

# Prompt v9 (22 nov): NIEUW gesprek, GEEN bijlage, zonder gezicht

## Jordi over v8 (`r8/gemini_v8.png`, letterlijk)
- "teveel detail, kunnen we niet gebruiken, maak er wel echt een pokemon van"

## Analyse Claude
v8 = realistische maanfoto in pixels (vlekkerige textuur, veel scheurtjes, grijze brokken). Nu: weinig grote vormen, vlakke Gen 3-schaduw, Pokémon-stijl zoals Minior/Geodude/Carbink; gezicht blijft leeg (plakken we later).

```
Design a new Rock-type Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art). It must look like a real Pokémon from the games, not like a picture of a planet.

CONCEPT
- A crumbling blood moon: a living full moon of stone during a total lunar eclipse, falling apart. Old, battered and powerful.

DESIGN
- Body: a big round full moon of stone in coppery blood red. Simple and bold like Minior, Geodude or Carbink: a clean round shape with only a few big, clear craters (3 or 4) and 2 or 3 bold cracks. No noisy texture, no speckles, no realistic moon surface.
- Crumbling: a few big chunks have broken off its edge and float loose around it, none of them touching it, in the same red stone. Only 4 or 5 chunks, plus 2 or 3 tiny fragments.
- No face: no eyes, no nose, no mouth. Leave the front-left of the moon smooth and plain.

POSE
- Three-quarter view, the sphere slightly tilted, floating.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from the top left, clean flat cel shading in 4 or 5 tones of red like official Game Freak Gen 3 sprites.
- Plain white background. NO soft glow or halo behind the creature, no floor, shadow, sparkles or effects. One single creature, no extra views.

AVOID
- No realistic or photographic texture, no dithering noise, no many small cracks.
- No notch, hollow, cut-out or bite in the moon. Not an emblem or logo. Not a sun. No lava, no gems, no fire.
- No arms, legs, wings or human features. No glossy 3D render, no plush or mascot look.
```

## Jordi over v9 (`r9/gemini_v9.png`, letterlijk)
- "hebben we ook niks aan, het is geen pokemon en het is niet de stijl waar we met lunatone net ver waren"
- Claude: zonder Lunatone-gezicht verliest Gemini de Pokémon-stijl; voorstel: v4/v5 (of v6) als model nemen en de uitsparing in de sprite dichtmaken (knippen en plakken). Wacht op Jordi.

---

# Prompt v10 (22 nov): NIEUW gesprek, GEEN bijlage

## Jordi (letterlijk)
- "het ligt aan je prompt, je moet de pokemon gewoon beschrijven puur zonder lunatone te benoemen"
- "dus incl oog en neus hoe die eruit moeten zien" (oog en neus beschreven naar Lunatones Gen 3-sprite)

```
Draw an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art) of this Pokémon:

A Rock/Cosmic-type Pokémon that is a blood moon. Its body is a big round full moon made of stone, deep coppery red, as if lit by a total lunar eclipse. It is old and battered: a few large craters, some deep cracks, and pieces have broken off its edge. Those broken pieces float loose around it, close to the body but not touching it.

Its face sits on the left half of the body, at mid-height:
- The eye: one large round eye, bright red iris with a small black vertical slit pupil and a tiny white highlight. The eye sits deep in a thick black socket that is wider on its right side, like a dark crescent-shaped rim hugging the eye.
- The nose: a long, sharp stone spike growing straight out to the left from just beside the eye, level with the eye, about twice as long as the eye is wide. It is wedge-shaped and tapers to a sharp point: a lighter top face and a darker bottom face, divided by one dark line running along its length to the tip. Same red stone as the body.
- The body stays round all the way around the nose: the nose grows out of the bulging surface. The stone around the base of the nose is cracked and crumbled. It has no mouth, no arms, no legs. It floats, seen in three-quarter view facing left.

Sprite: 64x64 pixels, max 16 colors, 1 px dark outline, light from the top left, clean Game Freak shading with bold, simple shapes. Plain white background, no glow, no shadow, no effects.
```

---

# Prompt v11 (22 nov): zelfde gesprek als v10, bijsturen (reactie op `r10/gemini_v10.png`)

## Jordi (letterlijk)
- "ok en nu moeten er meer stukken uitgebrokkeld zijn"

```
Good. Keep everything exactly as it is: the eye, the nose, the colors, the craters, the pose and the size. Change only one thing:

More pieces have crumbled out of the moon. Several clear chunks are missing from its edge, with jagged broken gaps in the round outline, and those broken-off chunks float loose around the body, close to it but not touching it.

Same Gen 3 sprite style, plain white background.
```

## Jordi over v11 (`r11/gemini_v11.png`, letterlijk)
- "nu plak je hier de neus en oog op van lunatone die we al hadden, we halen wat puinstukken weg want dat is ruis en dan hebben we een model"
- "netter plakken"
- "is de pose voldoende driekwart? anders moeten we een nieuwe versie aan gemini vragen"
- Tussenstand plakken (oog + neus van v5, kleine puinstukjes weg; naad rond het oog nog zichtbaar): `model/plak_v11_v5_tussenstand.png`, script `model/script/plak2.py`.

- Jordi: "nee je plakt nu vluchtig en dan vragen we om een driekwart versie"

# Prompt v12 (22 nov): NIEUW gesprek, bijlage `model/plak_v11_v5_tussenstand.png`

```
The attached image is my Pokémon design, a crumbling blood moon. Redraw this exact same Pokémon as a clean official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art). Keep its design exactly: the red cracked stone ball with chunks broken out of its edge, the floating broken pieces, the single red eye with the thick black rim and the pointed stone nose with the dark line along it. Keep the colors.

Change only the pose: a clear three-quarter view facing left. The face sits on the left part of the ball, so more of the right side of the ball is visible. Because the ball is turned, the eye is a slightly narrower oval and the nose points left and a little toward the viewer. The ball stays round all the way around the nose.

64x64 pixels, max 16 colors, 1 px dark outline, light from the top left, clean Game Freak shading. Plain white background, no glow, no shadow, no effects.
```

## Jordi over v12 (`r12/gemini_v12.png`, letterlijk)
- "het lukt hem niet" (pose niet gedraaid; wel netjes opnieuw getekend, oog en neus van v5 erin opgenomen)
- Claude: zelf draaien in het 1024-model geeft naden (geprobeerd, niet bewaard). Voorstel: v12 als model; driekwart in de sprite op 64×64 door oog + neus als geheel een paar pixels naar links te schuiven en het oog 1 px smaller te maken (Krassault-methode: onderdelen als assets verschuiven). Wacht op Jordi.
- Jordi: "probeer nogn 1 keer een prompt from scratch" / "zonder bijlagen"

---

# Prompt v13 (22 nov): NIEUW gesprek, GEEN bijlage, from scratch

Basis v10 (werkte) + Jordi's punten daarna: meer uitgebrokkeld (v11), minder puin (ruis), oog en neus zoals in v5, driekwart.

```
Draw an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art) of this Pokémon:

A Rock/Cosmic-type Pokémon that is a crumbling blood moon. Its body is a big round full moon made of stone, deep coppery red, as if lit by a total lunar eclipse. It is old and battered: a few large craters, some deep cracks, and several big chunks have crumbled out of its edge, leaving jagged gaps in the round outline. Only 4 or 5 of those broken chunks float loose around it, close to the body but not touching it. No tiny debris.

It is seen in a clear three-quarter view, turned to the left, like a globe turned so that its face is on the left side of the ball, close to the left edge. The right half of the ball shows plain cratered stone.

Its face:
- The eye: one large eye, a slightly narrow upright oval because the ball is turned. Bright red iris with a black vertical slit pupil, set in a thick black rim.
- The nose: a short, pointed stone wedge growing out of the curved left side of the ball, just left of the eye, level with the eye, pointing left and a little toward the viewer. A lighter top face and a darker bottom face, divided by one dark line running to the tip. Same red stone as the body.
- The ball stays round all the way around the nose; the stone around the base of the nose is cracked and crumbled.

It has no mouth, no arms, no legs. It floats.

Sprite: 64x64 pixels, max 16 colors, 1 px dark outline, light from the top left, clean Game Freak shading with bold, simple shapes. Plain white background, no glow, no shadow, no effects.
```

## v13 (`r13/gemini_v13.png`): Jordi stuurde hem zonder commentaar
Analyse Claude: driekwart gelukt (gezicht links op de bol), bol rond, weinig puin. Mis: wit oogwit (geen Lunatone-oog), neus klein en kaal (geen lijn), te weinig uitgebrokkeld.

# Prompt v14 (22 nov): zelfde gesprek als v13, bijsturen (voorstel)

```
Good, the three-quarter pose is right. Keep the pose, the ball, the colors, the craters and the floating chunks exactly as they are. Change only two things:

1. The eye: no white in it. The whole eye is a bright red iris with a black vertical slit pupil, filling a thick black rim, like a red gem set deep in the stone. Keep its size and place.
2. Crumbling: more pieces have crumbled out of the moon's edge: several clear chunks missing, with jagged broken gaps in the round outline.

Same Gen 3 sprite style, plain white background.
```

---

# Prompt v14 (23 nov): NIEUW gesprek, bijlage `lunatone_evo_8x.png` (sprite r5 A)

## Jordi (letterlijk)
- "hij is mooi, maar wel volledig horizontaal, misschien nog even toch een keer aan gemini vragen"

```
The attached image is my finished Pokémon sprite, a crumbling blood moon. Redraw this exact same Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), with the same design, colors, eye, nose, cracks, crumbled gaps and floating chunks.

Change only its orientation. Right now it is completely horizontal: the nose points straight left and the eye and nose sit on one flat level line, like a side view. Tilt and turn the whole ball instead, the way Lunatone's own Gen 3 sprite is tilted: the face rotated down toward the lower left, so the nose points down-left and slightly toward the viewer, and the eye sits a bit above and behind the base of the nose. The ball shows more of its top and right side.

64x64 pixels, max 16 colors, 1 px dark outline, light from the top left, clean Game Freak shading. Plain white background, no glow, no shadow, no effects.
```

## Jordi over v14 (`r14/gemini_v14.png`, letterlijk)
- "dit is gedraaid, maar geen driekwart pose" (Gemini draaide alleen in het vlak)
- "hij moet een x aantal graden draaien" / "naar rechts" (graden niet genoemd; in de prompt 30–45 als voorstel Claude)

# Prompt v15 (23 nov): NIEUW gesprek, bijlage `lunatone_evo_8x.png`

```
The attached image is my finished Pokémon sprite, a crumbling blood moon. Redraw this exact same Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), with the same design, colors, eye, nose, cracks, crumbled gaps and floating chunks.

Change only the angle. Right now we see it in pure side view, facing left. Do NOT rotate the picture flat. Instead, the ball spins around its own vertical axis, about 30 to 45 degrees to the right, so its face turns toward the viewer: a three-quarter view facing left, like every Pokémon front sprite:
- The eye is now on the front-left of the ball, seen in perspective: an upright, narrower oval.
- The nose now points toward the viewer and to the left, so it looks shorter in perspective and overlaps the ball; we see its base on the front of the ball, not on the left edge.
- More of the ball's right side, with its cracks and crumbled gaps, is visible behind the face.

64x64 pixels, max 16 colors, 1 px dark outline, light from the top left, clean Game Freak shading. Plain white background, no glow, no shadow, no effects.
```

## Jordi over v15 (`r15/gemini_v15.png`, letterlijk)
- "nee dit is ook niet geslaagd"

---

# Prompt v16 (23 nov): NIEUW gesprek, bijlage `lunatone_evo_8x.png`

## Jordi (letterlijk)
- "laten we nog een keer gemini vragen om een andere pose" / "met perspectief"
- Richting (eerder): "hij moet een x aantal graden draaien" / "naar rechts"; r6 draaide "de verkeerde kant op".

```
The attached image is my finished Pokémon sprite, a crumbling blood moon. Redraw this same Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), with the same design and colors: red cracked stone ball, crumbled gaps, floating chunks, the single red eye with thick black rim and the pointed stone nose.

Give it a new pose WITH PERSPECTIVE, a real three-quarter view like Pokémon front sprites:
- The ball has turned toward the viewer. The face is no longer on the left edge of the ball but on the front of the ball, left of center.
- Behind and around the base of the nose we see the round left edge of the ball continue.
- The nose points left and toward the viewer, so it looks shorter in perspective and its base sits on the front of the ball.
- The eye is seen slightly from the side: an upright oval.
- The ball shows real volume: light on its upper left, a dark shadow band along its right side and bottom, as a sphere seen in perspective.
- The floating chunks are spread in depth: some in front of the ball (larger, overlapping it), some behind it (smaller, partly hidden).

64x64 pixels, max 16 colors, 1 px dark outline, light from the top left, clean Game Freak shading. Plain white background, no glow, no shadow, no effects.
```

## Jordi over v16 (`r16/gemini_v16.png`, letterlijk)
- "voor mijn gevoel is deze beter"
- "alleen de rechterkant is niet meer rond"

# Prompt v17 (23 nov): zelfde gesprek als v16, bijsturen

```
Better. Keep everything exactly as it is: the pose, the perspective, the face, the colors, the cracks and the floating chunks. Change only one thing:

The right side of the ball is flattened into a straight edge. Make the right side round again, so the whole ball has a round outline, like a sphere.

Same Gen 3 sprite style, plain white background.
```
