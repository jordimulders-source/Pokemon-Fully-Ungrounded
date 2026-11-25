# Impala (fase 2 impala-lijn, Normal/Steel): Gemini-prompts
Besluiten en citaten: `docs/concept/IDEEEN.md` → "Impala-lijn"; samenvatting `POKEMON.md` → Impala-lijn. Fase 1: `../../dikdik/` (prompt r3 werkte: Pokémon-verhoudingen bovenaan).
Vast (Jordi): Normal/Steel; "hoorns echt van metaal"; hoornvorm van het echte dier blijft kloppen; overdrijven "zodat ze een beetje afwijken van de dieren ook, maar de inspiratie wel nog kenbaar is"; lichaamskleur zilver ("lichaamskleur he"); hoorns gepolijst staal; echte tekening: scherpe tweedeling rug/flank/buik + zwarte M + plukjes.
Eigen invulling Claude (niet door Jordi gezegd, schrappen bij twijfel):
- Soort: mannetjesimpala (*Aepyceros melampus*), want alleen die heeft hoorns. Ribbels op de hoorns weggelaten (kans op ruis), alleen de liervorm genoemd.
- Verhoudingen: "middenfase, Pokémon, geen realistisch dier" (les uit dikdik r1–r3); pose en uitdrukking laat Gemini kiezen (geen uitstraling van Jordi voor de impala).
- Zilveren vacht en stalen hoorns lezen anders: vacht mat, hoorns met harde glans (anders vloeien ze samen).
- Driekwart naar links met de achterhand zichtbaar: de zwarte M zit op het achterwerk (staart + dijen) en valt anders weg.

## r1 (nieuw gesprek, zonder bijlage)
```
Design an original Pokemon. Type: Normal/Steel. Second stage of a three-stage line (it evolves from a dik-dik and later evolves into a kudu).

Concept: a male impala, the African antelope, in Pokemon style. Its horns are real metal: polished steel, growing from its head as part of its body. They keep the typical impala horn shape: lyre-shaped, sweeping back, then out, then up. The horns are clearly exaggerated (longer and more dramatic than a real impala's), so the design is stylized, but it must still be recognizable as an impala. It does not hold or carry anything.

PROPORTIONS (most important): this is a Pokemon, not a realistic animal. Stylized, simplified, clean shapes, drawn as a Pokemon designed by Ken Sugimori. Middle stage: slimmer and more athletic than a cute first stage, but with a head big enough to read clearly in a small sprite.

Anatomy: based on a real male impala (Aepyceros melampus): slender athletic body, long slender legs with small hooves, large ears, big dark eyes, slim muzzle.

Colors and pattern: the fur is silver (normal fur, matte, not metal), with the real impala pattern made sharper and bolder: a sharp three-tone split with a dark silver back, a lighter silver flank and a white belly, with clean hard edges between the bands. A black "M" on the rump (black vertical stripes on the tail and on the back of each thigh). Black tufts of hair just above the hind hooves. Horns: polished steel, clearly different from the fur: brighter, with hard shine and strong highlights.

Style: official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, dark outline, facing 3/4 to the left with the body turned so the hindquarters with the black M are visible, compact composition that fills a square. White background, no ground, no shadow, no effects, no glow.

AVOID: realistic animal proportions, a deer with antlers, Deerling, Sawsbuck, Stantler, Wyrdeer, armor plates, a metal body, robot parts, holding or carrying weapons, glowing metal, horns that blend into the fur.
```

## Ronde 1 (25 nov)
- `r1/impala_r1.png`. Gemeten: vacht #82888D–#B2B6BC (grijs, weinig verschil tussen de banden), hoorns #59636B (zelfde grijs als de vacht, nauwelijks glans).
- Jordi: "not bad, maar het is iets teveel een gekleurd dier, nog niet genoeg pokemon, ook meer een hert dan echt impala denk ik, wat betreft lichaam en hoorns, genoeg verschil denk je?"; daarna: "misschien de oren ietsje groter".
- Claude: niet genoeg verschil. Hoorns staan bijna recht omhoog met een kleine knik (gazelle/hert), geen lier; kop klein op een lange hals, lijf als een ree; drieslag nauwelijks zichtbaar (geen witte buik, geen harde randen); de M staat als letter op de dij; hoorns grijs als de vacht.

