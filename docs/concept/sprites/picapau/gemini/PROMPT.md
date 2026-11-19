# Gemini-prompt: Picapau in driekwart (19 nov)

Jordi: "die moet gewoon driekwart staan en voor de rest precies hetzelfde." Design = bevroren (SPEC.md; B1-model "subliem").

## Bijlagen
1. `bijlage1_huidige_sprite_8x.png`: huidige sprite (kleuren, kenmerken).
2. `bijlage2_model_b1.png`: het goedgekeurde 3D-model (vorm, bolle buik, kuif).

## Prompt v1
```
Redraw this Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), now in a proper 3/4 view.

ATTACHMENTS
- Attachment 1 is the current sprite, attachment 2 is the approved 3D model. The DESIGN is final and must stay exactly the same: same creature, same proportions, same colors, same features. Do not add, remove or reinterpret anything.
- The only problem: the current sprite looks flat and 2D, almost a side view, and the perspective is wrong. Redraw it in a real 3/4 view facing left, with volume, like an official Game Freak sprite.

THE CREATURE (keep all of this)
- Electric/Flying woodpecker, based on the cream-colored woodpecker (Celeus flavus), with Pikachu colors and markings.
- Bright yellow round body; the belly is clearly round and full (like Pikachu).
- Head: yellow, a short sturdy grey chisel beak pointing up and to the left, a round black eye, a round red cheek patch.
- Crest: two pointed crest spikes on top with BLACK tips (like Pikachu's ears), plus a ragged spiky crest running down the back of the head.
- Wings closed against the body: dark brown with round cream spots.
- Tail: a stiff reddish-brown woodpecker tail pointing down and back, used as a prop.
- Short grey legs attached to the body, grey toes.
- Pose: upright and leaning slightly back, head and beak raised.

3/4 VIEW
- Body turned about 30-45 degrees towards the viewer: we see the round chest and belly from the front-left and the closed wing on the side.
- The head is turned towards the viewer too, not a profile: the far eye may just be visible or hidden behind the beak, the near eye and cheek patch clearly visible.
- Both feet visible.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise.
- Plain white background. No branch, ground, rock, shadow or base. No electricity, sparkles or effects. One single creature.

AVOID
- Not Pikipek, Pikachu, Woody Woodpecker or Chatot. No plush toy, chibi or mascot look, no oversized sparkly eyes.
```

## Ronde 1 (prompt v1) → `r1_prompt_v1.png`
Jordi (19 nov): "ziet er goed uit, behalve dat de vleugelkleur veranderd is, maar dat is geen issue, ik twijfel wel of hij weer niet hetzelfde eruit gaat zien, want het oog links zal wegvallen, hoe dan andere sprites dat? Moeten we misschien voor een leukere pose gaan?"
Studie `studie_vogels_gen3.png`: profielkop met één oog is gewoon in Gen 3 (Taillow, Swellow, Spearow, Chatot, Pikipek); de diepte zit dan in het lijf. Kop naar de kijker met twee ogen: Pidgey, Starly, Torchic, Hoothoot.
Jordi (19 nov): "nee prima, laten we hem nog een beetje naar de kijker draaien, kan met een korte verbeterprompt wel toch? Praat tegen Gemini in graden"

### Verbeterprompt r2 (in hetzelfde gesprek)
```
Good, keep everything exactly as it is (design, colors, crest, wings closed, tail, legs, style). Change only the angle:

- Right now the bird is almost in side view: about 10-15 degrees from a pure profile. Rotate the whole bird about 30 degrees more towards the viewer, so the body is at about 45 degrees (a true 3/4 view, facing front-left). We see more of the round yellow chest and belly from the front.
- Turn the head a bit further than the body, to about 60 degrees, so it looks more at the viewer: both eyes and both red cheeks are visible, the far ones partly. The beak points front-left, slightly up.
- The far wing and the tail may peek out behind the body.

Same 64x64 Gen 3 sprite style, white background, nothing else changed.
```
