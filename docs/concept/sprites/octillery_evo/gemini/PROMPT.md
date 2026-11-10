# Gemini-prompts: Octillery-evolutie (10 nov)

Regels: `docs/lessen/GEMINI.md`. Lijn: `docs/concept/POKEMON.md` (Octillery-evolutie).

## Besloten (Jordi, 10 nov)
- Geen oorlogsschip: "het gaat er bij remoraid en octillery om dat ze dingen afschieten"; "ik ben bang dat bij een warship de kanonnen niet pronounced genoeg zijn".
- **Water/Steel**, "maar het moet wel pokemon blijven, dus niet te overdesigned en het moet overduidelijk een evolutie van octillery zijn".
- "hij moet wel sterker worden, dus ook een sterkere look, meer kraken". **Duidelijk groter en zwaarder.**
- **Metaal organisch.** "meer dan 3 kanonnen wordt teveel, of 1 gatling gun en 2 kanonnen".
- Pose driekwart (sprites). De beta-tank (Spaceworld #210) laten we los.
- Twee prompts naast elkaar: **A** = richting 1+2 (gatlingsnuit + twee tentakelkanonnen), **B** = richting 3 (kanonnen op de mantel).
- Keuze Claude in B (Jordi kan bijsturen): de buissnuit van Octillery blijft en telt als kanon, plus 2 op de mantel = 3.

## Bijlagen (beide prompts, in deze volgorde)
1. `bijlage_octillery_8x.png` (Octillery, Gen 3-sprite)
2. `bijlage_remoraid_8x.png` (Remoraid, Gen 3-sprite)

Elke prompt in een **eigen nieuw gesprek**.

## Prompt A: gatlingsnuit + twee tentakelkanonnen

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

ATTACHMENTS
- Attachment 1 is Octillery (Gen 3 sprite). The new Pokémon is its EVOLUTION and must be instantly recognisable as an evolved Octillery.
- Attachment 2 is Remoraid, the first stage. The line is about shooting things: Remoraid is a pistol, Octillery a cannon, this stage is heavy artillery.

THE CREATURE
- Third stage of the line, Water/Steel. A kraken: clearly BIGGER, HEAVIER and STRONGER than Octillery. Broader, taller mantle, thick powerful tentacles that spread out wide and heavy over the ground.
- Keep from Octillery: the round red head/mantle, the heavy-lidded grumpy eyes, the round yellow warts on the head and on the tentacle tips, the red-orange body colour.
- The Steel is ORGANIC: parts of the mantle are covered by smooth gunmetal-grey armour that has grown out of the body like a shell or a thick hide. No bolts, screws, rivets, seams, wires or machine parts. It looks grown, not built.

THE WEAPONS (exactly three, nothing more)
- 1: Octillery's tube snout has grown into a rotary gatling: a short cluster of several barrels grown together around the mouth, made of the same organic gunmetal. It points forward-left. This is the most important feature.
- 2 and 3: the two front tentacles end in one thick cannon barrel each, grown from the tentacle like a shell, with the opening at the tip. They are raised and aimed forward.
- All other tentacles are normal octopus tentacles with the yellow warts at the tips.
- The weapons must be big and clearly readable in the silhouette, but the creature must still look like an animal, not a machine.

POSE AND VIEW
- Body in 3/4 view facing left, sitting heavily on its spread tentacles, gatling and both tentacle cannons aimed forward-left.
- Both eyes visible. Calm and menacing; heavy and unshakable, not angry and not screaming.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO water, splash, ground, rock, shadow or base.
- No muzzle flash, smoke, bullets, ink, glow, sparkles, motion lines, text or effects. One single creature, no extra views.

AVOID
- Not Blastoise, Clawitzer, Tentacruel, Grapploct, Cloyster or a recoloured Octillery.
- Not a robot, mech, tank, ship or submarine: no hull, deck, treads, turrets, chimneys or flags.
- Not over-designed: no spikes, chains, armour everywhere or tiny details. No plush toy, chibi, Neopets or mascot look.
```

## Prompt B: kanonnen op de mantel

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

ATTACHMENTS
- Attachment 1 is Octillery (Gen 3 sprite). The new Pokémon is its EVOLUTION and must be instantly recognisable as an evolved Octillery.
- Attachment 2 is Remoraid, the first stage. The line is about shooting things: Remoraid is a pistol, Octillery a cannon, this stage is heavy artillery.

THE CREATURE
- Third stage of the line, Water/Steel. A kraken: clearly BIGGER, HEAVIER and STRONGER than Octillery. Broader, taller mantle, thick powerful tentacles that spread out wide and heavy over the ground.
- Keep from Octillery: the round red head/mantle, the heavy-lidded grumpy eyes, the round yellow warts on the head and on the tentacle tips, the red-orange body colour.
- The Steel is ORGANIC: parts of the mantle are covered by smooth gunmetal-grey armour that has grown out of the body like a shell or a thick hide. No bolts, screws, rivets, seams, wires or machine parts. It looks grown, not built.

THE WEAPONS (exactly three, nothing more)
- 1: Octillery's tube snout stays, bigger and thicker, with a gunmetal rim grown around the opening, pointing forward-left.
- 2 and 3: two thick cannon barrels grow out of the top of the mantle, one on each side, like horns made of the same organic gunmetal, both aimed forward. They grow from the body, they are not mounted turrets.
- All tentacles are normal octopus tentacles with the yellow warts at the tips; no weapons on the tentacles.
- The weapons must be big and clearly readable in the silhouette, but the creature must still look like an animal, not a machine.

POSE AND VIEW
- Body in 3/4 view facing left, sitting heavily on its spread tentacles, snout and both mantle cannons aimed forward-left.
- Both eyes visible. Calm and menacing; heavy and unshakable, not angry and not screaming.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO water, splash, ground, rock, shadow or base.
- No muzzle flash, smoke, bullets, ink, glow, sparkles, motion lines, text or effects. One single creature, no extra views.

AVOID
- Not Blastoise, Clawitzer, Tentacruel, Grapploct, Cloyster or a recoloured Octillery.
- Not a robot, mech, tank, ship or submarine: no hull, deck, treads, turrets, chimneys or flags.
- Not over-designed: no spikes, chains, armour everywhere or tiny details. No plush toy, chibi, Neopets or mascot look.
```

## Rondes
- **r1 (10 nov):** `r1_A_gatling.png`, `r1_B_mantel.png`. Jordi: "Beide echt slecht, is gewoon octillery met wat kanonnen". Jordi stuurde géén bijlagen mee ("dat is het ironische"); de tekst "keep from Octillery" + de opsomming van Octillery-kenmerken was genoeg om Octillery na te tekenen met wapens en een helm erop. Jordi: "Ik wil dat die meer kraken wordt. Maar ook echt een oorlogswapen. Het steel gedeelte moet natuurlijk zijn, hier lijkt het erop geplakt. Dat is bij een Empoleon bijv ook niet". Verder met richting A.

- **r2 (10 nov):** `r2_A2.png` (prompt A2). Jordi: "nog steeds lelijk, nu is die wat meer een kraken vorm, maar het lijkt echt heel goedkoop, wat metaal erop geplakt en voor de rest echt precies octillery". Twee rondes mis → stoppen, eerst overleggen.

## Prompt A2 (na r1; richting A, meer kraken, oorlogswapen, steel als anatomie zoals Empoleon)
Keuzes Claude (Jordi kan schrappen): mantel langgerekt als bij een inktvis met twee stalen vinnen bovenaan (leest als granaat/torpedo); de snuit = de sifon (waarmee inktvissen echt water spuiten) die een gatling is.

```
Design an original Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

THE IDEA
- The final evolution of the Remoraid line, Water/Steel. Remoraid is a pistol, Octillery a cannon; this stage is a living weapon of war: a KRAKEN, the giant sea monster that drags warships down, grown into heavy artillery.
- This is NOT Octillery with weapons added. The whole body has changed into a new, much bigger and more dangerous animal. Only the red colour, the heavy-lidded half-closed eyes and a few round yellow warts tell you it evolved from Octillery.

ANATOMY (a giant squid / kraken)
- A long, tall, torpedo-shaped mantle that rises up and back behind the head, like a giant squid, ending in two broad fins at the top.
- Long, thick, muscular tentacles, much longer than the body is tall. Several of them rise up and curl in the air around the body like a sea monster rising from the deep; the others brace heavily on the ground.
- Big, heavy and powerful. Menacing and calm, not screaming, not angry.

THE STEEL IS PART OF THE BODY (like Empoleon's steel beak and wing edges)
- No armour, helmet, plates or casing laid over the body. Only these body parts ARE steel, dark gunmetal with a blue sheen, and they keep the natural shape of that body part, flowing smoothly into the red flesh:
  - the siphon/snout in front of the face (the tube squids use to jet water) has grown into a rotary gatling of several barrels, pointing forward-left. The most important feature;
  - the two fins at the top of the mantle, shaped like the tail fins of a torpedo or artillery shell;
  - the ends of the two front tentacles, which have hardened into one thick cannon barrel each, the opening at the tip, raised and aimed forward. The tentacle itself becomes the barrel; nothing is attached to it.
- Exactly three weapons: the gatling and the two tentacle cannons. No other guns.

POSE AND VIEW
- 3/4 view facing left, towering up, weapons aimed forward-left. Both eyes visible.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO water, splash, ground, rock, shadow or base.
- No muzzle flash, smoke, bullets, ink, glow, sparkles, motion lines, text or effects. One single creature, no extra views.

AVOID
- Not Octillery with a helmet or guns stuck on. Not Blastoise, Clawitzer, Tentacruel, Grapploct, Malamar or Cloyster.
- Not a robot, mech, tank, ship or submarine: no hull, deck, treads, turrets, bolts, rivets, seams or flags.
- Not over-designed: no spikes, chains or tiny details. No plush toy, chibi, Neopets or mascot look.
```

## Na r2: nieuwe aanpak (Jordi, 10 nov)
- Jordi: "pokemon zijn niet dieren met wapens erop geplakt, ze zijn vaak op handige manieren onderdeel van het lichaam. Je moet de prompt anders schrijven want gemini moet juist ontwerpen, niet ik, doe maar humboldt ipv kraken, is wat meer gedefinieerd. En de gatling gun mag gewoon organisch eruitzien, de kanonnen moeten ook wat meer onderdeel van de tentakels. Hij moet verder op een mooie manier bepantserd zijn, zoals bij andere pokemon steel types".
- Anatomie: **Humboldtinktvis** (*Dosidicus gigas*, "diablo rojo", Peru/Chili): pijlvormige mantel met grote driehoekige vinnen aan de punt, grote ogen, 8 armen + **2 lange vangtentakels met verdikte knots** (→ de twee kanonnen, natuurlijk onderdeel van de tentakels), **sifon/trechter** voor straalaandrijving (→ de organische gatling), papegaaiachtige snavel, flitst rood/wit, jaagt in groepen.
- Steel-voorbeelden (types gecontroleerd in de repo): Empoleon (Water/Steel; snavel, kroon en vleugelranden zíjn staal), Corviknight (veren als platen van een harnas), Aggron (platen op kop en rug volgen de lichaamsvorm, grijs pantser op donker lijf), Scizor (scharen zijn het wapen en het pantser), Skarmory (veren zijn bladen), Kingambit (de bladen zijn het lijf), Steelix (gesegmenteerd lijf). Bij ons ook Blastoise Water/Steel (kanonnen uit het schild). Wapen als lichaamsdeel: Clawitzer (Water; de schaar is het kanon).
- Prompt-aanpak: Gemini krijgt een ontwerpopdracht (probleem + principes + voorbeelden), geen onderdelenlijst; geen woorden als "gatling"/"barrel".

## Prompt A3

```
You are a Pokémon designer at Game Freak. Design a new Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art). You make the design decisions; below are the brief and the design rules.

THE BRIEF
- The final evolution of the Remoraid line: Remoraid (a fish that is a pistol) evolves into Octillery (an octopus that is a cannon), and this third stage is heavy artillery. Water/Steel.
- Animal: the Humboldt squid ("diablo rojo") from the Pacific coast of Peru and Chile: an arrow-shaped mantle with large triangular fins at the tip, big eyes, a powerful beak, eight arms plus two long hunting tentacles with thickened clubs at the ends, and a siphon it uses to shoot jets of water. A fierce pack hunter that flashes red.
- It must be bigger, heavier and clearly stronger than Octillery, and read as its evolution at a glance (red body, round yellow warts on the arms). It is not Octillery with things added: design a new face and body.

DESIGN RULES
- Pokémon are never animals with weapons attached. The weapon IS a body part that grows naturally out of the animal's anatomy, the way Clawitzer's claw is its cannon, Blastoise's cannons grow from its shell and Scizor's pincers are both its weapon and its armour.
- Use the squid's own anatomy for the three weapons: its siphon becomes a multi-barrel rapid-fire organ that still looks organic, and its two long hunting tentacles become its two cannons, with the club itself forming the cannon. No other weapons.
- The Steel type is beautiful armour that follows the body, as in Steel-type Pokémon: Empoleon's steel beak, crown and wing edges, Corviknight's feathers like plates of a knight's armour, Aggron's plates following the shape of its head and back. Hard, polished, dark steel on the parts of a squid that would naturally be hard or protective (for example the fins, the mantle or the arm edges), flowing into the red flesh. Never a helmet, casing or plates stuck on top.
- Keep it clean and readable like a real Pokémon: a few strong shapes, not over-designed.

POSE AND VIEW
- 3/4 view facing left, the full body visible, the three weapons aimed forward-left. Both eyes visible. Calm, confident and dangerous; not screaming.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO water, splash, ground, rock, shadow or base.
- No muzzle flash, smoke, bullets, ink, glow, sparkles, motion lines, text or effects. One single creature, no extra views.

AVOID
- Real-world guns or machine parts: no gatling cylinders, pipes, collars, bolts, rivets, seams or screws.
- Not a robot, mech, tank, ship or submarine. Not Octillery's face, not Malamar, Tentacruel, Grapploct or Clawitzer.
- No plush toy, chibi, Neopets or mascot look.
```

- **r3 (10 nov):** `r3_A3.png` (prompt A3). Jordi: "beter qua vorm en anatomie, alleen hij blijft gewoon geweren erop zetten, voor de tentakels vind ik het best prima, maar de rest moet organischer". → r3 als bijlage in een nieuw gesprek (Gemini verbetert slecht in hetzelfde gesprek): vorm, anatomie en tentakelkanonnen blijven; sifonwapen en pantser organisch.

## Prompt A4 (bijlage: `r3_A3.png`, nieuw gesprek)

```
You are a Pokémon designer at Game Freak. The attached image is your previous draft of a new Pokémon: the final evolution of Remoraid and Octillery, a Water/Steel Humboldt squid that is living heavy artillery. Draw an improved version as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art).

KEEP FROM THE DRAFT
- The body shape, anatomy, proportions and pose: the arrow-shaped mantle with the large steel fin at the tip, the eye, the arms with yellow warts and steel hooks, the red colour.
- The two long hunting tentacles with cannons at the ends: these are good, keep them as they are.

CHANGE: IT STILL LOOKS LIKE GUNS AND ARMOUR WERE PUT ON A SQUID
- The weapon under the head is a real-world gatling gun with a collar: remove it. Instead the squid's own siphon (the funnel it shoots water jets from) has grown into several fleshy tubes fused side by side, like Octillery's tube mouth multiplied, made of the same red flesh with hard dark steel only at the rims of the openings. It must look grown, like part of the animal.
- The grey plates on the mantle and around the eye look like a helmet: remove them. The steel must be seamless and grown, like a nautilus shell, a beetle's shell or Empoleon's steel beak and crown: smooth polished dark steel flowing out of the red skin in one or two clean shapes that follow the curve of the mantle. No segments, plate edges, bolts, rivets, seams or machine parts anywhere.
- Everything that is not the two tentacle cannons must read as a living animal.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- 3/4 view facing left, full body visible. Plain white background. NO water, splash, ground, shadow or base.
- No muzzle flash, smoke, bullets, ink, glow, sparkles, motion lines, text or effects. One single creature, no extra views.

AVOID
- Gatling cylinders, pipes, collars, helmets, armour plates, bolts or screws.
- Not a robot, mech or submarine. Not Octillery's face, not Malamar, Tentacruel or Clawitzer.
```

- **r4 (10 nov):** `r4_A4.png` (prompt A4 met r3 als bijlage). Jordi: "veel slechter". Claude: tentakels werden dunne zwepen met losse buisjes (ondanks "keep"), lijf kleiner en lichter, sifon werd een ring donuts voor het gezicht, mantelstaal werd één grote kap. r3 blijft de beste.

## Na r4 (Jordi, 10 nov)
- "ja pak prompt a3, belangrijk is nog wel dat het een gen 3 sprite wordt, want deze is te breed horizontaal. Steel pokemon hebben eigenlijk vrijwel nooit stukken stalen platen zoals je hier kan zien, het staal is juist fysiologisch onderdeel van het lichaam, of left to the imagination. Laten we daarom voor nu gaan voor texturen die op bepantsering duiden, maar geen stalen platen. De gatling gun moet een octopus mond zijn met een andere vorm, zoals bij octillery het ook een soort kanon is, maar wel rood."
- Jordi's overzicht van Steel-Pokémon: `../referenties/steel_pokemon_overzicht.webp`.

## Prompt A5 (A3 aangepast, geen bijlage, nieuw gesprek)

```
You are a Pokémon designer at Game Freak. Design a new Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art). You make the design decisions; below are the brief and the design rules.

THE BRIEF
- The final evolution of the Remoraid line: Remoraid (a fish that is a pistol) evolves into Octillery (an octopus that is a cannon), and this third stage is heavy artillery. Water/Steel.
- Animal: the Humboldt squid ("diablo rojo") from the Pacific coast of Peru and Chile: an arrow-shaped mantle with large triangular fins at the tip, big eyes, eight arms plus two long hunting tentacles with thickened clubs at the ends. A fierce pack hunter that flashes red.
- It must be bigger, heavier and clearly stronger than Octillery, and read as its evolution at a glance (red body, round yellow warts on the arms). It is not Octillery with things added: design a new face and body.

DESIGN RULES
- Pokémon are never animals with weapons attached. The weapon IS a body part that grows naturally out of the animal's anatomy, the way Clawitzer's claw is its cannon.
- Three weapons, no others:
  - its mouth is the rapid-fire weapon: a red octopus mouth that is a kind of cannon, like Octillery's tube mouth, but with a different shape;
  - its two long hunting tentacles are its two cannons, with the club itself forming the cannon.
- The Steel type is part of the body's physiology, as with Steel-type Pokémon like Aggron, Steelix, Metagross, Mawile, Scizor and Empoleon, or left to the imagination. Here it is shown only through textures on the body that suggest armour. NO steel plates, no grey metal pieces, no helmet, no casing.
- Keep it clean and readable like a real Pokémon: a few strong shapes, not over-designed.

POSE AND SIZE
- A real Gen 3 sprite composition: the whole creature fits compactly in a square 64x64 frame, about as tall as it is wide. NOT a wide horizontal picture: the arms and tentacles curl close around the body instead of stretching out to the sides.
- 3/4 view facing left, mouth and both tentacle cannons aimed forward-left. Both eyes visible. Calm, confident and dangerous; not screaming.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO water, splash, ground, rock, shadow or base.
- No muzzle flash, smoke, bullets, ink, glow, sparkles, motion lines, text or effects. One single creature, no extra views.

AVOID
- Real-world guns or machine parts: no gatling cylinders, pipes, collars, bolts, rivets, seams, screws or metal plates.
- Not a robot, mech, tank, ship or submarine. Not Octillery's face, not Malamar, Tentacruel, Grapploct or Clawitzer.
- No plush toy, chibi, Neopets or mascot look.
```

- **r5 (10 nov):** `r5_A5.png` (prompt A5). Jordi: "juist, nu komen we ergens. Ik zou hem nog wat meer uitgestrekt willen hebben, nu is het wat meer een bal. de mond vind ik nog net niet gattling gun genoeg, maar misschien kan gemini dat niet. De pose zou ik zodanig willen dat de tentakels die kunnen schieten op schouderhoogte zitten. Dan zou het wel kunnen dat we 2 tentakels als rupsbanden maken. Dus 2 zijn rupsbanden, 2 zijn kanonnen, en de voorste twee zijn reguliere tentakels"

## Prompt A6 (A5 aangepast, geen bijlage, nieuw gesprek)

```
You are a Pokémon designer at Game Freak. Design a new Pokémon and draw it as an official Gen 3 front sprite (Ruby/Sapphire/Emerald style pixel art). You make the design decisions; below are the brief and the design rules.

THE BRIEF
- The final evolution of the Remoraid line: Remoraid (a fish that is a pistol) evolves into Octillery (an octopus that is a cannon), and this third stage is heavy artillery. Water/Steel.
- Animal: the Humboldt squid ("diablo rojo") from the Pacific coast of Peru and Chile: a long arrow-shaped mantle with large triangular fins at the tip, big eyes, arms and long hunting tentacles. A fierce pack hunter that flashes red.
- It must be bigger, heavier and clearly stronger than Octillery, and read as its evolution at a glance (red body, round yellow warts on the arms). It is not Octillery with things added: design a new face and body.

DESIGN RULES
- Pokémon are never animals with weapons attached. Every weapon IS a body part that grows naturally out of the animal's anatomy, the way Clawitzer's claw is its cannon.
- Its mouth is a rapid-fire weapon like a gatling gun, but made of red flesh: several fleshy red tubes grown together in a ring around the mouth, an octopus mouth that is clearly a multi-barrel gun. Like Octillery's tube mouth, but evolved.
- Its arms have three roles:
  - two arms are its tank treads: they run under the body in long flat loops and it rolls on them like a tank, still clearly red squid arms;
  - two long tentacles are its two cannons, with the club at the end forming the cannon. They come out at shoulder height, beside the head, and are aimed forward like the guns of a tank;
  - the two front arms are regular tentacles.
- The Steel type is part of the body's physiology, as with Steel-type Pokémon like Aggron, Steelix, Metagross, Mawile, Scizor and Empoleon. Here it is shown only through textures on the body that suggest armour. NO steel plates, no grey metal pieces, no helmet, no casing.
- Keep it clean and readable like a real Pokémon: a few strong shapes, not over-designed.

POSE AND SIZE
- The body is stretched out and long, the mantle reaching back and up like a long arrow; NOT rolled up into a ball.
- Still a real Gen 3 sprite composition: the whole creature fits in a 64x64 frame, a little wider than tall at most, not a wide horizontal picture.
- 3/4 view facing left, mouth and both tentacle cannons aimed forward-left. Both eyes visible. Calm, confident and dangerous; not screaming.

STYLE AND FORMAT
- 64x64 pixel sprite, max 16 colors, 1 px dark outline, light from top left, clean shading like official Game Freak Gen 3 sprites.
- Plain white background. NO water, splash, ground, rock, shadow or base.
- No muzzle flash, smoke, bullets, ink, glow, sparkles, motion lines, text or effects. One single creature, no extra views.

AVOID
- Real-world guns or machine parts: no metal gatling cylinders, pipes, collars, bolts, rivets, seams, screws, metal plates or metal tank treads.
- Not a robot, mech, tank, ship or submarine. Not Octillery's face, not Malamar, Tentacruel, Grapploct or Clawitzer.
- No plush toy, chibi, Neopets or mascot look.
```