## r2 (nieuw gesprek, zonder bijlage; prompt r1 + alleen deze punten)
- Eigen invulling Claude: hoe de lier eruitziet (beschrijving van een echte impalahoorn), de M als strepen in plaats van letter, meer Pokémon via verhoudingen zoals bij dikdik r3 (grote kop, grote ogen, compacter lijf), alleen pose/uitstraling niet ingevuld.
```
Design an original Pokemon. Type: Normal/Steel. Second stage of a three-stage line (it evolves from a dik-dik and later evolves into a kudu).

Concept: a male impala, the African antelope, in Pokemon style. Its horns are real metal: polished steel, growing from its head as part of its body. They must have the real impala horn shape, NOT deer or gazelle horns: from the base they rise up and lean back, then spread wide outward to the sides, then the tips turn up and forward again. Seen from the front the pair forms a wide lyre; seen from the side each horn is an S-curve. The horns are clearly exaggerated (bigger, wider and more dramatic than a real impala's), so the design is stylized, but it must still be recognizable as an impala. It does not hold or carry anything.

PROPORTIONS (most important): this is a Pokemon, not a realistic animal and not a recolored animal. Drawn as a Pokemon designed by Ken Sugimori: stylized, simplified, bold shapes. Big head with big expressive eyes, ears a bit bigger than a real impala's, short neck, compact athletic body, legs slender but not long and stilt-like. Middle stage: more athletic than a cute first stage, but clearly a Pokemon.

Anatomy: based on a real male impala (Aepyceros melampus), not a deer: compact, muscular antelope body with a deep chest and a slightly raised rump, small hooves, large ears, big dark eyes, slim muzzle.

Colors and pattern: the fur is silver (normal fur, matte, not metal), with the real impala pattern made sharper and bolder: three clearly different bands with hard clean edges: dark silver back (a saddle), much lighter silver flank, pure white belly. The black "M" is NOT a letter: it is three black vertical stripes, one down the middle of the tail and one down the back edge of each thigh, which together read as an M from behind. Black tufts of hair on the back of the hind legs just above the hooves. Horns: polished steel, clearly different from the fur: brighter, with hard shine, strong white highlights and dark reflections.

Style: official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, dark outline, facing 3/4 to the left with the body turned so the hindquarters with the black stripes are visible, compact composition that fills a square. White background, no ground, no shadow, no effects, no glow.

AVOID: deer, roe deer, gazelle, realistic animal proportions, a small head on a long neck, long stilt legs, a recolored real animal, straight or upright horns, a letter M, Deerling, Sawsbuck, Stantler, Wyrdeer, armor plates, a metal body, robot parts, holding or carrying weapons, glowing metal, horns in the same grey as the fur.
```

## Ronde 2 (25 nov)
- `r2/impala_r2.png`. Claude: drieslag nu zichtbaar (witte borst/buik, donkere zadel), hoorns lichter met glans; maar hoorns nog steeds omhoog met knik naar voren (geen wijde lier), kop klein op lange hals, lange poten (nog steeds hert), M nog als letter, oren nauwelijks groter.
- Jordi: "de impala moet stoicijns zijn, misschien iets meer in een protector houding pose".

