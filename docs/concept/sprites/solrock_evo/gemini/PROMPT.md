# Gemini-prompt: Solrock-evolutie "corona", startprompt v1 (17 nov)

Regels: `docs/lessen/GEMINI.md`. Ideeën en citaten: `docs/concept/IDEEEN.md` (Cosmic-lijnen).
Bijlage: `bijlage_solrock_gen3.png` (Solrocks eigen Gen 3-frontsprite, 8× vergroot). Zelf toe te voegen (Jordi, optioneel): een foto van een meteoriet met zwarte smeltkorst en een doorgezaagde pallasiet (Imilac, Atacama).

## Jordi (letterlijk, 17 nov)
- "lunatone zou wel moeten lukken, maar hoe ga je solrock een geloofwaardige corona evolutie geven, terwijl je tegelijkertijd de link met solrock blijft behouden, wat een stenen meteoriet is geinspireerd door de zon ipv een zon"
- "doe een prompt zodat ik kan visualiseren"

## Voorstel Claude (17 nov), nog niet besloten
- Evolutie zoals optie B: Solrock evolueert met een Lunatone in het team; de corona wordt pas zichtbaar als de maan voor de zon schuift.
- Alles blijft steen: gezicht zwart als smeltkorst, stralen breken los en zweven als een halo van steensplinters, de corona is licht dat tussen de stenen door lekt, protuberansen zijn lussen van gesmolten gesteente, de diamantring is één olivijnkristal (pallasiet) in de rand.
- 6–8 grote stukken + 2 lange splinters (meer wordt pixelruis).

## Prompt

```
Design the evolution of the Pokémon SOLROCK and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE ATTACHED SPRITE IS SOLROCK (the pre-evolution). Keep it clearly recognizable: the same kind of yellow stone spikes, the same yellow face plate with the red eye slit, the same stony texture.

CONCEPT
- Solrock is NOT the sun: it is a stone meteorite shaped like the sun. Its evolution stays made of stone.
- It evolves when a Lunatone (the moon) is with it, like a solar eclipse: the moon covers the sun and the hidden corona becomes visible.
- Everything in the design is rock, not gas, plasma or fire.

DESIGN
- Central body: the round stone body has turned dark, almost black, with a glassy fusion crust like a real meteorite that burned through the atmosphere. Solrock's face plate and red eye are still there, set in this dark body.
- Corona: Solrock's yellow stone spikes have broken off the body and now float around it as a ring of separate stone shards, with small gaps between the body and each shard. Use 6 to 8 large shards, plus 2 long thin splinters that stick out further (the corona streamers).
- The corona is the bright pale yellow-white light that shines through the gaps between the dark body and the floating shards. The shards themselves stay stone.
- One or two arcs of molten red-orange rock loop off the edge of the body (like solar prominences), thick enough to read as solid lava, not as fire effects.
- One single bright yellow-green crystal (olivine, like in a pallasite meteorite) set in the rim of the body, where the "diamond ring" flash of an eclipse would be.
- Readable silhouette: a dark round core with a jagged, broken halo of floating stone shards. Recognizably an evolved Solrock.

POSE
- Three-quarter view facing left, floating (no legs).

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO floor, shadow, base platform, sparkles, glow aura or effects outside the creature. One single creature, no extra views.

AVOID
- Not a sun with a face. Not made of gas, flames or plasma.
- Not a black sphere with a plain glowing ring around it.
- Not a crown or headdress on a ball. No arms, legs, wings or human features.
- No glossy 3D render, no plush or mascot look.
```

---

# Prompt v2 (17 nov): zelfde gesprek, reactie op v1 (`r1/gemini_v1.png`)

## Jordi (letterlijk)
- "dit is niet helemaal wat je bedoelt he" / "ja schrijf v2"

## Analyse Claude
Punten zitten nog vast (geen kieren, geen licht ertussen; corona = vage gloed erachter, leest als zeemijn); lava = lange touwen eromheen. Goed: donker lijf met smeltkorst, gezicht. Kristal later. Max. 2 wijzigingen.

