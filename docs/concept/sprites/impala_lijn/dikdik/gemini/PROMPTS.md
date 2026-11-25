# Dikdik (fase 1 impala-lijn, puur Normal): Gemini-prompts
Besluiten en citaten: `docs/concept/IDEEEN.md` → "Impala-lijn"; samenvatting `POKEMON.md` → Impala-lijn.
Vast (Jordi): dikdik → impala → kudu; dikdik puur Normal; "korte houten speren met een metalen uiteinde, niet genoeg om steel te worden"; speerpunt dof ijzer; hoorns overdrijven "zodat ze een beetje afwijken van de dieren ook, maar de inspiratie wel nog kenbaar is"; lichaamskleur brons; echte tekening, bijna effen (traan voor het oog, kuif).
Eigen invulling Claude (niet door Jordi gezegd, schrappen bij twijfel): de soort Kirk-dikdik als anatomie; pose en uitdrukking laat Gemini kiezen.

## r1 (nieuw gesprek, zonder bijlage)
```
Design an original Pokemon. Type: Normal. First stage of a three-stage line (it later evolves into an impala and then a kudu).

Concept: a dik-dik, the tiny African antelope, in Pokemon style. Its two horns ARE short wooden spears: straight spear shafts of wood growing from its head, each ending in a dull iron spearhead. The horns are part of its body, it does not hold or carry anything. The horns are exaggerated: longer and thicker than a real dik-dik's horns, so the design is clearly stylized, but it must still be recognizable as a dik-dik.

Anatomy: a real Kirk's dik-dik (Madoqua kirkii): very small antelope, slender legs with tiny hooves, short stubby tail, large ears, big dark eyes with a pale ring around them, a long soft mobile snout, a tuft of hair (crest) on the forehead between the horns, a dark tear-like gland spot in front of each eye. Drawn as a Pokemon designed by Ken Sugimori: stylized, simplified shapes and clean forms, NOT a realistic animal.

Colors: the fur is a bronze color (warm orange-brown with a bronze tone), but it is normal fur, not metal. Almost no pattern: only the dark tear spot in front of each eye and the crest. Lighter cream belly. Horns: wooden shafts in light brown, spearheads in dull dark iron grey without shine.

Style: official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, dark outline, facing 3/4 to the left, compact composition with the legs close to the body. White background, no ground, no shadow, no effects, no glow.

AVOID: plush toy / Neopets look, Bambi or fawn look, Deerling, Stantler, Sawsbuck, a deer with antlers, armor plates, a metal body, holding or carrying weapons, shiny or glowing metal.
```

## Ronde 1 (25 nov)
- `r1/dikdik_r1.png`. Jordi: "ik vind de speren te lang sowieso, is het lichaam wel brons? en de speerkleur klopt die?"
- Gemeten: lijf #D7874E/#EBA05C (licht oranje-reebruin; brons is dieper, bijv. #CD7F32 met donkere schaduw), schacht #A27D4A, punt #9A928E (dof warmgrijs).
- Jordi: "A, en neem je punten mee": speren ± zo lang als het hoofd; lijf dieper brons; punt koeler/donkerder ijzer; lange beweeglijke snuit; traan voor het oog zichtbaar; kleiner en gedrongener (geen Bambi).

## r2 (nieuw gesprek, zonder bijlage; prompt r1 + alleen deze punten)
```
Design an original Pokemon. Type: Normal. First stage of a three-stage line (it later evolves into an impala and then a kudu).

Concept: a dik-dik, the tiny African antelope, in Pokemon style. Its two horns ARE short wooden spears: straight spear shafts of wood growing from its head, each ending in a dull iron spearhead. Each spear is short: about as long as the head itself, no longer. The horns are part of its body, it does not hold or carry anything. The horns are exaggerated: thicker than a real dik-dik's horns, so the design is clearly stylized, but it must still be recognizable as a dik-dik.

Anatomy: a real Kirk's dik-dik (Madoqua kirkii): a very small, compact antelope with a short rounded body, short slender legs with tiny hooves, short stubby tail, large ears, big dark eyes with a pale ring around them, a tuft of hair (crest) on the forehead between the horns. The most important features of the head: a long, soft, mobile snout that clearly sticks out and droops slightly at the tip (the typical dik-dik nose), and a clearly visible dark tear-like gland spot in front of each eye. Drawn as a Pokemon designed by Ken Sugimori: stylized, simplified shapes and clean forms, NOT a realistic animal.

Colors: the fur is a deep, rich bronze color (like the metal bronze: saturated warm brown-orange with dark warm shadows), but it is normal fur, not metal. Almost no pattern: only the dark tear spot in front of each eye and the crest. Lighter cream belly. Horns: wooden shafts in light brown, spearheads in dull, cool dark iron grey without shine (iron, not stone or flint).

Style: official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, dark outline, facing 3/4 to the left, compact composition with the legs close to the body. White background, no ground, no shadow, no effects, no glow.

AVOID: plush toy / Neopets look, Bambi or fawn look, a deer face with a short muzzle, long thin legs, long spears or antenna-like horns, Deerling, Stantler, Sawsbuck, a deer with antlers, armor plates, a metal body, holding or carrying weapons, shiny or glowing metal.
```

