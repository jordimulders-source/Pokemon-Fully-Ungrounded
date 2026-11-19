# Gemini-prompt: Moonkey opknappen (19 nov)

Jordi (19 nov, letterlijk): "ook prima model en design, maar iets betere pose." · "driekwart hoek en iets meer kloppend qua perspectief".
Design = bevroren (`../af/nachtaap_evo.png`). Les van Nocticue: een echte Gen 3-sprite als hoekvoorbeeld werkt beter dan graden; bij driekwart naar links staat het verre oog/oor/ledemaat links.

## Bijlagen
1. `bijlage1_huidige_sprite_8x.png`: huidige sprite (design, kleuren, kenmerken, pose).
2. `bijlage2_hoek_persian_8x.png`: Persian (Gen 3), laag gehurkte viervoeter in driekwart naar links, kop naar de kijker, staart omhoog achter het lijf: alleen voor hoek en perspectief.

## Prompt v1 (nieuw gesprek, bijlagen 1 en 2)
```
Draw an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art) of the Pokémon in attachment 1.

TWO ATTACHMENTS, EACH FOR ONE THING
- Attachment 1 = the DESIGN and the POSE. Same creature, colors, proportions and features; this is final. Keep the pose: crouched low on four limbs, head low in front, the back higher behind the head, tail raised high and ending in a spiral, eyes looking straight at the viewer.
- Attachment 2 = ONLY the CAMERA ANGLE and PERSPECTIVE. This is an official Gen 3 sprite (Persian) in a classic 3/4 view facing left: the body turned about 40 degrees, the near legs in front and lower, the far legs higher and partly hidden behind the body, the head turned towards the viewer. Use this angle and perspective. Do not take anything else from it: no cat, no coin, no whiskers, no colors.

THE PROBLEM WITH ATTACHMENT 1
- It is not a real 3/4 view and the perspective does not add up: the body is almost a side view while the head is a flat front view, and the four feet stand on one line. Make head, body and limbs belong to one 3D creature seen from the same 3/4 angle.

THE CREATURE (keep all of this)
- Night monkey (owl monkey, Aotus), Psychic type: small round head on a big round body, long arms and legs, long fingers with cream tips.
- Dark violet fur, a lighter pale-blue pattern of three tapering wedges on the back, centered on the spine.
- On the head: one big white crescent moon, points down, covering the upper half of the face and falling over the eyes. No other white on the head.
- Big round red eyes with a dark ring around them and a dark pupil, staring at the viewer. Small neutral mouth, no smile.
- Small round ears.
- Tail raised high behind the body, ending in a spiral curl.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean Gen 3 shading. Plain white background, no branch, no ground, no shadow, no effects. One single creature.

AVOID
- No new pose, no smile, no Aipom or Ambipom look, no Persian features, no plush toy or mascot look.
```

## Rondes
Jordi (19 nov, vóór r1): "ja de poten en de rugpositie zijn niet geweldig".
### Ronde 1 (prompt v1) → `r1_prompt_v1.png`
Jordi: "nee er is teveel aan het design gezeten nu".
Claude: maan werd een kleine C i.p.v. de grote sikkel over de ogen, ogen hoekig, kop kleiner, lijf lang en dun (geen groot bol lijf), poten lang. Wel: verre poten achter/hoger, lijf in driekwart.
Jordi: "zonder persian is het beter".

## Prompt v2 (nieuw gesprek, alleen bijlage 1)
```
Redraw this exact Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), in a better 3/4 view.

The DESIGN is final: keep it exactly as in the attachment. Same head (shape, size, the big white crescent moon with points down covering the upper half of the face and falling over the eyes, the big round red eyes with dark rings, the small neutral mouth, the small round ears), same big round body, same proportions between head and body, same pale-blue wedges on the back, same cream fingertips, same tail with the spiral, same colors.

Change ONLY the angle and the perspective:
- Now the body is almost a side view, the head a flat front view, and the four feet stand on one straight line. Turn the whole creature into one consistent 3/4 view facing left.
- The legs and the back must follow that same perspective: the near front leg and near hind leg in front and lower, the far front leg and far hind leg higher and partly hidden behind the body. The back is one round, consistent shape in 3/4, rising behind the head as now.
- The head still faces the viewer and the eyes stare straight at us.

Same 64x64 Gen 3 style, max 16 colors, 1 px dark outline, light from top left. Plain white background, no ground, no shadow, no effects.

AVOID: no new design, no smaller moon, no square eyes, no thin or long body, no long legs, no smile, no Aipom look.
```

### Ronde 2 (prompt v2) → `r2_prompt_v2.png`, vergelijking `vergelijk_r2.png` (huidig | r2)
Jordi (19 nov): "wat vind jij?"
Claude: design bleef (kop, ogen, lijf, wiggen, staart); poten iets beter gespreid, maar de voeten staan nog bijna op één lijn en het lijf is nog bijna profiel, dus het perspectief is maar een beetje beter. De maan verliest zijn sikkelpunten (onderrand recht, leest als een witte kap).

### Verbeterprompt r3 (in hetzelfde gesprek)
```
Good, the design is right. Keep head, eyes, body, wedges, tail and colors exactly as they are. Fix only these two things:

1. PERSPECTIVE OF THE FEET: the four feet still stand almost on one line. In a 3/4 view the far legs stand further back: put the far front foot and the far hind foot clearly higher in the image (about 4-6 pixels higher than the near feet) and partly behind the body. The near front foot is the lowest and most to the front.
2. MOON: keep the big white crescent, but make its lower edge curve so the two points clearly point down at the sides of the eyes, like a crescent moon. Same size.

Nothing else changed.
```

### Ronde 3 (verbeterprompt r3) → `r3_verbeter.png`, vergelijking `vergelijk_r3.png` (huidig | r2 | r3)
Jordi (19 nov): "negeer de maanvorm, die fixen we zelf, hoe is de lichaamspose?"
Claude: lichaamspose r3 is de beste van de drie: achterpoot hoger en verder weg geeft eindelijk diepte, nabije voorpoot laagst vooraan, verre voorpoot piept ertussen. Zwak: achterpoot leest wat als blok (geen dij), voet zweeft licht. Let op: door de maan zijn de ogen half afgedekt en kijken ze boos; ogen uit r2/oude sprite halen.