## r3 (nieuw gesprek, zonder bijlage; prompt r2 + uitstraling/pose; M en hoorns scherper gezegd)
- Eigen invulling Claude bij "stoicijns" en "protector houding": kalme, ernstige, onbewogen blik; stevig geplante poten, borst vooruit, kop hoog, alsof hij iets achter zich beschermt.
```
Design an original Pokemon. Type: Normal/Steel. Second stage of a three-stage line (it evolves from a dik-dik and later evolves into a kudu).

Concept: a male impala, the African antelope, in Pokemon style. Its horns are real metal: polished steel, growing from its head as part of its body. They must have the real impala horn shape, NOT deer or gazelle horns: from the base they rise up and lean back, then spread wide outward to the sides, then the tips turn up and forward again. Seen from the front the pair forms a wide lyre; seen from the side each horn is an S-curve. The horns are clearly exaggerated (bigger, wider and more dramatic than a real impala's), so the design is stylized, but it must still be recognizable as an impala. It does not hold or carry anything.

PROPORTIONS AND PERSONALITY (most important): this is a Pokemon, not a realistic animal and not a recolored animal. Drawn as a Pokemon designed by Ken Sugimori: stylized, simplified, bold shapes. Big head with big expressive eyes, ears clearly bigger than a real impala's, short thick neck, compact athletic body, legs slender but not long and stilt-like. Middle stage: more athletic than a cute first stage, but clearly a Pokemon. Personality: stoic. Calm, serious, unmoved expression. Pose: a protector stance, as if it stands guard in front of something it protects: legs planted firmly and wide, chest out, head held high.

Anatomy: based on a real male impala (Aepyceros melampus), not a deer: compact, muscular antelope body with a deep chest and a slightly raised rump, small hooves, big dark eyes, slim muzzle.

Colors and pattern: the fur is silver (normal fur, matte, not metal), with the real impala pattern made sharper and bolder: three clearly different bands with hard clean edges: dark silver back (a saddle), much lighter silver flank, pure white belly. On the rear: three separate, parallel black vertical stripes, one down the middle of the tail and one down the back edge of each thigh (no letter, no M shape drawn on the side). Black tufts of hair on the back of the hind legs just above the hooves. Horns: polished steel, clearly different from the fur: brighter, with hard shine, strong white highlights and dark reflections.

Style: official Gen 3 front sprite (Ruby/Sapphire/Emerald style), 64x64, max 16 colors, dark outline, facing 3/4 to the left with the body turned so the hindquarters with the black stripes are visible, compact composition that fills a square. White background, no ground, no shadow, no effects, no glow.

AVOID: deer, roe deer, gazelle, realistic animal proportions, a small head on a long neck, long stilt legs, a recolored real animal, straight or upright horns, horns bending forward, a letter M on the side, a cute or playful pose, an aggressive charging pose, Deerling, Sawsbuck, Stantler, Wyrdeer, armor plates, a metal body, robot parts, holding or carrying weapons, glowing metal, horns in the same grey as the fur.
```

## Ronde 3 (25 nov)
- `r3/impala_r3.png`. Claude: hoorns nu echt staal met glans; drieslag en houding (stoïcijns, poten geplant) beter; maar oog klein en realistisch (amandelvorm, geen glimlicht), kop nog klein t.o.v. het lijf, hoorns nog geen wijde lier, de M is nu 4 strepen op de zijkant van de bil (leest als kudu/zebra).
- Jordi: "is nog net iets teveel een dier en geen pokemon he, misschien door het oog?"

## r3b (bijsturen in hetzelfde gesprek, zoals dikdik r3b)
- Regel 1 = Jordi (oog). Regels 2–4 = voorstel Claude, alleen meesturen als Jordi ze wil.
```
Keep everything exactly the same (pose, body, horns, colors, pattern). Change ONLY:
1. The eye: make it a Pokemon eye, not a realistic animal eye: clearly bigger, rounder, a large dark iris that fills most of the eye, a clear white highlight, and a bold dark outline. Keep the calm, serious, stoic expression.
2. The head: make it bigger relative to the body (Pokemon proportions).
3. The rear stripes: remove the stripes on the side of the haunch. Instead: one black stripe down the middle of the tail and one black stripe along the back edge of the thigh only.
4. The horns: same steel, but shaped as a wide lyre: from the base up and back, then spreading wide outward, then the tips turn up and forward.
```
- Verstuurd met regels 1–4. `r3b/impala_r3b.png`: oog groter en rond (anime-achtig), staartstreep goed; kop niet groter, hoorns onveranderd (zie GEMINI.md: bijsturen werkt hooguit 1–2 keer).
- Jordi: "niet beter"; "anders moeten wij maar een oog maken".