## Ronde 2 (25 nov)
- `r2/dikdik_r2.png`. Gemeten: lijf #E28638, schaduw #CC7728 (te weinig diepte), punt #989CAF (koel ijzer), schacht #CA9F70.
- Claude: speren (± kop) en ijzer goed, snuit langer, traan zichtbaar; lijf nog lang op lange poten en kop kleiner dan r1; brons = feller oranje maar mist donkere schaduw (kan in de spritefase).
- Jordi: "is het voldoende pokemon?" Claude: nee (kop te klein, volwassen verhoudingen, geen uitstraling). Jordi: uitstraling "nieuwsgierig, schrijf de prompt voor ronde 3".

## r3 (nieuw gesprek, zonder bijlage; prompt r2 + alleen verhoudingen en uitstraling)
```
Design an original Pokemon. Type: Normal. First stage of a three-stage line (it later evolves into an impala and then a kudu).

Concept: a dik-dik, the tiny African antelope, in Pokemon style. Its two horns ARE short wooden spears: straight spear shafts of wood growing from its head, each ending in a dull iron spearhead. Each spear is short: about as long as the head itself, no longer. The horns are part of its body, it does not hold or carry anything. The horns are exaggerated: thicker than a real dik-dik's horns, so the design is clearly stylized, but it must still be recognizable as a dik-dik.

PROPORTIONS AND PERSONALITY (most important): this is a first-stage Pokemon, not a realistic animal. Big head, almost as big as the body, with big expressive eyes. Short, round, compact body. Short, simple, slightly sturdy legs with tiny hooves. Simplified, clean shapes. Personality: curious. Show it in the pose and face: head tilted and stretched forward towards something it is investigating, ears perked up and turned forward, eyes wide open with interest, snout sniffing.

Anatomy: based on a real Kirk's dik-dik (Madoqua kirkii): short stubby tail, large ears, big dark eyes with a pale ring around them, a tuft of hair (crest) on the forehead between the horns. The most important features of the head: a long, soft, mobile snout that clearly sticks out and droops slightly at the tip (the typical dik-dik nose), and a clearly visible dark tear-like gland spot in front of each eye. Drawn as a Pokemon designed by Ken Sugimori.

Colors: the fur is a deep, rich bronze color (like the metal bronze: saturated warm brown-orange with dark warm shadows), but it is normal fur, not metal. Almost no pattern: only the dark tear spot in front of each eye and the crest. Lighter cream belly. Horns: wooden shafts in light brown, spearheads in dull, cool dark iron grey without shine (iron, not stone or flint).

Style: official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, dark outline, facing 3/4 to the left, compact composition that fills a square, legs close to the body. White background, no ground, no shadow, no effects, no glow.

AVOID: realistic animal proportions, a small head on a long body, long thin legs, a neutral standing pose, plush toy / Neopets look, Bambi or fawn look, a deer face with a short muzzle, long spears or antenna-like horns, Deerling, Stantler, Sawsbuck, a deer with antlers, armor plates, a metal body, holding or carrying weapons, shiny or glowing metal.
```
- Eigen invulling Claude bij "nieuwsgierig": kop vooruit/schuin, oren naar voren, ogen wijd, snuit snuffelt.

## Ronde 3 (25 nov)
- `r3/dikdik_r3.png`. Gemeten: lijf #9A552F, licht #B06D3D (donker kastanje), punt #848A9D.
- Claude: veel meer Pokémon (grote kop, grote oren, compacter); maar snuit weer kort (reekalf), "traan" is een blauwe druppel onder het oog (leest als huilen), houding nog vrij neutraal; kleur nu te donker/bruin, brons later in de spritefase.

## r3b (bijsturen in hetzelfde gesprek)
```
Keep everything exactly the same (pose, body, head size, ears, horns, colors). Change ONLY the face:
1. Make the snout longer: a long, soft dik-dik nose that clearly sticks out forward and droops slightly at the tip.
2. Remove the blue tear drop under the eye. Instead, add a dark brown spot directly in front of the eye (towards the snout), in the fur color, not a drop, not blue.
```
- `r3b/dikdik_r3b.png`: rest gelijk gebleven; snuit langer met donkere bolle neuspunt; donkere vlek voor het oog. Jordi: "beter?"
