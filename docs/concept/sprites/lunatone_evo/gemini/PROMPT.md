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
