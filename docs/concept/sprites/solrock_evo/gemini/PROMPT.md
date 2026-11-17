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
