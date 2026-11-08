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

## Prompt v2 (afgekeurd, ronde 1: `afgekeurd_r1.png`)

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

## Ronde 1 (Jordi, 8 nov, letterlijk)
"nog steeds niet tevreden, de handen zijn nog steeds ontzettend onnatuurlijk, en het silhouet is nog niet mooi, de maanvorm op het hoofd is slechter dan het origineel en hij kijkt boos, waar die heel neutraal moet kijken. de tak zit in de bovenste voet wat ook op een hand lijkt, die moet in de staart. Het rugpatroon is echt lelijk, net zo lelijk als wat we al hadden, je prompt wilde de originele sprite denk ik te true to form houden, maak een nieuwe prompt, ik start een nieuw gesprek in gemini, wel met de originele sprite nog steeds erbij"

## Prompt v3 (nieuw gesprek, bijlage: alleen `bijlage1_huidige_sprite_8x.png`)

```
Design a Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art). Draw it fresh, as a Game Freak artist would.

ATTACHMENT
- The attachment is an old, failed sprite of this Pokémon. Use it ONLY as a rough reference for the concept, the colors and the pose idea. Do NOT trace it or stay close to its shapes: its silhouette, hands, head, body, back pattern and tail are all badly drawn. Redesign all of those so they look like they belong to an official Pokémon.

THE CREATURE
- Final stage of a Psychic starter line from South America. Based on a real muriqui (woolly spider monkey, Brachyteles): long arms and legs, slim body, long prehensile tail. Exactly two arms, two legs and one tail.
- A gentle healer. It hangs from invisible branches in mid-air with psychic power.
- Expression: completely NEUTRAL and calm. Not angry, not frowning, not smiling, not sleepy.
- Face: a muriqui face: bare dark face framed by fur, small turquoise eyes, a lighter muzzle, a neutral closed mouth.
- On the head: a crescent moon like in the attachment, a broad white crescent that follows the curve of the top of the head. Not a small icon or sticker on the forehead.
- Colors: lavender-blue violet fur, turquoise eyes, silver-blue hands.
- Back pattern: the pattern in the attachment is ugly. Design a clean, simple back pattern the way Game Freak would: a few large, calm shapes that follow the 3D form of the body. No scratchy, wavy or thin stripes.

THE POSE (keep this idea, the only thing that is fixed)
- It floats low in the air as if hanging from invisible branches. Body almost horizontal and tilted up towards the back, head at the front left in 3/4 view, looking at the viewer.
- One arm raised up and forward, its hand gripping an invisible branch.
- One leg raised up high, its FOOT gripping an invisible branch. It is clearly a monkey foot, not a hand, and it holds NOTHING visible.
- The other leg hangs relaxed down and back.
- The other arm reaches forward-down under the head: the healing hand, open, palm towards the viewer, like a healer casting a healing spell in anime. Around this hand a soft turquoise band of light with its own outline.
- Tail up behind the body, ending in an open spiral like the Nazca monkey geoglyph. ONLY the tip of the TAIL holds a small twig with a few coca leaves.

HANDS (most important, they failed every time)
- Both hands must look natural and anatomically believable, drawn like the hands of official Pokémon such as Machamp, Hitmonchan, Mr. Mime or Medicham: correct size for the arm (not huge, not tiny), fingers in proportion, a clear wrist.
- No glove, mitten, cartoon cushion hand or stiff spread fingers.

SILHOUETTE
- A beautiful, readable silhouette with flowing lines, like an official Pokémon: limbs tapering naturally, legs growing out of the hips, arms out of the shoulders, the body as one smooth animal. No starfish pose, no stiff straight tubes.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Gen 3 sprites, large calm shading areas, no noise.
- Plain white background. No ground, rock, shadow or base. No visible branch except the twig in the tail.
- No sparkles, motion lines, text or effects besides the band of light around the healing hand. One single creature.

AVOID
- Not Oranguru, Ambipom, Aipom, Infernape, Mew or Alakazam. Not a gibbon or a human; no clothing.
- No plush toy, chibi, Neopets or mascot look; no oversized sparkly eyes.
```

