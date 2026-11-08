# Gemini-prompt: Hitmontop-evolutie (capoeira), startprompt v1 (7 nov)

Regels: `docs/lessen/GEMINI.md`. Nieuw gesprek (Gemini weigerde verdere bewerkingen van pose v3).

## Jordi (7 nov, letterlijk)
"ik wil dat die geen shirt heeft, en dat de broek gele en groene strepen hebben als patroon. er zit zon typisch capoeira touwtje aan de broek en ik wil dat zijn armen een soort van muay thai banden hebben, maar dan meer capoeira mode"

## Bijlagen (in deze volgorde)
1. `bijlage1_hoofd.webp` (= `../referenties/hoofd_gemini_concept.webp`): het goedgekeurde hoofd.
2. `bijlage2_pose.png` (= `../referenties/model_gemini_pose_v3.png`): de pose.

## Nog open (Jordi kiest vóór het plakken; vul in op de plek van [...])
- Grondkleur van de broek: [WHITE / BLUE] (model v3 wit, SPEC blauw).
- Kleur van het capoeira-koord (cordão): [...].

## Prompt

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

It is a new evolution of Hitmontop, based on capoeira (Hitmontop's Japanese name already refers to capoeira). It must clearly read as a member of the Hitmon family: smooth brown skin, round ball hands, simple shapes. It is a Pokémon, not a human.

PROPORTIONS (most important)
- It stays a Hitmon, not a human. Think of Hitmontop, Hitmonchan and Tyrogue: a big head, big round hands and big feet, connected by thin, simple limbs.
- The head is the biggest single shape of the body, at least as wide as the torso.
- Each hand is a big round ball, about half the width of the head and about three times as thick as the arm.
- Each foot is about as big as a hand and about three times as thick as the leg.
- Arms and legs are thin, smooth tubes of even thickness: no muscles, no visible elbows or knees, no human joints. The legs may be long, but they stay thin.
- The torso is a simple, smooth, rounded shape, no human anatomy.
- If in doubt: make the head, hands and feet bigger and the arms and legs thinner.

ATTACHMENTS
- Attachment 1 is the approved HEAD. Copy it exactly: Hitmontop's head shape, the V-shaped line between the eyes pulled back over the head, all the "hair" combed back into a round bun with a white band (like its hands with wristbands), a smaller horn on top. Hair, horn and head are one material and one color (the same brown as the skin), no separate hair color. Eyes are black circles with one white dot. Mouth is one short line. No eyebrows, no nose, no ears.
- Attachment 2 is the POSE. Copy it exactly: a one-arm handstand, the support arm straight down with a round hand on the floor, the body tilted, the head low next to the support arm looking at the viewer, the legs spread wide in a V-split up into the air, the free arm bent across the hip. Blue feet with white claws at the ends of the legs.

CHANGES TO THE BODY (only these)
- NO shirt: the torso is bare brown skin, smooth and simple like Hitmontop's arms. No muscles, no chest or shoulder blade anatomy, no nipples or belly button.
- Long, tight trousers in [WHITE / BLUE] with a pattern of BROAD yellow and green stripes (few, wide stripes that stay readable at 64x64 pixels, not thin pinstripes).
- A typical capoeira cord (cordão) tied around the waist of the trousers, [COLOR], knotted at the side with the two ends hanging down.
- On the upper arms: armbands like Muay Thai prajiad, but in capoeira style, made of the same braided cord as the waist cord, tied around the upper arm with a short hanging end.
- Keep everything else from the attachments.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO floor, rock, shadow, base, motion lines, glow or effects. One single creature, no extra views.

AVOID
- No human body, no realistic muscles, no human face; not a person in a costume.
- No human proportions: no small head on a long body, no small human hands or fingers, no human feet, no thick muscular arms or legs.
- No shirt, vest, tank top or jacket. No shoes, no hat, no headband.
- Not Hitmonchan, Hitmonlee or Machop. No plush toy, chibi or mascot look.
```

## Tips
- Bijsturen hooguit 1–2 keer met één zin, bijv. `same design, make the stripes wider and fewer`.
- Daarna een nieuw gesprek met de beste versie als bijlage: `Use the attached image as the base design. Keep its pose, proportions and colors. Change only: ...`
- Rondes en Jordi's keuze vastleggen in `README.md` hier; gekozen ontwerp als `../referenties/gemini_gekozen_capoeira.png`.

Jordi (7 nov): "belangrijk is dat die echt hitmon blijft en dus niet mens, dus verhoudingen van hoofd, handen en voeten zijn groter dan de benen en armen" (blok PROPORTIONS en AVOID-regel; stickman met grotere kop, handen en voeten). Jordi: "nee dat zit hem vooral in prompting, dus schrijf dat goed in de prompt".

## Variant B (aanbevolen): hoofd + stickman, pose beschreven
Jordi: "misschien kunnen we daar meer een stickman van maken [...] of misschien kan jij het heel goed beschrijven". Bijlagen: 1 = `bijlage1_hoofd.webp`, 2 = `bijlage2_stickman.png` (schone stickman van pose v3: kop = cirkel, handen/voeten = rondjes). Vervang ATTACHMENTS door het blok hieronder en voeg na de eerste ATTACHMENT-regels toe: `- Attachment 2 is a stick figure that shows only the POSE (big circle = head, small circles = hands and feet, grey line = floor). Follow the pose, not the drawing style.` Werkt Gemini ook zonder stickman: alleen bijlage 1.

### Oorspronkelijk: alleen het hoofd als bijlage (als Gemini weigert)
Jordi (7 nov): "ik ben wel bang dat de hitmontop in die pose ervoor kan zorgen dat die weigert het te bouwen". Dan alleen `bijlage1_hoofd.webp` meesturen en in de prompt het blok ATTACHMENTS vervangen door:

```
ATTACHMENT
- The attached image is the approved HEAD. Copy it exactly: Hitmontop's head shape, the V-shaped line between the eyes pulled back over the head, all the "hair" combed back into a round bun with a white band (like its hands with wristbands), a smaller horn on top. Hair, horn and head are one material and one color (the same brown as the skin), no separate hair color. Eyes are black circles with one white dot. Mouth is one short line. No eyebrows, no nose, no ears.
- Ignore the body in the attachment; draw the body and pose as described below.

POSE
- A one-arm handstand, frozen in the middle of a capoeira move: the support arm straight down, the round hand flat on the floor.
- The body tilted about 45 degrees, the hips are the highest point of the torso.
- The head low, next to the support arm, upright enough to read, looking at the viewer.
- The legs spread wide in a V-split up into the air, one leg to the upper left, one to the upper right; these are the two highest points of the silhouette. Blue feet with white claws at the ends.
- The free arm bent across the hip.
- Silhouette like an upside-down triangle: wide at the top, a narrow point at the bottom (the hand).
```

## Startprompt v2 (7 nov, nieuw gesprek)
Jordi: "de broek mag ook echt minder een broek zijn en gewoon meer de benen met kleur".
Bijlagen: 1 = `ronde1.png` (ontwerp), 2 = `bijlage2_stickman.png` (pose). Weigert of negeert hij de stickman: bijlage 2 = `bijlage2_pose.png` (model v3).

```
Use attachment 1 as the base design. Keep EXACTLY its design: the head (V line pulled back, round bun with a white band, small horn, black eyes with a white dot, one short mouth line), the big round hands, the big blue clawed feet, the thin smooth brown limbs, the bare brown torso, the yellow capoeira cord around the waist, the yellow cord armbands.

Change the trousers: they should be much less like trousers. The legs themselves are colored white with the broad yellow and green stripes, as if it is the color of the legs: thin, smooth and tight like the bare brown arms, no loose fabric, no folds, no flared or wide parts, no hems. The waist cord stays. Keep its Hitmon proportions: big head, big hands, big feet, thin arms and legs. Keep the Gen 3 sprite style, white background, no floor or shadow.

Change the pose. Attachment 2 shows the pose as a stick figure (big circle = head, small circles = hands and feet, grey line = floor). In attachment 1 the body hangs straight upside down; that is wrong. The correct pose, a frozen one-arm handstand from capoeira:
- The support arm is a straight vertical line from the hand on the floor up to the shoulder. The shoulder is at the top of this arm, NOT under the head.
- From the shoulder the torso goes diagonally UP and to the RIGHT, at about 45 degrees. The hips are the highest point of the torso, upper right.
- The head hangs LOW, to the LEFT of the support arm, at about the middle height of the arm, on a short neck from the shoulder, face towards the viewer.
- From the hips the legs open in a wide V-split: one leg crosses up and to the far upper left, the other goes up to the upper right. The two feet are the highest points of the sprite.
- The free arm comes out of the same shoulder, bends at the elbow, and its round hand rests on the hip at the upper right. It does not stick out sideways and is not hidden.
- Both upper arms have the yellow cord armband.
- Silhouette: an upside-down triangle, wide at the top (the feet), a narrow point at the bottom (the hand on the floor).

AVOID: baggy or wide trousers, a straight vertical upside-down body, the head directly under the hips, an arm coming out of the chin or neck, human proportions, a shirt, a floor or shadow.
```

## Startprompt v3 (7 nov, nieuw gesprek)
Waarom: met ronde 1 als basisontwerp kopieert Gemini dat plaatje (ook de verkeerde pose); de stickman leest hij niet. Nu: het hele ontwerp in woorden, en als posebron het 3D-model, dat de schuine romp wél laat zien.
Bijlagen: 1 = `bijlage1_hoofd.webp`, 2 = `bijlage2_pose.png` (model v3). Weigert hij: bijlage 2 weglaten (de tekst beschrijft de pose).

```
Draw an original Pokémon as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art): a new evolution of Hitmontop, based on capoeira. It is a Pokémon of the Hitmon family, not a human.