```
Good start: keep the dark fusion-crust body and the face exactly as they are. Change only two things:

1. The yellow stone spikes must be DETACHED from the body. Each spike floats at a clear distance from the dark body, not touching it. In the gap between the body and the ring of floating spikes there is a narrow, bright pale yellow-white band of light, as if light is shining out from behind the dark body. This band of light is the corona. Remove the soft round glow behind the creature.
2. The lava: replace the long red ropes with one short arc of molten rock that rises from the rim of the body and falls back onto it, close to the edge, like a solar prominence.

Same number of spikes, same pose, same Gen 3 sprite style, plain white background.
```

---

# Prompt v3 (17 nov): NIEUW gesprek, startprompt (reactie op v2, `r2/gemini_v2.png`)

## Jordi (letterlijk)
- "al wel ietsje beter he, maar nog niet helemaal"

## Analyse Claude
v2: grote punten zitten nog steeds vast, gloed erachter blijft; nieuw is een buitenring van kleine losse splinters (die maakt het "opengebroken"). Lava werd een haakje dat op een tong lijkt. Gemini begrijpt "licht in de kier" niet; daarom nieuw gesprek (vorige versie niet als bijlage, anders kopieert hij hem) en de corona nu als concreet beeld: een dunne felle rand strak om het zwarte lijf, zoals op eclipsfoto's, met witte achtergrond tussen rand en zwevende stukken.

```
Design the evolution of the Pokémon SOLROCK and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE ATTACHED SPRITE IS SOLROCK (the pre-evolution). Keep its yellow stone spikes, its yellow face plate with the red eye slit and its stony texture recognizable.

CONCEPT
- Solrock is a stone meteorite shaped like the sun. It evolves when the moon (Lunatone) is with it: a total solar eclipse made of stone.
- Everything is rock. No gas, flames, plasma or glow effects.

DESIGN
- Core: a round body of dark, almost black stone with a glassy fusion crust (like a meteorite that burned through the atmosphere). Solrock's yellow face plate with the red eye sits on it.
- Eclipse rim: around the dark body runs a thin, bright pale yellow-white rim, hugging the body tightly, exactly like the bright edge around the black moon in a photo of a total solar eclipse. This rim is the only light in the design.
- Broken corona: Solrock's yellow stone spikes have broken loose. All of them float OUTSIDE the bright rim, with white background visible between the rim and every spike. Not a single spike touches the body. 8 large spikes pointing outward, and between them a few small loose stone splinters further out, as if the corona is crumbling apart.
- Prominence: one small arch of molten red-orange rock standing on the top-right edge of the body, shaped like an upside-down U with both ends on the rim.
- One bright yellow-green olivine crystal set into the rim of the body.

POSE
- Three-quarter view facing left, floating.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO soft glow or halo behind the creature, no floor, shadow, sparkles or effects. One single creature, no extra views.

AVOID
- Not a naval mine or spiked ball: the spikes must not be attached to the body.
- Not a sun with a face. No tongue-like shapes, no ropes or tentacles.
- No arms, legs, wings or human features. No glossy 3D render, no plush or mascot look.
```

---

# Prompt v4 (17 nov): NIEUW gesprek, startprompt (reactie op v3, `r3/gemini_v3.png`)

## Jordi (letterlijk)
- "dat oranje ding en die gele edelsteen, verzint die dat zelf telkens?" (nee: voorstellen van Claude; geschrapt)
- "ik vind deze niet zo mooi, asynchroon en maar 1 oog"

## Behouden uit v3
Losse punten buiten een dunne felle rand om het zwarte lijf (eclipsbeeld werkt).

