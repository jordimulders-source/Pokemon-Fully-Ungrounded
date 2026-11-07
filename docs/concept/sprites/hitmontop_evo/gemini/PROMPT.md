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
- No shirt, vest, tank top or jacket. No shoes, no hat, no headband.
- Not Hitmonchan, Hitmonlee or Machop. No plush toy, chibi or mascot look.
```

## Tips
- Bijsturen hooguit 1–2 keer met één zin, bijv. `same design, make the stripes wider and fewer`.
- Daarna een nieuw gesprek met de beste versie als bijlage: `Use the attached image as the base design. Keep its pose, proportions and colors. Change only: ...`
- Rondes en Jordi's keuze vastleggen in `README.md` hier; gekozen ontwerp als `../referenties/gemini_gekozen_capoeira.png`.

## Variant B: alleen het hoofd als bijlage (als Gemini weigert)
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