ATTACHMENTS
- Attachment 2 is a 3D model of this Pokémon. Use it for the POSE: copy the pose exactly, including the 45 degree tilted torso. Redraw it as a Gen 3 sprite with the changes listed below.
- Attachment 1 is the approved HEAD. Use it for the head: Hitmontop's head shape, the V-shaped line between the eyes pulled back over the head, the "hair" combed back into a round bun with a white band, a smaller horn on top. Head, hair and horn are one material and one color (the same brown as the skin). Black circle eyes with one white dot, one short mouth line, no eyebrows, no nose, no ears.

POSE (as in attachment 2)
- A frozen one-arm handstand. The support arm is a straight vertical line from the round hand on the floor up to the shoulder.
- From the shoulder the torso goes diagonally UP and to the RIGHT, about 45 degrees; the hips are the highest point of the torso.
- The head hangs LOW, to the LEFT of the support arm, face towards the viewer.
- From the hips the legs open in a wide V-split to the upper left and upper right; the feet are the highest points.
- The free arm bends at the elbow and its round hand rests on the hip.
- NOT a straight vertical upside-down body, NOT the head directly under the hips.

PROPORTIONS (most important)
- Hitmon proportions, like Hitmontop, Hitmonchan and Tyrogue: a big head, big round hands and big feet, connected by thin, simple limbs.
- The head is the biggest single shape, at least as wide as the torso. Each hand is a big ball, about half the width of the head and about three times as thick as the arm. Each foot is about as big as a hand.
- Arms and legs are thin, smooth tubes of even thickness, no muscles, no visible elbows or knees. The torso is simple and smooth, no human anatomy.

