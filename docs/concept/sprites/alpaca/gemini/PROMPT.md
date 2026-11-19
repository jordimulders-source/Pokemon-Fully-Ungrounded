# Gemini-prompt: Palpaca opknappen (19 nov)

Opknapronde (`../../OPKNAPRONDE_GEMINI.md`). Huidige sprite: `../ronde17/variant_kop/anim_front.png`.

## Jordi (19 nov, letterlijk)
- "palpaca heeft bijv nog steeds een beetje een gek aangezicht, daar gaat het mij vooral om"
- "Belangrijk hierin is dat de sprite moet zijn zoals een alpaca in het echt loopt, dat is anders dan een paard doet toch? Het design moet zo blijven alleen de pose moet natuurlijker, de hoek moet natuurlijker, hij moet netter"

## Wat Claude ziet in de huidige sprite
- Gezicht: de snuit staat in zijprofiel naar links, maar het oog staat ver naar rechts op de kop alsof die naar de kijker kijkt; de twee hoeken vechten. Snuit is een lege vlek (geen neusje/mond).
- Hoek: lijf in zuiver zijaanzicht, kop half gedraaid; geen echte driekwart.
- Pose: beide handschoenen op dezelfde hoogte los onder het lijf, achterpoten dunne stokjes; leest als een stijve stoel.

## Alpaca lopen (vs. paard)
- Kameelachtigen (alpaca, lama) lopen in **telgang**: beide poten aan dezelfde kant gaan tegelijk naar voren. Een paard draaft diagonaal (linksvoor + rechtsachter).
- Nek bijna rechtop, kop hoog en horizontaal, oren rechtop; poten vrij recht onder het lijf; zachte voeten met twee tenen (geen hoeven); korte staart.

## Bijlage
1. `bijlage1_huidige_sprite_8x.png`: de huidige sprite (frame 1, 8×).

## Prompt v1
```
Redraw this Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), with a more natural pose and angle.

ATTACHMENT
- The attachment is the current sprite. The DESIGN is final and must stay exactly the same: same creature, same proportions, same colors, same features. Do not add, remove or reinterpret anything.
- Use it only for the design. It is an old, clumsy sprite: do NOT trace its pose, angle or face. Its problems:
  1. The face is confused: the snout is in side view pointing left, but the eye sits far to the right as if the head faces the viewer. The snout is an empty blob without nose or mouth.
  2. The body is in pure side view while the head is half turned, so the angle is unnatural.
  3. The legs are stiff like a chair: both boxing gloves hang at the same height under the body and the hind legs are thin sticks.

THE CREATURE (keep all of this)
- Fighting-type alpaca, cute and fluffy but a fighter.
- Cream-white fluffy wool body, fluffy tail held up.
- Head with a woolly topknot, two upright pointed ears with small red wool tassels.
- A woven collar in Andean colors (pink, teal, yellow) around the neck.
- The two front feet are wrapped in big red woolly boxing gloves with a colorful woven cuff. The hind legs are normal cream legs.

POSE: WALKING LIKE A REAL ALPACA
- Alpacas walk with a PACING gait, unlike a horse: the front and hind leg on the SAME side move forward together. So the near front leg (glove) and near hind leg are both stepping forward, while the far front leg and far hind leg are both back.
- Neck held almost upright, head high and level, ears up, alert and a bit cocky. Legs fairly straight under the body, soft padded feet, no hooves.

ANGLE
- A real 3/4 view facing front-left: the body turned about 30-45 degrees towards the viewer, so we see the chest and the near side.
- The head is turned a bit further towards the viewer (about 45-60 degrees): the snout points front-left, the near eye clearly visible and placed where it belongs on a 3/4 head, the far eye partly visible. Small nose and mouth on the snout.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise.
- Plain white background. No ground, shadow or base. No effects. One single creature.

AVOID
- Not a horse, not a lamb, not a llama. No plush toy, chibi or mascot look, no oversized sparkly eyes.
```
