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
Jordi (19 nov): "nee ik wil gewoon kleine sprite verbeteringen, gewoon dat die gepolijst wordt, tot nu toe zie ik niks wat we nieuw moeten maken, dus 1 nieuwe prompt"

## Prompt v3 (nieuw gesprek, alleen bijlage 1)
Gemini als pixelartist die een cleanup-pass doet op de sprite zelf; alleen algemene spritetechniek benoemd, geen ontwerppunten.
```
You are a professional Game Freak pixel artist. Attachment 1 is a work-in-progress Pokémon front sprite (64x64 pixel art, shown enlarged). Do a POLISH PASS on this exact sprite, the final cleanup an artist does before a sprite ships in Pokémon Ruby/Sapphire/Emerald.

WHAT STAYS (do not change)
- Same creature, design, pose, 3/4 angle, proportions, silhouette, colors and expression. Every body part stays where it is and keeps its size. Nothing added, nothing removed, nothing redrawn as a new design.

WHAT THE POLISH PASS FIXES (pixel technique only)
- Outline: one clean, continuous 1 px dark outline all around the creature, with no gaps, no double pixels and no stray pixels. Inner lines where parts overlap (arm over body, hand over chest, tail behind leg).
- Curves: jagged, stair-stepped or blocky edges become smooth pixel curves with even steps, like official sprites.
- Shading: one consistent light source from the top left, 2-3 tones per color area, clean shaded shapes that show volume (round head, body, legs, tail rings, sack). Remove noise, random dark spots and single loose pixels.
- Readability: every part reads clearly at 1x: the face (mask, eyebrows, eyes, nose, muzzle), the ears, both hands with their claws, the sack, the tail rings and the feet.

The result must look like the same sprite, but clearly cleaner and more finished. Do not return the attachment unchanged.

FORMAT
- Pixel art only: a 64x64 sprite on a visible pixel grid, enlarged with hard square pixels, exactly like the attachment. Not an illustration, no smooth line art, no anti-aliasing, no gradients. Max 16 colors.
- Plain white background, no ground, no shadow, no effects.
```

### Ronde 3 (prompt v3) → `r3_prompt_v3.png`
Jordi (19 nov): "ik zie wederom geen verschil?"
Claude: Gemini kan een bestaande pixelsprite niet oppoetsen; met de sprite als bijlage kopieert hij hem (r2, r3) of maakt hij een tekening (r1). Voorstel: Gemini stoppen, poetsronde in de sprite zelf (zoals Picapau: alleen pixels aanpassen, niets hertekenen).
Jordi (19 nov): "we moeten denk ik specifieker zijn, wat zou jij nog willen verbeteren aan deze sprite?" → Claude noemde 9 punten; Jordi: "doe allemaal maar" · "ik bedoel een prompt he" · "prompt, niet maken aub" (Claude was ten onrechte een maker gestart; gestopt).

## Prompt v4 (nieuw gesprek, alleen bijlage 1)
De 9 punten van Claude, letterlijk als lijst; de rest blijft.
```
You are a professional Game Freak pixel artist. Attachment 1 is a Pokémon front sprite (64x64 pixel art, shown enlarged). Fix the 9 specific problems below in this sprite. Everything else stays exactly as it is.

KEEP (do not change)
- Same creature, design, pose, 3/4 angle, proportions, colors and face (black mask, red eyes with pupil, white eyebrow arcs, white muzzle, round nose). Same claws with the crowbar notch, same red-brown sack. Nothing added, nothing removed.

FIX THESE 9 PROBLEMS
1. The hand in front of the chest: now a cream block with black stripes at the bottom and a dark grey blob next to it; it reads like a skull or teeth. Make it read clearly as a paw seen from the front with two big cream claws pointing down, crowbar tips with a notch, like the hand reaching down on the left.
2. Under that hand a light brown horizontal bar runs across the belly and reads like a belt. Remove the bar; the belly below the hand is plain fur.
3. Hips and thighs: the near leg and the belly are one flat grey area, so you cannot see where the leg starts. Give the thigh a clear rounded shape with a shadow line where it meets the belly. The far leg in front needs volume too. The dark lower legs get light and shadow instead of one flat tone.
4. Chest and neck have noise: loose blocks of different greys. Make them calm areas with a clear light side (top left) and shadow side, like official Gen 3 sprites.
5. The left edge of the neck and chest is a straight vertical line from the muzzle to the arm. Make it a natural curve of the throat and chest.
6. The pale stripe left of the sack is a loose line without shape. Make it a clear strap of the sack, or remove it if it is not a strap.
7. The sack is shaded in horizontal stripes. Shade it as one round, full bag: light top left, shadow bottom right, with its opening.
8. The tail: the cream rings are rectangular blocks with hard steps, so the tail looks stiff. Make the rings follow the round, bending tail, each ring a curved band, so the tail looks soft and flexible. Keep the hook at the end with air in the bend.
9. The top of the head between the ears is rather flat. Make it gently rounded.

FORMAT
- Pixel art only: a 64x64 sprite on a visible pixel grid, enlarged with hard square pixels, exactly like the attachment. Not an illustration, no smooth line art, no anti-aliasing, no gradients. Max 16 colors, 1 px dark outline, light from the top left.
- Plain white background, no ground, no shadow, no effects.
```

### Ronde 4 (prompt v4) → `r4_prompt_v4.png`
Jordi (19 nov): "ik weet niet of ik hem beter vind, ik neig ernaar dat die slechter is geworden"
Claude: beter: borsthand leest als poot, riem weg, riem van de buidel duidelijk, dij los van de buik. Slechter (ontwerp gebroken): koel grijs i.p.v. warm grijsbruin, reikende hand donker i.p.v. crème, staartringen grijs/zwart i.p.v. crème, buidel kleiner en dichtgeknoopt (zakmond weg), dijen grote platte bollen, borstklauwen klein, kop nog plat. Les GEMINI.md: te veel eisen tegelijk = fouten wisselen.
Jordi (19 nov): "wat misschien betekent dat het ontwerp gewoon prima is" · "jazeker, ik denk dat het gewoon een puike sprite was, ik kan ook niet direct benoemen wat beter moest"
**Afgesloten: `../af/wasbeer.png` blijft.**
