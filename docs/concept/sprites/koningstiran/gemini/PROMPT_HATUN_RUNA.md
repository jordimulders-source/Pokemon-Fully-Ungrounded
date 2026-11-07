# Gemini-prompt: koningstiran fase 1 "hatun runa" (7 nov)

Regels: `docs/lessen/GEMINI.md`. Lijn: `docs/concept/POKEMON.md` (Koningstiran-lijn), eindvorm `../af/sapa_inca.png`, richting `docs/concept/ontwerp/koningstiran/schets_v2.png` (fase 1 links).

## Bijlagen (in deze volgorde)
1. Een foto van een **grote kiskadie** (*Pitangus sulphuratus*, Great kiskadee), staand, liefst van schuin voren (Jordi zoekt er een; zet hem daarna in `../referenties/kiskadie_foto.*`).
2. `bijlage_sapa_inca_6x.png` (de eindvorm, 6× vergroot): alleen voor kleuren en stijl van de lijn.

## Prompt (in een nieuw gesprek plakken)

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

WHAT IT IS
- The first stage of a 3-stage bird line from a South American region. Typing: Normal/Flying. A common early-route bird, small and plain, like a city sparrow, but with a hidden royal destiny.
- Anatomy: the Great kiskadee (Pitangus sulphuratus) in attachment 1. Keep it a real flycatcher: big flat-topped head, thick black mask through the eye, broad white eyebrow stripe that meets at the back of the head, white throat, short straight sturdy black beak, bright yellow belly, warm dark brown back, rusty-brown edges on the wing and tail feathers, short dark legs, medium tail.
- Inside the white eyebrow stripe: a small repeating Andean textile pattern (tiny squares and step shapes, like Inca tocapu) in red, gold and black, as if the feathers themselves are woven. It is a feather marking, NOT a headband, rope, cloth or knot (it must not look Japanese).
- Hidden crown: on top of the head only a small yellow patch peeks out between the dark feathers (the real kiskadee has a hidden yellow crown). Just a hint, no fan, no crest.
- Attachment 2 is its FINAL evolution. Use it only for the shared palette (warm brown, ochre-yellow belly, gold accents). Do NOT copy its fan crown, staff, ear discs or pose. This stage is the humble beginning.

POSE AND VIEW
- Standard front-sprite view: body in 3/4 view facing left, head turned slightly more towards the viewer than the body (we see the beak pointing left-down and one eye clearly, the far eye barely).
- Standing upright on its own feet, wings folded, a bit of attitude: chest slightly out, alert, confident, curious. Not sleepy, not angry.
- Chunky proportions: head about 40% of the body height, round compact body.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean flat shading like official Game Freak sprites.
- Plain white background. NO branch, perch, rock, ground, shadow or base under the feet.
- No glow, sparkles, motion lines, speech bubbles, text or effects.
- One single creature, no turnaround sheet, no extra views.