## Ronde 2 (prompt v3) → basis: `basis_r2.png`
Jordi (8 nov): "beter, ik ben wel fan van de maanvorm. Kleuren van de handen en voeten zijn wel wat willekeurig nu en de tak zit nog steeds niet in de staart, is denk ik niet mogelijk? het patroon op de rug lijkt wel willekeurig, deze maanvorm die uitsteekt op het hoofd ben ik wel fan van, laten we kijken of we een verbeterprompt kunnen doen. Ogen mogen ook groter"

### Verbeterprompt (in hetzelfde gesprek)
```
This is much better. Keep everything as it is (pose, silhouette, head shape, the crescent moon sticking out of the head, colors of the fur), and change only these four things:

1. HANDS AND FEET: their colors look random now (one pink, one silver, one grey). Give both hands and both feet the same color, so they clearly belong together. The healing hand keeps its turquoise band of light.
2. TWIG: the twig is floating next to the tail. The tail must actually HOLD it: the very tip of the tail at the centre of the spiral curls tightly around the twig, like a monkey's prehensile tail gripping a branch. The twig touches and is wrapped by the tail, it does not float.
3. BACK PATTERN: the light patches on the back look random. Replace them with one clear, deliberate pattern that follows the shape of the body, like the patterns on official Pokémon. No random blotches.
4. EYES: make the eyes a bit bigger, still turquoise, neutral and calm.

Same 64x64 Gen 3 sprite style, white background, nothing else changed.
```

## Ronde 3 (verbeterprompt) → `basis_r3.png`
Jordi (8 nov): "De tak mag helemaal eruit, de ogen zijn nog te klein en het patroon op de rug is vaag, kunnen we niet meerdere crescent moons doen? of 1 maan achtig patroon?" → takje en cocabladeren vervallen. Twee varianten:

### Verbeterprompt A: meerdere sikkels
```
Good. Keep everything as it is (pose, silhouette, head, the crescent moon on the head, hands, feet, colors), and change only these three things:

1. Remove the twig and leaves completely. The tail ends in the clean spiral only.
2. Make the eyes clearly bigger than now, still turquoise, neutral and calm.
3. Replace the vague back pattern with a few crescent moons (white, the same style as the moon on the head) in a row along the back, following the shape of the body. Crisp shapes with a clear outline, not blurry.

Same 64x64 Gen 3 sprite style, white background, nothing else changed.
```

### Verbeterprompt B: één maanpatroon
```
Good. Keep everything as it is (pose, silhouette, head, the crescent moon on the head, hands, feet, colors), and change only these three things:

1. Remove the twig and leaves completely. The tail ends in the clean spiral only.
2. Make the eyes clearly bigger than now, still turquoise, neutral and calm.
3. Replace the vague back pattern with one large moon-like pattern on the back (white, the same style as the moon on the head), following the shape of the body. A crisp shape with a clear outline, not blurry.

Same 64x64 Gen 3 sprite style, white background, nothing else changed.
```

## Ronde 4 (verbeterprompt A) → **gekozen: `gekozen_r4.png`**
Jordi (8 nov): "beide maanpatronen kan die niet goed, maar ik moet zeggen, ik ben nu eigenlijk met alles tevreden behalve rugpatroon en ogen, maar dat zijn dingen die jij prima kan fixen denk ik. Hij is wat te vrolijk qua gelaat/ogen, dat moet neutraler, het rugpatroon mag je deze type bogen gebruiken, maar dan ongeveer als het origineel, 3 die meeschalen met de vorm van de rug, kan je dat? voor de rest de sprite volledig overnemen"
→ Sprite: `../gemini_sprite/` (onderlaag `grid128.png` = Gemini-pixelraster 128×128, `s64.npy` = 2× verkleind).
