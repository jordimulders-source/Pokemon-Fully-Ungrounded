# Gemini-prompt: Nocticue opknappen (19 nov)

Jordi (19 nov, letterlijk): "Laten we Nocticue nog wat oppoetsen, belangrijk, ik ben echt fan van het design, dus het is puur de pose. De cuteness moet niet weg" · "ook de positie van zijn armen" · "dus puur de hoek".

Design = bevroren (`../ronde12/variant_spiraal/anim_front.png`, goedgekeurd 23 okt). Alleen de hoek verandert (lijf en armen); kleuren, kenmerken, verhoudingen en de schattigheid blijven.

## Bijlagen
1. `bijlage1_huidige_sprite_8x.png`: huidige sprite (design, kleuren, kenmerken).

## Prompt v1
```
Redraw this Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), now in a proper 3/4 view.

ATTACHMENT
- Attachment 1 is the current sprite. The DESIGN is final and must stay exactly the same: same creature, same proportions, same colors, same features, same cute look. Do not add, remove or reinterpret anything.
- The only problem: it stands perfectly straight-on and symmetrical, which looks flat and 2D. Change ONLY the angle: rotate the body and the arms about 30-45 degrees, into a real 3/4 view facing left, with volume, like an official Game Freak sprite. The arms follow the new angle (near arm in front, far arm partly behind the body).

THE CREATURE (keep all of this)
- Baby night monkey (owl monkey, Aotus) with tarsier proportions: a very big round head and a small body. Psychic type.
- Violet fur. A cream face disc with a violet stripe running from the top of the head down between the eyes.
- Very big pink-magenta eyes with dark pupils, exactly as in the attachment: mysterious but cute, not sleepy, not bored.
- Small round ears on the sides of the head with cream insides. Small cream muzzle, tiny mouth.
- Cream chest and belly.
- Sitting on the ground, knees up in front, small cream hands and feet.
- A thin violet tail that rises behind the body and ends in a small spiral curl (like the Nazca monkey geoglyph).
- The cuteness must stay: same big head, same big eyes, same soft expression.

3/4 VIEW
- Body and arms turned about 30-45 degrees towards the front-left.
- The head turns along with the body but keeps looking at the viewer: both eyes clearly visible, the far eye a little narrower.
- Exactly two arms and two legs; near arm and leg in front, far arm and leg partly hidden. The tail curl peeks out behind the body on the right.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise.
- Plain white background. No ground, rock, shadow or base. No glow, sparkles or psychic effects. One single creature.

AVOID
- Not Aipom, Ambipom, Mew, Espeon or a lemur. No plush toy, no Neopets or mascot look, no oversized sparkly anime eyes, no new accessories.
```

## Rondes
### Ronde 1 (prompt v1) → `r1_prompt_v1.png`
Jordi (19 nov): "hij heeft de hele pose aangepast".
Claude: Gemini heeft een nieuwe pose bedacht (nabije arm reikt naar voren, ander zitten) en de kop staat nog bijna recht van voren. Jordi: "en hij moet niet glimlachen" · "het gelaat was goed" · "eigenlijk was alles prima, behalve de hoek en wat details in het spritewerk" (het gezicht van de huidige sprite blijft). Les: "rotate the body and the arms" las Gemini als "nieuwe pose". In v2 eerst de huidige pose in woorden vastleggen en de draai als een beeldje op een draaischijf beschrijven. Nieuw gesprek.

## Prompt v2 (nieuw gesprek, alleen bijlage 1)
```
Redraw this exact Pokémon sprite from a different camera angle, as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

Think of attachment 1 as a small figurine on a turntable. Do NOT change its pose. Only turn the turntable about 30-40 degrees, so we see the same figurine in a 3/4 view facing left. Nothing moves relative to the body: no limb is lifted, stretched, bent differently or moved.

THE POSE (keep exactly)
- Sitting upright, compact and round.
- Both arms hang straight down along the sides of the body, close to the body. Both hands rest on the ground next to the feet. No arm reaches out.
- Knees up together in front of the belly, small cream feet on the ground.
- Head upright on top of the body, looking straight at the viewer.
- Thin violet tail rises from behind the hip and ends in a small spiral curl.

WHAT CHANGES WITH THE ROTATION
- Body, head, arms and legs all turn together by the same 30-40 degrees towards the front-left.
- We now see the left side of the body a bit more: the near arm (viewer's left) is fully visible along the side, the far arm (viewer's right) is partly hidden behind the belly.
- The face disc and eyes shift a little to the left on the head; the far eye is a bit narrower than the near eye; the near ear is smaller, the far ear sticks out more.
- The tail curl peeks out behind the body on the right.

KEEP (design is final)
- Same creature, same proportions (very big round head, small body), same colors, same features, same big pink-magenta eyes.
- The face stays exactly as in attachment 1: same calm, slightly mysterious expression. NOT smiling: the mouth is a tiny neutral mark under the small cream muzzle, as in the attachment.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean Gen 3 shading. Plain white background, no ground, no shadow, no effects.

AVOID
- No new pose, no reaching or waving arm, no smile, no new facial expression, no plush toy or mascot look, no oversized sparkly anime eyes.
```

### Ronde 2 (prompt v2) → `r2_prompt_v2.png`
Jordi (19 nov): "iets beter maar nog niet perfect, hij kijkt niet echt driekwart he. De pose is wel goed, staart nog niet. Het rechteroog mag ronder, dat was een van de dingen die in de originele sprite niet perfect zijn".
Claude: de kop staat tussen recht en profiel in zonder dat het klopt (snuit en streep schuiven naar links, maar het rechteroog is het grootste); de staart is dik geworden met een grote krul naast de kop.

### Verbeterprompt r3 (in hetzelfde gesprek)
```
Better, the pose is good now. Keep the body, arms, legs, colors and face expression exactly as they are. Fix only these three things:

1. ANGLE: it does not read as a real 3/4 view yet. Turn the head and body together about 35-40 degrees from the front, towards the left. Then the face disc, the stripe and the muzzle sit in the left half of the head, the near (left) eye is fully visible, the far (right) eye is a bit narrower because it turns away, and more of the round back of the head shows on the right.
2. RIGHT EYE: make it rounder. Both eyes are round shapes, no flat or angular top.
3. TAIL: back to a thin tail (2-3 pixels wide), as in the first attachment: it starts behind the hip on the right, rises next to the body and ends in a small spiral curl at about ear height, a little away from the head. Not thick, no big curl.

Same 64x64 Gen 3 sprite style, white background, nothing else changed.
```
