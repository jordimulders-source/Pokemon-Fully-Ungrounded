# Gemini-prompt: Vigiloot opknappen (19 nov)

Jordi (19 nov, letterlijk): "Laten we vigiloot nog wat verbeteren. De enige referentie afbeelding wordt de sprite die we al hebben. Hij is al heel ver, maar mag gewoon wat meer opgepoetst worden. Ik wil het model verder niet veranderen, het design concept, dat is goed, maar puur afwerking, zoals we ook met nocticue deden bijv. Pose is ook al grotendeels goed, is iig driekwart"

Design = bevroren (`../af/wasbeer.png`, goedgekeurd 3 nov; kenmerken in `../SPEC.md`). Alleen afwerking.

## Bijlagen
1. `bijlage1_huidige_sprite_8x.png`: huidige sprite (enige referentie).

## Prompt v1
```
Redraw this Pokémon as a clean, polished official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

ATTACHMENT
- Attachment 1 is the current sprite. The DESIGN and the POSE are final: same creature, same proportions, same colors, same features, same 3/4 view facing left, same sneaking pose. Do not add, remove or reinterpret anything.
- What it needs is only finishing: it was made from a rough 3D render and still has small inconsistencies and messy pixel work. Redraw it the way a Game Freak artist would finish it: clean shapes, clear volume, consistent shading.

THE CREATURE (keep all of this)
- Dark-type raccoon (crab-eating raccoon), the final form of a starter line. Warm grey-brown fur.
- Black mask over the eyes in two lobes with a bridge over the nose, white eyebrow arcs above it, white muzzle, round dark nose. Red eyes with a pupil. Small round ears with light inner fur.
- Sneaking forward on two legs, body leaning forward: near leg far back on its toes, far leg planted in front. Dark lower legs and feet.
- Cream hands with two big claws each, the claw tips shaped like a crowbar with a notch. One hand in front of the chest, the other reaching down-forward on the left.
- A red-brown sack on its back as a thief's bag, with its opening.
- A ringed tail (dark brown and cream rings) that curves up behind the body and ends in a hook, with air inside the bend.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading with large calm areas like official Gen 3 sprites, no noise, no random spots.
- Plain white background. No ground, rock, shadow or base. No effects. One single creature.

AVOID
- No new pose, no new expression, no standing fully upright, no clothes or Robin Hood costume. Not Zangoose, Sneasel, Weavile, Thievul or Obstagoon. No plush toy or mascot look.
```

## Rondes
### Ronde 1 (prompt v1) → `r1_prompt_v1.png`
Jordi (19 nov): "hij maakt er geen sprite van, moet je even beter benadrukken". (Gemini gaf een gladde illustratie met lijnwerk.)

## Prompt v2 (nieuw gesprek, alleen bijlage 1)
Zelfde als v1, maar met een openingsblok dat pixel art eist en een AVOID-regel tegen illustratie.
```
OUTPUT MUST BE PIXEL ART: a 64x64 pixel game sprite, drawn on a visible pixel grid, enlarged with hard square pixels (nearest neighbour). NOT an illustration, NOT a drawing, NOT anime/cartoon art, NOT vector art, no smooth lines, no anti-aliasing, no gradients. Exactly like the attachment: a Game Boy Advance sprite from Pokémon Ruby/Sapphire/Emerald.

Redraw this Pokémon as a clean, polished official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art), in the same pixel resolution as the attachment.

ATTACHMENT
- Attachment 1 is the current sprite. The DESIGN and the POSE are final: same creature, same proportions, same colors, same features, same 3/4 view facing left, same sneaking pose. Do not add, remove or reinterpret anything.
- What it needs is only finishing: it was made from a rough 3D render and still has small inconsistencies and messy pixel work. Redraw it the way a Game Freak pixel artist would finish the sprite: clean pixel shapes, clear volume, consistent shading.

THE CREATURE (keep all of this)
- Dark-type raccoon (crab-eating raccoon), the final form of a starter line. Warm grey-brown fur.
- Black mask over the eyes in two lobes with a bridge over the nose, white eyebrow arcs above it, white muzzle, round dark nose. Red eyes with a pupil. Small round ears with light inner fur.
- Sneaking forward on two legs, body leaning forward: near leg far back on its toes, far leg planted in front. Dark lower legs and feet.
- Cream hands with two big claws each, the claw tips shaped like a crowbar with a notch. One hand in front of the chest, the other reaching down-forward on the left.
- A red-brown sack on its back as a thief's bag, with its opening.
- A ringed tail (dark brown and cream rings) that curves up behind the body and ends in a hook, with air inside the bend.

STYLE AND FORMAT
- 64x64 pixels, max 16 colors, 1 px dark outline, light from top left, clean pixel shading with large calm areas like official Gen 3 sprites, no dithering noise, no random spots.
- Plain white background. No ground, rock, shadow or base. No effects. One single creature.

AVOID
- No illustration, no smooth line art, no high resolution, no anime or cartoon rendering: pixel art only.
- No new pose, no new expression, no standing fully upright, no clothes or Robin Hood costume. Not Zangoose, Sneasel, Weavile, Thievul or Obstagoon. No plush toy or mascot look.
```

### Ronde 2 (prompt v2) → `r2_prompt_v2.png`, vergelijking `vergelijk_huidig_r1_r2.png` (huidig · r1 · r2)
Jordi (19 nov): "hij erandert niet echt iets he? Kan je eens kijken hoe we dit in andere gesprekken deden?"
Claude: r2 trekt de oude sprite over (les GEMINI.md: bijlage + "keep" = kopie). In de andere gesprekken (Palpaca r4, Nocticue r4, Hummlet) was de Gemini-uitkomst vaak een gladde tekening; die werd het **model** en de sprite bouwde Claude zelf (reductie + oud palet). De pixelvraag aan Gemini was dus niet nodig: r1 is zo'n model. Verschillen r1 t.o.v. de huidige sprite: boze blik (wenkbrauwen schuin), kop rechter op, borsthand een poot met vingers zonder koevoetklauwen, buidel dichtgeknoopt (geen zakmond), koeler grijs. Voorgelegd aan Jordi.
