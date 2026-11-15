# Gemini-prompt r1 Hauntflare (Claude, 15 nov)
Regels: `docs/lessen/GEMINI.md`. Bijlage: `../referenties/haunter_gen3_8x.png` (Haunter, Gen 3 frontsprite).

## Jordi (letterlijk)
- "hauntflare tijd, maak een prompt voor gemini"
- Lijn en verschijnselen: zie `../SPEC.md` en `../../gengas/SPEC.md`.

## Keuzes Claude (Jordi heeft hier niets over gezegd; schrappen of aanpassen mag)
- **Gezicht:** ogen en grijns exact Haunter (zoals bij Gengas, waar Jordi dat voor Gengar vroeg).
- **Lijf:** de protoster = een gloeiende gasbol in een donkere stofschijf die als een rand om het midden ligt (zoals echte protosterfoto's: heldere bol, donkere band ervoor).
- **Jets = Haunters vorm:** de bovenste jet geeft de puntige kop/stekels, de onderste jet is de staartsliert van Haunter.
- **Handen = Herbig-Haro-knopen:** twee losse gloeiende gasknopen in Haunters handvorm, aan het eind van de jets (zelfde idee als de manen van Gengas: los, met een gat).
- **Kleur:** de echte kleur van Herbig-Haro-knopen (rood/roze van waterstof, het oranje van de schokfronten), stofschijf donker roodbruin; past bij Gengas (rood-magenta). Geen Haunter-paars.
- **Pose:** zwevend, driekwart naar links (zoals Gengas).
- Gloed wordt niet gevraagd (GEMINI.md): jets als vaste vormen.

## Prompt

```
Design a new Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style): 64x64 pixel art, at most 16 colours, 1-pixel dark outline around every part, light from the top left, plain white background, no ground, no shadow, no glow, no sparkles, no effects outside the creature.

The Pokémon is "Hauntflare", a Cosmic/Poison type based on a PROTOSTAR: a newborn star inside a cloud of dust that shoots out two jets of gas from its poles (Herbig-Haro jets). It is NOT a ghost and NOT related to Haunter; it only looks similar by coincidence (convergent evolution, like Wiglett and Diglett). Its shape must clearly differ from Haunter.

FACE: use the attached Haunter sprite. The eyes and the wide grin must be exactly Haunter's (same shape, same size, same teeth), turned into the three-quarter view.

BODY: a round, glowing ball of hot gas (the young star) in the centre, with a dark, thick ring of dust around its middle like a flat disc seen slightly from above, crossing in front of the lower part of the ball. The face sits on the ball, above the dust ring.
JETS: two jets of gas shoot out of the ball in opposite directions, drawn as solid, clean shapes:
- the upper jet comes out of the top of the ball as two or three sharp, backward-pointing flame-like spikes, which give the head its pointed shape;
- the lower jet comes out of the bottom as one long, tapering, wavy tail that ends in a point.
HANDS: exactly two hands, shaped like Haunter's hands (three fingers), made of bright knots of glowing gas. They float free near the ends of the jets, with a clear gap of white background between each hand and the body. Nothing else floats.
COLOUR: the real colours of Herbig-Haro jets: the ball bright pinkish-white in the centre, the jets and hands red and rose-pink with orange edges, the dust ring dark reddish-brown. NOT Haunter's purple, not blue.

POSE: a true three-quarter view facing LEFT, floating in space, the near hand bigger and in front, the far hand smaller and partly behind the body. Compact so everything fits in a square.

AVOID: a ghost look, a purple colour, a cape or cloth, legs or feet, arms connected to the body, extra hands, rings like Saturn around the whole body, stars or sparkles around it, glow effects, messy smoke strands, a cute plush, chibi or Neopets look, a glossy 3D render.
```

## Tips
- Wordt het Haunter met een andere kleur: nieuw gesprek, "its body is a ball with a dust disc, not Haunter's head" bovenaan.
- Schijf wordt een Saturnusring om alles heen: "the dust disc is thick and dark and only crosses the lower half of the ball".
- Niet langer dan 1–2 keer bijsturen in hetzelfde gesprek (GEMINI.md).