```
Design the evolution of the Pokémon SOLROCK and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE ATTACHED SPRITE IS SOLROCK (the pre-evolution). Keep its yellow stone spikes, its yellow face plates with the two red eye slits and its stony texture recognizable.

CONCEPT
- Solrock is a stone meteorite shaped like the sun. It evolves when the moon (Lunatone) is with it: a total solar eclipse made of stone.
- Everything is rock. No gas, flames, plasma, lava, gems or glow effects.

DESIGN
- Core: a round body of dark, almost black stone with a glassy fusion crust (like a meteorite that burned through the atmosphere).
- Face: Solrock's own face, with TWO red eye slits, as in the attached sprite, set on the dark body.
- Eclipse rim: around the dark body runs a thin, bright pale yellow-white rim, hugging the body tightly, exactly like the bright edge around the black moon in a photo of a total solar eclipse. This rim is the only light in the design.
- Broken corona: Solrock's yellow stone spikes have broken loose. All of them float OUTSIDE the bright rim, with white background visible between the rim and every spike. Not a single spike touches the body. 8 large spikes, evenly spaced all around and pointing straight outward, with a few small loose stone splinters further out between them.
- Symmetrical and balanced: the spikes form an even, regular ring around the body.

POSE
- Facing the viewer, turned slightly to the left, floating.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO soft glow or halo behind the creature, no floor, shadow, sparkles or effects. One single creature, no extra views.

AVOID
- Not a naval mine or spiked ball: the spikes must not be attached to the body.
- No lava, no gems or crystals, no one-eyed face.
- Not a sun with a human face. No arms, legs, wings or human features. No glossy 3D render, no plush or mascot look.
```

---

# Prompt v5 (22 nov): NIEUW gesprek, startprompt (reactie op v4, `r4/gemini_v4.png`)

## Jordi (letterlijk)
- "dit is het nog niet helemaal he"; op Claudes analyse (embleem/logo, gezicht = sieraad, te weinig evolutie): "wat je zegt klopt volledig"
- "A is lastig uit te beelden, het gaat er vooral om dat Solrock echt een meteoor is die aan elkaar vast zit en dat deze nu veel meer losgaat, dus de stenen zijn echt los en zweven eromheen, diagonale baan is wel een goed idee, en qua kleur echt eclipse creëren, dan lijkt die krachtiger. Punten afbreken ook wel een goed idee, ouder en gehavender ook"

## Keuzes Claude (schrappen mag)
- 3/4 gekanteld zoals Solrocks eigen sprite (tegen het embleemgevoel); gezicht = Solrocks gezichtsplaat uit de bijlage.
- "Echt eclipse" als kleur: zwarte kern, felle wit-gouden rand; de zwevende stenen in tegenlicht (donker met een lichte rand aan de kant van de kern).

```
Design the evolution of the Pokémon SOLROCK and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE ATTACHED SPRITE IS SOLROCK (the pre-evolution). Copy its face plate with the red eyes exactly, and keep the shape of its stone spikes recognizable.

CONCEPT
- Solrock is a meteorite of stones stuck together in the shape of the sun. Its evolution is that meteorite coming apart: the stones are now truly loose and float around a dark core.
- It evolves when the moon (Lunatone) is with it: a total solar eclipse made of stone. Older, battered and more powerful than Solrock.

DESIGN
- Core: a round body of dark, almost black stone, scarred and cracked, with Solrock's face plate on it.
- Eclipse colors: the black core is surrounded by a thin, intensely bright white-gold rim, like the edge of the black moon in a total solar eclipse. This rim is the main light source.
- Floating stones: Solrock's spikes have broken off and float around the core as separate stones, none of them touching the body. Several spikes are broken: snapped tips, jagged ends, chips missing. Between them float smaller fragments.
- The floating stones are backlit by the eclipse: dark stone with a bright edge on the side facing the core.
- Orbit: the stones circle the core in a tilted, diagonal orbit (like a ring seen at an angle), so stones in front of the core are larger and overlap it, stones behind it are smaller and partly hidden by it.

POSE
- Three-quarter view facing left, tilted like Solrock's own sprite, floating. Not straight-on, not symmetrical.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO soft glow or halo behind the creature, no floor, shadow, sparkles or effects. One single creature, no extra views.

AVOID
- Not an emblem, badge, logo or compass: no flat, symmetrical, straight-on layout.
- Not a spiked ball: the stones must not be attached to the body.
- No lava, no gems or crystals. No arms, legs, wings or human features. No glossy 3D render, no plush or mascot look.
```