CHANGES TO THE 3D MODEL
- NO shirt: the torso is bare brown skin, like the arms.
- No trousers: the legs themselves are colored white with a few BROAD yellow and green stripes, as if it is the color of the legs. Thin, smooth and tight like the arms, no loose fabric, no folds, no wide parts, no hems.
- A yellow capoeira cord (cordão) tied around the waist, knotted at the side, the two ends hanging down.
- On both upper arms: a band of the same braided yellow cord, like Muay Thai prajiad but in capoeira style, with a short hanging end.
- Big blue feet with white claws, round brown hands with a white band at the wrist.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO floor, shadow, base, motion lines or effects. One single creature, no extra views.

AVOID
- Human body or proportions, realistic muscles, small hands, a shirt, baggy trousers.
- Not Hitmonchan, Hitmonlee or Machop. No plush toy, chibi or mascot look.
```

## Bijsturing op v3 (zelfde gesprek)
```
Same design, same pose, same colors. Change only these four things: (1) the support arm is too long: make it clearly shorter, so the head and body sit lower, closer to the floor; (2) both hands are plain round balls, perfect spheres with a white wrist band, no fingers, no flat palm, no thumb; (3) the torso is too human: make it one smooth, simple rounded shape like Hitmontop's body, no chest, no nipples, no belly button, no abs, no shoulder blades, no muscle lines; (4) the waist cord is a real capoeira cordão: a thick, tightly braided rope wrapped around the waist, tied in one knot at the side of the hip, the two ends hanging down long, ending in small tassels.
```
