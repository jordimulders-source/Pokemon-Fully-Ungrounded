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
- Anatomy: the Great kiskadee (Pitangus sulphuratus) in attachment 1. Keep it a real flycatcher: big flat-topped head, thick black mask through the eye, broad white eyebrow stripe that meets at the back of the head, white throat, short straight sturdy black beak, bright yellow belly, olive-brown back, rusty-brown edges on the wing and tail feathers, short dark legs, medium tail.
- The white eyebrow stripe is a braided headband (the Inca llawt'u): woven white band with a few small red diagonal stripes in it. It must grow from the feathers, it is NOT a separate hat or accessory.
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
