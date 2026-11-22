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
