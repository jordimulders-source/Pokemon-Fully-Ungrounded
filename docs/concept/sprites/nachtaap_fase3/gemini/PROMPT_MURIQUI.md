# Gemini-prompt: muriqui (nachtaap fase 3) mooier en natuurlijker (8 nov)

Regels: `docs/lessen/GEMINI.md`. SPEC: `../SPEC.md`. Huidige frontsprite (beta): `../af/nachtaap_fase3.png`.

## Jordi (8 nov, letterlijk)
"de muriqui sprite vind ik toch nog wel slordig, dat zouden we gemini nog beter kunnen doen. het idee en concept houden we hetzelfde, maar de pose mag er iets natuurlijker uit zien, hoe lichaam aansluit op benen, armen etc. de healer hand ook, daar blijf ik toch niet helemaal tevreden over, de nazca spiraal staart en hoe de staart toch wel een takje met wat typische andes healing bladeren vast houdt, voor de rest houden we het concept en model, maar maken we het gewoon net wat mooier, passender en natuurlijker."
- De bladeren komen dus terug (5 nov waren ze uit het ontwerp): de staart houdt een takje met bladeren vast.
- "Typische Andes-healingbladeren" in de prompt ingevuld als **coca** (de yatiri leest cocabladeren, zie `POKEMON.md`). Ander blad (bijv. muña) = één woord in de prompt wijzigen.

## Bijlagen (in deze volgorde)
1. `bijlage1_huidige_sprite_8x.png` (huidige sprite; concept, kleuren, pose)
2. `../referenties/foto6_muriqui_tekening_hangend.png` (muriqui hangend, één been omhoog)
3. `../referenties/foto4_moeder_met_jong.jpg` (muriqui-gezicht)
4. `../referenties/drowzee_gen1_sugimori.png` (healerhand: vijf vingers, palm naar de kijker)

Nieuw gesprek per poging; niet lang bijsturen (Gemini drijft af).

## Prompt

```
Redraw an existing original Pokémon as a cleaner, more natural official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

ATTACHMENTS
- Attachment 1 is the current sprite of this Pokémon. KEEP its concept, pose idea, colors and features. It is too messy: the body, arms and legs do not connect naturally, the healing hand looks like a glove, and the tail is stiff. Make it more beautiful and natural, not a different design.
- Attachment 2 is a drawing of the real animal, a muriqui (woolly spider monkey, Brachyteles, Atlantic Forest of Brazil), hanging with one leg up: use it for anatomy and how the long limbs attach to the body.
- Attachment 3 is a photo of a muriqui face.
- Attachment 4 shows the kind of hand I want for the healing hand: five fingers, palm flat towards the viewer.

THE CREATURE
- Final stage of a Psychic starter line (owl monkey line). A gentle healer who looks a bit sinister. Lore: it channels plants and branches with psychic power, so it hangs from invisible branches in mid-air.
- Anatomy of a muriqui: very long thin arms and legs, slim body, long prehensile tail. Exactly two arms, two legs and one tail.
- Face: big bare dark purple face mask framed by fur, straight brow line, small turquoise eyes close together under the brow (stern, not sleepy, no eyelids), light pink-lilac muzzle with nostrils at the top, straight neutral mouth, no ears visible. A white crescent moon on top of the head.
- Colors: lavender-blue violet fur (lighter and bluer than Oranguru), darker violet in the shadows, three broad light silver-blue curved bands across the middle of the back that wrap around the body.

POSE AND VIEW (same as attachment 1, but natural)
- It floats low in the air, body almost horizontal and tilted up towards the back, head at the front left in 3/4 view looking at the viewer.
- Near arm raised up and forward, the hand closed in a fist around an invisible branch.
- One leg raised straight up, the foot curled around an invisible branch. The other leg hangs relaxed down and back. Both legs grow naturally out of the hips, the arms out of the shoulders; the body reads as one smooth animal, like a muriqui really hanging.
- The other arm reaches forward-down under the head: the HEALING HAND. A real open hand with five fingers close together and slightly curved, palm flat towards the viewer, thumb to the side, like a healer or mage casting a healing spell in anime. The hand is silver-blue, surrounded by a soft flat turquoise band of light with its own outline (Reuniclus style, not a blurry glow).
- Tail: up behind the body, ending in a big open spiral like the Nazca monkey geoglyph, with air between the coils (they do not touch). The tip of the tail holds a small twig with three or four coca leaves (small oval green leaves, Andean healing leaves), big enough to read clearly at sprite size.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites, large calm shading areas, no noise.
- Plain white background. NO visible branches except the small twig in the tail, no ground, rock, shadow or base.
- No sparkles, motion lines, text or extra effects besides the turquoise band around the hand. One single creature, no extra views.

AVOID
- Not Oranguru, Ambipom, Aipom, Infernape, Mew or Alakazam.
- Not a gibbon or a human; no clothing.
- No starfish pose with stiff straight limbs, no glove or mitten hand, no fingers spread wide apart, no balloon arms.
- No plush toy, chibi, Neopets or mascot look; no oversized sparkly eyes.
```
