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

## Ronde 1 (prompt v1) → `r1_prompt_v1.png`
Claude: netter (neus/mond, langere nek, pluimstaart), maar de oude sprite is overgetrokken: zijaanzicht, oog nog op de 3/4-plek bij een profielsnuit, handschoenen naast elkaar, geen telgang. Volgende: prompt v2 in een nieuw gesprek zonder bijlage, gang per poot beschreven ("a bit determined" bij de ogen is Claudes toevoeging, voorgelegd).
Jordi (19 nov) over "a bit determined": "nee hij moet een cute starter zijn" → weggehaald; "cute starter Pokémon" in de beschrijving.

## Prompt v2 (nieuw gesprek, geen bijlage)
```
Draw an official Gen 3 Pokémon front sprite (Ruby/Sapphire/Emerald style pixel art) of this Pokémon.

THE CREATURE
- A cute starter Pokémon: a young Fighting-type alpaca, fluffy and huggable, but a fighter.
- Cream-white fluffy wool body, a fluffy tail held up.
- Head: woolly cream topknot, two upright pointed ears with pink insides and a small red wool tassel on each ear. Short snout with a small nose and mouth. Dark eyes.
- A woven collar in Andean colors (pink, teal, yellow) around the neck.
- The two front feet are wrapped in big red woolly boxing gloves with a colorful woven cuff (pink, teal, yellow). The hind legs are normal cream legs with soft padded feet, no hooves.

POSE: WALKING LIKE A REAL ALPACA
- Caught mid-step. Alpacas walk with a PACING gait, unlike a horse: the front and hind leg on the SAME side move together.
- Near front leg (glove) reaches forward and is lifted off the ground; the near hind leg also steps forward at the same moment.
- Far front leg (glove) and far hind leg are both planted further back.
- All four legs visible. Neck almost upright, head high and level, ears up.

ANGLE
- A real 3/4 view facing front-left: the body is turned about 40 degrees towards the viewer, so we see the woolly chest from the front and the near side of the body. The far legs show partly behind the near legs.
- The head is turned about 60 degrees towards the viewer: the snout points front-left, both eyes visible (the far one partly), the face reads as one consistent 3/4 head.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise.
- Plain white background. No ground, shadow or base. No effects. One single creature.

AVOID
- Not a horse, not a lamb, not a llama. No side view. No plush toy look, no oversized sparkly eyes.
```

## Ronde 2 (prompt v2) → afbeelding niet ontvangen
Jordi (19 nov): "mijn mening is dat het gezicht beter is, maar dat de hoek nog steeds iets teveel zijaanzicht is, en misschien geinig om een van de voorpoten iets meer te heffen"
Verbeterprompt r3 (zelfde gesprek): 20-25° verder draaien + nabije handschoen heffen tot borsthoogte.

## Ronde 3 (verbeterprompt) → `r3_verbeter.png`
Jordi: "dit gaat fout". Claude: drie handschoenen (geheven poot erbij getekend i.p.v. verplaatst, zoals awki's derde vleugel) en niet gedraaid. → Prompt v3: nieuw gesprek, poten geteld.

## Prompt v3 (nieuw gesprek, geen bijlage)
Prompt v2 met: hoek 45°/70° en "no side view, no profile body"; precies vier poten, twee handschoenen, elke poot benoemd; nabije handschoen geheven tot borsthoogte, de verre handschoen op de grond.

## Ronde 4 (prompt v3) → `r4_prompt_v3.png`
Jordi (19 nov): "Prima denk ik maar het is nu geen sprite meer". Claude: illustratie i.p.v. pixelart; mogelijk model (sprite dan zelf bouwen: reductie + oud palet, zoals Hummlet). Nabije voorpoot geheven + verre achterpoot naar voren = diagonaal (paardengang), voorgelegd.

## Ronde 5 (pixelart-verzoek, zelfde gesprek) → `r5_pixel_verzoek.png`
Jordi: "vrijwel hetzelfde" (Gemini voegde alleen krullen op het lijf toe). Gang: "ja dat moet wel aangepast worden, anders is het geen alpaca". → r4 blijft het model; sprite bouwt Claude zelf.
Gangfix: in r4 is de voorste achterpoot de verre (donker, achter het lijf) en de achterste de nabije. Prompt v4: nieuw gesprek, r4 als bijlage, alleen de diepte van de achterpoten omwisselen (geen poot verplaatsen). Lukt dat niet: Claude wisselt het zelf in de sprite (licht/donker + omlijning).

## Ronde 6 (gangfix, nieuw gesprek) → `r6_gangfix.png`
Jordi: "hij snapt het niet" (Gemini maakte de voorste achterpoot juist donkerder). → Claude wisselt per script in het model: voorste achterpoot krijgt de lijftint (nabij), achterste de oude donkere tint (ver): `../model/r4_gang_wissel.png`, vergelijking `../model/gang_voor_na.png`.
