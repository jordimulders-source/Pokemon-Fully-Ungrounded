# Gemini-prompt: muriqui (nachtaap fase 3) mooier en natuurlijker (8 nov)

Regels: `docs/lessen/GEMINI.md`. SPEC: `../SPEC.md`. Huidige frontsprite (beta): `../af/nachtaap_fase3.png`.

## Jordi (8 nov, letterlijk)
"de muriqui sprite vind ik toch nog wel slordig, dat zouden we gemini nog beter kunnen doen. het idee en concept houden we hetzelfde, maar de pose mag er iets natuurlijker uit zien, hoe lichaam aansluit op benen, armen etc. de healer hand ook, daar blijf ik toch niet helemaal tevreden over, de nazca spiraal staart en hoe de staart toch wel een takje met wat typische andes healing bladeren vast houdt, voor de rest houden we het concept en model, maar maken we het gewoon net wat mooier, passender en natuurlijker."
- De bladeren komen dus terug (5 nov waren ze uit het ontwerp): de staart houdt een takje met bladeren vast.
- "Typische Andes-healingbladeren" in de prompt ingevuld als **coca** (de yatiri leest cocabladeren, zie `POKEMON.md`). Ander blad (bijv. muña) = één woord in de prompt wijzigen.

## Bijlage
1. `bijlage1_huidige_sprite_8x.png` (huidige sprite), **de enige bijlage** (Jordi, 8 nov: "we gaan alleen de muriqui sprite als bron gebruiken, geen andere afbeeldingen. gemini kan wel een hand maken").

Jordi (8 nov, tweede bericht): "het gaat erom dat we een slordige sprite hebben waar ik eigenlijk totaal niet tevreden mee ben en die moet een stuk mooier op veel vlakken (gezicht, hoofdvorm, lichaamsvorm, positie armen en benen, aansluiting op lichaam, lichaam zelf, patroon op lichaam, staartvorm etc), maar dat ik heilig blijf gelopen in die zweefhangende pose" → prompt herschreven: alles mag mooier, de zweefhangende pose is heilig.

Nieuw gesprek per poging; niet lang bijsturen (Gemini drijft af).

## Prompt

```
Redesign this Pokémon as a beautiful official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

ATTACHMENT
- The attachment is the current sprite of this Pokémon. It is sloppy and I am not happy with it. It must become much more beautiful in almost every area: the face, the head shape, the body shape, the position of the arms and legs, how the limbs connect to the body, the body itself, the pattern on the body and the shape of the tail.
- The ONE thing that is sacred: its floating-hanging pose. Keep that pose idea exactly (described below). Everything else may be redrawn and improved, as long as it stays the same creature and concept.

THE CREATURE
- Final stage of a Psychic starter line from South America (it starts as an owl monkey). Based on a real muriqui (woolly spider monkey, Brachyteles, Atlantic Forest of Brazil): very long arms and legs, slim body, long prehensile tail. Exactly two arms, two legs and one tail.
- Personality: a gentle healer who looks a bit sinister. Lore: it channels plants and branches with psychic power, so it hangs from invisible branches in mid-air.
- Face: a muriqui face. Bare dark face framed by fur, small turquoise eyes close together under a straight brow (stern, not sleepy), a lighter muzzle, a neutral mouth. A white crescent moon on the head.
- Colors: lavender-blue violet fur (bluer and lighter than Oranguru), turquoise eyes, a silver-blue healing hand, a pattern of light silver-blue curved bands across the back that follow the shape of the body.

THE POSE (sacred, keep this)
- It floats low in the air, as if hanging from invisible branches. Body almost horizontal and tilted up towards the back, head at the front left in 3/4 view, looking at the viewer.
- One arm raised up and forward, the hand closed around an invisible branch.
- One leg raised up high, the foot curled around an invisible branch. The other leg hangs relaxed down and back.
- The other arm reaches forward-down under the head and makes a HEALING gesture: an open hand with five fingers, palm towards the viewer, like a healer or mage casting a healing spell in anime. Around the hand a soft turquoise band of light with its own outline (Reuniclus style, not a blurry glow).
- Tail up behind the body, ending in a big open spiral like the Nazca monkey geoglyph, with air between the coils. The tip of the tail holds a small twig with a few coca leaves (Andean healing leaves), big enough to read at sprite size.
- Make the pose natural: legs grow out of the hips, arms out of the shoulders, the body is one smooth animal, like a real monkey hanging and reaching.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites, large calm shading areas, no noise.
- Plain white background. No visible branches except the small twig in the tail, no ground, rock, shadow or base.
- No sparkles, motion lines, text or effects besides the band of light around the hand. One single creature, no extra views.

AVOID
- Not Oranguru, Ambipom, Aipom, Infernape, Mew or Alakazam. Not a gibbon or a human; no clothing.
- No starfish pose with stiff straight limbs, no glove or mitten hand, no balloon arms.
- No plush toy, chibi, Neopets or mascot look; no oversized sparkly eyes.
```
