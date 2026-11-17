# Gemini-prompt: mate-lijn fase 2 (kano), v2 (16 nov)

Nieuw gesprek (Gemini verbetert slecht). Bijlagen: `../../mate/af/mate_8x.png` (fase 1) en `r1/gemini_r1.png` (concept). Optioneel: een foto van een echte bombilla (lepelvormig zeefje onderaan, gebogen mondstuk).

## Jordi over r1 (letterlijk, 16 nov)
"conceptueel klopt die, maar dit is geen pokemon sprite. de kano heeft ook niks meer weg van de kalebas, de roeispanen moeten echt bombillos zijn"
- "en de ogen moeten uit het hout gekerfd zijn"

## Keuzes Claude (niet besproken; schrappen mag)
- "Geen Pokémon-sprite" gelezen als: lange, platte zijaanzicht-compositie met een klein figuurtje, veel losse spetters en zachte schaduw. Prompt vraagt een compact silhouet dat 64×64 vult, zoals een echte Gen 3-frontsprite.
- Kalebas: de kano is de mate-kalebas zelf, op zijn zij en uitgehold (bolle buik, smalle hals als punt = neus), met dezelfde bruine textuur en de zilveren rand van fase 1 als boord.
- Water: één kleine stroom over de achterrand, geen losse druppels eromheen.

## Prompt

```
Two attached images: (1) a Gen 3 sprite of a yerba mate gourd Pokémon, (2) a concept of its evolution. The CONCEPT of image 2 is right, but it does not look like a Pokémon sprite, the canoe no longer looks like a mate gourd, and the paddles are normal oars. Redesign it.

THE POKÉMON
- The canoe IS the mate gourd from image 1: the same brown dried calabash with the same texture and the silver rim, lying on its side and hollowed out. Short, round and bulbous like the gourd, NOT a long slim boat. The narrow neck of the gourd is the pointed front tip.
- The canoe has two eyes near the front, CARVED into the gourd (cut-in shapes in the brown material, like carvings on a decorated mate gourd), not painted or cartoon eyes. The pointed tip works as its nose. No mouth on the canoe.
- The front part is closed and carries a heap of green yerba mate leaves and powder.
- The back part is open and holds hot water; a little of the water spills over the back edge.
- In the middle sits the little man made of yerba mate leaves (as in image 2). He has the face.
- He paddles with two real bombillas, one in each hand: thin silver metal mate straws with a curved mouthpiece at the top and the flat, spoon-shaped filter at the bottom as the paddle blade. They must clearly be bombillas, not oars.

STYLE AND FORMAT
- An official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, 1 px dark outline, light from top left, flat Gen 3 shading, no dithering, no soft shadows.
- Compact, chunky silhouette that fills the 64x64 frame, seen 3/4 facing left, like a real Pokémon sprite (think of how Lotad or Corphish fill their sprites), not a wide side-view illustration.
- Plain white background. NO river, NO floor, NO shadow, NO loose splash drops or effects.

AVOID
- No long slim canoe, no wooden boat, no normal oars, no human sailor, no Lotad/Ludicolo or Sinistcha look, no Neopets/plush style.
```

## Tips
- Kano nog te lang: "the canoe is almost as tall as it is long, like a round gourd cut open on top".
- Bombilla's nog roeispanen: "replace the oars with mate drinking straws, as thin as a straw, silver".