AVOID
- Do not make it look like Pikachu (yellow + black is a risk: no red cheeks, no pointed ears, no zigzag tail).
- Do not make it look like Pidgey, Taillow, Starly, Fletchling, Pikipek, Rookidee or Wattrel.
- No plush toy, chibi, Neopets or mascot look; no oversized sparkly eyes. It is a wild animal that looks like a Pokémon.
- No Inca costume, mask, hat, jewelry or clothing. The Inca references are feathers and markings only.
```

## Tips voor Jordi (Gemini-beperkingen)
- Gemini maakt geen echte 64×64; dat is niet erg: het plaatje is de ontwerpreferentie, de maker-agent vertaalt het later naar de sprite.
- Bijsturen werkt hooguit 1–2 keer met één korte zin per keer (bijv. "same design, only make the eyebrow band wider"). Daarna drijft hij af.
- Daarna liever: **nieuw gesprek**, de beste versie als bijlage erbij en bovenaan de prompt: `Use the attached image as the base design. Keep its pose, proportions and colors. Change only: ...`
- Vraag niet om "more Pokémon" of "cuter": dan glijdt hij naar bekende soorten.
- Stuur elke ronde terug; ik leg de feedback vast in `gemini/README.md` en de keuze als `referenties/gemini_gekozen_*.png`.

## Startprompt v2 (7 nov, nieuw gesprek; vervangt de prompt hierboven)
Jordi: "schrijf een nieuwe prompt voor een nieuw gesprek en ik zal de sprite van fase 3 erbij doen, het helpt als je heel specifiek beschrijft wat voor inca verwijzing we erin doen". Bijlage: de Sapa Inca-sprite (eventueel ook een kiskadiefoto als tweede bijlage).

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

The attached sprite is the FINAL (3rd) stage of this line: a royal bird based on the Inca emperor (Sapa Inca). I need the FIRST stage: the same bird as a humble commoner (in Quechua: "hatun runa", common man). Use the attached sprite only for the palette and the family resemblance. Do NOT copy its fan crown, staff, gold ear discs, size or pose.

THE ANIMAL
- A Great kiskadee (Pitangus sulphuratus), a common South American city bird. Small, chunky, Normal/Flying, an early-route bird.
- Real kiskadee anatomy: big flat-topped head, BLACK crown, thick BLACK mask through the eye, broad WHITE eyebrow stripe from above the beak all the way around the back of the head, white throat, short straight sturdy black beak, yellow belly, short dark legs, medium tail.
- Colors matched to the attached final stage: back and folded wings warm dark brown, belly golden yellow, rust-brown edges on wing and tail feathers.

THE INCA REFERENCE (be exact, nothing more)
- In the Inca empire every commoner wore a "llawt'u": a narrow woven band wrapped around the head, with a pattern of "tocapu" (small square cells with simple geometric shapes: steps, crosses, diagonal halves, checkers). Only the emperor added the red fringe and feather crown, which this bird gets later when it evolves.
- On this bird, the llawt'u IS the white eyebrow stripe of the kiskadee. Inside that white feather stripe, a single row of tiny square tocapu cells (about 5 to 7 visible on the near side), alternating red, gold and black, each with a simple step or checker shape, with a thin black line along the top and bottom of the stripe. It is a FEATHER MARKING, flat on the head, following the curve of the head.
- Hidden crown: in the middle of the black crown, one small gold-yellow spot peeking out between the feathers (the real kiskadee has a hidden yellow crown; it is the seed of the emperor's fan crown). Just a spot, no crest, no fan.
- That is the only Inca element. No clothing, jewelry, mask, hat, gold ear discs or fringe at this stage.

POSE AND VIEW
- Body in 3/4 view facing left, head turned a bit more towards the viewer than the body: beak pointing left, near eye clearly visible, the far side of the eyebrow stripe just visible so the pattern reads as going around the head.
- Standing on its own feet, wings folded, chest slightly out, alert and a bit cocky: a small bird that already acts important. Not sleepy, not angry.
- Head about 40% of the body height, round compact body.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO branch, perch, rock, ground, shadow or base.
- No glow, sparkles, motion lines, text or effects. One single creature, no extra views.

AVOID
- Nothing Japanese: no rope, twisted cord, knot, loose ends, cloth headband or hachimaki. No red-and-white only combination on the head.
- Not Pikachu (no red cheeks, no pointed ears, no zigzag tail).
- Not Pidgey, Taillow, Starly, Fletchling, Pikipek, Rookidee or Wattrel; not a great tit or generic finch: the black-and-white kiskadee head must be the first thing you see.
- No plush toy, chibi, Neopets or mascot look; no oversized sparkly eyes.
```

## Startprompt v3 (7 nov, nieuw gesprek; vervangt v2)
Jordi: "ik wil eigenlijk ook een actievere pose [...] ik wil iets anders dan een vogel die weer vooruit poseert zoals zoveel sprites". Patroon in fase 1 weg (Claude-voorstel: Inca-tekens pas vanaf fase 2). Bijlagen: 1 = Sapa Inca-sprite, 2 = `ronde3_bijgestuurd.png` (kop en kleuren).

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

ATTACHMENTS
- Attachment 1 is the FINAL (3rd) stage of this line, a royal bird based on the Inca emperor. Use it only for palette and family resemblance. Do NOT copy its fan crown, staff, ear discs or pose.
- Attachment 2 is my current design of the FIRST stage. Keep its head, colors and proportions. Change the pose completely and remove the band pattern (see below).

THE CREATURE
- First stage, Normal/Flying, an early-route bird: a Great kiskadee (Pitangus sulphuratus), the loud, bold city bird of South America that shouts its own name ("bem-te-vi") and chases birds much bigger than itself.
- Head: black crown, thick black mask through the eye, two broad WHITE eyebrow stripes that meet at the back of the head, white throat, one small gold-yellow spot in the middle of the black crown (its hidden crown). The white stripes are PLAIN white feathers: no pattern, no dots, no band, no cap look; the black crown must show clearly between the two white stripes.
- Body: warm dark brown back and wings, rust-brown edges on wing and tail feathers, golden yellow belly, short straight sturdy black beak, short dark legs.

POSE (most important)
- Not the standard standing bird. Show it in action: the moment it launches off to snatch an insect. Body tilted forward and down towards the left, about 30 degrees.
- Near wing raised high in the upstroke, bent at the wrist, flight feathers fanned out behind the body; far wing half visible, lower, not symmetrical with the near wing. Not a T-pose, not both wings spread flat.
- Beak wide open, shouting, showing the inside of the mouth. Eye fierce and focused on its target, cocky, not cute and not angry.
- Legs tucked under the body or kicking back, tail fanned and angled up behind.
- Head in 3/4 view towards the viewer: near eye clearly visible, both white stripes visible.
- The whole bird must fit inside the frame with a clear, compact silhouette.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO branch, perch, ground, shadow, insect, motion lines, speed lines, wind, glow or effects. One single creature, no extra views.

AVOID
- No headband, cap, rope, cord, beads or any accessory; no Inca or Japanese clothing.
- Not Pikachu, Pidgey, Taillow, Swellow, Starly, Fletchling, Pikipek, Rookidee or Wattrel; not a generic finch or great tit.
- No plush toy, chibi, Neopets or mascot look; no oversized sparkly eyes.
```

Bijsturen (max. 1–2 keer, één zin): bijv. `same design, near wing higher and more bent at the wrist` of `same design, beak open wider, shouting`.
